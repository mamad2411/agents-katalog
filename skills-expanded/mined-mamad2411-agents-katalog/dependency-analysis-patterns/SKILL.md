---
name: dependency-analysis-patterns
description: Dependency graph visualization, circular dependency detection, CVE scanning, and license compliance
---

# Dependency Analysis Patterns

## Dependency Graph Visualization

```bash
# npm
npx depcruise --output-type dot src/ | dot -T svg > deps.svg

# Python
pipdeptree --graph-output svg > deps.svg

# Go
go mod graph | modgraphviz | dot -T svg > deps.svg
```

## Circular Dependency Detection

```bash
# JavaScript/TypeScript
npx madge --circular src/
npx dpdm --circular src/index.ts

# Python
pydeps --cluster --no-show src/
```

### Fix Strategies

| Circular Tip | Çözüm |
|-------------|-------|
| A → B → A | Interface/port ile inversion |
| A → B → C → A | Shared module extract et |
| Barrel file circular | Direct import kullan |

## CVE Scanning

```bash
# npm
npm audit --json | jq '.vulnerabilities | to_entries[] | select(.value.severity == "critical")'

# pip
pip-audit --format json --desc

# Go
govulncheck ./...

# Multi-tool
trivy fs --severity CRITICAL,HIGH .
```

### CVE Prioritization

| CVSS | Severity | Aksiyon | SLA |
|------|----------|---------|-----|
| 9.0+ | Critical | Hotfix | 24h |
| 7.0-8.9 | High | Sprint fix | 1 hafta |
| 4.0-6.9 | Medium | Backlog | 1 ay |
| <4.0 | Low | Track | Fırsatçı |

## License Compliance

```bash
# npm
npx license-checker --production --json --failOn "GPL-3.0;AGPL-3.0"

# Python
pip-licenses --format=json --fail-on="GPL-3.0"
```

| License | Commercial OK | Copyleft | Risk |
|---------|-------------|----------|------|
| MIT | Evet | Hayır | Düşük |
| Apache-2.0 | Evet | Hayır | Düşük |
| BSD-3 | Evet | Hayır | Düşük |
| MPL-2.0 | Evet | Kısmi | Orta |
| LGPL | Dikkat | Kısmi | Orta |
| GPL-3.0 | Dikkat | Evet | Yüksek |
| AGPL-3.0 | Dikkat | Evet | Çok yüksek |

## Update Impact Analysis

```bash
# npm - outdated
npm outdated --json

# Semver risk
# patch (0.0.x) → güvenli
# minor (0.x.0) → genelde güvenli
# major (x.0.0) → breaking change riski

# Test after update
npm update <pkg> && npm test
```

## Checklist

- [ ] `npm audit` / `pip-audit` temiz (critical/high yok)
- [ ] License audit pass (GPL yok)
- [ ] Circular dependency yok
- [ ] Lockfile committed ve güncel
- [ ] Unused dependency yok (`depcheck`)
- [ ] Renovate/Dependabot aktif
- [ ] Major version behind ≤1

## Anti-Patterns

- Audit warning'leri ignore etmek
- Lockfile commit etmemek
- Pinned version kullanmamak (^, ~)
- License check'siz production dependency
- Dependency update'siz 6+ ay
