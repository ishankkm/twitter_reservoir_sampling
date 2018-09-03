'''
Created on Aug 28, 2018
@author: ishank
'''

from threading import Lock
from flask_socketio import emit
from middleware import Middleware
from flask import render_template, jsonify, request

class Routes():
    
    def __init__(self, app, socket):
        self._threads = {}
        self._thread_lock = Lock()
        self._socket = socket
        self._app = app
        self._middlewares = {}

    def init_api_routes(self):
        self._app.add_url_rule('/', 'page_index', self.page_index, methods=['GET'])
        self._app.add_url_rule('/api', 'list_routes', self.list_routes, methods=['GET'])
            
    def init_socket_connections(self):
        self._socket.on_event('connect', self.on_connect)
        self._socket.on_event('disconnect', self.on_disconnect)
    
    def page_index(self):
        return render_template("index.html")
    
    def on_connect(self): 
        sid = request.sid       
        self._socket.on_event(sid, self.manage_events)
        self.send_status(streaming=False)   
        
    def on_disconnect(self):
        try:
            mw = self._middlewares.get(request.sid, None)
            if mw:
                mw.stop_backgroung_job()
        except:
            print('Client Disconnected with exception')
        
        print('Client Disconnected', request.sid)
        
    def send_status(self, streaming=False, error=[]):
        status = {
            'streaming': streaming,
            'error': error
        }
        emit('status', status)
    
    def manage_events(self, params):
        sid = request.sid
        try:
            if params["streaming"]:
                
                with self._thread_lock:
                    if not sid in self._threads:
                        mw = Middleware(self._socket, sid, params['topics'], params['reservoirSize'])
                        self._middlewares[sid] = mw
                        self._threads[sid] = self._socket.start_background_task(target=mw.start_background_job)
                        
                    elif not self._threads[sid].is_alive():
                        mw = Middleware(self._socket, sid, params['topics'], params['reservoirSize'])
                        self._middlewares[sid] = mw
                        self._threads[sid] = self._socket.start_background_task(target=mw.start_background_job)
                        
                self.send_status(streaming=True)  
                     
            else:
                mw = self._middlewares.get(request.sid, None)
                if mw:
                    mw.stop_backgroung_job()
                self.send_status(streaming=False)
                
        except:
            print('Request Invalid')
            self.send_status(streaming=False, error=[{'type': 'Request Invalid'}])
        
    def list_routes(self):
        result = []
        for rt in self._app.url_map.iter_rules():
            result.append({
                "methods": list(rt.methods),
                "route": str(rt)
            })
        return jsonify({"routes": result, "total": len(result)})
    
    
    
    
    
    
    
    
    
    
    
    