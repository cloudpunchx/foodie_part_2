from app import app
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data

# GET Orders
@app.get('/api/order')
def get_client_order_information():
    """
    Expects Arg:
    token
    Optional:
    orderId
    """
    required_data = ['token']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    token = request.json.get('token')
    orderId = request.args.get('orderId')
    if (orderId == None):
        orderId = None
    keys = ["orderId", "clientId", "restaurantId", "is_confirmed", "is_complete", "is_cancelled", "created_at", "item"]
    response = []
    result = run_statement('CALL get_orders(?,?)', [token, orderId])
    if(type(result) == list):
        for order in result:
            response.append(dict(zip(keys, order)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(response), 500)

# POST Order
@app.post('/api/order')
def create_order():
    """
    Expects 3 Args:
    token, restaurantId, items(array)
    """
    required_data = ['token', 'restaurantId']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    token = request.json.get('token')
    restaurantId = request.json.get('restaurantId')
    result = run_statement("CALL create_order(?,?)", [token, restaurantId])
    if (type(result) == list):
        orderId = result[0][0]
        items = request.json.get('items')
        for item in items:
            result = run_statement("CALL add_to_order(?,?)", [item, orderId])
            if (type(result) == list):
                if result[0][0] == 1:
                    return make_response(jsonify(f"Successfully Sent Order {orderId} to Restaurant"), 200)
                elif result[0][0] == 0:
                    return make_response(jsonify("Error: Order was not sent, please try again."), 500)
    elif "orders_FK_restaurant" in result:
        return make_response(jsonify("Error: Restaurant ID does not exist."), 404)
    else:
        return make_response(jsonify(result), 500)

# PATCH Order 
@app.patch('/api/order')
def update_order_status():
    """
    Expects 2 Args:
    token, orderId
    Client Optional:
    cancelOrder
    Restaurant Optional (only one of these is allowed at a time):
    confirmOrder, completeOrder
    """
    required_data = ['token', 'orderId']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    token = request.json.get('token')
    orderId = request.json.get('orderId')
    cancelOrder = request.json.get('cancelOrder')
    if (cancelOrder == ""):
        cancelOrder = "0"
    confirmOrder = request.json.get('confirmOrder')
    if (confirmOrder == ""):
        confirmOrder = "0"
    completeOrder = request.json.get('completeOrder')
    if (completeOrder == ""):
        completeOrder = "0"
    result = run_statement("CALL update_order_status(?,?,?,?,?)", [token, orderId, cancelOrder, confirmOrder, completeOrder])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Successfully Updated Order Status."), 200)
        elif result[0][0] == 0:
            return make_response(jsonify("Error: Order Status was not updated, please try again."), 500)
    else:
        return make_response(jsonify(result), 500)