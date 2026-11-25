---
name: generate-image-gemini
description: Gemini API로 이미지를 생성한다. 패널 배경, UI 리소스, 아이콘, 장면 삽화 등 디자인 리소스 제작에 사용한다. ComfyUI가 없을 때의 이미지 생성 대안이기도 하다.
allowed-tools: Bash, Read, Write
---

# 이미지 생성 (Gemini)

Google Gemini의 네이티브 이미지 생성 기능을 사용한다. 자연어 프롬프트로 이미지를 생성하며, Danbooru 태그 대신 서술형 영어 프롬프트를 사용한다.

## ComfyUI vs Gemini 사용 구분

| 용도 | ComfyUI | Gemini |
|---|---|---|
| 캐릭터 일러스트 (일관성 중요) | **우선** | 대안 |
| 패널 배경/텍스처/패턴 | - | **우선** |
| UI 아이콘/뱃지/장식 | - | **우선** |
| 장면 삽화/CG | 가능 | **가능** |
| 컨셉 아트/분위기 참고 | - | **우선** |

ComfyUI가 설정되어 있으면 캐릭터 일러스트에는 ComfyUI를 우선 사용하라 (LoRA/체크포인트로 스타일 일관성 유지 가능). Gemini는 범용 리소스 생성에 강점이 있다.

## 절차

### 1단계: 프롬프트 구성

**영어 서술형 프롬프트**를 작성한다. Danbooru 태그가 아닌 자연어로 원하는 이미지를 묘사한다.

좋은 프롬프트 예시:
```
A dark fantasy tavern interior with warm candlelight, wooden tables and barrels, stone walls covered in ivy, atmospheric fog, medieval aesthetic, digital painting style
```

```
A small pixel-art style icon of a golden key with a glowing aura, transparent background, game UI asset
```

```
An elegant watercolor portrait of a young woman with silver hair and blue eyes, wearing a white Victorian dress, soft lighting, dreamy atmosphere
```

### 2단계: API 호출

**빌더 세션** (persona 파라미터 필수):
```bash
cat > /tmp/gemini-req.json << 'REQEOF'
{
  "prompt": "A dark fantasy tavern interior with warm candlelight, wooden tables, stone walls, atmospheric, digital painting",
  "filename": "tavern-bg.png",
  "persona": "캐릭터이름"
}
REQEOF
curl -s -X POST "http://localhost:{{PORT}}/api/tools/gemini/generate" \
  -H "Content-Type: application/json" \
  -d @/tmp/gemini-req.json
```

**대화 세션** (활성 세션에 자동 저장):
```bash
curl -s -X POST "http://localhost:{{PORT}}/api/tools/gemini/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A moonlit forest path with fireflies, ethereal atmosphere","filename":"forest-night.png"}'
```

### 3단계: 응답에 이미지 삽입

`<dialog_response>` 안에 `$IMAGE:images/파일명.png$` 토큰을 포함한다.
이미지는 비동기 생성되므로 사용자 화면에서 로딩 스피너 → 완성 후 자동 교체.

---

## 활용 예시

### 패널 배경 이미지
```json
{"prompt": "Dark blue gradient texture with subtle starfield pattern, seamless, UI background", "filename": "panel-bg.png"}
```

### 장소 아이콘
```json
{"prompt": "A simple icon of a medieval castle tower, flat design, dark background, game UI style", "filename": "location-castle.png"}
```

### 장면 삽화
```json
{"prompt": "Two people sitting across from each other at a candlelit cafe table, warm atmosphere, anime illustration style, soft lighting", "filename": "cafe-scene.png"}
```

### 아이템 이미지
```json
{"prompt": "A glowing magical sword with blue runes on the blade, dark background, fantasy game item illustration", "filename": "magic-sword.png"}
```

---

## 규칙

- **⚠ Gemini 이미지 생성은 유료 API다. 호출을 최소화하라.**
  - 한번 생성한 이미지는 반드시 재사용한다 (`$IMAGE:images/filename.png$`)
  - 비슷한 이미지를 반복 생성하지 마라
  - 사용자가 명시적으로 요청하거나, 서사적으로 꼭 필요한 경우에만 생성한다
  - 재사용 가능한 리소스(배경, 아이콘 등)는 빌더 단계에서 미리 만들어 두라
- prompt는 **반드시 영어**로 작성한다
- filename은 영문 kebab-case `.png` (예: `tavern-bg.png`)
- **⚠ `filename` 파라미터에는 `images/` 접두사를 붙이지 마라.** 도구가 자동으로 `images/` 디렉토리 아래에 저장한다. `filename: "images/foo.png"` 로 호출하면 실제 저장 경로가 `images/images/foo.png` 가 되어 챗 토큰(`$IMAGE:images/foo.png$`)의 경로와 어긋나 404가 난다. 항상 파일명만 — `filename: "foo.png"` → 자동 저장 위치 `images/foo.png` → 챗 토큰 `$IMAGE:images/foo.png$`.
- persona 이름에 한글이 포함되면 heredoc + `@파일` 방식을 사용하라 (curl 인코딩 이슈 방지)
- Gemini는 콘텐츠 필터가 있을 수 있다. 거부당하면 프롬프트를 조정하라
