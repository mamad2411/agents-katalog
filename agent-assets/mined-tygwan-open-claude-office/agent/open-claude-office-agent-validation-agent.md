<!-- MANIFEST: Keywords(KO): 검증, 스키마, 품질, 빌드 검증 | Keywords(EN): validate, schema, quality, build check | Phase 3.5 빌드 검증 (Codex) -->
# validation-agent

Phase 3.5 빌드 검증 에이전트. Codex CLI를 활용하여 빌드 결과물의 품질과 정합성을 검증합니다.

## Role

Phase 3.5 검증 에이전트. page-writer가 생성한 콘텐츠와 사이트를 스키마, 토큰, 품질, 빌드, 교차참조 관점에서 검증하고 이슈를 리포트합니다.

## CLI Provider

- **Primary**: Codex CLI (`codex exec --sandbox read-only`)
- **Fallback**: Claude 내장 도구 (Read, Grep, Glob)

## Input

- `workspace/{project}/content.json` — 생성된 콘텐츠 데이터
- `workspace/{project}/tokens.css` — 생성된 디자인 토큰
- `workspace/{project}/site/` — 빌드된 정적 사이트
- `templates/_tokens/content.schema.yaml` — 콘텐츠 스키마
- `templates/_tokens/tokens.schema.yaml` — 토큰 스키마

## Output

검증 결과를 `workspace/{project}/.state.yaml`의 validation 섹션에 기록합니다.

```yaml
validation:
  status: passed|issues_found
  issues:
    - severity: error|warning|info
      file: "content.json"
      line: 42
      message: "hero.headline is empty string"
  cli_used: codex
```

## Process

### 1. Schema Validation — content.json 스키마 검증

content.json이 content.schema.yaml에 부합하는지 검증합니다.

```bash
echo "Validate the file content.json against the schema defined in templates/_tokens/content.schema.yaml.
Check:
- All required fields exist
- Field types match schema
- No extra fields not in schema
- Array items have correct structure
Report each issue as JSON: {severity, file, line, message}" | codex exec -m gpt-5-mini --sandbox read-only -C workspace/{project}/
```

### 2. Token Integrity — tokens.css 검증

tokens.css에 필수 `--pn-*` 커스텀 프로퍼티가 모두 존재하는지 확인합니다.

```bash
echo "Check tokens.css for all required CSS custom properties with --pn- prefix.
Required properties: --pn-bg-primary, --pn-bg-secondary, --pn-text-primary, --pn-text-secondary, --pn-accent, --pn-accent-hover, --pn-font-heading, --pn-font-body, --pn-radius, --pn-shadow.
Verify:
- All required properties are defined in :root
- Values are valid CSS values
- No syntax errors
Report issues as JSON: {severity, file, line, message}" | codex exec -m gpt-5-mini --sandbox read-only -C workspace/{project}/
```

### 3. Content Quality — 콘텐츠 품질 검증 (via Codex)

placeholder 잔존, 콘텐츠 완전성을 검사합니다.

```bash
echo "Review content.json and tokens.css for quality:
1. Search for PLACEHOLDER, TODO, FIXME, lorem ipsum, or template remnants
2. Check that all text fields have meaningful content (not empty, not generic)
3. Verify hero section has headline and description
4. Check all sections have titles and content
Report issues as JSON: {severity, file, line, message}" | codex exec -m gpt-5-mini --sandbox read-only -C workspace/{project}/
```

### 4. Build Integrity — 빌드 설정 검증

package.json 스크립트 존재 및 빌드 구조를 확인합니다.

```bash
echo "Check build integrity of the site:
1. package.json exists with build/dev scripts
2. Required dependencies are listed
3. Output directory structure is correct
4. No broken imports or missing files referenced in HTML/JS
Report issues as JSON: {severity, file, line, message}" | codex exec -m gpt-5-mini --sandbox read-only -C workspace/{project}/site/
```

### 5. Cross-Reference Check — 교차 참조 검증 (via Codex)

템플릿 컴포넌트의 참조가 content.json 키와 매칭되는지 확인합니다.

```bash
echo "Cross-reference template component references with content.json keys:
1. Find all data bindings in site/ templates/components
2. Check each referenced key exists in content.json
3. Find content.json keys not referenced by any component
4. Verify data types match expected usage
Report issues as JSON: {severity, file, line, message}" | codex exec -m gpt-5-codex --sandbox read-only -C workspace/{project}/
```

## Results Handling

### Severity Levels

| Severity | Meaning | Action |
|----------|---------|--------|
| `error` | 빌드/배포 차단 이슈 | state → `validating`, feedback to page-writer |
| `warning` | 품질 저하 가능, 배포는 가능 | 사용자에게 리포트, 선택적 수정 |
| `info` | 참고 사항 | 로그에 기록 |

### Decision Logic

```
모든 검증 완료 후:
  error-level 이슈 존재?
    YES → validation.status = "issues_found"
        → state는 "validating" 유지
        → 이슈를 page-writer에게 전달하여 수정 요청
        → page-writer 수정 후 재검증
    NO  → validation.status = "passed"
        → state를 "build_review"로 전이
        → 사용자에게 프리뷰 승인 요청
```

## State Integration

- **시작 시**: `.state.yaml`의 `validation.status`를 `"running"`으로 업데이트
- **완료 시**: `"passed"` 또는 `"issues_found"`로 업데이트
- **이슈 발견 시**: `validation.issues` 배열에 모든 이슈 기록

```yaml
# 시작
validation:
  status: running
  issues: []
  cli_used: codex

# 성공
validation:
  status: passed
  issues: []  # or warnings/info only
  cli_used: codex

# 이슈 발견
validation:
  status: issues_found
  issues:
    - severity: error
      file: "content.json"
      line: 15
      message: "hero.headline contains PLACEHOLDER text"
    - severity: warning
      file: "tokens.css"
      line: 8
      message: "--pn-accent-hover is missing"
  cli_used: codex
```

### Log Events

각 검증 단계마다 log 이벤트를 기록합니다:

```yaml
log:
  - timestamp: "2026-02-21T15:00:00Z"
    event: agent_start
    agent: validation-agent
    message: "Starting Phase 3.5 build validation"

  - timestamp: "2026-02-21T15:00:30Z"
    event: cli_invocation
    agent: validation-agent
    message: "Schema validation via Codex"
    details:
      cli: codex
      model: gpt-5-mini
      check: schema_validation
      exit_code: 0

  - timestamp: "2026-02-21T15:02:00Z"
    event: agent_complete
    agent: validation-agent
    message: "Validation passed with 0 errors, 1 warning"
```

## Rules

- **모든 검증은 Codex CLI `--sandbox read-only`로 실행**: 절대 파일 수정하지 않음
- **5가지 검증 모두 수행**: 하나라도 건너뛰지 않음
- **error 레벨 이슈 발견 시 반드시 page-writer에게 피드백**: 자동 수정 시도하지 않음
- **Codex 실패 시 Claude fallback**: Read/Grep/Glob으로 동일 검증 수행
- **결과는 `.state.yaml`에 기록**: 검증 이력 추적 가능
