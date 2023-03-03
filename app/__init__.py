from flask import Flask

app = Flask(__name__)


from endpoints import client, client_login, restaurant, restaurant_login, restaurant_menu, order


# TO DO: Come back to Dbeaver Edit Menu Item and endpoint