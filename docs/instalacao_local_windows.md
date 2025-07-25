# Instalação Local - Windows

Este guia detalha como instalar e configurar o MongoDB localmente no Windows para executar o desafio DataOps.

## ?? Pré-requisitos

- Windows 10 ou superior
- Python 3.8 ou superior
- Privilégios de administrador (para instalação do MongoDB)

## ?? Passo a Passo

### 1. Instalação do MongoDB Community Server

#### Opção A: Download Manual
1. Acesse: https://www.mongodb.com/try/download/community
2. Selecione:
   - Version: Latest (ex: 7.0.x)
   - Platform: Windows
   - Package: msi
3. Baixe e execute o instalador
4. Durante a instalação:
   - Escolha "Complete" installation
   - Marque "Install MongoDB as a Service"
   - Marque "Install MongoDB Compass" (interface gráfica)

#### Opção B: Usando Chocolatey
```powershell
# Instalar Chocolatey (se não tiver)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar MongoDB
choco install mongodb

# Instalar MongoDB Compass (opcional)
choco install mongodb-compass
```

### 2. Verificação da Instalação

```powershell
# Verificar se o serviço está rodando
Get-Service -Name MongoDB

# Testar conexão
mongo --eval "db.runCommand('ping')"
```

### 3. Configuração do Ambiente Python

```powershell
# Navegar para o diretório do projeto
cd D:\Dev\Case-Engenheiro-dados

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### 4. Execução do Projeto

```powershell
# Verificar se MongoDB está rodando
net start MongoDB

# Executar script principal
python scripts/main_local.py
```

## ?? Configurações

### Localização dos Arquivos MongoDB
- **Executáveis**: `C:\Program Files\MongoDB\Server\7.0\bin\`
- **Dados**: `C:\data\db\`
- **Logs**: `C:\data\log\`
- **Configuração**: `C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg`

### Comandos Úteis

```powershell
# Iniciar serviço MongoDB
net start MongoDB

# Parar serviço MongoDB
net stop MongoDB

# Conectar ao MongoDB shell
mongo

# Conectar ao banco específico
mongo dataops_challenge
```

### Configuração de Firewall (se necessário)

```powershell
# Abrir porta 27017 no firewall
New-NetFirewallRule -DisplayName "MongoDB" -Direction Inbound -Protocol TCP -LocalPort 27017 -Action Allow
```

## ??? Estrutura de Diretórios

Após a execução, você terá:

```
D:\Dev\Case-Engenheiro-dados\
??? .venv\                     # Ambiente virtual Python
??? mongodb\
?   ??? exports\
?       ??? carros.json        # Export da collection carros
?       ??? montadoras.json    # Export da collection montadoras
?       ??? aggregation_result.json # Resultado da agregação
??? scripts\
    ??? ...
```

## ??? Troubleshooting

### Problema: "MongoDB service failed to start"
**Solução:**
```powershell
# Verificar logs
Get-Content "C:\data\log\mongodb.log" -Tail 20

# Recriar diretório de dados
Remove-Item -Recurse -Force C:\data\db\*
mongod --dbpath C:\data\db --logpath C:\data\log\mongodb.log --install
```

### Problema: "Python não reconhecido"
**Solução:**
```powershell
# Verificar instalação do Python
python --version

# Ou usar py launcher
py --version

# Instalar Python se necessário
winget install Python.Python.3.12
```

### Problema: "Access denied"
**Solução:**
- Execute o PowerShell como Administrador
- Ou execute: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Problema: "Port 27017 already in use"
**Solução:**
```powershell
# Verificar processo usando a porta
netstat -ano | findstr :27017

# Terminar processo se necessário
taskkill /PID <PID_NUMBER> /F
```

## ?? Monitoramento

### MongoDB Compass
1. Abra MongoDB Compass
2. Conecte em: `mongodb://localhost:27017`
3. Navegue até database: `dataops_challenge`
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

// Executar agregação manualmente
load('mongodb/aggregation.js')
```

## ? Validação

Após a instalação e execução, você deve ter:

1. ? MongoDB rodando como serviço
2. ? Database `dataops_challenge` criado
3. ? Collections `carros` e `montadoras` populadas
4. ? Agregação executada com sucesso
5. ? Arquivos JSON exportados

## ?? Próximos Passos

Após completar a instalação local, você pode:
1. Explorar os dados no MongoDB Compass
2. Modificar a agregação em `mongodb/aggregation.js`
3. Testar a conexão remota seguindo o guia em `conexao_remota.md`

## ?? Suporte

Em caso de problemas:
1. Verifique os logs em `C:\data\log\mongodb.log`
2. Consulte a documentação oficial: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
3. Verifique se todas as dependências Python foram instaladas corretamente
