import os

import psycopg2


def condition(conditions):
    condition = []
    for i in conditions:
        condition.append(f"{i}={conditions[i]}")
    return ' AND '.join(condition)


class Database:
    """
    connect to database
    """

    def __init__(self):
        self.connect()

    def connect(self):
        self.connection = psycopg2.connect(os.environ.get('DATABASE_URL'))
        self.cursor = self.connection.cursor()

    def add(self, table, **value):
        """
        add data into the database
        :param str table: name of table for edit
        :param str value: data, which you  want to insert
        :return: nothing
        """
        sql = f"INSERT INTO {table} ({', '.join(value)}) VALUES ({', '.join(list(value.values()))})"
        self.cursor.execute(sql)
        self.connection.commit()

    def remove(self, table, **conditions):
        """
        remove of data out of the database
        :param str table: name of table for remove data
        :param str conditions: conditions for data, which you want to remove
        :return: nothing
        """
        if conditions:
            sql = f"DELETE FROM {table} WHERE ({condition(conditions)})"
        else:
            sql = f"DELETE FROM {table}"
        self.cursor.execute(sql)
        self.connection.commit()

    def edit(self, table, values, **conditions):
        """
        edit of data in the database
        :param str table: name of data, which you need to edit
        :param dict values: value, which you need to edit (column: value)
        :param str conditions: conditions for data, which you want to edit
        :return: nothing
        """
        value = []
        for i in values:
            value.append(f"{i} = {values[i]}")
        if conditions:
            sql = f"UPDATE {table} SET {', '.join(value)} WHERE {condition(conditions)}"
        else:
            sql = f"UPDATE {table} SET {', '.join(value)}"
        self.cursor.execute(sql)
        self.connection.commit()

    def select(self, table, show_column="*", **conditions):
        """
        show data form database
        :param str table: name of the data table that you want to view
        :param str show_column: columns, which you want to view
        :param str conditions: conditions of data, which you want to view
        :return: nothing
        """
        if conditions:
            sql = f"SELECT {show_column} FROM {table} WHERE {condition(conditions)}"
        else:
            sql = f"SELECT {show_column} FROM {table}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def add_table(self, name_table, **columns):
        """
        add the table into the database
        :param str name_table: name of table, which you want to add
        :param str columns: columns in table
        :return: nothing
        """
        column = []
        for i in columns:
            column.append(f"{i} {columns[i]}")

        sql = f"CREATE TABLE IF NOT EXISTS {name_table} ({', '.join(column)})"
        self.cursor.execute(sql)

        self.connection.commit()
