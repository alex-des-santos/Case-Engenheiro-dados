# Instalação Local - Linux

Este guia detalha como instalar e configurar o MongoDB localmente no Linux para executar o desafio DataOps.

## ?? Pré-requisitos

- Ubuntu 20.04+ / Debian 10+ / CentOS 8+ / RHEL 8+
- Python 3.8 ou superior
- Privilégios sudo
- Conexão com internet

## ?? Instalação

### Ubuntu/Debian

#### 1. Importar chave pública MongoDB
```bash
# Importar chave GPG
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Adicionar repositório MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```

#### 2. Instalar MongoDB
```bash
# Atualizar lista de pacotes
sudo apt-get update

# Instalar MongoDB Community Edition
sudo apt-get install -y mongodb-org

# Fixar versão (evitar updates automáticos)
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-database hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections
```

#### 3. Iniciar e habilitar serviço
```bash
# Iniciar MongoDB
sudo systemctl start mongod

# Habilitar inicialização automática
sudo systemctl enable mongod

# Verificar status
sudo systemctl status mongod
```

### CentOS/RHEL

#### 1. Criar arquivo de repositório
```bash
sudo tee /etc/yum.repos.d/mongodb-org-7.0.repo << 'EOF'
[mongodb-org-7.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/7.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc
EOF
```

#### 2. Instalar MongoDB
```bash
# Instalar MongoDB
sudo yum install -y mongodb-org

# Ou para systems com dnf
sudo dnf install -y mongodb-org
```

#### 3. Configurar SELinux (se habilitado)
```bash
# Verificar se SELinux está ativo
sestatus

# Se ativo, configurar políticas
sudo setsebool -P mongod_exec_t on
```

#### 4. Iniciar serviço
```bash
# Iniciar MongoDB
sudo systemctl start mongod

# Habilitar inicialização automática
sudo systemctl enable mongod

# Verificar status
sudo systemctl status mongod
```

## ?? Configuração do Ambiente

### 1. Configurar Python
```bash
# Instalar Python e pip (se não instalado)
# Ubuntu/Debian
sudo apt-get install -y python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install -y python3 python3-pip
# ou
sudo dnf install -y python3 python3-pip

# Verificar instalação
python3 --version
pip3 --version
```

### 2. Configurar projeto
```bash
# Clonar/navegar para o projeto
cd /path/to/Case-Engenheiro-dados

# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar permissões
```bash
# Garantir que o usuário mongodb possui as permissões corretas
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown -R mongodb:mongodb /var/log/mongodb

# Configurar limites de arquivo (se necessário)
echo "mongodb soft nofile 64000" | sudo tee -a /etc/security/limits.conf
echo "mongodb hard nofile 64000" | sudo tee -a /etc/security/limits.conf
```

## ?? Execução

```bash
# Verificar se MongoDB está rodando
sudo systemctl status mongod

# Se não estiver rodando
sudo systemctl start mongod

# Ativar ambiente virtual
source .venv/bin/activate

# Executar script principal
python scripts/main_local.py
```

## ?? Estrutura de Arquivos Linux

### Localizações importantes:
- **Arquivos de configuração**: `/etc/mongod.conf`
- **Dados**: `/var/lib/mongodb`
- **Logs**: `/var/log/mongodb/mongod.log`
- **Executáveis**: `/usr/bin/mongo*`

### Configuração customizada (se necessário):
```bash
# Editar configuração
sudo nano /etc/mongod.conf

# Reiniciar após mudanças
sudo systemctl restart mongod
```

## ??? Comandos Úteis

### Gerenciamento do Serviço
```bash
# Status do serviço
sudo systemctl status mongod

# Iniciar serviço
sudo systemctl start mongod

# Parar serviço
sudo systemctl stop mongod

# Reiniciar serviço
sudo systemctl restart mongod

# Ver logs em tempo real
sudo tail -f /var/log/mongodb/mongod.log

# Ver logs do systemd
sudo journalctl -u mongod -f
```

### Conexão e Teste
```bash
# Conectar ao MongoDB shell
mongosh
# ou (versões antigas)
mongo

# Testar conexão
mongosh --eval "db.runCommand('ping')"

# Conectar a database específica
mongosh dataops_challenge
```

### Monitoramento
```bash
# Verificar processos MongoDB
ps aux | grep mongod

# Verificar porta em uso
netstat -tlnp | grep :27017
# ou
ss -tlnp | grep :27017

# Verificar uso de recursos
top -p $(pgrep mongod)
```

## ?? Firewall

### Ubuntu/Debian (UFW)
```bash
# Habilitar UFW (se não habilitado)
sudo ufw enable

# Permitir MongoDB
sudo ufw allow 27017/tcp

# Verificar regras
sudo ufw status
```

### CentOS/RHEL (firewalld)
```bash
# Abrir porta MongoDB
sudo firewall-cmd --permanent --add-port=27017/tcp

# Recarregar firewall
sudo firewall-cmd --reload

# Verificar regras
sudo firewall-cmd --list-ports
```

## ?? Alternativa com Docker

Se preferir usar Docker:

```bash
# Instalar Docker (Ubuntu)
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
# Fazer logout/login para aplicar

# Executar MongoDB via Docker
docker run -d \
  --name mongodb-dataops \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:7.0

# Verificar container
docker ps

# Conectar ao MongoDB no container
docker exec -it mongodb-dataops mongosh
```

## ??? Troubleshooting

### Problema: "Failed to start mongod"
```bash
# Verificar logs
sudo journalctl -u mongod -n 50

# Verificar permissões
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown -R mongodb:mongodb /var/log/mongodb

# Verificar configuração
sudo mongod --config /etc/mongod.conf --fork
```

### Problema: "Address already in use"
```bash
# Verificar processo usando porta 27017
sudo lsof -i :27017

# Terminar processo se necessário
sudo kill -9 <PID>

# Ou parar serviço MongoDB
sudo systemctl stop mongod
```

### Problema: "Permission denied"
```bash
# Verificar proprietário dos diretórios
ls -la /var/lib/mongodb
ls -la /var/log/mongodb

# Corrigir permissões
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown -R mongodb:mongodb /var/log/mongodb
sudo chmod 755 /var/lib/mongodb
sudo chmod 755 /var/log/mongodb
```

### Problema: Python não encontrado
```bash
# Ubuntu/Debian
sudo apt-get install -y python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install -y python3 python3-pip
# ou
sudo dnf install -y python3 python3-pip

# Criar link simbólico se necessário
sudo ln -s /usr/bin/python3 /usr/bin/python
```

## ?? Validação da Instalação

```bash
# 1. Verificar serviço MongoDB
sudo systemctl is-active mongod
# Deve retornar: active

# 2. Testar conexão
mongosh --eval "db.runCommand('ping')"
# Deve retornar: { ok: 1 }

# 3. Verificar versão
mongod --version

# 4. Executar script de teste
python scripts/main_local.py
```

## ? Checklist Final

- [ ] MongoDB instalado e rodando
- [ ] Python 3.8+ instalado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências Python instaladas
- [ ] Firewall configurado (se necessário)
- [ ] Script principal executado com sucesso
- [ ] Arquivos JSON exportados

## ?? Próximos Passos

1. Instalar MongoDB Compass para interface gráfica:
   ```bash
   # Ubuntu/Debian
   wget https://downloads.mongodb.com/compass/mongodb-compass_1.40.4_amd64.deb
   sudo dpkg -i mongodb-compass_1.40.4_amd64.deb
   
   # CentOS/RHEL
   wget https://downloads.mongodb.com/compass/mongodb-compass-1.40.4.x86_64.rpm
   sudo rpm -i mongodb-compass-1.40.4.x86_64.rpm
   ```

2. Configurar backup automático
3. Explorar conexão remota

## ?? Suporte

- **Documentação oficial**: https://docs.mongodb.com/manual/administration/install-on-linux/
- **Logs do sistema**: `sudo journalctl -u mongod`
- **Logs do MongoDB**: `/var/log/mongodb/mongod.log`
