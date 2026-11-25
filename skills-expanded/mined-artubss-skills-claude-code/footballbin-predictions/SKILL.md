---
name: footballbin-predictions
description: Obtenha previsões de partidas alimentadas por IA para Premier League e Champions League, incluindo placar, próximo gol e escanteios.
homepage: https://apps.apple.com/app/footballbin/id6757111871
metadata: {"clawdbot":{"emoji":"⚽","requires":{"bins":["curl","jq"]},"files":["scripts/*"]}}
---

# Previsões de Partidas FootballBin

Obtenha previsões alimentadas por IA para partidas de Premier League e Champions League via API FootballBin MCP.

## Início Rápido

Execute `scripts/footballbin.sh` com os seguintes comandos:

### Obter previsões da rodada atual
```bash
scripts/footballbin.sh predictions premier_league
scripts/footballbin.sh predictions champions_league
```

### Obter rodada específica
```bash
scripts/footballbin.sh predictions premier_league 27
```

### Filtrar por time
```bash
scripts/footballbin.sh predictions premier_league --home arsenal
scripts/footballbin.sh predictions premier_league --away liverpool
scripts/footballbin.sh predictions premier_league --home chelsea --away wolves
```

### Listar ferramentas disponíveis
```bash
scripts/footballbin.sh tools
```

## Ligas Suportadas

| Entrada | Liga |
|---------|------|
| `premier_league`, `epl`, `pl`, `prem` | Premier League |
| `champions_league`, `ucl`, `cl` | Champions League |

## Aliases de Times Suportados

Aliases comuns funcionam: `united` (Man Utd), `city` (Man City), `spurs` (Tottenham), `wolves` (Wolverhampton), `gunners` (Arsenal), `reds` (Liverpool), `blues` (Chelsea), `villa` (Aston Villa), `forest` (Nottingham Forest), `palace` (Crystal Palace), `barca` (Barcelona), `real` (Real Madrid), `bayern` (Bayern Munich), `psg` (PSG), `juve` (Juventus), `inter` (Inter Milan), `bvb` (Dortmund), `atleti` (Atletico Madrid).

## Dados da Resposta

Cada previsão de partida inclui:
- **Placar do primeiro tempo** (ex: "1:0")
- **Placar final** (ex: "2:1")
- **Próximo marcador** (ex: "Casa,Salah")
- **Contagem de escanteios** (ex: "7:4")
- **Jogadores-chave** com justificativa baseada em forma

## Endpoints Externos

| URL | Dados Enviados | Propósito |
|-----|----------------|-----------|
| `https://ru7m5svay1.execute-api.eu-central-1.amazonaws.com/prod/mcp` | Liga, rodada, filtros de time | Buscar previsões de partidas |

## Segurança e Privacidade

- Nenhuma chave de API necessária (endpoint público, com limite de taxa)
- Nenhum dado de usuário coletado ou armazenado
- Somente leitura: apenas busca dados de previsões
- Nenhum segredo ou variável de ambiente necessário

## Links

- App iOS: https://apps.apple.com/app/footballbin/id6757111871
- App Android: https://play.google.com/store/apps/details?id=com.achan.footballbinandroid