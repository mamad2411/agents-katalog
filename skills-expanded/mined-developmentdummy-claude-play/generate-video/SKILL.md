---
name: generate-video
description: claude-play-bridge MCP 서버로 영상을 생성한다. 로컬 ComfyUI의 영상 워크플로 패키지(MiniMax H3 = 영상+오디오 동시 생성, WAN 2.2 i2v, Z-Image→영상)를 호출한다. 렌더가 수 분~수십 분 걸리므로 async 큐잉 + 파일 폴링이 기본 절차다. "영상", "동영상", "비디오", "video", "i2v", "t2v", "클립 만들어", "움직이는", "애니메이션 영상" 요청에 트리거된다.
---

# 영상 생성 (claude-play-bridge)

같은 PC에서 실행 중인 Claude Play 브릿지를 통해 로컬 ComfyUI 영상 워크플로를 돌린다.
브릿지 서버(기본 포트 {{PORT}})와 ComfyUI가 둘 다 켜져 있어야 한다.

이미지 생성은 `generate-image` 스킬을 쓴다. 이 스킬은 **영상 전용**이다.

## 0. 시작 전 30초 체크

```
mcp__claude-play-bridge__comfyui_health          → ComfyUI 연결 확인
mcp__claude-play-bridge__comfyui_workflow(list)  → 사용 가능한 워크플로 패키지 목록
```

영상 패키지의 파라미터 전체 설명(프롬프트 작성법 포함)은 **반드시** 여기서 읽는다:

```
mcp__claude-play-bridge__comfyui_workflow(action="get", name="minimax-h3-video")
```

이 스킬 문서는 절차와 함정만 다룬다. **파라미터의 실측 근거와 프롬프트 문법은 패키지 params 설명이 1차 진실**이다.

## 1. ⭐ 가장 중요한 두 가지

### (1) filename 확장자를 실제 출력 포맷에 맞춰라

렌더 대기 예산은 브릿지가 **제출 그래프에 영상 출력 노드가 있는지**로 판단하므로, 파일명을 어떻게 짓든 타임아웃이 잘못 걸리지는 않는다. 다만 **파일 내용과 확장자가 어긋나면 재생이 안 된다**. 패키지별 실제 포맷은 이렇다.

| 워크플로 계열 | 실제 출력 포맷 | filename |
|---|---|---|
| `minimax-h3-video`, `minimax-h3-video-turbo` | mp4 (SaveVideo) | `clip01.mp4` |
| `wan-i2v`, `wan-i2v-real`, `zimage-to-video` | 애니메이션 webp (SaveAnimatedWEBP) | `clip01.webp` |

`filename`을 생략하면 기본값이 `comfyui_<타임스탬프>.png`가 되어 mp4 내용이 `.png` 이름으로 저장된다. 영상 호출에서 `filename`은 사실상 필수다.

### (2) 영상은 async로 던지고 파일로 확인한다

MiniMax H3 15초물은 12~40분이 걸린다. MCP 도구 호출을 그 시간 동안 동기로 붙잡고 있으면 클라이언트 쪽 유휴 타임아웃(HTTP MCP 기본 5분)에 먼저 끊긴다.

```
mcp__claude-play-bridge__comfyui_generate(
  outputDir = "<이 프로젝트의 절대 경로>/out",
  workflow  = "minimax-h3-video",
  filename  = "shot01.mp4",
  async     = true,
  params    = { ... }
)
→ 즉시 { status: "queued", path: "<outputDir>/shot01.mp4", async: true } 반환
```

그다음 **로컬 파일 시스템을 폴링**한다. 산출물은 `outputDir` 직하에 그 이름 그대로 떨어진다.

- 성공: `<outputDir>/shot01.mp4` 가 생긴다.
- 실패: `<outputDir>/shot01.mp4.error.txt` 가 생기고 안에 사유가 적혀 있다.
- 폴링 간격은 30~60초, 상한은 워크플로별 예상 시간의 2배로 잡는다.
- **샷마다 고유한 filename을 써라.** 같은 이름으로 재시도하면 이전 실행이 남긴 파일을 보고 "이미 완료"로 오판한다.

짧은 클립(WAN 6스텝, 3~5초물)은 보통 1~3분이라 `async` 없이 동기로 기다려도 되지만, 큐가 밀려 있으면 동일하게 위험하다. **기본은 async로 통일하라.**

## 2. 워크플로 고르기

| 패키지 | 쓰는 상황 | 오디오 | 입력 | 대략 소요 |
|---|---|---|---|---|
| `minimax-h3-video` | 최대 15초, 대사·효과음·BGM까지 한 번에. 품질 기준선 | **네이티브 동시 생성** | 없어도 됨(t2v) / 첫 프레임(i2v) | 1152×640 L362 20스텝 ≈ 36분 |
| `minimax-h3-video-turbo` | 위와 같은 그래프에 전용 Turbo 노드. 드래프트·반복 확인용 | 동일 | 동일 | 6~8스텝, 기준선의 1/3 이하 |
| `wan-i2v` | 이미지 1장 → 3~5초 애니 클립 | 없음 | **시작 이미지 필수** | lightning 6스텝, 수 분 |
| `wan-i2v-real` | 위의 실사 튜닝(RealESRGAN 업스케일) | 없음 | 시작 이미지 필수 | 수 분 |
| `zimage-to-video` | 텍스트만으로 실사 베이스 생성 → 그대로 영상까지 | 없음 | 없음 | 수 분 |

고르는 기준 한 줄: **소리가 필요하거나 10초를 넘기면 H3, 이미 이미지가 있고 몇 초만 움직이면 WAN.**

## 3. MiniMax H3 — 최소 호출 예시

```
params = {
  prompt: "<4단 필드 구조. 아래 참조>",
  width: 1152, height: 640,   // 15초물의 실용 최대치. 1344×768로 15초는 금지(약 3시간)
  length: 362,                 // 24fps 기준 프레임 수. 124(5.17초)~362(15.08초)가 훈련 범위
  steps: 20,                   // 기준선. turbo 패키지는 6~8
  lufs: -20                    // 오디오 정규화. 원본 레벨이 -14~-47로 튀므로 필수
}
```

H3에는 `negative_prompt` 파라미터가 없다(툴이 기본값을 채워 보내도 패키지가 무시한다). 원하지 않는 것은 ①번 매체 선언 문단에 평범한 말로 적는다. WAN 계열은 반대로 `negative_prompt`가 실제로 동작한다.

프롬프트는 한 덩어리 문장으로 쓰면 눈에 띄게 나빠진다. **4단 필드 구조**로 쓴다:

1. **매체 선언** — `2D-animated Japanese anime, hand-inked line art, flat cel-shading` 처럼 매체를 평범한 말로 선언하고 유지할 것을 지목. 부정 지시도 여기(`no 3D rendering, no photorealism`).
2. **`[Shot N]` 시각 서술 + 카메라** — 두 번째 샷부터 `[Shot 2] At 00:05.200, hard cut to ...` (타임스탬프는 프레임 단위로 지켜진다). 카메라는 샷 끝에 `Camera: <무브> at <속도> speed with <크기> amplitude`로 분리. 컷이 바뀌면 의상을 다시 해석하므로 샷마다 의상을 반복 명시.
3. **Soundscape** — 앰비언스·폴리를 별도 문단으로. 없으면 `N/A`.
4. **Music** — 악기명 + 타임스탬프(`A low drone enters at 0s; strings join at 3s`). 없으면 `N/A`.
5. **대사** — `<d>[Korean] 대사 내용</d>`. 화자 ID와 목소리 묘사는 태그 **밖**에. 대사를 안 쓰면 모델이 어느 언어도 아닌 웅얼거림을 만든다.

H3가 **못 하는 것**: 정확한 개수 지정(`exactly three`), 개체별 역할 부여(`두 번째 것만 잡아라`), 소품을 집었다 놓는 동작(개체가 복제된다). 소품이 화면에 있어야 하면 `The single mug stays on the floor untouched for the entire shot`처럼 고정 명령을 박는다.
**잘 하는 것**: 텍스트 렌더링, 좌우 소품 배치, 다중 인물 속성 결합, 호흡·눈·고개 각도·어깨 연기.

## 4. i2v / FLF2V — 입력 이미지를 넘기는 법

이미지 파라미터(`first_frame`, `last_frame`, `start_image`, `end_image`)는 **두 가지 형태**를 받는다.

1. **슬래시가 포함된 상대 경로** → 브릿지가 `outputDir` 기준으로 파일을 찾아 ComfyUI에 자동 업로드한다. 외부 프로젝트에서는 이 방식을 쓴다.
   ```
   outputDir = "D:/myproj/out"
   params.first_frame = "images/base01.png"   // 실제 파일: D:/myproj/out/images/base01.png
   ```
   `outputDir` 직하도 되지만 슬래시가 없으면 아래 2번으로 해석되니, **반드시 하위 디렉터리를 하나 끼워라**.
2. **슬래시 없는 순수 파일명** → ComfyUI의 `input/` 디렉터리에 이미 있는 파일로 간주한다.

H3에서 `first_frame`을 생략하면 t2v로, 주면 i2v로 자동 분기한다. `last_frame`까지 주면 FLF2V(끝 프레임 수렴)가 되어 후반부 드리프트가 줄고 다음 세그먼트와의 이음새를 고정할 수 있다. WAN은 `start_image`가 **필수**다.

첫 프레임의 공간감이 곧 영상의 공간감이다. 창·하늘이 프레임을 다 먹은 스틸을 넣으면 인물이 공중에 뜬 것처럼 나온다. 인물 뒤에 물체(벽·침대·선반)가 있고 바닥이 카메라 쪽으로 뻗은 스틸을 쓴다.

## 5. 실패했을 때

| 증상 | 원인 | 조치 |
|---|---|---|
| 5분쯤 호출이 끊김 | 동기 호출 + 클라이언트 유휴 타임아웃(HTTP MCP 기본 5분) | `async: true`로 전환 후 파일 폴링 |
| 파일이 안 생기고 `.error.txt`만 있음 | 렌더 실패 | 파일 내용의 사유를 읽고 조치 |
| `ComfyUI is not connected` (503) | ComfyUI 미기동 | `comfyui_health`로 확인 후 사용자에게 기동 요청 |
| 400 + 누락 파라미터명 | 필수 파라미터 빠짐 | `comfyui_workflow(get)`으로 required 확인 |
| 파일은 나왔는데 재생 안 됨 | webp 출력에 `.mp4` 이름을 붙임 | 1절 표대로 확장자 교정 |
| 오디오가 너무 크거나 작음 | `lufs` 기본값 | -20 기준, 더 조용히는 -23 |

## 6. 경계와 예외

**기본 경로는 브릿지 MCP다.** ComfyUI(`127.0.0.1:8188`)를 임의로 직접 호출하지 마라 — 워크플로 패키지가 해상도 스냅·오디오 정규화·i2v 분기·산출물 회수를 대신 처리한다.

**예외**: 함께 설치된 고급 스킬 `minimax-h3` / `h3-longtake` / `long-video-chaining` / `video-sound-design`은 설계상 같은 PC의 ComfyUI를 직접 다루는 **로컬 파이프라인**이다. 이 스킬로 처리되지 않는 작업 — 15초를 넘는 세그먼트 체이닝, MMAudio 사운드 레이어링, 장편 제작 — 에서는 그쪽 절차를 따른다. 그 문서들의 경로 예시는 원본 개발 환경 기준이므로 이 프로젝트에 맞게 바꿔 읽어야 한다.

## 7. 하지 말 것
- 렌더 시간을 줄이려고 `length`를 훈련 범위(124~362) 밖으로 내리지 마라. 짧게 하려면 `minimax-h3-video-turbo`로 스텝을 줄이는 쪽이 옳다.
- 한 번에 여러 영상을 병렬로 던지지 마라. GPU 한 장을 공유하므로 큐만 길어지고 예상 시간 계산이 무너진다.
