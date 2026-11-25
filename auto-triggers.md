# AUTO-TRIGGERS — peta maksud → tool LENGKAP (ON-DEMAND, jangan inject)

Baca file ini saat tugas butuh tool spesifik. Sumber kanonik: `~/.agents/RULES.md`.
Prinsip: pahami maksud → pilih tool → jalan → verifikasi. Shell = 0 token prompt.
Legend: ✅ terinstall · 🔧 bisa install (`tool-install.py`/`brew`/`sk --repo`) · 📦 via skill.

## 1. Maksud → tool (umum)

| User bilang | Langsung pakai |
|---|---|
| commit, simpan | `git diff` → commit conventional |
| review, cek kode, bug? | baca diff → temuan + `file:baris` |
| test, uji, error? | test relevan → exit code · crash → repro→isolasi→fix→uji |
| plan, mau bikin X | rencana 3-7 langkah → eksekusi |
| refactor | perilaku-tetap + verifikasi |
| dokumen, README, manual | tulis/ubah dokumen |
| deploy, rilis, ship | pre-ship check → deploy |
| panas, lemot, baterai, RAM | `device-cool/scripts/check.sh` |
| ingat, catat, lupa | `memory-store add\|recall` · memory-graph |
| buka web, screenshot, cek URL | `browser-use-local/scripts/browse.py` · `dref <url>` |
| kirim/baca gambar/PDF | `baca-gambar/scripts/read.py` |
| UI, layout, "kayak situs X" | `DESIGN-PLAYBOOK.md` + `sk --design` + `dref` |
| logo, wordmark, favicon | `logo-studio/scripts/run.sh {build,proof,fonts}` |
| riset/dokumen panjang | `sk -l deep-research` |
| terjemahan/i18n | `sk "translate|i18n|localization|l10n"` |
| SEO/audit situs | `sk -l seo-audit` · `dcheck` |
| email/draft/nulis | `sk "email|copywriting|newsletter"` · `dcopy` |
| presentasi/pitch | `sk -l pptx` · DeckCraft · `sk "slides|presentation"` |
| kursus/tutorial/belajar | `sk "tutorial|course|explain|learn"` |
| brainstorm/ide | `sk "brainstorm|ideation|mindmap"` |
| keputusan/arsitektur | `sk "adr|architecture decision|system design"` |
| lemah/mental/stress | jawaban manusiawi, bukan tool |

## 2. Media & kreatif

`media-forge` ✅ 27 cmd: `probe video gif thumb concat enhance upscale bgremove
vectorize svg2png anim lottie manim audio tts music waveform stem 3d gen see find screen
transcribe tile format scan`

| Kebutuhan | Tool |
|---|---|
| foto/gambar AI dari teks | `media-forge gen` · fallback `sk -l image-generation`/`imagegen`/`imagen` |
| edit foto | `media-forge enhance\|upscale\|bgremove\|vectorize\|format\|tile` |
| tanya/lihat isi gambar | `media-forge see in.jpg "pertanyaan"` |
| cari aset | `media-forge find "kata" [--in dir]` |
| screenshot | `media-forge screen out.png` |
| video edit/gif/thumb | `media-forge video\|gif\|thumb\|concat` · AI: `sk -l ai-video-generation` |
| animasi | `media-forge anim\|lottie\|manim` |
| musik/lagu/backsound | `media-forge music` · `sk -l ai-music\|ai-music-album` |
| suara/tts/transkrip | `media-forge tts\|transcribe` · `whisper-talk-llama` ✅ |
| 3D/model/render | `media-forge 3d` · `blender -b -P` ✅(5.2.1) · `sk "blender\|3d\|unity\|unreal\|godot"` |
| foto RAW/edit pro | `sk "darktable|lightroom|raw photo|capture one"` 🔧 |
| podcast/audio pro | `sk "podcast|audio editing|reaper|audacity|pro tools"` · SoundCraft ✅ |
| streaming/overlay | `sk "obs|streaming|stream deck"` 🔧 |
| e-book/epub/mobi | `sk "epub|ebook|mobi|calibre"` 🔧 |
| font/ikon | `sk "font|icon|glyph|typography"` · `logo-studio` |
| mockup/placeholder | `sk "mockup|placeholder|dummy image|picsum"` |
| **ArtCraft** ✅13 app | PhotoCraft VectorCraft FilmCraft SoundCraft PdfCraft WordCraft DeckCraft GridCraft EffectCraft FigCraft LightCraft CADCraft DesignCraft — `sk -l artcraft-skills-*` (FilmCraft `--control port` JSON-lines) |
| ArtCraft belum ada | AniCraft TextureCraft MaterialCraft SolidCraft MailCraft — `sk` saja |

## 3. Dokumen, data & produktivitas

| Kebutuhan | Tool |
|---|---|
| Word/.docx | `sk -l docx\|wordcraft\|docx-manipulation` · WordCraft ✅ |
| Excel/.xlsx/.csv | `sk -l xlsx\|excel-automation\|xlsx-manipulation` · `uv run --with pandas` |
| PPT/.pptx | `sk -l pptx\|pptx-generator\|powerpoint` · DeckCraft ✅ |
| PDF (baca/merge/form/watermark/ocr) | `sk -l pdf` + varian · PdfCraft ✅ |
| LibreOffice | ✅ `/Applications/LibreOffice.app` · `soffice --headless --convert-to` |
| DB CLI | `sqlite3` `psql` `mysql` `redis-cli` ✅ |
| DB GUI | DBeaver ✅ · pgAdmin ✅ · Another Redis Desktop ✅ |
| JSON/YAML/TOML | `jq` `yq` ✅ · `sk "toml|hcl|jsonschema"` |
| CSV/data besar | `uv run --with pandas\|polars\|duckdb` |
| Spreadsheet AI | `sk "spreadsheet|excel ai|google sheets"` |
| Catatan/PKM | Obsidian ✅ `~/mamatXobsidian` · memory-graph |
| Mindmap/diagram | `sk "mermaid|excalidraw|diagram|flowchart"` |
| API docs (OpenAPI/Swagger) | `sk "openapi|swagger|redoc|api documentation"` |
| Invoice/receipt | `sk "invoice|receipt|billing"` |
| Kalender/scheduling | `sk "calendar|scheduling|cron|appointment"` |
| Email automation | `sk "email|smtp|imap|newsletter|mail merge"` |
| Presentasi web (reveal.js) | `sk "reveal.js|slidev|marp"` |

## 4. Coding & debugging

Runtime ✅ semua PATH: `python3` `uv` `node` `npm` `pnpm` `bun` `deno` `go` `cargo/rustc`
`java` `dotnet` `gcc` `clang` `cmake` `make` `lldb`.

| Kebutuhan | Tool |
|---|---|
| Scaffold | `project-forge new\|adopt\|verify\|gates` ✅ · `sk "scaffold|starter|boilerplate"` |
| Peta repo | `repo-map [DIR]` ✅ |
| Debug native | `lldb` ✅ · `-fsanitize=address,undefined` · `valgrind` 🔧 |
| Debug web | Playwright MCP · Chrome DevTools · `sk "debugging|breakpoint|profiling"` |
| Profiling perf | `sk "profiling|flamegraph|perf|py-spy|speedscope"` 🔧 |
| Fuzzing | `sk "fuzzing|afl|libfuzzer|cargo-fuzz|hypothesis"` |
| Coverage | `pytest --cov` · `go test -cover` · `cargo llvm-cov` · `sk "coverage"` |
| Refactor massal | `sk -l refactor` · ast-grep MCP (`pow mcp on ast-grep`) |
| Review kode | `sk -l code-review` · domain skills (golang/react/python/vue/ts patterns) |
| Test all kinds | `testing-forge` ✅ + `TESTING.md` 13 lapisan |
| Git/GitHub | `gh` ✅ · GitHub Desktop ✅ · Sourcetree ✅ |
| IDE | VS Code ✅ PyCharm ✅ Xcode ✅ Trae ✅ Kiro ✅ |
| Terminal | iTerm ✅ kitty ✅ Warp ✅ tmux ✅ `btop`/`htop` ✅ `zoxide` `fzf` `bat` `eza` `fd` `rg` ✅ |
| Shell config | `sk "shell|zsh|bash|dotfiles|starship|oh-my-zsh"` |
| Dependency audit | `security-forge deps` · `npm audit` `cargo audit` `sk -l dependency-audit` |
| API docs | `sk -l documentation-lookup` · Context7 · `web-search` |
| Monorepo | `sk "monorepo|nx|turborepo|lerna|bazel|moon"` |
| Code search AI | `codebase-memory` MCP (`pow mcp on`) · `ast-grep` |
| Pair/agent code | Devin/Claude/CodeBuddy/Cline/Kiro/Trae ✅ semua terinstall |

### Per bahasa
- **Python**: `uv` `pytest` `ruff`? `mypy`? · `sk "python|django|fastapi|flask|pandas|numpy"`
- **JS/TS**: node ecosystem · `sk "typescript|react|next|vue|svelte|node"` + pattern skills ✅
- **Go**: `go` ✅ · `sk "golang|go patterns"` · `golangci-lint` 🔧
- **Rust**: `cargo` ✅ · `sk "rust|cargo|clippy"` · `cargo-watch` 🔧
- **Java/JVM**: `java javac` ✅ · `sk "java|kotlin|spring|gradle|maven"` · DBeaver ✅
- **.NET**: `dotnet` ✅ · `sk "dotnet|csharp|asp.net|blazor"`
- **C/C++**: `gcc clang cmake` ✅ · `sk "cpp|embedded|arduino|raspberry pi"`
- **Mobile**: `sk "react native|flutter|swift|kotlin android|ios"` · Xcode ✅
- **Game**: `sk "unity|unreal|godot|game dev|phaser"` 🔧
- **WASM/webassembly**: `sk "wasm|webassembly|emscripten|rust wasm"`
- **Smart contract**: `sk "solidity|web3|ethereum|smart contract|foundry|hardhat"` ⚠️ audit only

## 5. AI/ML ops (RAG, fine-tune, local model, GGUF, agent)

| Kebutuhan | Tool/cara |
|---|---|
| RAG/retrieval | `sk "rag|retrieval|vector database|embedding|chromadb|qdrant|pinecone|weaviate"` · `mcp-router retrieve` |
| Fine-tune LoRA/QLoRA | `sk "fine-tune|lora|qlora|axolotl|unsloth|peft|trl"` · butuh GPU/cloud |
| GGUF/llama.cpp | `sk "gguf|llama.cpp|llamafile"` · `brew install llama.cpp` 🔧 |
| Ollama/local LLM | 🔧 `brew install ollama` · API `localhost:11434` · `sk "ollama"` |
| Quantization | `sk "quantization|awq|gptq|fp8|int8|gguf|bitsandbytes"` |
| Serving vLLM/TGI | `sk "vllm|tgi|llm serving|inference|triton|onnx"` |
| Embedding | `sk "embedding|sentence-transformers|bge|e5|openai embeddings"` |
| Whisper/STT | `media-forge transcribe` ✅ · `whisper-talk-llama` ✅ · `sk "whisper|stt|speech"` |
| Image-gen lokal | `sk "stable diffusion|comfyui|fooocus|sdxl|flux|controlnet|lora image"` |
| Video-gen AI | `sk "video generation|runway|pika|kling|sora|veo|wan"` |
| AI agent build | `sk "ai agent|langchain|llamaindex|crewai|autogen|semantic kernel|mcp"` · `mcp-builder` |
| MCP server bikin | `sk -l mcp-builder` |
| Prompt engineering | `sk -l prompt-engineering` |
| Eval/model bench | `sk "llm eval|benchmark|lm-eval|deepeval|ragas"` |
| Multimodal/VLM | `sk "vision language|vlm|llava|qwen-vl|gemini vision"` |
| Guardrail/safety | `sk "llm guardrail|jailbreak|prompt injection defense|neMo"` |
| Cost/latency opt | `sk "llm cost|token optimization|prompt caching|quantization"` |
| Neural net train | `sk "pytorch|tensorflow|jax|training|distributed training"` |
| Data labeling | `sk "data labeling|annotation|label studio|snorkel"` |
| Synthetic data | `sk "synthetic data|data generation|augly|nlpaug"` |

## 5b. Repo komunitas TRENDING (baru di-clone → `~/.agents/repo-refs/`, semua sudah di-scan)

**Trading/finance:**
- `openbyteinc/quantdinger` ⭐13k — Agentic Trading OS self-hosted (AI research + Python backtest)
- `marketcalls/openalgo` ⭐3k — ekosistem trading open-source + 7 skill OpenAlgo ter-ingest
- `lumiwealth/lumibot` ⭐2k — framework trading Python + AI agents (backtest→live)
- `chrisleekr/binance-trading-bot` ⭐5k — bot Binance, strategi pluggable + backtest
- `atilaahmettaner/tradingview-mcp` ⭐5k — MCP server analisis market (screener, multi-TF)
  → `pow mcp on tradingview` bila perlu
- `jakeschincariol/day-trader-skill` ⭐9k — 11 skill day-trading (scan chart, berita)
- `lzwme/finance-quant-skills` — skill kuant A-share (akshare/bt/jaqs)
- `superior-trade/superior-skills` — skill backtest/deploy Superior Trade
- Skill backtest lain: `trading-strategy-backtest` `backtest-expert` `backtest-report-generator`

**Security/bug bounty:**
- `mukul975/anthropic-cybersecurity-skills` ⭐35k — **202 skill cybersec** ter-ingest
  (mitre, detection, ir, cloud, forensik — cari `sk "<topik>"`)
- `awarexone/agentic-bug-hunter` ⭐5k — toolkit bug bounty + 12 skill (omni-killchain dll)
- `baarai/artex` + `jiwoochris/artex-global` ⭐16k/4k — AI autonomous pentest multi-agent
- `edoardottt/awesome-hacker-search-engines` ⭐11k — list search engine untuk recon

**AI/RAG/agent:**
- `k-dense-ai/scientific-agent-skills` ⭐56k — **151 skill** riset ilmiah (paper, grant, lab)
- `nirdiamant/rag_techniques` ⭐30k — 30+ teknik RAG dengan kode
- `labring/fastgpt` ⭐30k — platform RAG/knowledge base self-hosted (+9 skill)
- `quantumnous/new-api` ⭐51k — AI gateway self-hosted (OpenAI/Claude/Gemini compatible)
- `bojieli/ai-agent-book` ⭐57k — buku+kode "AI Agent dari nol" (+12 skill)
- `janestreet/agent_skills` ⭐10k — skill internal Jane Street
- `browser-use/jev-ultrafast` ⭐24k — web agent tercepat/termurah (alternatif browser-use)

**Belajar/devops/konten:**
- `snailclimb/javaguide` ⭐159k — panduan Java/interview backend paling lengkap
- `michaelcade/90daysofdevops` ⭐30k — kurikulum DevOps 90 hari
- `skyzh/vector-db-from-scratch` ⭐813 — bangun vector DB dari nol (Rust)
- `enescingoz/awesome-n8n-templates` ⭐26k — 280+ template otomasi n8n gratis
- `evil0ctal/douyin_tiktok_download_api` ⭐21k — API download TikTok/Douyin + MCP + transkrip

Cara pakai repo-refs: baca `README`/docs di path → butuh kode → sudah ter-clone.
Tool yang butuh install/deps: baca docs repo dulu, install di venv/`tool-install.py`.
Hasil scan: semua 21 repo di-scan; critical hanya di pola wajar security-tooling/docs
(powershell-encoded di skill deteksi malware, install.sh pipe di artex-global, docs
exfil-endpoint di openalgo). `ingest` auto-blokir skill berbahaya: 44 diblokir, 431 lolos.
Jangan run script arbitrary dari repo ini tanpa baca dulu.

## 5c. Repo komunitas GELOMBANG 2 (semua di `~/.agents/repo-refs/`, sudah scan+ingest)

**Math/simbolik & data:** `morluto/jacobian` (math tools agent) · `xbp-europe/sagemath-mcp`
(SageMath MCP 40 tools) · `deepgraphlearning/graphvite` (graph embedding) ·
`siconos/siconos` (simulasi sistem nonsmooth) · `abdiraimov-otabek/dashboard-design-skill`
(desain dashboard KPI/BI).

**OSINT/security lanjut:** `openosint/openosint` (OSINT toolkit agent: skill+MCP+CLI,
passive) · `duty1g/x64dbg-mcp-server` (debugging binary via MCP) ·
`morluto/awesome-reverse-engineering` (katalog RE) · `cyb3rmx/qu1cksc0pe` (all-in-one
malware analysis) · `assafkip/investigators-copilot` (6 skill: case mgmt, OSINT).

**3D/CAD/percetakan:** `el4cteo/blender-skills` (**24 skill** workflow Blender 5.3) ·
`earthtojake/text-to-cad` ⭐26k (8 skill, text→CAD) · `tangency-labs/solidcraft` ⭐15k
(parametric CAD Rust, 8 skill) · `adam-cad/cadam` · `kai-jungsthoefel/soma` (CadQuery
parametric) · `timschmidt/synaps-cad` (CAD IDE) · `leandrodaf/3d-new-era-ai` (floor plan editor).

**Musik/audio:** `nota-daw/nota` (**19 skill**, DAW gratis) · `conceptual-machines/magda-core`
(**19 skill**, ecosystem produksi musik) · `monglong0214/logic-pro-mcp` (kontrol Logic Pro).

**Video/motion/VFX:** `kajisho5/ffmpeg-skill` (**5 skill**, 42 tool FFmpeg untuk agent) ·
`juneyaooo/rea-video` ⭐12k (reverse-engineer video shot-by-shot) · `shinyobjectz/raea` ⭐4k
(render engine utk agent) · `patch-gg/pixelfx` ⭐9k (244 efek pixel art) · `voyager-so/vork`
(headless 3D/VFX) · `tumourlove/monolith` (MCP Unreal Engine) · `xuliang2024/cutcli-cookbook`
(CapCut/Jianying templates) · `oil-oil/oil-subtitle` (transkrip+burn subtitle) ·
`alchaincyf/huashu-art-motion` (animasi 35 gaya).

**Buku/riset/referensi:** `pdfmathtranslate/pdfmathtranslate` ⭐38k (terjemah PDF paper,
format utuh) · `54yyyu/zotero-mcp` ⭐6k · `yilewang/llm-for-zotero` · `codedogqby/readany`
(ebook reader + RAG chat) · `heartleo/zlib` (Z-Library CLI) · `edwardxlai/easyread` (paper→Tionghoa)
· `docsagent/docsagent` (knowledge base personal utk agent) · `federicodeponte/opendraft`
(tulis paper + sitasi verified) · `faust-donf/beamer-academic` (PPT defense dari tesis).

**Patent/legal:** `r14dd/patent` (prior-art search utk ide kode) ·
`robthepcguy/claude-patent-creator` (**7 skill**, USPTO + RAG) · `lexifina/global-law` ⭐2k
(hukum dunia di git) · `open-source-legal/opencontracts` · `lawve-ai/awesome-legal-skills`
(**86 skill** legal!) — ⚠️ bukan nasihat hukum.

**Akuntansi/keuangan/bisnis:** `tnt-likely/beecount` (**6 skill**, bookkeeping lokal) ·
`ryanduguid/australian-accounting-skills` (**28 skill**, pajak AU) ·
`hany202507/finance-ai-skills` (skill akuntansi Korea) · `dubbl-org/dubbl` (alternatif
Xero/QuickBooks) · `keptinventory/kept` (inventory barang) · `xjli360/sealeap-amazon-skills`
 riset+listing Amazon · `guangshu100/bidmaster-pro` (tender/penawaran otomatis) ·
`superjack2050/1688-cli` (sourcing 1688 utk agent).

**Properti/HR/karir:** `haydenschmitty/floorplan` ⭐6k (peta arsitektur app) ·
`tae0y/real-estate-mcp` (harga apartemen KR via MCP) · `tuanductran/hr-skills` (**16 skill** HR)
· `polar-bear-org/claude-skills` (**21 skill**) · `ai-job-search-dev/ai-job-search` ⭐70k
(cari kerja otomatis) · `career-ops-hq/career-ops` ⭐81k.

**Agent infra/konten:** `inkeep/agents` (no-code agent builder) · `lee-to/ai-factory` (**9 skill**)
· `alikon-art/determinflow` (**6 skill**, ⚠️ scan critical reverse-shell di validation.py —
hati-hati) · `codespar/mcp-dev-latam` (MCP commerce LatAm) · `cargofy/atlas` (MCP logistik
TMS/WMS) · `pnoker/iot-dc3` (IoT runtime) · `alireza787b/mavsdk_drone_show` (armada drone
PX4, ⚠️ 5 critical docs) · `w1ne/labwired-core` (simulator firmware MCU, ⚠️ 4 critical)
· `huangjunsen0406/py-xiaozhi` (ekosistem asisten AI+MCP) · `beihaili/get-started-with-web3`
(kurikulum web3) · `caiovicentino/polymarket-mcp-server` ( trading prediksi via MCP) ·
`openfilm/openfilm` ⭐9k (4 skill, agent→video) · `yihui-dev/awesome-opus5-5-videos` ⭐16k
(koleksi video viral + prompt) · `alchaincyf/deepseek-harness-orange-book`.

## 6. Security & hacking (DEFENSIF — target berizin)

**Forges ✅:** `security-forge audit|secret|sast|deps|image|docker|shell|headers|tls|report`
**Bins ✅:** `nmap` `httpx` `nuclei` `tshark` `exiftool` `binwalk` `gitleaks` `semgrep` `trivy` `gh` `docker`

| Kebutuhan | Cara |
|---|---|
| OSINT orang/domain | `sk "osint|recon|sherlock|theharvester|maigret|spiderfoot"` + `exiftool`/`httpx` |
| Bug bounty | `sk "bug bounty|vulnerability|cve|exploit dev|payload"` — scope wajib |
| Web vuln | `nuclei` `httpx` · `sk "owasp|xss|sqli|ssrf|csrf|jwt|oauth"` |
| Network forensik | `tshark` `nmap` `binwalk` `exiftool` · `sk "forensics|pcap|memory forensics|volatility"` |
| Binary/reverse | `sk "malware|reverse engineering|ghidra|radare|cutter|ida|binary ninja"` 🔧 |
| Cloud sec | `sk "cloud security|aws security|gcp|azure|kubernetes security|kubesec"` |
| Container sec | `trivy image` ✅ · `sk "docker security|container escape|supply chain"` |
| Secrets/cred | `gitleaks` `trufflehog` 🔧 · `sk "secrets management|vault|doppler|1password"` |
| Pentest install | `tool-install.py`/`brew`/`sk --repo` — JANGAN scan tanpa izin |
| CTF/lab | `sk "ctf|hackthebox|tryhackme|pentest lab"` |
| Compliance | `sk "gdpr|hipaa|soc2|pci|compliance|audit"` |

⚠️ Batas keras: audit sistem sendiri, lab/CTF, target berizin tertulis. Scan/exfil/serang
tanpa izin = tolak & jelaskan.

## 7. Server, infra, DevOps & jaringan

**✅:** `docker` OrbStack `kubectl` `helm` `terraform` `ansible` `gh` `tmux` `btop` `ssh` `rsync`
**Apps ✅:** Tailscale ZeroTier Proxyman AnyDesk Royal TSX DBeaver

| Kebutuhan | Tool |
|---|---|
| Container | `docker`/`orb` · `sk "docker|kubernetes|k8s|containerd|podman"` |
| K8s advanced | `sk "kubernetes|helm|kustomize|istio|argocd|flux|service mesh"` |
| IaC | `terraform` `ansible` · `sk "pulumi|cdk|crossplane|opentofu"` |
| CI/CD | `gh` actions · `sk "ci/cd|github actions|gitlab ci|jenkins|drone|woodpecker|buildkite|circleci"` |
| GitOps | `sk "gitops|argocd|flux|flagger"` |
| VPN/remote | Tailscale ✅ ZeroTier ✅ AnyDesk ✅ Royal TSX ✅ · `sk "wireguard|tailscale|headscale"` |
| HTTP debug | Proxyman ✅ · `curl -v` `httpx` · `sk "mitmproxy|charles|fiddler|wireshark"` |
| Monitoring | `btop` ✅ · `sk "prometheus|grafana|datadog|newrelic|sentry|opentelemetry|jaeger|loki"` |
| Logging | `sk "logging|loki|fluentd|vector|papertrail|graylog"` |
| SSH/server | `ssh` `rsync` `scp` · `sk "ssh|server hardening|linux admin|sysadmin|ansible"` |
| DNS/domain | `dig` `whois` · `sk "dns|domain|cloudflare|route53|dnssec"` |
| Email server | `sk "mail server|postfix|mailcow|stalwart|maddy"` |
| Home server | `sk "home server|nas|proxmox|trueNAS|unraid|homelab"` |
| Backup | `sk "backup|restic|borg|duplicati|rclone|snapshots"` |
| Secrets infra | `sk "vault|secrets|sops|age|infisical|doppler"` |
| Load balancer | `sk "nginx|caddy|traefik|haproxy|envoy|load balancer"` |
| Message queue | `sk "kafka|rabbitmq|nats|redis queue|sqs|pubsub|celery"` |
| Cache | `redis-cli` ✅ · `sk "redis|memcached|dragonfly|keydb"` |
| Search engine | `sk "elasticsearch|opensearch|meilisearch|typesense|solr|algolia"` |
| DB server | `psql` `mysql` ✅ · `sk "postgres|mysql|mongodb|clickhouse|duckdb|supabase|firebase|planetscale"` |
| Feature flags | `sk "feature flag|launchdarkly|unleash|flagsmith"` |
| Chaos eng | `sk "chaos engineering|gremlin|litmus|chaos monkey"` |

## 8. Web, browser & API

| Kebutuhan | Tool |
|---|---|
| Test/screenshot web | `playwright-mcp` (`pow mcp on`) · `browser-use-local` ✅ |
| Design ukur | `dref` `dcheck` `dvisual` `dcopy` ✅ |
| Scraping/crawl | `sk "scraping|crawl|firecrawl|playwright|puppeteer|selenium|beautifulsoup"` · `internet-asset-fetcher` |
| API test | `curl` ✅ · `sk "api testing|schemathesis|postman|bruno|insomnia|httpie|rest client"` · `testing-forge tests-api` |
| API design | `sk -l api-design-principles` · `sk "graphql|grpc|openapi|protobuf"` |
| Web perf | `sk "web performance|lighthouse|core web vitals|pagespeed"` |
| A11y | `sk -l accessibility` · `dcheck` axe · `sk "wcag|a11y|screen reader"` |
| Browser ext | `sk "chrome extension|firefox extension|webextension"` |
| PWA/offline | `sk "pwa|service worker|offline first|workbox"` |
| SEO | `sk -l seo-audit` · `sk "seo|schema.org|sitemap|og image|meta"` |
| i18n web | `sk "i18n|internationalization|locale|translation"` |
| E-commerce | `sk "shopify|woocommerce|stripe|payment|checkout|cart"` |
| Auth/websec | `sk "oauth|jwt|session|csrf|authentication|authorization|rbac"` |

## 9. Data engineering & analytics

| Kebutuhan | Tool |
|---|---|
| ETL/ELT | `sk "etl|elt|airflow|dagster|prefect|dbt|fivetran|airbyte"` |
| Data warehouse | `sk "snowflake|bigquery|redshift|databricks|clickhouse|duckdb"` |
| Streaming data | `sk "kafka|flink|spark streaming|kinesis|pulsar"` |
| Notebook | `sk "jupyter|notebook|observable|hex|deepnote"` · `uv run jupyter` |
| Dashboard/BI'da | `sk "metabase|superset|grafana|looker|tableau|powerbi|streamlit|dash"` |
| Spreadsheet/report | `sk "report|dashboard|data viz|matplotlib|seaborn|plotly"` ✅ skills |
| Data eng | `sk "data engineering|pipeline|orchestration|spark|hadoop|beam"` |
| Geo/spatial | `sk "gis|geospatial|qgis|postgis|leaflet|mapbox|geojson"` |
| Time series | `sk "timeseries|influxdb|timescaledb|questdb|prometheus"` |
| OCR/doc AI | `sk "ocr|document ai|textract|tesseract|layoutlm"` · `baca-gambar` ✅ |

## 10. AI agent & automation lanjut

| Kebutuhan | Tool |
|---|---|
| Browser agent | `browser-use-local` ✅ · `playwright-mcp` |
| Computer use | `sk "computer use|desktop automation|pyautogui|cliclick"` |
| RPA/workflow | `sk "rpa|workflow automation|n8n|make|zapier|activepieces|windmill"` |
| Chatbot | `sk "chatbot|rag chatbot|voice assistant|whatsapp bot|telegram bot"` |
| Cron/schedule | `hermes cron` ✅ · `sk "cron|scheduler|job queue|bullmq|celery"` |
| Webhook | `sk "webhook|callback|event-driven|sqs|pubsub"` |
| Form/survey | `sk "form|survey|typeform|google forms|tally"` |
| Scraping+AI | `sk "scraping|crawl4ai|firecrawl|jina reader|tavily|exa"` |
| Meeting notes | `sk -l meeting-notes` · `sk "transcription|otter|fireflies|meet"` |
| Email triage | `sk "email automation|gmail|outlook|imap|ai email"` |
| Calendar AI | `sk "calendar|scheduling|cal.com|calendly|cron"` |
| Smart home | `sk "home assistant|smart home|mqtt|homekit|matter"` |
| IoT/embedded | `sk "arduino|esp32|raspberry pi|microcontroller|firmware|mqtt"` |
| 3D printing | `sk "3d printing|prusa|cura|klipper|octoprint|fusion360|onshape"` 🔧 |
| CNC/laser | `sk "cnc|laser cutting|silhouette|glowforge|mach3"` 🔧 |
| Drone | `sk "drone|dji|mavlink|ardupilot|pixhawk"` |
| Robotics | `sk "robotics|ros|ros2|moveit|gazebo"` |

## 11. Bisnis, marketing & konten

| Kebutuhan | Tool |
|---|---|
| Copywriting | `sk "copywriting|copy edit|headline|ad copy|landing page"` · `dcopy` |
| Social media | `sk -l social-content` · `sk "linkedin|twitter|instagram|tiktok|content calendar"` |
| SEO content | `sk -l seo-audit` · `sk "seo content|keyword research|ahrefs|semrush"` |
| Brand/voice | `sk -l brand-voice` |
| Humanizer | `sk -l avoid-ai-writing\|content-humanizer` |
| Image brand | `sk "brand kit|logo|brand guidelines|style guide"` |
| Pitch deck | `sk -l pptx` · DeckCraft · `sk "pitch deck|investor deck"` |
| Resume/CV | `sk "resume|cv|cover letter|linkedin profile"` |
| Legal docs | `sk "contract|terms|privacy policy|legal|nda"` ⚠️ bukan nasihat hukum |
| Invoice/billing | `sk "invoice|stripe|payment|subscription|billing"` |
| CRM | `sk "crm|hubspot|salesforce|pipedrive|attio|twenty"` |
| Analytics | `sk "analytics|plausible|umami|posthog|mixpanel|amplitude|ga4"` |
| A/B test | `sk "ab test|experimentation|feature flag|split test"` |
| Ads | `sk "google ads|meta ads|advertising|campaign"` |
| Marketplace | `sk "etsy|shopee|tokopedia|lazada|amazon seller"` |
| Real estate | `sk "real estate|property|listing|mls"` |
| Job/recruiting | `sk "recruiting|job description|interview|ats|linkedin hiring"` |

## 12. Niche & lainnya

| Kebutuhan | Tool |
|---|---|
| Music theory/DAW | `sk "music theory|ableton|logic|fl studio|pro tools|reaper|midi"` 🔧 |
| Podcast produksi | `sk "podcast|audacity|reaper|descript|riverside|anchor"` |
| Photography | `sk "photography|exif|raw|darktable|lightroom|capture one"` 🔧 |
| Video pro edit | FilmCraft ✅ · `sk "premiere|after effects|davinci|final cut|resolve|fusion"` 🔧 |
| Color grading | `sk "color grading|lut|davinci|resolve|colour science"` |
| Subtitle | `media-forge` ffmpeg `--sub` · `sk "subtitle|srt|vtt|caption"` |
| Print/packaging | `sk "print design|packaging|label|sticker|business card"` · PdfCraft |
| Font custom | `sk "font|typeface|fontforge|glyphs|variable font"` 🔧 |
| Accessibility | `sk -l accessibility` · `dcheck` · `sk "wcag|a11y|aria|screen reader"` |
| Crypto/web3 | `sk "bitcoin|ethereum|web3|wallet|nft|defi"` ⚠️ security only |
| Forex/trading | `sk "trading|forex|stock|crypto trading|backtest|quant"` |
| Academic/research | `sk "academic|paper|citation|literature review|zotero|latex"` ✅ deep-research |
| LaTeX | `sk "latex|tex|beamer|thesis|overleaf"` 🔧 |
| Patent/prior art | `sk "patent|prior art|invention|trademark"` |
| Bio/informatics | `sk "bioinformatics|genomics|protein|chemistry|lab"` |
| Medical/health | `sk "medical|health|fhir|hl7|clinical"` ⚠️ bukan nasihat medis |
| Legal/e-discovery | `sk "legal|ediscovery|contract review|compliance"` ⚠️ bukan nasihat hukum |
| Gaming/mod | `sk "game mod|minecraft|roblox|unity mod|skyrim"` |
| Vintage/retro | `sk "retro|emulation|retroarch|dosbox|amiga|c64"` 🔧 |
| Board game/D&D | `sk "dnd|tabletop|board game|rpg|miniature"` |
| Language learning | `sk "language learning|vocab|anki|spaced repetition"` |
| Cooking/recipe | `sk "recipe|cooking|meal plan|nutrition"` |
| Travel | `sk "travel|itinerary|flight|hotel|visa"` |
| Event planning | `sk "event|conference|wedding|party planning"` |
| Nonprofit/NGO | `sk "nonprofit|ngo|grant|donation|fundraising"` |
| Government/civic | `sk "government|civic|permit|zoning|public records"` |
| Faith/spiritual | `sk "bible|quran|torah|meditation|journal|gratitude"` |
| Pet/parenting | `sk "parenting|baby|pet|dog|cat|family"` |
| Auto/vehicle | `sk "car|vehicle|obd|maintenance|ev|charging"` |
| Home improvement | `sk "home|diy|renovation|interior|garden|landscaping"` |
| Fashion/style | `sk "fashion|outfit|style|wardrobe|beauty"` |
| Sports/fitness | `sk "fitness|workout|nutrition|running|yoga|sports"` |
| Mental health | `sk "mental health|therapy|journal|mindfulness|cbt"` — dukung, bukan diagnosis |
| Finance pribadi | `sk "budget|expense|investment|tax|accounting|invoice"` ⚠️ bukan nasihat finansial |
| Insurance | `sk "insurance|claim|policy|coverage"` |
| Immigration | `sk "visa|immigration|passport|citizenship|relocation"` |
| Wedding | `sk "wedding|engagement|anniversary|honeymoon"` |
| Baby/parenting | `sk "baby|newborn|toddler|parenting|sleep training"` |
| Pet care | `sk "dog|cat|pet|veterinary|aquarium|bird"` |
| Gardening | `sk "garden|plants|compost|hydroponic|indoor garden"` |
| Craft/hobby | `sk "knitting|crochet|woodworking|leather|candle|soap"` |
| Collectibles | `sk "collectible|card|coin|stamp|antique|memorabilia"` |
| Cars/vehicles | `sk "car|vehicle|obd|carplay|tesla|ev|motorcycle"` |
| Aviation | `sk "aviation|pilot|flight sim|drone|aircraft"` |
| Maritime | `sk "sailing|boat|maritime|navigation|fish"` |
| E-sports/gaming | `sk "esports|gaming|twitch|stream|overlay|emote"` |
| Music production | `sk "music production|mixing|mastering|daw|vst|midi"` 🔧 |
| Podcast | `sk "podcast|audio editing|descript|riverside|anchor|spotify"` |
| Newsletter | `sk "newsletter|substack|beehiiv|convertkit|email marketing"` |
| Course creation | `sk "course|udemy|skillshare|teach|curriculum|lesson plan"` |
| Book writing | `sk "book|novel|fiction|nonfiction|kindle|amazon kdp| Wattpad"` |
| Fan fiction | `sk "fanfic|fan fiction|roleplay|rp|character"` |
| Roleplay | `sk "roleplay|rp|character ai|persona|scenario"` |
| Tarot/astrology | `sk "tarot|astrology|horoscope|zodiac|birth chart"` |
| Dream interpretation | `sk "dream|dream journal|lucid dreaming|sleep"` |
| Therapy/journal | `sk "therapy|journal|mental health|cbt|mindfulness|gratitude"` |
| Support groups | `sk "support group|community|forum|discord server|moderation"` |

## 13. Belum terinstall? Install dulu

Urutan: `sk --repo "<kebutuhan>"` → `repo-hub.py get <owner/name>` → `tool-install.py <owner/name>`
(→ `~/.agents/bin`, auto PATH) → `brew install <pkg>` / app store / `npm i -g` / `cargo install` / `go install`.
Jangan klaim "tidak bisa" sebelum cek `which` + `/Applications` + `sk` + repo + web.
