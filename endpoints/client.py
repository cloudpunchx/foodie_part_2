from app import app
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data
import json

# GET Client Profile    
@app.get('/api/client')
def get_client():
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