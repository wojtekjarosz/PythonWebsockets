import asyncio
import websockets
import difflib
import traceback

from io import StringIO
import sys

import sqlite3
from sqlite3 import Error

def compile_source_code(sourceCode):
    """"
    This function attempts to compile the received source code
    Successful Compilation - returns the results of the compiled source code
    Compilation Failure - returns empty variable
    :param sourceCode code to compile
    :return output results of the compiled code or empty variable
    """
    try:
        code = compile(sourceCode, "code.py", 'exec')
        # redirect stdout to variable
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        exec(code)

        # restore stdout
        sys.stdout = old_stdout

        print(mystdout.getvalue())
        output = mystdout.getvalue()

        return output
    except:
        print("Compilation failed.")
        return


def generate_comparison_raport(allProjects, sourceCode):
    """"
    This function compares the source code with codes stored in the database
    :param allProjects source codes of all stored projects
    :param sourceCode code for comparison
    :return report the comparison report
    """
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
    db_file = "C:\\sqlite\db\pythonsqlite.db"
    conn = create_connection(db_file)
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


def select_all_projects():
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


def select_project_by_id(id):
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
        return True
    else:
        print("Error! Cannot create the database connection")
        return False


# if __name__ == '__main__':
#     initialize_db()
