---
name: bash-linux
description: Padrões de terminal Bash/Linux. Comandos críticos, piping, tratamento de erros, scripting. Use ao trabalhar em sistemas macOS ou Linux.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Padrões Bash Linux

> Padrões essenciais para Bash em Linux/macOS.

---

## 1. Sintaxe de Operadores

### Encadeamento de Comandos

| Operador | Significado | Exemplo |
|----------|---------|---------|
| `;` | Executar sequencialmente | `cmd1; cmd2` |
| `&&` | Executar se anterior sucedeu | `npm install && npm run dev` |
| `\|\|` | Executar se anterior falhou | `npm test \|\| echo "Tests failed"` |
| `\|` | Pipe de saída | `ls \| grep ".js"` |

---

## 2. Operações com Arquivos

### Comandos Essenciais

| Tarefa | Comando |
|------|---------|
| Listar tudo | `ls -la` |
| Encontrar arquivos | `find . -name "*.js" -type f` |
| Conteúdo do arquivo | `cat file.txt` |
| Primeiras N linhas | `head -n 20 file.txt` |
| Últimas N linhas | `tail -n 20 file.txt` |
| Seguir log | `tail -f log.txt` |
| Buscar em arquivos | `grep -r "pattern" --include="*.js"` |
| Tamanho do arquivo | `du -sh *` |
| Uso de disco | `df -h` |

---

## 3. Gerenciamento de Processos

| Tarefa | Comando |
|------|---------|
| Listar processos | `ps aux` |
| Encontrar por nome | `ps aux \| grep node` |
| Matar por PID | `kill -9 <PID>` |
| Encontrar usuário da porta | `lsof -i :3000` |
| Matar porta | `kill -9 $(lsof -t -i :3000)` |
| Background | `npm run dev &` |
| Jobs | `jobs -l` |
| Trazer para frente | `fg %1` |

---

## 4. Processamento de Texto

### Ferramentas Principais

| Ferramenta | Propósito | Exemplo |
|------|---------|---------|
| `grep` | Buscar | `grep -rn "TODO" src/` |
| `sed` | Substituir | `sed -i 's/old/new/g' file.txt` |
| `awk` | Extrair colunas | `awk '{print $1}' file.txt` |
| `cut` | Cortar campos | `cut -d',' -f1 data.csv` |
| `sort` | Ordenar linhas | `sort -u file.txt` |
| `uniq` | Linhas únicas | `sort file.txt \| uniq -c` |
| `wc` | Contar | `wc -l file.txt` |

---

## 5. Variáveis de Ambiente

| Tarefa | Comando |
|------|---------|
| Ver todas | `env` ou `printenv` |
| Ver uma | `echo $PATH` |
| Definir temporariamente | `export VAR="value"` |
| Definir em script | `VAR="value" command` |
| Adicionar ao PATH | `export PATH="$PATH:/new/path"` |

---

## 6. Rede

| Tarefa | Comando |
|------|---------|
| Download | `curl -O https://example.com/file` |
| Requisição API | `curl -X GET https://api.example.com` |
| POST JSON | `curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' URL` |
| Verificar porta | `nc -zv localhost 3000` |
| Informações de rede | `ifconfig` ou `ip addr` |

---

## 7. Template de Script

```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined var, pipe fail

# Colors (optional)
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Main
main() {
    log_info "Starting..."
    # Your logic here
    log_info "Done!"
}

main "$@"
```

---

## 8. Padrões Comuns

### Verificar se comando existe

```bash
if command -v node &> /dev/null; then
    echo "Node is installed"
fi
```

### Valor padrão de variável

```bash
NAME=${1:-"default_value"}
```

### Ler arquivo linha por linha

```bash
while IFS= read -r line; do
    echo "$line"
done < file.txt
```

### Loop sobre arquivos

```bash
for file in *.js; do
    echo "Processing $file"
done
```

---

## 9. Diferenças do PowerShell

| Tarefa | PowerShell | Bash |
|------|------------|------|
| Listar arquivos | `Get-ChildItem` | `ls -la` |
| Encontrar arquivos | `Get-ChildItem -Recurse` | `find . -type f` |
| Ambiente | `$env:VAR` | `$VAR` |
| Concatenação string | `"$a$b"` | `"$a$b"` (igual) |
| Verificar nulo | `if ($x)` | `if [ -n "$x" ]` |
| Pipeline | Baseado em objeto | Baseado em texto |

---

## 10. Tratamento de Erros

### Definir opções

```bash
set -e          # Exit on error
set -u          # Exit on undefined variable
set -o pipefail # Exit on pipe failure
set -x          # Debug: print commands
```

### Trap para limpeza

```bash
cleanup() {
    echo "Cleaning up..."
    rm -f /tmp/tempfile
}
trap cleanup EXIT
```

---

> **Lembre-se:** Bash é baseado em texto. Use `&&` para cadeias de sucesso, `set -e` para segurança, e sempre coloque aspas em suas variáveis!