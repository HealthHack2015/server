import cherrypy
import cherrypy_cors
import sqlite3

class Server(object):
    def __init__(self):
        object.__init__(self)
        # TODO: Read in raw data and index
        self.db = sqlite3.connect(":memory:")
        self.c = self.db.cursor()
        self.c.execute('''create table drugs (name text unique, class text, indication text)''')
        self.c.execute('''create table interactions (d1 text, d2 text, severity integer, warning text, desc text)''')
        self.db.commit()
        with open("drugs_table.psv", "r") as drugs:
            for drug in drugs.readlines():
                drug = tuple(drug.strip().split("|"))
                self.c.execute('''insert into drugs(name,class,indication) values(?,?,?)''', drug)
        self.db.commit()
        with open("drug_interactions.psv", "r") as interactions:
            for interaction in interactions.readlines():
                interaction = tuple(drug.strip().split("|"))
                self.c.execute('''insert into interactions(d1,d2,severity,warning,desc) values(?,?,?,?)''', interaction)
        self.db.commit()

    def query(query):
        self.c.execute(query)
        self.db.commit()


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
        try:
            query('''select distinct class from drugs''')
        except Exception, e:
            pass
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