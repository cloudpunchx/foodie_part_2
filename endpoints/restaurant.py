from app import app
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data

# GET Restaurants and with Optional RestaurantId Arg you can GET specific restaurant information  
@app.get('/api/restaurant')
def get_restaurants():
    """
    Optional Arg:
    restaurantId
    """
    restaurantId = request.args.get('restaurantId')
    if (restaurantId == None):
        restaurantId = None
    keys = ["restaurantId", "name", "address", "bio", "city", "email", "phoneNum", "bannerUrl", "profileUrl"]
    result = run_statement('CALL get_restaurants(?)', [restaurantId])
    response = []
    if(type(result) == list):
        for restaurant in result:
            response.append(dict(zip(keys, restaurant)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(response), 500)