---
name: setup-research-stack
description: Instala e verifica o stack de pesquisa completo, medindo o tempo de cada etapa. Use quando o usuário instalar este plugin pela primeira vez, pedir para configurar o ambiente de pesquisa, disser "roda o setup", "instala o stack", "configura a pesquisa", ou quando uma skill do ciclo falhar por ferramenta ausente.
---

# Setup do research-stack

Instale as ferramentas, registre o tempo real de cada etapa e relate o que ficou faltando. Não silencie falha: ferramenta ausente vira aviso explícito.

## Etapa 0: descobrir onde o Bash roda

Antes de qualquer instalação, verifique se o Bash disponível é a máquina do usuário ou um ambiente isolado.

Rode `ls /` e confirme se o sistema de arquivos do usuário está acessível. No Claude Code em terminal local, está. No Cowork e em ambientes com sandbox, o Bash é outro computador e instalar ali não serve para nada, porque os servidores MCP rodam na máquina do usuário.

Se o ambiente for isolado, **não rode o script**. Entregue os comandos para o usuário rodar no terminal dele e siga para a Etapa 2 no mesmo formato. Diga isso explicitamente em vez de instalar no lugar errado e reportar sucesso.

## Etapa 1: rodar o script

Execute `${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh` com Bash. Ele instala os conversores e os clientes MCP em Python, cronometra cada instalação e grava o resultado em `./research-stack-timings.txt`.

Peça confirmação ao usuário antes de rodar, porque o script instala pacotes na máquina dele. Ofereça a flag `--dry-run` para ele ver a lista antes.

## Etapa 2: skills de terceiros

Este plugin não redistribui skill de outro autor. Instale da fonte original, preservando crédito e mantendo tudo atualizado.

**Caminho padrão, sem custo e sem chave de API.** Rode um por vez e reporte quais funcionaram:

```
npx skills add mattpocock/skills --skill research --agent claude-code
npx skills add tw93/waza --skill learn --agent claude-code
npx skills add 199-biotechnologies/claude-deep-research-skill --skill deep-research --agent claude-code
npx skills add lllllllama/RigorPilot-Skills --skill ai-research-explore --agent claude-code
npx skills add coreyhaines31/marketingskills --skill competitor-profiling --agent claude-code
```

Essas cinco usam as ferramentas nativas do agente e as bases públicas do `paper-search`, então funcionam sem credencial paga.

**Opcional, só para quem já paga Firecrawl.** Pergunte antes de instalar, e pule sem insistir se o usuário não tiver chave:

```
npx skills add firecrawl/firecrawl-workflows --skill firecrawl-deep-research --agent claude-code
npx skills add firecrawl/firecrawl-workflows --skill firecrawl-research-papers --agent claude-code
```

Nunca instale as duas do Firecrawl no caminho padrão. Skill que instala e falha por falta de credencial gera a impressão de que o stack está quebrado.

## Etapa 3: configuração que exige o usuário

Estas não dá para automatizar. Liste e ofereça ajuda em cada uma:

1. **Zotero**: abrir o Zotero, ativar "Allow other applications on this computer to communicate with Zotero" nas preferências, e rodar `zotero-mcp setup`
2. **Obsidian**: informar o caminho do vault, que será usado como destino das notas
3. **Gemini Notebook**: opcional, e só se o usuário quiser a etapa de segunda leitura
4. **Firecrawl**: apenas se o usuário já tiver chave de API, exportada em variável de ambiente

## Etapa 4: verificação

Confirme cada peça e monte uma tabela de status com o que respondeu e o que faltou:

```
markitdown --help
paper-search-mcp --help
zotero-mcp version
```

Para os MCPs, confirme que `paper-search` e `zotero` aparecem na lista de servidores conectados. Se não aparecerem, o usuário precisa reiniciar o cliente depois da instalação.

## Etapa 5: fechar com os números

Mostre a tabela de tempo gerada pelo script e convide o usuário a comparar com o tempo de referência do README. Se o tempo dele divergir muito, peça para ele abrir uma issue com a máquina e o sistema operacional, porque esses números alimentam a tabela pública do projeto.
