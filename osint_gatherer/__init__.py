from flask import Flask
import rq_dashboard

app = Flask(__name__)
app.config.from_object("osint_gatherer.config")
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

import osint_gatherer.views
