# Contribuindo para o Desafio DataOps

Obrigado pelo interesse em contribuir com este projeto! Este documento fornece diretrizes para contribui��es.

## Como Contribuir

### 1. Fork do Projeto
```bash
# Fa�a um fork no GitHub e clone localmente
git clone https://github.com/SEU-USUARIO/Case-Engenheiro-dados.git
cd Case-Engenheiro-dados
```

### 2. Configurar Ambiente de Desenvolvimento
```bash
# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\Activate.ps1  # Windows

# Instalar depend�ncias
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

### 4. Fazer Altera��es

#### Padr�es de C�digo
- **Python**: Seguir PEP 8
- **Formata��o**: Usar `black` para formata��o autom�tica
- **Imports**: Organizar com `isort`
- **Lint**: Passar no `flake8`

#### Executar Ferramentas de Qualidade
```bash
# Formata��o autom�tica
black scripts/ configs/

# Organizar imports
isort scripts/ configs/

# Verificar lint
flake8 scripts/ configs/
```

### 5. Testes

#### Executar Testes Existentes
```bash
# Teste de depend�ncias
python test_dependencies.py

# Teste b�sico
python simple_test.py

# Teste completo (precisa do MongoDB rodando)
python scripts/main_local.py
```

#### Adicionar Novos Testes
- Testes unit�rios para novas fun��es
- Testes de integra��o quando aplic�vel
- Documentar casos de teste espec�ficos

### 6. Documenta��o

#### Atualizar Documenta��o
- Atualizar README.md se necess�rio
- Documentar novas funcionalidades
- Atualizar guia interativo (`docs/index.html`) se aplic�vel

#### Padr�es de Documenta��o
- Docstrings em Python seguindo formato Google
- Coment�rios claros no c�digo
- Exemplos de uso quando aplic�vel

### 7. Commit e Push

#### Padr�es de Commit
```bash
# Formato: tipo(escopo): descri��o
git commit -m "feat(scripts): adicionar valida��o de dados"
git commit -m "fix(mongodb): corrigir conex�o remota SSL"
git commit -m "docs(readme): atualizar instru��es de instala��o"
```

#### Tipos de Commit
- `feat`: Nova funcionalidade
- `fix`: Corre��o de bug
- `docs`: Documenta��o
- `style`: Formata��o (sem mudan�a de c�digo)
- `refactor`: Refatora��o de c�digo
- `test`: Adicionar ou corrigir testes
- `chore`: Tarefas de manuten��o

### 8. Pull Request

#### Antes de Abrir PR
- [ ] C�digo formatado com `black`
- [ ] Imports organizados com `isort`
- [ ] Passou no `flake8`
- [ ] Testes est�o passando
- [ ] Documenta��o atualizada
- [ ] Branch atualizada com `main`

#### Template de PR
```markdown
## Descri��o
Breve descri��o das mudan�as realizadas.

## Tipo de Mudan�a
- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Breaking change
- [ ] Atualiza��o de documenta��o

## Como Testar
1. Passos para testar as mudan�as
2. Comandos espec�ficos
3. Cen�rios de teste

## Checklist
- [ ] C�digo segue padr�es do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documenta��o foi atualizada
- [ ] Mudan�as foram testadas localmente
```

## Estrutura do Projeto

### Diret�rios Principais
```
??? scripts/          # Scripts Python principais
??? configs/          # Arquivos de configura��o
??? docs/            # Documenta��o e GitHub Pages
??? mongodb/         # Scripts e exports MongoDB
??? docker/          # Configura��es Docker
??? .github/         # Templates e workflows
```

### Arquivos Importantes
- `requirements.txt`: Depend�ncias Python
- `test_dependencies.py`: Teste de depend�ncias
- `simple_test.py`: Testes b�sicos
- `.env.example`: Template de configura��o

## Diretrizes Espec�ficas

### Adicionando Nova Funcionalidade
1. Criar fun��o em m�dulo apropriado
2. Adicionar testes unit�rios
3. Documentar fun��o com docstring
4. Atualizar documenta��o relevante
5. Considerar impacto em configura��es

### Corrigindo Bugs
1. Reproduzir bug localmente
2. Escrever teste que falha (se aplic�vel)
3. Implementar corre��o
4. Verificar que teste agora passa
5. Testar cen�rios relacionados

### Melhorando Documenta��o
1. Verificar clareza e precis�o
2. Adicionar exemplos pr�ticos
3. Atualizar guia interativo se necess�rio
4. Considerar diferentes n�veis de usu�rio

## Suporte

### D�vidas sobre Contribui��o
- Abra uma issue com label "question"
- Descreva claramente sua d�vida
- Inclua contexto relevante

### Reportar Bugs
- Use template de issue para bugs
- Inclua steps para reproduzir
- Especifique ambiente (OS, Python version, etc.)
- Adicione logs de erro se dispon�vel

### Sugerir Melhorias
- Use template de issue para features
- Descreva o problema que resolve
- Proponha solu��o detalhada
- Considere impacto em usu�rios existentes

## Reconhecimento

Contribui��es s�o sempre bem-vindas! Contribuidores ser�o reconhecidos no README.md do projeto.

---

Obrigado por contribuir para tornar este projeto melhor! ??
