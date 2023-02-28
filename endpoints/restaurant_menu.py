from app import app
import bcrypt
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data

# GET Restaurant Menu and with Optional RestaurantId 
@app.get('/api/menu')
def get_restaurant_menu():
    """
    Optional Arg:
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