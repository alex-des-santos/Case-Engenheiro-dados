# Instala��o Local - Windows

Este guia detalha como instalar e configurar o MongoDB localmente no Windows para executar o desafio DataOps.

## ?? Pr�-requisitos

- Windows 10 ou superior
- Python 3.8 ou superior
- Privil�gios de administrador (para instala��o do MongoDB)

## ?? Passo a Passo

### 1. Instala��o do MongoDB Community Server

#### Op��o A: Download Manual
1. Acesse: https://www.mongodb.com/try/download/community
2. Selecione:
   - Version: Latest (ex: 7.0.x)
   - Platform: Windows
   - Package: msi
3. Baixe e execute o instalador
4. Durante a instala��o:
   - Escolha "Complete" installation
   - Marque "Install MongoDB as a Service"
   - Marque "Install MongoDB Compass" (interface gr�fica)

#### Op��o B: Usando Chocolatey
```powershell
# Instalar Chocolatey (se n�o tiver)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar MongoDB
choco install mongodb

# Instalar MongoDB Compass (opcional)
choco install mongodb-compass
```

### 2. Verifica��o da Instala��o

```powershell
# Verificar se o servi�o est� rodando
Get-Service -Name MongoDB

# Testar conex�o
mongo --eval "db.runCommand('ping')"
```

### 3. Configura��o do Ambiente Python

```powershell
# Navegar para o diret�rio do projeto
cd D:\Dev\Case-Engenheiro-dados

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.venv\Scripts\Activate.ps1

# Instalar depend�ncias
pip install -r requirements.txt
```

### 4. Execu��o do Projeto

```powershell
# Verificar se MongoDB est� rodando
net start MongoDB

# Executar script principal
python scripts/main_local.py
```

## ?? Configura��es

### Localiza��o dos Arquivos MongoDB
- **Execut�veis**: `C:\Program Files\MongoDB\Server\7.0\bin\`
- **Dados**: `C:\data\db\`
- **Logs**: `C:\data\log\`
- **Configura��o**: `C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg`

### Comandos �teis

```powershell
# Iniciar servi�o MongoDB
net start MongoDB

# Parar servi�o MongoDB
net stop MongoDB

# Conectar ao MongoDB shell
mongo

# Conectar ao banco espec�fico
mongo dataops_challenge
```

### Configura��o de Firewall (se necess�rio)

```powershell
# Abrir porta 27017 no firewall
New-NetFirewallRule -DisplayName "MongoDB" -Direction Inbound -Protocol TCP -LocalPort 27017 -Action Allow
```

## ??? Estrutura de Diret�rios

Ap�s a execu��o, voc� ter�:

```
D:\Dev\Case-Engenheiro-dados\
??? .venv\                     # Ambiente virtual Python
??? mongodb\
?   ??? exports\
?       ??? carros.json        # Export da collection carros
?       ??? montadoras.json    # Export da collection montadoras
?       ??? aggregation_result.json # Resultado da agrega��o
??? scripts\
    ??? ...
```

## ??? Troubleshooting

### Problema: "MongoDB service failed to start"
**Solu��o:**
```powershell
# Verificar logs
Get-Content "C:\data\log\mongodb.log" -Tail 20

# Recriar diret�rio de dados
Remove-Item -Recurse -Force C:\data\db\*
mongod --dbpath C:\data\db --logpath C:\data\log\mongodb.log --install
```

### Problema: "Python n�o reconhecido"
**Solu��o:**
```powershell
# Verificar instala��o do Python
python --version

# Ou usar py launcher
py --version

# Instalar Python se necess�rio
winget install Python.Python.3.12
```

### Problema: "Access denied"
**Solu��o:**
- Execute o PowerShell como Administrador
- Ou execute: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Problema: "Port 27017 already in use"
**Solu��o:**
```powershell
# Verificar processo usando a porta
netstat -ano | findstr :27017

# Terminar processo se necess�rio
taskkill /PID <PID_NUMBER> /F
```

## ?? Monitoramento

### MongoDB Compass
1. Abra MongoDB Compass
2. Conecte em: `mongodb://localhost:27017`
3. Navegue at� database: `dataops_challenge`
4. Visualize as collections: `carros` e `montadoras`

### Via Linha de Comando
```javascript
// Conectar ao MongoDB shell
mongo

// Usar database
use dataops_challenge

// Listar collections
show collections

// Visualizar dados
db.carros.find().pretty()
db.montadoras.find().pretty()

// Executar agrega��o manualmente
load('mongodb/aggregation.js')
```

## ? Valida��o

Ap�s a instala��o e execu��o, voc� deve ter:

1. ? MongoDB rodando como servi�o
2. ? Database `dataops_challenge` criado
3. ? Collections `carros` e `montadoras` populadas
4. ? Agrega��o executada com sucesso
5. ? Arquivos JSON exportados

## ?? Pr�ximos Passos

Ap�s completar a instala��o local, voc� pode:
1. Explorar os dados no MongoDB Compass
2. Modificar a agrega��o em `mongodb/aggregation.js`
3. Testar a conex�o remota seguindo o guia em `conexao_remota.md`

## ?? Suporte

Em caso de problemas:
1. Verifique os logs em `C:\data\log\mongodb.log`
2. Consulte a documenta��o oficial: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
3. Verifique se todas as depend�ncias Python foram instaladas corretamente
