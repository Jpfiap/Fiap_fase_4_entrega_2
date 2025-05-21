import psycopg2
from psycopg2 import Error
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database_config import DB_CONFIG, TABLES

def create_database():
    try:
        # Conecta ao PostgreSQL sem especificar um banco de dados
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Verifica se o banco de dados já existe
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_CONFIG['database'],))
        exists = cursor.fetchone()
        
        if not exists:
            # Cria o banco de dados
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
            print(f"Banco de dados {DB_CONFIG['database']} criado com sucesso!")
        else:
            print(f"Banco de dados {DB_CONFIG['database']} já existe.")

        cursor.close()
        conn.close()

    except Error as e:
        print(f"Erro ao criar banco de dados: {e}")
        raise

def create_tables():
    try:
        # Conecta ao banco de dados criado
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Cria as tabelas
        for table_name, table_config in TABLES.items():
            columns = ', '.join(table_config['columns'])
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_config['name']} ({columns})"
            
            try:
                cursor.execute(create_table_query)
                print(f"Tabela {table_config['name']} criada com sucesso!")
            except Error as e:
                print(f"Erro ao criar tabela {table_config['name']}: {e}")
                raise

        conn.commit()
        cursor.close()
        conn.close()
        print("Todas as tabelas foram criadas com sucesso!")

    except Error as e:
        print(f"Erro ao criar tabelas: {e}")
        raise

if __name__ == "__main__":
    try:
        create_database()
        create_tables()
    except Error as e:
        print(f"Erro durante a migração: {e}")
        sys.exit(1) 