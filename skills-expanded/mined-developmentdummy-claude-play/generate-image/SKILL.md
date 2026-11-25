---
name: generate-image
description: claude-play-bridge MCP 서버로 이미지를 생성한다. 기본 백엔드는 ComfyUI(로컬 GPU, 워크플로 패키지 기반)이고, 사용자가 명시적으로 요청할 때만 GPT/Gemini 백엔드를 사용한다.
---

# 이미지 생성 (claude-play-bridge)

같은 PC에서 실행 중인 Claude Play 브릿지의 이미지 생성 기능을 MCP로 사용한다.
브릿지 서버가 켜져 있어야 한다 (기본 포트 {{PORT}}).

**영상(동영상/클립)을 만들 때는 이 스킬이 아니라 `generate-video` 스킬을 쓴다.**

## 도구 요약

| 도구 | 용도 |
|---|---|
| `mcp__claude-play-bridge__comfyui_generate` | **기본 백엔드.** ComfyUI 워크플로 패키지로 생성 (로컬 GPU, 무비용) |
| `mcp__claude-play-bridge__generate_image_openai` | GPT 이미지 — 텍스트 렌더링·레퍼런스 편집에 강함. **사용자가 명시 요청할 때만** |
| `mcp__claude-play-bridge__generate_image_gemini` | Gemini 이미지 — **사용자가 명시 요청할 때만** |
| `mcp__claude-play-bridge__comfyui_health` | ComfyUI 연결 상태 확인 |
| `mcp__claude-play-bridge__comfyui_models` | 체크포인트/LoRA 목록 |
| `mcp__claude-play-bridge__comfyui_workflow` | 워크플로 패키지 조회 (list/get, 읽기 전용) |

## 공통 규칙

- **`outputDir`은 절대경로 필수.** 생성된 파일은 `outputDir` 바로 아래에 저장되고 응답에 절대경로가 돌아온다.
- `filename`은 파일명만 (`foo.png`). 경로 접두사를 붙이지 말 것.
- 모든 생성 도구는 동기 — 응답이 오면 파일이 이미 존재한다.

## ComfyUI 생성 절차

1. 첫 사용 전 `comfyui_health`로 연결 확인. unreachable이면 사용자에게 ComfyUI 기동을 요청.
2. `comfyui_workflow` `{"action":"list"}`로 사용 가능한 워크플로 패키지와 파라미터를 확인.
3. 프롬프트는 Danbooru 스타일 태그 나열이 기본 (예: `1girl, silver hair, blue eyes, portrait, smile`).
   품질 태그는 패키지가 자동으로 붙이므로 본문 태그만 작성한다.
4. 생성:

```json
{
  "outputDir": "C:\\path\\to\\my\\project\\assets",
  "workflow": "portrait",
  "prompt": "1girl, silver hair, blue eyes, gentle smile, upper body",
  "filename": "heroine.png"
}
```

- `workflow` 생략 시 브릿지의 활성 프리셋 기본 템플릿 사용.
- 고급 파라미터(`width`/`height`/`steps` 등)는 `params` 객체로 — 패키지의 params.json 스키마(`comfyui_workflow` get으로 확인)를 따른다.
- LoRA는 `loras: [{"name": "...", "strength": 0.8}]` — 이름은 `comfyui_models`에서 확인.

## GPT/Gemini 백엔드 (명시 요청 시에만)

- `generate_image_openai`: 텍스트가 들어간 이미지(로고·UI목업·포스터)나 레퍼런스 기반 편집(`reference_image`)에 강함.
- `generate_image_gemini`: `aspect_ratio`/`image_size` 지정 가능, 다중 레퍼런스 지원.
- `reference_image` 경로는 `outputDir` 기준 상대경로 또는 절대경로.

## 트러블슈팅

- `Unauthorized` → 토큰 불일치. 브릿지 쪽에서 `node scripts/setup-external.mjs <이 프로젝트 경로>` 재실행.
- `ComfyUI is not connected` → 브릿지 PC에서 ComfyUI 미기동. 사용자에게 알린다.
- 연결 자체가 안 됨 → 브릿지 서버 미기동. 사용자에게 브릿지 실행(`npm run dev`)을 요청.
