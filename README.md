# Desafio DataOps - MongoDB & Python

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-success)](https://SEU-USUARIO.github.io/Case-Engenheiro-dados/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0%2B-green)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Implementa��o completa de pipeline de dados usando Python e MongoDB, com suporte para instala��o local e conex�o remota.**

## ?? Objetivo

Desenvolver um sistema de processamento de dados que:
- Cria DataFrames pandas com dados de carros e montadoras
- Conecta ao MongoDB (local ou remoto)
- Executa agrega��es relacionando collections
- Exporta resultados em formato JSON

## ?? Documenta��o Interativa

**[?? Acesse o Guia Completo](https://SEU-USUARIO.github.io/Case-Engenheiro-dados/)**

O guia interativo cont�m:
- Instru��es passo a passo para Windows, Linux e Docker
- Configura��o de conex�o remota (servidor 192.168.22.111)
- Troubleshooting detalhado
- Visualiza��o dos resultados

## ?? Quick Start

### Local (Windows)
```powershell
# Clonar reposit�rio
git clone https://github.com/SEU-USUARIO/Case-Engenheiro-dados.git
cd Case-Engenheiro-dados

# Ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1

# Instalar depend�ncias  
pip install -r requirements.txt

# Executar
python scripts/main_local.py
```

### Local (Linux)
```bash
# Clonar reposit�rio
git clone https://github.com/SEU-USUARIO/Case-Engenheiro-dados.git
cd Case-Engenheiro-dados

# Ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar depend�ncias
pip install -r requirements.txt

# Executar
python scripts/main_local.py
```

### Docker
```bash
# Subir ambiente MongoDB
docker-compose -f docker/docker-compose.yml up -d

# Executar aplica��o
python scripts/main_local.py
```

### Conex�o Remota
```bash
# Configurar .env (copiar de .env.example)
cp .env.example .env

# Editar .env com dados do servidor
# MONGO_HOST=192.168.22.111
# MONGO_PORT=27017
# ...

# Executar
python scripts/main_remote.py
```

## ?? Estrutura dos Dados

### DataFrame Carros
| Carro | Cor | Montadora |
|---------|----------|-------------|
| Onix    | Prata    | Chevrolet   |
| Polo    | Branco   | Volkswagen  |
| Sandero | Prata    | Renault     |
| Fiesta  | Vermelho | Ford        |
| City    | Preto    | Honda       |

### DataFrame Montadoras
| Montadora | Pa�s |
|-----------|------|
| Chevrolet | EUA |
| Volkswagen | Alemanha |
| Renault | Fran�a |
| Ford | EUA |
| Honda | Jap�o |

## ?? Funcionalidades

- ? **DataFrames Pandas**: Estruturas de dados otimizadas
- ? **MongoDB Local**: Conex�o e configura��o autom�tica  
- ? **MongoDB Remoto**: Suporte a servidores externos
- ? **Agrega��o Pipeline**: Relacionamento entre collections
- ? **Exporta��o JSON**: Resultados salvos em arquivos
- ? **Docker Support**: Ambiente containerizado
- ? **Multi-plataforma**: Windows, Linux, macOS
- ? **Tratamento de Erros**: Logs detalhados e recovery

## ?? Estrutura do Projeto

```
??? docs/                    # Documenta��o (GitHub Pages)
?   ??? index.html          # Guia interativo
??? scripts/                # Scripts Python
?   ??? main_local.py       # Execu��o local
?   ??? main_remote.py      # Execu��o remota  
?   ??? data_processing.py  # Fun��es auxiliares
??? configs/                # Configura��es
?   ??? local_config.py     # MongoDB local
?   ??? remote_config.py    # MongoDB remoto
??? mongodb/                # Scripts MongoDB
?   ??? aggregation.js      # Pipeline de agrega��o
??? docker/                 # Containers
?   ??? docker-compose.yml  # MongoDB + Mongo Express
??? requirements.txt        # Depend�ncias Python
```

## ??? Tecnologias

| Tecnologia | Vers�o | Uso |
|------------|--------|-----|
| Python | 3.8+ | Linguagem principal |
| MongoDB | 7.0+ | Base de dados |
| Pandas | Latest | Manipula��o de dados |
| PyMongo | Latest | Driver MongoDB |
| Docker | Latest | Containeriza��o |
| Colorama | Latest | Logs coloridos |

## ?? Resultados

A agrega��o final agrupa os carros por pa�s da montadora:

| Pa�s | Quantidade | Carros |
|------|------------|--------|
| Alemanha | 1 | Polo (Volkswagen) |
| EUA | 2 | Onix (Chevrolet), Fiesta (Ford) |
| Fran�a | 1 | Sandero (Renault) |
| Jap�o | 1 | City (Honda) |

## ?? Monitoramento

- **MongoDB Compass**: Interface visual para MongoDB
- **Mongo Express**: Web UI (Docker) - `http://localhost:8081`
- **Logs**: Feedback detalhado em tempo real
- **Exports**: Arquivos JSON com resultados

## ?? Desenvolvimento

### Pr�-requisitos
- Python 3.8+
- MongoDB 7.0+
- Git

### Instala��o de Desenvolvimento
```bash
git clone https://github.com/SEU-USUARIO/Case-Engenheiro-dados.git
cd Case-Engenheiro-dados
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### Testes
```bash
# Testar depend�ncias
python test_dependencies.py

# Teste simples
python simple_test.py

# Executar pipeline completo
python scripts/main_local.py
```

## ?? Documenta��o Adicional

- [Instala��o Local Windows](docs/instalacao_local_windows.md)
- [Instala��o Local Linux](docs/instalacao_local_linux.md)
- [Conex�o Remota](docs/conexao_remota.md)
- [Troubleshooting](docs/troubleshooting.md)

## ?? Contribui��o

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudan�as (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ?? Licen�a

Este projeto est� sob a licen�a MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## ?? Contato

**Nome do Desenvolvedor**
- GitHub: [@SEU-USUARIO](https://github.com/SEU-USUARIO)
- LinkedIn: [Seu LinkedIn](https://linkedin.com/in/seu-perfil)
- Email: seu.email@example.com

---

<div align="center">
  <strong>?? Desafio DataOps - MongoDB & Python ??</strong><br>
  Desenvolvido com ?? para processamento eficiente de dados
</div>
