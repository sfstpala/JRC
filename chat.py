
import cherrypy

import time
import os
import json


class App (object):

    class Static (object):

        _cp_config = {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(os.path.split(
                os.path.realpath(__file__))[0], "static")
        }


    static = Static()
    messages = []

    @cherrypy.expose
    def index(self):
        return open(os.path.join(os.path.split(os.path.realpath(__file__))[0],
            "views", "index.html")).read()

    @cherrypy.expose
    def post_message(self, user="", message="", last_atime="0"):
        self.messages.append((int(time.time() * 10000),
            time.strftime("%H:%M"), self.safe(user), self.safe(message)))
        if len(self.messages) > 100:
            self.messages = self.messages[-100:]
        cherrypy.response.headers["Content-Type"] = "application/json"
        return json.dumps([i for i in self.messages
            if i[0] > int(last_atime)]).encode()

    @cherrypy.expose
    def read_messages(self, last_atime="0"):
        cherrypy.response.headers["Content-Type"] = "application/json"
        return json.dumps([i for i in self.messages
            if i[0] > int(last_atime)]).encode()

    def safe(self, s):
        s = s.replace("&", "&amp;").replace("<", "&lt;")
        s = s.replace(">", "&gt;").replace("'", "&#39;")
        s = s.replace("\"", "&quot;")
        return s or ""


cherrypy.quickstart(App(), config={'global': {
    'tools.encode.encoding': 'utf-8',
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 21211,
}})
