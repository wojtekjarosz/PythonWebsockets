import asyncio
import websockets
import difflib
import traceback

from io import StringIO
import sys

import sqlite3
from sqlite3 import Error


async def hello(websocket, path):
    initialize_db()
    message = await websocket.recv()
    print(f"Received message from client: {message}")
    greeting = f"Hello!"

    await websocket.send(greeting)
    print(f"Sending message to client: {greeting}")

    try :
        sourceCode = await websocket.recv()

    except:
        print("Error while receiving source file")
        return

    print(f"Received code from client:\n{sourceCode} ")

    # Kompilacja przesłanego kodu
    isSucces = compileSourceCode(sourceCode)

    if isSucces:
        # Jesli się udało to widomośc do klienta że sie udało
        await websocket.send("Successful compilation.")
    else:
        # Jeśli sie nie udalo to wiadomość że sie nie udało
        await websocket.send("Compilation failed.")



def compileSourceCode(sourceCode):
    try:
        code = compile(sourceCode, "code.py", 'exec')
        # redirect stdout to variable
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        exec(code)  # Wykonanie kodu

        # restore stdout
        sys.stdout = old_stdout

        print(mystdout.getvalue())
        output = mystdout.getvalue()

    except:
        print("Nie udało sie skompilowac kodu.")
        return False

    # clear projects table
    # delete_all_projects()

    insert_output(output, sourceCode)
    allProjects = select_all_tasks()
    select_task_by_id(1)
    raport = generateComparisonRaport(allProjects, sourceCode)
    print("PRINTING REPORT")
    print(raport)

    return True


def generateComparisonRaport(allProjects, sourceCode):
    report = "REPORT: \n"

    for row in allProjects:
        print("COMPARE WITH PROJECT_ID: " + str(row[0]))
        report += "COMPARE WITH: " + str(row[0]) + "\n"

        project = ''.join(row[4]).splitlines(1)
        source = sourceCode.splitlines(1)

        diff = difflib.ndiff(project, source)
        results = ''.join(diff)
        print(results)
        report += results + "\n\n"
    report += "THE END\n"
    return report


def create_connection(db_file):
    """ create a database connection to a database that resides
        in the memory
    """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    # finally:
    #     conn.close()

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date,code)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid

def delete_project(conn, id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM projects WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))


def delete_all_projects():
    """
    Delete all rows in the tasks table
    :param conn: Connection to the SQLite database
    :return:
    """
    conn = create_connection("C:\\sqlite\db\pythonsqlite.db")
    with conn:
        sql = 'DELETE FROM projects'
        cur = conn.cursor()
        cur.execute(sql)
        print("Deleting all projects")

def insert_output(output, sourceCode):
    conn = create_connection("C:\\sqlite\db\pythonsqlite.db")
    with conn:
        project = (output, '2015-01-01', '2015-01-30', sourceCode)
        project_id = create_project(conn, project)
        print(project_id)


def select_all_tasks():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    conn = create_connection("C:\\sqlite\db\pythonsqlite.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects")

    rows = cur.fetchall()

    print("All projects: ")
    for row in rows:
        print(row)

    return rows


def select_task_by_id(id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    conn = create_connection("C:\\sqlite\db\pythonsqlite.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE id=?", (id,))

    rows = cur.fetchall()


def initialize_db():
    print("Initializing db")

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                           id integer PRIMARY KEY,
                                           name text NOT NULL,
                                           begin_date text,
                                           end_date text,
                                           code txt
                                       ); """

    conn = create_connection("C:\\sqlite\db\pythonsqlite.db")
    if conn is not None:
        create_table(conn, sql_create_projects_table)
        print("Created table projects")
        # create a new project
        # project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
        # project_id = create_project(conn, project)
        # print(project_id)
        # project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
        # project_id = create_project(conn, project)
        # print(project_id)

    else:
        print("Error! Cannot create the database connection")


# if __name__ == '__main__':
#     initialize_db()

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
