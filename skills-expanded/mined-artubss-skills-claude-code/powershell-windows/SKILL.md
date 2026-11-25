---
name: powershell-windows
description: Padrões PowerShell Windows. Armadilhas críticas, sintaxe de operadores, tratamento de erros.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Padrões PowerShell Windows

> Padrões críticos e armadilhas para PowerShell Windows.

---

## 1. Regras de Sintaxe de Operadores

### CRÍTICO: Parênteses Obrigatórios

| ❌ Errado | ✅ Correto |
|----------|-----------|
| `if (Test-Path "a" -or Test-Path "b")` | `if ((Test-Path "a") -or (Test-Path "b"))` |
| `if (Get-Item $x -and $y -eq 5)` | `if ((Get-Item $x) -and ($y -eq 5))` |

**Regra:** Cada chamada de cmdlet DEVE estar entre parênteses ao usar operadores lógicos.

---

## 2. Restrição de Unicode/Emoji

### CRÍTICO: Sem Unicode em Scripts

| Propósito | ❌ Não use | ✅ Use |
|-----------|-----------|--------|
| Sucesso | ✅ ✓ | [OK] [+] |
| Erro | ❌ ✗ 🔴 | [!] [X] |
| Aviso | ⚠️ 🟡 | [*] [WARN] |
| Informação | ℹ️ 🔵 | [i] [INFO] |
| Progresso | ⏳ | [...] |

**Regra:** Use apenas caracteres ASCII em scripts PowerShell.

---

## 3. Padrões de Verificação de Nulo

### Sempre Verificar Antes de Acessar

| ❌ Errado | ✅ Correto |
|----------|-----------|
| `$array.Count -gt 0` | `$array -and $array.Count -gt 0` |
| `$text.Length` | `if ($text) { $text.Length }` |

---

## 4. Interpolação de Strings

### Expressões Complexas

| ❌ Errado | ✅ Correto |
|----------|-----------|
| `"Value: $($obj.prop.sub)"` | Armazene em variável primeiro |

**Padrão:**
```
$value = $obj.prop.sub
Write-Output "Value: $value"
```

---

## 5. Tratamento de Erros

### ErrorActionPreference

| Valor | Use |
|-------|-----|
| Stop | Desenvolvimento (falhar rapidamente) |
| Continue | Scripts de produção |
| SilentlyContinue | Quando erros são esperados |

### Padrão Try/Catch

- Não retorne dentro do bloco try
- Use finally para limpeza
- Retorne após try/catch

---

## 6. Caminhos de Arquivo

### Regras de Caminho Windows

| Padrão | Use |
|--------|-----|
| Caminho literal | `C:\Users\User\file.txt` |
| Caminho variável | `Join-Path $env:USERPROFILE "file.txt"` |
| Relativo | `Join-Path $ScriptDir "data"` |

**Regra:** Use Join-Path para segurança multiplataforma.

---

## 7. Operações com Arrays

### Padrões Corretos

| Operação | Sintaxe |
|----------|---------|
| Array vazio | `$array = @()` |
| Adicionar item | `$array += $item` |
| ArrayList adicionar | `$list.Add($item) | Out-Null` |

---

## 8. Operações com JSON

### CRÍTICO: Parâmetro Depth

| ❌ Errado | ✅ Correto |
|----------|-----------|
| `ConvertTo-Json` | `ConvertTo-Json -Depth 10` |

**Regra:** Sempre especifique `-Depth` para objetos aninhados.

### Operações com Arquivo

| Operação | Padrão |
|----------|--------|
| Ler | `Get-Content "file.json" -Raw | ConvertFrom-Json` |
| Escrever | `$data | ConvertTo-Json -Depth 10 | Out-File "file.json" -Encoding UTF8` |

---

## 9. Erros Comuns

| Mensagem de Erro | Causa | Solução |
|------------------|-------|--------|
| "parameter 'or'" | Parênteses ausentes | Envolver cmdlets em () |
| "Unexpected token" | Caractere Unicode | Usar apenas ASCII |
| "Cannot find property" | Objeto nulo | Verificar nulo primeiro |
| "Cannot convert" | Incompatibilidade de tipo | Usar .ToString() |

---

## 10. Modelo de Script

```powershell
# Modo strict
Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

# Caminhos
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Principal
try {
    # Lógica aqui
    Write-Output "[OK] Concluído"
    exit 0
}
catch {
    Write-Warning "Erro: $_"
    exit 1
}
```

---

> **Lembre-se:** PowerShell tem regras de sintaxe únicas. Parênteses, apenas ASCII e verificações de nulo são inegociáveis.