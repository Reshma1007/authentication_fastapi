from fastapi import FastAPI
from neo4j import GraphDatabase
import app as app

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
session = driver.session()


@app.post("/create/<string:username>&<int:pwd>", response_model=["POST"])
async def create_node(name, id):
    q1 = """
    create (n:Admin{"name": name, "id" : id}
    """
    map={"name": name, "id": id}
    try:
        session.run(q1, map)
        return (f"admin node is created with admin name={name}  and id={id}")
    except Exception as e:
        return (str(e))


    app.run(port=7474)

