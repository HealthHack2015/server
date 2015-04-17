import cherrypy
import cherrypy_cors
import sqlite3
import itertools as it

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

    def compute_score(self,combo):
        raw_interacts = []
        for pair in it.combinations(combo, 2):
            temp = [list(el) for el in self.query('''select severity,warning,desc from interactions where ((d1="{0}" and d2="{1}") or (d1="{0}" and d2="{1}"))'''.format(pair[0],pair[1]))]
            if len(temp) > 0:
                raw_interacts.append(temp[0])
        max_score = 0
        warning = ""
        descs = []
        for interact in raw_interacts:
            descs.append[interact[2]]
            if interact[0] > max_score:
                max_score = interact[0]
                warning = interact[1]
        return [max_score, warning, '\n'.join(descs)]

    @cherrypy.expose
    def index(self):
        return "Testing..."

    @cherrypy.expose
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
    def get_scores(self):
        try:
            diseases = cherrypy.request.json
            disease_drugs = []
            for disease in diseases:
                temp = [el[0] for el in self.query('''select distinct name from drugs where class = "{0}"'''.format(disease))] # Disease name
                disease_drugs.append(temp)
            return sorted([compute_score(combo).append(combo) for combo in list(it.product(*disease_drugs))], key = lambda x: x[0])
        except:
            return []

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    cherrypy.config.update({'tools.CORS.on': True,})
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.socket_port = 8081
    cherrypy.quickstart(Server())
