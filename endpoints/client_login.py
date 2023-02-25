from app import app
import bcrypt
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data

# MOVING ON - COME BACK AND ADD PASSWORD ENCRYPTING, FOLLOW STEPS IN NOTES. 
# POST Client Login Sessions, completed through 1 stored procedure
# @app.post('/api/client-login')
# def post_client_login():
#     """
#     Expects 2 Args
#     Email, Password
#     """
#     required_data = ['email', 'password']
#     check_result = check_data(request.json, required_data)
#     if check_result != None:
#         return check_result
#     email = request.json.get('email')
#     password = request.json.get('password')
#     result = run_statement("CALL client_login(?,?)", [email, password])
#     if (type(result) == list):
#         if result[0][0] == 1:
#             return make_response(jsonify("Successfully logged in."), 200)
#         elif result[0][0] == 0:
#             return make_response(jsonify("Something went wrong, please try again."), 500)
#     else:
#         return make_response(jsonify(result), 500)

# @app.post('/api/client-login')
# def post_client_login():
#     """
#     Expects 2 Args
#     Email, Password
#     """
#     required_data = ['email', 'password']
#     check_result = check_data(request.json, required_data)
#     if check_result != None:
#         return check_result
#     email = request.json.get('email')
#     password = request.json.get('password')
#     salt = bcrypt.gensalt()
#     hash_result = bcrypt.hashpw(password.encode(), salt)
#     result = run_statement("CALL get_client_login(?)", [email])
#     if(type(result) == list):
#         if result == []:
#             return make_response(jsonify('Incorrect email address, please re-enter email.'), 400)
#         for password in result:
#             password_return = "".join(password)
#             if (bcrypt.checkpw(password_return.encode(), hash_result)):
#                 result = run_statement("CALL client_login(?)", [email])
#                 if (type(result) == list):
#                     if result[0][0] == 1:
#                         return make_response(jsonify("Welcome, login successful."), 200)
#                     elif result[0][0] == 0:
#                         return make_response(jsonify("Error, please try again."), 400)
#                 else:
#                     "There has been an unexpected error."
#             else:
#                 return make_response(jsonify('Something went wrong, please try again.'), 500)

# THIS IS RETURNING A HASHED PW BUT IT DOESN'T MATCH THE INPUT PW, EVEN THOUGH I KNOW THEY'RE THE
@app.post('/api/client-login')
def post_client_login():
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
    salt = bcrypt.gensalt()
    hash_result = bcrypt.hashpw(password.encode(), salt)
    result = run_statement("CALL get_client_login(?)", [email])
    if(type(result) == list):
        if result == []:
            return make_response(jsonify('Incorrect email address, please re-enter email.'), 400)
        for password in result:
            password_return = "".join(password)
            if (bcrypt.checkpw(password_return.encode(), hash_result)):
                result = run_statement("CALL client_login(?,?)", [email,hash_result])
                if (type(result) == list):
                    if result[0][0] == 1:
                        return make_response(jsonify("Welcome, login successful."), 200)
                    elif result[0][0] == 0:
                        return make_response(jsonify("Error, please try again."), 400)
                else:
                    "There has been an unexpected error."
            else:
                return make_response(jsonify('Something went wrong, please try again.'), 500)



# DELETE Client Login Sessions, completed through 1 stored procedure
@app.delete('/api/client-login')
def delete_client_login():
    """
    Expects 1 Argument:
    Token
    """
    required_data = ['token']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    token = request.json.get('token')
    result = run_statement("CALL client_logout(?)", [token])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Successfully logged out."), 200)
        elif result[0][0] == 0:
            return make_response(jsonify("Error, please try logging out again."), 400)
    else:
        "There has been an unexpected error."