# Conexão Remota - MongoDB

Este guia detalha como configurar e conectar a um servidor MongoDB remoto (exemplo: 192.168.22.111) para executar o desafio DataOps.

## ?? Visão Geral

A conexão remota permite executar o desafio DataOps em um servidor MongoDB localizado em outra máquina da rede, proporcionando:
- Centralização dos dados
- Maior disponibilidade
- Separação entre aplicação e banco de dados
- Ambiente mais próximo à produção

## ?? Configuração do Servidor Remoto

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

```bash
# Conectar ao MongoDB no servidor
mongosh

# Criar usuário administrador
use admin
db.createUser({
  user: "admin",
  pwd: "senha_admin_segura",
  roles: ["root"]
})

# Criar usuário específico para o projeto
use dataops_challenge
db.createUser({
  user: "dataops_user",
  pwd: "dataops_password",
  roles: [
    { role: "readWrite", db: "dataops_challenge" },
    { role: "dbAdmin", db: "dataops_challenge" }
  ]
})

# Sair e reconectar com autenticação
exit
mongosh -u admin -p senha_admin_segura --authenticationDatabase admin
```

### Configuração de Firewall no Servidor

#### Ubuntu/Debian (UFW)
```bash
# Permitir conexão MongoDB
sudo ufw allow from 192.168.22.0/24 to any port 27017
# ou para IP específico
sudo ufw allow from 192.168.22.100 to any port 27017

# Verificar regras
sudo ufw status
```

#### CentOS/RHEL (firewalld)
```bash
# Permitir porta MongoDB
sudo firewall-cmd --permanent --add-port=27017/tcp
sudo firewall-cmd --reload

# Ou criar zona específica
sudo firewall-cmd --permanent --new-zone=mongodb
sudo firewall-cmd --permanent --zone=mongodb --add-source=192.168.22.0/24
sudo firewall-cmd --permanent --zone=mongodb --add-port=27017/tcp
sudo firewall-cmd --reload
```

## ??? Configuração do Cliente

### 1. Arquivo de Configuração

Edite o arquivo `configs/remote_config.py`:

```python
# configs/remote_config.py
MONGODB_CONFIG = {
    'host': '192.168.22.111',
    'port': 27017,
    'database': 'dataops_challenge',
    'username': 'dataops_user',
    'password': 'dataops_password',
    'auth_source': 'dataops_challenge'  # ou 'admin'
}
```

### 2. Usando Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
MONGO_HOST=192.168.22.111
MONGO_PORT=27017
MONGO_DATABASE=dataops_challenge
MONGO_USERNAME=dataops_user
MONGO_PASSWORD=dataops_password
MONGO_AUTH_SOURCE=dataops_challenge
MONGO_TLS=false
MONGO_TLS_ALLOW_INVALID_CERTS=false
```

**Importante**: Adicione `.env` ao `.gitignore` para não versionar senhas!

### 3. Configuração SSL/TLS (se necessário)

```python
# configs/remote_config.py
SSL_CONFIG = {
    'tls': True,
    'tlsAllowInvalidCertificates': True,  # Apenas para desenvolvimento
    'tlsCAFile': '/path/to/ca.pem',      # Certificado CA
    'tlsCertificateKeyFile': '/path/to/client.pem'  # Certificado cliente
}
```

## ?? Execução

### Teste de Conectividade

```bash
# Testar conectividade de rede
ping 192.168.22.111

# Testar porta MongoDB
telnet 192.168.22.111 27017
# ou
nc -zv 192.168.22.111 27017
```

### Teste de Conexão MongoDB

```bash
# Conectar via mongosh (se instalado localmente)
mongosh "mongodb://dataops_user:dataops_password@192.168.22.111:27017/dataops_challenge"

# Testar sem autenticação
mongosh "mongodb://192.168.22.111:27017/dataops_challenge"
```

### Executar Script Python

```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\Activate.ps1  # Windows

# Executar script remoto
python scripts/main_remote.py
```

## ?? Monitoramento e Logs

### No Servidor
```bash
# Monitorar logs do MongoDB
sudo tail -f /var/log/mongodb/mongod.log

# Monitorar conexões ativas
mongosh --eval "db.runCommand('currentOp')"

# Verificar status do servidor
mongosh --eval "db.runCommand('serverStatus')"
```

### No Cliente
```bash
# Executar com debug
python scripts/main_remote.py --verbose

# Verificar conectividade
python -c "
from pymongo import MongoClient
import sys
try:
    client = MongoClient('mongodb://192.168.22.111:27017/', serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print('? Conexão bem-sucedida!')
except Exception as e:
    print(f'? Erro na conexão: {e}')
    sys.exit(1)
"
```

## ?? Exemplos de String de Conexão

### Sem Autenticação
```python
mongodb://192.168.22.111:27017/dataops_challenge
```

### Com Autenticação
```python
mongodb://usuario:senha@192.168.22.111:27017/dataops_challenge?authSource=admin
```

### Com SSL
```python
mongodb://usuario:senha@192.168.22.111:27017/dataops_challenge?authSource=admin&tls=true
```

### Replica Set
```python
mongodb://usuario:senha@mongo1.example.com:27017,mongo2.example.com:27017,mongo3.example.com:27017/dataops_challenge?replicaSet=rs0&authSource=admin
```

## ??? Troubleshooting

### Erro: "Connection refused"
```bash
# Verificar se MongoDB está rodando no servidor
sudo systemctl status mongod

# Verificar se porta está aberta
sudo netstat -tlnp | grep :27017

# Verificar firewall
sudo ufw status
```

### Erro: "Authentication failed"
```bash
# Verificar usuários existentes
mongosh -u admin -p --authenticationDatabase admin
db.getUsers()

# Recriar usuário se necessário
db.dropUser('dataops_user')
db.createUser({...})
```

### Erro: "Network timeout"
```bash
# Verificar conectividade
ping 192.168.22.111
traceroute 192.168.22.111

# Testar porta específica
telnet 192.168.22.111 27017
```

### Erro: "SSL/TLS required"
```python
# Habilitar SSL na configuração
SSL_CONFIG = {
    'tls': True,
    'tlsAllowInvalidCertificates': True  # Apenas para desenvolvimento
}
```

## ?? Segurança

### Boas Práticas

1. **Usar autenticação sempre**
```javascript
// Criar usuários com permissões mínimas
db.createUser({
  user: "app_user",
  pwd: "strong_password",
  roles: [{ role: "readWrite", db: "dataops_challenge" }]
})
```

2. **Configurar bind IP específico**
```yaml
# mongod.conf
net:
  bindIp: 127.0.0.1,192.168.22.111  # IPs específicos
```

3. **Usar SSL/TLS em produção**
```yaml
# mongod.conf
net:
  tls:
    mode: requireTLS
    certificateKeyFile: /path/to/server.pem
    CAFile: /path/to/ca.pem
```

4. **Configurar firewall restritivo**
```bash
# Permitir apenas IPs específicos
sudo ufw allow from 192.168.22.100 to any port 27017
```

5. **Monitorar logs regularmente**
```bash
# Configurar logrotate para MongoDB
sudo nano /etc/logrotate.d/mongodb
```

## ?? Performance

### Otimizações de Rede
```python
# configs/remote_config.py
CONNECTION_PARAMS = {
    'maxPoolSize': 10,           # Pool de conexões
    'minPoolSize': 1,
    'maxIdleTimeMS': 30000,      # 30 segundos
    'connectTimeoutMS': 10000,   # 10 segundos para conexões remotas
    'socketTimeoutMS': 30000,    # 30 segundos
    'serverSelectionTimeoutMS': 10000,
    'retryWrites': True,
    'w': 'majority'              # Write concern
}
```

### Monitoramento
```bash
# No servidor, instalar MongoDB tools
sudo apt-get install mongodb-database-tools

# Monitorar operações
mongostat --host 192.168.22.111:27017 -u admin -p

# Monitorar performance
mongotop --host 192.168.22.111:27017 -u admin -p
```

## ? Checklist de Configuração

### Servidor (192.168.22.111)
- [ ] MongoDB instalado e rodando
- [ ] Configuração de bind IP atualizada
- [ ] Firewall configurado
- [ ] Usuários criados (se autenticação habilitada)
- [ ] SSL/TLS configurado (se necessário)

### Cliente
- [ ] Dependências Python instaladas
- [ ] Arquivo de configuração atualizado
- [ ] Variáveis de ambiente configuradas
- [ ] Conectividade testada
- [ ] Script executado com sucesso

## ?? Próximos Passos

1. **Implementar backup automatizado**
2. **Configurar replicação** (se necessário)
3. **Implementar monitoramento** avançado
4. **Configurar alertas** de performance
5. **Documentar procedimentos** de disaster recovery

## ?? Suporte

Para problemas de conexão remota:
1. Verificar logs do servidor: `/var/log/mongodb/mongod.log`
2. Testar conectividade de rede
3. Validar configurações de firewall
4. Confirmar credenciais de autenticação
