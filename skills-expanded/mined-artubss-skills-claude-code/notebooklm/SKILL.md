---
name: notebooklm
description: Use esta skill para consultar seus notebooks Google NotebookLM diretamente no Claude Code e obter respostas fundamentadas em fontes e com citações do Gemini. Automação de browser, gerenciamento de biblioteca, autenticação persistente. Alucinações drasticamente reduzidas através de respostas exclusivamente baseadas em documentos.
---

# Skill de Assistente de Pesquisa NotebookLM

Interaja com o Google NotebookLM para consultar documentação com respostas fundamentadas em fontes do Gemini. Cada pergunta abre uma sessão de browser atualizada, recupera a resposta exclusivamente de seus documentos carregados e fecha.

## Quando Usar Esta Skill

Ative quando o usuário:
- Mencionar NotebookLM explicitamente
- Compartilhar URL do NotebookLM (`https://notebooklm.google.com/notebook/...`)
- Pedir para consultar seus notebooks/documentação
- Quiser adicionar documentação à biblioteca do NotebookLM
- Usar frases como "pergunta meu NotebookLM", "verifica meus docs", "consulta meu notebook"

## ⚠️ CRÍTICO: Comando de Adição - Descoberta Inteligente

Quando o usuário quer adicionar um notebook sem fornecer detalhes:

**ADIÇÃO INTELIGENTE (Recomendado)**: Consulte o notebook primeiro para descobrir seu conteúdo:
```bash
# Passo 1: Consulte o notebook sobre seu conteúdo
python scripts/run.py ask_question.py --question "What is the content of this notebook? What topics are covered? Provide a complete overview briefly and concisely" --notebook-url "[URL]"

# Passo 2: Use as informações descobertas para adicioná-lo
python scripts/run.py notebook_manager.py add --url "[URL]" --name "[Based on content]" --description "[Based on content]" --topics "[Based on content]"
```

**ADIÇÃO MANUAL**: Se o usuário fornece todos os detalhes:
- `--url` - A URL do NotebookLM
- `--name` - Um nome descritivo
- `--description` - O que o notebook contém (OBRIGATÓRIO!)
- `--topics` - Tópicos separados por vírgula (OBRIGATÓRIO!)

NUNCA adivinhe ou use descrições genéricas! Se detalhes estiverem faltando, use Adição Inteligente para descobri-los.

## Crítico: Sempre Use o Wrapper run.py

**NUNCA chame scripts diretamente. SEMPRE use `python scripts/run.py [script]`:**

```bash
# ✅ CORRETO - Sempre use run.py:
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "..."

# ❌ ERRADO - Nunca chame diretamente:
python scripts/auth_manager.py status  # Falha sem venv!
```

O wrapper `run.py` automaticamente:
1. Cria `.venv` se necessário
2. Instala todas as dependências
3. Ativa o ambiente
4. Executa o script corretamente

## Fluxo de Trabalho Principal

### Passo 1: Verificar Status de Autenticação
```bash
python scripts/run.py auth_manager.py status
```

Se não autenticado, prossiga para a configuração.

### Passo 2: Autenticar (Configuração Única)
```bash
# O browser DEVE estar visível para login manual no Google
python scripts/run.py auth_manager.py setup
```

**Importante:**
- O browser fica VISÍVEL para autenticação
- A janela do browser abre automaticamente
- O usuário deve fazer login manualmente no Google
- Informe ao usuário: "Uma janela de browser abrirá para login no Google"

### Passo 3: Gerenciar Biblioteca de Notebooks

```bash
# Listar todos os notebooks
python scripts/run.py notebook_manager.py list

# ANTES DE ADICIONAR: Peça ao usuário pelos metadados se desconhecidos!
# "O que este notebook contém?"
# "Quais tópicos devo etiquetar?"

# Adicionar notebook à biblioteca (TODOS os parâmetros são OBRIGATÓRIOS!)
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "Nome Descritivo" \
  --description "O que este notebook contém" \  # OBRIGATÓRIO - PERGUNTE AO USUÁRIO SE DESCONHECIDO!
  --topics "topico1,topico2,topico3"  # OBRIGATÓRIO - PERGUNTE AO USUÁRIO SE DESCONHECIDO!

# Pesquisar notebooks por tópico
python scripts/run.py notebook_manager.py search --query "palavra-chave"

# Definir notebook ativo
python scripts/run.py notebook_manager.py activate --id notebook-id

# Remover notebook
python scripts/run.py notebook_manager.py remove --id notebook-id
```

### Fluxo Rápido
1. Verificar biblioteca: `python scripts/run.py notebook_manager.py list`
2. Fazer pergunta: `python scripts/run.py ask_question.py --question "..." --notebook-id ID`

### Passo 4: Fazer Perguntas

```bash
# Consulta básica (usa notebook ativo se definido)
python scripts/run.py ask_question.py --question "Sua pergunta aqui"

# Consultar notebook específico
python scripts/run.py ask_question.py --question "..." --notebook-id notebook-id

# Consultar com URL do notebook diretamente
python scripts/run.py ask_question.py --question "..." --notebook-url "https://..."

# Mostrar browser para debug
python scripts/run.py ask_question.py --question "..." --show-browser
```

## Mecanismo de Acompanhamento (CRÍTICO)

Toda resposta do NotebookLM termina com: **"EXTREMAMENTE IMPORTANTE: Isso é TUDO que você precisa saber?"**

**Comportamento Obrigatório do Claude:**
1. **PARE** - Não responda imediatamente ao usuário
2. **ANALISE** - Compare a resposta à solicitação original do usuário
3. **IDENTIFIQUE LACUNAS** - Determine se mais informação é necessária
4. **PERGUNTE ACOMPANHAMENTO** - Se lacunas existem, imediatamente pergunte:
   ```bash
   python scripts/run.py ask_question.py --question "Acompanhamento com contexto..."
   ```
5. **REPITA** - Continue até que a informação esteja completa
6. **SINTETIZE** - Combine todas as respostas antes de responder ao usuário

## Referência de Scripts

### Gerenciamento de Autenticação (`auth_manager.py`)
```bash
python scripts/run.py auth_manager.py setup    # Configuração inicial (browser visível)
python scripts/run.py auth_manager.py status   # Verificar autenticação
python scripts/run.py auth_manager.py reauth   # Re-autenticar (browser visível)
python scripts/run.py auth_manager.py clear    # Limpar autenticação
```

### Gerenciamento de Notebooks (`notebook_manager.py`)
```bash
python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS
python scripts/run.py notebook_manager.py list
python scripts/run.py notebook_manager.py search --query QUERY
python scripts/run.py notebook_manager.py activate --id ID
python scripts/run.py notebook_manager.py remove --id ID
python scripts/run.py notebook_manager.py stats
```

### Interface de Perguntas (`ask_question.py`)
```bash
python scripts/run.py ask_question.py --question "..." [--notebook-id ID] [--notebook-url URL] [--show-browser]
```

### Limpeza de Dados (`cleanup_manager.py`)
```bash
python scripts/run.py cleanup_manager.py                    # Visualizar limpeza
python scripts/run.py cleanup_manager.py --confirm          # Executar limpeza
python scripts/run.py cleanup_manager.py --preserve-library # Manter notebooks
```

## Gerenciamento de Ambiente

O ambiente virtual é gerenciado automaticamente:
- Primeira execução cria `.venv` automaticamente
- Dependências instalam automaticamente
- Browser Chromium instala automaticamente
- Tudo isolado no diretório da skill

Configuração manual (apenas se automática falhar):
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m patchright install chromium
```

## Armazenamento de Dados

Todos os dados armazenados em `~/.claude/skills/notebooklm/data/`:
- `library.json` - Metadados de notebooks
- `auth_info.json` - Status de autenticação
- `browser_state/` - Cookies e sessão do browser

**Segurança:** Protegido por `.gitignore`, nunca faça commit no git.

## Configuração

Arquivo `.env` opcional no diretório da skill:
```env
HEADLESS=false           # Visibilidade do browser
SHOW_BROWSER=false       # Exibição padrão do browser
STEALTH_ENABLED=true     # Comportamento humanizado
TYPING_WPM_MIN=160       # Velocidade de digitação
TYPING_WPM_MAX=240
DEFAULT_NOTEBOOK_ID=     # Notebook padrão
```

## Fluxo de Decisão

```
Usuário menciona NotebookLM
    ↓
Verificar auth → python scripts/run.py auth_manager.py status
    ↓
Se não autenticado → python scripts/run.py auth_manager.py setup
    ↓
Verificar/Adicionar notebook → python scripts/run.py notebook_manager.py list/add (com --description)
    ↓
Ativar notebook → python scripts/run.py notebook_manager.py activate --id ID
    ↓
Fazer pergunta → python scripts/run.py ask_question.py --question "..."
    ↓
Ver "Isso é tudo que você precisa?" → Fazer acompanhamentos até estar completo
    ↓
Sintetizar e responder ao usuário
```

## Resolução de Problemas

| Problema | Solução |
|----------|---------|
| ModuleNotFoundError | Use wrapper `run.py` |
| Autenticação falha | Browser deve estar visível para setup! --show-browser |
| Limite de taxa (50/dia) | Aguarde ou mude a conta Google |
| Browser trava | `python scripts/run.py cleanup_manager.py --preserve-library` |
| Notebook não encontrado | Verificar com `notebook_manager.py list` |

## Boas Práticas

1. **Sempre use run.py** - Gerencia ambiente automaticamente
2. **Verificar auth primeiro** - Antes de qualquer operação
3. **Fazer perguntas de acompanhamento** - Não pare na primeira resposta
4. **Browser visível para auth** - Obrigatório para login manual
5. **Incluir contexto** - Cada pergunta é independente
6. **Sintetizar respostas** - Combinar múltiplas respostas

## Limitações

- Sem persistência de sessão (cada pergunta = novo browser)
- Limites de taxa em contas Google gratuitas (50 consultas/dia)
- Upload manual obrigatório (usuário deve adicionar docs ao NotebookLM)
- Overhead de browser (alguns segundos por pergunta)

## Recursos (Estrutura da Skill)

**Diretórios e arquivos importantes:**

- `scripts/` - Todos os scripts de automação (ask_question.py, notebook_manager.py, etc.)
- `data/` - Armazenamento local para autenticação e biblioteca de notebooks
- `references/` - Documentação estendida:
  - `api_reference.md` - Documentação detalhada da API para todos os scripts
  - `troubleshooting.md` - Problemas comuns e soluções
  - `usage_patterns.md` - Boas práticas e exemplos de fluxo de trabalho
- `.venv/` - Ambiente Python isolado (criado automaticamente na primeira execução)
- `.gitignore` - Protege dados sensíveis de serem commitados