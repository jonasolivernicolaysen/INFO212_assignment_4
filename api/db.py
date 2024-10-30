# db.py
from neo4j import GraphDatabase
from flask import g, current_app

# Sett opp URI og autentisering for Neo4j
URI = "bolt://localhost:7687"  # Endre hvis Neo4j kjører på en annen URI
AUTH = ("neo4j", "NrE6a_WGEicq8HLTJ3rCM5_4FSvIoTZSFw0LGstZqpo")


class Neo4jDatabase:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]


def get_db():
    if 'neo4j_db' not in g:
        uri = current_app.config['NEO4J_URI']
        auth = (current_app.config['NEO4J_USER'], current_app.config['NEO4J_PASSWORD'])
        g.neo4j_db = Neo4jDatabase(uri, auth)
    return g.neo4j_db

def close_db(e=None):
    db = g.pop('neo4j_db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

db = Neo4jDatabase(URI, AUTH)