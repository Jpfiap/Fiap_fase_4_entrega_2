import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import DatabaseManager

class CLI:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()

    def __del__(self):
        if hasattr(self, 'db'):
            self.db.disconnect()

    def menu_principal(self):
        while True:
            print("\n=== Sistema de Monitoramento Agrícola ===")
            print("1. Gerenciar Culturas")
            print("2. Gerenciar Lotes")
            print("3. Gerenciar Sensores")
            print("4. Gerenciar Leituras")
            print("5. Gerenciar Ajustes")
            print("6. Gerenciar Leituras de Solo")
            print("0. Sair")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.menu_cultura()
            elif opcao == "2":
                self.menu_lote()
            elif opcao == "3":
                self.menu_sensor()
            elif opcao == "4":
                self.menu_leitura()
            elif opcao == "5":
                self.menu_ajuste()
            elif opcao == "6":
                self.menu_leitura_solo()
            elif opcao == "0":
                print("\nSaindo do sistema...")
                break
            else:
                print("\nOpção inválida!")

    def menu_cultura(self):
        while True:
            print("\n=== Gerenciamento de Culturas ===")
            print("1. Listar Culturas")
            print("2. Adicionar Cultura")
            print("3. Atualizar Cultura")
            print("4. Remover Cultura")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.listar_culturas()
            elif opcao == "2":
                self.adicionar_cultura()
            elif opcao == "3":
                self.atualizar_cultura()
            elif opcao == "4":
                self.remover_cultura()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")

    def menu_lote(self):
        while True:
            print("\n=== Gerenciamento de Lotes ===")
            print("1. Listar Lotes")
            print("2. Adicionar Lote")
            print("3. Atualizar Lote")
            print("4. Remover Lote")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.listar_lotes()
            elif opcao == "2":
                self.adicionar_lote()
            elif opcao == "3":
                self.atualizar_lote()
            elif opcao == "4":
                self.remover_lote()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")

    def menu_sensor(self):
        while True:
            print("\n=== Gerenciamento de Sensores ===")
            print("1. Listar Sensores")
            print("2. Adicionar Sensor")
            print("3. Atualizar Sensor")
            print("4. Remover Sensor")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.listar_sensores()
            elif opcao == "2":
                self.adicionar_sensor()
            elif opcao == "3":
                self.atualizar_sensor()
            elif opcao == "4":
                self.remover_sensor()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")

    def menu_leitura(self):
        while True:
            print("\n=== Gerenciamento de Leituras ===")
            print("1. Listar Leituras")
            print("2. Adicionar Leitura")
            print("3. Atualizar Leitura")
            print("4. Remover Leitura")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.listar_leituras()
            elif opcao == "2":
                self.adicionar_leitura()
            elif opcao == "3":
                self.atualizar_leitura()
            elif opcao == "4":
                self.remover_leitura()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")

    def menu_ajuste(self):
        while True:
            print("\n=== Gerenciamento de Ajustes ===")
            print("1. Listar Ajustes")
            print("2. Adicionar Ajuste")
            print("3. Atualizar Ajuste")
            print("4. Remover Ajuste")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.listar_ajustes()
            elif opcao == "2":
                self.adicionar_ajuste()
            elif opcao == "3":
                self.atualizar_ajuste()
            elif opcao == "4":
                self.remover_ajuste()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")

    def menu_leitura_solo(self):
        while True:
            print("\n=== Gerenciamento de Leituras de Solo ===")
            print("1. Listar Leituras de Solo")
            print("2. Adicionar Leitura de Solo")
            print("3. Atualizar Leitura de Solo")
            print("4. Remover Leitura de Solo")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.listar_leituras_solo()
            elif opcao == "2":
                self.adicionar_leitura_solo()
            elif opcao == "3":
                self.atualizar_leitura_solo()
            elif opcao == "4":
                self.remover_leitura_solo()
            elif opcao == "0":
                break
            else:
                print("\nOpção inválida!")

    def listar_culturas(self):
        try:
            culturas = self.db.select_all('cultura')
            if not culturas:
                print("\nNenhuma cultura cadastrada.")
                return
            
            print("\nCulturas cadastradas:")
            for cultura in culturas:
                print(f"ID: {cultura[0]}")
                print(f"Nome: {cultura[1]}")
                print(f"Tipo: {cultura[2]}")
                print(f"Data de Plantio: {cultura[3]}")
                print(f"Data de Colheita Prevista: {cultura[4]}")
                print(f"Status: {cultura[5]}")
                print(f"Necessidade de Água (min/max): {cultura[6]}% / {cultura[7]}%")
                print(f"Necessidade de pH (min/max): {cultura[8]} / {cultura[9]}")
                print(f"Necessidade de Fósforo (min/max): {cultura[10]} g/m² / {cultura[11]} g/m²")
                print(f"Necessidade de Potássio (min/max): {cultura[12]} g/m² / {cultura[13]} g/m²")
                print("-" * 30)
        except Exception as e:
            print(f"\nErro ao listar culturas: {e}")

    def adicionar_cultura(self):
        try:
            print("\nAdicionar nova cultura:")
            nome = input("Nome: ")
            tipo = input("Tipo: ")
            data_plantio = input("Data de Plantio (YYYY-MM-DD): ")
            data_colheita = input("Data de Colheita Prevista (YYYY-MM-DD): ")
            status = input("Status: ")
            
            print("\nNecessidades da cultura:")
            necessidade_agua_min = float(input("Necessidade de Água Mínima (%): "))
            necessidade_agua_max = float(input("Necessidade de Água Máxima (%): "))
            necessidade_ph_min = float(input("Necessidade de pH Mínimo: "))
            necessidade_ph_max = float(input("Necessidade de pH Máximo: "))
            necessidade_fosforo_min = float(input("Necessidade de Fósforo Mínimo (g/m²): "))
            necessidade_fosforo_max = float(input("Necessidade de Fósforo Máximo (g/m²): "))
            necessidade_potassio_min = float(input("Necessidade de Potássio Mínimo (g/m²): "))
            necessidade_potassio_max = float(input("Necessidade de Potássio Máximo (g/m²): "))
            
            id_cultura = self.db.insert_cultura(
                nome, tipo, data_plantio, data_colheita, status,
                necessidade_agua_min, necessidade_agua_max,
                necessidade_ph_min, necessidade_ph_max,
                necessidade_fosforo_min, necessidade_fosforo_max,
                necessidade_potassio_min, necessidade_potassio_max
            )
            print(f"\nCultura adicionada com sucesso! ID: {id_cultura}")
        except Exception as e:
            print(f"\nErro ao adicionar cultura: {e}")

    def atualizar_cultura(self):
        try:
            id_cultura = input("\nDigite o ID da cultura a ser atualizada: ")
            cultura = self.db.select_by_id('cultura', 'id_cultura', id_cultura)
            
            if not cultura:
                print("\nCultura não encontrada!")
                return
            
            print("\nAtualizar cultura:")
            nome = input(f"Nome [{cultura[1]}]: ") or cultura[1]
            tipo = input(f"Tipo [{cultura[2]}]: ") or cultura[2]
            data_plantio = input(f"Data de Plantio [{cultura[3]}]: ") or cultura[3]
            data_colheita = input(f"Data de Colheita Prevista [{cultura[4]}]: ") or cultura[4]
            status = input(f"Status [{cultura[5]}]: ") or cultura[5]
            
            print("\nAtualizar necessidades da cultura:")
            necessidade_agua_min = input(f"Necessidade de Água Mínima (%) [{cultura[6]}]: ") or cultura[6]
            necessidade_agua_max = input(f"Necessidade de Água Máxima (%) [{cultura[7]}]: ") or cultura[7]
            necessidade_ph_min = input(f"Necessidade de pH Mínimo [{cultura[8]}]: ") or cultura[8]
            necessidade_ph_max = input(f"Necessidade de pH Máximo [{cultura[9]}]: ") or cultura[9]
            necessidade_fosforo_min = input(f"Necessidade de Fósforo Mínimo (g/m²) [{cultura[10]}]: ") or cultura[10]
            necessidade_fosforo_max = input(f"Necessidade de Fósforo Máximo (g/m²) [{cultura[11]}]: ") or cultura[11]
            necessidade_potassio_min = input(f"Necessidade de Potássio Mínimo (g/m²) [{cultura[12]}]: ") or cultura[12]
            necessidade_potassio_max = input(f"Necessidade de Potássio Máximo (g/m²) [{cultura[13]}]: ") or cultura[13]
            
            self.db.update_cultura(
                id_cultura, nome, tipo, data_plantio, data_colheita, status,
                necessidade_agua_min, necessidade_agua_max,
                necessidade_ph_min, necessidade_ph_max,
                necessidade_fosforo_min, necessidade_fosforo_max,
                necessidade_potassio_min, necessidade_potassio_max
            )
            print("\nCultura atualizada com sucesso!")
        except Exception as e:
            print(f"\nErro ao atualizar cultura: {e}")

    def remover_cultura(self):
        try:
            id_cultura = input("\nDigite o ID da cultura a ser removida: ")
            self.db.delete('cultura', 'id_cultura', id_cultura)
            print("\nCultura removida com sucesso!")
        except Exception as e:
            print(f"\nErro ao remover cultura: {e}")

    def listar_lotes(self):
        try:
            lotes = self.db.select_all('lote')
            if not lotes:
                print("\nNenhum lote cadastrado.")
                return
            
            print("\nLotes cadastrados:")
            for lote in lotes:
                print(f"ID: {lote[0]}")
                print(f"ID Cultura: {lote[1]}")
                print(f"Área: {lote[2]}")
                print(f"Localização: {lote[3]}")
                print(f"Status: {lote[4]}")
                print("-" * 30)
        except Exception as e:
            print(f"\nErro ao listar lotes: {e}")

    def adicionar_lote(self):
        try:
            print("\nAdicionar novo lote:")
            id_cultura = input("ID da Cultura: ")
            area = input("Área: ")
            localizacao = input("Localização: ")
            status = input("Status: ")
            
            id_lote = self.db.insert_lote(id_cultura, area, localizacao, status)
            print(f"\nLote adicionado com sucesso! ID: {id_lote}")
        except Exception as e:
            print(f"\nErro ao adicionar lote: {e}")

    def atualizar_lote(self):
        try:
            id_lote = input("\nDigite o ID do lote a ser atualizado: ")
            lote = self.db.select_by_id('lote', 'id_lote', id_lote)
            
            if not lote:
                print("\nLote não encontrado!")
                return
            
            print("\nAtualizar lote:")
            id_cultura = input(f"ID da Cultura [{lote[1]}]: ") or lote[1]
            area = input(f"Área [{lote[2]}]: ") or lote[2]
            localizacao = input(f"Localização [{lote[3]}]: ") or lote[3]
            status = input(f"Status [{lote[4]}]: ") or lote[4]
            
            self.db.update_lote(id_lote, id_cultura, area, localizacao, status)
            print("\nLote atualizado com sucesso!")
        except Exception as e:
            print(f"\nErro ao atualizar lote: {e}")

    def remover_lote(self):
        try:
            id_lote = input("\nDigite o ID do lote a ser removido: ")
            self.db.delete('lote', 'id_lote', id_lote)
            print("\nLote removido com sucesso!")
        except Exception as e:
            print(f"\nErro ao remover lote: {e}")

    def listar_sensores(self):
        try:
            sensores = self.db.select_all('sensor')
            if not sensores:
                print("\nNenhum sensor cadastrado.")
                return
            
            print("\nSensores cadastrados:")
            for sensor in sensores:
                print(f"ID: {sensor[0]}")
                print(f"ID Lote: {sensor[1]}")
                print(f"Tipo: {sensor[2]}")
                print(f"Modelo: {sensor[3]}")
                print(f"Data de Instalação: {sensor[4]}")
                print(f"Status: {sensor[5]}")
                print("-" * 30)
        except Exception as e:
            print(f"\nErro ao listar sensores: {e}")

    def adicionar_sensor(self):
        try:
            print("\nAdicionar novo sensor:")
            id_lote = input("ID do Lote: ")
            tipo = input("Tipo: ")
            modelo = input("Modelo: ")
            data_instalacao = input("Data de Instalação (YYYY-MM-DD): ")
            status = input("Status: ")
            
            id_sensor = self.db.insert_sensor(id_lote, tipo, modelo, data_instalacao, status)
            print(f"\nSensor adicionado com sucesso! ID: {id_sensor}")
        except Exception as e:
            print(f"\nErro ao adicionar sensor: {e}")

    def atualizar_sensor(self):
        try:
            id_sensor = input("\nDigite o ID do sensor a ser atualizado: ")
            sensor = self.db.select_by_id('sensor', 'id_sensor', id_sensor)
            
            if not sensor:
                print("\nSensor não encontrado!")
                return
            
            print("\nAtualizar sensor:")
            id_lote = input(f"ID do Lote [{sensor[1]}]: ") or sensor[1]
            tipo = input(f"Tipo [{sensor[2]}]: ") or sensor[2]
            modelo = input(f"Modelo [{sensor[3]}]: ") or sensor[3]
            data_instalacao = input(f"Data de Instalação [{sensor[4]}]: ") or sensor[4]
            status = input(f"Status [{sensor[5]}]: ") or sensor[5]
            
            self.db.update_sensor(id_sensor, id_lote, tipo, modelo, data_instalacao, status)
            print("\nSensor atualizado com sucesso!")
        except Exception as e:
            print(f"\nErro ao atualizar sensor: {e}")

    def remover_sensor(self):
        try:
            id_sensor = input("\nDigite o ID do sensor a ser removido: ")
            self.db.delete('sensor', 'id_sensor', id_sensor)
            print("\nSensor removido com sucesso!")
        except Exception as e:
            print(f"\nErro ao remover sensor: {e}")

    def listar_leituras(self):
        try:
            leituras = self.db.select_all('leitura_sensor')
            if not leituras:
                print("\nNenhuma leitura cadastrada.")
                return
            
            print("\nLeituras cadastradas:")
            for leitura in leituras:
                print(f"ID: {leitura[0]}")
                print(f"ID Sensor: {leitura[1]}")
                print(f"Data/Hora: {leitura[2]}")
                print(f"Valor: {leitura[3]}")
                print(f"Unidade: {leitura[4]}")
                print("-" * 30)
        except Exception as e:
            print(f"\nErro ao listar leituras: {e}")

    def adicionar_leitura(self):
        try:
            print("\nAdicionar nova leitura:")
            id_sensor = input("ID do Sensor: ")
            data_hora = input("Data/Hora (YYYY-MM-DD HH:MM:SS): ")
            valor = input("Valor: ")
            unidade = input("Unidade: ")
            
            id_leitura = self.db.insert_leitura(id_sensor, data_hora, valor, unidade)
            print(f"\nLeitura adicionada com sucesso! ID: {id_leitura}")
        except Exception as e:
            print(f"\nErro ao adicionar leitura: {e}")

    def atualizar_leitura(self):
        try:
            id_leitura = input("\nDigite o ID da leitura a ser atualizada: ")
            leitura = self.db.select_by_id('leitura_sensor', 'id_leitura', id_leitura)
            
            if not leitura:
                print("\nLeitura não encontrada!")
                return
            
            print("\nAtualizar leitura:")
            id_sensor = input(f"ID do Sensor [{leitura[1]}]: ") or leitura[1]
            data_hora = input(f"Data/Hora [{leitura[2]}]: ") or leitura[2]
            valor = input(f"Valor [{leitura[3]}]: ") or leitura[3]
            unidade = input(f"Unidade [{leitura[4]}]: ") or leitura[4]
            
            self.db.update_leitura(id_leitura, id_sensor, data_hora, valor, unidade)
            print("\nLeitura atualizada com sucesso!")
        except Exception as e:
            print(f"\nErro ao atualizar leitura: {e}")

    def remover_leitura(self):
        try:
            id_leitura = input("\nDigite o ID da leitura a ser removida: ")
            self.db.delete('leitura_sensor', 'id_leitura', id_leitura)
            print("\nLeitura removida com sucesso!")
        except Exception as e:
            print(f"\nErro ao remover leitura: {e}")

    def listar_ajustes(self):
        try:
            ajustes = self.db.select_all('ajuste')
            if not ajustes:
                print("\nNenhum ajuste cadastrado.")
                return
            
            print("\nAjustes cadastrados:")
            for ajuste in ajustes:
                print(f"ID: {ajuste[0]}")
                print(f"ID Lote: {ajuste[1]}")
                print(f"Tipo: {ajuste[2]}")
                print(f"Data/Hora: {ajuste[3]}")
                print(f"Descrição: {ajuste[4]}")
                print(f"Status: {ajuste[5]}")
                print("-" * 30)
        except Exception as e:
            print(f"\nErro ao listar ajustes: {e}")

    def adicionar_ajuste(self):
        try:
            print("\nAdicionar novo ajuste:")
            id_lote = input("ID do Lote: ")
            tipo = input("Tipo: ")
            data_hora = input("Data/Hora (YYYY-MM-DD HH:MM:SS): ")
            descricao = input("Descrição: ")
            status = input("Status: ")
            
            id_ajuste = self.db.insert_ajuste(id_lote, tipo, data_hora, descricao, status)
            print(f"\nAjuste adicionado com sucesso! ID: {id_ajuste}")
        except Exception as e:
            print(f"\nErro ao adicionar ajuste: {e}")

    def atualizar_ajuste(self):
        try:
            id_ajuste = input("\nDigite o ID do ajuste a ser atualizado: ")
            ajuste = self.db.select_by_id('ajuste', 'id_ajuste', id_ajuste)
            
            if not ajuste:
                print("\nAjuste não encontrado!")
                return
            
            print("\nAtualizar ajuste:")
            id_lote = input(f"ID do Lote [{ajuste[1]}]: ") or ajuste[1]
            tipo = input(f"Tipo [{ajuste[2]}]: ") or ajuste[2]
            data_hora = input(f"Data/Hora [{ajuste[3]}]: ") or ajuste[3]
            descricao = input(f"Descrição [{ajuste[4]}]: ") or ajuste[4]
            status = input(f"Status [{ajuste[5]}]: ") or ajuste[5]
            
            self.db.update_ajuste(id_ajuste, id_lote, tipo, data_hora, descricao, status)
            print("\nAjuste atualizado com sucesso!")
        except Exception as e:
            print(f"\nErro ao atualizar ajuste: {e}")

    def remover_ajuste(self):
        try:
            id_ajuste = input("\nDigite o ID do ajuste a ser removido: ")
            self.db.delete('ajuste', 'id_ajuste', id_ajuste)
            print("\nAjuste removido com sucesso!")
        except Exception as e:
            print(f"\nErro ao remover ajuste: {e}")

    def listar_leituras_solo(self):
        try:
            leituras = self.db.select_all('leitura_solo')
            if not leituras:
                print("\nNenhuma leitura de solo cadastrada.")
                return
            
            print("\nLeituras de solo cadastradas:")
            for leitura in leituras:
                print(f"ID: {leitura[0]}")
                print(f"ID Sensor: {leitura[1]}")
                print(f"Data/Hora: {leitura[2]}")
                print(f"Fósforo OK: {'Sim' if leitura[3] else 'Não'}")
                print(f"Potássio OK: {'Sim' if leitura[4] else 'Não'}")
                print(f"pH: {leitura[5]}")
                print(f"Status pH: {leitura[6]}")
                print(f"Umidade: {leitura[7]}")
                print(f"Status Umidade: {leitura[8]}")
                print(f"Irrigação: {leitura[9]}")
                print("-" * 30)
        except Exception as e:
            print(f"\nErro ao listar leituras de solo: {e}")

    def adicionar_leitura_solo(self):
        try:
            print("\nAdicionar nova leitura de solo:")
            id_sensor = input("ID do Sensor: ")
            fosforo_ok = input("Fósforo OK (S/N): ").upper() == 'S'
            potassio_ok = input("Potássio OK (S/N): ").upper() == 'S'
            ph = float(input("pH: "))
            ph_status = input("Status do pH: ")
            umidade = float(input("Umidade: "))
            umidade_status = input("Status da Umidade: ")
            irrigacao = input("Irrigação: ")
            
            id_leitura = self.db.insert_leitura_solo(
                id_sensor, fosforo_ok, potassio_ok,
                ph, ph_status, umidade, umidade_status, irrigacao
            )
            print(f"\nLeitura de solo adicionada com sucesso! ID: {id_leitura}")
        except Exception as e:
            print(f"\nErro ao adicionar leitura de solo: {e}")

    def atualizar_leitura_solo(self):
        try:
            id_leitura = input("\nDigite o ID da leitura a ser atualizada: ")
            leitura = self.db.select_by_id('leitura_solo', 'id_leitura_solo', id_leitura)
            
            if not leitura:
                print("\nLeitura não encontrada!")
                return
            
            print("\nAtualizar leitura de solo:")
            id_sensor = input(f"ID do Sensor [{leitura[1]}]: ") or leitura[1]
            fosforo_ok = input(f"Fósforo OK (S/N) [{'S' if leitura[3] else 'N'}]: ").upper() == 'S'
            potassio_ok = input(f"Potássio OK (S/N) [{'S' if leitura[4] else 'N'}]: ").upper() == 'S'
            ph = input(f"pH [{leitura[5]}]: ") or leitura[5]
            ph_status = input(f"Status do pH [{leitura[6]}]: ") or leitura[6]
            umidade = input(f"Umidade [{leitura[7]}]: ") or leitura[7]
            umidade_status = input(f"Status da Umidade [{leitura[8]}]: ") or leitura[8]
            irrigacao = input(f"Irrigação [{leitura[9]}]: ") or leitura[9]
            
            self.db.update_leitura_solo(
                id_leitura, id_sensor, fosforo_ok, potassio_ok,
                ph, ph_status, umidade, umidade_status, irrigacao
            )
            print("\nLeitura de solo atualizada com sucesso!")
        except Exception as e:
            print(f"\nErro ao atualizar leitura de solo: {e}")

    def remover_leitura_solo(self):
        try:
            id_leitura = input("\nDigite o ID da leitura a ser removida: ")
            self.db.delete('leitura_solo', 'id_leitura_solo', id_leitura)
            print("\nLeitura de solo removida com sucesso!")
        except Exception as e:
            print(f"\nErro ao remover leitura de solo: {e}")

if __name__ == "__main__":
    cli = CLI()
    cli.menu_principal() 