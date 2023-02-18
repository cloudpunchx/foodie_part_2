from app import app
from flask import make_response, jsonify
from helpers.dbhelpers import run_statement

# GET Client Profile
# @app.get('/api/client')
# def get_client():
#     """
#     """
#     keys = ["clientId", "username", "firstName", "lastName", "email", "pictureUrl", "createdAt"]
#     result = run_statement('CALL get_client_profile()')
#     client = []
#     if(type(result) == list):
#         for client in result:
#             zipped = zip(keys, client)
#             client.append(dict(zipped))
#         return make_response(jsonify(client), 200)
#     else:
#         return make_response(jsonify(result), 500)
    
@app.get('/api/client')
def get_client():
    """
    """
    keys = ["clientId", "username", "firstName", "lastName", "email", "pictureUrl", "createdAt"]
    result = run_statement('CALL get_client_profile()')
    if(type(result) == list):
        return make_response(jsonify(result), 200)
    else:
        return make_response(jsonify(result), 500)

