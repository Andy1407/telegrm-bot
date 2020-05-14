import sqlite3


def condition(conditions):
    condition = []
    for i in list(conditions.items()):
        condition.append("=".join(i))
    return ' AND '.join(condition)


class Database:
    def __init__(self, name_database):
        self.name_database = name_database
        self.connection = sqlite3.connect(f"{name_database}.sqlite3", check_same_thread=True)
        self.cursor = self.connection.cursor()

    def add(self, table, **value):
        sql = f"INSERT INTO {table} ({', '.join(value)}) VALUES ({', '.join(list(value.values()))})"
        self.cursor.execute(sql)
        self.connection.commit()

    def remove(self, table, **conditions):
        if conditions:
            sql = f"DELETE FROM {table} WHERE ({condition(conditions)})"
        else:
            sql = f"DELETE FROM {table}"
        self.cursor.execute(sql)
        self.connection.commit()

    def edit(self, table, values, **conditions):
        value = []
        for i in values:
            value.append(f"{i} = {values[i]}")
        if conditions:
            sql = f"UPDATE {table} SET {', '.join(value)} WHERE {condition(conditions)}"
        else:
            sql = f"UPDATE {table} SET {', '.join(value)}"
        self.cursor.execute(sql)
        self.connection.commit()

    def show(self, table, show_column="*", **conditions):
        if conditions:
            sql = f"SELECT {show_column} FROM {table} WHERE {condition(conditions)}"
        else:
            sql = f"SELECT {show_column} FROM {table}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def add_tables(self, name_table, columnKEY=None, columnKEY2=None, tableKEY=None, **columns):
        column = []
        for i in columns:
            column.append(f"{i} {columns[i]}")

        if columnKEY and columnKEY2 and tableKEY:
            column.append(f"FOREIGN KEY ({columnKEY}) REFERENCES {tableKEY}({columnKEY2}))")

        sql = f"CREATE TABLE IF NOT EXISTS {name_table} ({', '.join(column)})"
        self.cursor.execute(sql)

        self.connection.commit()