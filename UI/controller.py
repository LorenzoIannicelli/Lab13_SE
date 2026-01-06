import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """""
        nodes, edges, min, max = self._model.build_graph()
        txt1 = f'Numero di vertici: {nodes} Numero di archi: {edges}'
        txt2 = f'Informazioni sui pesi degli archi - valore minimo: {min} e valore massimo: {max}'

        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(txt1))
        self._view.lista_visualizzazione_1.controls.append(ft.Text(txt2))
        self._view.update()


    def handle_conta_edges(self, e):
        """ Handler per gestire il conteggio degli archi """""
        try :
            cnt_greater = 0
            cnt_less = 0
            threshold = float(self._view.txt_name.value)
            if threshold < 3 or threshold > 7:
                self._view.show_alert("Inserire un valore compreso nell'intervallo [3,7].")
                return

            edges = self._model.correlazioni()
            for edge in edges:
                if edge.correlazione > threshold:
                    cnt_greater += 1
                elif edge.correlazione < threshold:
                    cnt_less += 1


            txt1 = f'Numero archi con peso maggiore della soglia: {cnt_greater}'
            txt2 = f'Numero archi con peso maggiore della soglia: {cnt_less}'
            self._view.lista_visualizzazione_2.controls.clear()
            self._view.lista_visualizzazione_2.controls.append(ft.Text(txt1))
            self._view.lista_visualizzazione_2.controls.append(ft.Text(txt2))
            self._view.update()

        except ValueError:
            self._view.show_alert('Inserire un valore valido (float).')

    def handle_ricerca(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """""
        # TODO