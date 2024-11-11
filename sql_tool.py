# -*- coding: UTF-8 -*-

import psycopg2


class SQLTool:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def connect_to_db(self):
        # 连接到 PostgreSQL 数据库
        conn = None
        try:
            conn = psycopg2.connect(host=self.host, port=self.port, database=self.database,
                                    user=self.user, password=self.password)
            print("连接成功")
            self.conn = conn
        except Exception as e:
            print(f"连接失败：{e}")
        return conn

    def execute_sql_file(self, file_path):

        cursor = self.conn.cursor()

        with open(file_path, 'r') as file:
            sql = file.read()
        cursor.execute(sql)  # 执行SQL文件中的所有语句

        cursor.close()

    def analyze_data(self, query):

        cursor = self.conn.cursor()

        cursor.execute(query)
        records = cursor.fetchall()

        cursor.close()

        return records

    def get_column_names(self, table_name):

            query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';"

            records = self.analyze_data(query)

            column_names = [column[0] for column in records]

            return column_names

    def get_all_column_names(self):

        query = """
            SELECT table_name, column_name
            FROM information_schema.columns
            WHERE table_schema = 'eemstsmx'
            ORDER BY table_name, ordinal_position;"""

        records = self.analyze_data(query)

        columns_list = {}
        for table_name, column_name in records:
            if table_name not in columns_list:
                columns_list[table_name] = []
            columns_list[table_name].append(column_name)

        return columns_list


    def get_column_counts(self, table_name, column_name):

        query = f"""
            SELECT {column_name}, COUNT(*) AS count
            FROM {table_name}
            GROUP BY {column_name}
            ORDER BY count DESC;
            """

        records = self.analyze_data(query)

        return records


    def get_property_specific_value(self, table, column, value, property=None, order_by=None, limit=None):

        query = f"SELECT * FROM {table} WHERE {column} = {value};"

        if property is not None:
            query = f"SELECT id, collect_time, {property} FROM {table} WHERE {column} = {value};"
            if order_by is not None:
                query = f"SELECT id, collect_time, {property} FROM {table} WHERE {column} = {value} ORDER BY {order_by};"

        elif limit is not None:
            query = f"SELECT * FROM {table} WHERE {column} = {value} LIMIT 10;"

        records = self.analyze_data(query)

        property_list = []
        for id, collect_time, prop in records:
            property_list.append([id, collect_time, prop])

        return property_list


if __name__ == "__main__":
    # 数据库连接配置
    HOST = 'localhost'  # 数据库主机
    PORT = 15432
    DATABASE = 'eemstsmx'
    USER = 'postgres'
    PASSWORD = '123456'

    # SQL 文件路径
    # sql_file_path = 'D:/Docker/timescaledb/data/eemstsmx/eemstsmx.sql'

    db = SQLTool(HOST, PORT, DATABASE, USER, PASSWORD)
    # 连接到数据库
    conn = db.connect_to_db()

    if conn:
        cursor = conn.cursor()

        # 可以在此执行分析数据的查询，下面是一个示例查询
        query = 'SELECT * FROM eemstsmx.ts_g_gas LIMIT 10;'  # 替换为您的查询
        cursor.execute(query)
        records = cursor.fetchall()

        # 使用 pandas 数据框来分析数据
        import pandas as pd
        df = pd.DataFrame(records, columns=[desc[0] for desc in cursor.description])
        print(df)
        cursor.close()

        columns = db.get_column_names('ts_g_gas')
        print("列名:", columns)
        # 执行 SQL 文件
        # db.execute_sql_file(sql_file_path)

        conn.close()
