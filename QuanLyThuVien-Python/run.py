from flask import Flask
import mysql.connector
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Kết nối MySQL
    app.db = mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT
    )

    # Import routes
    from app.routes.book_routes import book_bp
    app.register_blueprint(book_bp, url_prefix="/books")

    @app.route("/")
    def home():
        return "Library Management System (Flask + MySQL)"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
