# AGENTS.md

## Project
`local-delegation-field-admin` is a static Next.js explorer for the 166 field-execution / supervisory-management delegation review tasks.

## Rules
- Keep the site static-export compatible for GitHub Pages.
- Do not add server-only APIs.
- Source data lives in `app/data/delegation.json` and should be regenerated from the analysis CSVs when needed.
- Preserve the core analysis axes:
  1. 법률상 지자체 유형
  2. 시행령 현재 수임자/상태
  3. 사무 성격
  4. 추진단계
- Avoid implying final legal conclusions. Use “검토”, “후보”, “쟁점관리” language.

## Commands
```bash
npm run build
```
