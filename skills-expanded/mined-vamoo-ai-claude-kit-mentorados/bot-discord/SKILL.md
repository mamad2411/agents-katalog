---
name: bot-discord
description: >-
  Use para criar, diagnosticar (caiu, não responde) ou colocar no ar um bot de
  Discord em Node/TypeScript numa VPS própria. Cobre do Developer Portal ao
  container rodando: intents, convite, código, idempotência, cron, Docker e a
  verificação de que subiu de verdade. Só dispara quando você chama:
  /kit-vamoo:bot-discord.
disable-model-invocation: true
---

# bot-discord — do Developer Portal ao container rodando

O que derruba bot de Discord raramente é o código: é configuração invisível (uma chavinha
do portal, um scope do convite) e operação (a mensagem reprocessada, o container que morre
calado). Onde diz **ARMADILHA**, um bot em produção já caiu por causa disso.

Aqui fica o que é do bot. Da VPS em si, a `references/03-deploy-vps.md` traz só o que o
bot precisa (firewall com Docker, reboot em Swarm, conferir o backup); ser avisado quando
ele cair é o `/kit-vamoo:monitoramento-infra`.

## Como usar esta skill

Bot novo: trabalhe em fases, na ordem. Bot que já existe e caiu ou não responde: comece
pela Fase 9 e pela tabela *Quando falhar*, e pergunte só o que o diagnóstico pedir (host,
nome do container, o sintoma exato).

Antes de escrever código, leia a reference da fase:

| Fase | O quê | Leia antes |
|---|---|---|
| 0 | Perguntar, só em bot novo (abaixo) | — |
| 1 | Developer Portal: app, token, intents, convite, IDs | `references/01-portal-discord.md` |
| 2–6 | Projeto, banco, handlers, idempotência, cron | `references/02-codigo-base.md` |
| 7–8 | Dockerfile, VPS, deploy | `references/03-deploy-vps.md` |
| 9 | Verificação — **está inline aqui embaixo, é o gate** | — |

Os valores entre `<COLCHETES ANGULARES>` nas references são **placeholders**: pergunte ao
usuário e substitua pelo valor real antes de rodar qualquer comando. Nunca execute um comando
com `<IP_DA_VPS>` literal dentro.

## Fase 0 — Bot novo: pergunte antes de escrever a primeira linha

Bloco único, e espere as respostas:

1. **Nome do bot** e o fluxo real que ele resolve (um parágrafo, não lista de features).
2. **Servidor (guild)**: já existe? Qual o ID?
3. **Quais canais** ele escuta e em qual ele responde/publica?
4. **Precisa de banco?** (Supabase/Postgres — já existe projeto?)
5. **VPS**: host/IP, usuário SSH, distro, já tem Docker? Roda mais alguma coisa lá (Traefik, n8n, Portainer)?
6. **HTTP exposto?** A maioria dos bots é só saída (gateway) — **não precisa de porta aberta nem domínio**. Confirme.
7. **Quem pode dar comando** — todo mundo do servidor ou allowlist?

O que você decide sozinho, sem perguntar: Node 22 + TypeScript rodando por `tsx` (sem build step),
`discord.js` v14, `node-cron`, deploy com `docker compose`. Swarm só se ele **já** usa Swarm.

## As armadilhas que mais custam

1. **MESSAGE CONTENT INTENT desligado no portal** → o bot fica online, sem nenhum erro, e
   `message.content` chega **string vazia**. Declarar a intent no código não basta; tem que
   ligar o toggle na tela **Bot** do portal. É a causa nº 1 de "conecta mas não responde".
2. **`import` estático antes do `dotenv.config()`** → imports ES são *hoisted* e rodam antes
   do dotenv: os clients nascem com env `undefined`. O entrypoint carrega o env e só então faz
   `await import()` do app.
3. **Lista seletiva de `COPY` no Dockerfile** → a lista defasa em silêncio, a imagem **builda
   verde** e o container morre em loop com `ERR_MODULE_NOT_FOUND`, com o bot fora do ar.
   Copie `src/` inteiro; alguns MB a mais são grátis.
4. **Convite sem o scope `applications.commands`** → slash command nunca registra.
5. **Slash sem `deferReply()`** → interaction expira em 3 s e o usuário vê "a aplicação não respondeu".
6. **Cron sem `timezone`** → o container roda em UTC e o relatório das 8h sai às 5h.
7. **Sem gate de idempotência** → mensagem editada, restart e reação re-disparam alerta/DM.
   Gravar dado é idempotente por upsert; **avisar gente precisa de gate** (`references/02-codigo-base.md`).

## Fase 9 — Verificação (obrigatória, é ela que fecha o trabalho)

**Build verde não prova nada.** O container pode buildar e morrer no boot — e o `update`
derruba o container antigo antes de o novo subir, então uma imagem quebrada tira o bot do ar.
Depois de **todo** deploy, nesta ordem:

```bash
# 1. está rodando (e não reiniciando em loop)?
ssh <USUARIO>@<IP> 'cd /opt/<BOT> && docker compose ps'
#    STATUS "Restarting (1) 5 seconds ago" = loop de crash → passo 2

# 2. imprimiu a linha de boot?
ssh <USUARIO>@<IP> 'cd /opt/<BOT> && docker compose logs --tail 30' | grep "Online as"
#    sem essa linha = NÃO subiu, por mais verde que o build tenha ficado

# 3. erro no boot?
ssh <USUARIO>@<IP> 'cd /opt/<BOT> && docker compose logs --tail 100' | grep -iE "error|ERR_MODULE|Missing|Invalid"
```

E o teste que realmente conta, no Discord, com um humano na frente:

- `!ajuda` no canal → respondeu?
- `/resumo` → o slash **aparece na lista** e responde?
- postar uma mensagem do formato que o bot escuta → gravou no banco?
- **editar** essa mensagem → atualizou o registro em vez de duplicar?
- reiniciar o container e repetir → **não** re-notificou ninguém?

Nunca diga "está pronto" sem colar a saída real dos passos 1–3.

### Quando falhar, é quase sempre um destes

| Sintoma | Causa quase sempre |
|---|---|
| Online, `message.content` vazio | MESSAGE CONTENT INTENT desligado no portal |
| Online, mudo em **um** canal só | permissão do canal (override de cargo), não código |
| Slash não aparece | faltou `applications.commands` no convite, ou registrou global (propaga em até 1h — em dev registre por guild) |
| `Invalid token` no boot | o `.env` não chegou no container (`env_file` faltando, ou subiu sem recriar) |
| Restart loop com `ERR_MODULE_NOT_FOUND` | o Dockerfile não copiou um arquivo que o código importa |
| Cron no horário errado | falta `timezone` no `node-cron` |
| Mensagem processada 2x | falta dedup na lista de canais, ou falta gate de idempotência |

## Checklist final

As sete armadilhas acima resolvidas e a Fase 9 colada, mais:

- [ ] `GUILD_ID` e IDs de canal em env var — nenhum ID hardcoded; convite com permissões mínimas
- [ ] `.env` fora do git e `chmod 600` na VPS; `.env.example` commitado com as chaves vazias
- [ ] Banco com `discord_message_id UNIQUE`; bot usando **service role**, nunca a anon key
- [ ] Parser de texto é função pura e tem teste; cron não posta quando não há nada a dizer
- [ ] Compose com `restart: always` e rotação de log; deploy por `git pull` + `docker compose up -d --build`
