import cherrypy
import cherrypy_cors
import sqlite3

class Server(object):
    def __init__(self):
        object.__init__(self)
        self.db = sqlite3.connect(":memory:", check_same_thread=False)
        self.db.text_factory = str
        c = self.db.cursor()
        c.execute('''create table drugs (name text unique, class text, indication text)''')
        c.execute('''create table interactions (d1 text, d2 text, severity integer, warning text, desc text)''')
        self.db.commit()
        with open("../raw_data/drugs_table.psv", "r") as drugs:
            for drug in drugs.readlines():
                drug = tuple(drug.strip().split("|"))
                c.execute('''insert into drugs(name,class,indication) values(?,?,?)''', drug)
        self.db.commit()
        with open("../raw_data/drug_interactions.psv", "r") as interactions:
            for interaction in interactions.readlines():
                interaction = tuple(interaction.strip().split("|"))
                c.execute('''insert into interactions(d1,d2,severity,warning,desc) values(?,?,?,?,?)''', interaction)
        self.db.commit()
    c.close()
    print "INIT FINISHED."

    def query(self, query):
	c = self.db.cursor()
	return c.execute(query).fetchall()
	
    def pair_query(self, query, dr1,dr2):
	c = self.db.cursor()
	return c.execute(query.format(d1=dr1,d2=dr2)).fetchall()

    @cherrypy.expose
    def index(self):
        return "Testing..."

    @cherrypy.expose
    #@cherrypy_cors.tools.expose()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.json_in(force=False)
    def get_diseases(self):
        return_val = []
        try:
            return_val = [el[0] for el in self.query('''select distinct class from drugs''')]
        except Exception, e:
        print e
        return return_val

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.json_in(force=False)
    def get_drugs(self,disease):
        try:  
           return_val = [el[0] for el in self.query('''select distinct name from drugs where class = "{disease}"'''.format(disease=disease))] # Disease name
        except Exception, e:
            print e
	return return_val

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.json_in(force=False)
    def pair_scores(self,d1="",d2=""):
        try:
            pairs = [el[0] for el in self.pair_query('''select severity from interactions where ((d1="{d1}" and d2="{d2}") or (d1="{d2}" and d2="{d1}"))''',d1,d2)] # Array of drug pairs
        except Exception, e:
            print e

        # TODO: Return array of drug pair scores in the same order
        return pairs

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    cherrypy.config.update({'tools.CORS.on': True,})
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.socket_port = 8081
    cherrypy.quickstart(Server())
