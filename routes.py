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
        mw = Middleware(self._socket, emit_at=sid)
        self._middlewares[sid] = mw
        
        with self._thread_lock:
            if not sid in self._threads:
                self._threads[sid] = self._socket.start_background_task(target=mw.start_background_job)
        emit(sid, sid)   
        
    def on_disconnect(self):
        mw = self._middlewares.get(request.sid, None)
        if mw:
            mw.stop_backgroung_job()
        
        print('Client Disconnected', self._threads[request.sid].is_alive())
        
    def list_routes(self):
        result = []
        for rt in self._app.url_map.iter_rules():
            result.append({
                "methods": list(rt.methods),
                "route": str(rt)
            })
        return jsonify({"routes": result, "total": len(result)})