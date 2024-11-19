from cassandra.cluster import Cluster


class Database:
    cluster: Cluster

    def __init__(self, cluster):
        self.cluster = cluster

    @property
    def movie(self):
        return self.cluster.connect("movie")

    @property
    def ticket(self):
        return self.cluster.connect("ticket")
