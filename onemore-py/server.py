"""App entry point."""

"""Initialize Flask app."""
import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    mail = Mail(app)

    # This is the configuration for the email server.
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_HOST_USER")
    app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_HOST_PASSWORD")
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True

    mail = Mail(app)

    app.config.from_object("config.Config")

    api = Api(app=app)
    from app.workspace.workspace_routes import create_workspace_routes
    from app.test_suite.testsuite_routes import create_testsuite_routes
    from app.test_case.testcase_routes import create_testcase_routes
    from app.users.user_routes import create_authentication_routes

    create_authentication_routes(api=api)
    create_workspace_routes(api=api)
    create_testsuite_routes(api=api)
    create_testcase_routes(api=api)

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create database tables for our data models

        return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
