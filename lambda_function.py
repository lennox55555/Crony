import json
import pymysql
import sys

REGION = 'us-west-2'

rds_host = 'cronydatabase.clzq708gdpes.us-west-2.rds.amazonaws.com'
name = 'admin'
password = 'Super1262Secure2020'
db_name = 'crony'

# conn = pymysql.connect(rds_host, user = name, passwd = password, db = db_name, connect_timeout = 5)
def save_events(event):
    global result
    result = []
    global conn
    conn = pymysql.connect(rds_host, user = name, passwd = password, db = db_name, connect_timeout = 5)

def lambda_handler(event, context):
    httpMethod = event.get("context").get("http-method")  # From Mapping Template
    resourcePath = event.get("context").get("resource-path")
    save_events(event)
    print("Event is: ")
    print(event)
    # print("CONTEXT", dir(context))
    result = None
    if httpMethod == "GET":
        if resourcePath == "/user/{id}":
            id = event.get("params").get("path").get("id")
            result = returnExecution(displayPerson, "User", id)
        else:
            result = returnExecution(displayTable, "User")
    elif httpMethod == "POST":
        result = returnExecution(addUser, event.get("first_name"), event.get("last_name"), event.get("email"), event.get("address1"), event.get("address2"))
    elif httpMethod == "DELETE":
        if resourcePath == "/user/{id}":
            id = event.get("params").get("path").get("id")
            idArr = [id]
            result = returnExecution(deleteUser, idArr)
        else:
            result = returnExecution(deleteUser, event.get("users_to_delete"))
    # result = displayColumnNames("User")
    # result = addUser("Aayush", "Saxena", "aayush19saxena@gmail.com", "Somewhere in Washington")
    print("Data from RDS...")
    print("Result: " + str(result))
    return {
        'statusCode': 200,
        'body': result
        # 'body': json.dumps(str(event)),
        # 'context': dir(context),
        # 'TEST1': event.get("context"),
        # 'TEST2': event.get("params").get("path").get("id")
    }

def main(event, context):
    save_events(event)
    
def returnExecution(func, *args):
    global cur
    with conn.cursor() as cur:
        func(*args)  # Unpacks args array into function parameters
        conn.commit()
        cur.close()
        for row in cur:
            print("HERE 1")
            result.append(list(row))
    return result
    
def displayTable(table):
    # cur.execute("""insert into User (id, firstName) values( %s, '%s')""" % (event['id'], event['name']))
    cur.execute(f"""SELECT * FROM {table}""")

def displayPerson(table, id):
    cur.execute(f"""
                SELECT * FROM {table}
                WHERE id = {id}
                """)

def addUser(firstName, lastName, email, address1, address2=None):
    cur.execute(f"""
                INSERT INTO User(first_name, last_name, email, address1, address2)
                VALUES("{firstName}", "{lastName}", "{email}", "{address1}", "{address2}")
                """)

def deleteUser(idArr):
    for id in idArr:
        cur.execute(f"""
                    DELETE FROM User
                    WHERE id = {id}
                    """)

def displayColumnNames(table):
    # cur.execute(f"""
    #             SELECT *
    #             FROM INFORMATION_SCHEMA.COLUMNS
    #             WHERE TABLE_NAME = N'{table}'
    #             """)
    cur.execute(f"""DESCRIBE {table}""")

def filterByExperience(min, max=5):  # max chosen arbitrarily
    cur.execute(f"""
                SELECT username, User.id
                FROM Profile JOIN User ON (Profile.id = User.id) 
                WHERE hikingLevel >= {min}
                AND hikingLevel <= {max}
                """)
