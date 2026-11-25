---
name: Writing Hookify Rules
description: Essa habilidade deve ser usada quando o usuário pede para "criar uma regra hookify", "escrever uma regra hook", "configurar hookify", "adicionar uma regra hookify", ou precisa de orientação sobre sintaxe e padrões de regras hookify.
version: 0.1.0
---

# Escrevendo Regras Hookify

## Visão Geral

Regras Hookify são arquivos markdown com YAML frontmatter que definem padrões a serem monitorados e mensagens a exibir quando esses padrões são detectados. Regras são armazenadas em arquivos `.claude/hookify.{nome-da-regra}.local.md`.

## Formato de Arquivo de Regra

### Estrutura Básica

```markdown
---
name: identificador-da-regra
enabled: true
event: bash|file|stop|prompt|all
pattern: padrão-regex-aqui
---

Mensagem a mostrar ao Claude quando essa regra é acionada.
Pode incluir formatação markdown, avisos, sugestões, etc.
```

### Campos do Frontmatter

**name** (obrigatório): Identificador único para a regra
- Use kebab-case: `warn-dangerous-rm`, `block-console-log`
- Seja descritivo e orientado à ação
- Comece com verbo: warn, prevent, block, require, check

**enabled** (obrigatório): Booleano para ativar/desativar
- `true`: Regra ativa
- `false`: Regra desabilitada (não será acionada)
- Pode alternar sem deletar a regra

**event** (obrigatório): Em qual evento hook acionar
- `bash`: Comandos da ferramenta Bash
- `file`: Ferramentas Edit, Write, MultiEdit
- `stop`: Quando o agente quer parar
- `prompt`: Quando o usuário envia um prompt
- `all`: Todos os eventos

**action** (opcional): O que fazer quando a regra corresponde
- `warn`: Mostrar mensagem mas permitir operação (padrão)
- `block`: Prevenir operação (PreToolUse) ou parar sessão (Stop events)
- Se omitido, usa padrão `warn`

**pattern** (formato simples): Padrão regex para corresponder
- Usado para regras simples de uma única condição
- Corresponde contra comando (bash) ou novo_texto (file)
- Sintaxe de regex do Python

**Exemplo:**
```yaml
event: bash
pattern: rm\s+-rf
```

### Formato Avançado (Múltiplas Condições)

Para regras complexas com múltiplas condições:

```markdown
---
name: warn-env-file-edits
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.env$
  - field: new_text
    operator: contains
    pattern: API_KEY
---

Você está adicionando uma chave de API a um arquivo .env. Certifique-se de que esse arquivo está em .gitignore!
```

**Campos de condição:**
- `field`: Qual campo verificar
  - Para bash: `command`
  - Para file: `file_path`, `new_text`, `old_text`, `content`
- `operator`: Como corresponder
  - `regex_match`: Correspondência de padrão regex
  - `contains`: Verificação de substring
  - `equals`: Correspondência exata
  - `not_contains`: Substring NÃO deve estar presente
  - `starts_with`: Verificação de prefixo
  - `ends_with`: Verificação de sufixo
- `pattern`: Padrão ou string para corresponder

**Todas as condições devem corresponder para a regra ser acionada.**

## Corpo da Mensagem

O conteúdo markdown após o frontmatter é mostrado ao Claude quando a regra é acionada.

**Boas mensagens:**
- Explicam o que foi detectado
- Explicam por que é problemático
- Sugerem alternativas ou melhores práticas
- Usam formatação para clareza (negrito, listas, etc.)

**Exemplo:**
```markdown
⚠️ **Console.log detectado!**

Você está adicionando console.log ao código de produção.

**Por que isso importa:**
- Logs de debug não devem ir para produção
- Console.log pode expor dados sensíveis
- Impacta performance do navegador

**Alternativas:**
- Use uma biblioteca de logging apropriada
- Remova antes de fazer commit
- Use builds de debug condicionais
```

## Guia de Tipo de Evento

### Eventos bash

Correspondem a padrões de comando Bash:

```markdown
---
event: bash
pattern: sudo\s+|rm\s+-rf|chmod\s+777
---

Comando perigoso detectado!
```

**Padrões comuns:**
- Comandos perigosos: `rm\s+-rf`, `dd\s+if=`, `mkfs`
- Escalação de privilégios: `sudo\s+`, `su\s+`
- Problemas de permissão: `chmod\s+777`, `chown\s+root`

### Eventos file

Correspondem a operações de Edit/Write/MultiEdit:

```markdown
---
event: file
pattern: console\.log\(|eval\(|innerHTML\s*=
---

Padrão de código potencialmente problemático detectado!
```

**Corresponder em diferentes campos:**
```markdown
---
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.tsx?$
  - field: new_text
    operator: regex_match
    pattern: console\.log\(
---

Console.log em arquivo TypeScript!
```

**Padrões comuns:**
- Código de debug: `console\.log\(`, `debugger`, `print\(`
- Riscos de segurança: `eval\(`, `innerHTML\s*=`, `dangerouslySetInnerHTML`
- Arquivos sensíveis: `\.env$`, `credentials`, `\.pem$`
- Arquivos gerados: `node_modules/`, `dist/`, `build/`

### Eventos stop

Correspondem quando o agente quer parar (verificações de conclusão):

```markdown
---
event: stop
pattern: .*
---

Antes de parar, verifique:
- [ ] Testes foram executados
- [ ] Build foi bem-sucedido
- [ ] Documentação foi atualizada
```

**Use para:**
- Lembretes sobre etapas obrigatórias
- Listas de verificação de conclusão
- Aplicação de processo

### Eventos prompt

Correspondem ao conteúdo do prompt do usuário (avançado):

```markdown
---
event: prompt
conditions:
  - field: user_prompt
    operator: contains
    pattern: deploy to production
---

Checklist de deployment em produção:
- [ ] Testes passando?
- [ ] Revisado pela equipe?
- [ ] Monitoramento pronto?
```

## Dicas para Escrever Padrões

### Noções Básicas de Regex

**Caracteres literais:** A maioria dos caracteres corresponde a si mesmos
- `rm` corresponde a "rm"
- `console.log` corresponde a "console.log"

**Caracteres especiais precisam escapar:**
- `.` (qualquer char) → `\.` (ponto literal)
- `(` `)` → `\(` `\)` (parênteses literais)
- `[` `]` → `\[` `\]` (colchetes literais)

**Metacaracteres comuns:**
- `\s` - espaço em branco (espaço, tabulação, quebra de linha)
- `\d` - dígito (0-9)
- `\w` - caractere de palavra (a-z, A-Z, 0-9, _)
- `.` - qualquer caractere
- `+` - um ou mais
- `*` - zero ou mais
- `?` - zero ou um
- `|` - OU

**Exemplos:**
```
rm\s+-rf         Corresponde a: rm -rf, rm  -rf
console\.log\(   Corresponde a: console.log(
(eval|exec)\(    Corresponde a: eval( ou exec(
chmod\s+777      Corresponde a: chmod 777, chmod  777
API_KEY\s*=      Corresponde a: API_KEY=, API_KEY =
```

### Testando Padrões

Teste padrões regex antes de usar:

```bash
python3 -c "import re; print(re.search(r'seu_padrao', 'texto_teste'))"
```

Ou use testadores regex online (regex101.com com sabor Python).

### Armadilhas Comuns

**Muito abrangente:**
```yaml
pattern: log    # Corresponde a "log", "login", "dialog", "catalog"
```
Melhor: `console\.log\(|logger\.`

**Muito específico:**
```yaml
pattern: rm -rf /tmp  # Corresponde apenas ao caminho exato
```
Melhor: `rm\s+-rf`

**Problemas de escapar:**
- Strings entre aspas YAML: `"pattern"` requer aspas invertidas duplas `\\s`
- Padrão sem aspas: `pattern: \s` funciona como está
- **Recomendação**: Use padrões sem aspas em YAML

## Organização de Arquivo

**Localização:** Todas as regras no diretório `.claude/`
**Nomenclatura:** `.claude/hookify.{nome-descritivo}.local.md`
**Gitignore:** Adicione `.claude/*.local.md` ao `.gitignore`

**Bons nomes:**
- `hookify.dangerous-rm.local.md`
- `hookify.console-log.local.md`
- `hookify.require-tests.local.md`
- `hookify.sensitive-files.local.md`

**Nomes ruins:**
- `hookify.rule1.local.md` (não descritivo)
- `hookify.md` (faltando .local)
- `danger.local.md` (faltando prefixo hookify)

## Fluxo de Trabalho

### Criando uma Regra

1. Identifique o comportamento indesejado
2. Determine qual ferramenta está envolvida (Bash, Edit, etc.)
3. Escolha o tipo de evento (bash, file, stop, etc.)
4. Escreva padrão regex
5. Crie arquivo `.claude/hookify.{nome}.local.md` na raiz do projeto
6. Teste imediatamente - regras são lidas dinamicamente no próximo uso da ferramenta

### Refinando uma Regra

1. Edite o arquivo `.local.md`
2. Ajuste padrão ou mensagem
3. Teste imediatamente - mudanças entram em vigor no próximo uso da ferramenta

### Desabilitando uma Regra

**Temporário:** Configure `enabled: false` no frontmatter
**Permanente:** Delete o arquivo `.local.md`

## Exemplos

Veja `${CLAUDE_PLUGIN_ROOT}/examples/` para exemplos completos:
- `dangerous-rm.local.md` - Bloqueie comandos rm perigosos
- `console-log-warning.local.md` - Avise sobre console.log
- `sensitive-files-warning.local.md` - Avise sobre edição de arquivos .env

## Referência Rápida

**Regra mínima viável:**
```markdown
---
name: minha-regra
enabled: true
event: bash
pattern: comando_perigoso
---

Mensagem de aviso aqui
```

**Regra com condições:**
```markdown
---
name: minha-regra
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.ts$
  - field: new_text
    operator: contains
    pattern: any
---

Mensagem de aviso
```

**Tipos de evento:**
- `bash` - Comandos Bash
- `file` - Edições de arquivo
- `stop` - Verificações de conclusão
- `prompt` - Entrada do usuário
- `all` - Todos os eventos

**Opções de field:**
- Bash: `command`
- File: `file_path`, `new_text`, `old_text`, `content`
- Prompt: `user_prompt`

**Operadores:**
- `regex_match`, `contains`, `equals`, `not_contains`, `starts_with`, `ends_with`