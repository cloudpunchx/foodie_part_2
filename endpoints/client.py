from app import app
import bcrypt 
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data

# GET Client Profile   
@app.get('/api/client')
def get_client_profile():
    """
    Expects 1 Arg:
    token
    """
    required_data = ['token']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    token = request.json.get('token')
    keys = ["clientId", "username", "firstName", "lastName", "email", "pictureUrl", "createdAt"]
    result = run_statement('CALL get_client_profile(?)', [token])
    if(type(result) == list):
        for client in result:
            zipped = zip(keys, client)
            client = (dict(zipped))
        return make_response(jsonify(client), 200)
    else:
        return make_response(jsonify(result), 500)

# Post Client Profile, (Client Sign Up) then logs user session and created token in 1 stored procedure that calls another procedure.
# @app.post('/api/client')
# def post_client():
#     """
#     Expects 5 Args:
#     username, firstName, lastName, email, password
#     1 Optional:
#     pictureUrl
#     """
#     required_data = ['username', 'firstName', 'lastName', 'email', 'password']
#     check_result = check_data(request.json, required_data)
#     if check_result != None:
#         return check_result
#     username = request.json.get('username')
#     first_name = request.json.get('firstName')
#     last_name = request.json.get('lastName')
#     email = request.json.get('email')
#     password = request.json.get('password')
#     pictureUrl = request.json.get('pictureUrl')
#     result = run_statement("CALL create_client_profile(?,?,?,?,?,?)", [username, first_name, last_name, email, password, pictureUrl])
#     if (type(result) == list):
#         if result[0][0] == 1:
#             return make_response(jsonify("Successfully created profile."), 200)
#         elif result[0][0] == 0:
#             return make_response(jsonify("Something went wrong, please try again."), 500)
#     elif "client_UN_email" in result:
#         return make_response(jsonify("This email is already in use, please enter another email or click forgot password."), 409)
#     elif "client_UN_username" in result:
#         return make_response(jsonify("This username is already in use, please enter another username."), 409)
#     else:
#         return make_response(jsonify(result), 500)

# Implementing bcrypt hash and salt
@app.post('/api/client')
def post_client():
    """
    Expects 5 Args:
    username, firstName, lastName, email, password
    1 Optional:
    pictureUrl
    """
    required_data = ['username', 'firstName', 'lastName', 'email', 'password']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    username = request.json.get('username')
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    email = request.json.get('email')
    password = request.json.get('password')
    salt = bcrypt.gensalt()
    hash_result = bcrypt.hashpw(password.encode(), salt)
    pictureUrl = request.json.get('pictureUrl')
    result = run_statement("CALL create_client_profile(?,?,?,?,?,?)", [username, first_name, last_name, email, hash_result, pictureUrl])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Successfully created profile."), 200)
        elif result[0][0] == 0:
            return make_response(jsonify("Something went wrong, please try again."), 500)
    elif "client_UN_email" in result:
        return make_response(jsonify("This email is already in use, please enter another email or click forgot password."), 409)
    elif "client_UN_username" in result:
        return make_response(jsonify("This username is already in use, please enter another username."), 409)
    else:
        return make_response(jsonify(result), 500)


