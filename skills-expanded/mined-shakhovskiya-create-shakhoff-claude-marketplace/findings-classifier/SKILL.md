---
name: findings-classifier
description: "Classify, deduplicate, and assign severity to audit findings. Use after all audit phases complete to produce final priority-ordered list."
---

# Findings Classifier

Постобработка raw findings от всех фаз: дедупликация, severity assignment, prioritization.

## Когда применять

- После всех фаз `/audit:full` complete
- Когда нужно объединить findings из разных команд (`/audit:architecture` + `/audit:code`)
- Перед генерацией BACKLOG.md

## Inputs

- Все `findings.json` файлы из `docs/audit/<TS>/<phase>/`
- `_language-detection.json` для контекста
- Optional: `audit.config.yaml` с custom severity overrides

## Workflow

### F1. Collection

Собрать все findings из всех phases:

```bash
find docs/audit/<TS>/ -name "findings.json" -type f
```

Объединить в единый array (с сохранением phase metadata).

### F2. Deduplication

Findings из разных фаз могут описывать одну и ту же проблему. Дедупликация:

**Same finding indicator**:
- Same file + nearby line numbers (±10)
- Similar description (semantic similarity)
- Same root cause

Если deduplicated:
- Объединить evidence из всех источников
- Severity = max из источников
- Добавить metadata: `originally_found_in: [phase1, phase2]`

**Не объединять**:
- Если разные **types** проблем в одном файле (security CRITICAL и code MEDIUM в одном файле - это два finding'а)

### F3. Severity Assignment

Каждое finding имеет proposed severity от своей audit phase. Classifier validates и может переопределить:

**Universal severity rubric**:

| Severity | Definition | Examples |
|----------|------------|----------|
| **BLOCKER** | Production safety, immediate ship-stop | Hardcoded prod secret, active CVE с known exploit, broken auth |
| **CRITICAL** | High risk to production stability/security/data | God class в hot path, missing auth checks, mutation score <40% в core domain |
| **HIGH** | Significant technical debt, harder to fix later | Anaemic core domain models, missing ADRs для major decisions, complexity 15-30 |
| **MEDIUM** | Quality issues, some impact | Magic numbers, missing tests для new code, some docs drift |
| **LOW** | Style, minor improvements | Naming inconsistencies, unused imports, formatting |
| **INFO** | Observations, не findings per se | "Project uses framework X version Y", "100% test coverage в module Z" |

**Severity adjustments**:

Bump up:
- Hot file (top-20 most changed) → +1 severity
- Core domain module → +1 severity
- Production-running code (vs dev/test utilities) → +1 severity

Bump down:
- Test code → -1 severity (unless it's about test quality itself)
- Docs/scripts/internal tooling → -1 severity
- Dev-only configurations → -1 severity

### F4. Effort Estimation

Каждое finding получает estimate:

| Effort | Time | Examples |
|--------|------|----------|
| XS | <30 минут | Naming fix, single line update, config change |
| S | 30 минут - 2 часа | Add missing test, simple refactor of one function |
| M | 2-8 часов | Extract class, add new abstraction layer, fix moderate complexity |
| L | 1-3 дня | Major refactor, architecture change in module |
| XL | 1+ неделя | Cross-cutting changes, framework migration, major redesign |

### F5. Risk-If-Ignored Estimation

Опциональное поле "что произойдёт если не починить":

| Risk | Description |
|------|-------------|
| HIGH | Active production issue, security breach risk, data loss risk |
| MEDIUM | Future bugs likely, maintenance cost increasing, onboarding harder |
| LOW | Slight quality degradation, minor inconvenience |

### F6. Cross-Phase Correlation

Иногда findings из разных фаз reinforce друг друга. Классифайер должен это поймать:

**Example correlation**:
- `domain` finding: "Project total invariant not enforced"
- `tests` finding: "calculate_total() has no unit tests"
- `code` finding: "calculate_total() has cyclomatic complexity 22"

Это **correlated cluster** - все три про одну функцию. В backlog показать как related findings.

### F7. False Positive Elimination

Tools generate false positives. Classifier должен:

- Если detect-secrets находит "secret" в файле тестов помеченном как stub - FP, drop
- Если bandit находит SQL injection в admin command который читает из argparse (не user input) - FP, drop
- Если eslint-plugin-security находит eval в build script (not runtime) - FP, drop

В сомнительных случаях - **оставлять finding** с пометкой "Possible false positive, manual review".

### F8. Output

Создай enriched findings в `docs/audit/<TS>/_findings-classified.json`:

```json
{
  "metadata": {
    "audit_timestamp": "2026-04-29-1430",
    "total_findings_raw": 123,
    "total_after_dedup": 87,
    "total_after_fp_filter": 78
  },
  "findings": [
    {
      "id": "BLOCKER-001",
      "severity": "BLOCKER",
      "phase": "security",
      "category": "secrets",
      "title": "Hardcoded production AWS access key in settings",
      "evidence": [
        {"file": "settings/prod.py", "line": 23, "snippet": "AWS_ACCESS_KEY = 'AKIA...' (redacted)"}
      ],
      "impact": "AWS account compromise; full S3/EC2 access if leaked.",
      "fix_prompt": "Move AWS credentials to your project's secret manager (e.g., Infisical, Vault, AWS Secrets Manager, Doppler). Replace settings.py:23 with `os.environ['AWS_ACCESS_KEY']`. Add the secret to the appropriate environment. Rotate the current key in AWS console immediately.",
      "verification_checklist": [
        "AWS key removed from settings.py",
        "Key added to project's secret manager (prod environment)",
        "Old key rotated in AWS",
        "Application starts and authenticates correctly with new key"
      ],
      "effort": "S",
      "risk_if_ignored": "HIGH",
      "originally_found_in": ["security"],
      "related_findings": []
    }
  ]
}
```

### F9. Custom overrides

Если в проекте есть `audit.config.yaml` - применить overrides:

```yaml
# audit.config.yaml
severity_overrides:
  - rule: "bandit:B101"  # assert_used
    severity: LOW  # downgrade because we use asserts in dev only
  - rule: "any in test_*"
    severity: LOW  # bump down anything found in tests

ignore_patterns:
  - "vendor/**"
  - "**/migrations/*.py"
  - "scripts/legacy_*.py"
```

## Принципы

1. **Better few precise findings, чем много шумных** - quality > quantity
2. **Severity defended, не subjective** - rubric выше + adjustments documented
3. **Always actionable** - каждое finding имеет specific fix path
4. **Conservative deduplication** - в сомнениях оставлять отдельно
