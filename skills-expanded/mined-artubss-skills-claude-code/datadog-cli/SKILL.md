---
name: datadog-cli
description: CLI do Datadog para buscar logs, consultar métricas, rastrear requisições e gerenciar dashboards. Use isso ao depurar problemas em produção ou trabalhar com observabilidade do Datadog.
---

# Datadog CLI

Uma ferramenta CLI para agentes de IA depurarem e triarem usando logs e métricas do Datadog.

## Leitura Obrigatória

**Você DEVE ler a documentação de referência relevante antes de usar qualquer comando:**
- [Log Commands](references/logs-commands.md)
- [Metrics](references/metrics.md)
- [Query Syntax](references/query-syntax.md)
- [Workflows](references/workflows.md)
- [Dashboards](references/dashboards.md)

## Configuração

### Variáveis de Ambiente (Obrigatórias)

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-app-key"
```

Obtenha as chaves em: https://app.datadoghq.com/organization-settings/api-keys

### Executando a CLI

```bash
npx @leoflores/datadog-cli <command>
```

Para sites Datadog fora dos EUA, use a flag `--site`:
```bash
npx @leoflores/datadog-cli logs search --query "*" --site datadoghq.eu
```

## Visão Geral dos Comandos

| Comando | Descrição |
|---------|-------------|
| `logs search` | Buscar logs com filtros |
| `logs tail` | Transmitir logs em tempo real |
| `logs trace` | Encontrar logs para um rastreamento distribuído |
| `logs context` | Obter logs antes/depois de um timestamp |
| `logs patterns` | Agrupar mensagens de log semelhantes |
| `logs compare` | Comparar contagens de logs entre períodos |
| `logs multi` | Executar múltiplas consultas em paralelo |
| `logs agg` | Agregar logs por faceta |
| `metrics query` | Consultar métricas de séries temporais |
| `errors` | Resumo rápido de erros por serviço/tipo |
| `services` | Listar serviços com atividade de log |
| `dashboards` | Gerenciar dashboards (CRUD) |
| `dashboard-lists` | Gerenciar listas de dashboards |


## Exemplos Rápidos

### Buscar Erros
```bash
npx @leoflores/datadog-cli logs search --query "status:error" --from 1h --pretty
```

### Transmitir Logs (Tempo Real)
```bash
npx @leoflores/datadog-cli logs tail --query "service:api status:error" --pretty
```

### Resumo de Erros
```bash
npx @leoflores/datadog-cli errors --from 1h --pretty
```

### Correlação de Rastreamento
```bash
npx @leoflores/datadog-cli logs trace --id "abc123def456" --pretty
```

### Consultar Métricas
```bash
npx @leoflores/datadog-cli metrics query --query "avg:system.cpu.user{*}" --from 1h --pretty
```

### Comparar Períodos
```bash
npx @leoflores/datadog-cli logs compare --query "status:error" --period 1h --pretty
```

## Flags Globais

| Flag | Descrição |
|------|-------------|
| `--pretty` | Saída legível para humanos com cores |
| `--output <file>` | Exportar resultados para arquivo JSON |
| `--site <site>` | Site do Datadog (ex: `datadoghq.eu`) |

## Formatos de Tempo

- **Relativo**: `30m`, `1h`, `6h`, `24h`, `7d`
- **ISO 8601**: `2024-01-15T10:30:00Z`

## Fluxo de Triagem de Incidentes

```bash
# 1. Visão geral rápida de erros
npx @leoflores/datadog-cli errors --from 1h --pretty

# 2. Isso é novo? Comparar com período anterior
npx @leoflores/datadog-cli logs compare --query "status:error" --period 1h --pretty

# 3. Encontrar padrões de erro
npx @leoflores/datadog-cli logs patterns --query "status:error" --from 1h --pretty

# 4. Estreitar por serviço
npx @leoflores/datadog-cli logs search --query "status:error service:api" --from 1h --pretty

# 5. Obter contexto em torno de um timestamp
npx @leoflores/datadog-cli logs context --timestamp "2024-01-15T10:30:00Z" --service api --pretty

# 6. Seguir o rastreamento distribuído
npx @leoflores/datadog-cli logs trace --id "TRACE_ID" --pretty
```

Veja [workflows.md](references/workflows.md) para mais fluxos de depuração.