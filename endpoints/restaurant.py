from app import app
import bcrypt
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

# POST Restaurants
@app.post('/api/restaurant')
def create_restaurant():
    """
    Expects 7 Args:
    name, address, bio, city, email, password, phoneNum
    Optional:
    bannerUrl, profileUrl
    """
    required_data = ['name', 'address', 'bio', 'city', 'email', 'password', 'phoneNum']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    name = request.json.get('name')
    address = request.json.get('address')
    bio = request.json.get('bio')
    city = request.json.get('city')
    email = request.json.get('email')
    password = request.json.get('password')
    phone_num = request.json.get('phoneNum')
    banner_url = request.json.get('banner_url')
    profile_url = request.json.get('profile_url')
    salt = bcrypt.gensalt()
    hash_result = bcrypt.hashpw(password.encode(), salt)
    result = run_statement("CALL create_restaurant_profile(?,?,?,?,?,?,?,?,?)", [name, address, bio, city, email, hash_result, phone_num, banner_url, profile_url])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Successfully created profile."), 200)
        elif result[0][0] == 0:
            return make_response(jsonify("Something went wrong, please try again."), 500)
    elif "restaurant_UN_email" in result:
        return make_response(jsonify("This email is already in use, please enter another email or click forgot password."), 409)
    elif "restaurant_UN_username" in result:
        return make_response(jsonify("This username is already in use, please enter another username."), 409)
    else:
        return make_response(jsonify(result), 500)