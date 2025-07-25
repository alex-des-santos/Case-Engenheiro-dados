# -*- coding: utf-8 -*-
"""
Script principal para execu��o em MongoDB local
"""

import sys
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import json

# Adicionar diret�rio raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.local_config import get_connection_string, get_connection_params, COLLECTIONS
from scripts.data_processing import (
    create_carros_dataframe, 
    create_montadoras_dataframe, 
    dataframe_to_dict,
    print_success, 
    print_error, 
    print_info, 
    print_header
)

class MongoDBLocalManager:
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self):
        """Estabelece conex�o com MongoDB local"""
        try:
            print_info("Conectando ao MongoDB local...")
            
            connection_string = get_connection_string()
            connection_params = get_connection_params()
            
            self.client = MongoClient(connection_string, **connection_params)
            
            # Testar conex�o
            self.client.admin.command('ping')
            
            # Selecionar database
            self.db = self.client.dataops_challenge
            
            print_success("Conex�o estabelecida com sucesso!")
            return True
            
        except ConnectionFailure as e:
            print_error(f"Falha na conex�o: {e}")
            return False
        except ServerSelectionTimeoutError as e:
            print_error(f"Timeout na conex�o. Verifique se o MongoDB est� rodando: {e}")
            return False
        except Exception as e:
            print_error(f"Erro inesperado: {e}")
            return False
    
    def create_collections(self):
        """Cria as collections no MongoDB (se n�o existirem)"""
        try:
            collections = self.db.list_collection_names()
            
            for collection_name in COLLECTIONS.values():
                if collection_name not in collections:
                    self.db.create_collection(collection_name)
                    print_success(f"Collection '{collection_name}' criada!")
                else:
                    print_info(f"Collection '{collection_name}' j� existe")
            
            return True
        except Exception as e:
            print_error(f"Erro ao criar collections: {e}")
            return False
    
    def insert_dataframes(self, carros_df, montadoras_df):
        """Insere os dataframes nas collections"""
        try:
            # Limpar collections existentes
            self.db[COLLECTIONS['carros']].delete_many({})
            self.db[COLLECTIONS['montadoras']].delete_many({})
            print_info("Collections limpas")
            
            # Inserir carros
            carros_data = dataframe_to_dict(carros_df)
            result_carros = self.db[COLLECTIONS['carros']].insert_many(carros_data)
            print_success(f"Inseridos {len(result_carros.inserted_ids)} carros")
            
            # Inserir montadoras
            montadoras_data = dataframe_to_dict(montadoras_df)
            result_montadoras = self.db[COLLECTIONS['montadoras']].insert_many(montadoras_data)
            print_success(f"Inseridas {len(result_montadoras.inserted_ids)} montadoras")
            
            return True
        except Exception as e:
            print_error(f"Erro ao inserir dados: {e}")
            return False
    
    def create_aggregation(self):
        """Executa a agrega��o conforme especificado no desafio"""
        try:
            print_info("Executando agrega��o...")
            
            pipeline = [
                {
                    "$lookup": {
                        "from": "montadoras",
                        "localField": "montadora",
                        "foreignField": "montadora",
                        "as": "montadora_info"
                    }
                },
                {
                    "$unwind": "$montadora_info"
                },
                {
                    "$group": {
                        "_id": "$montadora_info.pais",
                        "carros": {
                            "$push": {
                                "carro": "$carro",
                                "cor": "$cor",
                                "montadora": "$montadora"
                            }
                        }
                    }
                },
                {
                    "$sort": {"_id": 1}
                }
            ]
            
            result = list(self.db[COLLECTIONS['carros']].aggregate(pipeline))
            
            print_success("Agrega��o executada com sucesso!")
            print_info("Resultado da agrega��o:")
            
            for doc in result:
                print(f"\n?? Pa�s: {doc['_id']}")
                for carro in doc['carros']:
                    print(f"  ?? {carro['carro']} ({carro['cor']}) - {carro['montadora']}")
            
            # Salvar resultado em arquivo
            self.save_aggregation_result(result)
            
            return result
            
        except Exception as e:
            print_error(f"Erro na agrega��o: {e}")
            return None
    
    def save_aggregation_result(self, result):
        """Salva o resultado da agrega��o em arquivo JSON"""
        try:
            os.makedirs('mongodb/exports', exist_ok=True)
            
            with open('mongodb/exports/aggregation_result.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
            
            print_success("Resultado da agrega��o salvo em 'mongodb/exports/aggregation_result.json'")
            
        except Exception as e:
            print_error(f"Erro ao salvar resultado: {e}")
    
    def export_collections(self):
        """Exporta as collections para arquivos JSON"""
        try:
            os.makedirs('mongodb/exports', exist_ok=True)
            
            # Exportar carros
            carros = list(self.db[COLLECTIONS['carros']].find({}))
            with open('mongodb/exports/carros.json', 'w', encoding='utf-8') as f:
                json.dump(carros, f, indent=2, ensure_ascii=False, default=str)
            print_success("Collection 'carros' exportada")
            
            # Exportar montadoras
            montadoras = list(self.db[COLLECTIONS['montadoras']].find({}))
            with open('mongodb/exports/montadoras.json', 'w', encoding='utf-8') as f:
                json.dump(montadoras, f, indent=2, ensure_ascii=False, default=str)
            print_success("Collection 'montadoras' exportada")
            
            return True
        except Exception as e:
            print_error(f"Erro ao exportar collections: {e}")
            return False
    
    def close_connection(self):
        """Fecha a conex�o com o MongoDB"""
        if self.client:
            self.client.close()
            print_info("Conex�o fechada")

def main():
    """Fun��o principal"""
    print_header("DESAFIO DATAOPS - EXECU��O LOCAL")
    
    # Criar inst�ncia do gerenciador
    mongo_manager = MongoDBLocalManager()
    
    try:
        # 1. Conectar ao MongoDB
        if not mongo_manager.connect():
            print_error("N�o foi poss�vel conectar ao MongoDB. Verifique se est� rodando.")
            return
        
        # 2. Criar collections
        if not mongo_manager.create_collections():
            return
        
        # 3. Criar dataframes
        print_header("CRIANDO DATAFRAMES")
        carros_df = create_carros_dataframe()
        montadoras_df = create_montadoras_dataframe()
        
        # 4. Inserir dados no MongoDB
        print_header("INSERINDO DADOS NO MONGODB")
        if not mongo_manager.insert_dataframes(carros_df, montadoras_df):
            return
        
        # 5. Executar agrega��o
        print_header("EXECUTANDO AGREGA��O")
        aggregation_result = mongo_manager.create_aggregation()
        
        if aggregation_result is None:
            return
        
        # 6. Exportar collections
        print_header("EXPORTANDO COLLECTIONS")
        if not mongo_manager.export_collections():
            return
        
        print_header("EXECU��O CONCLU�DA COM SUCESSO!")
        print_success("Todos os passos foram executados com sucesso!")
        print_info("Arquivos gerados:")
        print_info("  ?? mongodb/exports/carros.json")
        print_info("  ?? mongodb/exports/montadoras.json")
        print_info("  ?? mongodb/exports/aggregation_result.json")
        
    except KeyboardInterrupt:
        print_error("Execu��o interrompida pelo usu�rio")
    except Exception as e:
        print_error(f"Erro durante execu��o: {e}")
    finally:
        mongo_manager.close_connection()

if __name__ == "__main__":
    main()
