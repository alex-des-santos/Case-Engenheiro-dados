# Contribuindo para o Desafio DataOps

Obrigado pelo interesse em contribuir com este projeto! Este documento fornece diretrizes para contribuições.

## Como Contribuir

### 1. Fork do Projeto
```bash
# Faça um fork no GitHub e clone localmente
git clone https://github.com/SEU-USUARIO/Case-Engenheiro-dados.git
cd Case-Engenheiro-dados
```

### 2. Configurar Ambiente de Desenvolvimento
```bash
# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\Activate.ps1  # Windows

# Instalar dependências
pip install -r requirements.txt

# Instalar ferramentas de desenvolvimento
pip install black flake8 isort pytest
```

### 3. Criar Branch para Feature
```bash
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b fix/correcao-bug
```

### 4. Fazer Alterações

#### Padrões de Código
- **Python**: Seguir PEP 8
- **Formatação**: Usar `black` para formatação automática
- **Imports**: Organizar com `isort`
- **Lint**: Passar no `flake8`

#### Executar Ferramentas de Qualidade
```bash
# Formatação automática
black scripts/ configs/

# Organizar imports
isort scripts/ configs/

# Verificar lint
flake8 scripts/ configs/
```

### 5. Testes

#### Executar Testes Existentes
```bash
# Teste de dependências
python test_dependencies.py

# Teste básico
python simple_test.py

# Teste completo (precisa do MongoDB rodando)
python scripts/main_local.py
```

#### Adicionar Novos Testes
- Testes unitários para novas funções
- Testes de integração quando aplicável
- Documentar casos de teste específicos

### 6. Documentação

#### Atualizar Documentação
- Atualizar README.md se necessário
- Documentar novas funcionalidades
- Atualizar guia interativo (`docs/index.html`) se aplicável

#### Padrões de Documentação
- Docstrings em Python seguindo formato Google
- Comentários claros no código
- Exemplos de uso quando aplicável

### 7. Commit e Push

#### Padrões de Commit
```bash
# Formato: tipo(escopo): descrição
git commit -m "feat(scripts): adicionar validação de dados"
git commit -m "fix(mongodb): corrigir conexão remota SSL"
git commit -m "docs(readme): atualizar instruções de instalação"
```

#### Tipos de Commit
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (sem mudança de código)
- `refactor`: Refatoração de código
- `test`: Adicionar ou corrigir testes
- `chore`: Tarefas de manutenção

### 8. Pull Request

#### Antes de Abrir PR
- [ ] Código formatado com `black`
- [ ] Imports organizados com `isort`
- [ ] Passou no `flake8`
- [ ] Testes estão passando
- [ ] Documentação atualizada
- [ ] Branch atualizada com `main`

#### Template de PR
```markdown
## Descrição
Breve descrição das mudanças realizadas.

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Breaking change
- [ ] Atualização de documentação

## Como Testar
1. Passos para testar as mudanças
2. Comandos específicos
3. Cenários de teste

## Checklist
- [ ] Código segue padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Mudanças foram testadas localmente
```

## Estrutura do Projeto

### Diretórios Principais
```
📦 scripts/          # Scripts Python principais
📦 configs/          # Arquivos de configuração
📦 docs/            # Documentação e GitHub Pages
📦 mongodb/         # Scripts e exports MongoDB
📦 docker/          # Configurações Docker
📦 .github/         # Templates e workflows
```

### Arquivos Importantes
- `requirements.txt`: Dependências Python
- `test_dependencies.py`: Teste de dependências
- `simple_test.py`: Testes básicos
- `.env.example`: Template de configuração

## Diretrizes Específicas

### Adicionando Nova Funcionalidade
1. Criar função em módulo apropriado
2. Adicionar testes unitários
3. Documentar função com docstring
4. Atualizar documentação relevante
5. Considerar impacto em configurações

### Corrigindo Bugs
1. Reproduzir bug localmente
2. Escrever teste que falha (se aplicável)
3. Implementar correção
4. Verificar que teste agora passa
5. Testar cenários relacionados

### Melhorando Documentação
1. Verificar clareza e precisão
2. Adicionar exemplos práticos
3. Atualizar guia interativo se necessário
4. Considerar diferentes níveis de usuário

## Suporte

### Dúvidas sobre Contribuição
- Abra uma issue com label "question"
- Descreva claramente sua dúvida
- Inclua contexto relevante

### Reportar Bugs
- Use template de issue para bugs
- Inclua steps para reproduzir
- Especifique ambiente (OS, Python version, etc.)
- Adicione logs de erro se disponível

### Sugerir Melhorias
- Use template de issue para features
- Descreva o problema que resolve
- Proponha solução detalhada
- Considere impacto em usuários existentes

## Reconhecimento

Contribuições são sempre bem-vindas! Contribuidores serão reconhecidos no README.md do projeto.

---

Obrigado por contribuir para tornar este projeto melhor! 🚀
