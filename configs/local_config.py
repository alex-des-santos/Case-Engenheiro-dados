# -*- coding: utf-8 -*-
"""
Configuração para MongoDB Local
"""

# Configurações do MongoDB Local
MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'dataops_challenge',
    'username': None,  # Para MongoDB local sem autenticação
    'password': None,
    'auth_source': None
}

# Collections
COLLECTIONS = {
    'carros': 'carros',
    'montadoras': 'montadoras'
}

# Configurações de conexão
CONNECTION_TIMEOUT = 5000  # 5 segundos
SERVER_SELECTION_TIMEOUT = 5000  # 5 segundos

def get_connection_string():
    """Retorna a string de conexão para MongoDB local"""
    config = MONGODB_CONFIG
    return f"mongodb://{config['host']}:{config['port']}/{config['database']}"

def get_connection_params():
    """Retorna parâmetros de conexão"""
    return {
        'serverSelectionTimeoutMS': SERVER_SELECTION_TIMEOUT,
        'connectTimeoutMS': CONNECTION_TIMEOUT,
        'socketTimeoutMS': CONNECTION_TIMEOUT
    }
