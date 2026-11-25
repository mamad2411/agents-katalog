---
name: Error Resolver
description: Diagnóstico e resolução sistemática de erros usando análise de primeiros princípios. Use quando encontrar qualquer mensagem de erro, stack trace ou comportamento inesperado. Suporta funcionalidade de replay para registrar e reutilizar soluções.
---

# Error Resolver

Uma abordagem de primeiros princípios para diagnosticar e resolver erros em todas as linguagens e frameworks.

## Filosofia Central

**O Processo de Resolução de Erros em 5 Passos:**

```
1. CLASSIFICAR  ->  2. ANALISAR  ->  3. CORRESPONDER  ->  4. INVESTIGAR  ->  5. RESOLVER
     |                  |                |                    |                |
  Que tipo?         Extrair chaves    Padrão             Causa raiz      Corrigir +
                    informações       conhecido?         análise         Prevenir
```

## Início Rápido

Quando encontrar um erro:

1. **Cole o erro completo** (incluindo stack trace, se disponível)
2. **Forneça contexto** (o que você estava tentando fazer?)
3. **Compartilhe código relevante** (arquivo/função envolvida)

## Framework de Classificação de Erros

### Categorias Primárias

| Categoria | Indicadores | Causas Comuns |
|----------|------------|---------------|
| **Sintaxe** | Parse error, Unexpected token | Digitação, parênteses faltantes, sintaxe inválida |
| **Tipo** | TypeError, type mismatch | Tipo de dados errado, acesso a null/undefined |
| **Referência** | ReferenceError, NameError | Variável indefinida, problemas de escopo |
| **Execução** | RuntimeError, Exception | Erros de lógica, operações inválidas |
| **Rede** | ECONNREFUSED, timeout, 4xx/5xx | Problemas de conexão, URL incorreta, servidor indisponível |
| **Permissão** | EACCES, PermissionError | Acesso a arquivo/diretório, sudo necessário |
| **Dependência** | ModuleNotFound, Cannot find module | Pacote faltante, incompatibilidade de versão |
| **Configuração** | Config error, env missing | Configurações incorretas, variáveis de ambiente faltantes |
| **Banco de Dados** | Connection refused, query error | BD indisponível, credenciais incorretas, query inválida |
| **Memória** | OOM, heap out of memory | Vazamento de memória, processamento de dados grande |

### Atributos Secundários

- **Severidade**: Fatal / Erro / Aviso / Informação
- **Escopo**: Tempo de compilação / Execução / Tempo de teste
- **Origem**: Código do usuário / Framework / Third-party / Sistema

## Workflow de Análise

### Passo 1: Classificar

Identifique a categoria do erro examinando:
- Nome/código do erro (ex: `ENOENT`, `TypeError`)
- Palavras-chave da mensagem de erro
- Onde ocorreu (compilação, execução, teste)

### Passo 2: Analisar

Extraia informações-chave:
```
- Código do erro: [código específico, se houver]
- Caminho do arquivo: [onde o erro originou]
- Número da linha: [linha exata, se disponível]
- Função/método: [contexto do erro]
- Variável/valor: [o que estava envolvido]
- Profundidade da stack trace: [quão profunda é a pilha de chamadas]
```

### Passo 3: Corresponder Padrões

Verifique contra padrões de erro conhecidos:
- Veja o diretório `patterns/` para padrões específicos de linguagem
- Corresponda assinaturas de erro a soluções conhecidas
- Verifique o histórico de replay para soluções anteriores

### Passo 4: Análise de Causa Raiz

Aplique a técnica dos **5 Porquês**:
```
Erro: Cannot read property 'name' of undefined
  Por que 1? -> objeto user está undefined
  Por que 2? -> chamada de API retornou null
  Por que 3? -> ID do usuário não existe no banco de dados
  Por que 4? -> ID veio de cache desatualizado
  Por que 5? -> invalidação de cache não foi implementada

Causa Raiz: Lógica de invalidação de cache ausente
```

### Passo 5: Resolver

Gere solução acionável:
1. **Correção imediata** - Fazer funcionar agora
2. **Correção apropriada** - A forma correta de resolver
3. **Prevenção** - Como evitar no futuro

## Formato de Output

Ao resolver um erro, forneça:

```
## Diagnóstico do Erro

**Classificação**: [Categoria] / [Severidade] / [Escopo]

**Assinatura do Erro**:
- Código: [código do erro]
- Tipo: [tipo do erro]
- Localização: [arquivo:linha]

## Causa Raiz

[Explicação de por que esse erro ocorreu]

**Fatores Contribuintes**:
1. [Fator 1]
2. [Fator 2]

## Solução

### Correção Imediata
[Passos rápidos para resolver]

### Mudança de Código
[Código específico a adicionar/modificar]

### Verificação
[Como verificar se a correção funciona]

## Prevenção

[Como prevenir esse erro no futuro]

## Tag de Replay

[Identificador único para essa solução - para referência futura]
```

## Sistema de Replay

O sistema de replay registra soluções bem-sucedidas para referência futura.

### Registrando uma Solução

Após resolver um erro, registre-o:

```bash
# Crie diretório de registro de solução no projeto
mkdir -p .claude/error-solutions

# Formato do arquivo de solução: [error-type]-[hash].yaml
```

### Formato de Registro de Solução

```yaml
# .claude/error-solutions/[error-signature].yaml
id: "nodejs-module-not-found-express"
created: "2024-01-15T10:30:00Z"
updated: "2024-01-20T14:22:00Z"

error:
  type: "dependency"
  category: "ModuleNotFound"
  language: "nodejs"
  pattern: "Cannot find module 'express'"
  context: "npm project, missing dependency"

diagnosis:
  root_cause: "Package not installed or node_modules corrupted"
  factors:
    - "Missing npm install after git clone"
    - "Corrupted node_modules directory"
    - "Package not in package.json"

solution:
  immediate:
    - "Run: npm install express"
  proper:
    - "Check package.json has express listed"
    - "Run: rm -rf node_modules && npm install"
  code_change: null

verification:
  - "Run the application again"
  - "Check express is in node_modules"

prevention:
  - "Add npm install to project setup docs"
  - "Use npm ci in CI/CD pipelines"

metadata:
  occurrences: 5
  last_resolved: "2024-01-20T14:22:00Z"
  success_rate: 1.0
  tags: ["nodejs", "npm", "dependency"]
```

### Busca de Replay

Ao encontrar um erro:
1. Gere assinatura de erro a partir da mensagem de erro
2. Pesquise `.claude/error-solutions/` para padrões correspondentes
3. Se encontrado, aplique a solução registrada
4. Se novo, prossiga com análise completa e registre a solução

### Geração de Assinatura de Erro

```
signature = hash(
  error_type +
  error_code +
  normalized_message +  # remova valores específicos
  language +
  framework
)
```

Exemplos de transformações:
- `Cannot find module 'express'` -> `Cannot find module '{module}'`
- `TypeError: Cannot read property 'name' of undefined` -> `TypeError: Cannot read property '{prop}' of undefined`

## Comandos de Debug

Comandos úteis durante depuração:

### Node.js
```bash
# Output de erro verboso
NODE_DEBUG=* node app.js

# Debug de memória
node --inspect app.js

# Verificar pacotes instalados
npm ls [package-name]

# Verificar package.json
npm ls --depth=0
```

### Python
```bash
# Modo debug
python -m pdb script.py

# Verificar pacotes instalados
pip show [package-name]
pip list
```

### Geral
```bash
# Verificar permissões de arquivo
ls -la [file]

# Verificar uso de porta
lsof -i :[port]
netstat -an | grep [port]

# Verificar variáveis de ambiente
env | grep [VAR_NAME]
printenv [VAR_NAME]

# Verificar espaço em disco
df -h

# Verificar memória
free -m  # Linux
vm_stat  # macOS
```

## Padrões Comuns de Depuração

### Padrão 1: Busca Binária
Quando a localização do erro é incerta:
1. Comente metade do código
2. Se o erro persistir, está na metade restante
3. Repita até encontrar a linha exata

### Padrão 2: Reprodução Mínima
Crie o menor código que reproduz o erro:
1. Comece com arquivo vazio
2. Adicione código peça por peça
3. Interrompa quando o erro aparecer
4. Esse é seu caso de reprodução mínimo

### Padrão 3: Rubber Duck Debugging
Explique o problema em voz alta (ou para Claude):
1. O que deveria acontecer?
2. O que realmente acontece?
3. O que mudou recentemente?
4. Quais pressupostos estou fazendo?

### Padrão 4: Git Bisect
Encontre qual commit introduziu o bug:
```bash
git bisect start
git bisect bad  # commit atual é ruim
git bisect good [last-known-good-commit]
# Git fará checkout de commits para você testar
git bisect good/bad  # marque cada um como bom ou ruim
git bisect reset  # quando concluído
```

## Arquivos de Referência

- **patterns/** - Padrões de erro específicos de linguagem
  - `nodejs.md` - Erros comuns de Node.js
  - `python.md` - Erros comuns de Python
  - `react.md` - Erros de React/Next.js
  - `database.md` - Erros de banco de dados
  - `docker.md` - Erros de Docker/container
  - `git.md` - Erros de Git
  - `network.md` - Erros de rede/API

- **analysis/** - Metodologias de análise
  - `stack-trace.md` - Guia de análise de stack trace
  - `root-cause.md` - Técnicas de análise de causa raiz

- **replay/** - Sistema de replay
  - `solution-template.yaml` - Template para registrar soluções