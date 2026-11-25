---
name: hermit-audit
description: |
  Hermit + Claude Code 종합 감사 (read-only) — 8축 28항목 체크리스트로 Hermit/CC 환경(토큰 경제, 모델 라우팅, 스킬·훅·룰·MCP·세션 습관)을 평가.
  Git-shipped audit tool. 2026 best-practice adoption 검증용.

  Trigger: "/hermit-audit", "hermit audit", "hermit 감사", "hermit 점검", "토큰 감사", "cache hit rate", "MCP 오버헤드", "토큰 최적화 점검"
---

# /hermit-audit — Hermit + CC 종합 감사

**8축 평가 사이클**: 구조 → 맥락 → 계획 → 실행 → 검증 → 개선 → **토큰 경제** → **모델 라우팅**

체크리스트 원본: `references/checklist.md` (반드시 먼저 읽어 항목 정의 확인).

> **분석의 정의**: 갖춘 것(Static)과 실제로 하는 것(Behavioral)의 **gap**을, User/Project 두 스코프에서 측정.
> 축 7-8은 Hermit 전용 — CC 환경에서는 N/A 처리.

---

## 8축 매핑 개요

| 축 | 이름 | 항목 수 | 출처 |
|---|---|---|---|
| 1 | 구조 (Structure) | 3 | check-harness 6축에서 차용 |
| 2 | 맥락 (Context) | 3 | check-harness 6축에서 차용 |
| 3 | 계획 (Plan) | 2 | check-harness 6축에서 차용 |
| 4 | 실행 (Execution) | 3 | check-harness 6축에서 차용 |
| 5 | 검증 (Verification) | 2 | check-harness 6축에서 차용 |
| 6 | 개선 (Improvement) | 2 | check-harness 6축에서 차용 |
| 7 | 토큰 경제 (Token Economy) | 6 | **신규 — Hermit 전용** |
| 8 | 모델 라우팅 (Model Routing) | 4 | **신규 — Hermit 전용** |

총 항목: **25개** (15 + 6 + 4)

축 1-6은 check-harness의 검증된 6축 프레임워크를 그대로 상속한다.
이 스킬의 핵심 가치는 **축 7-8** — Hermit 환경에만 존재하는 토큰 경제 및 모델 라우팅 지표.

---

## D-minimal 실행 절차

Python 스크립트 없이 수동 체크리스트 스캔으로 실행한다.

### Step 0 — 준비

```bash
# 작업 디렉토리 생성
mkdir -p /tmp/hermit-audit/

# checklist.md 읽기 (항목 정의 확인)
cat hermit_agent/skills/hermit_audit/references/checklist.md
```

### Step 1 — 축 1-6 (CC 하네스 공통)

각 항목을 `references/checklist.md` 기준으로 수동 확인.
파일 존재 여부, 설정값 유무 등 정적 지표는 bash로 검증:

```bash
# 축 1: 구조
ls ~/.claude/skills/ 2>/dev/null | head -20
ls ~/.claude/rules/ 2>/dev/null
cat ~/.claude/settings.json 2>/dev/null | python3 -m json.tool | grep -A5 hooks

# 축 2: 맥락
wc -w ~/.claude/CLAUDE.md 2>/dev/null
wc -w CLAUDE.md 2>/dev/null

# 축 4: 실행
cat ~/.claude/settings.json 2>/dev/null | python3 -m json.tool | grep -A3 mcpServers
```

### Step 2 — 축 7 (Token Economy)

```bash
# T1: CLAUDE.md 토큰 추정 (wc -w × 1.3)
echo "Global CLAUDE.md words: $(wc -w < ~/.claude/CLAUDE.md 2>/dev/null || echo 0)"
echo "Project CLAUDE.md words: $(wc -w < CLAUDE.md 2>/dev/null || echo 0)"

# T2: rules 파일 토큰 합계
echo "Global rules tokens:"
for f in ~/.claude/rules/*.md; do
  words=$(wc -w < "$f" 2>/dev/null || echo 0)
  tokens=$(python3 -c "print(int($words * 1.3))")
  echo "  $f: ~$tokens tokens"
done

# T5: MCP 서버 수
python3 -c "
import json, os
s = json.load(open(os.path.expanduser('~/.claude/settings.json')))
mcp = s.get('mcpServers', {})
print(f'MCP servers: {len(mcp)} — {list(mcp.keys())}')
" 2>/dev/null || echo "settings.json not found or no mcpServers"

# T6: Skill phased header 채택률
grep -l "## Phase" ~/.claude/skills/**/SKILL.md 2>/dev/null | wc -l
```

### Step 3 — 축 8 (Model Routing)

Gateway DB 또는 로그에서 수동 샘플링:

```bash
# Gateway usage 로그 확인 (파일 위치는 프로젝트 설정에 따라 다름)
# M3: 로컬 vs 클라우드 분산
sqlite3 ~/.hermit/gateway.db "
  SELECT model, count(*) as cnt
  FROM usage
  GROUP BY model
  ORDER BY cnt DESC
  LIMIT 10;
" 2>/dev/null || echo "Gateway DB not available — check hermit_agent/gateway/ for log path"

# M4: session log에서 Monitor vs sleep 패턴
ls ~/.hermit/sessions/ 2>/dev/null | tail -5
```

### Step 4 — 결과 렌더

`/tmp/hermit-audit/report-$(date +%Y%m%d).md` 에 아래 형식으로 저장:

```markdown
# Hermit Audit Report — YYYY-MM-DD

## Scorecard
| Axis | Score | Level |
|------|-------|-------|
| 1 구조 | PASS/WEAK_PASS/FAIL | L1/L2/L3 |
...
| 7 Token Economy | | |
| 8 Model Routing | | |

## Quick Wins
- ...

## Action Items (P1)
- ...
```

---

## Future Work (D-full)

다음 항목은 D-full iteration(축 A/B/C 완료 후)에서 구현:

- `scripts/audit_cc.py` — CC 하네스 지표 자동 수집 (settings.json, skills/, rules/ 파싱)
- `scripts/audit_hermit.py` — Gateway DB 쿼리, session log 분석, model 분포 계산
- `scripts/render_report.py` — 8축 스코어카드 HTML/Markdown 렌더러
- 서브에이전트 병렬 실행 (check-harness Phase 1 패턴 참조)
- Gateway DB `usage` 테이블 기반 T1(cache hit rate) 자동 측정

---

## 자매 스킬과의 구분

| 목적 | 스킬 |
|------|------|
| CC 하네스만 진단 | `/check-harness` |
| Hermit + CC 통합 감사 | `/hermit-audit` (이 스킬) |
| 설정 파일 수정까지 | `/update-config` |
