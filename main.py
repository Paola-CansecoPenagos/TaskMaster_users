from flask import Flask, jsonify
from flask_cors import CORS
from infrastructure.routers.user_router import user_router
from threading import Thread
from infrastructure.messaging.rabbitmq_consumer_categories import start_consumer

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(user_router)


if __name__ == '__main__':
    consumer_thread = Thread(target=start_consumer)
    consumer_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5001)
