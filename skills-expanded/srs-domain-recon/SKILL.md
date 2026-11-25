---
name: srs-domain-recon
description: >-
  Coleta o máximo de informação (recon/OSINT) sobre um ou mais domínios usando a
  ferramenta local SimpleReconSubdomain, entregando a saída em JSON por domínio.
  Use SEMPRE que o usuário quiser investigar um domínio do ponto de vista de
  segurança — mesmo que diga só "investiga o domínio X" ou cole uma lista de
  domínios. Triggers (PT/EN): "recon do domínio", "fazer recon de", "enumerar
  subdomínios", "subdomain enumeration", "mapear superfície de ataque", "attack
  surface", "descobrir ativos / asset discovery de um domínio", "OSINT de
  domínio", "coletar informações sobre o(s) domínio(s)", "coletar/pegar/listar URLs
  do domínio", "collect URLs", "spider URLs", "rodar
  SimpleReconSubdomain / simplerecon", "usar/rodar via docker", "no container",
  "sem instalar python". Não use para varredura de vulnerabilidade,
  exploração, ou scan de porta — isso é outra etapa.
---

# Domain Recon (SimpleReconSubdomain)

Roda a ferramenta local **SimpleReconSubdomain** contra um ou mais domínios. Para cada
domínio coleta um **JSON** (subdomínios, hosts vivos, IPs, cloud provider, SANs de
certificado, possíveis subdomain takeovers e mapa de rede), converte esse JSON num
**relatório Markdown** que é o output da coleta, e ao final **anexa os arquivos `.db`**
(além do `.md` e do `.json`) para o usuário baixar.

## Subcomando: configurar caminho de instalação

Quando o usuário disser algo como:

> `/srs-domain-recon setar pwd /home/osint/Documentos/SimpleReconSubdomain`
> `srs-domain-recon set path C:\Users\user\Documents\SimpleReconSubdomain`
> `setar o caminho do simplerecon para …`

Execute **apenas** isso (não rode recon) — use o helper, que grava o caminho (exatamente
como digitado) em `settings.json` preservando outras chaves e **não** valida existência
(o usuário pode estar configurando antes de instalar):

```bash
python3 "<SKILL_DIR>/scripts/resolve_install.py" --set "<caminho fornecido>"
```

Ele confirma com `Caminho salvo em …: <caminho>`. `<SKILL_DIR>` é o diretório que contém
este SKILL.md.

## Pré-requisitos (não validar além do necessário)

- O usuário cuida do próprio ambiente: **não** instale dependências, **não** rode
  `pip install`, **não** cheque/valide `config/api_keys.json`. Assuma que está pronto.
- A ferramenta acha seu próprio `config/`/`system.db`/`tlds.txt` via `__file__` (independe
  do cwd), **mas** os caminhos relativos que você passa (`--outfile`, `--db`, `--brute
  wordlists/...`, `--resolvers config/resolvers.txt`) são relativos ao cwd → sempre `cd`
  para o diretório de instalação antes de rodar (ou use caminhos absolutos).
- Interpretador: prefira **`python3.12+`** (recomendado pelo README do tool); cai para
  `python3` se não houver. O `requirements.txt` aceita 3.10+. Veja `$PY` no workflow.

### Resolução do diretório de instalação

**A cada execução da skill**, resolva `INSTALL` chamando o helper — ele faz toda a
precedência e sai com erro (exit 1) se nada servir:

```bash
INSTALL="$(python3 "<SKILL_DIR>/scripts/resolve_install.py")" || exit 1
```

Precedência aplicada pelo helper:
1. `<SKILL_DIR>/settings.json` → `simplerecon_install`, se não-vazio.
2. Senão, padrão por plataforma: Linux `~/Documentos/...` (depois `~/Documents/...`),
   macOS `~/Documents/...`, Windows `%USERPROFILE%\Documents\SimpleReconSubdomain`.
3. Valida que o diretório existe **e contém `simplerecon.py`**.

Se falhar, ele já imprime no stderr o caminho tentado e a dica de `--set` — basta abortar
(o `|| exit 1`). Em PowerShell:
`$INSTALL = python3 "<SKILL_DIR>/scripts/resolve_install.py"; if ($LASTEXITCODE) { exit 1 }`.

## Entrada

A entrada é um domínio ou vários. Antes de rodar:
- Normalize cada alvo para o domínio nu: remova `http(s)://`, `www.`, caminho, porta e
  barra final (ex.: `https://www.exemplo.com/login` → `exemplo.com`).
- Trate uma lista (vírgula, espaço, quebras de linha, ou um arquivo colado) como N alvos.

## Workflow

Rode **um processo por domínio** em loop. Isso mantém cada JSON isolado e dá a cada
domínio o seu próprio `--db` persistente — atendendo a "diferenciar os domínios e
processos". (Para uma run única consolidada, dá pra usar `-l lista.txt`; veja o final.)

```bash
# SKILL_DIR = diretório onde está este SKILL.md (resolvido pelo agente antes de rodar)
SKILL_DIR="<caminho desta skill>"

# Interpretador: prefere python3.12 (README do tool), cai para python3.
PY="$(command -v python3.12 || command -v python3.13 || command -v python3)"
[ -n "$PY" ] || { echo "[!] Python 3.12+ não encontrado"; exit 1; }

# INSTALL via helper (settings.json → padrão de plataforma → valida simplerecon.py).
INSTALL="$("$PY" "$SKILL_DIR/scripts/resolve_install.py")" || exit 1

cd "$INSTALL" || { echo "[!] Instalação não encontrada em $INSTALL"; exit 1; }
mkdir -p results/json results/db results/md results/html
STAMP="$(date +%Y%m%d-%H%M%S)"

for DOMAIN in exemplo1.com exemplo2.com; do
  echo "[*] Recon: $DOMAIN"
  # Monta o comando num array e roda — assim o mesmo comando vai pro relatório (--cmd).
  CMD=( "$PY" simplerecon.py
        -d "$DOMAIN" --profile full --verify-live --network-map --timeout 60 -v 3
        -o json
        --outfile "results/json/${DOMAIN}_${STAMP}.json"
        --db      "results/db/${DOMAIN}.db" )
  "${CMD[@]}"

  # JSON → Markdown (o "output da coleta", legível). O --db é linkado no topo do
  # relatório (junto do JSON e, se gerado, do HTML) — só entra se o arquivo existir.
  # O --cmd registra o comando exato da run na seção "Comandos executados".
  "$PY" "$SKILL_DIR/scripts/json_to_md.py" \
    "results/json/${DOMAIN}_${STAMP}.json" \
    -o "results/md/${DOMAIN}_${STAMP}.md" \
    --db "results/db/${DOMAIN}.db" \
    --cmd "${CMD[*]}"
done
```

Defina `SKILL_DIR` com o caminho real desta skill (onde estão `scripts/json_to_md.py` e
`scripts/resolve_install.py`).

Por que cada flag, no modo "máximo de informação" (default):
- `--profile full` → **todas** as fontes passivas **e ativas** (cobertura máxima).
- `--verify-live` → probe HTTP, extrai IPs, cloud, WAF, SANs do TLS e detecta takeover.
- `--network-map` → adiciona o grafo (`network`: nodes/edges/stats) ao JSON.
- `-v 3` → inclui o bloco `extras` (hosts/IPs/URLs externos) no JSON e no `--db`.
- `--timeout 60` → mais tolerante com fontes lentas em runs amplas.
- `--outfile` por domínio + `--db` por domínio → resultados isolados e persistentes.

O `--db` por domínio fica em caminho **estável** (sem timestamp) de propósito: assim, em
re-execuções, a base acumula histórico e o `--db-news` consegue diferenciar o que é novo.
O JSON, esse sim, leva timestamp por run.

### ⚠️ Antes de rodar o modo `full`

`--profile full` inclui módulos **ativos** que falam direto com a infra/DNS do alvo
(ex.: `zone_transfer`, `vhost_probe`, `spider`) e são detectáveis. Rode recon apenas
contra domínios que o usuário está **autorizado** a avaliar. Se o contexto for passivo,
furtivo, ou houver qualquer dúvida sobre autorização para tocar o alvo, troque para o
modo passivo abaixo.

### Coleta de URLs (source `spider`)

Quando o usuário quer **somente coletar URLs** de um domínio (não a superfície inteira de
subdomínios), use a source `spider` isolada. O miolo do comando passa a ser:

```
--sources spider --verify-live -v 3 --timeout 60
```

`spider` é uma source **ativa** (faz crawl direto no site do alvo) → vale a mesma trava de
autorização do modo `full` abaixo. As URLs coletadas saem no bloco `extras.urls` do JSON
(por isso o `-v 3`) e aparecem na seção **"URLs coletadas"** do relatório Markdown. O resto
do workflow é igual (resolução de `INSTALL`, `--outfile`/`--db` por domínio, geração do
`.md` via `json_to_md.py`, anexar `.db`/`.md`/`.json` no fim).

### Modos alternativos

Troque só o miolo do comando conforme o objetivo:

| Modo | Flags | Quando |
|---|---|---|
| **Máximo (default)** | `--profile full --verify-live --network-map -v 3 --timeout 60` | Cobertura total; alvo autorizado |
| **Coleta de URLs** | `--sources spider --verify-live -v 3 --timeout 60` | Usuário quer **só URLs** (source spider, ativa) |
| **Passivo / OSINT** | `--profile osint --verify-live --network-map -v 3` | Sem tocar o alvo; furtivo; autorização incerta |
| **Rápido** | `--profile fast` | Sanity check veloz |
| **Mais fundo (opt-in)** | adicione `--brute wordlists/subdomains-top1million-20000.txt --resolvers config/resolvers.txt --validate-resolvers --recursive --tld-brute` | Quando precisar esgotar a superfície (bem mais lento) |
| **Re-run / monitoramento** | adicione `--db-news` (mantendo o mesmo `--db`) | Só o que apareceu desde a última run |

Bônus visual: adicione `--network-html "results/html/${DOMAIN}_${STAMP}.html"` para gerar
um mapa de rede interativo (abre no browser; precisa de internet ao abrir). Ao usar isso,
passe também `--html "results/html/${DOMAIN}_${STAMP}.html"` ao `json_to_md.py` para o
relatório linkar o HTML no topo (junto do JSON e do `.db`).

Monitoramento contínuo: além de `--db-news`, o tool tem um agendador embutido —
`--watch-add "MIN HOR DIA MES DOW"` registra a run e `--watch` roda o daemon (jobs em
`config/system.db`; `--watch-list`/`--watch-del`/`--watch-clear` gerenciam). Para presets
de flags reutilizáveis, há `--config arquivo.json`. Veja a referência.

Detalhes de qualquer flag, perfil, ou do schema completo do JSON estão em
`references/simplerecon-reference.md` — leia esse arquivo se precisar ajustar fontes,
brute-force, proxy, etc.

### Execução via Docker (opt-in)

Use **apenas** quando o usuário pedir Docker explicitamente ("usar docker", "no container",
"sem instalar python"); senão, siga o modo nativo acima. A trava de autorização do
`--profile full` (módulos ativos) **continua valendo** — só o ambiente de execução muda.

Princípio: **só o motor de recon roda no container**; o passo JSON→Markdown
(`scripts/json_to_md.py`) continua no **host** (`$PY`, stdlib-only), lendo o que o container
gravou no `results/` montado. Não há `docker-compose.yml` no tool — usamos `docker run` com
a imagem `docker/simplerecon` (buildada do `docker/Dockerfile`).

Resolva `INSTALL`/`STAMP` e faça o `mkdir -p results/...` no host como no workflow nativo.
Depois:

```bash
IMAGE="docker/simplerecon"

# Builda a imagem do docker/Dockerfile (context = raiz do install) se ela não existir.
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "[*] Buildando $IMAGE…"
  docker build -t "$IMAGE" -f "$INSTALL/docker/Dockerfile" "$INSTALL" || exit 1
fi

# Monta config/api_keys.json read-only só se existir (fontes autenticadas).
KEYS="$INSTALL/config/api_keys.json"; KEYMOUNT=()
[ -f "$KEYS" ] && KEYMOUNT=(-v "$KEYS:/app/config/api_keys.json:ro")

for DOMAIN in exemplo1.com exemplo2.com; do
  echo "[*] Recon (docker): $DOMAIN"
  CMD=( docker run --rm
        -v "$INSTALL/results:/app/results"
        "${KEYMOUNT[@]}"
        "$IMAGE"
        -d "$DOMAIN" --profile full --verify-live --network-map --timeout 60 -v 3
        -o json --outfile "results/json/${DOMAIN}_${STAMP}.json"
        --db "results/db/${DOMAIN}.db" )
  "${CMD[@]}"

  # JSON → Markdown roda no HOST (lê o que o container gravou via mount).
  # --cmd registra o docker run realmente executado na seção "Comandos executados".
  "$PY" "$SKILL_DIR/scripts/json_to_md.py" \
    "$INSTALL/results/json/${DOMAIN}_${STAMP}.json" \
    -o "$INSTALL/results/md/${DOMAIN}_${STAMP}.md" \
    --db "$INSTALL/results/db/${DOMAIN}.db" \
    --cmd "${CMD[*]}"
done
```

Por que funciona: os caminhos relativos (`results/json/…`, `--db results/db/…`) resolvem a
partir do `WORKDIR /app`; com `-v "$INSTALL/results:/app/results"` eles caem em
`$INSTALL/results/...` no host. Wordlists/resolvers (`--brute wordlists/…`, `--resolvers
config/resolvers.txt`) já estão **dentro da imagem** — sem mounts extras. Para
`--network-html results/html/…` idem (cai no mount); passe `--html` ao `json_to_md.py`. Os
mesmos modos da tabela acima valem — troca-se só o miolo de flags.

Notas: a imagem roda como **uid 1000**; se o uid do host for igual, a escrita em `results/`
funciona direto — senão, acrescente `--user "$(id -u):$(id -g)"`. Run consolidada (`-l`) e
`--db-news` valem igual (grave a lista em `results/scope_*.txt`, que vai pelo mount, e
referencie `results/scope_*.txt` no container; o `--db` no mount persiste o histórico).
Detalhes adicionais — build remoto (`docker/Dockerfile.remote`), `--watch` e persistência de
`config/system.db` — estão em `docker/README.md` do install.

## Saída e fechamento

A coleta produz, por domínio:
- `results/md/<domínio>_<stamp>.md` — **relatório Markdown, o output da coleta** (entregável legível).
- `results/json/<domínio>_<stamp>.json` — dados brutos, **fonte da verdade**.
- `results/db/<domínio>.db` — base SQLite persistente (histórico; `--db-news`/`--db-list`).

Ao terminar, **sempre**:
1. **Anexe os arquivos `.db`** de cada domínio para o usuário baixar — use a ferramenta
   `present_files` (ou o mecanismo equivalente de anexo do ambiente) com os caminhos de
   `results/db/<domínio>.db`. Anexe também os `.md` e `.json` gerados.
2. Mostre/encaminhe o **relatório Markdown** como o resultado da coleta (é o
   `json_to_md.py` que o gera: no topo, links pros artefatos da run — JSON/`.db`/HTML — e a
   seção **"Comandos executados"** alimentada pelo `--cmd` (o comando exato — nativo ou
   `docker run`); depois resumo, takeovers em destaque, CNAMEs externos, hosts vivos,
   subdomínios, extras e stats do mapa de rede).
3. Diga os caminhos exatos dos arquivos.

Se um domínio falhar (ex.: zero resultados, erro de rede em uma fonte), siga para os
demais e reporte qual falhou no fim, em vez de abortar tudo. O `json_to_md.py` é
tolerante a campos ausentes, então rode-o mesmo em coletas parciais.

### Run consolidada (alternativa ao loop)

Se o usuário preferir uma única run para a lista inteira:

```bash
printf '%s\n' exemplo1.com exemplo2.com > results/scope_${STAMP}.txt
CMD=( "$PY" simplerecon.py -l "results/scope_${STAMP}.txt"
      --profile full --verify-live --network-map -v 3 --timeout 60
      -o json --outfile "results/json/scope_${STAMP}.json"
      --db "results/db/scope.db" )
"${CMD[@]}"

# Numa run multi-alvo o tool grava vários objetos JSON CONCATENADOS (não um array JSON);
# o json_to_md.py entende esse formato e gera uma seção por domínio.
"$PY" "$SKILL_DIR/scripts/json_to_md.py" \
  "results/json/scope_${STAMP}.json" -o "results/md/scope_${STAMP}.md" \
  --db "results/db/scope.db" \
  --cmd "${CMD[*]}"
```

O `--db` é keyed por domínio, então um DB compartilhado ainda distingue os alvos pela
coluna `domain`. O loop por-domínio continua sendo o default por dar JSONs separados e
ser mais robusto a falha de um alvo isolado. Anexe `results/db/scope.db` no fim.
