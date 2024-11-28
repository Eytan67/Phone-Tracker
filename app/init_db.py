from flask import current_app

from neo4j import GraphDatabase


def init_driver(uri, username, password):
    try:
        current_app.driver = GraphDatabase.driver(uri, auth=(username, password))
        current_app.driver.verify_connectivity()
    except Exception as e:
        current_app.logger.error(f"Failed to initialize Neo4j driver: {e}")
        raise e
    return current_app.driver

def get_driver():
    return current_app.driver

def close_driver():
    if current_app.driver != None:
        current_app.driver.close()
        current_app.driver = None

        return current_app.driver

