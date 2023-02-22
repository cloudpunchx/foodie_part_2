from app import app
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data

# GET Client Profile   
# probably should remove client id as arg because the token should be attached to an ID in the call? THE TOKEN grabs the ID to return personal profile?

@app.get('/api/client')
def get_client_profile():
    """
    Expects 1 Arg:
    ClientId
    """
    required_data = ['clientId']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    clientId = request.json.get('clientId')
    keys = ["clientId", "username", "firstName", "lastName", "email", "pictureUrl", "createdAt"]
    result = run_statement('CALL get_client_profile(?)', [clientId])
    if(type(result) == list):
        for client in result:
            zipped = zip(keys, client)
            client = (dict(zipped))
        return make_response(jsonify(client), 200)
    else:
        return make_response(jsonify(result), 500)


# Leaving off on Client POST - create_profile procedure, research uuid randomize token
# post profile procedure as normal, return ID, then call 2nd procedure with id client id and add uuid from import

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
    pictureUrl = request.json.get('pictureUrl')
    result = run_statement("CALL create_client_profile(?,?,?,?,?,?)", [username, first_name, last_name, email, password, pictureUrl])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Successfully created profile."), 200)
        elif result[0][0] == 0:
            return make_response(jsonify("Something went wrong, please try again."), 500)
    else:
        return make_response(jsonify(result), 500)
    
# Error for POST says the function returns None

# Start POST for client-session then work on post_client since they need each other
