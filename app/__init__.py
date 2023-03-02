from flask import Flask

app = Flask(__name__)


from endpoints import client, client_login, restaurant, restaurant_login, restaurant_menu


# TO DO: GO BACK AND CHANGE FORMULAS SO THE PATCHES WITH OPTIONAL ARGS DON'T ALWAYS NEED A VALUE ENTERED TO GO THROUGH