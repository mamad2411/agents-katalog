---
name: generate-image-openai
description: OpenAI/GPT 이미지 생성(GPT Image 품질 / 텍스트 렌더링·이미지 편집 강점). 기본 백엔드는 Codex CLI 구독(건당 과금 없음). ⚠️ 사용자가 이 백엔드를 명시적으로 지정했을 때만 사용한다(예 "GPT로/OpenAI로 그려줘"). 기본 이미지 생성은 generate-image(ComfyUI)이며, 사용자가 콕 집어 요청하지 않았다면 절대 OpenAI를 자동으로 선택하지 마라.
allowed-tools: Bash, Read, Write
---

# 이미지 생성 (OpenAI/GPT · GPT Image)

GPT Image 품질의 이미지를 생성한다. 자연어 영어 프롬프트를 사용하며, 텍스트 렌더링·지시 충실도가 강점이다. `referenceImage`를 함께 보내면 기존 이미지의 변형/편집이 가능하다.

> 렌더링 백엔드는 서버가 결정한다(환경변수 `OPENAI_IMAGE_BACKEND`). 기본값 `codex`는 Codex CLI의 내장 `image_gen` 툴로 **ChatGPT 구독을 통해 렌더링**(건당 API 과금 없음, 대신 에이전트 턴이라 느리고 구독 레이트리밋 적용). `api`로 바꾸면 메터링 OpenAI Responses API(`gpt-5.5`)를 쓴다. **이 스킬에서 호출 방식(아래 HTTP 요청)은 백엔드와 무관하게 동일하다 — 신경 쓸 필요 없다.**

## ⚠️ 사용 조건 — 명시적 요청 전용

**이 스킬은 사용자가 OpenAI/GPT 이미지 생성을 콕 집어 지정했을 때만 사용한다.** (예: "GPT로 그려줘", "OpenAI로 간판 만들어줘")

- 그 외 모든 이미지 생성(캐릭터, 장면, 패널 배경, 아이콘, 컨셉 아트, 텍스트 리소스 등)의 **기본 백엔드는 generate-image(ComfyUI)**다.
- 사용자가 백엔드를 지정하지 않았다면 **절대 OpenAI를 자동으로 고르지 마라.** ComfyUI로 생성하라. (텍스트 렌더링·정밀 구도가 필요해 보여도 마찬가지 — 사용자가 명시하지 않았으면 자동 전환 금지)
- ComfyUI를 쓸 수 없는 환경이더라도 자동 폴백하지 말고, **먼저 "OpenAI로 생성할까요?"라고 물어본 뒤** 사용자가 동의하면 사용한다.

아래는 사용자가 명시적으로 OpenAI를 요청했을 때를 위한 참고 사항이다. 이 백엔드는 **프롬프트를 그대로 따르는 정밀도**, **텍스트 렌더링**, **기존 이미지 편집(referenceImage)**이 강점이다.

## 절차

### 1단계: 프롬프트 구성

**영어 서술형 프롬프트**를 작성한다. Danbooru 태그 대신 자연어로 묘사한다. 모델은 긴 지시문을 잘 따른다.

좋은 프롬프트 예시:
```
A vintage wooden tavern sign hanging from a metal bracket. The sign reads "The Drunken Dragon" in gothic gold lettering, with a small painted dragon curling around the letters. Weathered wood texture, warm afternoon lighting, photorealistic.
```

```
A medieval scroll lying on a stone table, with the heading "ROYAL DECREE" written in elegant calligraphy in dark red ink, wax seal at the bottom, parchment texture, dramatic lighting, top-down view.
```

```
A character portrait split into four panels showing the same young woman with silver hair and blue eyes expressing: 1) joy, 2) anger, 3) sadness, 4) determination. Clean anime illustration style, consistent character design, neutral background.
```

### 2단계: API 호출

**저장 위치 결정 — 활성 세션에서는 `persona` 파라미터를 넘기지 마라.**

| 상황 | 권장 | 저장 위치 |
|---|---|---|
| 대화 세션 — 1회용 장면 | 둘 다 생략 | 활성 세션 dir |
| 대화 세션 — 영구 공유 자산 (definitions에서 참조) | `targetScope: "persona"` 단독 | 부모 페르소나 dir |
| 빌더 세션 (활성 세션 없음) | `persona: "<이름>"` 필수 | 명시한 페르소나 dir |

활성 세션에서 `persona`를 넘기면 라우팅이 빌더 모드로 잘못 해석돼 InlineImage가 이미지를 못 찾는다. 페르소나 공유 자산이 필요하면 `targetScope: "persona"`를 쓴다.

**빌더 세션** (persona 파라미터 필수):
```bash
cat > /tmp/openai-req.json << 'REQEOF'
{
  "prompt": "A vintage tavern sign reading 'The Drunken Dragon' in gothic gold lettering, weathered wood, warm lighting, photorealistic",
  "filename": "tavern-sign.png",
  "persona": "캐릭터이름"
}
REQEOF
curl -s -X POST "http://localhost:{{PORT}}/api/tools/openai/generate" \
  -H "Content-Type: application/json" \
  -d @/tmp/openai-req.json
```

**대화 세션** (활성 세션에 자동 저장):
```bash
curl -s -X POST "http://localhost:{{PORT}}/api/tools/openai/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A handwritten letter on cream paper, ink stains, vintage romantic atmosphere","filename":"love-letter.png"}'
```

**레퍼런스 이미지를 사용한 편집/변형** (`referenceImage` 필드):
```bash
cat > /tmp/openai-edit-req.json << 'REQEOF'
{
  "prompt": "Same character but now wearing a red winter coat and scarf, snowy background",
  "filename": "character-winter.png",
  "referenceImage": "images/character-base.png"
}
REQEOF
curl -s -X POST "http://localhost:{{PORT}}/api/tools/openai/generate" \
  -H "Content-Type: application/json" \
  -d @/tmp/openai-edit-req.json
```
`referenceImage`는 세션/페르소나 디렉토리 기준 상대 경로다. 이 필드가 있으면 자동으로 input_image로 첨부되고 image_generation 툴의 action이 `edit`로 설정된다.

**크기/품질 조정** (선택):
```json
{
  "prompt": "...",
  "filename": "scene.png",
  "size": "1024x1024",
  "quality": "high"
}
```
`size`: `"1024x1024"`, `"1536x1024"`, `"1024x1536"`, `"auto"`(기본). `quality`: `"low"`, `"medium"`, `"high"`, `"auto"`(기본).

### 3단계: 응답에 이미지 삽입

`<dialog_response>` 안에 `$IMAGE:images/파일명.png$` 토큰을 포함한다.
이미지는 비동기로 생성되므로 사용자 화면에서 로딩 스피너 → 완성 후 자동 교체된다.

---

## 활용 예시

### 텍스트가 포함된 UI 리소스
```json
{"prompt": "A wooden game UI button with the text 'START' carved into it, fantasy game style, glowing edges", "filename": "btn-start.png"}
```

### 정밀한 다중 패널 일러스트
```json
{"prompt": "A 3-panel comic strip: panel 1 shows a knight drawing his sword, panel 2 shows him charging at a dragon, panel 3 shows him standing victorious. Manga style, consistent character.", "filename": "battle-comic.png"}
```

### 기존 캐릭터 의상 변경 (편집)
```json
{"prompt": "Same character with the same face and hair, but now wearing formal ballroom attire", "filename": "character-ballroom.png", "referenceImage": "images/profile.png"}
```

### 텍스트가 포함된 장면 (편지, 메모, 간판 등)
```json
{"prompt": "A torn handwritten note on a wooden desk. The note reads 'Meet me at the old oak tree at midnight - L' in slanted blue ink. Soft natural light from a window.", "filename": "mystery-note.png"}
```

---

## 규칙

- **⚠ 호출을 최소화하라.** (기본 Codex 백엔드는 건당 과금은 없지만 한 장당 수십 초가 걸리고 구독 레이트리밋을 먹는다. `api` 백엔드면 유료다.)
  - 한번 생성한 이미지는 반드시 재사용한다 (`$IMAGE:images/filename.png$`)
  - 비슷한 이미지를 반복 생성하지 마라
  - 사용자가 명시적으로 요청하거나, 서사적으로 꼭 필요한 경우에만 생성한다
  - 재사용 가능한 리소스(배경, 아이콘, 캐릭터 변형)는 빌더 단계에서 미리 만들어 두라
  - 생성은 비동기다. 기본 Codex 백엔드는 완료까지 보통 40~60초 걸리니, 토큰(`$IMAGE:...$`)만 응답에 넣고 기다리지 말고 진행하라(완성 시 자동 교체).
- prompt는 **반드시 영어**로 작성한다. 영어 지시 충실도가 가장 높다
- filename은 영문 kebab-case `.png` (예: `tavern-sign.png`)
- **⚠ `filename` 파라미터에는 `images/` 접두사를 붙이지 마라.** 도구가 자동으로 `images/` 디렉토리 아래에 저장한다. `filename: "images/foo.png"` 로 호출하면 실제 저장 경로가 `images/images/foo.png` 가 되어 챗 토큰(`$IMAGE:images/foo.png$`)의 경로와 어긋나 404가 난다. 항상 파일명만 — `filename: "foo.png"` → 자동 저장 위치 `images/foo.png` → 챗 토큰 `$IMAGE:images/foo.png$`.
- persona 이름에 한글이 포함되면 heredoc + `@파일` 방식을 사용하라 (curl 인코딩 이슈 방지)
- `referenceImage`는 세션/페르소나 디렉토리 기준 **상대 경로**다. 절대 경로나 외부 URL은 거부된다
- OpenAI는 콘텐츠 정책이 있다. 거부당하면 프롬프트를 순화하거나 다른 백엔드(ComfyUI)로 우회하라
- 렌더링 백엔드는 환경변수 `OPENAI_IMAGE_BACKEND`로 결정된다 — `codex`(기본, 구독) / `api`(메터링, `OPENAI_IMAGE_MODEL`로 모델 지정·기본 `gpt-5.5`). 호출하는 쪽은 신경 쓸 필요 없다.
