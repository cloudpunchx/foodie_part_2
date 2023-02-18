from flask import Flask
from flask_cors import CORS
from dbcreds import production_mode

# to run code
# flask --app app run

app = Flask(__name__)

if (production_mode == True):
    print("Running server in Production Mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    print("Running Server in Testing Mode.")
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)

from endpoints import client