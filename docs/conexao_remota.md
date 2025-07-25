# Conex�o Remota - MongoDB

Este guia detalha como configurar e conectar a um servidor MongoDB remoto (exemplo: 192.168.22.111) para executar o desafio DataOps.

## ?? Vis�o Geral

A conex�o remota permite executar o desafio DataOps em um servidor MongoDB localizado em outra m�quina da rede, proporcionando:
- Centraliza��o dos dados
- Maior disponibilidade
- Separa��o entre aplica��o e banco de dados
- Ambiente mais pr�ximo � produ��o

## ?? Configura��o do Servidor Remoto

### Pr�-requisitos no Servidor (192.168.22.111)

1. **MongoDB instalado e rodando**
2. **Firewall configurado** para permitir conex�es na porta 27017
3. **Autentica��o configurada** (opcional, mas recomendado)
4. **Rede acess�vel** a partir da m�quina cliente

### Configura��o do MongoDB no Servidor

#### 1. Editar arquivo de configura��o
```bash
# No servidor remoto (192.168.22.111)
sudo nano /etc/mongod.conf
```

#### 2. Configurar bind IP
```yaml
# /etc/mongod.conf
net:
  port: 27017
  bindIp: 0.0.0.0  # Permite conex�es de qualquer IP
  # bindIp: 127.0.0.1,192.168.22.111  # Mais seguro: especificar IPs
```

#### 3. Habilitar autentica��o (recomendado)
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

### Configura��o de Usu�rios (se autentica��o habilitada)

```bash
# Conectar ao MongoDB no servidor
mongosh

# Criar usu�rio administrador
use admin
db.createUser({
  user: "admin",
  pwd: "senha_admin_segura",
  roles: ["root"]
})

# Criar usu�rio espec�fico para o projeto
use dataops_challenge
db.createUser({
  user: "dataops_user",
  pwd: "dataops_password",
  roles: [
    { role: "readWrite", db: "dataops_challenge" },
    { role: "dbAdmin", db: "dataops_challenge" }
  ]
})

# Sair e reconectar com autentica��o
exit
mongosh -u admin -p senha_admin_segura --authenticationDatabase admin
```

### Configura��o de Firewall no Servidor

#### Ubuntu/Debian (UFW)
```bash
# Permitir conex�o MongoDB
sudo ufw allow from 192.168.22.0/24 to any port 27017
# ou para IP espec�fico
sudo ufw allow from 192.168.22.100 to any port 27017

# Verificar regras
sudo ufw status
```

#### CentOS/RHEL (firewalld)
```bash
# Permitir porta MongoDB
sudo firewall-cmd --permanent --add-port=27017/tcp
sudo firewall-cmd --reload

# Ou criar zona espec�fica
sudo firewall-cmd --permanent --new-zone=mongodb
sudo firewall-cmd --permanent --zone=mongodb --add-source=192.168.22.0/24
sudo firewall-cmd --permanent --zone=mongodb --add-port=27017/tcp
sudo firewall-cmd --reload
```

## ??? Configura��o do Cliente

### 1. Arquivo de Configura��o

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

### 2. Usando Vari�veis de Ambiente (.env)

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

**Importante**: Adicione `.env` ao `.gitignore` para n�o versionar senhas!

### 3. Configura��o SSL/TLS (se necess�rio)

```python
# configs/remote_config.py
SSL_CONFIG = {
    'tls': True,
    'tlsAllowInvalidCertificates': True,  # Apenas para desenvolvimento
    'tlsCAFile': '/path/to/ca.pem',      # Certificado CA
    'tlsCertificateKeyFile': '/path/to/client.pem'  # Certificado cliente
}
```

## ?? Execu��o

### Teste de Conectividade

```bash
# Testar conectividade de rede
ping 192.168.22.111

# Testar porta MongoDB
telnet 192.168.22.111 27017
# ou
nc -zv 192.168.22.111 27017
```

### Teste de Conex�o MongoDB

```bash
# Conectar via mongosh (se instalado localmente)
mongosh "mongodb://dataops_user:dataops_password@192.168.22.111:27017/dataops_challenge"

# Testar sem autentica��o
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

# Monitorar conex�es ativas
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
    print('? Conex�o bem-sucedida!')
except Exception as e:
    print(f'? Erro na conex�o: {e}')
    sys.exit(1)
"
```

## ?? Exemplos de String de Conex�o

### Sem Autentica��o
```python
mongodb://192.168.22.111:27017/dataops_challenge
```

### Com Autentica��o
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
# Verificar se MongoDB est� rodando no servidor
sudo systemctl status mongod

# Verificar se porta est� aberta
sudo netstat -tlnp | grep :27017

# Verificar firewall
sudo ufw status
```

### Erro: "Authentication failed"
```bash
# Verificar usu�rios existentes
mongosh -u admin -p --authenticationDatabase admin
db.getUsers()

# Recriar usu�rio se necess�rio
db.dropUser('dataops_user')
db.createUser({...})
```

### Erro: "Network timeout"
```bash
# Verificar conectividade
ping 192.168.22.111
traceroute 192.168.22.111

# Testar porta espec�fica
telnet 192.168.22.111 27017
```

### Erro: "SSL/TLS required"
```python
# Habilitar SSL na configura��o
SSL_CONFIG = {
    'tls': True,
    'tlsAllowInvalidCertificates': True  # Apenas para desenvolvimento
}
```

## ?? Seguran�a

### Boas Pr�ticas

1. **Usar autentica��o sempre**
```javascript
// Criar usu�rios com permiss�es m�nimas
db.createUser({
  user: "app_user",
  pwd: "strong_password",
  roles: [{ role: "readWrite", db: "dataops_challenge" }]
})
```

2. **Configurar bind IP espec�fico**
```yaml
# mongod.conf
net:
  bindIp: 127.0.0.1,192.168.22.111  # IPs espec�ficos
```

3. **Usar SSL/TLS em produ��o**
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
# Permitir apenas IPs espec�ficos
sudo ufw allow from 192.168.22.100 to any port 27017
```

5. **Monitorar logs regularmente**
```bash
# Configurar logrotate para MongoDB
sudo nano /etc/logrotate.d/mongodb
```

## ?? Performance

### Otimiza��es de Rede
```python
# configs/remote_config.py
CONNECTION_PARAMS = {
    'maxPoolSize': 10,           # Pool de conex�es
    'minPoolSize': 1,
    'maxIdleTimeMS': 30000,      # 30 segundos
    'connectTimeoutMS': 10000,   # 10 segundos para conex�es remotas
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

# Monitorar opera��es
mongostat --host 192.168.22.111:27017 -u admin -p

# Monitorar performance
mongotop --host 192.168.22.111:27017 -u admin -p
```

## ? Checklist de Configura��o

### Servidor (192.168.22.111)
- [ ] MongoDB instalado e rodando
- [ ] Configura��o de bind IP atualizada
- [ ] Firewall configurado
- [ ] Usu�rios criados (se autentica��o habilitada)
- [ ] SSL/TLS configurado (se necess�rio)

### Cliente
- [ ] Depend�ncias Python instaladas
- [ ] Arquivo de configura��o atualizado
- [ ] Vari�veis de ambiente configuradas
- [ ] Conectividade testada
- [ ] Script executado com sucesso

## ?? Pr�ximos Passos

1. **Implementar backup automatizado**
2. **Configurar replica��o** (se necess�rio)
3. **Implementar monitoramento** avan�ado
4. **Configurar alertas** de performance
5. **Documentar procedimentos** de disaster recovery

## ?? Suporte

Para problemas de conex�o remota:
1. Verificar logs do servidor: `/var/log/mongodb/mongod.log`
2. Testar conectividade de rede
3. Validar configura��es de firewall
4. Confirmar credenciais de autentica��o
