# Instalação Local - Linux

Este guia detalha a instalação e configuração do ambiente para executar o desafio DataOps em sistemas Linux (Ubuntu, Debian, CentOS, Fedora).

## 🐧 Pré-requisitos

- Sistema Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+, Fedora 35+)
- Usuário com privilégios sudo
- Conexão com internet
- 2GB de RAM disponível
- 5GB de espaço em disco

## 🚀 Instalação Rápida

### Script Automatizado
```bash
# Download e execução do script de instalação
curl -fsSL https://raw.githubusercontent.com/SEU-USUARIO/Case-Engenheiro-dados/main/scripts/install_linux.sh | bash
```

## 📋 Instalação Manual Detalhada

### 1. Atualizar Sistema

#### Ubuntu/Debian
```bash
sudo apt update && sudo apt upgrade -y
```

#### CentOS/RHEL/Fedora
```bash
# CentOS/RHEL 8+
sudo dnf update -y

# Fedora
sudo dnf update -y

# CentOS 7 (se aplicável)
sudo yum update -y
```

### 2. Instalar Python 3.8+

#### Ubuntu/Debian
```bash
# Verificar versão atual
python3 --version

# Se versão < 3.8, instalar
sudo apt install python3.8 python3.8-venv python3.8-dev python3-pip -y

# Criar link simbólico (opcional)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
```

#### CentOS/RHEL/Fedora
```bash
# Verificar versão
python3 --version

# Instalar se necessário
sudo dnf install python3 python3-pip python3-venv python3-devel -y

# CentOS 7 (Python 3.8 via Software Collections)
sudo yum install centos-release-scl -y
sudo yum install rh-python38 -y
scl enable rh-python38 bash
```

### 3. Instalar Git

#### Ubuntu/Debian
```bash
sudo apt install git -y
```

#### CentOS/RHEL/Fedora
```bash
sudo dnf install git -y
```

#### Configurar Git
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
```

### 4. Instalar MongoDB

#### Método 1: Repositório Oficial (Recomendado)

##### Ubuntu
```bash
# Importar chave pública
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Adicionar repositório
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Atualizar e instalar
sudo apt update
sudo apt install mongodb-org -y
```

##### CentOS/RHEL/Fedora
```bash
# Criar arquivo de repositório
sudo tee /etc/yum.repos.d/mongodb-org-7.0.repo << EOF
[mongodb-org-7.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/7.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc
EOF

# Instalar
sudo dnf install mongodb-org -y
```

#### Método 2: Docker (Alternativo)
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Reiniciar sessão ou executar
newgrp docker

# Executar MongoDB via Docker
docker run -d --name mongodb -p 27017:27017 mongo:7.0
```

### 5. Configurar e Iniciar MongoDB

#### Iniciar serviço
```bash
# Habilitar e iniciar
sudo systemctl enable mongod
sudo systemctl start mongod

# Verificar status
sudo systemctl status mongod
```

#### Configurar MongoDB (opcional)
```bash
# Editar configuração
sudo nano /etc/mongod.conf

# Exemplo de configuração básica
storage:
  dbPath: /var/lib/mongo
  journal:
    enabled: true

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

net:
  port: 27017
  bindIp: 127.0.0.1

processManagement:
  fork: true
  pidFilePath: /var/run/mongodb/mongod.pid
```

#### Testar conexão
```bash
# Via mongosh (MongoDB Shell)
mongosh

# Comando de teste
> db.runCommand({connectionStatus: 1})
> exit
```

### 6. Clonar Repositório

```bash
# Navegar para diretório de projetos
cd ~/Projects  # ou local preferido

# Clonar repositório
git clone https://github.com/SEU-USUARIO/Case-Engenheiro-dados.git
cd Case-Engenheiro-dados
```

### 7. Configurar Ambiente Virtual Python

```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate

# Verificar se está ativo
which python
# Deve retornar: ~/Projects/Case-Engenheiro-dados/.venv/bin/python

# Atualizar pip
pip install --upgrade pip
```

### 8. Instalar Dependências Python

```bash
# Instalar dependências do projeto
pip install -r requirements.txt

# Verificar instalação
pip list
```

### 9. Configurar Variáveis de Ambiente (Opcional)

```bash
# Copiar template
cp .env.example .env

# Editar se necessário
nano .env

# Exemplo de conteúdo .env para local
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DATABASE=dataops_db
MONGO_USERNAME=
MONGO_PASSWORD=
```

## 🧪 Teste da Instalação

### 1. Teste de Dependências
```bash
python test_dependencies.py
```

**Saída esperada:**
```
✅ Python 3.8+ - OK
✅ Pandas - OK  
✅ PyMongo - OK
✅ Colorama - OK
✅ MongoDB Connection - OK
```

### 2. Teste Simples
```bash
python simple_test.py
```

### 3. Execução do Projeto
```bash
python scripts/main_local.py
```

**Saída esperada:**
```
🚀 Iniciando Desafio DataOps - MongoDB & Python
📊 Criando DataFrames...
✅ DataFrame Carros criado com 5 registros
✅ DataFrame Montadoras criado com 5 registros
🔗 Conectando ao MongoDB local...
✅ Conexão estabelecida com sucesso
📥 Inserindo dados no MongoDB...
✅ Collections criadas e populadas
🔄 Executando agregação...
✅ Agregação executada com sucesso
💾 Exportando resultados...
✅ Arquivos JSON exportados
🎉 Desafio concluído com sucesso!
```

## 📊 Ferramentas de Monitoramento

### 1. MongoDB Compass (GUI)

#### Ubuntu/Debian
```bash
# Download e instalação
wget https://downloads.mongodb.com/compass/mongodb-compass_1.40.4_amd64.deb
sudo dpkg -i mongodb-compass_1.40.4_amd64.deb
sudo apt-get install -f

# Executar
mongodb-compass
```

#### CentOS/RHEL/Fedora
```bash
# Download
wget https://downloads.mongodb.com/compass/mongodb-compass-1.40.4.x86_64.rpm
sudo rpm -ivh mongodb-compass-1.40.4.x86_64.rpm

# Executar
mongodb-compass
```

### 2. Mongo Shell (CLI)
```bash
# Instalar mongosh separadamente se necessário
curl -fsSL https://mongocli.s3.amazonaws.com/install.sh | sudo sh

# Conectar
mongosh mongodb://localhost:27017

# Comandos úteis
> show dbs
> use dataops_db
> show collections
> db.carros.find().pretty()
> db.montadoras.find().pretty()
```

## 🐳 Alternativa com Docker

### 1. Instalar Docker e Docker Compose

#### Ubuntu/Debian
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Reiniciar sessão
newgrp docker
```

### 2. Executar com Docker
```bash
# Subir MongoDB via Docker Compose
docker-compose -f docker/docker-compose.yml up -d

# Verificar containers
docker ps

# Executar aplicação
python scripts/main_local.py

# Parar containers
docker-compose -f docker/docker-compose.yml down
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. MongoDB não inicia
```bash
# Verificar logs
sudo journalctl -u mongod -f

# Verificar configuração
sudo nano /etc/mongod.conf

# Reiniciar serviço
sudo systemctl restart mongod
```

#### 2. Python não encontrado
```bash
# Verificar versão
python3 --version

# Criar link simbólico
sudo ln -sf /usr/bin/python3 /usr/bin/python
```

#### 3. Permissões de MongoDB
```bash
# Corrigir permissões
sudo chown -R mongodb:mongodb /var/lib/mongo
sudo chown mongodb:mongodb /var/log/mongodb/mongod.log
sudo systemctl restart mongod
```

#### 4. Erro de conexão PyMongo
```bash
# Verificar se MongoDB está rodando
sudo systemctl status mongod

# Testar conexão
mongosh --eval "db.runCommand({connectionStatus: 1})"

# Verificar firewall
sudo ufw status
```

#### 5. Ambiente virtual não ativa
```bash
# Verificar se está no diretório correto
pwd

# Ativar novamente
source .venv/bin/activate

# Verificar Python
which python
```

### Logs Úteis

#### MongoDB
```bash
# Logs do sistema
sudo journalctl -u mongod

# Logs do MongoDB
sudo tail -f /var/log/mongodb/mongod.log
```

#### Aplicação Python
```bash
# Executar com logs detalhados
python -v scripts/main_local.py

# Ou usar logging interno
export LOG_LEVEL=DEBUG
python scripts/main_local.py
```

## ⚙️ Configurações Avançadas

### 1. MongoDB com Autenticação

#### Habilitar autenticação
```bash
# Editar configuração
sudo nano /etc/mongod.conf

# Adicionar:
security:
  authorization: enabled
```

#### Criar usuário administrador
```bash
# Conectar sem autenticação
mongosh

# Criar usuário admin
use admin
db.createUser({
  user: "admin",
  pwd: "senha_forte",
  roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase"]
})
exit

# Reiniciar MongoDB
sudo systemctl restart mongod

# Conectar com autenticação
mongosh -u admin -p senha_forte --authenticationDatabase admin
```

### 2. Configuração de Rede

#### Permitir conexões externas
```bash
# Editar configuração
sudo nano /etc/mongod.conf

# Alterar bindIp
net:
  port: 27017
  bindIp: 0.0.0.0  # Cuidado: permite qualquer IP

# Reiniciar
sudo systemctl restart mongod
```

#### Configurar firewall
```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 27017

# Firewalld (CentOS/RHEL/Fedora)
sudo firewall-cmd --permanent --add-port=27017/tcp
sudo firewall-cmd --reload
```

## 📈 Otimização de Performance

### 1. Configurações MongoDB
```yaml
# /etc/mongod.conf
storage:
  engine: wiredTiger
  wiredTiger:
    engineConfig:
      cacheSizeGB: 1  # Ajustar conforme RAM disponível

operationProfiling:
  slowOpThresholdMs: 100

setParameter:
  logLevel: 1
```

### 2. Índices (para datasets maiores)
```javascript
// Via mongosh
use dataops_db

// Criar índices úteis
db.carros.createIndex({ "montadora": 1 })
db.montadoras.createIndex({ "montadora": 1 })
db.montadoras.createIndex({ "pais": 1 })
```

## ✅ Checklist de Instalação

- [ ] Sistema Linux atualizado
- [ ] Python 3.8+ instalado
- [ ] Git configurado
- [ ] MongoDB 7.0+ instalado e rodando
- [ ] Repositório clonado
- [ ] Ambiente virtual criado e ativo
- [ ] Dependências Python instaladas
- [ ] Teste de dependências passou
- [ ] Script principal executado com sucesso
- [ ] MongoDB Compass instalado (opcional)
- [ ] Docker configurado (opcional)

## 🎯 Próximos Passos

1. **Explorar dados**: Use MongoDB Compass para visualizar collections
2. **Modificar scripts**: Experimente alterar os dados ou agregações
3. **Testar conexão remota**: Configure um servidor MongoDB remoto
4. **Monitorar performance**: Use ferramentas de monitoramento
5. **Contribuir**: Faça melhorias e abra Pull Requests

---

**Dica**: Mantenha sempre o ambiente virtual ativo ao trabalhar no projeto:
```bash
source .venv/bin/activate
```

Para desativar:
```bash
deactivate
```

**Suporte**: Para problemas específicos do Linux, consulte a documentação da sua distribuição ou abra uma issue no repositório.
