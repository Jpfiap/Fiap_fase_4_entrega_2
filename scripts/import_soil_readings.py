import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import DatabaseManager

def import_soil_readings(file_path, sensor_id):
    db = DatabaseManager()
    db.connect()
    
    try:
        with open(file_path, 'r') as file:
            # Pula o cabeçalho
            next(file)
            
            for line in file:
                # Remove espaços em branco e quebras de linha
                line = line.strip()
                if not line:
                    continue
                
                # Divide a linha em campos
                fields = line.split(',')
                if len(fields) != 7:
                    print(f"Linha inválida: {line}")
                    continue
                
                # Converte os campos
                fosforo_ok = fields[0].strip() == 'Sim'
                potassio_ok = fields[1].strip() == 'Sim'
                ph = float(fields[2].strip())
                ph_status = fields[3].strip()
                umidade = float(fields[4].strip())
                umidade_status = fields[5].strip()
                irrigacao = fields[6].strip()
                
                # Insere no banco de dados
                db.insert_leitura_solo(
                    id_sensor=sensor_id,
                    data_hora=datetime.now(),  # Você pode ajustar isso conforme necessário
                    fosforo_ok=fosforo_ok,
                    potassio_ok=potassio_ok,
                    ph=ph,
                    ph_status=ph_status,
                    umidade=umidade,
                    umidade_status=umidade_status,
                    irrigacao=irrigacao
                )
                
        print("Importação concluída com sucesso!")
        
    except Exception as e:
        print(f"Erro durante a importação: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python import_soil_readings.py <caminho_do_arquivo> <id_do_sensor>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    sensor_id = int(sys.argv[2])
    
    import_soil_readings(file_path, sensor_id) 