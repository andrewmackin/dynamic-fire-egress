from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import phillips
import os

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def init_db(self):
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self._init_db)
    
    def get_sign_ids(self):
        with self.driver.session(database="neo4j") as session:
            return session.execute_read(self._get_sign_ids)

    def set_fire(self, alarm_id):
        with self.driver.session(database="neo4j") as session:
            return session.execute_write(self._update_delta, alarm_id)

    def shortest_path(self, sign_id):
        with self.driver.session(database="neo4j") as session:
            return session.execute_read(self._shortest_path, sign_id)

    @staticmethod
    def _init_db(tx):
        tx.run("MATCH (n) DETACH DELETE n")
        tx.run(phillips.QUERY)

    @staticmethod
    def _get_sign_ids(tx):
        result = tx.run("MATCH (n:Sign) WHERE NOT (n:Exit) RETURN n")
        return [row['n']['id'] for row in result.data()]

    @staticmethod
    def _update_delta(tx, alarm_id):
        query = ("MATCH path = "
        "(startNode:Alarm WHERE startNode.id = $alarm_id)-[:CONNECTED_TO*1]->(finalNode:Delta) "
        "MATCH (s:Delta) WHERE s in nodes(path) SET s:Fire RETURN s")
        result = tx.run(query, alarm_id = alarm_id)
        return result.data()

    @staticmethod
    def _shortest_path(tx, sign_id):
        query = ("MATCH path = (startSign:Sign "
        "WHERE startSign.id = $sign_id)-[:CONNECTED_TO*]->(exit:Exit) "
        "WHERE NONE(x in nodes(path) WHERE x:Fire) RETURN path ORDER BY "
        "REDUCE(dist = 0, rela in relationships(path) | dist + rela.cost) "
        "ASC LIMIT 1")
        result = tx.run(query, sign_id = sign_id)
        return result.data()