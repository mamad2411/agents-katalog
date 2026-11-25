---
name: limpeza-mac
description: >-
  Limpeza profunda de um Mac de desenvolvimento (só macOS). Cobre worktrees órfãs e
  mergeadas, branches já mergeadas, node_modules e .next de repo parado, caches de
  npm/uv/bun/yarn, versões velhas de CLIs de IA, a VM do Claude Desktop e os restos do
  OrbStack. Primeiro um inventário que não apaga nada; o SHA de cada branch vai para um
  ledger antes de apagar. Só manual: "/kit-vamoo:limpeza-mac".
disable-model-invocation: true
allowed-tools:
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/skills/limpeza-mac/scripts/inventario.sh" *)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/skills/limpeza-mac/scripts/inventario.sh *)'
---

# Limpeza do Mac

O espaço de um Mac de dev raramente está onde o limpador comercial procura. Ele mora em
node_modules/.next dos repos (dezenas de GB), no disco da VM do OrbStack, no cache do npm e
na VM do Claude Desktop. Esta skill mede isso, apaga só o que é seguro por construção e
guarda o SHA de cada branch que sai, para dar para restaurar.

Só roda no macOS: em outro sistema os dois scripts dizem isso e saem sem fazer nada. Os
caminhos de `~/Library` abaixo também são só do Mac.

```bash
echo "$HOME/backups/limpeza-$(date +%F)"   # o ledger desta limpeza
df -h /System/Volumes/Data | tail -1     # o `df /` mostra o volume do sistema, não o seu
```

Cada bloco roda num shell novo, sem as variáveis do anterior. Anote o caminho que o `echo`
imprimiu e escreva-o por extenso nos comandos seguintes, no lugar de `<ledger>`: a data sai
uma vez só, e uma limpeza que passa da meia-noite continua no mesmo ledger. O plano fica em
`<ledger>/plano`.

O ledger vai para `~/backups`, não para o scratchpad: quando a sessão acaba, o scratchpad
some, e o SHA iria junto.

Depois de uma compactação só o começo desta skill volta ao contexto: leia o arquivo de
`references/` no passo que o cita, mesmo que já tenha lido antes.

## Regras duras

Não toque em:
- `~/.claude/projects`: memória e transcripts, que o CLI já poda por `cleanupPeriodDays`;
- `~/.cache/huggingface` e `~/.cache/whisper-cpp`: modelos que um projeto pode estar usando,
  às vezes por symlink, e que custam GBs para baixar de novo;
- `~/Downloads`.

## 1. Inventário (não apaga nada)

Pergunte à pessoa onde ficam os repos dela. Sem raiz na linha de comando, o inventário usa
`LIMPEZA_RAIZES` (pastas separadas por `:`), e sem ela procura em `~/Developer`,
`~/Projects`, `~/code`, `~/WORKSPACES` e `~/Documents`. Pasta que não existe é ignorada.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/limpeza-mac/scripts/inventario.sh" <ledger>/plano ~/pasta-dos-repos ~/outra-pasta
```

A rodada leva alguns minutos, porque faz `git fetch --prune` em todos os repos (a única
escrita, e é nas refs remotas) e um `gh pr list` por
branch que não é ancestral do default. Não rode `du` em `~` inteiro: demora demais, e o
inventário já mede o que importa em `pocos.tsv` e `builds.tsv`. Um cache com `timeout` no
lugar do tamanho é um `du` que não voltou em 60 s (`POCO_TIMEOUT` troca): o mais provável é
um aviso de privacidade do macOS esperando resposta. Peça à pessoa para responder o aviso e
rode o inventário de novo.

Antes de apagar, mostre à pessoa só o que exige decisão dela:
- worktrees e branches `LOCAL(+N)` e `pushed(+N)`: trabalho que não chegou ao default;
- repos com `sem-origin`: as branches são a única cópia;
- clones duplicados do mesmo remote (`git remote get-url` igual): apagar clone inteiro está
  fora do escopo desta skill;
- órfãs com arquivo fora de build: o `aplicar.sh` não as toca. O git não as conhece mais,
  então `git status` ali não responde. Compare com o clone principal
  (`diff -rq -x node_modules -x .next -x .git <órfã> <clone>`) e mostre à pessoa o que só
  existe ou difere na órfã: é ela quem decide.

## 2. Git, builds e órfãs

```bash
DRY=1 bash "${CLAUDE_PLUGIN_ROOT}/skills/limpeza-mac/scripts/aplicar.sh" <ledger>/plano <ledger>   # mostre a saída à pessoa
```

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/limpeza-mac/scripts/aplicar.sh" <ledger>/plano <ledger>   # só com o OK dela
```

**Leia [references/travas-do-aplicar.md](references/travas-do-aplicar.md)** antes de mostrar
a saída do `DRY=1` à pessoa e sempre que algo ficar em `<ledger>/mantidas.tsv`: lá estão as
travas que o `aplicar.sh` respeita, e por quê (SHA igual ao head do PR, `worktree-gc.sh
--verificar`, ignorado conta como sujeira, worktree `ativa`, `DIAS_NM`, idade pelo reflog).

O que continua com você:
- **`worktree remove` sem `--force`.** Ele recusa sozinho uma árvore suja. Se a sujeira for
  só symlink de `.venv`/`models`, mostre à pessoa e remova com `--force` apenas com o OK
  dela.
- **Worktree detached** sai quando o HEAD é ancestral do default. Squash não é ancestral:
  o inventário mantém esse worktree, e a decisão é à mão. O `worktree-gc.sh --verificar
  <caminho>` já prova o caso quando o HEAD é o head de um PR MERGED no default, pelo `gh`
  ou pela API REST (token de `git config git-sync.tokenVar`, como no git-sync): exit 0 é a
  sua confirmação antes do remove. Quando ele diz "sem gh nem token da API", a prova não
  rodou; aí vale a prova manual da skill `worktrees`, seção "Limpeza no fim", com uma conta
  do `gh` que enxergue o repo. Detached não tem branch: ache o PR pelo SHA
  (`gh pr list -R <dono/repo> --state merged --search <sha-do-HEAD>`), e aqui o `headRefOid`
  tem de ser **igual** ao HEAD do worktree, num PR mergeado no default. A prova cobre só
  esse motivo: qualquer outro da linha `keep:` continua valendo. Com ela,
  `git -C <repo> worktree remove <caminho>`, sem `--force`, e só com o OK da pessoa.

Não rode `git gc --prune=now` nem `--aggressive` depois. O ledger restaura com
`git -C <repo> branch <branch> <sha>` enquanto os objetos soltos existirem, o que dura
cerca de duas semanas.

## 3. Caches

São regeneráveis e custam só um novo download:

```bash
npm cache clean --force
uv cache clean
rm -rf ~/.bun/install/cache ~/.yarn/berry/cache   # `bun pm cache rm` exige estar num projeto
brew cleanup -s --prune=all
```

Em cada ferramenta abaixo, mantenha a versão que o binário usa e apague o resto. Rode só as
que existirem na máquina:
- `~/.local/share/claude/versions/*`: confira `which -a claude` antes. Se o binário for o
  do Homebrew, todas as versões dali são lixo.
- `~/.local/share/cursor-agent/versions/*`: a versão ativa é o alvo de `~/.local/bin/cursor-agent`.
- `~/Library/Application Support/Cursor/User/globalStorage/anysphere.cursor-agent-worker/agent-cli/.local/share/cursor-agent/versions/*`:
  pode passar de centenas de MB por versão. A ativa é o alvo do link em `agent-cli/.local/bin/cursor-agent`.
  Os `cursor-agent-worker-*.log/.spec/.owner.json` com mais de 7 dias também saem.
- `~/Library/Caches/ms-playwright/*`: só a revisão mais antiga de cada navegador. Um
  projeto que fixa uma versão velha baixa de novo.

Estes precisam do app fechado. Rode `pgrep -fl` antes; se o app estiver aberto, o item vira
PENDENTE:
- **Claude Desktop**: `~/Library/Application Support/Claude/vm_bundles/claudevm.bundle`
  (pode passar de GBs, recriado quando o Cowork sobe). Se esta sessão roda dentro do Desktop,
  não toque.
- **Cursor**: `logs/*` e `CachedData/*`. O `state.vscdb` inchado se resolve com `DELETE FROM
  cursorDiskKV` + `VACUUM`. O VACUUM sozinho não resolve, porque a freelist fica vazia.
- **Chrome**: `OptGuideOnDeviceModel` (modelo on-device, pode passar de GBs). Ele volta sozinho
  se o recurso estiver ligado. Para de voltar desligando
  `chrome://flags/#optimization-guide-on-device-model`.

## 4. OrbStack

Com o app instalado, `orb stop` encolhe o disco esparso. Containers removidos não devolvem
espaço antes disso. Para a remoção completa, com o app já desinstalado e com o OK da pessoa:

```bash
rm -rf ~/Library/Group\ Containers/*.dev.orbstack ~/.orbstack
chmod u+w ~/OrbStack && rm -rf ~/OrbStack        # ponto de montagem, read-only
sed -i '' '/\.orbstack\/shell\/init.zsh/d' ~/.zprofile
```

Os links `docker`, `docker-compose`, `docker-credential-osxkeychain`, `kubectl`, `orb` e
`orbctl` em `/usr/local/bin` são do root e ficam quebrados. Entregue à pessoa o comando
pronto para ela rodar com sudo no terminal dela:
`sudo rm -f /usr/local/bin/{docker,docker-compose,docker-credential-osxkeychain,kubectl,orb,orbctl}`.

## 5. Relatório

Mostre o `df -h /System/Volumes/Data` de antes e de depois e o que saiu em cada fase. Feche
com um bloco `PENDENTE:` com o que ficou para a pessoa decidir: branches LOCAL, repos sem
origin, clones duplicados, apps que estavam abertos e o comando com sudo.
