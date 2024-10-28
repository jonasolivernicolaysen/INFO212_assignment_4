from neo4j import GraphDatabase

URI = "NEO4J_URI"
AUTH = ("neo4j", "password")

class Neo4j_database:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase(uri, auth=auth)
    
    def close(self):
        self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]
        
db = Neo4j_database(URI, AUTH)