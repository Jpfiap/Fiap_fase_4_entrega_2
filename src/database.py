import psycopg2
from psycopg2 import Error
from config.database_config import DB_CONFIG, TABLES

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.tables = TABLES

    def connect(self):
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            print("Conexão com o PostgreSQL estabelecida com sucesso!")
        except Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            raise

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Conexão com o PostgreSQL fechada.")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor
        except Error as e:
            self.connection.rollback()
            print(f"Erro ao executar query: {e}")
            raise

    def select_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        return self.execute_query(query).fetchall()

    def select_by_id(self, table_name, id_column, id_value):
        query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"
        return self.execute_query(query, (id_value,)).fetchone()

    def insert_cultura(self, nome, tipo, data_plantio, data_colheita_prevista, status,
                      necessidade_agua_min, necessidade_agua_max,
                      necessidade_ph_min, necessidade_ph_max,
                      necessidade_fosforo_min, necessidade_fosforo_max,
                      necessidade_potassio_min, necessidade_potassio_max):
        query = """
            INSERT INTO cultura (
                nome, tipo, data_plantio, data_colheita_prevista, status,
                necessidade_agua_min, necessidade_agua_max,
                necessidade_ph_min, necessidade_ph_max,
                necessidade_fosforo_min, necessidade_fosforo_max,
                necessidade_potassio_min, necessidade_potassio_max
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_cultura
        """
        return self.execute_query(query, (
            nome, tipo, data_plantio, data_colheita_prevista, status,
            necessidade_agua_min, necessidade_agua_max,
            necessidade_ph_min, necessidade_ph_max,
            necessidade_fosforo_min, necessidade_fosforo_max,
            necessidade_potassio_min, necessidade_potassio_max
        )).fetchone()[0]

    def insert_lote(self, id_cultura, area, localizacao, status):
        query = """
            INSERT INTO lote (id_cultura, area, localizacao, status)
            VALUES (%s, %s, %s, %s)
            RETURNING id_lote
        """
        return self.execute_query(query, (id_cultura, area, localizacao, status)).fetchone()[0]

    def insert_sensor(self, id_lote, tipo, modelo, data_instalacao, status):
        query = """
            INSERT INTO sensor (id_lote, tipo, modelo, data_instalacao, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_sensor
        """
        return self.execute_query(query, (id_lote, tipo, modelo, data_instalacao, status)).fetchone()[0]

    def insert_leitura(self, id_sensor, data_hora, valor, unidade):
        query = """
            INSERT INTO leitura_sensor (id_sensor, data_hora, valor, unidade)
            VALUES (%s, %s, %s, %s)
            RETURNING id_leitura
        """
        return self.execute_query(query, (id_sensor, data_hora, valor, unidade)).fetchone()[0]

    def insert_leitura_solo(self, id_sensor, fosforo_ok, potassio_ok, ph, ph_status, umidade, umidade_status, irrigacao):
        query = """
            INSERT INTO leitura_solo (
                id_sensor, data_hora, fosforo_ok, potassio_ok,
                ph, ph_status, umidade, umidade_status, irrigacao
            )
            VALUES (%s, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_leitura_solo
        """
        return self.execute_query(query, (
            id_sensor, fosforo_ok, potassio_ok,
            ph, ph_status, umidade, umidade_status, irrigacao
        )).fetchone()[0]

    def insert_ajuste(self, id_lote, tipo, data_hora, descricao, status):
        query = """
            INSERT INTO ajuste (id_lote, tipo, data_hora, descricao, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_ajuste
        """
        return self.execute_query(query, (id_lote, tipo, data_hora, descricao, status)).fetchone()[0]

    def update_cultura(self, id_cultura, nome, tipo, data_plantio, data_colheita_prevista, status,
                      necessidade_agua_min, necessidade_agua_max,
                      necessidade_ph_min, necessidade_ph_max,
                      necessidade_fosforo_min, necessidade_fosforo_max,
                      necessidade_potassio_min, necessidade_potassio_max):
        query = """
            UPDATE cultura 
            SET nome = %s, tipo = %s, data_plantio = %s, data_colheita_prevista = %s, status = %s,
                necessidade_agua_min = %s, necessidade_agua_max = %s,
                necessidade_ph_min = %s, necessidade_ph_max = %s,
                necessidade_fosforo_min = %s, necessidade_fosforo_max = %s,
                necessidade_potassio_min = %s, necessidade_potassio_max = %s
            WHERE id_cultura = %s
        """
        self.execute_query(query, (
            nome, tipo, data_plantio, data_colheita_prevista, status,
            necessidade_agua_min, necessidade_agua_max,
            necessidade_ph_min, necessidade_ph_max,
            necessidade_fosforo_min, necessidade_fosforo_max,
            necessidade_potassio_min, necessidade_potassio_max,
            id_cultura
        ))

    def update_lote(self, id_lote, id_cultura, area, localizacao, status):
        query = """
            UPDATE lote 
            SET id_cultura = %s, area = %s, localizacao = %s, status = %s
            WHERE id_lote = %s
        """
        self.execute_query(query, (id_cultura, area, localizacao, status, id_lote))

    def update_sensor(self, id_sensor, id_lote, tipo, modelo, data_instalacao, status):
        query = """
            UPDATE sensor 
            SET id_lote = %s, tipo = %s, modelo = %s, data_instalacao = %s, status = %s
            WHERE id_sensor = %s
        """
        self.execute_query(query, (id_lote, tipo, modelo, data_instalacao, status, id_sensor))

    def update_leitura(self, id_leitura, id_sensor, data_hora, valor, unidade):
        query = """
            UPDATE leitura_sensor 
            SET id_sensor = %s, data_hora = %s, valor = %s, unidade = %s
            WHERE id_leitura = %s
        """
        self.execute_query(query, (id_sensor, data_hora, valor, unidade, id_leitura))

    def update_leitura_solo(self, id_leitura_solo, id_sensor, fosforo_ok, potassio_ok,
                           ph, ph_status, umidade, umidade_status, irrigacao):
        query = """
            UPDATE leitura_solo 
            SET id_sensor = %s, fosforo_ok = %s, potassio_ok = %s,
                ph = %s, ph_status = %s, umidade = %s, umidade_status = %s, irrigacao = %s
            WHERE id_leitura_solo = %s
        """
        self.execute_query(query, (
            id_sensor, fosforo_ok, potassio_ok,
            ph, ph_status, umidade, umidade_status, irrigacao,
            id_leitura_solo
        ))

    def update_ajuste(self, id_ajuste, id_lote, tipo, data_hora, descricao, status):
        query = """
            UPDATE ajuste 
            SET id_lote = %s, tipo = %s, data_hora = %s, descricao = %s, status = %s
            WHERE id_ajuste = %s
        """
        self.execute_query(query, (id_lote, tipo, data_hora, descricao, status, id_ajuste))

    def delete(self, table_name, id_column, id_value):
        query = f"DELETE FROM {table_name} WHERE {id_column} = %s"
        self.execute_query(query, (id_value,))

# Exemplo de uso
if __name__ == "__main__":
    db = DatabaseManager()
    db.connect()
    
    # Exemplo de inserção de dados do ESP32
    dados_esp32 = [
        (1, 86.50, 3.40, "Fora da faixa", "Fora da faixa", "Inativa"),
        (1, 73.00, 3.40, "Fora da faixa", "Fora da faixa", "Inativa"),
        (1, 66.50, 3.40, "OK", "Fora da faixa", "Ativa"),
        (1, 53.00, 3.40, "OK", "Fora da faixa", "Ativa"),
        (1, 44.50, 6.20, "OK", "OK", "Ativa")
    ]
    
    for dado in dados_esp32:
        db.insert_leitura(*dado)
    
    # Exemplo de consulta
    readings = db.select_all('leitura_sensor')
    print("\nLeituras do sensor 1:")
    for reading in readings:
        print(reading)
    
    db.disconnect() 