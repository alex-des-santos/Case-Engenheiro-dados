# -*- coding: utf-8 -*-
"""
Configura��o para MongoDB Local
"""

# Configura��es do MongoDB Local
MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'dataops_challenge',
    'username': None,  # Para MongoDB local sem autentica��o
    'password': None,
    'auth_source': None
}

# Collections
COLLECTIONS = {
    'carros': 'carros',
    'montadoras': 'montadoras'
}

# Configura��es de conex�o
CONNECTION_TIMEOUT = 5000  # 5 segundos
SERVER_SELECTION_TIMEOUT = 5000  # 5 segundos

def get_connection_string():
    """Retorna a string de conex�o para MongoDB local"""
    config = MONGODB_CONFIG
    return f"mongodb://{config['host']}:{config['port']}/{config['database']}"

def get_connection_params():
    """Retorna par�metros de conex�o"""
    return {
        'serverSelectionTimeoutMS': SERVER_SELECTION_TIMEOUT,
        'connectTimeoutMS': CONNECTION_TIMEOUT,
        'socketTimeoutMS': CONNECTION_TIMEOUT
    }
