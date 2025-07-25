# -*- coding: utf-8 -*-
"""
Configura��o para MongoDB Remoto
Exemplo de conex�o para servidor 192.168.22.111
"""

import os
from dotenv import load_dotenv

# Carregar vari�veis de ambiente
load_dotenv()

# Configura��es do MongoDB Remoto
MONGODB_CONFIG = {
    'host': os.getenv('MONGO_HOST', '192.168.22.111'),
    'port': int(os.getenv('MONGO_PORT', 27017)),
    'database': os.getenv('MONGO_DATABASE', 'dataops_challenge'),
    'username': os.getenv('MONGO_USERNAME', 'dataops_user'),
    'password': os.getenv('MONGO_PASSWORD', 'dataops_password'),
    'auth_source': os.getenv('MONGO_AUTH_SOURCE', 'admin')
}

# Collections
COLLECTIONS = {
    'carros': 'carros',
    'montadoras': 'montadoras'
}

# Configura��es de conex�o
CONNECTION_TIMEOUT = 10000  # 10 segundos para conex�es remotas
SERVER_SELECTION_TIMEOUT = 10000  # 10 segundos

# Configura��es de SSL (se necess�rio)
SSL_CONFIG = {
    'tls': os.getenv('MONGO_TLS', 'false').lower() == 'true',
    'tlsAllowInvalidCertificates': os.getenv('MONGO_TLS_ALLOW_INVALID_CERTS', 'false').lower() == 'true'
}

def get_connection_string():
    """Retorna a string de conex�o para MongoDB remoto"""
    config = MONGODB_CONFIG
    
    if config['username'] and config['password']:
        auth_string = f"{config['username']}:{config['password']}@"
    else:
        auth_string = ""
    
    base_url = f"mongodb://{auth_string}{config['host']}:{config['port']}/{config['database']}"
    
    # Adicionar par�metros de autentica��o se necess�rio
    params = []
    if config['auth_source']:
        params.append(f"authSource={config['auth_source']}")
    
    if SSL_CONFIG['tls']:
        params.append("tls=true")
        if SSL_CONFIG['tlsAllowInvalidCertificates']:
            params.append("tlsAllowInvalidCertificates=true")
    
    if params:
        base_url += "?" + "&".join(params)
    
    return base_url

def get_connection_params():
    """Retorna par�metros de conex�o"""
    params = {
        'serverSelectionTimeoutMS': SERVER_SELECTION_TIMEOUT,
        'connectTimeoutMS': CONNECTION_TIMEOUT,
        'socketTimeoutMS': CONNECTION_TIMEOUT
    }
    
    # Adicionar configura��es SSL se habilitado
    if SSL_CONFIG['tls']:
        params['tls'] = True
        if SSL_CONFIG['tlsAllowInvalidCertificates']:
            params['tlsAllowInvalidCertificates'] = True
    
    return params

def validate_remote_config():
    """Valida se as configura��es remotas est�o corretas"""
    config = MONGODB_CONFIG
    
    required_fields = ['host', 'port', 'database']
    missing_fields = [field for field in required_fields if not config.get(field)]
    
    if missing_fields:
        raise ValueError(f"Configura��es obrigat�rias ausentes: {missing_fields}")
    
    return True
