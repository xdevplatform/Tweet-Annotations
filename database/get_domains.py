import requests
import yaml
import json
from manage_db import create_connection, create_table
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth

def get_annotations():
    pass

def initialise_annotations_db():

    print("test")
    
    sql_create_annotation_domains_table = """ CREATE TABLE IF NOT EXISTS annotation_domains (
                                              id integer PRIMARY KEY,
                                              domain_id text NOT NULL,
                                              domain_name text NOT NULL
                                          ); """

    sql_create_annotation_entities_table = """ CREATE TABLE IF NOT EXISTS annotation_entities (
                                               id integer PRIMARY KEY,
                                               entity_id text NOT NULL,
                                               entity_name text NOT NULL
                                           ); """

    # Create a DB connection
    connection = create_connection(r"./annotations.db")

    #Create tables for annotation domains and for annotation entities
    if connection is not None: 
        create_table(connection, sql_create_annotation_domains_table)
        create_table(connection, sql_create_annotation_entities_table)
    else: 
        print("Error: cannot create the database connection.")
    
    # Close database connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    get_annotations()
    initialise_annotations_db()