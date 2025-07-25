# Conexão Remota - MongoDB

Este guia detalha como configurar e conectar a um servidor MongoDB remoto (exemplo: 192.168.22.111) para executar o desafio DataOps.

## 🌐 Visão Geral

A conexão remota permite executar o desafio DataOps em um servidor MongoDB localizado em outra máquina da rede, proporcionando:
- Centralização dos dados
- Maior disponibilidade
- Separação entre aplicação e banco de dados
- Ambiente mais próximo à produção

## 🖥️ Configuração do Servidor Remoto

### Pré-requisitos no Servidor (192.168.22.111)

1. **MongoDB instalado e rodando**
2. **Firewall configurado** para permitir conexões na porta 27017
3. **Autenticação configurada** (opcional, mas recomendado)
4. **Rede acessível** a partir da máquina cliente

### Configuração do MongoDB no Servidor

#### 1. Editar arquivo de configuração
```bash
# No servidor remoto (192.168.22.111)
sudo nano /etc/mongod.conf
```

#### 2. Configurar bind IP
```yaml
# /etc/mongod.conf
net:
  port: 27017
  bindIp: 0.0.0.0  # Permite conexões de qualquer IP
  # bindIp: 127.0.0.1,192.168.22.111  # Mais seguro: especificar IPs
```

#### 3. Habilitar autenticação (recomendado)
```yaml
# /etc/mongod.conf
security:
  authorization: enabled
```

#### 4. Reiniciar MongoDB
```bash
sudo systemctl restart mongod
sudo systemctl status mongod
```

### Configuração de Usuários (se autenticação habilitada)

#### 1. Conectar sem autenticação (primeira vez)
```bash
mongosh --host 192.168.22.111
```

#### 2. Criar usuário administrador
```javascript
use admin
db.createUser({
  user: "admin",
  pwd: "senha_forte_admin",
  roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]
})
```

#### 3. Criar usuário específico para o projeto
```javascript
use dataops_db
db.createUser({
  user: "dataops_user",
  pwd: "senha_dataops",
  roles: [
    { role: "readWrite", db: "dataops_db" }
  ]
})
```

#### 4. Sair e reconectar com autenticação
```bash
exit
mongosh --host 192.168.22.111 -u admin -p senha_forte_admin --authenticationDatabase admin
```

### Configuração de Firewall no Servidor

#### Ubuntu/Debian (UFW)
```bash
# Permitir conexão MongoDB
sudo ufw allow 27017
# ou para IP específico
sudo ufw allow from 192.168.22.0/24 to any port 27017
```

#### CentOS/RHEL (firewalld)
```bash
# Abrir porta
sudo firewall-cmd --permanent --add-port=27017/tcp
sudo firewall-cmd --reload

# Ou criar zona específica
sudo firewall-cmd --permanent --new-zone=mongodb
sudo firewall-cmd --permanent --zone=mongodb --add-source=192.168.22.0/24
sudo firewall-cmd --permanent --zone=mongodb --add-port=27017/tcp
sudo firewall-cmd --reload
```

## 💻 Configuração do Cliente

### 1. Arquivo de Configuração

Edite `configs/remote_config.py`:
```python
REMOTE_CONFIG = {
    'host': '192.168.22.111',
    'port': 27017,
    'database': 'dataops_db',
    'username': 'dataops_user',  # se autenticação habilitada
    'password': 'senha_dataops',  # se autenticação habilitada
    'authentication_source': 'dataops_db',
    'ssl': False,  # True se SSL configurado
    'ssl_cert_reqs': None
}
```

### 2. Usando Variáveis de Ambiente (.env)

Crie arquivo `.env` na raiz do projeto:
```bash
# Configuração MongoDB Remoto
MONGO_HOST=192.168.22.111
MONGO_PORT=27017
MONGO_DATABASE=dataops_db
MONGO_USERNAME=dataops_user
MONGO_PASSWORD=senha_dataops
MONGO_AUTH_SOURCE=dataops_db
MONGO_SSL=false
```

**Importante**: Adicione `.env` ao `.gitignore` para não versionar senhas!

### 3. Executar o Script Remoto

```bash
# Usando configuração em arquivo
python scripts/main_remote.py

# Ou com variáveis de ambiente
export MONGO_HOST=192.168.22.111
export MONGO_USERNAME=dataops_user
export MONGO_PASSWORD=senha_dataops
python scripts/main_remote.py
```

## 🧪 Teste de Conectividade

### 1. Teste Básico de Rede
```bash
# Verificar se porta está aberta
telnet 192.168.22.111 27017
# ou
nc -zv 192.168.22.111 27017
```

### 2. Teste MongoDB Direto
```bash
# Sem autenticação
mongosh --host 192.168.22.111

# Com autenticação
mongosh --host 192.168.22.111 -u dataops_user -p senha_dataops --authenticationDatabase dataops_db
```

### 3. Teste com Python
```python
from pymongo import MongoClient

try:
    client = MongoClient(
        host='192.168.22.111',
        port=27017,
        username='dataops_user',
        password='senha_dataops',
        authSource='dataops_db',
        serverSelectionTimeoutMS=5000
    )
    
    # Testar conexão
    client.admin.command('ping')
    print("✅ Conexão MongoDB remota bem-sucedida!")
    
except Exception as e:
    print(f"❌ Erro de conexão: {e}")
```

## 🔒 Configuração SSL/TLS (Opcional)

### No Servidor MongoDB

#### 1. Gerar certificados
```bash
# Certificado auto-assinado (desenvolvimento)
openssl req -newkey rsa:2048 -new -x509 -days 3653 -nodes -out mongodb-cert.crt -keyout mongodb-cert.key
cat mongodb-cert.key mongodb-cert.crt > mongodb.pem
```

#### 2. Configurar mongod.conf
```yaml
net:
  port: 27017
  bindIp: 0.0.0.0
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/ssl/mongodb.pem
```

### No Cliente Python

```python
import ssl
from pymongo import MongoClient

client = MongoClient(
    host='192.168.22.111',
    port=27017,
    username='dataops_user',
    password='senha_dataops',
    authSource='dataops_db',
    tls=True,
    tlsCertificateKeyFile='/path/to/client.pem',
    tlsCAFile='/path/to/ca.pem',
    tlsAllowInvalidCertificates=True  # Apenas para desenvolvimento
)
```

## 🐳 Usando Docker no Servidor Remoto

### 1. Docker Compose no Servidor
```yaml
# docker-compose.yml no servidor 192.168.22.111
version: '3.8'
services:
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin_password
      MONGO_INITDB_DATABASE: dataops_db
    volumes:
      - mongodb_data:/data/db
      - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
    networks:
      - mongodb_network

volumes:
  mongodb_data:

networks:
  mongodb_network:
```

### 2. Script de inicialização (mongo-init.js)
```javascript
// mongo-init.js
db = db.getSiblingDB('dataops_db');

db.createUser({
  user: 'dataops_user',
  pwd: 'senha_dataops',
  roles: [
    {
      role: 'readWrite',
      db: 'dataops_db'
    }
  ]
});
```

### 3. Iniciar no servidor
```bash
# No servidor 192.168.22.111
docker-compose up -d
```

## 🛠️ Troubleshooting

### Problemas Comuns

#### 1. Conexão Recusada
```
pymongo.errors.ServerSelectionTimeoutError: [Errno 111] Connection refused
```

**Soluções:**
- Verificar se MongoDB está rodando: `sudo systemctl status mongod`
- Verificar bindIp no mongod.conf
- Verificar firewall: `sudo ufw status`
- Testar conectividade: `telnet 192.168.22.111 27017`

#### 2. Erro de Autenticação
```
pymongo.errors.OperationFailure: Authentication failed
```

**Soluções:**
- Verificar usuário e senha
- Confirmar authenticationDatabase
- Verificar se usuário tem permissões na database

#### 3. Timeout de Conexão
```
pymongo.errors.ServerSelectionTimeoutError: timed out
```

**Soluções:**
- Aumentar serverSelectionTimeoutMS
- Verificar latência de rede: `ping 192.168.22.111`
- Verificar se não há proxy/firewall bloqueando

#### 4. Erro SSL/TLS
```
pymongo.errors.ConfigurationError: TLS is not available
```

**Soluções:**
- Instalar dependências TLS: `pip install pymongo[tls]`
- Verificar certificados no servidor
- Testar sem TLS primeiro

### Logs Úteis

#### No Servidor MongoDB
```bash
# Logs do sistema
sudo journalctl -u mongod -f

# Logs do MongoDB
sudo tail -f /var/log/mongodb/mongod.log
```

#### No Cliente Python
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Monitoramento

### 1. Status do Servidor
```bash
# Via mongosh
mongosh --host 192.168.22.111 -u admin -p admin_password --eval "db.serverStatus()"
```

### 2. Conexões Ativas
```javascript
// No mongosh
db.serverStatus().connections
```

### 3. Métricas de Performance
```javascript
// No mongosh
db.serverStatus().opcounters
db.serverStatus().network
```

## ✅ Checklist de Configuração

### Servidor MongoDB
- [ ] MongoDB instalado e rodando
- [ ] bindIp configurado para aceitar conexões externas
- [ ] Firewall liberado para porta 27017
- [ ] Usuários criados (se autenticação habilitada)
- [ ] SSL configurado (se necessário)
- [ ] Logs monitorados

### Cliente Python
- [ ] Arquivo .env configurado
- [ ] Dependências instaladas (pymongo)
- [ ] Teste de conectividade realizado
- [ ] Scripts executados com sucesso
- [ ] Dados inseridos e consultados

### Rede
- [ ] Conectividade IP verificada
- [ ] Porta 27017 acessível
- [ ] DNS resolvendo (se usando hostname)
- [ ] Sem proxy/firewall bloqueando
- [ ] Latência de rede aceitável

---

**Próximos Passos:**
1. Configurar servidor remoto seguindo este guia
2. Testar conectividade básica
3. Executar `python scripts/main_remote.py`
4. Verificar dados no MongoDB Compass
5. Monitorar logs para troubleshooting

Para dúvidas específicas, consulte a [documentação do MongoDB](https://docs.mongodb.com/) ou abra uma issue no repositório.
