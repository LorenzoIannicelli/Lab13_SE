from database.DB_connect import DBConnect
from model.correlazione import Correlazione

class DAO:

    @staticmethod
    def read_cromosomi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM gene WHERE cromosoma > 0 """

        cursor.execute(query)

        for row in cursor:
            result.append(row['cromosoma'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_edges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select Cromosoma1, Cromosoma2, sum(Correlazione) as Correlazione
                from (select  g1.cromosoma as Cromosoma1, g2.cromosoma as Cromosoma2, i.id_gene1 as Gene1, i.id_gene2 as Gene2, i.correlazione as Correlazione
                from gene g1, gene g2, interazione i
                where g1.cromosoma > 0 and g2.cromosoma > 0
                and g1.id = i.id_gene1 and g2.id = i.id_gene2
                and g1.cromosoma <> g2.cromosoma
                group by Cromosoma1, Cromosoma2, Gene1, Gene2, Correlazione) as temp
                group by Cromosoma1, Cromosoma2
                """

        cursor.execute(query)

        for row in cursor:
            correlazione = Correlazione(int(row['Cromosoma1']),
                                        int(row['Cromosoma2']),
                                        float(row['Correlazione']))
            result.append(correlazione)

        cursor.close()
        conn.close()
        return result