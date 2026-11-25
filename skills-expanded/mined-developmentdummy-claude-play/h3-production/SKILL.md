---
name: h3-production
description: MiniMax H3로 10분+ 스토리라인 영상(여행기/Vlog 톤)을 제작하는 파이프라인. 각본→샷리스트→검토 게이트→2-tier 렌더링(터보 드래프트/승인 후 파이널)→포스트(BGM 베드·loudnorm·J/L컷) 전 공정을 다룬다. 씬 3종 오디오 배분, 카메라 문법 로테이션, 목소리 일관성 하이브리드(TTS 내레이션+H3 대사), 실측 기반 제작 시간표를 포함한다. "장편", "10분 영상", "스토리라인", "브이로그 제작", "샷리스트", "제작 파이프라인", "드래프트 렌더" 키워드에 트리거된다.
---

# H3 장편 제작 파이프라인

## 한 줄 요약

**10분 영화는 프롬프트가 아니라 공장이다.** 종이 위에서 다 틀리고(프리프로덕션),
싸게 전량 뽑아 고르고(드래프트), 승인분만 비싸게 다시 뽑아(파이널), 소리는 편집에서
완성한다(포스트). 샷 하나의 품질 규칙은 `minimax-h3` 스킬이, 15초 초과 세그먼트는
`h3-longtake` 스킬이 담당한다 — 이 스킬은 그 위의 **제작 체계**만 다룬다.

## 0. 실측 단가표 (2026-08-13, RTX 5070 Ti 16GB / ComfyUI 0.32.0)

| 용도 | 설정 | 실측 | 출력 1초당 |
|---|---|---|---|
| 드래프트 | 832×480 · 터보 8스텝 | 5.17초에 ~85초 | **~16초** |
| 파이널 | 1152×640 · 터보 8스텝 | 15.08초에 1110초 | **~74초** |
| 히어로 샷 | 1152×640 · 20스텝 | 15.08초에 2190초 | ~145초 |

**10분(600초) 환산**: 드래프트 전량 2~3시간(하룻밤 배치) + 파이널 ~12시간(이틀 밤)
+ 리테이크 버퍼 25% ≈ **주말 하나 규모.**

⚠️ 터보는 반드시 `larryvrh/ComfyUI-MiniMax-H3-Turbo` 전용 노드 2종
(`MiniMaxH3TurboLoRA` + `MiniMaxH3TurboSampler`)과 원본
`minimax_h3_turbo_v4_step600_ema.safetensors`로 배선한다. generic 로더로 얹으면
time-conditioning이 깨져 반드시 붕괴한다 — `minimax-h3` 스킬 4-C절 참조.

## 0-B. 페이싱 원칙 — 트레일러를 만들지 마라 (2026-08-13 시운전 교훈)

52초 시험판에 장소 6곳을 넣었더니 예고편 리듬이 됐다. **장편의 시간·공간 흐름은
씬 단위로만 움직인다.**

- **10분 = 씬 6~8개, 씬당 60~100초.** 장소 이동은 씬 경계에서만
- **씬 하나 = 샷 4~8개 뭉치** — 설정 와이드 → 디테일 인서트 → 인물 → 리액션.
  한 공간에 머물러야 그 장소가 "있던 곳"이 된다
- **시간대는 씬 단위로만 전진** (오후→노을→저녁→밤). 샷 사이에서 시간이 튀면 안 된다
- 같은 씬 안의 샷들은 배경 명세·공간 레퍼런스를 재사용한다 — 일관성과 비용 둘 다 유리
- 씬당 와이드 설정샷 1개 이상, 음식 씬은 insert→reaction 템플릿

## 0-C. 레퍼런스 이원 체제 — 캐릭터는 로라, 공간은 GPT (2026-08-13 확립)

일관성은 텍스트 명세로 못 잡는다(시드마다 재추첨). 이미지 레퍼런스로 잠근다.

| 대상 | 생성 경로 | 규격 | 실측 근거 |
|---|---|---|---|
| **캐릭터 시트** | Illustrious + 캐릭터 LoRA (**강도 1.0** — 0.85보다 캐논 재현 우수) | 흰 배경, 정면 전신/좌프로필/얼굴 크롭 3장 | 흰 배경은 조명 바이어스를 넣지 않는다(노을 유지 확인). 4샷 연속 의상·정체성 일치 실증 |
| **공간 시트** | **2단 체인**: ① Illustrious로 화풍 앵커 1장 → ② GPT Image `reference_image` 편집으로 구도 집행 | 씬당 무인 와이드 1장, 지정 시간대 조명 | 씬 내 샷 간 배경·팔레트 앵커 |

**⭐ 공간 시트 2단 체인 (2026-08-13 확립).** 어느 한쪽 단독은 실패한다:
- GPT 단독 → 지글거리는 과밀 텍스처와 높은 채도. H3의 플랫 셀 룩과 계보가 어긋나고,
  레퍼런스의 스타일은 출력에 새기 때문에 그대로 오염된다
- Illustrious 단독 → 화풍은 맞지만 **지시 수행이 약해** 구도·소품 배치를 못 잡는다

절차: ① Illustrious(캐릭터 시트와 같은 체크포인트)로 화풍 앵커 1장 — 구도는 아무래도 좋다.
② **첫 로케이션을 GPT edit으로 완성** → 이후 나머지 전 로케이션은 **그 완성본 하나를 공용
앵커**로 물린다. 화풍뿐 아니라 **세계 연속성**(지붕색·건축 양식·등대 형태)까지 상속된다.
프롬프트 정형: "Repaint in EXACTLY the same art style as the reference — same flat clean
anime background painting, same muted palette, same level of detail. **Do not add extra
texture or busy detail.** Keep the style; change the composition to: {구도}".
밤·노을 등 조명이 크게 바뀌어도 화풍이 유지됨을 실측 확인(주간→노을→저녁→밤 7장).
⚠️ GPT 이미지 호출은 **직렬로만** — 병렬 시 산출물 수확 레이스로 같은 그림이 중복 저장된다.

**⭐⭐ 점묘 아티팩트 — 프롬프트로 못 잡는다. 3단 파이프라인이 답 (2026-08-13 실측).**

GPT 출력 표면에 깔리는 점묘/그레인(커뮤니티 명칭 *tiling texture / grime / digital
ripples*)은 **모델의 렌더링 특성**이며 프롬프트로 제거되지 않는다. 고주파 지표 실측:
일러 앵커 **1.65** → GPT 1회 편집만 거쳐도 **17~21** (연쇄 편집 누적은 부차적 —
편집 깊이를 1로 줄여도 21.2로 그대로였다).

**해법: 일러 → GPT → 일러 3단.**
```
① Illustrious 화풍 앵커  →  ② GPT edit으로 구도 집행  →  ③ Illustrious img2img 재도장
                                                            denoise 0.40~0.50
                                                            neg: film grain, grain, noise,
                                                            speckle, stippling, dithering,
                                                            dotted texture, halftone, crosshatch
```
③이 표면만 다시 칠해 점묘를 지우고 화풍을 우리 계보로 수렴시킨다. 구도는 보존된다.
- **0.40**: 점묘 소멸 + 구도 완전 보존. 안전한 기본값
- **0.50**: 표면이 더 매끄럽고 회화적. 소품이 약간 재해석될 수 있으니 구도가 중요한
  샷은 0.40, 분위기 컷은 0.50
- 한 장 1분 남짓. GPT 재생성보다 싸다
- ⚠️ **고주파 지표로 판정하지 마라** — 정당한 선화와 점묘를 구분하지 못한다(정제 후에도
  15.7). 눈으로 본다.

**(구) 자글거림(과밀 텍스처) 제거 — 금지 스택 (2026-08-13).**
"same level of detail" 같은 **소극적 동조 문구는 효과가 없다.** GPT는 기본적으로 미세
디테일을 덧붙이므로 **무엇을 그리지 말지를 항목으로 나열**해야 한다. 실측으로 확인된 스택:

```
STYLE RULES — these override everything else:
- Paint surfaces as large simple areas of colour. Keep shapes broad and readable.
- Do NOT draw individual stones, individual roof tiles, individual bricks, or individual
  leaves. Suggest these surfaces with flat colour plus one or two soft shadow shapes.
- No visible paint texture, no grain, no speckle, no stippling, no hatching, no noise,
  no weathering, no cracks, no rust, no moss.
- No dense micro-detail and no ornamental detail anywhere.
- Soft cel shading: one light tone and one shadow tone per surface, hard edges
  (a gentle gradient allowed only in sky and water).
- Muted, desaturated palette. No glare, no lens effects, no glow.
- Clouds as plain rounded shapes with no internal detail.
```
- **"detailed / intricate / high quality / masterpiece" 류 형용사는 쓰지 마라** — 덧붙임을 부른다
- `quality: medium`이 `high`보다 디테일 밀도가 낮아 이 목적엔 유리
- 강도 조절: 위 스택에서 "large **flat** areas"+"big simple shapes only"까지 밀면 벡터
  일러스트처럼 납작해진다. **"large simple areas with soft gradients"**가 애니 배경화의
  중간 지점 — 두 판을 뽑아 비교하고 고르는 것을 권장

- 바인딩: `<Picture 1~3>`=캐릭터, `<Picture 4>`=해당 씬 공간. ref2va `ref_images.ref_image_N`
  (점 표기 — flat 키는 TypeError)
- **동명 원칙(손목시계 교훈)**: 레퍼런스에 있는 것은 텍스트에서 같은 이름으로 부르고,
  레퍼런스에 없는 착용물·소품을 텍스트로 추가하지 않는다. 시트끼리도 서로 일치해야 한다
  (액세서리 개수·위치까지 — 감사자가 이미지를 직접 열어 대조하게 하라)
- 캐릭터 시트 채택 전 사용자(원작자) 검수 필수. 시트 갱신 시 캐릭터 블록도 함께 갱신

## 1. 프로젝트 스캐폴드

```
research/projects/<제목>/
  bible.md            # 주인공·무대·톤·시간대 아치·의상·소품 — 모든 샷의 헌법
  voice.md            # 캐노니컬 보이스: 목소리 묘사문 + 클론 소스 경로
  screenplay.md       # 씬 단위 각본 (씬 번호, 장소, 시간대, 목적)
  shots/S##_s##.json  # 샷 명세 (아래 스키마)
  renders/draft/      # 드래프트 산출물 (샷 id로 파일명)
  renders/final/      # 승인 샷 파이널
  review/decisions.md # 승인/리테이크 판정 로그 (사유 필수)
  post/               # BGM, 내레이션 wav, 편집 타임라인, 최종본
```

대용량 산출물은 페르소나 `research/`에 두고 `.sessionignore`에 등록한다(기존 관례).

## 2. 샷 스키마 — 연출 문법을 필드로 강제한다

```json
{
  "id": "S03_s02",
  "scene": 3,
  "duration_s": 8.7,
  "length": 209,
  "audio_tier": "ambient",        // talk | ambient | montage
  "shot_size": "medium",          // wide | medium | closeup | insert
  "camera": { "move": "Pan Right", "speed": "slow", "amplitude": "small" },
  "time_of_day": "sunset",
  "dialogue": [],                  // talk일 때만. {speaker, voice_ref, line, receiver}
  "music_policy": "post",          // 원칙: 논디제틱은 전부 post
  "prompt": "<16축 명세를 채운 완성 프롬프트>",
  "location": "pier",              // 공간 시트 파일 키 (refs/loc_<location>.png)
  "render": { "engine": "ref2va", "steps": 20 },   // ref2va | fl2va-turbo | fl2va-base
  "ref_images": ["refs/gj_front.png","refs/gj_profile.png","refs/gj_face.png","refs/loc_pier.png"],
  "voice_ref": "post/voice/canonical.wav",         // talk 샷 필수
  "status": "draft_pending"        // draft_pending → draft_ok|retake → final_ok
}
```

### ⭐ `ref_images`는 샷마다 명시 배열로 — 규약 암기에 맡기지 마라 (2026-08-13 감사 적발)

"Picture 1~3=캐릭터, 4=공간"을 **고정 규약으로만** 두면 무인 샷에서 터진다. `ref_image_0..N`은
구멍을 못 만들므로 무인 샷은 공간이 **Picture 1**이 되어 번호가 당겨진다. 러너가 규약대로
캐릭터를 먼저 주입하면 "No people are visible"인 설정 와이드에 캐릭터 시트가 물린다.

- 샷 JSON에 **실제 파일 배열**을 적고 러너는 그 순서 그대로 주입한다
- 러너는 `ref_images.length === 프롬프트 내 최대 <Picture N>`을 assert하고 불일치 시 중단
- 무인 샷: `["refs/loc_*.png"]` / fl2va 인서트: `[]`

### 무인 샷 엔진 규칙 (명문화)

- **무인 설정 와이드** = ref2va + `<Picture 1>`=공간 레퍼런스. 배경·팔레트 앵커가 필수이므로
  base 스텝 비용을 지불한다
- **무인 디테일 인서트** = fl2va-turbo 8스텝, 레퍼런스 없음. 대신 프롬프트에 재질·색을
  문자로 못 박는다 (`the planks are warm weathered brown, the rope is pale hemp...`)

### 시드 규칙

`9{씬번호 2자리}{샷번호 2자리}` 등 **씬·샷이 자리별로 분해되는 체계**로 정하고 bible에 못 박는다.
시험판과 대역이 겹치면 리테이크 대조가 불가능해진다.

### ⭐⭐ 매 샷 빠지는 5축 — 씬 헤더 정형구로 강제하라 (감사 실측: 7/7 누락)

샷을 손으로 쓰면 **아래 다섯 축이 계통적으로 빠진다.** 씬 단위 정형구를 만들어 전 샷에
기계적으로 삽입하라.

1. **색 팔레트(축 10)** — `Dominant palette: {지배색 2~3개}.` 없으면 씬 경계마다 색이 튄다
2. **타임스탬프(축 12)** — 8.7초 이상 샷마다 박자 앵커 2~3개.
   `At 00:02.0 she plants both feet; at 00:05.5 ...; from 00:08.0 ... until the end.`
3. **촬영 주체(축 13)** — `The camera is an unmanned observing camera; no camera, phone,
   tripod, gimbal or filming equipment is visible anywhere in the frame, and nobody is
   holding the camera.` 브이로그+렌즈 응시 조합에서 특히 필수
4. **조명은 월드 기준으로** — `sunlight from screen-left`는 카메라 상대 표현이라 **리버스
   샷에서 반드시 깨진다.** `The sun is low over the sea to the west; in this shot the sea
   is at screen-left, so the light comes from screen-left and shadows fall to screen-right.`
   그림자 방향도 매 샷 명시
5. **정형구 오염 린트** — 무브별로 문구 라이브러리를 분리하라. `camera.move`가
   `Push In`/`Pull Out`/`Zoom`인데 프롬프트에 `same distance`/`same size in frame`이
   있으면 **fail**. (트래킹용 거리 고정 문구가 푸시인 샷에 복사되는 사고가 실제로 났다)

### 로케이션 레퍼런스와 각본이 충돌하면 각본이 아니라 **먼저 그림을 고쳐라**

`Keep the setting identical to <Picture N>`을 걸어 놓고 레퍼런스에 없는 구조물(계단, 난간
등)을 화면 중심 소재로 요구하면 배경이 매 프레임 흔들린다. 샷 작성 전에 **각본이 요구하는
구조물이 그 로케이션 시트에 실제로 그려져 있는지 확인**하고, 없으면 시트를 다시 뽑거나
각본을 그림에 맞춰 내려라. 불가피하면 그 샷만 바인딩을 완화한다 —
`The look of this place is exactly the world shown in <Picture N>: the same materials,
architecture and palette.` (설정 동일 → **양식 동일**로 약화)

### 오디오 3종 배분 (씬 단위 예산)

| tier | 비중 | 규칙 |
|---|---|---|
| **talk** | ≤ 1/3 | 가슴 위 프레이밍 강제, 대사는 샷 중반 이후, 수신자 명시 |
| **ambient** | ~1/2 | 대사 없음. 지배음 선언 + 폴리 위계. 영상의 숨 쉬는 여백 |
| **montage** | 나머지 | 컷 빠르게, 화면은 소리 최소, 음악은 post에서 전면 배치 |

### ⭐⭐ 저역 펄스 잡음 — H3 앰비언스를 포기하는 근거 (2026-08-13 실측)

인물이 등장하는 샷의 오디오에 **초당 2회 안팎의 저역 펄스**가 깔린다. 사용자 청취
표현: "배경에 노이즈 같은 소리가 주기적으로 낀다."

| 조건 | 펄스 | 200~800Hz 비중 |
|---|---|---|
| 무인 샷 (s01·s03) | **0회** | — |
| 인물 걷는 샷 3개 | 18~29회 (2.1~2.4/s) | 74~94% |
| 샘플러 euler 교체 | 21~24회 | 89.6% |
| 샘플러 heun / euler 25스텝 | 26 / 22회 | 93 / 90% |
| **발소리 소거 지시** (`footsteps are completely inaudible`) | **26회 (변화 없음)** | 91.4% |
| **정규화 미적용** | 26회 (변화 없음), RMS −40.6dB | 92.1% |

**시도해서 실패한 것 전부**: 샘플러 교체(euler/heun), 스텝 증가(25), 프롬프트로 발소리
소거, `NormalizeAudioLoudness` 제거. **어느 것도 펄스를 없애지 못했다.**
정규화는 원인이 아니라 **증폭기**일 뿐이다(−40dB → −21dB).

**해석**: 인물 샷의 생성 오디오가 사실상 200~800Hz 대역에 90% 이상 몰린 저역 덩어리다.
프롬프트 층위에서 제어되는 축이 아니다.

**⭐⭐ 정정 (2026-08-16 사용자 판정): 전량 폐기는 과잉이었다 — EQ로 살린다.**
무대사 샷 오디오를 통째로 버리면 파도·바람·시장 소음이 함께 사라져 편집본이 빈다.
펄스가 200~800Hz에 몰려 있으므로 **그 대역만 깎으면 앰비언스는 살고 펄스는 죽는다.**

```bash
# 무대사 일반 샷 — 앰비언스 유지 + 저역 펄스 제거 (사용자 청취 승인)
-af "highpass=f=180,equalizer=f=400:t=q:w=1.2:g=-6,volume=0.8"
# 입이 열리는 무대사 샷(먹기·하품) — 발화가 음성대역이라 EQ로 못 잡는다 → 음소거
-af "volume=0"
# 대사 샷 — 원본 유지
```
결과: H3 앰비언스가 베이스로 쓰이고 post의 MMAudio는 **부족한 폴리만 보강**하면 된다.

**(구) 결론 — 오디오 아키텍처를 바꾼다. H3에는 대사만 맡긴다.**
- **talk 샷**: H3 오디오 사용(립싱크 때문에 대체 불가). 대사 외 앰비언스는 어차피 대사에
  묻힌다
- **그 외 전 샷**: H3 오디오를 **버리고** 영상만 쓴다. 앰비언스·폴리·BGM은 전부 post에서
  얹는다(`video-sound-design` 스킬의 MMAudio + 연속 베드)
- 이렇게 하면 세그먼트 간 앰비언스 튐, 저역 펄스, 무대사 샷 웅얼거림이 **한꺼번에** 사라진다
- 부수 이득: 무대사 샷의 Soundscape 문단을 짧게 유지해도 되고, 발성 억제 문구만 남기면 된다

**논디제틱 음악은 생성하지 않는다.** H3는 세그먼트마다 오디오를 독립 생성해 음악이
컷마다 튄다(실측). H3에는 디제틱(현장음·폴리·대사)만 맡기고 BGM은 post에서 연속
베드로 깐다 — 세그먼트 오디오 이음새 문제까지 함께 사라진다.

### 카메라 문법 린트 (검토 게이트가 기계적으로 검사)

- 같은 camera.move **연속 2회 금지** (전부 Tracking이면 컷이 바뀐 줄 모른다 — 실측)
- 씬마다 wide 설정샷 1개 이상, shot_size 3연속 동일 금지
- talk 샷의 shot_size는 medium 이상 (closeup 권장)
- 씬 유형 템플릿: 도착(wide→walk-in→reaction) / 음식(insert→reaction) / 이동(montage 3~4컷)
- time_of_day는 씬 블록 단위로만 전진(아침→정오→노을→밤) — 팔레트 연속성 공짜 확보

## 3. 목소리 일관성 — 하이브리드 3층

H3는 세그먼트마다 음색이 재추첨된다(실측). 역할별로 갈라 대응한다.

1. **내레이션/보이스오버 → TTS 완전 이관.** 립싱크가 없으므로 H3가 만들 이유가 없다.
   Qwen3TTS 보이스 클로닝으로 60샷 내내 동일 목소리. 공식 지원되는 "입 닫힌 화면 밖
   보이스오버" 프레이밍과 조합.
⭐ **실측 확정(2026-08-13): talk 샷에 터보 금지.** 터보 8스텝에서 `<d>[Korean]` 대사가
일본어풍 음소로 드리프트했고, 같은 시드 base 20스텝에서 한국어가 정상 복귀했다(사용자
청취 확인). 터보의 공식 약점(오디오)이 언어 정체성까지 무너뜨린다 — **대사 있는 샷은
드래프트든 파이널이든 base 스텝으로 뽑는다.** 대사 없는 샷의 웅얼거림 통제는 별개 축.

### ⭐ ref2va × 터보 호환 — 정지컷은 합격, 시간축은 불합격 (2026-08-13 실측)

같은 샷·같은 시드·같은 레퍼런스 4장으로 A/B (832×480 L294):

| | ref2va base 20스텝 | ref2va + 터보 8스텝 |
|---|---|---|
| 소요 | 629초 | **291초 (2.16×)** |
| 배경 띠 프레임차 mean/max | **1.99 / 5.87** | **11.45 / 21.63** |
| 8 초과 프레임 비율 | 0% | **71.7%** |
| 정지컷 | 정상 | 정상 (오히려 배경이 더 화사) |

**판정: 최종 산출물에 쓰지 마라.** 정지 프레임만 보면 멀쩡하고 2배 이상 빠르지만,
배경이 재생 시간의 **71.7%** 동안 출렁인다(FL2VA 터보의 정상치는 0%). 터보는 FL2VA
경로에서 증류되었으므로 ref2va의 레퍼런스 토큰 흐름과는 시간축이 맞지 않는다.
lightx2v 로드맵의 **Ref2V 전용 증류**가 나오기 전까지 인물 샷은 base 스텝이 유일한 선택.

용도 제한: 구도만 확인하는 **초저가 프리뷰**로는 쓸 수 있다(2.16× 저렴, 배치 앞단에서
동선·프레이밍만 판정). 그 목적이면 해상도를 낮추는 편이 부작용이 없다.

2. **온스크린 대사 → H3 유지 + `ref_audios` 앵커.** 립싱크 때문에 대체 불가.
   `MiniMaxH3ReferenceToVideo`의 `ref_audios`에 같은 음성 샘플을 물려 음색 고정.
   ⚠️ 드리프트 억제 효과는 미검증 — 본편 투입 전 3클립 A/B 필수. ref2va 경로는
   별도 가중치 + 터보 호환 미확인이라 talk 샷은 비싸게 갈 각오.
3. **잔여 편차 → post 평탄화.** loudnorm 2패스 + 가벼운 EQ 매칭.

**캐노니컬 보이스 절차**: 목소리 묘사문으로 대사 클립 3~5개 생성 → 사용자가 선정 →
가장 깨끗한 3~10초를 잘라 `voice.md`에 등록 → TTS 클론 소스와 H3 ref_audio가
**같은 파일을 공유**한다(목소리의 단일 진실 공급원).

## 4. 2-tier 렌더링 절차

1. **드래프트 패스**: 전 샷을 832×480 터보 8스텝으로 배치 렌더. 목적은 구도·동작·
   타이밍 판정이지 화질이 아니다.
2. **리뷰 게이트**: 사용자가 draft_ok / retake 판정. retake는 사유를 `decisions.md`에
   남기고 프롬프트를 수정해 재드래프트. **드래프트 승인 없이 파이널 금지.**
3. **파이널 패스**: 승인 샷만 1152×640 터보 8스텝. 감정 절정·포스터 컷 등 히어로 샷만
   20스텝. 4스텝은 몽타주 후보로 검토 가능하나 대모션 스미어 미검증 — 쓰기 전 A/B.
4. **배치 러너**: 큐는 샷 id 순, 완료분은 status 갱신으로 체크포인트. 중단돼도 pending만
   재개. 진행 판정은 로그가 아니라 `/prompt` 큐와 출력 mtime(디버깅 3원칙).

## 5. 포스트 체인

1. 세그먼트/샷 이어붙임 — 15초 초과 단일 테이크는 `h3-longtake`(ConText-Loop),
   컷 전환은 그냥 이어붙임
2. 내레이션 TTS 트랙 삽입 (씬별 타이밍은 screenplay.md 기준)
3. BGM 베드 — 씬 블록 단위 1곡, 컷과 무관하게 연속. talk 구간 3~5dB 더킹
4. J/L컷 — 씬 경계에서 다음 씬 앰비언스를 0.5초 선행/지연
5. 마스터링 — `ffmpeg loudnorm` 2패스 (I=-16, TP=-1.5, LRA=11)

## 6. 검토 게이트 (생성 전 필수)

각 샷 프롬프트는 `minimax-h3` 스킬 4-J절의 16축 검토를 통과해야 한다. 장편에서는
추가로: bible.md와 의상·소품·시간대 일치, 직전 샷과의 카메라 문법 린트, audio_tier
예산 준수. 검토는 서브에이전트에게 "무엇이 미지정인가"를 묻는 형식으로 — blocking 0이
될 때까지. **리테이크 단가가 낮아졌다고 검토를 건너뛰지 마라. 60샷이면 낭비도 60배다.**
