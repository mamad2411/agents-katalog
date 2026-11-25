# CLAUDE.md — SIMEops

> Este arquivo é carregado automaticamente a cada sessão. Contém regras operacionais do projeto.
> Estado do sistema: [workdesk/ARQUITETURA.md](workdesk/ARQUITETURA.md) — a porta de entrada de toda sessão.

---

## 0. Nome do projeto

O app chama-se **SIMEops**. O diretório ainda se chama `Netrios News/` por legado (nome antigo, erro do início). **Sempre referir como SIMEops** em código, docs, logs. Renomear diretório/repos está no backlog (ver ROADMAP).

---

## 1. Regra zero — como trabalhamos

- **Sócio, não funcionário** — discutir antes de codar, questionar pedido que parece errado, discordar com argumento.
- **Pró-ativo** — reportar achado inesperado na hora, sem esperar ser perguntado.
- **Sem agentes de code review/auditoria** — investigar manual com Grep+Read, mostrar findings, só codar após aprovação.
- **Fixes cirúrgicos** — nada de scope creep. Bug fix ≠ refactor.
- **Verificar antes de afirmar** — nenhum documento é fonte da verdade sobre o código. Antes de escrever "X está quebrado" ou "falta fazer Y", **conferir na fonte**. Em 27/08, 20 minutos de Grep acharam três pendências consertadas semanas antes, uma delas no bloco que mandava ler primeiro.

**Quando o João estiver frustrado** ("puta merda", "não sei mais o que fazer"): cortar a análise longa e ir direto aos 3 principais culpados + proposta de fix. Análise extensa só quando ele pedir.

**O João autorizou consultar a documentação da Anthropic sobre o próprio modelo** para saber como ser mais eficaz.

**Quando o pedido não aproveitar bem o modelo** (vago, contexto de menos): dizer **antes** de executar — "do jeito que tá pedindo vai sair capenga; meu ponto forte aqui é X, me dá Y que eu entrego melhor". Vale igual para limitação: não dá para ver o Flutter renderizado nem rodar o app no device dele. **Dizer, nunca fingir que funcionou.**

---

## 2. Workdesk — a mesa de trabalho

A workdesk é onde o Claude mantém a memória do app. Ela existe para que **qualquer instância nova chegue sênior**, sem reconstruir contexto do zero. Por isso é orgânica: cresce e é podada.

### Por onde começar

🚪 **Em sessão nova, começar por [workdesk/ARQUITETURA.md](workdesk/ARQUITETURA.md).** É o **único** documento de estado do sistema. Se aparecer uma segunda cópia do estado atual em qualquer outro lugar, **apagar a cópia** — não mantê-la em sincronia.

Isso já falhou uma vez, e caro: até 27/08 existia um bloco "ESTADO DO MUNDO" no topo do DEV_LOG fazendo esse papel. Ele chegou a **376 linhas**, listava como pendente um bug corrigido 18 dias antes, e dava **três respostas diferentes** para "a migration 025 rodou?" — no mesmo bloco. Foi dissolvido.

### A regra zero

🚨 **Documento não copia o que o código já diz.** Sem stack, sem árvore de arquivos, sem lista de chaves de config, sem shapes de request, sem versões de dependência — isso se lê na fonte, em dois segundos, e sempre certo. A cópia **apodrece calada** e vira uma segunda verdade que faz errar com confiança (em 04/08 a ARQUITETURA afirmava 4 coisas falsas dentro de uma caixa escrita "LEIA ANTES DE MEXER"; em 08/08 duas cópias da tabela de cores puseram dois violetas diferentes no mesmo APK).

Entra na workdesk só o que **custa dinheiro ou tempo para redescobrir**: medições, o porquê das decisões, o que foi tentado e falhou, e o estado do que não se enxerga do código. **O porquê de uma linha específica mora num comentário colado nela, não aqui.**

### Os documentos, e o papel de cada um

Três tempos, e um item vive em **um** deles:

- [ARQUITETURA](workdesk/ARQUITETURA.md) — **presente**. Como o sistema é e por quê. Editado in-place quando algo estrutural muda. **A porta de entrada.**
- [DEV_LOG](workdesk/DEV_LOG.md) — **passado**. Append a cada mudança de código ou decisão técnica, sem esperar pedido. É consultável por busca, não por leitura — pode ser grande.
- [ROADMAP](workdesk/ROADMAP.md) — **futuro**, em três seções: 🔴 AGORA / 🟡 DEPOIS / 🔵 IDEIAS. **Item feito SAI** — não vira ✅ de troféu, a história dele já está no DEV_LOG.

Mais três vivos, por domínio: [API_CONTRATO](workdesk/API_CONTRATO.md) (decisões de contrato que não se desfazem), [FUNIL](workdesk/FUNIL.md) (onde cada item da busca morre, com números) e [DESIGN_CONTRATO](workdesk/DESIGN_CONTRATO.md) (a linguagem visual do app).

📍 **O único pedaço de "presente" que fica no DEV_LOG** é o bloco **ONDE PARAMOS**, no topo: **teto de ~25 linhas, sempre sobrescrito, nunca acumulado**. Passou disso, é porque virou arquitetura ou virou roadmap — mandar para o documento certo. Foi ignorar esse teto que criou o ESTADO DO MUNDO.

### O que rotaciona e o que persiste

Esta é a divisão que sustenta tudo:

| 🔄 **rotaciona por fase** | 📌 **persiste e muda com o código** |
|---|---|
| `DEV_LOG`, `ROADMAP` e os briefings daquele trabalho | `ARQUITETURA`, `API_CONTRATO`, `FUNIL`, `DESIGN_CONTRATO`, `SQL/` |
| são **recortados** para `workdesk/Fases/` no encerramento | **nunca** são arquivados; editados in-place |
| descrevem um período que acabou | descrevem o presente |

O DEV_LOG e o ROADMAP **andam juntos**: são as duas metades do mesmo período — o que se fez e o que se ia fazer.

🚨 **O gatilho da rotação é o ROADMAP fechar:** os itens de 🔴 AGORA acabaram e o que vem a seguir é outro assunto. **Não é o mês virando, nem o arquivo crescendo.** Se o DEV_LOG passar de ~1.500 linhas ou começar a cobrir dois assuntos que não se conversam, a fase provavelmente já devia ter fechado — propor o corte na hora. A antiga "Fase 9" acumulou **25 dias, seis trabalhos distintos e 5.053 linhas** antes de alguém notar.

**Ao encerrar**, a pasta tem que ficar **auto-contida**: recebe os 🔄 recortados, uma **cópia** da `ARQUITETURA` (retrato do fim da fase — a viva continua na raiz) e um **README** com o que a fase resolveu, as descobertas que valem para sempre e os erros cometidos. Atualizar também o índice [Fases/README.md](workdesk/Fases/README.md). Só então a raiz recomeça com DEV_LOG e ROADMAP novos.

📁 **O nome da pasta carrega o período:** `Fase 08 — 2026-07-30 a 2026-08-02`. Com o zero à esquerda, a ordem alfabética é a cronológica.

**Arquivar 🗂️ na hora certa.** O `FRONTEND_BRIEFING` dizia "o app ignora oito campos" meses depois do app parar de ignorar, e seguia sendo apontado como "documento de entrada" em três lugares. Documento que descreve problema resolvido é pior que documento nenhum.

**Documento arquivado não se reescreve.** Retrato é retrato — link quebrado em pasta de fase é esperado, e o que sumiu está mapeado no [índice das fases](workdesk/Fases/README.md).

Estamos na **Fase 11** (produção de verdade: deploy, auth, dedup, infra); 1 a 10 estão arquivadas.

### O verificador — a única defesa que não depende de memória

```bash
node workdesk/scripts/verificar-workdesk.cjs
```

Ele confere, nos documentos **persistentes**, se todo `identificador` citado ainda existe no código e se todo link ainda resolve. Roda em 0,2s e **já roda sozinho no início de cada sessão** (hook `SessionStart`), calado quando está tudo certo.

Ele existe porque **regra escrita não é defesa**. Só em 2026 apodreceram a ARQUITETURA (quatro afirmações falsas dentro de uma caixa escrita "LEIA ANTES DE MEXER"), o ESTADO DO MUNDO e o MIGRATIONS_LOG — os três com regra mandando atualizar.

⚠️ **O que ele não pega:** se o que está escrito é **verdade**. Um identificador pode existir e a frase sobre ele estar errada. Ele cobre apodrecimento estrutural, não semântico — o resto continua sendo conferir na fonte.

Achou algo? Ou o documento ficou para trás (corrija o documento), ou o identificador é externo legítimo (adicione a `EXTERNOS` no script, **com o motivo escrito**).

### Obrigações que não dependem de pedido

- Toda migration SQL em [workdesk/SQL/migrations/](workdesk/SQL/migrations/) **obriga** entrada em [MIGRATIONS_LOG.md](workdesk/SQL/MIGRATIONS_LOG.md) **no mesmo turno**.
- Achou **duas respostas para a mesma pergunta** em documentos? Medir na fonte e **apagar a errada no mesmo turno**. Não deixar para depois: é assim que nasce a segunda verdade.
- Mudou algo estrutural no código? A `ARQUITETURA` muda **no mesmo turno** — ela é a que acompanha o código, não a que se revisa depois.
- **Fim de sessão:** revisar ROADMAP + ARQUITETURA + confirmar que a última entrada do DEV_LOG cobre a sessão inteira.

---

## 3. Definição de "pronto"

1. **Backend TS** — `npx tsc --noEmit` passa sem erro
2. **Flutter** — `flutter clean` + build, testado em **device físico via LAN IP**, nunca emulador
3. **Migration SQL** — aplicada no Supabase **e** registrada no [MIGRATIONS_LOG](workdesk/SQL/MIGRATIONS_LOG.md), no mesmo turno
4. **DEV_LOG** atualizado com a mudança
5. **Commit feito** — ou adiado explicitamente, com motivo

> **Nada disto é sagrado.** Se uma regra daqui atrapalhar, o João reporta e a gente revisa. Refinar com o uso, não engessar.

---

## 4. Stack e comandos

**Backend** (Node + TypeScript + Express + BullMQ)
```bash
cd backend
npm run dev              # desenvolvimento local
npx tsc --noEmit         # OBRIGATÓRIO após mudança TS
```

**Admin Panel** (Next.js 16 + shadcn/ui)
```bash
cd admin-panel
npm run dev              # localhost:3001
```

**Mobile** (Flutter/Android)
```bash
cd mobile-app
# URLs + DSN por ambiente vem de env/{dev,staging,prod}.json (dart-define-from-file).
run-dev.bat              # dev local (ajustar IP em env/dev.json)
build-staging.bat        # APK staging (Sentry OFF)
build-prod.bat           # APK producao (Sentry ON via env/prod.json — git-ignored)
```

- `env/prod.json` NÃO é versionado (contém SENTRY_DSN). Use `env/prod.json.example` como template.
- Sentry só ativa se `SENTRY_DSN` não-vazia — dev/staging ficam sem envio (zero quota).
- Testar APK em **device físico via LAN IP**, nunca emulador.

**Branches**: `develop` (local) → `staging` (Render free) → `main` (Render prod).

---

## 5. Estrutura — onde mora o quê

```
backend/src/
├── services/
│   ├── filters/            → Filter0 regex, Filter1/2 GPT
│   ├── pipelineCore.ts     → stages compartilhados + post-filter cidade/estado
│   ├── scanPipeline.ts     → auto-scan CRON (periodoDias=2)
│   ├── manualSearchWorker.ts → busca manual BullMQ
│   ├── pushService.ts      → Firebase FCM por categoria
│   └── filter2GPT.ts       → extrai cidade+estado+tipo_crime
├── routes/newsRoutes.ts    → feed (aceita cidades=A,B,C)
└── cron/cronScheduler.ts   → filtra type='city' (NÃO state)

admin-panel/                → configuração do sistema
mobile-app/                 → Flutter (Android)
workdesk/                   → diário de bordo (DEV_LOG, ROADMAP, ARQUITETURA, SQL)
```

---

## 6. Gotchas do projeto (armadilhas conhecidas)

- **gpt-5-nano NÃO funciona** (reasoning tokens) — manter `gpt-4o-mini`.
- **CORS no Render** usa callback function, **não array direto** (array não funciona em produção).
- **Scan CRON** filtra `type === 'city'` — escanear `state` polui banco com cidades erradas.
- **Cidade + estado no Filter2** — sem estado, São José (SC) vira São José (SP).
- **Flutter visual** — sempre `flutter clean` antes do build, hot reload só pelo terminal do VSCode.
- **Device físico** (LAN IP), não emulador — emulador não simula push real.

---

## 7. Segurança — nunca sem autorização explícita

- `git push --force` (qualquer branch)
- `git reset --hard`, `git clean -f`, `git checkout .`
- `git commit --no-verify` ou bypass de hooks
- Migration SQL destrutiva: `DROP`, `TRUNCATE`, `ALTER ... DROP COLUMN`
- Commit de `.env`, credentials, keystores
- Merge direto em `main`
- Instalação/remoção em massa de dependências

Ação reversível = pode. Afeta produção ou perde dados = pergunta primeiro.

---

## 8. Deploy e infra (referência rápida)

**Produção** (Render Starter $7 cada, branch `main`)
- Backend: `https://sistemaprogestao-7fzs.onrender.com`
- Admin: `https://sistemaprogestao-r7fw.onrender.com`
- Health: `/health`

**Staging** (Render free, branch `staging`)
- Backend: `https://simeops-backend.onrender.com`
- Admin: `https://sistemaprogestao.onrender.com`

**Monitoramento**
- Sentry: org `joao-mw`, project `simeopsbackend` (plano Team $29/mo, só produção)
- Dev Panel: `c:/Projetos/dev-panel/` em `localhost:3100` (billing + health)

**Custos fixos**: Render $14 + Sentry $29 = **$43/mo** (+ OpenAI, BrightData, Jina variáveis).

---

## 9. Terminologia do projeto

- **SIMEops** — nome oficial e atual do app. ("Netrios News" é legado, só sobrevive no nome da pasta.)
- **Feed** — lista de notícias da cidade/grupo selecionado no app.
- **Tipo de crime** — campo granular (roubo, homicídio, tráfico...).
- **Categoria** — grupo de tipos (Patrimonial, Segurança, Operacional, Fraude, Institucional).
- **Cidade** (type=city) — unidade escaneável. **Estado** (type=state) — agrupador, NÃO é escaneado.
- **Grupo de cidades** — agrupamento visual (ex: "Grande Florianópolis").
- **Busca manual** — Flutter dispara dual-source (Web Top 100 + News paginado) em paralelo por cidade.
- **Auto-scan** — CRON Bright Data News (tbm=nws, qdr:d), rodando 24/7.
- **Pipeline de filtros** — Filter0 (regex) → Filter1 (GPT batch YES/NO) → Jina fetch → Filter2 (GPT full extrai campos) → dedup (embedding + DB 3 camadas).
