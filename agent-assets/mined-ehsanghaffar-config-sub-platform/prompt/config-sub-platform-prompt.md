You are a senior backend and infrastructure engineer.

Build a production-grade V2Ray/VLESS/Trojan/ShadowSocks subscription aggregator platform using Python.

The goal is NOT to build a giant config dump repository.
The goal is to build a CURATED, lightweight, high-quality subscription generator.

The system must:
- Collect configs from public Telegram channels
- Collect configs from GitHub repositories and raw URLs
- Parse and normalize configs
- Deduplicate intelligently
- Score and rank configs
- Generate categorized lightweight subscriptions
- Publish subscriptions automatically every 10 minutes

====================================================
PROJECT GOALS
====================================================

Main goals:

1. Lightweight outputs
   Avoid massive subscription files.
   Output only high-quality configs.

2. Curated subscriptions
   Publish only the best configs.

3. Multiple categorized outputs
   Example:
   - mix
   - cloudflare-only
   - reality-only
   - mobile-friendly
   - fast
   - clean

4. Stable architecture
   Async, modular, scalable.

5. Easy deployment
   Support:
   - GitHub Actions
   - VPS cron jobs
   - Docker

====================================================
TECH STACK
====================================================

Use:

- Python 3.11+
- asyncio
- httpx
- telethon
- pydantic
- orjson
- uvloop (optional)
- PyYAML

Do NOT use:
- synchronous requests
- monolithic code
- unnecessary databases

====================================================
ARCHITECTURE
====================================================

Design modular architecture:

project/
│
├── app/
│   ├── collectors/
│   │   ├── telegram.py
│   │   ├── github.py
│   │   └── subscriptions.py
│   │
│   ├── extractors/
│   │   └── links.py
│   │
│   ├── parsers/
│   │   ├── vmess.py
│   │   ├── vless.py
│   │   ├── trojan.py
│   │   └── shadowsocks.py
│   │
│   ├── normalizers/
│   │   └── normalize.py
│   │
│   ├── scoring/
│   │   └── engine.py
│   │
│   ├── filters/
│   │   ├── cloudflare.py
│   │   ├── reality.py
│   │   ├── mobile.py
│   │   ├── fast.py
│   │   └── clean.py
│   │
│   ├── health/
│   │   └── checker.py
│   │
│   ├── outputs/
│   │   ├── generator.py
│   │   ├── base64.py
│   │   └── clash.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── retry.py
│   │   └── cache.py
│   │
│   └── models/
│       └── config.py
│
├── config/
│   ├── telegram_channels.txt
│   ├── github_sources.json
│   ├── subscription_sources.txt
│   └── settings.yaml
│
├── generated/
│   ├── mix.txt
│   ├── cloudflare.txt
│   ├── reality.txt
│   ├── mobile.txt
│   ├── fast.txt
│   ├── clean.txt
│   └── base64/
│
├── cache/
├── tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── .env.example
└── main.py

====================================================
CONFIG TYPES
====================================================

Support parsing:

- vmess://
- vless://
- trojan://
- ss://

====================================================
TELEGRAM COLLECTION
====================================================

Use Telethon.

Requirements:

- Read public Telegram channels
- Async message fetching
- Parse recent messages
- Extract config links from messages
- Handle Telegram rate limits
- Use retry logic
- Use environment variables:
  - TG_API_ID
  - TG_API_HASH
  - TG_SESSION

Create:

config/telegram_channels.txt

Example:

@freev2ray
@proxy_channel
@config_collector

====================================================
GITHUB COLLECTION
====================================================

Collect from:

- raw GitHub URLs
- GitHub repositories
- subscription text files

Create:

config/github_sources.json

Format:

[
  {
    "name": "source1",
    "url": "https://raw.githubusercontent.com/...",
    "type": "raw"
  }
]

Requirements:

- async downloads
- timeout handling
- retry handling
- cache responses

====================================================
SUBSCRIPTION URL COLLECTION
====================================================

Support collecting from existing subscription URLs.

Create:

config/subscription_sources.txt

Requirements:

- auto detect base64 subscriptions
- decode automatically
- extract configs

====================================================
EXTRACTION
====================================================

Extract links using regex.

Supported patterns:

- vmess://
- vless://
- trojan://
- ss://

Handle malformed inputs safely.

====================================================
NORMALIZATION
====================================================

Normalize all configs.

Requirements:

- trim whitespace
- fix malformed URLs
- decode vmess JSON
- validate required fields
- standardize transport names
- normalize security values
- normalize hostnames

====================================================
PYDANTIC MODEL
====================================================

Create a unified config model.

Fields:

- protocol
- host
- port
- uuid
- password
- security
- transport
- tls
- sni
- path
- network
- fp
- reality
- source
- raw
- score

====================================================
DEDUPLICATION
====================================================

Do NOT deduplicate using raw string compare.

Deduplicate using:

- protocol
- host
- port
- uuid/password
- transport
- security

Generate stable hash.

====================================================
SCORING ENGINE
====================================================

Implement scoring system.

Example scoring:

+25 => Reality
+20 => Cloudflare CDN
+15 => TLS enabled
+10 => clean hostname
+10 => ws transport
+8  => grpc transport
+5  => IPv4 valid
+5  => low latency
-10 => suspicious port
-10 => duplicate hostname spam
-20 => malformed params
-100 => failed health check

Configs with higher score should be prioritized.

====================================================
CLOUDFLARE DETECTION
====================================================

Detect Cloudflare-based configs.

Methods:

- known Cloudflare IP ranges
- Cloudflare domains
- CDN indicators
- ws + tls patterns

====================================================
REALITY DETECTION
====================================================

Detect:

- reality
- xtls
- vision

====================================================
HEALTH CHECKS
====================================================

Implement async health checks.

Requirements:

- async TCP connect
- configurable timeout
- optional TLS handshake
- lightweight checks only
- avoid long blocking operations

Health checks must NOT slow down the whole pipeline.

====================================================
FILTERS
====================================================

Implement categorized filters.

====================================================
1. MIX FILTER
====================================================

Best overall configs.

Limit:
- maximum 300 configs

====================================================
2. CLOUDFLARE FILTER
====================================================

Only:
- Cloudflare CDN
- ws/grpc
- tls

Limit:
- maximum 150 configs

====================================================
3. REALITY FILTER
====================================================

Only:
- reality
- xtls
- vision

Limit:
- maximum 100 configs

====================================================
4. MOBILE FILTER
====================================================

Prioritize:
- lightweight configs
- ws
- tls
- cloudflare
- stable latency

====================================================
5. FAST FILTER
====================================================

Sort by:
- lowest latency
- successful checks

====================================================
6. CLEAN FILTER
====================================================

Only configs with:
- readable hostnames
- valid params
- stable checks
- no garbage fields

====================================================
OUTPUT GENERATION
====================================================

Generate:

- raw txt subscriptions
- base64 subscriptions
- optional Clash YAML

Output directory:

generated/

Examples:

- generated/mix.txt
- generated/cloudflare.txt
- generated/reality.txt
- generated/mobile.txt
- generated/fast.txt
- generated/clean.txt

Also generate:

- generated/base64/mix.txt
- generated/base64/cloudflare.txt

====================================================
BASE64 OUTPUTS
====================================================

Encode subscriptions correctly.

Example:

base64.b64encode(content.encode()).decode()

====================================================
CLASH GENERATION
====================================================

Optional.

Generate Clash-compatible YAML.

Requirements:

- clean formatting
- grouped proxies
- proxy-groups
- provider support

====================================================
ASYNC REQUIREMENTS
====================================================

Everything must be async.

Use:

- asyncio.gather
- async context managers
- async HTTP clients

Avoid blocking calls.

====================================================
LOGGING
====================================================

Implement structured logging.

Log:

- collection stats
- parsing failures
- dead configs
- output counts
- execution duration

====================================================
RETRY STRATEGY
====================================================

Implement retry handling.

Requirements:

- exponential backoff
- configurable retries
- safe failure handling

====================================================
CACHE
====================================================

Implement lightweight cache.

Use:
- JSON files
- memory cache

Avoid databases initially.

====================================================
CONFIGURATION
====================================================

Create settings.yaml.

Include:

- output limits
- timeout values
- health check settings
- source toggles
- logging settings
- retry settings

====================================================
DOCKER SUPPORT
====================================================

Create:

- Dockerfile
- docker-compose.yml

Requirements:

- lightweight image
- production-ready
- environment variables support

====================================================
GITHUB ACTIONS
====================================================

Create GitHub Actions workflow.

Requirements:

- run every 10 minutes
- install dependencies
- execute pipeline
- commit generated files
- push automatically

Workflow file:

.github/workflows/update.yml

====================================================
README
====================================================

Create professional README.md.

Include:

- project overview
- architecture
- setup instructions
- Telegram setup
- GitHub Actions setup
- Docker setup
- environment variables
- deployment guide
- subscription examples

====================================================
CODE QUALITY
====================================================

Requirements:

- typed Python
- clean architecture
- modular code
- docstrings
- maintainable structure
- separation of concerns

====================================================
IMPORTANT REQUIREMENTS
====================================================

DO NOT:

- publish giant garbage dumps
- keep dead configs
- create monolithic files
- use blocking requests
- overcomplicate the system

PRIORITIZE:

- lightweight outputs
- clean architecture
- curated configs
- maintainability
- scalability
- async performance
- code readability

====================================================
FINAL GOAL
====================================================

Build a high-quality curated subscription platform that:

- feels lightweight
- has clean subscriptions
- updates automatically
- has categorized outputs
- is scalable
- is production-ready
- is easy to maintain
- provides significantly better quality than giant public dump repositories

