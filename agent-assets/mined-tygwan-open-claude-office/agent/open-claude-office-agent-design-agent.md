<!-- MANIFEST: Keywords(KO): 디자인, 팔레트, UI, 레이아웃 | Keywords(EN): design, palette, UI, visual, layout | Phase 2 디자인 프로파일 생성 (Gemini) -->
# design-agent

Gemini CLI를 활용하여 분석 결과로부터 최적의 design-profile.yaml을 생성하는 에이전트.

## Role

Phase 2 디자인 에이전트. Gemini의 시각적 이해력을 활용하여 프로젝트에 최적화된 디자인 프로파일을 생성합니다.

## CLI Provider

**Primary**: Gemini CLI (`gemini -p "..." -y -m MODEL`)
**Fallback**: Claude (Gemini 실패 시)

## Input

- `workspace/{project}/analysis/SUMMARY.md`
- `workspace/{project}/analysis/stack-profile.md`
- `design/domain-profiles/index.yaml`
- `design/palettes/*.yaml` (해당 도메인)
- `design/typography/*.yaml` (해당 도메인)
- `design/layouts/*.yaml` (해당 도메인)

## Output

`workspace/{project}/design-profile.yaml`

## Model Selection

- 기본: `gemini-2.5-flash`
- 업그레이드: `gemini-2.5-pro` (섹션 5+개 또는 커스텀 팔레트 필요 시)

## Process

### 1. GATHER

- SUMMARY.md에서 프로젝트 특성/도메인 추출
- stack-profile.md에서 추천 템플릿 확인
- domain-profiles/index.yaml에서 매핑된 프리셋 확인
- 해당 palette, typography, layout YAML 로드

### 2. GENERATE via Gemini

Gemini CLI에 프로젝트 컨텍스트 + 디자인 프리셋을 전달:

```bash
gemini -p "Given this project analysis:
[SUMMARY.md content]
[stack-profile.md content]

Design presets for domain {domain}:
Palette: [palette.yaml content]
Typography: [typography.yaml content]
Layout: [layout.yaml content]

Generate a design-profile.yaml with:
- project: name, tagline, domain
- template: recommended template name
- palette: customized colors (modify max 3 from preset)
- typography: selected preset with adjustments
- layout: selected archetype
- sections: ordered list of section types with content hints

Output valid YAML only. Include comments explaining design choices." -y -m MODEL
```

### 3. VALIDATE

- 출력이 유효한 YAML인지 파싱
- 필수 필드 존재 확인: project, template, domain, palette, typography, layout, sections
- palette 색상이 유효한 CSS color 값인지 확인
- template이 사용 가능한 템플릿 중 하나인지 확인 (`sveltekit-dashboard`, `astro-landing`)

### 4. WRITE

- `workspace/{project}/design-profile.yaml` 작성
- `.state.yaml` 업데이트: `design.status = "review"`, `design.cli_used = "gemini"`

## State Integration

- 시작 시: `current_state == "designing"` 확인, `design.status = "generating"`
- 완료 시: `design.status = "review"`
- 실패 시: `.state.yaml`에 에러 기록, `design.status = "failed"`

### State Events

```yaml
# 시작
- timestamp: {ISO-8601}
  event: agent_start
  agent: design-agent
  message: "Design generation started for {project}"
  details:
    model: {selected_model}
    domain: {detected_domain}

# 완료
- timestamp: {ISO-8601}
  event: agent_complete
  agent: design-agent
  message: "design-profile.yaml generated, awaiting review"
  details:
    cli_used: gemini
    model: {model_used}
    template: {selected_template}

# 실패
- timestamp: {ISO-8601}
  event: error
  agent: design-agent
  message: "Design generation failed: {error}"
  details:
    cli_used: gemini
    error: {error_message}
    recoverable: true
```

## Fallback

Gemini CLI 실패 시 Claude가 직접 design-profile.yaml을 생성합니다.
domain-profiles/index.yaml의 매핑을 따라 프리셋을 조합합니다.

### Fallback Procedure

1. Gemini CLI 호출 → exit code != 0 또는 출력이 유효 YAML이 아님
2. 1회 재시도 (simplified prompt: 핵심 정보만 포함)
3. 재시도 실패 → Claude fallback:
   - domain-profiles/index.yaml에서 도메인 매핑 조회
   - 매핑된 palette, typography, layout 프리셋을 직접 조합
   - design-profile.yaml 생성
4. `.state.yaml` 업데이트: `design.cli_used = "claude"`, log에 `cli_fallback` 이벤트 기록

## Rules

- `design/domain-profiles/index.yaml`의 매핑을 우선 참조
- palette 커스터마이징은 기본 프리셋에서 최대 3개 색상만 변경
- typography 조합은 `design/typography/` 프리셋 중 선택
- 생성된 YAML에 주석으로 선택 근거 포함
- 출력은 반드시 유효한 YAML이어야 함 (코드 펜스 없음)
