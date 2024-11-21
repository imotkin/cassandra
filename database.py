from cassandra.cluster import Cluster
from cassandra.query import ordered_dict_factory


class Database:
    cluster: Cluster
    sessions: dict

    def __init__(self, test=False):
        if test:
            return
        self.cluster = Cluster(["127.0.0.1"])
        self.sessions = {}

    def session(self, keyspace: str):
        session = self.cluster.connect(keyspace)
        session.row_factory = ordered_dict_factory
        return session

    @property
    def hosts(self):
        self.cluster.connect()

        return [
            {
                "host": f"{host.endpoint._address}:{host.endpoint._port}",
                "up": host.is_up,
            }
            for host in self.cluster.metadata.all_hosts()
        ]

    @property
    def movie(self):
        if "movie" in self.sessions:
            return self.sessions["movie"]
        else:
            created = self.session("movie")
            self.sessions["movie"] = created
            return created

    @property
    def ticket(self):
        if "ticket" in self.sessions:
            return self.sessions["ticket"]
        else:
            created = self.session("ticket")
            self.sessions["ticket"] = created
            return created
