# -*- coding: utf-8 -*-
"""
Configuração para MongoDB Remoto
Exemplo de conexão para servidor 192.168.22.111
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do MongoDB Remoto
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

# Configurações de conexão
CONNECTION_TIMEOUT = 10000  # 10 segundos para conexões remotas
SERVER_SELECTION_TIMEOUT = 10000  # 10 segundos

# Configurações de SSL (se necessário)
SSL_CONFIG = {
    'tls': os.getenv('MONGO_TLS', 'false').lower() == 'true',
    'tlsAllowInvalidCertificates': os.getenv('MONGO_TLS_ALLOW_INVALID_CERTS', 'false').lower() == 'true'
}

def get_connection_string():
    """Retorna a string de conexão para MongoDB remoto"""
    config = MONGODB_CONFIG
    
    if config['username'] and config['password']:
        auth_string = f"{config['username']}:{config['password']}@"
    else:
        auth_string = ""
    
    base_url = f"mongodb://{auth_string}{config['host']}:{config['port']}/{config['database']}"
    
    # Adicionar parâmetros de autenticação se necessário
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
    """Retorna parâmetros de conexão"""
    params = {
        'serverSelectionTimeoutMS': SERVER_SELECTION_TIMEOUT,
        'connectTimeoutMS': CONNECTION_TIMEOUT,
        'socketTimeoutMS': CONNECTION_TIMEOUT
    }
    
    # Adicionar configurações SSL se habilitado
    if SSL_CONFIG['tls']:
        params['tls'] = True
        if SSL_CONFIG['tlsAllowInvalidCertificates']:
            params['tlsAllowInvalidCertificates'] = True
    
    return params

def validate_remote_config():
    """Valida se as configurações remotas estão corretas"""
    config = MONGODB_CONFIG
    
    required_fields = ['host', 'port', 'database']
    missing_fields = [field for field in required_fields if not config.get(field)]
    
    if missing_fields:
        raise ValueError(f"Configurações obrigatórias ausentes: {missing_fields}")
    
    return True
