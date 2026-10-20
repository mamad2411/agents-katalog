# /craft-preview — Local Build & Serve

생성된 사이트를 로컬에서 빌드하고 프리뷰합니다. Phase 3.5 검증을 포함합니다.

## Usage

```
/craft-preview <project-name>
```

## Arguments

- `project-name`: workspace 내 프로젝트명 (필수, site/ 존재해야 함)

## State Machine

### Guard
- `current_state`가 `building` 완료 (build sub-statuses 모두 done/true) 또는 `build_review`
- `content.json`, `tokens.css`, `site/` 모두 존재해야 함

### Transitions
```
building (완료) → validating (Phase 3.5) → build_review (preview 가능)
validating → building (이슈 발견 시 page-writer 수정 후 재빌드)
```

### Event Logging
- validation 시작: `state_transition` (building → validating)
- validation 결과: `validation_issue` (이슈 발견 시) 또는 `state_transition` (validating → build_review)
- preview 시작: `user_input` (사용자 preview 승인)

## Prerequisites

- `workspace/{project}/site/` 존재 (Phase 3 완료)
- `workspace/{project}/site/package.json` 존재

## Quality Gate Integration

Before serving the preview, the pipeline checks:
- If `quality-gate` skill is available, run pre-build validation
- Check `workspace/{project}/.state.yaml` for `quality_gate.pre_build` status
- If failed, show warnings but still allow preview (non-blocking)

## Process

### 1. Validation (Phase 3.5)

preview 전 validation-agent를 호출하여 빌드 결과물을 검증합니다:

1. `.state.yaml` current_state = `validating`, phase = 3.5
2. validation-agent 실행 (Codex CLI primary)
3. 검증 항목:
   - Schema 검증: content.json이 content.schema.yaml에 맞는지
   - Content Quality: PLACEHOLDER 잔여 확인
   - CSS Integrity: `--pn-*` 프로퍼티 정의 확인
   - Build 검증: `npm run build` 성공 여부
   - Cross-Reference: content.json과 tokens.css 간 참조 정합성
4. **Validation Passed**: `.state.yaml` current_state = `build_review`, preview 실행
5. **Validation Issues**:
   - error 레벨: 이슈 표시, page-writer 수정 필요 → `building` 상태로 회귀
   - warning/info: 이슈 표시하되 preview 진행

### 2. Build & Preview

1. `workspace/{project}/site/` 디렉토리 확인
2. 의존성 설치: `npm install`
3. 빌드: `npm run build`
4. 프리뷰: `npm run preview` 또는 `npx serve dist/`

## Template-specific Commands

### sveltekit-dashboard
```bash
cd workspace/{project}/site
npm install
npm run build    # → .svelte-kit/output/
npm run preview  # → localhost:4173
```

### astro-landing
```bash
cd workspace/{project}/site
npm install
npm run build    # → dist/
npm run preview  # → localhost:4321
```

## Validation Checks

빌드 전 확인:
- [ ] `content.json`이 PLACEHOLDER가 아닌지 확인
- [ ] `tokens.css`가 PLACEHOLDER가 아닌지 확인
- [ ] `package.json`의 scripts에 build, preview 존재

## Example

```
/craft-preview n8n
```
