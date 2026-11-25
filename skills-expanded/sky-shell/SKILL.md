---
name: sky-shell
description: >-
  Kabuk betikleri ve terminal verimliliği: güvenli bash betiği iskeleti (set -euo pipefail,
  trap, tırnaklama), argüman ve hata yönetimi, sık kullanılan araçlar (rg, fd, jq, xargs, sed,
  awk, find), dosya ve metin işleme tarifleri, süreç ve port teşhisi, ssh ve scp/rsync,
  cron/systemd zamanlama, makefile ve justfile ile görev çalıştırıcılar, zsh/oh-my-zsh ve
  alias'lar, macOS ve Linux farkları, ShellCheck. "Script yaz", "terminal komutu", "bash",
  "otomatikleştir" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Shell

## Güvenli bash iskeleti

```bash
#!/usr/bin/env bash
set -euo pipefail            # hata olunca dur, tanımsız değişken hata, pipe'ta hata yakala
IFS=$'\n\t'
trap 'echo "✖ hata: satır $LINENO" >&2' ERR
cleanup() { rm -rf "${TMP_DIR:-}"; }
trap cleanup EXIT

usage() { echo "Kullanım: $0 <ortam> [--dry-run]" >&2; exit 2; }
[[ $# -ge 1 ]] || usage
ENV="$1"; DRY_RUN=false
[[ "${2:-}" == "--dry-run" ]] && DRY_RUN=true

TMP_DIR="$(mktemp -d)"
log() { printf '%s %s\n' "$(date +%H:%M:%S)" "$*" >&2; }

log "ortam: $ENV"
if $DRY_RUN; then log "kuru çalıştırma — hiçbir şey değişmeyecek"; fi
```
- **Her değişkeni tırnakla**: `"$file"` (boşluklu dosya adları), `"${arr[@]}"`.
- `[[ ]]` (bash) koşullar; `$(...)` komut ikamesi (backtick değil).
- Yıkıcı adımda onay veya `--dry-run`; `rm -rf "$DIR/"` öncesi `[[ -n "$DIR" ]]` kontrolü (boş değişken + rm = felaket).
- **ShellCheck** ile her betiği kontrol et (editör eklentisi + CI).
- 50 satırı geçen karmaşık mantık → Python/Node/Go betiği daha okunur ve test edilebilir.

## Araç kutusu

```bash
rg "createBooking" -t ts                       # ripgrep: hızlı içerik arama (.gitignore'a saygılı)
rg -l "TODO" | xargs -I{} echo {}              # dosya listesi
fd -e tsx components/                          # hızlı dosya bulma
jq '.dependencies | keys' package.json         # JSON sorgulama
jq -r '.[] | select(.status=="failed") | .id' runs.json
curl -s api/x | jq '.items[] | {id, name}'
sed -i '' 's/eski/yeni/g' dosya.txt            # macOS (BSD sed: -i '' gerekli); Linux: sed -i 's/…/…/g'
awk -F, '{ sum += $3 } END { print sum }' data.csv
find . -name "*.log" -mtime +7 -print          # önce listele…  (-delete eklemeden önce çıktıya bak)
du -sh * | sort -h                             # klasör boyutları
lsof -i :3000; kill -9 $(lsof -t -i :3000)     # portu kim kullanıyor / öldür
ps aux | rg node                               # süreçler
watch -n 2 "curl -s localhost:3000/health"     # periyodik kontrol (macOS: brew install watch)
```

## Dosya ve metin tarifleri

- Toplu yeniden adlandırma: `for f in *.jpeg; do mv -- "$f" "${f%.jpeg}.jpg"; done`
- Satır satır işleme: `while IFS= read -r line; do …; done < dosya.txt`
- Paralel: `xargs -P 4 -n 1` veya GNU `parallel`.
- Tekrar edenler: `sort | uniq -c | sort -rn | head`.
- CSV'de Türkçe karakter bozuksa: `iconv -f WINDOWS-1254 -t UTF-8 eski.csv > yeni.csv`.

## Uzak sunucu

`ssh -i ~/.ssh/key deploy@host`, `~/.ssh/config` ile kısa adlar (`Host prod` …), `rsync -avz --delete ./dist/ prod:/srv/app/` (scp yerine — artımlı),
`ssh prod 'journalctl -u api -n 100'`, tünel: `ssh -L 5433:localhost:5432 prod` (uzak DB'ye yerelden bağlan).

## Görev çalıştırıcı

```makefile
.PHONY: dev test db-reset
dev:      ; pnpm dev
test:     ; pnpm typecheck && pnpm test
db-reset: ; docker compose down -v && docker compose up -d db && pnpm db:migrate && pnpm db:seed
```
veya **just** (`justfile`) — Make'in tuzakları olmadan, argümanlı tarifler. Proje komutlarını tek yerde toplar; README'de `make dev`.

## Terminal verimliliği

- zsh + oh-my-zsh / starship (git dalı, Node sürümü istemde), `zoxide` (`z proj` ile klasöre atla), `fzf` (Ctrl+R geçmiş araması — insanların en sevdiği), `eza` (ls), `bat` (cat).
- Alias örnekleri: `alias gs="git status -sb"`, `alias dev="pnpm dev"`, `alias ports="lsof -i -P | grep LISTEN"`.
- macOS ↔ Linux farkları: `sed -i`, `date` bayrakları, `readlink -f` (macOS'ta `greadlink` veya `realpath`) — taşınabilir betikte GNU araçlarına güvenme veya kontrol et.
