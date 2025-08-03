# Main Flask application - now organized with structured folders
from flask import Flask
from routes.user_routes import user_routes

# Create Flask app
app = Flask(__name__)

# Register the user routes blueprint
app.register_blueprint(user_routes)

if __name__ == '__main__':
    print("🚀 Starting User Management System...")
    print("📁 Using organized folder structure: /config /models /routes")
    app.run(host='0.0.0.0', port=5000, debug=True)