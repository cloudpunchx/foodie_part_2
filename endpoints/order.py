from app import app
import bcrypt
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data

# NOT TESTED:
# GET Order Information
@app.get('/api/order')
def get_order_information():
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
    menuId = request.json.get('menuId')
    keys = ["orderId", "clientId", "restaurantId", "is_confirmed", "is_complete", "is_cancelled", "created_at"]
    response = []
    result = run_statement('CALL get_orders(?,?)', [token, menuId])
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
    required_data = ['token', 'restaurantId', 'items']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    token = request.json.get('token')
    restaurantId = request.json.get('restaurantId')
    items = request.json.get('items')
    result = run_statement("CALL create_order(?,?,?)", [token, restaurantId, items])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Successfully Sent Order"), 200)
        elif result[0][0] == 0:
            return make_response(jsonify("Error: Order was not sent, please try again."), 500)
    else:
        return make_response(jsonify(result), 500)
