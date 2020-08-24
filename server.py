# -*- coding: utf-8 -*-
import flasgger
import flask

import config
from controller import general_controller, sample_controller

app = flask.Flask(__name__)

# add blueprint
app.register_blueprint(general_controller.general_app)
app.register_blueprint(sample_controller.sample_app)
app.config["SWAGGER"] = {
    "version": "6.9",
    "title": "Brahm",
    "uiversion": 3,
    "description": f"Designed by {config.GITHUB_USERNAME}\n\n",
}

swagger = flasgger.Swagger(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3412, debug=False)
