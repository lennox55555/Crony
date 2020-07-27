import json
import pymysql
import sys
import re

REGION = 'us-west-2'

rds_host = 'cronydatabase.clzq708gdpes.us-west-2.rds.amazonaws.com'
name = 'admin'
password = 'Super1262Secure2020'
db_name = 'crony'

# conn = pymysql.connect(rds_host, user = name, passwd = password, db = db_name, connect_timeout = 5)
def save_events(event):
    global result
    result = []
    global errorMessage
    errorMessage = ""
    global conn
    conn = pymysql.connect(rds_host, user = name, passwd = password, db = db_name, connect_timeout = 5)

def lambda_handler(event, context):
    httpMethod = event.get("context").get("http-method")  # From Mapping Template
    resourcePath = event.get("context").get("resource-path")
    rootPath, extendedPath = splitResourcePath(resourcePath)
    save_events(event)
    print("Event is: ")
    print(event)
    global errorMessage  # Python is weird
    # print("CONTEXT", dir(context))
    if rootPath == "/user":
        if httpMethod == "GET":
            if extendedPath == "/{id}":
                id = event.get("params").get("path").get("id")
                result = returnExecution(displayPerson, "User", id)
                if result == []:
                    errorMessage = "400 Bad Request: User does not exist!"
            else:
                result = returnExecution(displayTable, "User")
        elif httpMethod == "POST":
            queryString = event.get("params").get("querystring")
            result = returnExecution(addUser, queryString.get("first_name"), queryString.get("last_name"), queryString.get("email"), queryString.get("address1"), queryString.get("address2"), queryString.get("password"))
        elif httpMethod == "DELETE":
            if extendedPath == "/{id}":
                id = event.get("params").get("path").get("id")
                idArr = [id]
                result = returnExecution(deleteUser, idArr)
            else:
                # result = returnExecution(deleteUser, event.get("users_to_delete"))
                pass
    elif rootPath == "/profile":
        if httpMethod == "GET":
            if extendedPath == "/{id}":
                id = event.get("params").get("path").get("id")
                result = returnExecution(displayPerson, "Profile", id)
                if result == []:
                    errorMessage = "400 Bad Request: Profile does not exist!"
            else:
                result = returnExecution(displayTable, "Profile")
        elif httpMethod == "POST":
            queryString = event.get("params").get("querystring")
            if extendedPath == "/{id}":
                id = event.get("params").get("path").get("id")
                result = returnExecution(addProfile, id, queryString.get("username"), queryString.get("age"), queryString.get("gender"), queryString.get("city"), queryString.get("state"), queryString.get("hiking_level"))
        elif httpMethod == "DELETE":
            if extendedPath == "/{id}":
                id = event.get("params").get("path").get("id")
                result = returnExecution(deleteProfile, id)
    else:
        result = "FAILED"
    # result = displayColumnNames("User")
    # result = addUser("Aayush", "Saxena", "aayush19saxena@gmail.com", "Somewhere in Washington")
    print("Data from RDS...")
    print("Result: " + str(result))
    if errorMessage != "":
        raise LambdaError(errorMessage)
    return {
        'statusCode': 200,
        'body': result,
        # 'body': json.dumps(str(event)),
        # 'context': dir(context),
        # 'TEST1': event.get("context"),
        # 'TEST2': event.get("params").get("path").get("id")
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        }
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
    if table == "User":
        cur.execute(f"""
                    SELECT * FROM {table}
                    WHERE id = {id}
                    """)
    elif table == "Profile":
        cur.execute(f"""
                    SELECT * FROM {table}
                    WHERE profile_id = {id}
                    """)

def addUser(firstName, lastName, email, address1, address2=None, password=None):
    cur.execute(f"""
                INSERT INTO User(first_name, last_name, email, address1, address2, password)
                VALUES("{firstName}", "{lastName}", "{email}", "{address1}", "{address2}", "{password}")
                """)

def deleteUser(idArr):
    for id in idArr:
        cur.execute(f"""
                    DELETE FROM User
                    WHERE id = {id}
                    """)
                    
def doesPersonExist(table, id):
    with conn.cursor() as cur2:
        # cur2.execute("SELECT 0 FROM User")
        if table == "User":
            cur2.execute(f"""
                         SELECT 1
                         FROM User
                         WHERE id = {id}
                         """)
        elif table == "Profile":
            cur2.execute(f"""
                         SELECT 1
                         FROM Profile
                         WHERE profile_id = {id}
                         """)
        conn.commit()
        cur2.close()
    return (cur2.fetchone() != None)

def addProfile(id, username, age, gender, city, state, hikingLevel):
    if doesPersonExist("User", id):
        if not doesPersonExist("Profile", id):
            cur.execute(f"""
                        INSERT INTO Profile(profile_id, username, age, gender, city, state, hiking_level)
                        VALUES("{id}", "{username}", "{age}", "{gender}", "{city}", "{state}", "{hikingLevel}")
                        """)
        else:
            errorMessage = "400 Bad Request: Profile already exists!"
    else:
        errorMessage = "400 Bad Request: User does not exist!"

def deleteProfile(id):
    cur.execute(f"""
                DELETE FROM Profile
                WHERE profile_id = {id}
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
                
def splitResourcePath(resourcePath):
    pattern = r"(/[^/]+)(/.+)?"
    match = re.match(pattern, resourcePath)
    return match.groups()
    
class LambdaError(Exception):
    pass
