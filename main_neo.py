from fastapi import FastAPI, Depends
from neo4j import GraphDatabase
import csv


app = FastAPI()

with open("cred.txt")as f1:
    data = csv.reader(f1, delimiter=",")
    for row in data:
        username = row[0]
        pwd = row[1]
        uri = row[2]
print(username, pwd, uri)
driver = GraphDatabase.driver(uri=uri, auth=(username, pwd))
session = driver.session


def get_driver(uri, username, pwd):
    driver = GraphDatabase.driver(uri, auth=(username, pwd))
    return driver

def run_graph_queries(uri, username, pwd, queries, do_graph_queries):
    driver = get_driver(uri, username, pwd)
    with driver.session() as session:
        r = session.read_transaction(do_graph_queries, queries)
        return r


def do_graph_query(tx, queries):
    result = []
    for query in queries:
        res = tx.run(query['query'], query['parameters'])
        result.append(res.graph())
    return result


app.run_graph_queries = lambda x: run_graph_queries(neo4j_uri, username, pwd, x)
