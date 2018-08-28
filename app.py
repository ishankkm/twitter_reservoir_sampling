'''
Created on Aug 24, 2018
@author: ishank
'''

from flask import Flask
from flask_socketio import SocketIO
from routes import Routes

# create the Flask application
app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")


# app.static_folder = './ui/build/static'
# app.template_folder = './ui/build'

rt = Routes(app, socketio)

rt.init_api_routes()
rt.init_socket_connections()

if __name__ == "__main__":
    socketio.run(app, debug=True)
    
    
    
    
    
    
    
    
    
    