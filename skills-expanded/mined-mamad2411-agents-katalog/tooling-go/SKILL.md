---
name: tooling-go
description: "Go audit tooling: golangci-lint, gosec (SAST), govulncheck (CVEs), staticcheck, gocyclo, deadcode, go-mutesting (mutations). Use during audit phases for Go projects."
---

# Go Audit Tooling

Запуск audit tools для Go проектов.

## Когда применять

- В audit phases для Go проектов
- После того как `language-detector` определил Go
- Tools проверены на наличие через `command -v`

## Tools

### golangci-lint (мета-linter)

```bash
golangci-lint run --out-format=json > /tmp/golangci.json 2>/dev/null
```

Это **главный tool** для Go - агрегирует множество linters:
- `errcheck` - не игнорированы ли возвращённые errors
- `gosimple` - simplifications
- `staticcheck` - bug patterns, performance, unused code
- `unused` - unused вertions
- `govet` - вetections и misconfigurations
- `ineffassign` - ineffective assignments
- `revive` - replacement для golint

Конфиг проекта в `.golangci.yml` если есть. Иначе - использовать defaults.

Severity mapping:
- Error category linters (`errcheck`, `staticcheck`, `unused`) → HIGH/MEDIUM
- Style linters (`revive`, `gofmt`) → LOW

### gosec (SAST)

```bash
gosec -fmt=json -out=/tmp/gosec.json ./... 2>/dev/null
```

Severity и Confidence в gosec output:
- `HIGH` severity + `HIGH` confidence → CRITICAL
- `HIGH` + `MEDIUM` → HIGH
- `MEDIUM` + `MEDIUM` → MEDIUM
- `LOW` → LOW

Common findings:
- G101: Hardcoded credentials
- G104: Errors unhandled
- G201/G202: SQL injection
- G304: File path provided as taint input  
- G404: Insecure random number source

### govulncheck (CVE check - Official Go vuln DB)

```bash
govulncheck -json ./... > /tmp/govulncheck.json 2>/dev/null
```

Это **official Google tool** для Go vulnerabilities. Лучше чем third-party tools.

Парсить:
- `Vulns[].OSV.aliases` - CVE IDs
- `Vulns[].Symbol` - какая функция уязвима
- `Vulns[].CallStack` - используется ли в проекте (важно!)

Severity mapping:
- Vuln в CallStack (used) → CRITICAL/HIGH
- Vuln НЕ в CallStack (transitive, not actually called) → MEDIUM/LOW

### Coverage (go test)

```bash
go test -coverprofile=coverage.out -covermode=atomic ./... 2>/dev/null
go tool cover -func=coverage.out > /tmp/coverage-func.txt
go tool cover -html=coverage.out -o /tmp/coverage.html 2>/dev/null
```

Парсить:
- `total:` line в coverage-func.txt - overall %
- Per-file breakdown
- Branch coverage **не** работает встроенно в Go - только statement

Это ограничение Go testing - statement coverage only.

### Staticcheck (более глубокий чем golangci linters)

```bash
staticcheck -f json ./... > /tmp/staticcheck.json 2>/dev/null
```

Хотя staticcheck включён в golangci-lint, иногда стоит запускать отдельно для:
- More detailed output
- Specific check categories (`-checks=SA*` для security analyses only)

### Deadcode

```bash
deadcode ./... > /tmp/deadcode.txt 2>/dev/null
```

Современный replacement для legacy `unused` checker. Better для cross-package analysis.

### Gocyclo (cyclomatic complexity)

```bash
gocyclo -avg . > /tmp/gocyclo-avg.txt 2>/dev/null
gocyclo -over 15 . > /tmp/gocyclo-over15.txt 2>/dev/null
```

CC thresholds for Go (часто more lenient чем для Python из-за стиля):
- 1-10: good
- 11-15: acceptable
- 16-30: high (HIGH finding)
- 30+: critical (CRITICAL finding в hot path)

### Cognitive complexity (gocognit)

```bash
gocognit -over 15 . > /tmp/gocognit.txt 2>/dev/null
```

Cognitive complexity больше отражает "как трудно читать", чем cyclomatic.

### Go-mutesting (mutation testing - DEEP MODE ONLY)

**Внимание**: less mature чем mutmut/Stryker. И медленный.

```bash
go-mutesting --json ./... > /tmp/mutesting.json 2>/dev/null
```

Mutation operators в go-mutesting:
- Branch flips
- Increment/decrement changes
- Constant value changes
- Removed statements

В deep mode:
- Запускать на критичных пакетах (не всё)
- Estimate time first
- Если > 4 hours - skip и flag incomplete

### Nancy (supply chain)

```bash
go list -json -m all | nancy sleuth --output=json > /tmp/nancy.json 2>/dev/null
```

Альтернатива govulncheck для supply chain. Использует Sonatype OSS Index.

### Built-in: go vet

```bash
go vet ./... 2>&1 | tee /tmp/govet.txt
```

Базовый Go tool, всегда доступен. Включён в golangci-lint, но запуск отдельно тоже useful.

## Output

Сырые outputs в `docs/audit/<TS>/<phase>/tooling-output/go/`.

## Tool unavailability

Если tools не установлены:

```markdown
## Missing tools (Go)

- gosec: not installed (`go install github.com/securego/gosec/v2/cmd/gosec@latest`)
- govulncheck: not installed (`go install golang.org/x/vuln/cmd/govulncheck@latest`)
- gocyclo: not installed (`go install github.com/fzipp/gocyclo/cmd/gocyclo@latest`)
- go-mutesting: not installed; mutation testing skipped
```

Tools для Go обычно устанавливаются через `go install`.

## Project structure detection

Standard Go project layouts:
- Cmd-based: `cmd/<binary-name>/main.go`
- Internal-only packages: `internal/`
- Public packages: `pkg/`
- API definitions: `api/` или `proto/`

Multi-module projects: `go.work` файл indicates workspace.

## Specific Go pitfalls (manual review priority)

1. **Goroutine leaks** - goroutines started but never finished
2. **Context handling** - propagated через все calls?
3. **Error wrapping** - используется `fmt.Errorf("...%w", err)` для context?
4. **Interface pollution** - too many small interfaces, defined в wrong package
5. **Panics в production code** - должны быть только в truly unrecoverable situations
6. **Channel deadlocks** - нет defer close на producer side, etc.
7. **sync primitives misuse** - sync.Mutex passed by value (bug), sync.Once в loop, etc.

Эти patterns часто require manual review - tools редко находят.

## Module integrity

```bash
# Verify module sums
go mod verify

# Check for ambient dependencies
go mod tidy -v 2>&1 | tee /tmp/mod-tidy.txt
```

`mod-tidy` output показывает:
- Missing dependencies (added)
- Unused dependencies (removed)
- Если `mod tidy` хочет много изменить - проект в drift state, MEDIUM finding.
