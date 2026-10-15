---
name: github-actions-integration
description: Claude Code Action entegrasyonu - PR review ve issue-to-fix workflow kurulumu
---

# GitHub Actions - Claude Code Integration

## claude-code-action Nedir?

`anthropics/claude-code-action@v1` GitHub Actions action'i. PR'lari otomatik review eder, issue'lardan otomatik fix olusturur. vibecosystem ile entegre calisir.

Kaynak: https://github.com/anthropics/claude-code-action

## Kurulum

### 1. Secret Ayarlama

Repository Settings > Secrets and variables > Actions > New repository secret:

```
Name: ANTHROPIC_API_KEY
Value: sk-ant-... (Anthropic API key)
```

### 2. PR Review Workflow

Dosya: `.github/workflows/claude-review.yml`

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write
  issues: write

jobs:
  claude-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Claude Code Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          review_comment_prefix: "vibecosystem-review"
          direct_prompt: |
            Review this PR for:
            1. Code quality and patterns
            2. Security vulnerabilities (OWASP Top 10)
            3. Performance issues
            4. Test coverage gaps
            5. Breaking changes

            Use vibecosystem's code-reviewer agent standards.
            Provide VERDICT: PASS | WARN | FAIL
```

**Ne yapar:** PR acildiginda, guncellediginde veya yeniden acildiginda otomatik review yapar. Review sonucunu PR comment olarak yazar.

### 3. Issue-to-Fix Workflow

Dosya: `.github/workflows/claude-fix.yml`

```yaml
name: Claude Code Fix
on:
  issues:
    types: [labeled]

permissions:
  contents: write
  pull-requests: write
  issues: write

jobs:
  claude-fix:
    if: contains(github.event.label.name, 'claude-fix')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Claude Code Fix
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          direct_prompt: |
            Fix the issue described below.
            Follow TDD workflow: write test first, then implement fix.
            Create a PR with the fix.

            Issue: ${{ github.event.issue.title }}
            Body: ${{ github.event.issue.body }}
```

**Ne yapar:** Issue'ya `claude-fix` label'i eklendiginde otomatik fix olusturur ve PR acar.

## Kullanim

### PR Review
1. PR ac - otomatik review baslar
2. Review comment'inde VERDICT gorursun: PASS, WARN veya FAIL
3. FAIL varsa issue'lari duzelt, PR'i guncelle - tekrar review olur

### Issue Fix
1. Issue ac, sorunu detayli yaz
2. `claude-fix` label'i ekle
3. Claude otomatik branch olusturur, fix yapar, PR acar
4. PR'i review et ve merge et

## Workflow Customization

### Review Scope Daraltma

Sadece belirli dosya tiplerini review et:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]
    paths:
      - '**.ts'
      - '**.tsx'
      - '**.js'
      - '**.jsx'
```

### Custom Review Prompt

vibecosystem agent standartlarina gore prompt'u genislet:

```yaml
direct_prompt: |
  Review this PR using vibecosystem standards:

  ## Code Quality
  - Immutability: no mutations, use spread operator
  - File size: max 800 lines per file
  - Function size: max 50 lines
  - Nesting: max 4 levels
  - No console.log in production code
  - No hardcoded values

  ## Security (OWASP Top 10)
  - Input validation (use zod)
  - SQL injection prevention
  - XSS prevention
  - No hardcoded credentials
  - Rate limiting check

  ## Testing
  - Test coverage >= 80%
  - Edge cases covered
  - Error paths tested

  VERDICT: PASS | WARN | FAIL
```

### Fix Workflow Ek Talimatlar

```yaml
direct_prompt: |
  Fix the issue below.
  Rules:
  - TDD: write failing test first, then implement
  - Defensive code: try/catch, null checks, input validation
  - No mutations, use immutable patterns
  - Follow repository's existing code style
  - Run tests before creating PR

  Issue: ${{ github.event.issue.title }}
  Body: ${{ github.event.issue.body }}
```

### Multiple Label Support

Farkli label'lar icin farkli davranislar:

```yaml
jobs:
  claude-fix:
    if: contains(github.event.label.name, 'claude-fix')
    # ... standard fix

  claude-refactor:
    if: contains(github.event.label.name, 'claude-refactor')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          direct_prompt: |
            Refactor the code described in this issue.
            Maintain all existing tests.
            Do not change external behavior.
            Issue: ${{ github.event.issue.title }}
            Body: ${{ github.event.issue.body }}
```

## vibecosystem Entegrasyonu

### CLAUDE.md ile Birlikte

Repository'de `CLAUDE.md` varsa claude-code-action onu otomatik okur. vibecosystem kurallarini CLAUDE.md'ye ekle:

```markdown
# Project Rules
- Follow vibecosystem coding standards
- Use TDD workflow for all changes
- Security review required for auth/data code
- VERDICT format: PASS | WARN | FAIL
```

### Agent Standarti

Review workflow'u vibecosystem'in code-reviewer agent standartlarini kullanir:
- Kod kalitesi (immutability, dosya boyutu, fonksiyon boyutu)
- Security (OWASP Top 10)
- Performance
- Test coverage
- Breaking changes

Fix workflow'u TDD workflow'unu kullanir:
- Onceki test yaz (RED)
- Fix implement et (GREEN)
- Refactor (IMPROVE)

## Troubleshooting

| Sorun | Cozum |
|-------|-------|
| Review calismadi | ANTHROPIC_API_KEY secret ayarli mi? |
| Permission hatasi | Workflow permissions blogu dogru mu? |
| Fix PR acilmadi | `claude-fix` label dogru yazildi mi? |
| Review cok uzun suruyor | `fetch-depth: 1` ile sadece son commit'i al |
| Rate limit | API key plan limitini kontrol et |
