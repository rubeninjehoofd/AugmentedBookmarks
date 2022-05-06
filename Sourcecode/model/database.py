# Define imports
# ----------------------------------
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from bs4 import BeautifulSoup

class App:

    def __init__(self):
        
        # Define auth variables
        # ----------------------------------------------------------------------
        with open("config/config.xml", "r") as f:
            config = f.read()
            file = BeautifulSoup(config, features="html.parser")
            
            uri = file.auth.uri.string
            user = file.auth.user.string
            password = file.auth.password.string

        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print("Connected to the database")

    def close(self):
        self.driver.close()

    # Actions with the database 
    # ----------------------------------------------------------------------    

    # Create person function
    # ----------------------------------------------------------------------    
    def create_person(self, name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            exist = self.find_person(name)
            if exist == False:
                result = session.write_transaction(self._create_person, name)
                print("Created person")
                for row in result:
                    print("Created person")
            else: 
                print("Person {p} already exists".format(p=name))

    @staticmethod
    def _create_person(tx, name):
        query = (
            "CREATE (p:User { name: $name }) "
        )
        result = tx.run(query, name=name)
        try:
            return [{"p": row["p"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    # ----------------------------------------------------------------------   

    # Crate bookmark
    # ----------------------------------------------------------------------    

    def create_bookmark(self, name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            exist = self.find_person(name)
            if exist == False:
                result = session.write_transaction(self._create_bookmark, name)
                for row in result:
                    print("Created person: {p}".format(p=name))
            else: 
                print("Person {p} already exists".format(p=name))

    
    @staticmethod
    def _create_bookmark(tx, name):
        query = (
            "CREATE (p:User { name: $name }) "
        )
        result = tx.run(query, name=name)
        try:
            return [{"p": row["p"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise



    # ----------------------------------------------------------------------    

    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            if len(result) == 0:
                print("No person found")
                return False
            else: 
                for row in result:
                    print("Found person: {row}".format(row=row))
                return True

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (u:User) "
            "WHERE u.name = $person_name "
            "RETURN u.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]


if __name__ == "__main__":
    app = App()
    app.create_person("Johan Hendrik")
    # app.find_person("Mark")
    app.close()