from datetime import datetime
from sqlite3 import Row
from typing import Sequence
import sqlalchemy as db

from src.Honeypotclass import Honeypot
from src.status_type import Status


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
        return self.conn.execute(table.update().where(db.text(where)).values(values))

    def delete(self, table, where):
        return self.conn.execute(table.delete().where(where))

    def display(self, result: Sequence[Row]) -> None:
        for row in result:
            print(row)

    def check_if_exists(self, table, where) -> bool:
        result = self.select_where(table, where, "*")
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
            db.Column("user_id", db.Integer(), db.ForeignKey("users.id")),
            db.Column("status", db.String(255)),
            db.Column("path", db.String(255)),
            db.Column("size", db.Float()),
            db.Column("created_at", db.TIMESTAMP),
        ],
    )
    # Création des contraintes de clé étrangère supplémentaires
    db.ForeignKeyConstraint(["id"], ["infos.user_id"])

    data_base.tables = {"users": users, "infos": infos, "logs": logs}
    return data_base


def insert_infos(server: Honeypot, ip: str, infos: dict, address: str) -> None:
    if server.bdd.check_if_exists(server.bdd.tables["users"], f"ip = '{ip}'"):
        user_id = server.bdd.select_where(
            server.bdd.tables["users"], f"ip = '{ip}'", "id"
        ).fetchone()[0]
        logs_user_values = {
            "user_id": user_id,
            "path": server.logger.get_file(),
            "size": 0,
            "status": Status.USED.value,
            "created_at": datetime.now(),
        }
        server.bdd.insert(server.bdd.tables["logs"], [logs_user_values])
        server.bdd.conn.commit()
        return
    else:
        result = server.bdd.insert(
            server.bdd.tables["users"], {"ip": ip, "created_at": datetime.now()}
        )
        user_id = result.lastrowid
        if infos is not None:
            infos_user_values = {
                "user_id": user_id,
                "country": infos.get("country", ""),
                "countryCode": infos.get("countryCode", ""),
                "region": infos.get("region", ""),
                "regionName": infos.get("regionName", ""),
                "city": infos.get("city", ""),
                "zip": infos.get("zip", ""),
                "isp": infos.get("isp", ""),
                "addr": address if address else "",
                "created_at": datetime.now(),
            }
        else:
            infos_user_values = {
                "user_id": user_id,
                "country": "",
                "countryCode": "",
                "region": "",
                "regionName": "",
                "city": "",
                "zip": "",
                "isp": "",
                "addr": address if address else "",
                "created_at": datetime.now(),
            }
        server.bdd.insert(server.bdd.tables["infos"], [infos_user_values])

        logs_user_values = {
            "user_id": user_id,
            "path": server.logger.get_file(),
            "size": 0,
            "status": Status.USED.value,
            "created_at": datetime.now(),
        }
        server.bdd.insert(server.bdd.tables["logs"], [logs_user_values])
        server.bdd.conn.commit()


def update_logs(server: Honeypot, status: str, size: float) -> None:
    server.bdd.update(
        server.bdd.tables["logs"],
        f"path = '{server.logger.get_file()}'",
        {"status": status, "size": size},
    )
    server.bdd.conn.commit()
