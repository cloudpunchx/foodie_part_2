from app import app
from flask_cors import CORS
from dbcreds import production_mode

if (production_mode == True):
    print("Running server in Production Mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    print("Running Server in Testing Mode.")
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)