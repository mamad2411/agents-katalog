---
name: understand-codebase
description: "Codebase'i derinlemesine anla. Onboarding, architecture discovery, dependency mapping."
---

# Understand Codebase

## Onboarding Workflow (Yeni Developer)

### Hizli Baslangic (5 Dakika)

```
1. Tech stack tespit:
   ls package.json go.mod pyproject.toml tsconfig.json Cargo.toml manage.py

2. Proje yapisi:
   tldr tree . --depth 2

3. Entry point'leri bul:
   tldr structure . --lang <detected-lang>

4. README/docs oku:
   cat README.md CONTRIBUTING.md docs/

5. CI/CD kontrol:
   ls .github/workflows/ .gitlab-ci.yml Jenkinsfile Dockerfile
```

### Detayli Kesif (30 Dakika)

```
1. Architecture overview:
   tldr arch src/

2. Import/dependency graph:
   tldr calls src/

3. Test yapisi:
   tldr tree . --ext .test.ts,.spec.ts,.test.py,_test.go

4. Config dosyalari:
   ls *.config.* .env.example docker-compose.yml

5. Data modelleri:
   Grep "interface|type|class|struct|model" --type ts/py/go
```

## Codebase Overview Olusturma

### Otomatik Overview

```bash
# 1. Dosya dagilimi
tldr tree . | wc -l  # toplam dosya
tldr tree . --ext .ts,.tsx  # TypeScript dosyalari
tldr tree . --ext .test.ts  # Test dosyalari

# 2. Kod yapisi
tldr structure src/ --lang typescript
# Fonksiyonlar, class'lar, export'lar

# 3. Mimari katmanlar
tldr arch src/
# Entry (controller/handler) > Middle (service) > Leaf (util)

# 4. Dead code
tldr dead src/ --entry main,test_
```

### Overview Template

```markdown
# Project: <name>

## Tech Stack
- Language: <lang> <version>
- Framework: <framework> <version>
- Database: <db>
- CI/CD: <tool>

## Architecture
- Pattern: <MVC|Clean|Hexagonal|Monolith|Microservice>
- Entry points: <files>
- Layers: <controller → service → repository → model>

## Key Directories
- src/         → Kaynak kod
- tests/       → Test dosyalari
- config/      → Konfigürasyon
- scripts/     → Yardimci scriptler
- docs/        → Dokumantasyon

## Key Files
- <entry-file>  → Uygulama entry point
- <config-file> → Ana konfigürasyon
- <schema-file> → Data modelleri
- <route-file>  → API routing

## Data Flow
<request → middleware → controller → service → repository → database>

## External Dependencies
- <key-dep-1>: <purpose>
- <key-dep-2>: <purpose>
```

## Architecture Dokumentasyonu

### Katman Tespiti

```bash
# tldr arch ile otomatik tespit
tldr arch src/
# Cikti: entry_layer, middle_layer, leaf_layer, circular_deps

# Manuel tespit: import yonlerini takip et
tldr calls src/ --depth 3
```

### Mimari Patern Tespiti

| Ipucu | Patern |
|-------|--------|
| controllers/, routes/, handlers/ | MVC / REST API |
| domain/, application/, infrastructure/ | Clean Architecture |
| ports/, adapters/ | Hexagonal |
| services/, modules/ | Modular Monolith |
| packages/, apps/ | Monorepo |
| pages/, app/ (Next.js) | File-based routing |
| resolvers/, schema/ | GraphQL |
| commands/, queries/, events/ | CQRS |
| aggregates/, entities/, value-objects/ | DDD |

### Architectural Decision Records (ADR)

```bash
# codebase-memory MCP ile ADR yonetimi
mcp_codebase_memory.manage_adr({
  action: "create",
  title: "Use PostgreSQL for primary database",
  status: "accepted",
  context: "Need ACID transactions, complex queries",
  decision: "PostgreSQL 16 with pgvector extension",
  consequences: "Need DBA expertise, managed service cost"
})

# ADR listele
mcp_codebase_memory.manage_adr({ action: "list" })
```

## Key File Identification

### Otomatik Tespit

```bash
# Entry point'ler
tldr structure . --lang typescript | grep -i "main\|index\|app\|server"

# Konfigürasyon
ls -la *.config.* .env* tsconfig.json package.json

# Schema/Model
tldr search "schema\|model\|entity\|interface" src/ --lang typescript

# Routing
tldr search "router\|route\|endpoint\|controller" src/
```

### Kritik Dosya Kategorileri

| Kategori | Nasil Bul | Neden Onemli |
|----------|-----------|--------------|
| Entry point | main.ts, index.ts, app.ts | Uygulamanin baslangici |
| Config | *.config.*, .env | Ortam ayarlari |
| Schema/Model | models/, schema/, types/ | Data yapisi |
| Routes | routes/, controllers/ | API surface |
| Middleware | middleware/ | Cross-cutting concerns |
| Database | migrations/, seeds/ | DB yapisi |
| Tests | *.test.*, *.spec.* | Test coverage |
| CI/CD | .github/workflows/ | Build/deploy |
| Docker | Dockerfile, docker-compose | Container config |

## Dependency Mapping

### Package Dependency Analizi

```bash
# Node.js
cat package.json | jq '.dependencies, .devDependencies'

# Python
cat requirements.txt  # veya pyproject.toml
pip list --outdated

# Go
cat go.mod
go list -m all

# Rust
cat Cargo.toml
```

### Internal Dependency Graph

```bash
# Dosyalar arasi import iliskileri
tldr calls src/ --depth 2

# Spesifik dosyanin import'lari
tldr imports src/services/auth.ts

# Kim bu modulu import ediyor?
tldr importers auth src/

# Impact analizi (refactoring oncesi)
tldr impact processOrder src/ --depth 3
```

### Dependency Risk Analizi

| Risk | Kontrol | Arac |
|------|---------|------|
| CVE/vulnerability | npm audit / pip audit | snyk, dependabot |
| Outdated | major version farki | npm outdated |
| Unmaintained | Son commit 1+ yil | GitHub API |
| License risk | GPL in commercial | license-checker |
| Size bloat | Bundle size | bundlephobia |

## Data Flow Tracing

### Request-Response Flow

```bash
# Fonksiyon cagri zinciri
tldr calls src/ --depth 4

# Spesifik fonksiyonun cagri yolu
tldr trace_call_path src/ fromFunction toFunction

# Data flow analizi
tldr dfg src/services/order.ts processOrder

# Program slice (spesifik satiri etkileyen her sey)
tldr slice src/services/order.ts processOrder 42
```

### Data Flow Mapping Template

```
USER INPUT
  → Validation (middleware/schema)
  → Controller (routing, request parse)
  → Service (business logic)
  → Repository (data access)
  → Database (persistence)
  → Response (serialization)
  → USER OUTPUT

Side effects:
  → Queue (async processing)
  → Cache (read optimization)
  → External API (3rd party)
  → Event bus (pub/sub)
```

### State Management Flow (Frontend)

```
User Action
  → Event Handler (onClick, onChange)
  → State Update (useState, dispatch, store.set)
  → Re-render (component tree)
  → Side Effect (useEffect, subscription)
  → API Call (fetch, axios)
  → State Update (response)
  → Re-render
```

## API Surface Discovery

### REST API Endpoints

```bash
# Route tanimlarini bul
Grep "router\.(get|post|put|patch|delete)\|app\.(get|post|put|patch|delete)" src/

# Express/Fastify route'lar
tldr search "route\|endpoint" src/ --lang typescript

# OpenAPI spec varsa
cat openapi.yaml  # veya swagger.json
```

### GraphQL Schema

```bash
# Schema tanimlarini bul
Grep "type Query|type Mutation|type Subscription" src/

# Resolver'lari bul
tldr search "resolver\|Resolver" src/
```

### API Dokumantasyonu

```
Her endpoint icin:
  - Method + Path: GET /api/users/:id
  - Auth: Bearer token / API key / Public
  - Request: Query params, body schema
  - Response: Success (200), Error (4xx, 5xx)
  - Rate limit: X req/min
```

## Test Coverage Mapping

### Test Yapisi Analizi

```bash
# Test dosyalarini bul
tldr tree . --ext .test.ts,.spec.ts,.test.py,_test.go

# Test/source orani
echo "Source files:" && tldr tree src/ --ext .ts,.tsx | wc -l
echo "Test files:" && tldr tree . --ext .test.ts,.spec.ts | wc -l

# Hangi dosyalarin testi YOK
tldr dead src/ --entry test_  # test'lerden cagrilmayan fonksiyonlar
```

### Coverage Raporu

```bash
# Node.js
npx jest --coverage --coverageReporters=text-summary

# Python
pytest --cov=src --cov-report=term-missing

# Go
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out
```

### Test Gap Analizi

| Dosya/Modul | Unit Test | Integration | E2E | Risk |
|-------------|-----------|-------------|-----|------|
| Auth service | var | var | yok | HIGH |
| Payment | var | var | var | LOW |
| User CRUD | var | yok | yok | MEDIUM |
| Config | yok | yok | yok | LOW |

## Tech Debt Identification

### Otomatik Tespit

```bash
# Dead code
tldr dead src/ --entry main,test_,handle,route

# Buyuk dosyalar (800+ satir)
find src/ -name "*.ts" -exec wc -l {} + | sort -rn | head -20

# TODO/FIXME/HACK
Grep "TODO|FIXME|HACK|XXX|TEMP|WORKAROUND" src/

# Complexity (control flow)
tldr cfg src/services/complex.ts processData
# Cok fazla branch = refactoring gerekli

# Diagnostics (type error + lint)
tldr diagnostics src/ --project
```

### Tech Debt Kategorileri

| Kategori | Gostergeler | Oncelik |
|----------|------------|---------|
| Dead code | Kullanilmayan fonksiyon/import | LOW |
| God file | 800+ satir dosya | MEDIUM |
| Missing tests | Coverage <50% | HIGH |
| Outdated deps | Major version farki | MEDIUM |
| Security | CVE, hardcoded secret | CRITICAL |
| Duplication | Benzer kod bloklari | MEDIUM |
| Complexity | Cyclomatic >10 | HIGH |

## Knowledge Graph (codebase-memory MCP)

### Repository Indexleme

```
mcp_codebase_memory.index_repository({
  path: "/path/to/project",
  name: "my-project"
})
```

### Graph Sorgulama

```
// Mimari overview
mcp_codebase_memory.get_architecture({
  project: "my-project"
})

// Kod arama
mcp_codebase_memory.search_code({
  project: "my-project",
  query: "authentication flow"
})

// Graph schema
mcp_codebase_memory.get_graph_schema({
  project: "my-project"
})

// Degisiklik tespiti
mcp_codebase_memory.detect_changes({
  project: "my-project"
})
```

## Entegrasyon: tldr CLI + codebase-memory MCP

### Tam Analiz Workflow

```bash
# 1. Yapi (tldr)
tldr tree . --depth 2
tldr structure src/ --lang typescript

# 2. Mimari (tldr)
tldr arch src/
tldr calls src/ --depth 3

# 3. Indexle (codebase-memory MCP)
mcp_codebase_memory.index_repository({ path: ".", name: "project" })

# 4. Graph sorgu (codebase-memory MCP)
mcp_codebase_memory.get_architecture({ project: "project" })

# 5. Impact analizi (tldr)
tldr impact targetFunction src/ --depth 3

# 6. Dead code (tldr)
tldr dead src/ --entry main

# 7. Diagnostics (tldr)
tldr diagnostics src/ --project

# 8. Test impact (tldr)
tldr change-impact --git
```

### Surekli Guncelleme

```
Her onemli degisiklikte:
1. tldr change-impact → etkilenen testleri bul
2. mcp_codebase_memory.detect_changes → graph'i guncelle
3. tldr dead src/ → yeni dead code kontrol
4. tldr diagnostics src/ → type/lint hata kontrolu
```

## Anti-Patterns

| Anti-Pattern | Dogru Yol |
|-------------|-----------|
| Hemen koda dal | Once overview al, sonra oku |
| Tek dosya oku, anladim san | Cagri zincirini takip et |
| grep ile yetiniyor | tldr structure + arch kullan |
| Mimariyi varsay | tldr arch ile dogrula |
| Dead code'u gormezden gel | tldr dead ile periyodik temizlik |
| Test coverage bilme | Coverage raporu al, gap analiz yap |
| Dependency'leri kontrol etme | npm audit / pip audit periyodik calistir |

## Quick Reference

```
HIZLI: "Bu proje ne yapar?"
  → tldr tree . && cat README.md

ORTA: "Nasil calisir?"
  → tldr arch src/ && tldr calls src/

DERIN: "Bu fonksiyon neyi etkiler?"
  → tldr impact <func> src/ && tldr dfg <file> <func>

TAM: "Her seyi anlamam lazim"
  → Yukaridaki Tam Analiz Workflow'u takip et
```
