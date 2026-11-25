---
name: video-sound-design
description: AI 생성 영상에 사운드를 입히는 절차. MMAudio(video-to-audio)로 배경음과 효과음을 레이어로 나눠 만들고 게인으로 믹스한다. CLIP 77토큰 제한, negative가 uncond를 통째로 대체하는 구조, mask_away_clip의 실제 동작 등 프롬프트가 왜 안 먹는지를 실측으로 기록했다. "영상에 소리", "효과음", "배경음", "앰비언스", "폴리", "MMAudio", "사운드 입히기", "BGM", "립싱크" 키워드에 트리거된다.
---

# 영상 사운드 디자인 스킬

## 핵심 원칙 — 한 번에 다 만들지 말고 층을 나눠라

`MMAudioSampler`는 **프롬프트를 하나만 받는다.** 그게 전체 길이에 똑같이 적용된다. 따라서 단일 패스로는

- 시간대별로 다른 소리를 지시할 수 없고
- 특정 소리가 과하게 나와도 줄일 방법이 없다

층을 나누면 둘 다 해결된다. 구간마다 다른 프롬프트를 쓸 수 있고, **믹스 단계의 게인으로 크기를 조절**할 수 있다.

| 층 | 성격 | 생성 방식 |
|---|---|---|
| **배경(앰비언스)** | 길고 일정함 | `mask_away_clip=True`, 8초씩 만들어 크로스페이드 |
| **효과음(폴리)** | 타이밍이 생명 | `mask_away_clip=False`, 필요한 구간에만 5초 |
| 음악(BGM) | 구조가 있음 | ACE-Step (별도 모델, 영상과 무관) |
| 대사 | 입 모양이 맞아야 함 | **완전히 다른 공정** — §대사 참조 |

## MMAudio 프롬프트 — 왜 안 먹는지의 구조적 이유

### 1. 텍스트 인코더가 CLIP이다 — 77토큰 하드캡

학습셋이 VGGSound 클래스명 + AudioCaps 캡션이라 **짧은 캡션체가 분포 내**다. 실효 길이는 20토큰 이하로 보는 게 안전하다.

```
✅ cafe ambience, murmuring crowd
✅ ceramic cup set down on wooden table
❌ cozy indoor coffee shop, soft mellow jazz playing quietly from ceiling speakers,
   warm murmur of people chatting at nearby tables, occasional ceramic cup and saucer
   clink, espresso machine steam hiss in the distance, muffled and roomy
```

긴 프롬프트는 뒷부분이 희석되거나 잘린다. 실측에서 위 ❌ 프롬프트는 의도한 재즈도 컵 소리도 제대로 안 나왔다.

### 2. negative_prompt는 별도 항이 아니라 uncond 분기를 통째로 대체한다

`get_empty_conditions(negative_text_features)` — 비우면 학습된 `empty_string_feat`를 쓰고, 채우면 그 자리에 들어간다. **길고 구체적으로 쓰면 CFG 기준선이 왜곡돼 전체 음질이 흔들린다.**

**1~3단어로 짧게.** 공식 Gradio의 video 탭 기본값은 `music` 하나뿐이다.

### 3. ⚠ negative에 무엇을 넣는지가 장면을 통째로 바꾼다

실측 실패 사례. 카페 앰비언스를 만들면서 이렇게 넣었다.

```
negative: music, speech, voice, singing
```

결과는 **"바람 부는 야외"**였다. 카페의 본질인 재즈 BGM과 손님 웅성거림을 전부 제거했으니 남는 게 광대역 잡음뿐이었던 것이다.

**카페·식당·바 같은 실내 공간은 music과 speech가 본질이다. 빼면 안 된다.** 화이트 노이즈가 문제라면 그걸 직접 눌러야 한다.

```
✅ negative: wind, hiss        (짧게, 문제를 직접 지목)
❌ negative: music, speech, voice, singing, loud, noise, static
```

| | 전체 RMS | 구간 변동폭 | 체감 |
|---|---|---|---|
| 잘못된 negative | 0.200 | 1.2배 | 화이트 노이즈, 야외 |
| 수정 후 | 0.055 | 7.69배 | 조용한 실내 + 소리 이벤트 |

### 4. `soft` / `faint` / `distant`는 볼륨 페이더가 아니다

**음원 클래스 선택자**다. `distant thunder`는 그런 캡션이 학습에 있어 먹히지만, `soft footsteps`는 발소리의 존재 자체를 줄이지 못한다.

**과하게 나오는 소리를 줄이는 1순위는 positive에서 그 단어를 빼는 것.** 크기 조절이 목적이면 그 소리를 별도 레이어로 뽑아 게인으로 낮춰라.

### 5. cfg는 이벤트 강도를 키운다

`cfg*cond + (1-cfg)*empty` 구조라 올리면 프롬프트에 쓴 이벤트가 **더 크고 잦게** 나온다. 기본 4.5, 실용 3.0~6.0. **시드 영향이 매우 크므로 같은 설정으로 여러 개 뽑아 채택하는 게 정석이다.**

### 6. `mask_away_clip=True` — 앰비언스 전용 스위치

CLIP 시각 특징만 죽이고 Synchformer 동기화 특징과 텍스트는 유지한다. 화면이 유도하는 엉뚱한 음원(사람이 보임 → 말소리)을 끊고 **텍스트로만 음색을 지정**할 때 켠다. 배경 레이어에 적합하다.

## 함정

### 함정 1 — 길이는 duration이 아니라 프레임 수가 결정한다

`duration=5.1`을 줘도 실제 출력은 **입력 프레임 수 ÷ 25fps**로 클램프된다. 41프레임을 넣었더니 1.65초가 나왔다(41/25 = 1.64).

**MMAudio의 sync 인코더는 25fps 기준이다. 8fps로 다운샘플해서 넣으면 안 된다.**

```python
# 16fps 소스를 25fps로 리샘플
SRC_FPS, TGT_FPS = 16.0, 25.0
n = int(round(len(frames) / SRC_FPS * TGT_FPS))
for i in range(n):
    idx = min(len(frames) - 1, int(round((i / TGT_FPS) * SRC_FPS)))
    frames[idx].save("f%04d.png" % i)
```
5.06초 영상(81f@16fps) → **127장**. 30.06초 → **752장**.

### 함정 2 — VHS_LoadVideo는 animated webp를 못 읽는다

OpenCV가 지원하지 않는다. `could not be loaded with cv` 에러가 난다. PNG 시퀀스로 풀어 `LoadImagesFromFolderKJ`(kjnodes)로 넣어라. `image_load_cap`과 `start_index`를 명시적으로 넘겨야 한다.

### 함정 3 — 학습 길이는 8초다

공식 README: "기본이자 학습 길이는 8초. 더 길거나 짧아도 동작하지만 크게 벗어나면 품질이 떨어진다."

30초 단발 생성도 **된다**(실측 확인, 752프레임 → 30.09초). 다만 구간 변동폭이 2.44배로 밋밋했다. 8초 스위트스팟에서 만들어 크로스페이드로 늘리는 쪽이 안전하다.

속도 차이도 크다.

| | 소요 |
|---|---|
| 30초 단발 | 267초 |
| 8초 × 4 + 5초 × 2 (레이어) | **약 67초** |

첫 호출은 모델 로딩으로 191초가 걸리지만, 상주한 뒤로는 8초 클립이 **6초** 만에 나온다.

### 함정 4 — ffmpeg mux의 `-shortest`

오디오가 영상보다 짧으면 **영상이 잘린다.** 위 함정 1로 오디오가 1.65초로 나왔을 때 30초 영상이 1.65초짜리 mp4가 됐다. 길이를 먼저 검증하고 mux하라.

## 믹스 — 게인 기준 실측

배경과 효과음의 원본 음량 차이가 크다. 게인을 그대로 두면 효과음이 안 들린다.

| 레이어 | 원본 RMS |
|---|---|
| 배경(웅성거림) | 0.10 ~ 0.14 |
| 효과음(컵 소리) | 0.009 ~ 0.017 |

효과음에 게인 0.3을 곱하면 0.003 — **배경보다 30배 작아 완전히 묻힌다.** 실측에서 사용자가 "컵 소리가 아예 없어진 것 같다"고 했다.

**출발점: 효과음 게인 1.0~2.0.** 거기서 귀로 조절하라. 게인 조절은 재생성이 필요 없어 5초면 끝난다 — 이것이 레이어를 나누는 가장 실용적인 이득이다.

정규화는 피크 기준 0.89 정도로. 클리핑을 피하면서 여유를 남긴다.

## 대사(립싱크) — 별개 공정

배경음·효과음은 완성된 영상 위에 얹으면 끝이지만, 대사는 **입 모양이 맞아야** 하므로 영상을 다시 만들거나 입 영역만 교체해야 한다.

두 갈래가 있다.

- **후처리 립싱크** (LatentSync, Wav2Lip 계열) — 얼굴을 찾아 입 주변만 잘라내 오디오에 맞춰 재생성 후 합성. 원본 포즈·배경·카메라가 100% 보존되고 가볍다. 다만 크롭 해상도 한계가 있다
- **오디오 구동 생성** (InfiniteTalk, Wan2.2-S2V) — 고개·표정까지 음성에 반응해 자연스럽지만 무겁고 30초 이상에서 정체성이 무너진다

**실무 제약**: 인물이 상반신 이하로 잡힌 영상(832×480에서 얼굴이 화면의 10% 미만)은 입 영역이 너무 작아 립싱크 결과가 뭉개진다. **대사를 넣으려면 처음부터 클로즈업으로 영상을 만들어야 한다.**

**한국어 주의**: 립싱크 모델의 오디오 인코더가 언어 편향적이다. InfiniteTalk는 `chinese-wav2vec2-base`, Wan2.2-S2V는 `wav2vec2_large_english`를 쓴다. 한국어 받침·평격경음 구분이 시각적으로 뭉개진다(추정, 미실측). 완화책은 발화 속도 하향, 문장 단위 분할, 배경음 제거.

## 미검증

- **ACE-Step BGM** — 체크포인트(`ace_step_v1_3.5b.safetensors`, 7.7GB)는 받아뒀고 ComfyUI 코어에 노드가 내장돼 있다(`TextEncodeAceStepAudio`, `EmptyAceStepLatentAudio`, 1.5 버전 노드도 있음). 아직 생성해보지 않았다
- **NAG** (arXiv 2506.20995) — MMAudio에 ControlNet을 붙여 이미 생성된 트랙을 negative audio로 밀어내며 순차 레이어링. 실제 폴리 워크플로를 모사한다. 표준 ComfyUI 노드는 아직 없음
- 라우드니스 정규화(loudnorm), 구간별 EQ, 리버브 후처리

## 스크립트

`scripts/audio_layers.py` — 배경 4개 + 폴리 N개 생성 후 크로스페이드·게인 믹스까지 한 번에. 상단 상수(`TOTAL`, `AMB_LEN`, `AMB_N`)와 `FOLEY` 리스트를 장면에 맞게 고쳐 쓴다.

```python
FOLEY = [
    {"seg": 2, "at": 5.06,  "prompt": "ceramic cup set down on wooden table", "gain": 1.2},
    {"seg": 5, "at": 20.24, "prompt": "ceramic cup picked up from table",     "gain": 1.0},
]
```

`at`은 전체 타임라인에서의 시각(초). 여기가 **시간대별 지시가 가능해지는 지점**이다.
