from datetime import datetime
from sqlite3 import Row
from typing import Sequence
import sqlalchemy as db


class Database:
    def __init__(self) -> None:
        self.engine = db.create_engine("sqlite:///logs.db")
        self.conn = self.engine.connect()
        self.metadata = db.MetaData()
        self.tables = {}

    def __repr__(self) -> str:
        return f"Database({self.engine})"

    def create_table(self, table_name, columns):
        return db.Table(table_name, self.metadata, *columns)

    def insert(self, table, values):
        return self.conn.execute(table.insert(), values)

    def select(self, table, *columns):
        query = db.text(
            f"SELECT {', '.join([str(column) for column in columns])} FROM {table.name}"
        )
        return self.conn.execute(query)

    def select_where(self, table, where, *columns):
        query = db.text(
            f"SELECT {', '.join([str(column) for column in columns])} FROM {table.name} WHERE {where}"
        )
        return self.conn.execute(query)

    def update(self, table, where, values):
        return self.conn.execute(table.update().where(where).values(values))

    def delete(self, table, where):
        return self.conn.execute(table.delete().where(where))

    def display(self, result: Sequence[Row]) -> None:
        for row in result:
            print(row)

    def check_if_exists(self, table, where) -> bool:
        result = self.select_where(table, where, '*')
        return result.fetchone() is not None

    def run(self):
        self.metadata.create_all(self.engine)


def create_database() -> Database:
    data_base = Database()

    # Définition des tables
    infos = data_base.create_table(
        "infos",
        [
            db.Column("user_id", db.Integer(), db.ForeignKey("users.id")),
            db.Column("country", db.String(255)),
            db.Column("countryCode", db.String(255)),
            db.Column("region", db.String(255)),
            db.Column("regionName", db.String(255)),
            db.Column("city", db.String(255)),
            db.Column("zip", db.String(255)),
            db.Column("isp", db.String(255)),
            db.Column("addr", db.String(255)),
            db.Column("created_at", db.TIMESTAMP),
        ],
    )

    users = data_base.create_table(
        "users",
        [
            db.Column("id", db.Integer(), primary_key=True),
            db.Column("ip", db.String(255)),
            db.Column("created_at", db.TIMESTAMP),
        ],
    )

    logs = data_base.create_table(
        "logs",
        [
            db.Column("pathname", db.String(255)),
            db.Column("filename", db.String(255)),
            db.Column("body", db.Text),
            db.Column("user_id", db.Integer(), db.ForeignKey("users.id")),
            db.Column("created_at", db.TIMESTAMP),
        ],
    )
    # Création des contraintes de clé étrangère supplémentaires
    db.ForeignKeyConstraint(["id"], ["infos.user_id"])

    data_base.tables = {"users": users, "infos": infos, "logs": logs}
    return data_base
