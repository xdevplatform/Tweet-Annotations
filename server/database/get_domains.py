import requests
import yaml
import json
from manage_db import create_connection, create_table
from authentication import Authentication

authentication = Authentication()

def get_annotations(authentication):

    connection = create_connection(r"./annotations.db")
    cursor = connection.cursor()

    url = "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=context_annotations"
    authentication = authentication.bearer_oauth

    response = requests.get(url=url, auth=authentication, stream=True)
    print(response.status_code)

    annotation = []

    for response_line in response.iter_lines():
        json_response = json.loads(response_line)

        if "context_annotations" in json_response["data"]:
            for item in json_response["data"]["context_annotations"]:
                domain_id = item["domain"]["id"]
                domain_name = item["domain"]["name"] 
                entity_id = item["entity"]["id"] 
                entity_name = item["entity"]["name"] 

                sql = f""" INSERT OR IGNORE INTO domains (domain_id, domain_name)
                           VALUES ('{domain_id}', '{domain_name}');
                       """
                
                print(sql)
                cursor.execute(sql)
                
                sql = f""" INSERT OR IGNORE INTO entities (entity_id, entity_name, domain_id)
                           VALUES ('{entity_id}', '{entity_name}', '{domain_id}');
                       """ 
                
                print(sql)
                cursor.execute(sql)
                connection.commit()

    # Close database connection
    connection.close()     

def initialise_annotations_db():
    
    sql_create_domains_table = """ CREATE TABLE IF NOT EXISTS domains (
                                              domain_id text NOT NULL PRIMARY KEY,
                                              domain_name text NOT NULL
                                          ); """

    sql_create_entities_table = """ CREATE TABLE IF NOT EXISTS entities (
                                               entity_id text NOT NULL PRIMARY KEY,
                                               entity_name text NOT NULL, 
                                               domain_id text NOT NULL
                                           ); """

    # Create a DB connection
    connection = create_connection(r"./annotations.db")

    #Create tables for annotation domains and for annotation entities
    if connection is not None: 
        create_table(connection, sql_create_domains_table)
        create_table(connection, sql_create_entities_table)
    else: 
        print("Error: cannot create the database connection.")
    
    # Close database connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    # initialise_annotations_db()
    get_annotations(authentication)