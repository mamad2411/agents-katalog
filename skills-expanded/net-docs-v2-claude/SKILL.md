# net/ — Олимпиадын өдрийн toolkit

**Тусдаа git repo** (origin: `https://github.com/bum035/net.git`, branch `main`). Олимпиад болон лаб дээр **GitHub clone (эсвэл USB)-аар зөөдөг config + reference toolkit**. Олимпиадын компьютерт SecureCRT, PuTTY, VS Code аль хэдийн суусан байгаа — энэ folder зөвхөн **тохиргоо, snippet, reference**-г агуулна.

**Зорилго**: 2026-05-09 II шатны лаб дээр SecureCRT/VS Code/Claude Code-ийг хамгийн бага алхамаар бэлэн болгох.

> 🟢 **Олимпиадын дүрэм**: AI болон интернет **ЗӨВШӨӨРСӨН**. Claude Code, claude.ai, ChatGPT, Google, Cisco/NX-OS docs бүгд ашиглах боломжтой. Доорх workflow-д Claude Code-ыг гол edit tool гэж тооцсон.

## 🚀 Олимпиадын өдрийн нэг-команд bootstrap

Repo-г clone хийсний дараа:

| Платформ | Нэг команд |
|---|---|
| **Linux** | `bash ~/net/scripts/setup-linux.sh` |
| **Windows (интернеттэй)** | `pwsh $env:USERPROFILE\net\scripts\setup-windows.ps1` |
| **Windows (бүрэн offline, цэвэр шинэ машин)** | `pwsh D:\net\usb-offline\setup-windows-offline.ps1` — Python 3.12 + netmiko + Graphviz-ийг USB-аас суулгана |
| **USB fallback bundle (репог зөөх)** | `bash ~/net/scripts/make-usb-bundle.sh ~/Desktop` → `net-usb-<date>.zip` |

Эдгээр скрипт нь idempotent — олон удаа ажилласан ч өмнөх state-ыг эвдэхгүй. Алхам алхмаар `[ OK ] / [SKIP] / [FAIL]` гэж report хийнэ. Доорх manual setup-ыг **зөвхөн алхам бүрийг нарийвчлан ойлгоход эсвэл скрипт алдаа өгсөн үед** хэрэглэнэ.

### 🔌 Offline Windows bootstrap (`usb-offline/`)

Цэвэр шинэ Windows машин **интернетгүйгээр** ашиглах бол `usb-offline/` folder-д бүх артефакт байна (~58 MB). EVE-NG нь LAN-д л байх ёстой, internet шаардлагагүй.

**Юу багтсан:**
- `python-full/python-3.12.7-amd64.exe` — admin-гүй ч `InstallAllUsers=0`-аар суудаг full installer (26 MB)
- `python-embed/python-3.12.7-embed-amd64.zip` — no-admin fallback (11 MB)
- `graphviz/...Graphviz-12.2.1-win64.zip` — `dot.exe` portable (9 MB)
- `wheels/` — netmiko + 18 transitive dep + pip/setuptools/wheel + `get-pip.py` (Python 3.12, win_amd64 — 13 MB)
- `setup-windows-offline.ps1` — auto admin/no-admin, `_pth` засна, `pip install --no-index`, PATH persist
- `OFFLINE_README.md` — алхам алхмаар runbook + EVE-NG curl/python снippet + алдаа шийдэх хүснэгт

**Ажиллах logic:**
1. Python шалгана. Байгаа бол алгасна. Үгүй бол full installer → `%USERPROFILE%\PyOlymp\Python312\` (UAC амжилтгүй бол embed unzip дээр шилжинэ)
2. `python -m pip install --no-index --find-links wheels netmiko pyyaml`
3. Graphviz unzip → `%USERPROFILE%\PyOlymp\graphviz\bin\dot.exe`
4. Session + User PATH-руу нэмнэ
5. Smoke test: `import netmiko`, `dot -V`, `curl --version`, `tar --version`

**.gitignore:** `*.exe` blanket-ignore байгаа учир `!usb-offline/python-full/*.exe`, `!usb-offline/.../*.zip`, `!usb-offline/wheels/*.whl` overrride-уудыг тусгайлан нэмсэн. Эдгээр binary артефактууд **GitHub-руу commit хийгдсэн** — олимпиадын машин нь зөвхөн репог clone (эсвэл `Code → Download ZIP`) хийгээд `setup-windows-offline.ps1` ажиллуулахад бэлэн.

**Шинэчлэх (хэрэв Python/netmiko хувилбар шинэчлэх бол):**
```bash
# wheels-ийг pre-fetch (Linux)
pip3 download --platform win_amd64 --python-version 312 --implementation cp \
  --only-binary=:all: -d usb-offline/wheels netmiko pyyaml pip setuptools wheel
# Python full installer:  https://www.python.org/ftp/python/<ver>/python-<ver>-amd64.exe
# Graphviz:  https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/<ver>/windows_10_cmake_Release_Graphviz-<ver>-win64.zip
```

## Setup workflow — Linux VM (Ubuntu — primary)

> Linux SecureCRT-ийн Windows-той ялгаа: config зам нь `~/.vandyke/SecureCRT/Config/` (`%APPDATA%` биш). VBS script-үүдийн COM-объектууд (`WScript.Shell`, `Scripting.FileSystemObject`) **ажиллахгүй** — оронд нь Linux-д зориулсан Python хувилбар (`Scripts/backup_configs.py`, `Scripts/push_config.py`) эсвэл terminal-аас netmiko script ашиглана.

### Алхам 1 — Repo татах

```bash
cd ~
git clone https://github.com/bum035/net.git
code ~/net
```

USB fallback: `net/` folder-ыг copy.

### Алхам 2 — SecureCRT config (per-subdir symlink)

Зорилго: `~/.vandyke/SecureCRT/Config/` доторх **зөвхөн** `Sessions`, `Commands`, `Keywords`, `Scripts`, `Global.ini`, `ButtonBarV5.ini`, `SCRTMenuToolbarV3.ini` нь репог зааж өгнө. License (`SecureCRT_eval.lic`) нь жинхэнэ файл хэвээр үлдэнэ — symlink-аар орлуулбал лиценз ажиллахаа болино.

```bash
cd ~/.vandyke/SecureCRT
mv Config Config.bak                            # хуучин default-ыг backup
mkdir -p Config
cp Config.bak/SecureCRT_eval.lic Config/ 2>/dev/null || true
cp Config.bak/SSH2.ini Config/ 2>/dev/null || true

REPO=~/net/secureCRT/VanDyke/Config
DEST=~/.vandyke/SecureCRT/Config
for d in Sessions Commands Keywords Scripts KnownHosts Snapshots; do
    ln -sfn "$REPO/$d" "$DEST/$d"
done
for f in Global.ini ButtonBarV5.ini SCRTMenuToolbarV3.ini; do
    ln -sfn "$REPO/$f" "$DEST/$f"
done
ls -la "$DEST"   # бүх дотор нь "->" гарч буйг шалга
```

**Шалгах:** SecureCRT-г бүрэн хааж нээгээд → Sessions tree дээр `pod-template/R1`...`SW3` гарах ёстой. Button Bar дээр `BACKUP`, `PUSH`, `clean_ALL` товч харагдах ёстой.

### Алхам 3 — Python script (VBS-ийн оронд)

ButtonBar-ийн `BACKUP`/`PUSH` товч default-аар `.vbs` файл руу заасан байна. Linux дээр SecureCRT нь VBS engine ажиллуулдаг **гэхдээ** `WScript.Shell` гэх Windows COM object-ууд тэнд байхгүй тул бичсэн VBS-үүд **ажиллахгүй**.

Шийдэл — 2 сонголт:
1. **Manual run**: SecureCRT GUI → `Script → Run...` → `~/net/secureCRT/VanDyke/Config/Scripts/backup_configs.py` сонгоно. `push_config.py`-г идэвхтэй tab дээр ижилхэн.
2. **Button Bar товч re-target**: `Tools → Button Bar Manager → BACKUP товч → Edit → Run script` талбарыг `${VDS_CONFIG_PATH}/Scripts/backup_configs.py`-руу солино. PUSH товчны хувьд `push_config.py`. Дараа `File → Save Settings`.

Backup output:
```
$OLYMP_BACKUP_DIR (тавиагүй бол ~/OlympBackup/)
```

### Алхам 4 — VS Code extensions

```bash
code --install-extension fabiospampinato.vscode-highlight
code --install-extension Anthropic.claude-code
code --install-extension auchenberg.vscode-browser-preview   # claude.ai VS Code дотор
```

`cisco_highlights.jsonc`-ыг `Ctrl+Shift+P → Preferences: Open User Settings (JSON)` → root-д paste. `.cfg` файл нээж өнгө гарч буйг шалга.

### Алхам 5 — Claude Code login

```bash
npx @anthropic-ai/claude-code   # browser auth
```

Эсвэл VS Code Claude Code panel → Sign in. Backup нэвтрэлтүүд: claude.ai (Browser Preview tab), chat.openai.com.

### Алхам 6a — Олимпиадын өдөр — `olymp-run.py` (бүх workflow-г нэг командаар)

```bash
# Эхний удаа: interactive setup (host/port/user/pass/per-node creds)
# дараа нь ~/net/olymp.conf-руу хадгална
python3 ~/net/scripts/olymp-run.py

# Дараагийн run-ууд: conf-аас уншина (prompt алга)
# Лабын нэрийг auto-detect → ~/net/olymp-day/<lab-name>/ үүсгэнэ
# inventory.yml + backup + topology.svg/png + tar.gz бүгдийг үүсгэнэ
python3 ~/net/scripts/olymp-run.py
```

#### Нэмэлт mode-ууд (--mode flag)

| Mode | Үүрэг |
|---|---|
| `full` (default) | login → lab detect → inventory → backup → topology → archive |
| `setup` | Зөвхөн interactive prompt → conf хадгал |
| `diagnose` | EVE pre-flight: TCP, login, lab list, per-node telnet probe |
| `backup` | Inventory + backup (topology болон archive алгасах) |
| `push` | Нэг `.cfg`-ийг харгалзах device-руу буцаах (`--push-cfg <file>`) |
| `push-all` | Сүүлчийн backup folder-ийг бүхэлд нь буцаах (auto-match by filename) |
| `scrt` | SecureCRT session `.ini` бүх device-д үүсгэх (`--deploy` нэмбэл live config-руу) |
| `topology` | Зөвхөн graphviz dot/svg/png |
| `archive` | Зөвхөн tar.gz |
| `list-labs` | EVE-NG root-д буй бүх лабыг харуулах |

#### Жишээ

```bash
# Conf-ыг дахин асуух (IP/user/password солигдсон бол)
python3 ~/net/scripts/olymp-run.py --reconfigure

# Active биш лабтай ажиллах
python3 ~/net/scripts/olymp-run.py --lab "/path.unl"

# Зөвхөн backup татах (5 минут тутамд автомат-д тохиромжтой)
python3 ~/net/scripts/olymp-run.py --mode backup --no-confirm

# SecureCRT session generate + live config-руу хуулах
python3 ~/net/scripts/olymp-run.py --mode scrt --deploy

# Сүүлчийн backup-ийг бүхэлд нь буцаах (rollback)
python3 ~/net/scripts/olymp-run.py --mode push-all --yes

# Тодорхой config-ыг тодорхой device-руу
python3 ~/net/scripts/olymp-run.py --mode push \
    --push-cfg backup-2026-05-09_10-00/R1_2026-05-09_10-00.cfg

# Зөвхөн төлөв шалгах
python3 ~/net/scripts/olymp-run.py --mode diagnose

# Лаб жагсаалт
python3 ~/net/scripts/olymp-run.py --mode list-labs
```

#### SecureCRT integration

`olymp-scrt.py` (эсвэл `olymp-run.py --mode scrt`):
- Inventory-аас (эсвэл EVE API-аас) device бүрд `<name>.ini` SecureCRT session генерацлана
- Output: `olymp-day/<lab>/secureCRT/`
- `--deploy` flag нэмбэл live SecureCRT folder-руу хуулна:
  - Linux:   `~/.vandyke/SecureCRT/Config/Sessions/<lab>/`
  - Windows: `%APPDATA%\VanDyke\Config\Sessions\<lab>\`
- SecureCRT-ийн Connection Manager-ыг refresh (F4) эсвэл restart хийгээд session-ууд гарч ирнэ

`olymp.conf` (auto-saved):
```yaml
eve:
  host: 10.X.Y.Z
  port: 80
  user: student1
  password: Lab2026
node_defaults: {username: '', password: ''}
node_overrides:                          # only for nodes with AAA
  R1: {username: cisco, password: cisco}
  SW2: {username: admin, password: Admin@123}
```

### Алхам 6b — netmiko + telnet (terminal fallback)

VS Code terminal-аас шууд EVE-NG node-руу холбогдоно. SecureCRT хэрэгтэйгүй.

```bash
pip3 install --user netmiko pyyaml          # netmiko 4.6+ already суугаа

# 0) EVE-NG-ийн төлөв шалгах + inventory.yml auto-emit
~/net/scripts/diagnose-eve.py --host 10.X.Y.Z --check-nodes
~/net/scripts/diagnose-eve.py --host 10.X.Y.Z --emit-inventory > ~/pod1.yml

# Хурдан telnet helper
~/net/scripts/eve_telnet.sh 32769            # localhost:32769
echo "R1 32769" >> ~/.eve_pods.conf
echo "R2 32770" >> ~/.eve_pods.conf
~/net/scripts/eve_telnet.sh R1               # нэрээр харна

# Batch backup бүх pod (auth auto-fallback: empty/cisco/admin)
~/net/scripts/netmiko_backup.py ~/pod1.yml
~/net/scripts/netmiko_backup.py ~/pod1.yml --slow            # banner sluggish бол
~/net/scripts/netmiko_backup.py ~/pod1.yml --raw-on-fail     # transcript on fail
~/net/scripts/netmiko_backup.py ~/pod1.yml --ssh             # SSH force

# Single push (auth fallback дээр slow mode-той)
~/net/scripts/netmiko_push.py ~/OlympBackup/R1_2026-05-09_10-30.cfg \
    --host 10.X.Y.Z --port 32769 --slow --delay-per-line 0.3

# Single ad-hoc backup
~/net/scripts/netmiko_backup.py --host 10.X.Y.Z --port 32769 --name R1
```

> **Алдаа гарвал:** `usb-offline/TROUBLESHOOTING.md`-аас шинж тэмдэг бүрд тохирох шийдэл + manual fallback (SecureCRT/PuTTY/cmd-telnet/browser HTML5 console).

### Алхам 7 — Browser-in-VS Code (claude.ai холбоо)

`Ctrl+Shift+P → Browser Preview: Open Preview` → `https://claude.ai`. Side-by-side Claude Code panel + Claude.ai веб = config debug хурдан болно.

### Алхам 8 — EVE-NG "Connect" товчийг SecureCRT-руу redirect

Default `eve-ng-integration` пакет нь `telnet://` URL-ийг **xfce4-terminal**-руу зааж байдаг. SecureCRT-руу шилжүүлнэ:

```bash
# Handler script + desktop entry бэлэн (репо дотор)
chmod +x ~/net/scripts/scrt-telnet-handler.sh
mkdir -p ~/.local/share/applications

# Desktop entry-г байнгын газар хуулна (репог зөөвөл symlink эвдэрч магад)
cp ~/net/secureCRT/securecrt-telnet.desktop ~/.local/share/applications/

# Default handler болгон бүртгэх
update-desktop-database ~/.local/share/applications
xdg-mime default securecrt-telnet.desktop x-scheme-handler/telnet
xdg-mime query default x-scheme-handler/telnet   # → securecrt-telnet.desktop

# Тест
xdg-open telnet://127.0.0.1:32769
```

Буцааж eve-ng-integration handler-руу шилжүүлэх:
```bash
xdg-mime default eve-ng-integration.desktop x-scheme-handler/telnet
```

> Анхаар: `scrt-telnet-handler.sh` нь URL-ыг parse хийж `SecureCRT /T /TELNET host port` команд гүйцэтгэдэг. user@host:port форматыг таних боломжтой. Дебаг лог: `~/.cache/scrt-telnet.log`.

---

## Setup workflow — Windows (alt-machine)

> Олимпиадын машин Windows бол энэ замаар.

### Алхам 1 — Repo татах

**A. GitHub clone (preferred):**
```powershell
cd $env:USERPROFILE
git clone https://github.com/bum035/net.git
code .\net
```

Git суугаагүй бол Git-for-Windows portable татах эсвэл `.zip` download:
```
https://github.com/bum035/net/archive/refs/heads/main.zip
```

**B. USB fallback (интернет байхгүй бол):** `net/` folder-ыг USB рүү copy (~5 MB, .git-гүйгээр).

### Алхам 2 — SecureCRT config

`secureCRT/VanDyke/Config/` доторхыг `%APPDATA%\VanDyke\Config\` рүү хуулна (хуучин contents-ыг урьдчилан backup хийнэ). Эсвэл junction (preferred — repo-руу зааж өгнө, шинэчлэлт автоматаар орно):
```powershell
Move-Item "$env:APPDATA\VanDyke\Config" "$env:APPDATA\VanDyke\Config.bak" -ErrorAction SilentlyContinue
New-Item -ItemType Junction -Path "$env:APPDATA\VanDyke\Config" -Target "$env:USERPROFILE\net\secureCRT\VanDyke\Config"
```

### Алхам 3 — VS Code highlighting + Claude Code

1. VS Code extensions суулгах:
   ```powershell
   code --install-extension fabiospampinato.vscode-highlight
   code --install-extension Anthropic.claude-code   # Claude Code VS Code extension
   ```
2. `cisco_highlights.jsonc`-ыг VS Code → `Ctrl+Shift+P` → "Preferences: Open User Settings (JSON)" → root-к `highlight.regexes` object-ыг paste.
3. **Claude Code login**:
   - `Ctrl+Esc` → Claude Code panel → Sign in
   - Эсвэл terminal-аас: `npx @anthropic-ai/claude-code` → browser auth
   - **Backup**: claude.ai веб interface (login session нөөц)

### Алхам 4 — EVE-NG telnet handler (optional)

Хэрэв EVE-NG web UI-аас "Connect" товчоор ажиллахыг хүсвэл: `EVE-NG/win10_64bit_sCRT.reg` дээр double-click → merge. Бусад `.reg` нь VNC/Wireshark-д зориулагдсан, апп нь суугаагүй бол хэрэггүй.

### Алхам 5 — SecureCRT restart

Бүгдийг хэрэгжүүлсний дараа SecureCRT-г бүрэн хааж нээнэ (Global.ini-ийг зөв унших).

## AI / Claude Code workflow (олимпиадын өдөр)

> 🟢 AI болон интернет зөвшөөрөгдсөн. Claude Code-ыг гол edit tool болгож ашиглана.

### Үндсэн цикл

```
EVE-NG WebUI → SecureCRT (console)
              ↓ Button Bar: BACKUP
    %USERPROFILE%\OlympBackup\R1_<ts>.cfg
              ↓ VS Code workspace
    Claude Code chat: "Энэ config-д X алдаа байна. засаарай"
              ↓ Edit applied to .cfg
    SecureCRT → Button Bar: PUSH (push_config.vbs)
              ↓
    Router-руу line-by-line paste (LINE_DELAY_MS=50)
```

### Useful Claude prompt template-үүд

`reference/prompts.md` (хэрэв нэмбэл):

| Зорилго | Prompt template |
|---|---|
| Алдааг олох | "Энэ Cisco config-д ____ ажиллахгүй байна. show output: <paste>. Шалтгаан болон засварыг өг" |
| Syntax conversion | "Энэ IOS config-ыг NX-OS syntax руу хөрвүүл, feature командуудыг бүгд багтаа" |
| Generate config | "AS 17000 iBGP RR-ээс client RR1-руу IPv4 + IPv6 family activate хийдэг config бичиж өг" |
| Verify | "Энэ vPC peer-link config зөв үү? `vpc peer-link` нь port-channel дээр л байх ёстой" |
| Troubleshoot logic | "BGP neighbor 'Active' state-д наалджээ. Шалгах команд + хэрэв `update-source` алгассан бол хэрхэн засах вэ?" |
| Olympiad task parse | "Энэ даалгавар: <paste>. Топологи болон тавьсан шаардлагыг нэгтгэн config skeleton гарга" |

### AI ашиглахгүй хэсэг (өөрөө хийх ёстой)

- **Хариу шалгах** — AI буруу config гаргаж магадгүй (вершин syntax, deprecated keyword). `show run` дээр өөрөө хяна.
- **Шалгуурын логик** — олимпиадын даалгаврыг **өөрөө уншиж**, хязгаарлалтыг (open standard, prepend ашиглахгүй г.м.) AI-руу зөв тайлбарлах ёстой.
- **Debugging** — AI шалтгааныг хэлж чадавч `show ip ospf neighbor`-ийн output-ыг **өөрөө уншиж** AI-руу буцаах ёстой.

### Backup plan — интернет тасрах

Хэрэв АН нь wifi/wired interrupt вэл:

1. `net/reference/lab-NN.pdf` (offline cheat sheet) → 5 лабын syntax + topology тус бүрд
2. `net/reference/2024_round2/` болон `net/reference/2025_round2/` → бэлэн жишээ config
3. `.spsl` snippet-үүд (`pc_ip`, `nat_pat`, `ipsec_gre`, `show`)
4. SecureCRT Button Bar (DHCP, OSPF, BGP, ACL, NAT категориуд)

**Шалгах:** Олимпиадын өмнөх өдөр (өнөөдөр) wifi-ыг unplug хийгээд бүх workflow ажиллаж буйг шалгах.

## Layout

| Path | Үүрэг |
|---|---|
| `secureCRT/VanDyke/Config/` | **SecureCRT config payload** — Sessions, Commands, Keywords, Scripts, ButtonBar, Global.ini. **Linux:** `~/.vandyke/SecureCRT/Config/`-руу subdir symlink. **Windows:** `%APPDATA%\VanDyke\Config\`-руу junction |
| `secureCRT/VanDyke/Config/Scripts/*.py` | **Linux SecureCRT Python хувилбар** (VBS-ийн оронд) — `backup_configs.py`, `push_config.py` |
| `scripts/` | **Terminal-side helper-ууд + bootstrap** — `setup-linux.sh` / `setup-windows.ps1` (one-shot машины тохиргоо), `make-usb-bundle.sh` (offline .zip), `eve_telnet.sh` (EVE-NG telnet wrapper), `olymp-run.py` (**end-to-end orchestrator**: interactive prompts → save conf → auto-detect lab → folder + inventory + backup + topology + archive), `netmiko_backup.py` (multi-cred + retry batch backup), `netmiko_push.py` (config push w/ auth fallback + slow mode), `diagnose-eve.py` (EVE pre-flight: auth, lab list, per-node probe, inventory.yml auto-emit), `scrt-telnet-handler.sh` (telnet:// URL parse → SecureCRT), `start-olymp-session.sh` (tmux), `inventory.example.yml` |
| `secureCRT/securecrt-telnet.desktop` | Linux desktop entry — telnet:// URL handler-ыг SecureCRT-руу заана (EVE-NG Connect товч) |
| `EVE-NG/` | EVE-NG protocol handlers — `.reg` (telnet/vnc/wireshark URL handler) + `.bat` wrappers. Зөвхөн Windows-ийн EVE-NG web UI "Connect" workflow-д хэрэгтэй |
| `OlympBackup/` | `backup_configs.{vbs,py}` болон `netmiko_backup.py`-ийн өмнөх run-ийн жишээ (test data) — олимпиадын дараа цэвэрлэж болно |
| `cisco_highlights.jsonc` | VS Code Highlight extension regex (`.cfg`-д өнгө) — SecureCRT-н "Cisco Words - DkBg" port |
| `vscode_settings.jsonc` | VS Code user settings (Cascadia, `*.cfg → cisco`, CRLF, telemetry off, дэлгэц layout). `cisco_highlights.jsonc`-той хамт settings.json-руу merge |
| `*.spsl` | SecureCRT chat-paste snippet (`pc_ip`, `show`, `nat_pat`, `ipsec_gre`) |
| `button bar.sh` | Button bar товчны жагсаалтын текст reference |
| `reference/` | Offline cheat sheet, lab PDF, өмнөх жилийн config-ууд, AI prompt template (`prompts.md` бэлэн; PDF + 2024/2025 round2 placeholder, олимпиадын өмнөх өдөр Windows local-аас хуулна) |
| `usb-offline/` | **Цэвэр шинэ Windows машинд интернетгүйгээр Python + netmiko + Graphviz суулгах бундл** (~200 MB). `setup-windows-offline.ps1` (`-PythonVersion 3.10|3.11|3.12|3.13`, `-Diagnose`, `-ForceEmbed`, `-SkipPython` flag), `OFFLINE_README.md`, `TROUBLESHOOTING.md` (бүх алдааны шинж тэмдэг → шийдэл + manual fallback), `python-full/` (4 хувилбарын installer: 3.10.11, 3.11.9, 3.12.7, 3.13.1), `python-embed/` (мөн 4), `graphviz/`, `wheels/` (3.12), `wheels-py310/`, `wheels-py311/`, `wheels-py313/`. `.gitignore`-ын `*.exe` блокыг `!usb-offline/...` rule-аар override хийсэн |
| `vm-setup/` | **Linux cloud VM provisioning scripts** (Caddy + code-server + KasmVNC + Claude CLI). Олимпиадын станцыг remote dev workstation болгох routes — `code.egulcloud.com` / `vnc.egulcloud.com`. Энэ folder нь Windows toolkit-д хэрэгтэй биш, цөөн scripts ба `REPORT.md` (gitignore) |
| `olymp-day/` | **Олимпиадын өдрийн ажлын workspace** — `lab-01-ospf` ... `lab-05-libre` хоосон folder, `scratch/`, `CLAUDE.md` (Claude-д өгөх exam-day context). Tmux script энд cd хийнэ. Олимпиадын task-ийн config-уудыг энд бичнэ |
| `scripts/start-olymp-session.sh` | tmux bootstrap (`bash ~/net/scripts/start-olymp-session.sh` → claude/shell/monitor windows, `~/net/olymp-day`-руу cd) |
| `.gitignore` | `*.exe`, license artifacts, pre-installed binary folder-ууд, `id_ed25519`, `vm-setup/REPORT.md`, `OlympBackup/*.cfg/*.log`-ыг ignore |

## SecureCRT config — `VanDyke/Config/`

`%APPDATA%\VanDyke\Config\`-той ижил структуртэй. Хуулах эсвэл junction-аар link хийх (USB drop-in workflow дээр харна уу).

### Critical файлууд

| Файл | Юу хийдэг |
|---|---|
| `Sessions/Default.ini` | SSH2 template. Font: **Cascadia Code 12** / narrow Lucida Console |
| `Sessions/pod-template/` | **Бэлэн стуб session-ууд** — `R1`, `R2`, `R3`, `SW1`, `SW2`, `SW3` (Telnet, Default-аас бусад settings inherited). Pod-ийн IP мэдсэний дараа right-click → **Clone Session** хийж `pod1/R1` руу хувилаад Hostname/Port-ыг оруулна |
| `Commands/<topic>/__Commands__.ini` | Button Bar команд (dhcp/etherch/interface/nat/routing/show). `\\r` = Enter. `SEND_TO_ALL_SESSIONS` нь "Send Commands to All Sessions" toggle идэвхтэй tab бүрд илгээнэ |
| `Keywords/Cisco Words - DkBg.ini` | SecureCRT терминалын **үг-түвшний** highlighting. `cisco_highlights.jsonc`-той нийцтэй байх ёстой — нэг үг хоёр дээр хоёр өөр өнгөтэй байвал төөрнө |
| `Scripts/backup_configs.vbs` | **Windows-only.** Бүх tab-аас `show running-config` татаж `%USERPROFILE%\OlympBackup\<hostname>_<timestamp>.cfg`. `%OLYMP_BACKUP_DIR%` орчны хувьсагч тавьсан бол түүнийг ашиглана |
| `Scripts/push_config.vbs` | **Windows-only.** `.cfg` файлыг идэвхтэй session-руу мөр-мөрөөр push (`LINE_DELAY_MS=50`). File picker default — backup-той ижил зам |
| `Scripts/backup_configs.py` | **Linux SecureCRT хувилбар.** Ижил логик, `~/OlympBackup/` (эсвэл `$OLYMP_BACKUP_DIR`)-руу бичнэ. VBS-ийн COM-объект ажиллахгүй тул энийг ашиглана |
| `Scripts/push_config.py` | **Linux SecureCRT хувилбар.** File picker → идэвхтэй tab руу line-by-line push |
| `ButtonBarV5.ini` | Toolbar товчуудын тодорхойлолт (`button bar.sh` нь reference хувилбар) |
| `Global.ini` | Global preferences. Font, color, keymap дотроос гарна — patch хийхэд **SecureCRT хаасан байх ёстой**, нээлттэй үед өөрөө дарж бичнэ |
| `SCRTMenuToolbarV3.ini` | Menu/toolbar layout |

## VS Code Cisco highlighting

`cisco_highlights.jsonc` нь `fabiospampinato.vscode-highlight` extension-д зориулагдсан.

1. Extension суулгана (`code --install-extension fabiospampinato.vscode-highlight`).
2. JSON object-ийг **User `settings.json`**-д paste — root-key нь аль хэдийн `highlight.regexes` гэж бичигдсэн.
3. `.cfg` файлд "cisco" language ID онооно:
   ```json
   "files.associations": { "*.cfg": "cisco" }
   ```
   `language-cisco` extension суулгасан бол automatic. `filterLanguageRegex: "cisco"` нь зөвхөн "cisco" language-тай файлд highlight идэвхжүүлнэ — бусад файлд noise болохгүй.

`OlympBackup/R1_*.cfg`-г нээгээд тэст хийнэ. IP, interface, hostname, dangerous (`reload`, `erase`), routing protocol бүгд гэрэлтэх ёстой.

### SecureCRT keyword-той synchronization

SecureCRT-ийн `Keywords/Cisco Words - DkBg.ini`-д үг нэмэх үед `cisco_highlights.jsonc`-д **ижил үгийг ижил өнгөөр** бичнэ. Хоёр газарт зөрвөл VS Code дотор болон SecureCRT терминал дээрх ижил config өөр өнгөтэй харагдаж эргэлзээ үүснэ.

## .spsl quick-paste snippet-үүд

SecureCRT chat window дээр right-click → **Send → Paste**. Эсвэл `View → Chat Window` нээгээд text paste → **Send Chat to All**. Файл бүр `#section` comment header-тай.

| Файл | Контент |
|---|---|
| `pc_ip.spsl` | VPCS-д IP оноох (`ip 192.168.1.10/24 192.168.1.1` + `save`) |
| `show.spsl` | `show etherchannel summary` |
| `nat_pat.spsl` | Static NAT, dynamic NAT, PAT reference |
| `ipsec_gre.spsl` | GRE+IPsec router-1/router-2 бүрэн config (3DES/MD5/group2 — олимпиадын legacy IOS-д тохирсон) |

> **Анхаар**: `.spsl` доторх IP, AS number бол **жишээ**. Pod-ийн actual addressing-той тааруулж засах ёстой.

## EVE-NG client integration (`EVE-NG/`)

`EVE-NG/` бол **EVE-NG Web UI-аас "Connect" товч дарахад SecureCRT/PuTTY-г local launch** хийх workflow-ын registry handler-ууд. Зөвхөн web UI-аас шууд асаах хэрэгтэй үед merge хийх — SecureCRT-аас Sessions tree-р холбогдоход хэрэггүй.

| Файл | Үүрэг |
|---|---|
| `win10_64bit_sCRT.reg` | `telnet://` URL handler → SecureCRT |
| `win10_64bit_putty.reg` | `telnet://` → PuTTY (fallback) |
| `win7_64bit_ultravnc.reg` + `ultravnc_wrapper.bat` | `vnc://` → UltraVNC (UltraVNC суусан үед) |
| `win7_64bit_wireshark.reg` + `wireshark_wrapper.bat` | `wireshark://` → Wireshark capture (Wireshark суусан үед) |

`.reg`-ийг merge хийхээсээ өмнө SecureCRT-ийн **актуал суусан зам** (`C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe`) олимпиадын машин дээрхтэй таарч буй эсэхийг текст editor-аар нээж шалгана.

## Бүх холболтын арга — нэгтгэл

| Method | Платформ | Хэрэглэх үе | Команд / Action |
|---|---|---|---|
| **SecureCRT GUI** | Linux + Windows | Interactive console, password recovery, multi-tab paste | Sessions tree → R1/SW1 |
| **Button Bar BACKUP/PUSH** | Linux (Python) / Windows (VBS) | Бүх tab-аас batch backup, .cfg push | `Script → Run...` эсвэл товч дарах |
| **VS Code Terminal + telnet** | Linux | Хурдан single-node debug | `~/net/scripts/eve_telnet.sh R1` |
| **netmiko batch (Python)** | Linux | Olympic-day мөгүүтэй pod (6+ node) backup/push | `~/net/scripts/netmiko_backup.py pod1.yml` |
| **Claude Code CLI** | Linux + Windows | Config edit, debug, generate | `npx @anthropic-ai/claude-code` |
| **Claude Code VS Code ext** | Linux + Windows | Inline edit, panel chat | `Ctrl+Esc` |
| **claude.ai веб (Browser Preview)** | Linux + Windows | CLI down эсвэл vision хэрэгтэй | `Browser Preview: Open Preview` → `https://claude.ai` |
| **EVE-NG Web "Connect"** | Linux + Windows | One-click telnet to node | **Linux:** `xdg-mime default securecrt-telnet.desktop x-scheme-handler/telnet`. **Windows:** `.reg` merge |

## Олимпиадын өдрийн checklist

### Repo & Tools (Linux VM)
- [ ] `git clone https://github.com/bum035/net.git ~/net` амжилттай
- [ ] VS Code workspace-аар `~/net/` нээгдсэн
- [ ] SecureCRT суулгасан + лиценз `~/.vandyke/SecureCRT/Config/SecureCRT_eval.lic` дээр байгаа
- [ ] `~/.vandyke/SecureCRT/Config/`-руу `Sessions/`, `Commands/`, `Keywords/`, `Scripts/`, `Global.ini`, `ButtonBarV5.ini` symlink хийгдсэн (`ls -la` → `->` гарна)
- [ ] `~/OlympBackup/` фолдер үүссэн, write permission-той
- [ ] `Scripts/backup_configs.py`-г `Script → Run...`-ээр test хийсэн (1-2 tab дээр)
- [ ] Button Bar товчуудыг `.py`-руу re-target хийсэн (BACKUP/PUSH) ЭСВЭЛ Manual run-аар ашиглах гэж шийдсэн
- [ ] `pip3 install --user netmiko pyyaml` дууссан
- [ ] `~/net/scripts/eve_telnet.sh 32769` нь localhost-руу telnet амжилттай
- [ ] `~/net/scripts/netmiko_backup.py --host 127.0.0.1 --port <PORT> --name R1` тэст ажилласан
- [ ] VS Code-д `fabiospampinato.vscode-highlight`, `Anthropic.claude-code`, `auchenberg.vscode-browser-preview` суусан
- [ ] `cisco_highlights.jsonc` settings.json-д paste хийгдсэн, `OlympBackup/R1_*.cfg` дээр өнгө гарч байна
- [ ] `xdg-mime query default x-scheme-handler/telnet` → `securecrt-telnet.desktop` (EVE-NG Connect товч SecureCRT нээнэ)

### Repo & Tools (Windows alt-machine)
- [ ] `git clone` амжилттай (эсвэл USB fallback)
- [ ] SecureCRT Config folder-ыг repo-руу junction хийсэн
- [ ] `%USERPROFILE%\OlympBackup\` write permission-той
- [ ] `backup_configs.vbs`-ийг button bar-аас дарж 1-2 минутаар тэст
- [ ] EVE-NG-Win-Client-Pack суулгасан, `.reg`-ийг merge хийсэн
- [ ] Pod-ийн IP мэдсэний дараа `Sessions/`-д бүртгэх (`pod1/R1`, `pod1/SW1` гэх folder-аар)

### AI / Internet
- [ ] Wifi/wired интернет ажиллаж байгаа (speedtest эсвэл `ping 8.8.8.8`)
- [ ] **Claude Code VS Code extension** суулгасан (`Anthropic.claude-code`) болон login хийсэн
- [ ] **Claude Code CLI fallback** (`npx @anthropic-ai/claude-code`) — терминалаас ажиллахыг шалгасан
- [ ] **claude.ai веб login** — browser bookmark, ам нэвтэрсэн (нөөц)
- [ ] **chat.openai.com fallback** — нэвтэрсэн (хоёр дахь нөөц)
- [ ] `reference/lab-NN.pdf`, `reference/2024_round2/`, `reference/2025_round2/` нь offline backup-аар бэлэн
- [ ] AI prompt template (`reference/prompts.md`) уншиж сэргээсэн

## Don'ts

- **Live PSK / production credential** энэ repo-д commit хийхгүй — origin public. `untitled.key` болон `sonfig extracted.*`-г үзэхэд урьдчилан scrub.
- **SSH private key, VM password** — `id_ed25519` болон `vm-setup/REPORT.md`-ийг **хэзээ ч commit хийхгүй**. (2026-05-08 нэг удаа алдсан, `git filter-repo`-аар scrub хийсэн.) Шинэ credential нэмэх үед `git status` дээр давхар шалгана.
- `.vbs` script-ийг өөрчлөхгүй — `BACKUP_DIR` нь `%OLYMP_BACKUP_DIR%` (хэрэв тавьсан бол) → `%USERPROFILE%\OlympBackup\` (default) зам шийдвэрлэдэг. Олимпиадын машин өөр зам шаардвал env var-аар л дарж бич.
- `.py` script-уудыг (`backup_configs.py`, `push_config.py`) хэт сайжруулахаас зайлсхийнэ — `crt.Screen.WaitForString`-ийн timeout, prompt regex нь олимпиадын legacy IOS дээр хэлбэлзэлтэй. Манай pod-аас өөр device-той ажиллах гэж байгаа бол Python хувилбарыг fork хийж reuse, оригиналыг бүү засаарай.
- Linux SecureCRT-ийн **license файлыг** symlink-аар орлуулахгүй — жинхэнэ файл хэвээр үлдээх ёстой (репо доторх path-ийг symlink хийвэл лиценз ажиллахаа болино).
- `.eve_pods.conf`-ыг repo-д commit хийхгүй (per-machine port mapping, .gitignore-д аль хэдийн орсон).
- `OlympBackup/`-д үлдсэн May-7/8 test файлуудыг устгахгүй — реал run-ийн жишээ.
- `Global.ini` / `SCRTMenuToolbarV3.ini`-ийг **SecureCRT нээлттэй үед** засахгүй — нэрээ дарж бичнэ.
