from app import app
import bcrypt
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data

# GET Restaurant Menu and with Optional RestaurantId 
@app.get('/api/menu')
def get_restaurant_menu():
    """
    Optional:
    restaurantId
    """
    restaurantId = request.args.get('restaurantId')
    if (restaurantId == None):
        restaurantId = None
    keys = ["name", "description", "price", "image_url", "restaurantId"]
    result = run_statement('CALL get_restaurant_menu(?)', [restaurantId])
    response = []
    if(type(result) == list):
        for menu in result:
            response.append(dict(zip(keys, menu)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(response), 500)

# POST Restaurant Menu Items
@app.post('/api/menu')
def add_restaurant_menu():
    """
    Expects 4 Args:
    token, name, description, price
    Optional:
    imageUrl
    """
    required_data = ['token', 'name', 'description', 'price']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    token = request.json.get('token')
    name = request.json.get('name')
    description = request.json.get('description')
    price = request.json.get('price')
    image_url = request.json.get('imageUrl')
    result = run_statement("CALL add_menu_item(?,?,?,?,?)", [token, name, description, price, image_url])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Successfully added Item to Menu."), 200)
        elif result[0][0] == 0:
            return make_response(jsonify("Something went wrong, please try again."), 500)
    elif "'restaurant_id' cannot be null" in result:
        return make_response(jsonify("Error: Action Not Authorized"), 401)
    else:
        return make_response(jsonify(result), 500)

# PATCH Restaurant Menu Items
@app.patch('/api/menu')
def edit_restaurant_menu():
    """
    Expects 2 Args:
    token, menuId
    Optional:
    name, description, price, imageUrl
    """
    required_data = ['token', 'menuId']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    token = request.json.get('token')
    menuId = request.json.get('menuId')
    name = request.json.get('name')
    description = request.json.get('description')
    price = request.json.get('price')
    image_url = request.json.get('imageUrl')
    result = run_statement("CALL edit_menu_item(?,?,?,?,?,?)", [token, menuId, name, description, price, image_url])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Successfully edited menu item."), 200)
        elif result[0][0] == 0:
            return make_response(jsonify(f"Error: Action Not Authorized, you do not own Menu Item {menuId}."), 403)
    else:
        return make_response(jsonify(result), 500)