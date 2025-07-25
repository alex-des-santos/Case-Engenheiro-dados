# Instalação Local - Windows

Este guia detalha a instalação e configuração do ambiente para executar o desafio DataOps em sistemas Windows (10, 11, Server 2019/2022).

## 🖥️ Pré-requisitos

- Windows 10 (build 1903+) ou Windows 11
- 4GB de RAM disponível
- 10GB de espaço em disco
- Conexão com internet
- Privilégios de administrador

## 🚀 Instalação Rápida

### Script Automatizado (PowerShell)
```powershell
# Executar como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
irm https://raw.githubusercontent.com/SEU-USUARIO/Case-Engenheiro-dados/main/scripts/install_windows.ps1 | iex
```

## 📋 Instalação Manual Detalhada

### 1. Instalar Python 3.8+

#### Opção A: Site Oficial (Recomendado)
1. Acesse [python.org/downloads](https://python.org/downloads)
2. Baixe Python 3.11+ (versão mais recente)
3. Execute o instalador
4. **IMPORTANTE**: Marque "Add Python to PATH"
5. Escolha "Install Now"

#### Opção B: Microsoft Store
1. Abra Microsoft Store
2. Pesquise "Python 3.11"
3. Clique em "Instalar"

#### Opção C: Winget (Windows Package Manager)
```powershell
# Instalar Python via winget
winget install Python.Python.3.11
```

#### Verificar instalação
```powershell
python --version
pip --version
```

### 2. Instalar Git

#### Opção A: Site Oficial
1. Acesse [git-scm.com](https://git-scm.com/download/win)
2. Baixe Git for Windows
3. Execute instalador com configurações padrão

#### Opção B: Winget
```powershell
winget install Git.Git
```

#### Configurar Git
```powershell
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
```

### 3. Instalar MongoDB

#### Opção A: MongoDB Community Server (Recomendado)

1. **Download**:
   - Acesse [mongodb.com/try/download/community](https://mongodb.com/try/download/community)
   - Selecione: Windows x64, MSI
   - Baixe MongoDB Community Server 7.0+

2. **Instalação**:
   - Execute o arquivo .msi baixado
   - Escolha "Complete" installation
   - Marque "Install MongoDB as a Service"
   - Marque "Run service as Network Service user"
   - Mantenha "Install MongoDB Compass" marcado

3. **Verificar instalação**:
```powershell
# Verificar se serviço está rodando
Get-Service -Name MongoDB

# Testar conexão
mongosh
```

#### Opção B: Chocolatey
```powershell
# Instalar Chocolatey primeiro (se não tiver)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar MongoDB
choco install mongodb mongodb-compass -y
```

#### Opção C: Docker Desktop
```powershell
# Instalar Docker Desktop
winget install Docker.DockerDesktop

# Após reiniciar, executar MongoDB
docker run -d --name mongodb -p 27017:27017 mongo:7.0
```

### 4. Configurar MongoDB

#### Verificar se está rodando
```powershell
# Verificar serviço
Get-Service -Name MongoDB

# Se não estiver rodando, iniciar
Start-Service -Name MongoDB

# Definir para inicialização automática
Set-Service -Name MongoDB -StartupType Automatic
```

#### Localização dos arquivos
- **Executáveis**: `C:\Program Files\MongoDB\Server\7.0\bin\`
- **Dados**: `C:\data\db\`
- **Logs**: `C:\data\log\`
- **Configuração**: `C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg`

#### Testar conexão
```powershell
# Via MongoDB Shell
mongosh

# Comandos de teste
> db.runCommand({connectionStatus: 1})
> show dbs
> exit
```

### 5. Clonar Repositório

```powershell
# Navegar para pasta de projetos
cd C:\Projects  # ou local preferido
# Se pasta não existir: mkdir C:\Projects

# Clonar repositório
git clone https://github.com/SEU-USUARIO/Case-Engenheiro-dados.git
cd Case-Engenheiro-dados
```

### 6. Configurar Ambiente Virtual Python

```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.venv\Scripts\Activate.ps1

# Se houver erro de execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verificar se está ativo (prompt deve mostrar (.venv))
python --version
where python
```

### 7. Instalar Dependências Python

```powershell
# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências do projeto
pip install -r requirements.txt

# Verificar instalação
pip list
```

### 8. Configurar Variáveis de Ambiente (Opcional)

```powershell
# Copiar template
copy .env.example .env

# Editar arquivo (usar Notepad++ ou VS Code)
notepad .env
```

Exemplo de conteúdo `.env`:
```bash
# Configuração local Windows
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DATABASE=dataops_db
MONGO_USERNAME=
MONGO_PASSWORD=
```

## 🧪 Teste da Instalação

### 1. Teste de Dependências
```powershell
python test_dependencies.py
```

**Saída esperada:**
```
✅ Python 3.8+ - OK (3.11.5)
✅ Pandas - OK (2.1.0)
✅ PyMongo - OK (4.5.0)  
✅ Colorama - OK (0.4.6)
✅ MongoDB Connection - OK
🎉 Todas as dependências estão funcionando!
```

### 2. Teste Simples
```powershell
python simple_test.py
```

### 3. Execução do Projeto
```powershell
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
✅ Arquivos JSON exportados em: mongodb/exports/
🎉 Desafio concluído com sucesso!
```

## 📊 Ferramentas de Monitoramento

### 1. MongoDB Compass (GUI)

Se não foi instalado automaticamente:
```powershell
# Download manual
# Acesse: https://www.mongodb.com/try/download/compass
# Ou via chocolatey
choco install mongodb-compass -y
```

**Conectar no Compass:**
- Connection String: `mongodb://localhost:27017`
- Explore databases: `dataops_db`
- Collections: `carros`, `montadoras`

### 2. MongoDB Shell (CLI)
```powershell
# Navegar para pasta do MongoDB (se não estiver no PATH)
cd "C:\Program Files\MongoDB\Server\7.0\bin"

# Conectar
mongosh mongodb://localhost:27017

# Comandos úteis
> show dbs
> use dataops_db
> show collections
> db.carros.find().pretty()
> db.montadoras.find().pretty()
> db.stats()
```

### 3. PowerShell MongoDB Commands
```powershell
# Verificar status do serviço
Get-Service -Name MongoDB | Format-Table -AutoSize

# Verificar processo
Get-Process -Name mongod -ErrorAction SilentlyContinue

# Verificar porta 27017
netstat -an | findstr :27017
```

## 🐳 Alternativa com Docker

### 1. Instalar Docker Desktop

#### Via site oficial
1. Baixe [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Execute instalador
3. Reinicie o computador
4. Abra Docker Desktop

#### Via Winget
```powershell
winget install Docker.DockerDesktop
```

### 2. Executar MongoDB via Docker
```powershell
# Baixar e executar MongoDB
docker run -d --name mongodb -p 27017:27017 mongo:7.0

# Verificar container
docker ps

# Executar aplicação
python scripts/main_local.py

# Parar container
docker stop mongodb
```

### 3. Usar Docker Compose
```powershell
# Navegar para pasta docker
cd docker

# Subir ambiente completo
docker-compose up -d

# Verificar serviços
docker-compose ps

# Parar ambiente
docker-compose down
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Python não reconhecido
```
'python' is not recognized as an internal or external command
```

**Soluções:**
```powershell
# Verificar se Python está no PATH
$env:PATH -split ';' | Where-Object { $_ -like '*Python*' }

# Adicionar manualmente ao PATH (temporário)
$env:PATH += ";C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python311"

# Ou usar py launcher
py --version
py -m pip install -r requirements.txt
```

#### 2. MongoDB não inicia
```powershell
# Verificar status
Get-Service -Name MongoDB

# Tentar iniciar
Start-Service -Name MongoDB

# Se falhar, verificar logs
Get-EventLog -LogName Application -Source MongoDB -Newest 10

# Ou executar manualmente
cd "C:\Program Files\MongoDB\Server\7.0\bin"
mongod --config "C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg"
```

#### 3. Erro de Execution Policy
```
execution of scripts is disabled on this system
```

**Solução:**
```powershell
# Alterar policy para usuário atual
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verificar
Get-ExecutionPolicy -List
```

#### 4. Porta 27017 em uso
```powershell
# Verificar qual processo está usando
netstat -ano | findstr :27017

# Parar processo (substitua PID)
taskkill /PID 1234 /F

# Ou mudar porta no MongoDB
# Editar: C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg
```

#### 5. Erro de conexão PyMongo
```python
pymongo.errors.ServerSelectionTimeoutError
```

**Soluções:**
```powershell
# Verificar se MongoDB está rodando
Get-Service -Name MongoDB

# Testar conexão direta
mongosh --eval "db.runCommand({connectionStatus: 1})"

# Verificar firewall (desabilitar temporariamente para teste)
netsh advfirewall set allprofiles state off
```

### Logs Úteis

#### MongoDB
```powershell
# Logs do Windows Event Viewer
Get-EventLog -LogName Application -Source MongoDB -Newest 20

# Arquivo de log (se configurado)
Get-Content "C:\data\log\mongod.log" -Tail 20
```

#### Aplicação Python
```powershell
# Executar com logs detalhados
python -v scripts/main_local.py

# Ou definir nível de log
$env:LOG_LEVEL="DEBUG"
python scripts/main_local.py
```

## ⚙️ Configurações Avançadas

### 1. MongoDB como Serviço Personalizado

#### Arquivo de configuração (mongod.cfg)
```yaml
# C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg
storage:
  dbPath: C:\data\db
  journal:
    enabled: true

systemLog:
  destination: file
  path: C:\data\log\mongod.log
  logAppend: true

net:
  port: 27017
  bindIp: 127.0.0.1

processManagement:
  windowsService:
    serviceName: MongoDB
    displayName: MongoDB
    description: MongoDB Database Service
```

#### Recriar serviço
```powershell
# Parar serviço existente
Stop-Service -Name MongoDB

# Remover serviço
sc.exe delete MongoDB

# Recriar serviço com configuração personalizada
mongod --config "C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg" --install

# Iniciar
Start-Service -Name MongoDB
```

### 2. Variáveis de Ambiente Permanentes

```powershell
# Adicionar MongoDB ao PATH permanentemente
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\MongoDB\Server\7.0\bin", [EnvironmentVariableTarget]::User)

# Definir variáveis do projeto
[Environment]::SetEnvironmentVariable("MONGO_HOST", "localhost", [EnvironmentVariableTarget]::User)
[Environment]::SetEnvironmentVariable("MONGO_PORT", "27017", [EnvironmentVariableTarget]::User)
```

### 3. Agendamento de Tarefas

```powershell
# Criar tarefa para executar script automaticamente
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\Projects\Case-Engenheiro-dados\scripts\main_local.py" -WorkingDirectory "C:\Projects\Case-Engenheiro-dados"
$trigger = New-ScheduledTaskTrigger -Daily -At "09:00"
Register-ScheduledTask -TaskName "DataOps-MongoDB" -Action $action -Trigger $trigger -Description "Executar desafio DataOps"
```

## 📈 Otimização de Performance

### 1. Configurações do Windows

```powershell
# Desabilitar Windows Defender para pasta do projeto (temporário, para desenvolvimento)
Add-MpPreference -ExclusionPath "C:\Projects\Case-Engenheiro-dados"

# Aumentar prioridade do processo Python
Get-Process -Name python | ForEach-Object { $_.PriorityClass = "High" }
```

### 2. Configurações MongoDB
```yaml
# mongod.cfg otimizado para desenvolvimento
storage:
  engine: wiredTiger
  wiredTiger:
    engineConfig:
      cacheSizeGB: 2  # Ajustar conforme RAM disponível

operationProfiling:
  slowOpThresholdMs: 100

setParameter:
  logLevel: 1
```

### 3. Configurações Python
```powershell
# Usar cache de bytecode
$env:PYTHONDONTWRITEBYTECODE=0

# Otimizações pandas
$env:PANDAS_COMPUTE_ENGINE="numba"
```

## ✅ Checklist de Instalação

- [ ] Windows 10/11 atualizado
- [ ] Python 3.8+ instalado e no PATH
- [ ] Git configurado
- [ ] MongoDB Community Server instalado
- [ ] Serviço MongoDB rodando
- [ ] Repositório clonado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências Python instaladas
- [ ] Teste de dependências passou
- [ ] Script principal executado com sucesso
- [ ] MongoDB Compass instalado e funcionando
- [ ] Docker Desktop configurado (opcional)

## 🎯 Próximos Passos

1. **Explorar MongoDB Compass**: Visualize as collections criadas
2. **Modificar dados**: Experimente alterar dados em `scripts/data_processing.py`
3. **Testar diferentes agregações**: Modifique `mongodb/aggregation.js`
4. **Configurar ambiente remoto**: Siga o guia de conexão remota
5. **Automatizar execução**: Configure tarefas agendadas

---

**Dicas importantes para Windows:**

- **Sempre ative o ambiente virtual** antes de trabalhar:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

- **Para desativar o ambiente virtual**:
  ```powershell
  deactivate
  ```

- **Use PowerShell como Administrador** para instalações

- **Mantenha Windows Defender configurado** adequadamente

**Suporte**: Para problemas específicos do Windows, consulte a documentação oficial ou abra uma issue no repositório.
