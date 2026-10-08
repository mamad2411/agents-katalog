# 🚀 Cursor Agent Instructions - Bridge_ScaleCmd_Rust

Jesteś agentem AI wspierającym development projektu **Bridge_ScaleCmd_Rust**.
Ten projekt to uniwersalny most komunikacyjny między aplikacjami React/TypeScript 
a wagami przemysłowymi (Rinstrum C320, Dini Argeo) poprzez serwer Rust.

---

## 📋 Projekt: Universal Industrial Scale Communication Bridge

┌────────────────────────┐
│ React Frontend         │
│ (Vite, port 5173)      │
└──────────┬─────────────┘
│ HTTP/REST/WebSocket
▼
┌────────────────────────┐
│ Rust Backend           │
│ (Actix-web, 8080)      │
└──────────┬─────────────┘
│ TCP/Serial
▼
┌────────────────────────┐
│ Industrial Scales      │
│ (Rinstrum, Dini Argeo) │
└────────────────────────┘

**Stack:** Rust 1.91.1 | React 18.x | TypeScript 5.x | Vite 5.x | Tailwind 3.x | Windows 10+

---

## 👥 5 Role - Używaj @prefix w Promptach

Zawsze wskaż swoją rolę poprzez prefix `@` aby Cursor załadował właściwy kontekst:

@backend "polecenie dla backendu"
@frontend "polecenie dla frontendu"
@devices "polecenie dla integracji urządzeń"
@build "polecenie dla build pipeline'u"
@testing "polecenie dla testowania"

**Szczegółowe opisy ról zobacz w:** `.cursor/rules.yaml`

---

## 🏗️ @backend - Backend Architecture

**Gdzie pracujesz:**
src-rust/src/
├── main.rs # Server entry point
├── device_manager.rs # Device orchestration
├── error.rs # Custom error types
├── models/ # Request/Response DTOs
└── adapters/ # Device adapters

**Kluczowe obowiązki:**
- Architektura serwera Actix-web (port 8080)
- Adapter pattern dla urządzeń
- Error handling: `Result<T, CustomError>`
- Async/await patterns
- Structured logging (tracing crate)

**Reguły:**
✅ Rustdoc comments dla public API
✅ Async/await zamiast callbacks
✅ Arc<T> zamiast clone()
⛔ Bez unwrap() w production
⛔ Bez hardcoded wartości

**Przykłady:**
@backend "Review main.rs and optimize for concurrent connections"
@backend "Add structured logging with tracing crate"
@backend "Implement graceful shutdown mechanism"

---

## 🎨 @frontend - Frontend Development

**Gdzie pracujesz:**
src/
├── pages/Index.tsx # ⭐ MAIN PAGE - ZAWSZE UPDATE!
├── components/ # shadcn/ui + custom
├── services/ # API client
├── context/ # State (Context API)
├── hooks/ # Custom hooks
└── types/ # TypeScript types

**Kluczowe obowiązki:**
- React komponenty (shadcn/ui based)
- State management (Context API)
- React Router v6+ navigation
- Tailwind CSS styling (utility-first)
- API integration
- Form validation (Zod, shadcn/ui)

**Reguły:**
✅ Import shadcn/ui z prebuilt library ONLY
✅ TypeScript strict (zero `any`)
✅ **ZAWSZE UPDATE `src/pages/Index.tsx` przy nowych komponentach!**
✅ Tailwind CSS dla wszystkich stylów
⛔ Nie edytuj shadcn/ui files
⛔ Nie inline CSS
⛔ Nie console.log() w production

**Przykłady:**
@frontend "Create DeviceConfigPanel component with form validation"
@frontend "Implement real-time status with WebSocket updates"
@frontend "Add new component to src/pages/Index.tsx"

---

## 🔌 @devices - Device Integration Specialist

**Gdzie pracujesz:**
src-rust/src/
├── adapters/ # Device implementations
│ ├── rinstrum_adapter.rs
│ └── dini_argeo_adapter.rs
└── device_manager.rs # Manager logic

config/
└── devices.json # Device definitions

docs/
└── device-protocols/ # Protocol specs

**Kluczowe obowiązki:**
- Device adapters (DeviceAdapter trait)
- RINCMD protocol (Rinstrum C320)
- DINI_ASCII protocol (Dini Argeo)
- TCP/Serial connection management
- Device configuration management
- Timeout handling, reconnection logic
- Protocol documentation

**Reguły:**
✅ Implementuj DeviceAdapter trait dla każdego urządzenia
✅ Definicje urządzeń w `config/devices.json`
✅ Loguj wszystkie komunikacje (INFO level)
✅ Graceful timeout handling
✅ Dokumentuj protocol specifications
⛔ Bez hardcoded IP/porty
⛔ Bez ignorowania timeouts
⛔ Bez blocking I/O (zawsze async)

**Przykłady:**
@devices "Add support for manufacturer XYZ with TCP protocol"
@devices "Debug Rinstrum connection timeout - improve logging"
@devices "Implement device auto-reconnection with exponential backoff"

---

## 🛠️ @build - Build & DevOps Engineer

**Gdzie pracujesz:**
scripts/
├── Setup-MinGW.ps1 # MinGW setup
├── build-rust-mingw.ps1 # Rust build
└── run-backend.ps1 # Run server

.github/workflows/ # CI/CD pipelines

installer/ # Inno Setup config

**Kluczowe obowiązki:**
- MinGW toolchain configuration (Windows)
- PowerShell build scripts
- GitHub Actions workflows
- Windows installer generation (Inno Setup)
- Environment setup, troubleshooting
- Release management, versioning

**Reguły:**
✅ Rust: 1.91.1 stable-x86_64-pc-windows-gnu
✅ MinGW: `D:\msys64\mingw64\bin`
✅ Wersjonowanie w `Cargo.toml` + `package.json`
✅ GitHub Actions dla każdego kroku
⛔ Bez build artifacts w repo
⛔ Bez hardcoded absolute paths

**Environment Variables:**
```powershell
$mingwPath = "D:\msys64\mingw64"
$env:CARGO_TARGET_X86_64_PC_WINDOWS_GNU_LINKER = "$mingwPath\bin\gcc.exe"
$env:PATH = "$mingwPath\bin;$mingwPath\x86_64-w64-mingw32\bin;$env:PATH"
```

**Przykłady:**
@build "Fix MinGW linker path - dlltool not found"
@build "Create GitHub Actions workflow for release builds"
@build "Generate Windows installer version 0.2.0"

---

## 🧪 @testing - QA & Testing Specialist

**Gdzie pracujesz:**
src/test/                   # Frontend unit tests
src-rust/tests/             # Backend integration tests
e2e/                        # Playwright E2E tests
vitest.config.ts            # Frontend test config
playwright.config.ts        # E2E test config

**Kluczowe obowiązki:**

Unit tests (Vitest frontend, Cargo backend)

Integration tests (API + device communication)

E2E tests (Playwright)

Performance testing, benchmarks

Code coverage tracking, reporting

Device connection testing

Reguły:
✅ Target >80% code coverage
✅ Unit testy dla każdej public function
✅ E2E testy dla critical workflows
✅ Test error scenarios (timeouts, disconnects)
✅ Performance benchmarks dla critical paths
⛔ Nie tylko happy paths
⛔ Nie flaky tests

**Przykłady:**
@testing "Write unit tests for DeviceConfigForm (90% coverage)"
@testing "Create E2E test for scale reading workflow"
@testing "Set up code coverage in GitHub Actions"

---

## 📁 Struktura Katalogów

Bridge_ScaleCmd_Rust/
│
├── src-rust/                    # 🏗️ Backend (Rust)
│   ├── src/
│   │   ├── main.rs
│   │   ├── device_manager.rs
│   │   ├── error.rs
│   │   ├── models/
│   │   └── adapters/
│   ├── tests/
│   └── Cargo.toml
│
├── src/                         # 🎨 Frontend (React)
│   ├── pages/
│   │   └── Index.tsx            # ⭐ MAIN PAGE
│   ├── components/
│   ├── services/
│   ├── context/
│   ├── hooks/
│   ├── types/
│   ├── test/
│   ├── App.tsx
│   └── main.tsx
│
├── config/                      # ⚙️ Configuration
│   └── devices.json
│
├── scripts/                     # 🛠️ Build Scripts
│   ├── Setup-MinGW.ps1
│   ├── build-rust-mingw.ps1
│   └── run-backend.ps1
│
├── e2e/                         # 🧪 E2E Tests
│
├── docs/                        # 📖 Documentation
│   └── device-protocols/
│
└── .cursor/                     # 🤖 Cursor Configuration
    ├── instructions.md          # ← Ten plik (praktyczne instrukcje)
    └── rules.yaml               # Szczegółowe reguły dla każdej roli

---

## 🛠️ Build Commands

| Komenda | Cel |
cd src-rust && cargo build	Build backend (debug)
cd src-rust && cargo build --release	Build backend (release)
cd src-rust && cargo test	Test backend
npm run dev	Frontend dev server (5173)
npm run build	Build frontend (production)
npm run test | Frontend unit tests |
npm run test:e2e | E2E tests (Playwright) |

---

## 📝 Naming Conventions

**Rust:**

Modules: snake_case (device_manager, rinstrum_adapter)

Types: PascalCase (DeviceManager, RinstrumAdapter)

Functions: snake_case (read_weight, connect_device)

- Constants: SCREAMING_SNAKE_CASE (DEFAULT_TIMEOUT, MAX_RETRIES)

**TypeScript:**

Components: PascalCase (DeviceStatus, ScaleReader)

Functions: camelCase (readWeight, connectDevice)

Constants: SCREAMING_SNAKE_CASE (DEFAULT_TIMEOUT, API_URL)

Types: PascalCase (DeviceConfig, ScaleReading)

- Files: kebab-case (device-status.tsx, scale-reader.tsx)

**CSS:**

Classes: kebab-case (device-status, scale-reader)

- Variables: kebab-case (--primary-color, --spacing-lg)

---

## 📝 Git Workflow

**Branch naming:**

feature/short-description

bugfix/short-description

refactor/short-description

- docs/short-description

**Commit messages:**
```
type(scope): description
```

Examples:
- feat(backend): Add connection pooling to DeviceManager
- fix(frontend): Fix TypeScript error in DeviceStatus
- docs(devices): Add RINCMD protocol documentation
- test(backend): Add integration tests for TCP connections
```

---

## ✅ Pre-Commit Checklist
 Określiłem rolę (@backend/@frontend/@devices/@build/@testing)

 Kod następuje konwencjom nazewnictwa

 Brak console.log(), unwrap(), hardcoded wartości

 TypeScript: brak błędów

 Rust: brak unwrap() w production code

 Dodałem/aktualizowałem testy

 Jeśli nowy komponent: UPDATE src/pages/Index.tsx!

 - Commit message: type(scope): description

---

## 🔗 Ważne Dokumenty

| Dokument | Dla | Opis |
.cursor/rules.yaml	Wszystkie role	Szczegółowe definicje ról i reguł
AI_RULES.md	@frontend	Frontend coding conventions
BACKEND_GUIDELINES.md	@backend	Backend best practices
BUILD_WINDOWS.md	@build	Windows build setup
| config/devices.json | @devices | Device configurations |
| swagger.yaml | @backend | API specification |

---

## 🚀 Szybki Start
Przeczytaj to: .cursor/instructions.md ← TUTAJ

Poznaj reguły: .cursor/rules.yaml (dla szczegółów)

Wybierz rolę: Zidentyfikuj swoją rolę (@backend/@frontend/@devices/@build/@testing)

Pisz kod: Następuj konwencjom dla swojej roli

- Commituj: type(scope): description

---

## 💡 Jak Używać Cursora w Praktyce

**Przykład 1:**
Ty: "@backend Review main.rs and optimize for 1000 concurrent connections"
    Cursor: Załaduje src-rust/src/main.rs + kontekst z rules.yaml
    Cursor: Będzie znał Rust best practices z instrukcji
    Cursor: Dostarczy optymalizacji zgodne z regułami

**Przykład 2:**
Ty: "@frontend Create DeviceConfigPanel component and add to Index.tsx"
    Cursor: Załaduje src/components/ + src/pages/Index.tsx
    Cursor: Będzie wiedział o shadcn/ui + Tailwind
    Cursor: Upewni się że komponent będzie widoczny w Index.tsx

**Przykład 3:**
Ty: "@devices Debug Rinstrum timeout issue"
    Cursor: Załaduje src-rust/src/adapters/ + config/devices.json
    Cursor: Będzie znał RINCMD protocol i timeout handling
    Cursor: Dostarczy logowania i debugging wskazówki