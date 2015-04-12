import cherrypy
import cherrypy_cors

class Server(object):
    def __init__(self):
        object.__init__(self)
        # TODO: Read in raw data and index
        # self.field = something

    @cherrypy.expose
    def index(self):
        return "Testing..."

    @cherrypy.expose
    #@cherrypy_cors.tools.expose()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.json_in(force=False)
    def get_diseases(self):
        # TODO: Return list of diseases
        return_val = []
        return return_val

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.json_in(force=False)
    def get_drugs(self):
        try:
            disease = cherrypy.request.json # Disease name
        except:
            pass

        # TODO: Return drugs associated with disease
        return_val = []
        return return_val

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.json_in(force=False)
    def pair_scores(self):
        try:
            pairs = cherrypy.request.json # Array of drug pairs
        except:
            pass

        # TODO: Return array of drug pair scores in the same order
        return_val = []
        return return_val

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    cherrypy.config.update({'tools.CORS.on': True,})
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.socket_port = 8081
    cherrypy.quickstart(Server())