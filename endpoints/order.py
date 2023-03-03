from app import app
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data

    # GET
    #Run procedure, either get ALL (one for restaurant, one for customer algorithm is the same)
    # run in either pass to it an order id and it only retrieves the single order,
    # or retrieve all orders that belong to either client or restaurant
    # with optional params, have the parameter declared in procedure regardless, if you don't want it active, pass null to it, in the procedure
    # if the order id input is = null, then get all orders
    # if its not null then run select with the param 
    # since select will have multi rows for the same order, ORDER BY order Id (id of the orders table) ASC OR DESC doesn't matter (append an item to items array)
    # procedure will return them in separate rows but we need to group them together (one object for order #5 with a list that holds all the items, iterate and double check, if you changed an order)

# Currently WORKING for client GET with and without param OrderId
# GET Client ONLY Order Information with optional OrderId
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
    keys = ["orderId", "clientId", "restaurantId", "is_confirmed", "is_complete", "is_cancelled", "created_at"]
    response = []
    result = run_statement('CALL get_orders(?,?)', [token, orderId])
    if(type(result) == list):
        for order in result:
            response.append(dict(zip(keys, order)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(response), 500)



# NOT TESTED:
# GET Order Information
# @app.get('/api/order')
# def get_order_information():
#     """
#     Expects Arg:
#     token
#     Optional:
#     orderId
#     """
#     required_data = ['token']
#     check_result = check_data(request.json, required_data)
#     if check_result != None:
#         return check_result
#     token = request.json.get('token')
#     orderId = request.args.get('orderId')
#     keys = ["orderId", "clientId", "restaurantId", "is_confirmed", "is_complete", "is_cancelled", "created_at"]
#     response = []
#     result = run_statement('CALL get_orders(?,?)', [token, orderId])
#     if(type(result) == list):
#         for order in result:
#             response.append(dict(zip(keys, order)))
#         return make_response(jsonify(response), 200)
#     else:
#         return make_response(jsonify(response), 500)


    # post order: 
    # procedure that creates order, attaches order to restaurant and person
    # returns the order ID
    # need that in next steps
    # then use 2nd procedure, add single item to an order, add 1 row to the order item table (takes order id and item id, maps one to the other)
    # with those 2 procedures, run a loop thru items array that has numbers of items (after you created the order, iterate through array and add items to order)
    # LOOP IS DONE IN PYTHON 



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
        items = request.json.get('items')
        for item in items:
            result = run_statement("CALL add_to_order(?,?)", [result[0][0], item])
            if (type(result) == list):
                if result[0][0] == 1:
                    return make_response(jsonify("Successfully Sent Order to Restaurant"), 200)
                elif result[0][0] == 0:
                    return make_response(jsonify("Error: Order was not sent, please try again."), 500)
    elif "orders_FK_restaurant" in result:
        return make_response(jsonify("Error: Restaurant ID does not exist."), 404)
    else:
        return make_response(jsonify(result), 500)

# VERSION WITH orderId variable set instead of result[0][0]
# @app.post('/api/order')
# def create_order():
#     """
#     Expects 3 Args:
#     token, restaurantId, items(array)
#     """
#     required_data = ['token', 'restaurantId']
#     check_result = check_data(request.json, required_data)
#     if check_result != None:
#         return check_result
#     token = request.json.get('token')
#     restaurantId = request.json.get('restaurantId')
#     result = run_statement("CALL create_order(?,?)", [token, restaurantId])
#     if (type(result) == list):
#         orderId = result[0][0]
#         items = request.json.get('items')
#         for item in items:
#             result = run_statement("CALL add_to_order(?,?)", [orderId, item])
#             if (type(result) == list):
#                 if result[0][0] == 1:
#                     return make_response(jsonify("Successfully Sent Order to Restaurant"), 200)
#                 elif result[0][0] == 0:
#                     return make_response(jsonify("Error: Order was not sent, please try again."), 500)
#     elif "orders_FK_restaurant" in result:
#         return make_response(jsonify("Error: Restaurant ID does not exist."), 404)
#     else:
#         return make_response(jsonify(result), 500)








# HOW TO WRITE 'IF' STATEMENT FOR 'IF TOKEN MATCHES RESTAURANT SESSION DO x' ELSE IF TOKEN MATCHES CLIENT SESSION DO x'
# IDEA: INSTEAD OF IF TOKEN, IF CANCELORDER, THEN CHECK TOKEN AGAINST CLIENT AND OPPOSITE FOR RESTAURANT
# need to test procedure 
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
    confirmOrder = request.json.get('confirmOrder')
    completeOrder = request.json.get('completeOrder')
    result = run_statement("CALL update_order_status(?,?,?,?,?)", [token, orderId, cancelOrder, confirmOrder, completeOrder])

    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Successfully Sent Order"), 200)
        elif result[0][0] == 0:
            return make_response(jsonify("Error: Order was not sent, please try again."), 500)
    else:
        return make_response(jsonify(result), 500)


    # post order: 
    # procedure that creates order, attaches order to restaurant and person
    # returns the order ID
    # need that in next steps
    # then use 2nd procedure, add single item to an order, add 1 row to the order item table (takes order id and item id, maps one to the other)
    # with those 2 procedures, run a loop thru items array that has numbers of items (after you created the order, iterate through array and add items to order)
    
    # GET
    #Run procedure, either get ALL (one for restaurant, one for customer algorithm is the same)
    # run in either pass to it an order id and it only retrieves the single order,
    # or retrieve all orders that belong to either client or restaurant
    # with optional params, have the parameter declared in procedure regardless, if you don't want it active, pass null to it, in the procedure
    # if the order id input is = null, then get all orders
    # if its not null then run select with the param 
    # since select will have multi rows for the same order, ORDER BY order Id (id of the orders table) ASC OR DESC doesn't matter (append an item to items array)
    # procedure will return them in separate rows but we need to group them together (one object for order #5 with a list that holds all the items, iterate and double check, if you changed an order)


    # back end deployment and modify apache to new url
    # START WITH STEP 2 ON THE LINKED IN FILE HE SENT
    # SINCE I bought a domain and I want to use a bunch of sub domains, foodie.cloudpunch.com
    # to avoid the need for a new certificate every time you set up a sub domain, you can generate a wild card certificate, you can put anything in the subdomain and it will be captured in the certificate
    # so generate 1 certificate, and you can use it in the path of the main url and sub domain
    # (certificates expire every 3 months so doing 1 cert for all is way easier)
    # go through DNS challenge, you prove to certbot that you are the owner of all subdomains to your domain
    # add a new record to your DNS handler and essentially say, acme challenge (add dns txt record under domain name then confirm)
    # TXT record can have anything in it, usually its used for dns challenges. You are telling certbot I am able to generate this info in this custom domain name, and this means that I own the whole domain
    # the chrontab might not work, depends on the policy of certbot (makes sure you dont have to manually go back and renew it every time - last step, hers is set for 1nce a day)


    # SKIP DOCUMENT ROOT IN APACHE CONFIG ** if you can't, just create an Empty folder (you can call it foodiefront end for later use) with nothing in it (in var/www), point it to there, we don't have a front end