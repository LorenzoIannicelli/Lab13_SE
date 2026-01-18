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
            self._ricorsione([n], [], threshold)

        return self._percorso, self._max_costo

    def _ricorsione(self, parziale, parziale_archi, threshold):
        disponibili = self.get_disponibili(parziale[-1], parziale_archi, threshold)

        if len(disponibili) == 0:
            costo = self._calcola_peso(parziale_archi)
            if costo > self._max_costo:
                self._percorso = parziale_archi.copy()
                self._max_costo = costo
            return

        for n1 in disponibili:
            parziale.append(n1)
            parziale_archi.append((parziale[-1], n1, self._G.get_edge_data(parziale[-1], n1)))
            self._ricorsione(parziale, parziale_archi, threshold)
            parziale.pop()
            parziale_archi.pop()

    def get_disponibili(self, n, archi, threshold):
        disponibili = []
        for u, v, data in self._G.out_edges(n, data=True):
            if data['weight'] > threshold:
                if (u, v) not in [(x[0], x[1]) for x in archi]:
                    disponibili.append(v)

        return disponibili

    def _calcola_peso(self, sequenza):
        costo = 0
        for e in sequenza :
            costo += e[2]['weight']

        return costo