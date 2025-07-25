# Desafio DataOps - MongoDB & Python

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-success)](https://SEU-USUARIO.github.io/Case-Engenheiro-dados/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0%2B-green)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Implementação completa de pipeline de dados usando Python e MongoDB, com suporte para instalação local e conexão remota.**

## 🎯 Objetivo

Desenvolver um sistema de processamento de dados que:
- Cria DataFrames pandas com dados de carros e montadoras
- Conecta ao MongoDB (local ou remoto)
- Executa agregações relacionando collections
- Exporta resultados em formato JSON

## 📖 Documentação Interativa

**[📚 Acesse o Guia Completo](https://SEU-USUARIO.github.io/Case-Engenheiro-dados/)**

O guia interativo contém:
- Instruções passo a passo para Windows, Linux e Docker
- Configuração de conexão remota (servidor 192.168.22.111)
- Troubleshooting detalhado
- Visualização dos resultados

## 🚀 Quick Start

### Local (Windows)
```powershell
# Clonar repositório
git clone https://github.com/SEU-USUARIO/Case-Engenheiro-dados.git
cd Case-Engenheiro-dados

# Ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1

# Instalar dependências  
pip install -r requirements.txt

# Executar
python scripts/main_local.py
```

### Local (Linux)
```bash
# Clonar repositório
git clone https://github.com/SEU-USUARIO/Case-Engenheiro-dados.git
cd Case-Engenheiro-dados

# Ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar
python scripts/main_local.py
```

### Docker
```bash
# Subir ambiente MongoDB
docker-compose -f docker/docker-compose.yml up -d

# Executar aplicação
python scripts/main_local.py
```

### Conexão Remota
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

## 📊 Estrutura dos Dados

### DataFrame Carros
| Carro | Cor | Montadora |
|---------|----------|-------------|
| Onix    | Prata    | Chevrolet   |
| Polo    | Branco   | Volkswagen  |
| Sandero | Prata    | Renault     |
| Fiesta  | Vermelho | Ford        |
| City    | Preto    | Honda       |

### DataFrame Montadoras
| Montadora | País |
|-----------|------|
| Chevrolet | EUA |
| Volkswagen | Alemanha |
| Renault | França |
| Ford | EUA |
| Honda | Japão |

## ⚡ Funcionalidades

- 📊 **DataFrames Pandas**: Estruturas de dados otimizadas
- 🗃️ **MongoDB Local**: Conexão e configuração automática  
- 🌐 **MongoDB Remoto**: Suporte a servidores externos
- 🔄 **Agregação Pipeline**: Relacionamento entre collections
- 📤 **Exportação JSON**: Resultados salvos em arquivos
- 🐳 **Docker Support**: Ambiente containerizado
- 🖥️ **Multi-plataforma**: Windows, Linux, macOS
- 🛡️ **Tratamento de Erros**: Logs detalhados e recovery

## 📁 Estrutura do Projeto

```
📦 docs/                    # Documentação (GitHub Pages)
│   └── index.html          # Guia interativo
📦 scripts/                # Scripts Python
│   ├── main_local.py       # Execução local
│   ├── main_remote.py      # Execução remota  
│   └── data_processing.py  # Funções auxiliares
📦 configs/                # Configurações
│   ├── local_config.py     # MongoDB local
│   └── remote_config.py    # MongoDB remoto
📦 mongodb/                # Scripts MongoDB
│   └── aggregation.js      # Pipeline de agregação
📦 docker/                 # Containers
│   └── docker-compose.yml  # MongoDB + Mongo Express
└── requirements.txt        # Dependências Python
```

## 🛠️ Tecnologias

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.8+ | Linguagem principal |
| MongoDB | 7.0+ | Base de dados |
| Pandas | Latest | Manipulação de dados |
| PyMongo | Latest | Driver MongoDB |
| Docker | Latest | Containerização |
| Colorama | Latest | Logs coloridos |

## 📈 Resultados

A agregação final agrupa os carros por país da montadora:

| País | Quantidade | Carros |
|------|------------|--------|
| Alemanha | 1 | Polo (Volkswagen) |
| EUA | 2 | Onix (Chevrolet), Fiesta (Ford) |
| França | 1 | Sandero (Renault) |
| Japão | 1 | City (Honda) |

## 📊 Monitoramento

- **MongoDB Compass**: Interface visual para MongoDB
- **Mongo Express**: Web UI (Docker) - `http://localhost:8081`
- **Logs**: Feedback detalhado em tempo real
- **Exports**: Arquivos JSON com resultados

## 💻 Desenvolvimento

### Pré-requisitos
- Python 3.8+
- MongoDB 7.0+
- Git

### Instalação de Desenvolvimento
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
# Testar dependências
python test_dependencies.py

# Teste simples
python simple_test.py

# Executar pipeline completo
python scripts/main_local.py
```

## 📚 Documentação Adicional

- [Instalação Local Windows](docs/instalacao_local_windows.md)
- [Instalação Local Linux](docs/instalacao_local_linux.md)
- [Conexão Remota](docs/conexao_remota.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

**Nome do Desenvolvedor**
- GitHub: [@SEU-USUARIO](https://github.com/alex-des-santos)
- LinkedIn: [Seu LinkedIn](https://linkedin.com/in/alex-des-santos)
- Email: eu@alexsantos.pro

---

<div align="center">
  <strong>🚀 Desafio DataOps - MongoDB & Python 🚀</strong><br>
  Desenvolvido com ❤️ para processamento eficiente de dados
</div>
