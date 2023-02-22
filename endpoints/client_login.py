from app import app
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data

# POST Client Login Sessions
# STEP 1: Take email land password to GET client ID and return it as clientID
# @app.post('/api/client-login')
# def post_client_login():
#     """
#     Expects 2 Args
#     ClientID, Token
#     """
#     required_data = ['email', 'password']
#     check_result = check_data(request.json, required_data)
#     if check_result != None:
#         return check_result
#     email = request.json.get('email')
#     password = request.json.get('password')
#     result = run_statement("CALL get_client_id(?,?)", [email, password])
#     if result == None:
#         return make_response(jsonify("Something went wrong, please try again."), 500)
#     else:
#         clientId = result
#         token = uuid.uuid4()
#         required_data = ['clientId', 'token']
#         if check_result != None:
#             return check_result
#         check_result = check_data(request.json, required_data)
#         result = run_statement("CALL post_client_login_session(?,?)", [clientId, token])
#         if result == 1:
#             return make_response(jsonify("Successfully created profile."), 200)
#         else:
#             return result

@app.post('/api/client-login')
def post_client_login():
    """
    Expects 2 Args
    ClientID, Token
    """
    required_data = ['email', 'password']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    email = request.json.get('email')
    password = request.json.get('password')
    result = run_statement("CALL client_login(?,?)", [email, password])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Successfully logged in."), 200)
        elif result[0][0] == 0:
            return make_response(jsonify("Something went wrong, please try again."), 500)
    else:
        return make_response(jsonify(result), 500)
