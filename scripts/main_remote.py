# -*- coding: utf-8 -*-
"""
Script principal para execução em MongoDB remoto
Exemplo: conexão para servidor 192.168.22.111
"""

import sys
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, AuthenticationFailed
import json

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.remote_config import (
    get_connection_string, 
    get_connection_params, 
    COLLECTIONS, 
    validate_remote_config,
    MONGODB_CONFIG
)
from scripts.data_processing import (
    create_carros_dataframe, 
    create_montadoras_dataframe, 
    dataframe_to_dict,
    print_success, 
    print_error, 
    print_info, 
    print_header,
    print_warning
)

class MongoDBRemoteManager:
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self):
        """Estabelece conexão com MongoDB remoto"""
        try:
            print_info("Validando configurações...")
            validate_remote_config()
            
            print_info(f"Conectando ao MongoDB remoto em {MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}...")
            
            connection_string = get_connection_string()
            connection_params = get_connection_params()
            
            # Mascarar senha na exibição
            safe_connection_string = connection_string
            if MONGODB_CONFIG['password']:
                safe_connection_string = safe_connection_string.replace(
                    MONGODB_CONFIG['password'], 
                    '*' * len(MONGODB_CONFIG['password'])
                )
            
            print_info(f"String de conexão: {safe_connection_string}")
            
            self.client = MongoClient(connection_string, **connection_params)
            
            # Testar conexão
            self.client.admin.command('ping')
            
            # Selecionar database
            self.db = self.client[MONGODB_CONFIG['database']]
            
            print_success("Conexão estabelecida com sucesso!")
            
            # Exibir informações do servidor
            server_info = self.client.server_info()
            print_info(f"Versão do MongoDB: {server_info.get('version', 'Desconhecida')}")
            
            return True
            
        except AuthenticationFailed as e:
            print_error(f"Falha na autenticação: {e}")
            print_warning("Verifique as credenciais em configs/remote_config.py ou variáveis de ambiente")
            return False
        except ConnectionFailure as e:
            print_error(f"Falha na conexão: {e}")
            print_warning("Verifique se o servidor MongoDB está acessível e rodando")
            return False
        except ServerSelectionTimeoutError as e:
            print_error(f"Timeout na conexão: {e}")
            print_warning("Verifique a conectividade de rede e se o endereço está correto")
            return False
        except Exception as e:
            print_error(f"Erro inesperado: {e}")
            return False
    
    def test_permissions(self):
        """Testa as permissões no banco de dados"""
        try:
            print_info("Testando permissões...")
            
            # Listar collections existentes
            collections = self.db.list_collection_names()
            print_info(f"Collections existentes: {collections}")
            
            # Testar permissão de escrita
            test_collection = self.db.test_permissions
            test_doc = {"test": "permission_check"}
            
            result = test_collection.insert_one(test_doc)
            test_collection.delete_one({"_id": result.inserted_id})
            
            print_success("Permissões de leitura e escrita confirmadas")
            return True
            
        except Exception as e:
            print_error(f"Erro ao testar permissões: {e}")
            return False
    
    def create_collections(self):
        """Cria as collections no MongoDB (se não existirem)"""
        try:
            collections = self.db.list_collection_names()
            
            for collection_name in COLLECTIONS.values():
                if collection_name not in collections:
                    self.db.create_collection(collection_name)
                    print_success(f"Collection '{collection_name}' criada!")
                else:
                    print_info(f"Collection '{collection_name}' já existe")
            
            return True
        except Exception as e:
            print_error(f"Erro ao criar collections: {e}")
            return False
    
    def insert_dataframes(self, carros_df, montadoras_df):
        """Insere os dataframes nas collections"""
        try:
            # Limpar collections existentes
            carros_deleted = self.db[COLLECTIONS['carros']].delete_many({})
            montadoras_deleted = self.db[COLLECTIONS['montadoras']].delete_many({})
            print_info(f"Collections limpas (carros: {carros_deleted.deleted_count}, montadoras: {montadoras_deleted.deleted_count})")
            
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
        """Executa a agregação conforme especificado no desafio"""
        try:
            print_info("Executando agregação...")
            
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
            
            print_success("Agregação executada com sucesso!")
            print_info("Resultado da agregação:")
            
            for doc in result:
                print(f"\n?? País: {doc['_id']}")
                for carro in doc['carros']:
                    print(f"  ?? {carro['carro']} ({carro['cor']}) - {carro['montadora']}")
            
            # Salvar resultado em arquivo
            self.save_aggregation_result(result)
            
            return result
            
        except Exception as e:
            print_error(f"Erro na agregação: {e}")
            return None
    
    def save_aggregation_result(self, result):
        """Salva o resultado da agregação em arquivo JSON"""
        try:
            os.makedirs('mongodb/exports', exist_ok=True)
            
            filename = f'mongodb/exports/aggregation_result_remote_{MONGODB_CONFIG["host"]}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
            
            print_success(f"Resultado da agregação salvo em '{filename}'")
            
        except Exception as e:
            print_error(f"Erro ao salvar resultado: {e}")
    
    def export_collections(self):
        """Exporta as collections para arquivos JSON"""
        try:
            os.makedirs('mongodb/exports', exist_ok=True)
            
            # Exportar carros
            carros = list(self.db[COLLECTIONS['carros']].find({}))
            filename_carros = f'mongodb/exports/carros_remote_{MONGODB_CONFIG["host"]}.json'
            with open(filename_carros, 'w', encoding='utf-8') as f:
                json.dump(carros, f, indent=2, ensure_ascii=False, default=str)
            print_success(f"Collection 'carros' exportada para '{filename_carros}'")
            
            # Exportar montadoras
            montadoras = list(self.db[COLLECTIONS['montadoras']].find({}))
            filename_montadoras = f'mongodb/exports/montadoras_remote_{MONGODB_CONFIG["host"]}.json'
            with open(filename_montadoras, 'w', encoding='utf-8') as f:
                json.dump(montadoras, f, indent=2, ensure_ascii=False, default=str)
            print_success(f"Collection 'montadoras' exportada para '{filename_montadoras}'")
            
            return True
        except Exception as e:
            print_error(f"Erro ao exportar collections: {e}")
            return False
    
    def get_server_status(self):
        """Obtém informações do status do servidor"""
        try:
            print_info("Obtendo status do servidor...")
            
            server_status = self.db.command("serverStatus")
            
            print_info(f"Host: {server_status.get('host', 'Desconhecido')}")
            print_info(f"Versão: {server_status.get('version', 'Desconhecida')}")
            print_info(f"Uptime: {server_status.get('uptime', 0)} segundos")
            
            # Informações de conexões
            connections = server_status.get('connections', {})
            print_info(f"Conexões ativas: {connections.get('current', 0)}")
            print_info(f"Conexões disponíveis: {connections.get('available', 0)}")
            
        except Exception as e:
            print_warning(f"Não foi possível obter status do servidor: {e}")
    
    def close_connection(self):
        """Fecha a conexão com o MongoDB"""
        if self.client:
            self.client.close()
            print_info("Conexão fechada")

def show_configuration_help():
    """Exibe ajuda sobre configuração"""
    print_header("CONFIGURAÇÃO DO SERVIDOR REMOTO")
    print_info("Para conectar a um servidor MongoDB remoto, configure:")
    print_info("")
    print_info("1. Arquivo configs/remote_config.py:")
    print_info("   - MONGODB_CONFIG['host'] = 'IP_DO_SERVIDOR'")
    print_info("   - MONGODB_CONFIG['port'] = PORTA")
    print_info("   - MONGODB_CONFIG['username'] = 'USUARIO'")
    print_info("   - MONGODB_CONFIG['password'] = 'SENHA'")
    print_info("")
    print_info("2. Ou usando variáveis de ambiente (.env):")
    print_info("   - MONGO_HOST=192.168.22.111")
    print_info("   - MONGO_PORT=27017")
    print_info("   - MONGO_USERNAME=seu_usuario")
    print_info("   - MONGO_PASSWORD=sua_senha")
    print_info("")

def main():
    """Função principal"""
    print_header("DESAFIO DATAOPS - EXECUÇÃO REMOTA")
    
    # Exibir configurações atuais (sem senha)
    print_info(f"Servidor configurado: {MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}")
    print_info(f"Database: {MONGODB_CONFIG['database']}")
    print_info(f"Usuário: {MONGODB_CONFIG['username'] or 'Não configurado'}")
    print("")
    
    # Criar instância do gerenciador
    mongo_manager = MongoDBRemoteManager()
    
    try:
        # 1. Conectar ao MongoDB
        if not mongo_manager.connect():
            show_configuration_help()
            return
        
        # 2. Testar permissões
        if not mongo_manager.test_permissions():
            return
        
        # 3. Obter status do servidor
        mongo_manager.get_server_status()
        
        # 4. Criar collections
        if not mongo_manager.create_collections():
            return
        
        # 5. Criar dataframes
        print_header("CRIANDO DATAFRAMES")
        carros_df = create_carros_dataframe()
        montadoras_df = create_montadoras_dataframe()
        
        # 6. Inserir dados no MongoDB
        print_header("INSERINDO DADOS NO MONGODB")
        if not mongo_manager.insert_dataframes(carros_df, montadoras_df):
            return
        
        # 7. Executar agregação
        print_header("EXECUTANDO AGREGAÇÃO")
        aggregation_result = mongo_manager.create_aggregation()
        
        if aggregation_result is None:
            return
        
        # 8. Exportar collections
        print_header("EXPORTANDO COLLECTIONS")
        if not mongo_manager.export_collections():
            return
        
        print_header("EXECUÇÃO CONCLUÍDA COM SUCESSO!")
        print_success("Todos os passos foram executados com sucesso!")
        print_info("Arquivos gerados:")
        print_info(f"  ?? mongodb/exports/carros_remote_{MONGODB_CONFIG['host']}.json")
        print_info(f"  ?? mongodb/exports/montadoras_remote_{MONGODB_CONFIG['host']}.json")
        print_info(f"  ?? mongodb/exports/aggregation_result_remote_{MONGODB_CONFIG['host']}.json")
        
    except KeyboardInterrupt:
        print_error("Execução interrompida pelo usuário")
    except Exception as e:
        print_error(f"Erro durante execução: {e}")
    finally:
        mongo_manager.close_connection()

if __name__ == "__main__":
    main()
