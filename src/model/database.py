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
        with open("src\config\config.xml", "r") as f:
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

    # Create person 
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

    # Create tag 
    # ----------------------------------------------------------------------
    def create_tag(self, name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            exist = self.find_tag(name)
            if exist == False:
                result = session.write_transaction(self._create_tag, name)
                print("Created tag")
                for row in result:
                    print("Created tag")
            else:
                print("Tag {p} already exists".format(p=name))

    @staticmethod
    def _create_tag(tx, name):
        query = (
            "CREATE (t:Tag { name: $name }) "
        )
        result = tx.run(query, name=name)
        try:
            return [{"p": row["p"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))

    # Crate bookmark
    # ----------------------------------------------------------------------

    def create_bookmark(self, name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            exist = self.find_bookmark(name)
            if exist == False:
                result = session.write_transaction(self._create_bookmark, name)
                for row in result:
                    print("Created bookmark: {p}".format(p=name))
            else:
                print("Bookmark {p} already exists".format(p=name))

    @staticmethod
    def _create_bookmark(tx, name):
        query = (
            "CREATE (b:Bookmark { name: $name }) "
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

    # Find person
    # ----------------------------------------------------------------------
    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_person, person_name)
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


    # Find tag
    # ----------------------------------------------------------------------
    def find_tag(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_tag, person_name)
            if len(result) == 0:
                print("No tag found")
                return False
            else:
                for row in result:
                    print("Found tag: {row}".format(row=row))
                return True

    @staticmethod
    def _find_and_return_tag(tx, tag):
        query = (
            "MATCH (t:Tag) "
            "WHERE t.name = $tag "
            "RETURN t.name AS name"
        )
        result = tx.run(query, tag=tag)
        return [row["name"] for row in result]

    # Find bookmark
    # ----------------------------------------------------------------------
    def find_bookmark(self, bookmark_name):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_tag, bookmark_name)
            if len(result) == 0:
                print("No bookmark found")
                return False
            else:
                for row in result:
                    print("Found bookmark: {row}".format(row=row))
                return True

    @staticmethod
    def _find_and_return_bookmark(tx, bookmark):
        query = (
                    "MATCH (b:Bookmark) "
                    "WHERE b.name = $bookmark "
                    "RETURN b.name AS name"
                )
        result = tx.run(query, bookmark=bookmark)
        return [row["name"] for row in result]

    # Create relationship between person and bookmark
    # ----------------------------------------------------------------------
    def create_relationship_person_bookmark(self, person_name, bookmark_name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            exist = self.find_person(person_name)
            if exist == True:
                session.write_transaction(self._create_relationship_person_bookmark, person_name, bookmark_name)
                print("Created relationship between person and bookmark")
            else:
                print("Person {p} doesn't exists".format(p=person_name))

    @staticmethod
    def _create_relationship_person_bookmark(tx, person_name, bookmark_name):
        query = (
            "match (p:User), (b:Bookmark) where p.name = $person_name AND b.name = $bookmark_name merge (p)-[:CREATED_BOOKMARK]->(b)"
        )
        result = tx.run(query, person_name=person_name, bookmark_name=bookmark_name)
        try:
            return [{"p": row["p"]["person_name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))

    # Create relationship between person and tag
    # ----------------------------------------------------------------------
    def create_relationship_person_tag(self, person_name, tag_name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            exist = self.find_person(person_name)
            if exist == True:
                session.write_transaction(self._create_relationship_person_tag, person_name, tag_name)
                print("Created relationship between person and tag")
            else:
                print("Person {p} doesn't exists".format(p=person_name))

    @staticmethod
    def _create_relationship_person_tag(tx, person_name, tag_name):
        query = (
            "match (p:User), (t:Tag) where p.name = $person_name AND t.name = $tag_name merge (p)-[:INTERESTED_IN]->(t)"
        )
        result = tx.run(query, person_name=person_name, tag_name=tag_name)
        try:
            return [{"p": row["p"]["person_name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))

    # Create relationship between bookmark and tag
    # ----------------------------------------------------------------------
    def create_relationship_bookmark_tag(self, bookmark_name, tag_name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            exist = self.find_bookmark(bookmark_name)
            if exist == True:
                session.write_transaction(self._create_relationship_bookmark_tag, bookmark_name, tag_name)
                print("Created relationship between bookmark and tag")
            else:
                print("Bookmark {p} doesn't exists".format(p=bookmark_name))

    @staticmethod
    def _create_relationship_bookmark_tag(tx, bookmark_name, tag_name):
        query = (
            "match (b:Bookmark), (t:Tag) where b.name = $bookmark_name AND t.name = $tag_name merge (b)-[:HAS_TAG]->(t)"
        )
        result = tx.run(query, bookmark_name=bookmark_name, tag_name=tag_name)
        try:
            return [{"p": row["p"]["bookmark_name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))

if __name__ == "__main__":
    app = App()
    # app.create_relationship_person_bookmark("Ruben", "Bavo kerk")
    # app.create_bookmark("Bavo kerk")
    # app.create_tag("Horeca")
    # app.find_person("Mark")
    app.close()
