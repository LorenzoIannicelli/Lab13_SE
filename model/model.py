import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._lista_nodi = []
        self._lista_correlazioni = []
        self._min_weight = float('inf')
        self._max_weight = float('-inf')
        self._G = nx.DiGraph()

    def correlazioni(self):
        return self._lista_correlazioni

    def build_graph(self):
        self._lista_nodi = DAO.read_cromosomi()
        self._G.add_nodes_from(self._lista_nodi)
        self._lista_correlazioni = DAO.read_edges()
        for c in self._lista_correlazioni:
            self._G.add_edge(c.crom1, c.crom2, weight=c.correlazione)
            if c.correlazione < self._min_weight:
                self._min_weight = c.correlazione
            elif c.correlazione > self._max_weight:
                self._max_weight = c.correlazione

        return self._G.number_of_nodes(), self._G.number_of_edges(), self._min_weight, self._max_weight