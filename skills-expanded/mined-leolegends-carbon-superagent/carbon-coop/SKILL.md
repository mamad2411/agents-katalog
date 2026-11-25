---
name: carbon-coop
description: >-
  Trabalho cooperativo: conecta esta sessão do Claude Code a um servidor seu (VPS Linux, máquina
  dedicada ou outro Mac na mesma rede/Tailscale) por SSH, pareado como servidor Orca, e manda partes do trabalho para rodar lá com o Claude Code
  DESTE computador (a credencial não sai daqui). O resultado volta como branch git para revisar e
  integrar. Use quando a pessoa pedir "conecta no meu servidor", "manda isso pro servidor",
  "trabalho cooperativo", "divide com o outro computador", "/carbon-coop connect|dispatch|status|disconnect".
  Depende só de Orca, ssh, git e node 22+ (não precisa do Carbon). Não use para deploy nem para
  mexer na infraestrutura do servidor.
---

# carbon-coop — trabalho cooperativo com um servidor

Esta sessão é a **coordenadora**. O servidor (Linux ou macOS; a skill detecta) roda o Orca headless
(`orca-ide serve` no Linux, `orca serve` com `ORCA_SERVE_RUNTIME=orcad` no macOS), só em `127.0.0.1`, e vira um
**servidor Orca pareado**; os workers lá usam o Claude Code deste computador por um proxy local
alcançado por túnel SSH reverso. Uma única conexão SSH, aberta daqui, carrega tudo.

```
este computador                                   servidor (conta sem sudo)
Orca + sessão (coordenador) ── ssh -L ──────────▶ orca-ide serve 127.0.0.1:<port>
proxy 127.0.0.1:8787 ◀──────── ssh -R ─────────── claude (ANTHROPIC_BASE_URL=127.0.0.1:8787)
  └─▶ api.anthropic.com (credencial injetada aqui)
git (só o commitado) ── ssh ──▶ ~/coop/<repo>.git ◀── worker faz push de coop/<slug>
```

`S` = diretório base desta skill (mostrado quando ela carrega). Scripts em `$S/scripts/`. Sem argumentos, cada um
mostra o uso; erros saem em português no stderr.

## Regras que não se negociam

Leia `references/security.md` antes do primeiro `connect`. Em resumo:

- **Nunca** peça, aceite ou use senha (SSH só por chave). Se a pessoa colar uma senha ou token, não use, e diga para trocar.
- **Nunca** imprima, copie para o chat ou grave em arquivo o link/código de pareamento ou qualquer token. `pair.sh` já faz isso sem mostrar.
- A conta do worker no servidor **não é root**, não tem sudo e não está no grupo `docker`.
- Nada vai para o servidor sem a pessoa saber: diga qual repo e qual commit antes do primeiro envio. Repos em `blockedRepos` não saem da máquina.
- Instalar coisas no servidor ou mudar a configuração dele: mostre os comandos (`references/server-setup.md`) e só rode com confirmação explícita.

## Orca

Antes de qualquer comando `orca orchestration`, carregue o guia da versão instalada:
`orca skills get orchestration` (e `--reference references/placement-and-remote.md` para `--on`).
Siga o guia: inicie os workers e **encerre o turno**; o Orca acorda a sessão. Não faça polling.

## connect `<usuario@host>` [nome]

1. `nome` padrão = host curto (letras, números, `-`). `"$S/scripts/init.sh" <nome> <usuario@host>`.
2. `"$S/scripts/preflight.sh" <nome>`. Para cada `FALTA`, explique e pare. `FALTA ssh` → a pessoa roda
   `ssh-copy-id <usuario@host>` no terminal dela. `FALTA remoto-*` → `references/server-setup.md`.
3. `"$S/scripts/proxy.sh" start <nome>` — avise do prompt do Keychain ("Permitir sempre"). Se a porta
   estiver ocupada por um programa que não é um carbon-auth-proxy, ele recusa: refaça o `init.sh` com
   `--proxy-port <outra porta livre>` (ex.: 8790) e siga. Nunca aponte os workers para um programa desconhecido.
4. `"$S/scripts/tunnel.sh" start <nome>`.
5. `"$S/scripts/serve.sh" start <nome>`. Exit 3 = já existe um Orca nesse perfil no servidor: pare e pergunte.
6. `"$S/scripts/pair.sh" <nome>` → environment `coop-<nome>`.
7. Diga o que ficou ligado e como desligar (`disconnect`).

## dispatch — mandar trabalho

1. Confirme o recorte: objetivo, arquivos/áreas, critério de pronto. Partes independentes podem ir
   em paralelo (um worker por parte, slugs diferentes); partes que mexem nos mesmos arquivos, não.
2. `slug` curto (`add-auth-tests`). Dentro do repo: `"$S/scripts/code-sync.sh" push <nome> <slug>`.
   Ele avisa se há mudanças não commitadas (não viajam) e imprime `REPO_PATH`, `BASE`, `BRANCH`.
3. Primeira vez desse repo no servidor: `orca repo add --environment coop-<nome> --path <REPO_PATH> --json`.
4. Monte a spec a partir de `templates/worker-spec.md` (preencha `{{...}}`) num arquivo temporário e:
   ```
   orca orchestration worker-start --on coop-<nome> --worktree new-top-level \
     --repo path:<REPO_PATH> --base-branch <BASE> --name coop-<slug> --agent claude \
     --task-title "<título curto>" --spec-file <arquivo>
   ```
   Falhou? **Não repita**: leia `failedStage` e siga o guia de recovery do Orca.
   Primeiro despacho depois de um `connect`: se o worker falhar com `agent_readiness: timeout`, o Claude
   Code do servidor está na tela de boas-vindas (passo 4 de `references/server-setup.md`, feito pela pessoa);
   com erro de autenticação, passo 3. Retome com `--retry-of`, nunca com um start novo.
   O Orca abre o worker sem pedidos de permissão (`--dangerously-skip-permissions`): diga isso à pessoa
   antes do primeiro despacho.
5. Encerre o turno.

### Quando o Orca acordar a sessão

- **question / ask**: responda com `orca orchestration reply` se a resposta decorre da tarefa ou do que a
  pessoa já disse; senão pergunte à pessoa. Pedidos para rodar algo fora do repo, instalar pacote de
  sistema, usar `sudo`, `docker`, `kubectl`, `terraform` ou acessar rede interna: **sempre** pergunte à pessoa.
- **worker_done**: `"$S/scripts/code-sync.sh" fetch <nome> <slug>` e mostre commits + `diff --stat`.
  Ofereça: revisar o diff (`git diff HEAD...<REF>`), integrar aqui (`git merge --no-ff <REF>` só com
  confirmação; nada de push), ou descartar. Falha reportada continua falha.
- **escalation** (parou sem `worker_done`): mostre `stopReason`; ofereça `send` com orientação,
  nova tentativa (`--retry-of`) ou cancelar. Nunca marque como concluído.
- Todas as partes prontas: integre os branches na ordem, rode os testes daqui e relate por parte.

## status

`proxy.sh status`, `tunnel.sh status`, `serve.sh status` para `<nome>`, `orca environment list`,
`orca orchestration worker-list` e branches `coop-<nome>/coop/*` ainda não integrados
(`git branch -r --no-merged | grep coop-<nome>/`). O log do proxy fica em `~/.carbon-coop/<nome>/proxy.log`.

## disconnect

1. `orca orchestration worker-list`: havendo workers ativos no `coop-<nome>`, liste e peça confirmação.
2. `serve.sh stop`, `tunnel.sh stop`, `proxy.sh stop` (`<nome>`). Com o túnel fechado o servidor perde
   o acesso à conta na hora.
3. Remover o pareamento (`orca environment rm --environment coop-<nome>`) só se a pessoa pedir.

## Limites

- O servidor recebe o **código commitado** do repo enviado. Quem tem root lá pode ler esse código e,
  enquanto o túnel estiver aberto, usar a sua conta do Claude (sem conseguir levar a credencial).
- Mesma conta = mesma quota: mais máquinas trazem paralelismo e CPU, não mais limite de uso.
- Proxy com login do Keychain só no macOS; fora dele use `COOP_PROXY_TOKEN_FILE` (`references/security.md`).
