import copy

import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._lista_nodi = []
        self._lista_correlazioni = []
        self._min_weight = float('inf')
        self._max_weight = float('-inf')
        self._G = nx.DiGraph()

        self._percorso = []
        self._max_costo = 0

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

    def get_percorso(self, threshold):

        for n in self._G.nodes():
            self._ricorsione([n], [n], threshold)

        return self._percorso, self._max_costo

    def _ricorsione(self, parziale, visited, threshold):
        peso = self._calcola_peso(parziale)
        if peso > self._max_weight:
            self._max_weight = peso
            self._percorso = copy.deepcopy(parziale)
            return

        v = parziale[-1]

        for u in self._G.neighbors(v):
            if u not in visited and self._G[v][u]['weight'] > threshold:
                parziale.append(u)
                visited.append(u)
                self._ricorsione(parziale, visited, threshold)

                visited.pop()
                parziale.pop()

    def _calcola_peso(self, parziale):
        costo = 0
        if len(parziale) < 2:
            return 0

        for i in range(len(parziale)-1):
            v = parziale[i]
            u = parziale[i+1]
            costo += self._G[v][u]['weight']

        return costo