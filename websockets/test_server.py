import unittest
import pythonsqlite

db_file = "C:\\sqlite\db\pythonsqlite.db"


class TestServer(unittest.TestCase):

    def test_example(self):
        # print("example test")
        result = 2 + 2
        self.assertEqual(result, 4)

    def test_create_connection(self):
        # print("create connection test")
        conn = pythonsqlite.create_connection(db_file)
        self.assertIsNotNone(conn)




    def test_create_project(self):
        conn = pythonsqlite.create_connection(db_file)
        sql = """ CREATE TABLE IF NOT EXISTS projects (
                                           id integer PRIMARY KEY,
                                           name text NOT NULL,
                                           begin_date text,
                                           end_date text,
                                           code txt
                                       ); """
        pythonsqlite.create_table(conn, sql)
        project = ('output', '2015-01-01', '2015-01-30', 'sourcecode')
        id = pythonsqlite.create_project(conn, project)
        self.assertIsNotNone(id)

    def test_compileSourceCode(self):
        output = pythonsqlite.compile_source_code("print(2)")
        self.assertEqual(output,'2\n')

    def test_generateComparisonRaport(self):
        allProjects = pythonsqlite.select_all_projects()
        raport = pythonsqlite.generate_comparison_raport(allProjects, "print(2)")
        self.assertIsNotNone(raport)

    def test_initialize_db(self):
        result = pythonsqlite.initialize_db()
        self.assertTrue(result)

