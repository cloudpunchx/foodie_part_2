from app import app
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data

# POST Restaurant Login Sessions, completed through 1 stored procedure
@app.post('/api/restaurant-login')
def post_restaurant_login():
    """
    Expects 2 Args
    Email, Password
    """
    required_data = ['email', 'password']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    email = request.json.get('email')
    password = request.json.get('password')
    result = run_statement("CALL restaurant_login(?,?)", [email, password])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Successfully logged in."), 200)
        elif result[0][0] == 0:
            return make_response(jsonify("Something went wrong, please try again."), 500)
    else:
        return make_response(jsonify(result), 500)

# DELETE Restaurant Login Sessions, completed through 1 stored procedure
@app.delete('/api/restaurant-login')
def delete_restaurant():
    """
    Expects 1 Argument:
    Token
    """
    required_data = ['token']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    token = request.json.get('token')
    result = run_statement("CALL restaurant_logout(?)", [token])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Successfully logged out."), 200)
        elif result[0][0] == 0:
            return make_response(jsonify("Error, please try logging out again."), 400)
    else:
        "There has been an unexpected error."