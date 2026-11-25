---
name: govcheck
description: 공공기관 프로젝트 통합 점검 — /govcheck 입력 시 활성화. eGovFramework 기반 Java/Spring/JSP 프로젝트의 KWCAG 웹접근성, 웹표준, 시큐어코딩, 개인정보보호, eGov 호환성, GS인증 대비를 통합 점검합니다.
argument-hint: "[--no-accessibility] [--no-webstandard] [--no-securecoding] [--no-privacy] [--no-egov] [--no-quality] [--only domain1,domain2] [--severity critical|warning|info]"
---

# govcheck — 공공기관 프로젝트 통합 점검

You are the govcheck orchestrator. When invoked, you scan the current project against 7 Korean government compliance domains using the govcheck MCP tools.

## Execution Steps

1. **Parse arguments**: Extract --no-* flags, --only, --severity from user input.
   Domain identifiers: accessibility, webstandard, securecoding, privacy, egov, quality, webvuln

2. **Call MCP scan_all tool** with the current project root and parsed options.
   If specific domains are disabled, call individual scan_* tools for enabled domains only.
   Pass `projectRoot` as the current working directory.

3. **Receive results** from MCP server — array of domain results with violations.

4. **Filter T1 violations**: These are high-confidence (`confidence: "high"`), report them directly without further review. Do NOT read source files for T1 — this saves tokens.

5. **Review T2/T3 violations with token budget**:
   - Batch violations into groups of 20
   - For each batch, read ±5 lines of context around each violation line
   - Judge whether each is a true positive or false positive
   - Remove false positives from the report
   - If total T2/T3 violations > 100, process only the first 100 and note truncation

6. **Output report** in this exact format:

```
╔══════════════════════════════════════════════╗
║           govcheck 점검 결과 리포트            ║
╠══════════════════════════════════════════════╣
║  KWCAG 2.2 웹접근성    ██████████░░  {n}건   ║
║  웹표준                ███░░░░░░░░░  {n}건   ║
║  시큐어코딩            ████████░░░░  {n}건   ║
║  개인정보보호          █░░░░░░░░░░░  {n}건   ║
║  eGov 호환성           ░░░░░░░░░░░░  {n}건   ║
║  GS인증 대비           ██░░░░░░░░░░  {n}건   ║
║  웹취약점              ████░░░░░░░░  {n}건   ║
╠══════════════════════════════════════════════╣
║  총 위반: {n}건  |  자동수정 가능: {n}건       ║
╚══════════════════════════════════════════════╝
```

Then per-domain detail:

```
▼ {도메인명} ({n}건)

  🔴 심각 ({n}건)
  ┌─────────────────────────────────────────────┐
  │ [{ID}] {title}                               │
  │ 파일: {file}:{line}                          │
  │ 코드: {code snippet}                         │
  │ 수정: {suggestion}                           │
  │ 상태: 🔧 자동수정 가능 / ⚠ 수동수정 필요      │
  └─────────────────────────────────────────────┘

  🟡 경고 ({n}건)
  ...

  🔵 권고 ({n}건)
  ...
```

7. **Offer auto-fix**: "자동수정 가능한 항목이 {n}건 있습니다. 어떻게 하시겠습니까?"
   (A) 전체 자동수정
   (B) 영역별 선택 수정
   (C) 건별 확인 후 수정
   (D) 수정하지 않음

8. **Execute fixes**: For option A/B, dispatch the govcheck-fixer agent.
   For option C, iterate violations one by one with user confirmation.
   For option D, done.

## Severity Mapping

| severity value | Display | Description |
|---------------|---------|-------------|
| critical | 🔴 심각 | 납품 시 반드시 걸림 |
| warning | 🟡 경고 | 검수자에 따라 걸릴 수 있음 |
| info | 🔵 권고 | 품질 향상 목적 |

## Important Rules

- Always show the summary table first, then details
- Group violations by severity within each domain
- For T2 violations you confirm as true: include in report with original confidence
- For T3 items: report as "Claude 분석" category with your assessment
- If total violations > 500: show summary only, suggest --only flag
- Respect .govcheckrc.json in the project root for path/ignore configuration
- Bar chart: use █ for filled and ░ for empty, scale to max 12 characters

## Error Handling

- If MCP returns `NO_FILES_MATCHED` for a domain: skip that domain, show "해당 파일 없음" in summary
- If MCP returns `truncated: true` with `reason: "timeout"`: show partial results with "⏱ 시간초과 — 일부 결과" note
- If no JSP files found: skip accessibility/webstandard scans automatically
- If no Java files found: skip securecoding scan automatically
- If MCP server is unreachable: inform user to check plugin installation
