import pandas as pd
import psycopg2
from datetime import datetime
import sys
import os

# Adiciona o diretório pai ao path para importar o módulo de configuração
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database_config import DB_CONFIG

def conectar_banco():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        sys.exit(1)

def inserir_cultura_milho(conn):
    try:
        cursor = conn.cursor()
        
        # Inserir cultura do milho
        cursor.execute("""
            INSERT INTO cultura (
                nome, tipo, data_plantio, data_colheita_prevista, status,
                necessidade_agua_min, necessidade_agua_max,
                necessidade_ph_min, necessidade_ph_max,
                necessidade_fosforo_min, necessidade_fosforo_max,
                necessidade_potassio_min, necessidade_potassio_max
            ) VALUES (
                'Milho', 'Grão', CURRENT_DATE, CURRENT_DATE + INTERVAL '120 days', 'Ativo',
                40.0, 70.0,
                5.5, 7.0,
                2.0, 4.0,
                6.0, 10.0
            ) RETURNING id_cultura
        """)
        
        id_cultura = cursor.fetchone()[0]
        conn.commit()
        print(f"Cultura do milho inserida com sucesso! ID: {id_cultura}")
        return id_cultura
        
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir cultura do milho: {e}")
        return None

def importar_leituras(conn, id_cultura):
    try:
        # Verificar se o arquivo existe
        arquivo_csv = os.path.join(os.path.dirname(__file__), 'dados_leituras.csv')
        if not os.path.exists(arquivo_csv):
            print(f"Erro: Arquivo não encontrado em: {arquivo_csv}")
            return

        print(f"Tentando ler o arquivo: {arquivo_csv}")
        
        # Tentar diferentes encodings
        encodings = ['latin1', 'utf-8', 'utf-8-sig', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                print(f"Tentando encoding: {encoding}")
                df = pd.read_csv(arquivo_csv, sep=';', encoding=encoding)
                print("Arquivo lido com sucesso!")
                break
            except Exception as e:
                print(f"Falha ao ler com encoding {encoding}: {e}")
                continue
        
        if df is None:
            print("Não foi possível ler o arquivo com nenhum encoding")
            return

        print(f"Colunas encontradas: {df.columns.tolist()}")
        print(f"Número de linhas: {len(df)}")
        
        cursor = conn.cursor()
        
        # Primeiro, criar um lote para a cultura
        cursor.execute("""
            INSERT INTO lote (id_cultura, area, localizacao, status)
            VALUES (%s, 100.0, 'Lote Principal', 'Ativo')
            RETURNING id_lote
        """, (id_cultura,))
        
        id_lote = cursor.fetchone()[0]
        print(f"Lote criado com ID: {id_lote}")
        
        # Criar um sensor para o lote
        cursor.execute("""
            INSERT INTO sensor (id_lote, tipo, modelo, data_instalacao, status)
            VALUES (%s, 'Solo', 'Sensor XYZ-123', CURRENT_DATE, 'Ativo')
            RETURNING id_sensor
        """, (id_lote,))
        
        id_sensor = cursor.fetchone()[0]
        print(f"Sensor criado com ID: {id_sensor}")
        
        # Inserir as leituras
        contador = 0
        for _, row in df.iterrows():
            try:
                # Converter valores booleanos
                fosforo_ok = str(row['Fósforo_OK']).strip().lower() == 'sim'
                potassio_ok = str(row['Potássio_OK']).strip().lower() == 'sim'
                
                # Converter valores numéricos
                ph = float(str(row['pH']).replace(',', '.'))
                umidade = float(str(row['Umidade']).replace(',', '.'))
                
                cursor.execute("""
                    INSERT INTO leitura_solo (
                        id_sensor, data_hora, fosforo_ok, potassio_ok,
                        ph, ph_status, umidade, umidade_status, irrigacao
                    ) VALUES (
                        %s, CURRENT_TIMESTAMP, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                """, (
                    id_sensor,
                    fosforo_ok,
                    potassio_ok,
                    ph,
                    str(row['pH_Status']),
                    umidade,
                    str(row['Umidade_Status']),
                    str(row['Irrigação'])
                ))
                contador += 1
                
            except Exception as e:
                print(f"Erro ao processar linha {contador + 1}: {e}")
                print(f"Dados da linha: {row.to_dict()}")
                continue
        
        conn.commit()
        print(f"Leituras importadas com sucesso! Total de registros: {contador}")
        
    except Exception as e:
        conn.rollback()
        print(f"Erro ao importar leituras: {e}")
        import traceback
        print(traceback.format_exc())

def main():
    conn = conectar_banco()
    try:
        # Inserir cultura do milho
        id_cultura = inserir_cultura_milho(conn)
        if id_cultura:
            # Importar leituras
            importar_leituras(conn, id_cultura)
    finally:
        conn.close()

if __name__ == "__main__":
    main() 