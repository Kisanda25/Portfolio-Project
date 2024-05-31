from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Define the base
Base = declarative_base()

# Database setup
engine = create_engine('sqlite:///users.db', echo=True)

# Configure session
Session = sessionmaker(bind=engine)
db_session = scoped_session(Session)

def create_app():
    app = Flask(__name__)

    with app.app_context():
        # Import models to ensure tables are created
        from app import models
        Base.metadata.create_all(engine)

        # Register routes
        from app import routes

    # Ensure the session is properly closed after each request
    @app.teardown_appcontext
    def shutdown_session_on_teardown(exception=None):
        db_session.remove()

    return app

