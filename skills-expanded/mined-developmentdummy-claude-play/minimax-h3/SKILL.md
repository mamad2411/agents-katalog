---
name: minimax-h3
description: MiniMax H3(Hailuo 3.0) 영상 모델을 ComfyUI에서 로컬 구동할 때 사용한다. 오디오가 네이티브로 동시 생성되는 33B omni-modal 모델이며, 16GB VRAM에서는 NVFP4 양자화가 정답 경로다. length 그리드(17k+5)와 훈련 범위(124~362 = 5~15초), 해상도별 실측 벤치마크, 프롬프트에 소리를 섞어 넣는 방식, 15초 초과 시의 체이닝 판단을 다룬다. "MiniMax", "H3", "Hailuo", "영상에 소리 같이", "omni-modal", "NVFP4", "15초 영상" 키워드에 트리거된다.
---

# MiniMax H3 로컬 구동

## 한 줄 요약

**15초까지는 체이닝 없이 한 방에 뽑는 것이 정답이다.** (15초 초과는 `h3-longtake` 스킬) 오디오는 별도 파이프라인이 아니라
프롬프트 안에 있고, **대사는 `<d>[Korean] ...</d>` 태그로 넣는다(한국어 동작 확인).**
실용 기본값은 **576×1024 세로 / L209 x 4세그먼트 = 약 55분에 35초**다(숏폼).
**연출 원칙은 0절을 먼저 읽어라** — 개별 규칙은 전부 거기서 파생된다.

## 0-Z. ⭐⭐ 장르가 밀도를 정한다 — 감성 컷은 0-A의 반대로 간다 (2026-08-18 실측)

> **0-A(5초 하드컷 / 동작 밀도 최대화)는 액션·댄스·리듬 컷의 공식이다. 감성·정적 컷에 그대로 쓰면 산만해진다.**

같은 날 같은 세션에서 두 방향을 다 뽑아 비교했다. 디스코 댄스 5초는 동작 5비트를 몰아넣어야 살았고, 새벽 방 15초는 **비트를 7개로 줄이고 사이를 벌려야** 살았다. 사용자 판정: *"아무것도 안 하는데 더 많은 말을 하는 것 같아."*

| 축 | 액션 컷 (0-A) | 감성 컷 (이 절) |
|---|---|---|
| 비트 수 | 5초에 5~6개 | **15초에 7개** (간격 2~2.5초) |
| 비트 사이 | 쉼 없이 이어붙임 | **완전 정지.** 호흡·눈 깜빡임만 |
| 카메라 | Handheld + 빠른 bob, moderate amplitude | **Static, locked framing, no push in / no pan / no zoom** |
| 사운드 | 꽉 채움(군중·음악·폴리) | **near silence.** 발소리까지 제거, 룸톤 + 냉장고 웅웅 + 커튼 + 호흡만 |
| 음악 | BPM 명시(125 등) | 지속음 1개 → 6s 피아노 → 12s 첼로. 멜로디 금지 |
| 대사 | 상황 설명 OK | **15초에 한 줄.** 문장을 끝까지 맺지 않는다 |

### 감성 컷의 핵심 비트 3종 (실측으로 효과 확인)

1. **말하려다 멈추는 비트** — `she opens her mouth as if to say something, then closes it`. 0.8초짜리인데 대사보다 감정을 더 싣는다.
2. **웃음의 종류를 지정** — `a small, tired smile that does not reach her eyes`. 이렇게 쓰면 H3가 눈과 입을 따로 연기한다. 그냥 `smile`은 밝게만 나온다.
3. **행동으로 사실을 설명** — 식은 커피를 들었다가 마시지 않고 내려놓는 동작 하나가 "밤을 새웠다"를 전부 말한다. 단, 소품 상호작용은 아래 0-Y의 위험을 감수해야 한다.

## 0-Y. ⭐⭐ 소품은 "집지 마라" — 개체 수 유지 실패가 장척 최대 사고 (2026-08-18 실측)

15초 컷에서 **머그가 복제됐다.** 바닥에 하나 있는 채로 손에 또 하나가 생겼다. `params.json`에도 "정확한 개수 지정은 실패한다"고 적혀 있는데, "머그를 들었다가 내려놓는다"는 비트가 정면으로 그 약점을 밟은 것이다. 같은 컷에서 유리에 손가락으로 선을 긋는 동작도 허공 스미어로 뭉갰다.

**규칙:**
- 감성 컷의 연기는 **호흡 · 눈 · 고개 각도 · 어깨**로만 짠다. H3가 가장 안정적으로 처리하는 영역이다.
- 소품이 화면에 있어야 한다면 **고정 명령을 프롬프트에 박아라**:
  ```
  The single mug stays on the floor untouched for the entire shot and is never picked up.
  The room stays exactly as it is, nothing new appears, no object is picked up,
  her hands stay on her knees the whole time.
  ```
- 장척(L362)은 **steps 8 → 10~12**로 올린다. 8스텝은 5초에서는 충분하지만 15초에서 미세 동작이 뭉개진다.
- **FLF2V로 끝 프레임 = 첫 프레임 고정**. 원래 자세로 돌아오는 연출은 감성 컷에 서사적으로도 맞고, 후반 3초 드리프트를 구조적으로 막는다.

## 0-X. ⭐⭐ 첫 프레임의 공간감이 곧 영상의 공간감 (2026-08-18 실측)

통유리창을 배경 전체로 채운 스틸로 i2v를 돌렸더니 **인물이 공중에 앉아 있는 것처럼** 보였다. 사용자 지적 원문: *"뒤가 허공 아니야?"*

원인은 영상이 아니라 **베이스 이미지**다. 창이 프레임을 다 먹으면 바닥·벽·천장이 사라져 깊이 단서가 0이 된다. H3는 첫 프레임의 공간을 그대로 계승하므로, 여기서 틀리면 15분짜리 렌더가 통째로 날아간다.

**베이스 이미지 체크리스트:**
- 창·하늘은 **구석으로** 밀고, 인물 **뒤에 물체**를 둔다(침대·벽·선반).
- 실내 단서를 명시적으로 나열: `wooden floor extending toward camera, rumpled bed, framed picture, floor lamp, laundry basket`.
- 카메라를 **방 안쪽에서** 3/4 각도로 (`three quarter view`) → 바닥이 카메라 쪽으로 뻗어 원근이 생긴다.
- 네거티브: `floating in air, empty background, void background, no floor`.
- **전신샷은 얼굴이 90~110px밖에 안 된다.** FaceDetailer 기본 `denoise 0.3 / guide_size 512`로는 못 살린다 → 전신 컷은 `detailer_face_denoise` 0.45~0.55 + `detailer_face_guide_size` 768로 올려라(상반신 컷은 0.3 그대로).

## 0-W. ⭐⭐ 색은 생성이 아니라 후처리로 잡아라 (2026-08-18 실측)

"빈티지 시네마틱"을 프롬프트로 주문했더니 (`1970s film still`, `kodak portra`, `soft focus edges`, `heavy film grain`) **캐릭터가 망가졌다.** 모델이 색만 바꾸는 게 아니라 그림 자체를 그 시대 사진처럼 다시 그려버리기 때문이다. 실사 프리셋 단어가 얼굴을 실사 쪽으로 끌어당기고, 스타일 LoRA 총합이 캐릭터 LoRA를 넘기면서 정체성이 밀렸다.

**정답은 촬영과 색보정의 분리** — 실제 영화도 플랫하게 찍고 후반에서 잡는다.

```bash
# 5초 클립 기준 2초면 끝난다. 재생성 없이 파라미터만 바꿔 반복 가능.
ffmpeg -i in.mp4 -vf "
eq=saturation=0.58:contrast=0.91:brightness=-0.012,
colorbalance=rs=-0.05:bs=0.08:rm=0.06:bm=-0.04:rh=0.12:bh=-0.07,
curves=all='0/0.055 0.5/0.5 1/0.95',
noise=alls=8:allf=t+u,
vignette=PI/4.8,
gblur=sigma=0.32
" -c:a copy -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p out.mp4
```

- `saturation` 0.5=더 바램 / 0.75=은은 — 톤 조절은 이것과 `noise=alls`(4=미세 / 12=거친 16mm) 두 개만 만지면 된다.
- `curves`의 `0/0.055`가 검정을 띄워 필름 라티튜드를 만든다. 이게 빈티지의 핵심이고 채도보다 기여가 크다.
- `gblur=sigma=0.3` 정도로 디지털 샤프함만 덜어낸다.
- **오디오는 `-c:a copy`로 무손실 유지.** 같은 파라미터를 쓰면 여러 클립의 톤이 자동으로 맞아 이어붙이기 좋다.
- 프롬프트에 남겨도 되는 것: 구도(`off-center framing`, `negative space on one side`, `dutch angle`, `looking away from viewer`). **시네마틱해 보이는 건 색보다 구도 기여가 크다.**

## 0-V. 오디오 기본 레벨은 -20 LUFS (2026-08-18 사용자 청취 판정)

`NormalizeAudioLoudness` 기본 -16 LUFS는 체감상 과하게 크다. 실측하니 integrated -16, **LRA 1.1~1.2 LU** — 다이내믹이 거의 없어 5초 내내 최대치로 밀린 소리가 난다. `minimax-h3-video` / `-turbo` 두 패키지의 workflow.json + params.json 기본값을 **-20**으로 하향했다. 더 조용하게 원하면 -23(팟캐스트 기준). 기존 파일은 `loudnorm=I=-20:TP=-1.5:LRA=7`로 재정규화하면 된다.

## 0-A. ⭐⭐ 15초는 한 방에 뽑지 말고 **5초 × 하드컷 3개**로 만들어라 (2026-08-18 실측)

> **⚠️ 위 "한 줄 요약"의 '15초까지는 한 방에'는 *길이가 가능한가*의 문제였다. *보기 좋은가*는 다른 축이고, 거기서는 이 절이 이긴다.**

**사용자 판정 원문**: *"매번 느낀 게 뭔가 너무 느릿느릿 움직인다는 거였는데, 5초로 하니까 오히려 그 느린 느낌이 사라져서 좋다."*

### 왜 15초 단발이 느려 보이는가

프롬프트에 넣는 동작 개수는 길이와 무관하게 비슷해진다(사람이 쓸 수 있는 동사 수에 한계가 있다). 실측한 15초물은 컷당 동사 5~7개 × 3컷 = 15~20개를 **15초에** 펼쳤고, 5초물은 6~7개를 **5초에** 몰아넣었다 — **초당 사건 밀도 3배 차이**다. H3는 지시된 동작을 주어진 길이에 **늘려서 배분**하므로, 동작이 모자라면 빈 시간을 "천천히 움직이기"로 메운다. 그게 슬로모션의 정체다.

### 파이프라인

```
1. 정지 이미지로 키프레임 N+1장 생성 (t2i, 같은 방·같은 조명·같은 시드 계열)
2. 각 구간을 FLF2V 5초로 렌더 — first_frame=키프레임n, last_frame=키프레임n+1
   · length 124 / turbo 8스텝 → 세그먼트당 약 60초
   · 동작 문장에 동사 6~8개를 몰아넣는다 (4-O절 밀도 규칙)
3. 컷마다 프레이밍·앵글을 **명시적으로 바꾼다** (WIDE → MEDIUM, a new camera angle → CLOSER SHOT)
4. ffmpeg concat으로 이어붙인다
```

**15초 단발 대비 실측**: 렌더 12분 → **3분**, 동작 밀도 3배, **컷 단위 부분 재작업 가능**(마음에 안 드는 5초만 다시 뽑으면 된다 — 이게 실무에서 제일 크다).

### 연속성을 포기하는 것이 오히려 정답이다

세그먼트를 매끄럽게 잇겠다고 배경을 고정하려 애쓰지 마라. 키프레임을 독립 생성하면 인물 위치가 바뀌는 순간 배경도 달라지고, 그걸 억지로 붙이면 어색해진다. **컷으로 끊으면 배경이 달라지는 것이 자연스러워진다** — 영화에서 컷이 바뀌면 앵글이 바뀌는 게 당연한 것과 같다. 사용자 지적: *"꼭 연속해서 찍을 필요는 없어. 하드컷 씬을 넣어봐."*

컷 전환 명시 방법: 각 세그먼트 프롬프트 앞머리에 `WIDE SHOT` / `MEDIUM SHOT from a new, lower camera angle` / `CLOSER SHOT from a new camera angle at the bed` 처럼 **샷 사이즈 + "새 앵글"**을 적는다.

### 🚨 탈의·의상 변화 연출의 3대 함정 (전부 실제로 밟았다)

1. **겉옷과 속옷을 같은 색으로 하지 마라.** 검은 새틴 드레스 + 검은 레이스 속옷으로 찍었더니 사용자 반응이 *"이거 옷을 벗는데 안에 또 드레스가 나옴"*이었다. 벗어도 화면상 색면이 그대로라 **"벗었다"는 정보가 픽셀에 실리지 않는다.** 속옷을 빨강/흰색으로 바꾸면 즉시 해결된다. 매체 선언에 `The lingerie underneath is always RED, never black.`처럼 색을 못 박아 컷마다 재해석되는 것도 막아라.
2. **통짜 옷의 물리를 명시하라.** "dress sag **open**"이라고 썼더니 앞이 열리는 옷으로 재해석됐다. 슬립·원피스는 `a single seamless tube of fabric with no buttons, no zipper and no front opening — it can only slide down her body as one piece and must never open or part at the front.`
3. **비유·형태 명사를 쓰지 마라.** `pooled in a ring around her ankles`라고 썼더니 **금속 링이 달린 훌라후프**가 바닥에 생성됐다. `a crumpled heap of shiny black cloth lying flat on the floor`로 바꾸고 네거티브에 `hula hoop, metal ring, circular object`를 넣어라. (Anima 치트시트의 "비유 금지" 규칙과 같은 함정 — t2i·i2v 양쪽에 공통이다.)

### 검증 방법

- **키프레임은 반드시 눈으로 봐라.** SSIM 같은 수치만 보고 넘어가면 "드레스가 실제로 안 내려갔다"를 놓친다(실제로 놓쳤다).
- FLF2V 수렴 확인: 영상 끝 프레임 vs 목표 키프레임 SSIM, 그리고 **교차 대조**(끝 프레임 vs *시작* 키프레임)를 같이 재라. 실측 0.835 / 0.252 — 교차 대조가 낮아야 실제로 이동한 것이다.
- ⚠️ SSIM 비교 시 레퍼런스를 단순 `scale`로 줄이지 마라. 워크플로의 `ImageScale`은 `crop: center`이므로 비교도 `scale=W:H:force_original_aspect_ratio=increase,crop=W:H`로 맞춰야 한다. 안 맞추면 0.82가 0.64로 나와 오판한다.

### first_frame / last_frame 비율 규칙

`ImageScale`이 `crop: center`라 **키프레임 비율이 출력 비율과 다르면 잘린다.** 세로 832×1216(1.462) 이미지를 832×480(1.733) 영상에 넣었더니 위아래가 통째로 날아갔다. 출력 768×512(1.500)로 맞추면 오차 2.6%로 크롭이 사실상 없다. **키프레임은 출력 해상도와 같은 비율로 생성하라.**

## 0. ⭐⭐ 연출 제1원칙 — 개별 규칙보다 이걸 먼저 읽어라

아래 4절부터의 세부 규칙은 전부 **네 개의 원칙**에서 파생된다. 새로운 실패를 만나면
개별 규칙을 찾기 전에 이 넷 중 무엇을 어겼는지 물어라.

### 원칙 1 — 모델에는 기본값이 있고, 명시하지 않으면 거기로 돌아간다

기본값은 대체로 **가장 무난하고 정적인 것**이다. 실측으로 확인된 기본값들:

| 축 | 기본값 | 벗어나려면 |
|---|---|---|
| 시선 | **렌즈를 본다** | 어디를 보는지 + `not to the camera` |
| 표정 | **웃는다** | 눈꺼풀·눈썹·입을 각각 지정 |
| 자세 | **서 있다·걷는다** | 동사를 촘촘히 나열 |
| 소품이 든 손 | **아무 손** | 손 + 화면 좌우 |
| 의상 | **컷마다 재해석** | 샷마다 재명시 |
| 오버레이 | **컷에서 사라진다** | 샷마다 지속 문구 |
| 카메라와의 거리 | **인물이 멀어진다** | 거리 고정 문구 |
| 화면 속 화면 | **얼룩** | 안 보이게 돌리거나 단순 내용 지정 |

**"안 적었는데 알아서 해주겠지"는 항상 틀린다.**

### 원칙 2 — 추상은 안 그려진다. 관찰 가능한 것으로 번역하라

이 모델은 **눈에 보이는 것**을 그리지 카메라 밖의 의미를 그리지 않는다.

| 쓰지 마라 (추상) | 이렇게 써라 (관찰 가능) |
|---|---|
| 실망한다 | 눈썹 끝이 올라가고 어깨가 툭 떨어지고 입이 일자로 다물린다 |
| 도발적이다 | 반쯤 감은 눈, 턱을 치켜들고, 허리에 주먹 |
| 급하게 | 홱 돌아 → 달리기 시작 → 상자를 피하고 → 로프를 뛰어넘고 |
| 예쁘게 | (그리지 못한다. 조명 방향·색 팔레트·프레이밍으로 바꿔 써라) |

감정·성격·분위기는 **전부 근육의 움직임과 기하로 번역**해야 한다.

### 원칙 3 — 축은 서로 독립이다. 하나를 지정해도 옆 축은 따라오지 않는다

오늘 반복해서 밟은 함정이다.

- 손을 지정했다 ≠ **화면 좌우**가 지정됐다 (마주 본 인물의 오른손은 화면 왼쪽)
- 대사 내용을 썼다 ≠ **발화 대상**이 지정됐다
- 감정을 지정했다 ≠ 그걸 담을 **프레이밍**이 확보됐다
- `prompt_prefix`에 썼다 ≠ **각 샷**에 적용된다
- 레퍼런스에 있다 ≠ **텍스트에서 같은 이름**으로 불렀다

**하나를 고칠 때마다 "그 옆 축은 지정됐나"를 물어라.**

### 원칙 4 — 프레이밍이 모든 미세 표현의 상한이다

얼굴이 90px이면 입은 15px이고, 그 안에 음소도 감정도 들어가지 않는다.
**표정·립싱크·감정선이 필요한 컷은 가슴 위 이상**으로 잡아야 한다. 프레이밍을
확보하지 않고 표정을 지시하는 것은 지시가 아니라 희망이다.

같은 이유로 **작은 화면·작은 글자·작은 손가락은 기본적으로 포기하고 설계**하라.
크게 잡을 수 있을 때만 시도한다.

---

## 1. length가 이 모델의 전부다

`MiniMaxH3ImageToVideo`의 `length` 툴팁 원문:

> Frame count at 24 fps, snapped up to the model's **17k+5 grid**
> (124 = ~5s; **trained range is ~124-362**, longer is untested)

| 값 | 초 | 비고 |
|---|---|---|
| 5, 22, 39, 56, 73, 90, 107 | ~0.2 ~ 4.5초 | **훈련 범위 아래** — 돌아가지만 기준선으로 쓰지 마라 |
| **124** | 5.17초 | 기본값, 훈련 범위 하한 |
| 209 / 294 | 8.7 / 12.25초 | |
| **362** | **15.08초** | 훈련 범위 상한 |
| 363~3600 | — | 입력은 되지만 미검증 |

**핵심**: WAN 계열에서 하던 last-frame 체이닝은 H3에서 **15초 미만이면 불필요하다.**
체이닝은 손실(이음새·색 드리프트·정체성 드리프트)을 반드시 동반하므로, 한 방에
되는 구간에서 굳이 쪼개지 마라.

## 2. 16GB Blackwell 자산 조합

RTX 50 시리즈(sm_120)는 FP4 텐서코어가 네이티브다. **NVFP4가 작아서 빠른 게 아니라
연산 자체가 빠르다.** int8은 크기 페널티와 연산 페널티를 둘 다 먹는다.

| 역할 | 파일 | 크기 | 폴더 |
|---|---|---|---|
| DiT | `MiniMax_H3_FL2VA_pruned_nvfp4.safetensors` | 11.67GB | `diffusion_models` |
| 텍스트 인코더 | `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | 14.61GB | `text_encoders` |
| 비디오 VAE | `minimax_h3_video_vae_fp16.safetensors` | 4.85GB | `vae` |
| 오디오 VAE | `minimax_h3_audio_vae_fp32.safetensors` | 0.56GB | `vae` |

- DiT는 `Abiray/Minimax-H3-nvfp4-INT4-INT8-Convrot`, 나머지는 `Comfy-Org/MiniMax-H3`
- **인코더가 DiT보다 크다**(14.61 > 11.67). 인코딩 단계 VRAM 피크가 14.4GB까지 올라간다
- 16GB에서 OOM 없이 통과한다. ComfyUI 0.30의 dynamic VRAM이 인코딩 후 정상 언로드한다
- 24~32GB면 `minimax_h3_fl2va_pruned_int8_convrot.safetensors`(19.53GB)가 품질 상위
- 공식 ComfyUI 템플릿의 기본값은 int8이므로 **16GB에서는 DiT 파일명을 nvfp4로 교체**해야 한다 (템플릿 안에 7군데 박혀 있다)

**요구 버전**: ComfyUI **0.31.0 이상**을 권장한다. 0.30.0에서 H3 네이티브 노드와
`comfy/ops.py`의 NVFP4 경로가 들어왔고, **0.31.0에서 int8_convrot VAE 지원(`bbda8364`),
minimax audio vae full offload 수정(`2340099d`), H3 VAE 최적화(`2a68ce33`)** 가 들어왔다.
0.30.x에서 int8_convrot VAE를 물리면 **검은 화면**으로 디코드된다.

**VAE 선택**: `minimax_h3_video_vae_int8_convrot.safetensors`(3.17GB,
`Kijai/MiniMax-H3-experimental`)가 fp16(4.85GB)보다 1.7GB 가볍고 decode가 빠르다.
단 **전체 소요에서 체감되는 차이는 크지 않았다**(1024×576 L124 기준 오차 범위).
샘플링이 시간의 대부분을 먹기 때문이다.

## 3. 실측 벤치마크

RTX 5070 Ti 16GB / RAM 67.5GB / torch 2.12.0+cu130 / ComfyUI 0.31.0 / 20step /
res_multistep + simple

| 해상도 | length | 출력 길이 | 소요 | 비고 |
|---|---|---|---|---|
| 832×480 | 73 | 3.04초 | 68초 | |
| 832×480 | 124 | 5.17초 | 158초 | |
| 832×480 | 362 | 15.08초 | 738초 | |
| 1024×576 | 124 | 5.17초 | 255초 | |
| 1152×640 | 124 | 5.17초 | 330초 | |
| **1152×640** | **362** | **15.08초** | **약 2190초 (36분)** | ⭐ **15초물 기본값.** 2186/2199초 두 번 재현 |
| 1344×768 | 124 | 5.17초 | 615초 | 최고 화질. VRAM 최저 여유 2.2GB — 경계 |
| **1344×768** | **362** | — | **약 3시간** | ❌ **사용 금지** |

**스케일링 법칙**: 해상도는 픽셀수^1.38, 길이는 프레임수^1.42로 시간이 증가한다.
각 축은 이 식으로 잘 예측된다.

> ⚠️ **그러나 두 축을 곱셈으로 외삽하지 마라.** 1344×768 × L362를 47분으로 예측했다가
> 실제로 약 3시간이 나왔다(3.8배 초과). VRAM이 모자라지면 블록 단위 오프로딩이 개입해
> **PCIe 전송이 시간을 지배**하고, 그 순간 연산 기반 예측식이 통째로 무효가 된다.
> **해상도 상한과 길이 상한은 따로 재고, 동시 최대는 반드시 실측하라.**

**16GB 실용 지도**
- **15초물** → **1152×640** (36분). 이것이 상한이다
- **5초 최고 화질** → **1344×768** (10분)
- **빠른 반복·측정용** → 832×480 (5초 158초)

**RAM은 병목이 아니었다.** 31GB → 64GB 증설 후 1024×576 L124를 재측정했으나
254.8초 → 256.2초로 **변화 없음**. 증설의 값은 속도가 아니라 헤드룸(고해상도 시도 가능)이다.

## 4. ⭐ 프롬프트 설계 — 4단 필드 구조가 정답이다

**H3는 한 덩어리 문장이 아니라 네 개의 필드로 나눠 쓰도록 설계됐다.** 노드 입력은
`prompt` 문자열 하나뿐이므로, 그 안에 **라벨 붙인 문단**으로 네 부분을 구분해 적는다.

```
2D-animated, hand-inked line art, flat cel-shading, warm sunset palette —
preserve the exact line weight, character design, flat cel shading, and
painterly background texture in every shot, with no 3D rendering and no
photorealism.

[Shot 1] A high school girl with long dark hair in a navy sailor uniform
stands at a rooftop railing at sunset, both hands resting on the rail, wind
lifting her hair and pleated skirt. She turns her head toward the camera, her
eyes widening, then breaks into a bright smile. Camera: Push In at slow speed
with small amplitude, moving toward her face.

Soundscape: Steady wind gusting across an open rooftop, the low continuous hum
of distant city traffic far below, her school shoes scuffing once on concrete
as she shifts her weight, the fabric of her uniform fluttering.

Music: N/A
```

### 각 부분의 규칙

**① 매체 선언 (첫 문단)**
- `2D-animated` / `live-action` / `3D CG` / `watercolor` / `claymation` 처럼 **평범한 말로**
- 이어서 **유지되어야 할 것을 이름으로 지목**: `preserve the exact line weight,
  character design, flat cel shading, and painterly background texture in every shot`
- 부정 지시도 여기: `with no 3D rendering and no photorealism`

**② `[Shot N]` — 시각 서술 + 카메라**
- 첫 샷은 `[Shot 1]`, 타임스탬프 없음. 이후는 `[Shot 2] At 00:01.300, hard cut to ...`
- 타임스탬프는 반드시 증가해야 하고 갭·중첩이 있으면 거부된다. 첫 샷은 0.000에서 시작
- 전환은 `hard cut`으로 명시
- **카메라는 샷 끝에 별도 문장으로.** 형식: `Camera: <무브> at <속도> speed with
  <크기> amplitude, <설명>`
  - 무브: `Push In` / `Push Out` / `Pan Left` / `Pan Right` / `Tilt Up` / `Arc Shot`
    / `Tracking Shot` / `Static Shot`
  - `at slow/fast speed`, `with small/large amplitude`
- 카메라 용어를 서술문에 녹이지 말고 **레이블 붙여 분리**하라

**③ `Soundscape:` — 앰비언스와 폴리**
- 화면에 보이는 동작에 붙은 소리 + 지속 환경음
- 무음이면 `N/A`
- ⭐ **믹스 위계를 명시하라. "크게 주문하라"는 옛 지침이고 지금은 해롭다.**
  아래 4-H 참조

## 4-H. ⭐ Soundscape는 "크기"가 아니라 "위계"로 쓴다 (2026-08-10 정정)

한때 이 스킬은 **"소리를 구체적이고 크게 주문하라"**고 적었다. 그건 레벨이 -45 LUFS로
떨어지던 시절의 우회책이었고, **`NormalizeAudioLoudness`가 레벨 문제를 이미 해결한
지금은 오히려 해롭다.** 크게 주문한 폴리(발소리·타격음)가 믹스를 지배해 버린다.

사용자 판정: *"사운드가 안 어울리고 발소리가 너무 크게 난다."*

### 실측 A/B (832×480 / L124 / 시드 424242 / 동일 장면, Soundscape 문구만 교체)

| | **A. 크게 주문** | **B. 위계 명시** |
|---|---|---|
| 문구 | `Loud reverberant classroom room tone — her loafers clacking hard and fast...` | `A quiet, calm classroom. The dominant sound is a soft warm breeze... Her footsteps are very soft and muffled, barely audible under the breeze, with no hard heel impacts.` |
| 25ms RMS 중앙값 | 173 | 500 |
| 90퍼센타일 | 1525 | 876 |
| **90p / 중앙값** | **8.8** | **1.8** |
| LUFS | -20.4 | -17.0 |

**비율 8.8 → 1.8.** A는 조용한 바닥에 발소리만 튀어나오는 구조고, B는 앰비언스가 바닥을
채워 폴리가 그 위에 얹힌다. **같은 장면, 같은 시드, 문구만 바꾼 결과다.**

### 쓰는 법

1. **먼저 무엇이 지배적인지 선언한다** — `The dominant sound is <지속 환경음>`
2. **폴리는 상대적 크기로** — `very soft and muffled, barely audible under the breeze`
3. **원하지 않는 성질을 부정한다** — `with no hard heel impacts`, `nothing is loud or percussive`
4. 전체 레벨은 건드리지 마라. `NormalizeAudioLoudness`가 알아서 맞춘다

발소리·타격음을 **주인공으로 만들고 싶을 때만** 크게 주문하라. 배경으로 원한다면
크기가 아니라 **위계로** 적어야 한다.

**④ `Music:` — 논디제틱 스코어**
- 실제 악기명과 템포 변화, 타임스탬프 포함:
  `A low drone enters at 0s; strings join at 3s; rhythm peaks at 6s`
- 없으면 `N/A`

### ⚠️ 이 구조가 오디오 문제의 진짜 해법이다

공식 가이드가 **"오디오를 시각 서술에서 완전히 분리하라 — 소리가 없거나 엉뚱하게
나오는 H3 영상의 가장 큰 단일 원인"** 이라고 못 박고 있다.

앞서 이 스킬에서 "소리 묘사를 프롬프트 꼬리에 섞어 쓰라"고 적었던 것은 **틀린
지침이었다.** 실제로 그렇게 써서 -45 ~ -47 LUFS가 나왔던 것이다. `Soundscape:`
라벨을 붙여 문단으로 분리하면 해결된다.

### 실측 — 같은 장면, 프롬프트 형식만 교체 (832×480 / L124 / 20스텝 / 시드 동일)

| | 한 덩어리 문장 | **4단 필드 구조** |
|---|---|---|
| 선화 | 흐릿하고 굵기가 흔들림 | **일정하고 깔끔** |
| 눈 | 캐치라이트 약함 | **또렷한 애니메 눈** |
| 배경 | 뭉갠 노을 | **도시 스카이라인·구름이 살아난 배경화** |
| 오디오 | -45.3 LUFS | -16.1 LUFS (정규화 노드 포함) |

**형식만 바꿔도 눈에 띄게 개선된다.** 내용을 늘린 게 아니라 배치를 바꾼 것뿐이다.

## 4-A. (구) 프롬프트 메모 — 소리를 문장에 섞던 방식

H3에는 **별도의 오디오 프롬프트 입력이 없다.** 한 문장 안에 그림과 소리를 같이 적으면
같은 트랜스포머가 픽셀과 파형을 동시에 뱉는다. 싱크를 맞출 일이 없다.

권장 구성 순서:

1. **피사체** — `A young woman in a red leather jacket`
2. **카메라 워크** — `camera tracking alongside her at hip height`
3. **물리 디테일** — `water splashing from puddles under her boots, wet hair whipping`
4. **동작의 진행** — `she slows to a walk and looks back over her shoulder, then turns forward and keeps moving`
5. **소리** — `steam rising from grates, distant thunder and city traffic noise`

**4번이 길이에 따라 필수가 된다.** 5초를 넘기면서 정적 프롬프트("달린다")만 주면
모델이 같은 포즈에서 얼어붙는다(모션 데드락). 동작을 서사처럼 이어 써라.

Danbooru 태그 나열이 아니라 **자연어 서술**이다. 이미지 모델 프롬프트 습관을 그대로
가져오지 마라.

## 4-B. 애니메·비실사 스타일 — LoRA 없이 프롬프트로 된다

**2026-08 기준 H3용 스타일 LoRA는 존재하지 않는다.** HF·CivitAI에 있는 H3 LoRA는
전부 Turbo(4~8스텝 가속) 계열이다(`lightx2v/Minimax-h3-Turbo`,
`Abiray/MiniMax-H3-Turbo-Lora-Pruned-ComfyUI` 등). 스타일은 프롬프트로 잡아야 한다.

**기법: 매체를 평범한 단어로 선언하고, 유지되어야 할 것을 이름으로 지목하라.**

실측 A/B (832×480 / L124 / 시드 동일, 프롬프트 앞머리만 교체):

| | 앞머리 | 결과 |
|---|---|---|
| **A** | `2D-animated Japanese anime, hand-drawn cel animation with clean black ink outlines and flat cel shading` + `Keep the exact hand-drawn 2D cel look throughout: the same ink outline weight, flat color fills, large anime eyes. No photorealism, no 3D rendering, no live-action footage.` | **TV 애니 셀화. 잉크 아웃라인 선명, 큰 눈, 플랫 채색. 클로즈업 구도.** 지시한 동작(돌아본다→눈이 커진다→미소)을 전부 수행 |
| B | `Anime style.` 만 | 배경화 느낌의 회화체(신카이풍). 선화 약하고 인물이 작다. **동작 지시를 거의 안 따름** |

- 둘 다 **애니메로는 나온다.** H3의 사전학습에 2D 애니메이션이 충분히 들어 있다
- 차이는 **양식의 정확도와 동작 추종**이다. 매체 선언이 약하면 "예쁜 배경 그림"으로
  흐르고 인물 연기가 사라진다
- **부정 지시(`No photorealism, no 3D rendering, no live-action`)가 효과 있다.** H3에는
  별도 네거티브 입력이 없으므로 프롬프트 안에 문장으로 넣어라
- 스타일 유지 문구(`Keep the exact ... the same ink outline weight`)는 15초처럼 긴
  구간에서 특히 중요할 것으로 보인다(미검증)

## 4-C. Turbo LoRA — ✅ 폐기 철회, 전용 노드로 사용 (2026-08-13 대반전)

> ## ⭐ 결론부터: 전용 노드 2종으로 얹으면 8스텝이 20스텝과 동급이다
>
> **2026-08-10의 "최종 폐기"는 오판이었다. 역대 turbo 실측 전부가 '부서진 그래프'
> 위에서 이루어졌다.** generic `LoraLoaderModelOnly`로 pruned 베이스에 얹으면
> time-conditioning이 깨진 채 샘플링되어 반드시 붕괴한다. 배경 노이즈 밭·캐치라이트
> 소실·배경 출렁임 전부 그 잔해였다.
>
> **올바른 배선** (`larryvrh/ComfyUI-MiniMax-H3-Turbo` 커스텀 노드 팩 필수):
> 1. **`MiniMaxH3TurboLoRA`** (MODEL→MODEL, strength 1.0, low_vram off) — pruned
>    베이스를 자동 감지해 `silu(t_emb)` 그리드로 time-conditioning을 런타임 재주입
> 2. **`MiniMaxH3TurboSampler`** (→SAMPLER, SamplerCustomAdvanced에 연결) — 비디오/
>    오디오 이중 flow 스케줄(shift 12/3)을 버전에 맞게 처리. res_multistep 쓰지 마라
> 3. **LoRA 파일은 원본 `minimax_h3_turbo_v4_step600_ema.safetensors`(706MB,
>    larryvrh).** Abiray 병합-어댑트판(620MB)은 양자화 병합에서 업데이트가 반올림에
>    깎여 소프트해진다 — 쓰지 마라
> 4. BasicScheduler `simple`, **6~8스텝** (4는 대모션 스미어 위험, 8 초과는 과선예화)
>
> 정정 그래프 실측(애니메 셀화 832×480 L124 / 8스텝 / 시드 777001): frame60 비교에서
> 20스텝 대조군과 동급 — 선화·캐치라이트·배경 정상, 지시 동작 수행, 사용자 육안 합격.
> 배경 띠 프레임차 0.78/최대 3.84/8초과 0%.
>
> ⚠️ **부서진 그래프와 정정 그래프의 배경 띠 수치가 거의 같았다(0.87 vs 0.78).**
> time-conditioning 붕괴는 공간적 노이즈 밭으로 나타나 프레임차 지표에 안 잡힌다.
> **strip-diff 통과 ≠ 합격. 육안 판정을 생략하지 마라.**
>
> 잔여 미검증: 4스텝 하한, 대모션 스미어, 실사 재시험, 15초/고해상도 실전 스피드업
> (저해상도 5초에서는 wall 85 vs 121초 — 고정비 희석으로 1.4×에 그침), 오디오 품질.

### (구) 2026-08-10 폐기 판정 경위 — 기록 보존

| 시점 | 조건 | 판정 |
|---|---|---|
| 1차 | fl2va + 프롬프트만 / 4스텝 | ❌ 정지컷 붕괴(캐치라이트 소실) — **generic 로더** |
| 2차 | ref2va + 글로벌 레퍼런스 / 5스텝 | ⭕ 정지컷 합격 후 재생에서 기각 — **generic 로더** |
| 최종 | ref2va + 레퍼런스 2장 / 5스텝 / 1152×640 | ❌ 배경 출렁임 — **generic 로더** |

사용자 판정(당시): *"전혀 살지 않았어. 영상 실제로 보면 막 건물들이 쓱쓱 왜곡되고 난리도 아니야."*
→ 세 판 모두 전용 로더 없이 실행됐음이 2026-08-13에 확인되어 판정 무효.
"레퍼런스 조건화는 시간축 일관성을 복구하지 못한다"는 해석도 같은 이유로 근거 상실.

### 모션 붕괴를 수치로 잡는 법 — 배경 전용 프레임차

전체 화면 평균 프레임차로는 **인물 동작에 묻혀서 안 보인다.** 인물이 없는 영역(보통
화면 좌우 끝)만 잘라내서 프레임차를 재라.

```
1152×640 클립의 좌측 200px 띠만 crop → 그레이 축소 → 프레임 간 평균 절대차
```

| 지표 | Turbo 5스텝 (1152×640) |
|---|---|
| 배경 띠 프레임차 평균 | **12.15** |
| 최대 | 64.45 |
| **8 초과 프레임 비율** | **50% (335 중 167)** — 컷 전환 구간 제외 |

배경이 절반의 시간 동안 출렁이고 있었다. **이 지표를 새 가속 기법 검증의 필수 항목으로
삼아라.**

### ⚠️ 정지컷과 재생은 서로를 대체하지 못한다

같은 날 정반대 방향으로 두 번 틀렸다.

- 오전: *"스틸로는 안 보이고 프레임 사이에서 열화가 난다"* → **틀림.** 스틸에서 이미 다 보였다
- 오후: *"스틸 얼굴 크롭이 깨끗하니 통과"* → **틀림.** 재생하니 배경이 무너졌다

**반드시 둘 다 확인하라.** 얼굴은 크롭해서 확대하고, 배경은 재생하거나 배경 전용
프레임차로 재라.

---

(이하 기록용 — 당시 실측 데이터)

## 4-C-1. (구) Turbo LoRA 도입 기록

`Abiray/MiniMax-H3-Turbo-Lora-Pruned-ComfyUI` /
`minimax_h3_turbo_4step_ckpt600_ema_V4.safetensors` (592MB) → `models/loras`

**키 포맷 주의**: 이 LoRA는 `diffusion_model.` 접두사 + **PEFT식 `lora_A`/`lora_B`**이며
`.alpha`가 없다(416키). ComfyUI 네이티브 `lora_down`/`lora_up`과 다르지만,
**0.30.2의 `comfy/weight_adapter/lora.py`가 `lora_A.weight` 형식을 지원하므로 변환 없이
그대로 로드된다.** (SVI LoRA 때와 달리 손댈 필요 없음)

배선: `UNETLoader` → `LoraLoaderModelOnly`(strength 1.0) → `BasicGuider` + `BasicScheduler`

### 3대조군 실측 (832×480 / L124 / 애니메 프롬프트 / 시드 동일)

| 조건 | 소요 | 결과 |
|---|---|---|
| 20스텝 base | 158초 | 기준선. 색이 진하고 선화가 가장 촘촘 |
| **4스텝 + Turbo** | **약 68초** | **구조 정상.** 세일러복·리본 정확, 동작 지시 수행. 색이 다소 옅고 뿌옇다 |
| 4스텝 without Turbo | 약 44초 | **붕괴.** 얼굴 이목구비 왜곡, 의상이 다른 옷으로 변형, 하이라이트 날아감 |

**세 번째 대조군이 핵심이다.** 이게 없으면 "LoRA가 효과 있다"와 "LoRA가 로드 안 됐는데
4스텝이 원래 이렇다"를 구분할 수 없다. 4스텝 단독이 명백히 붕괴했으므로
**Turbo LoRA가 실제로 적용되었다는 사실 자체는 증명된다.**

### ❌ 그러나 실사용 판정은 불합격이다

**사용자 판정: 4스텝 + Turbo는 용납 가능한 품질이 아니다. 정지 프레임 단계에서 이미
무너져 있다** — "예쁜 느낌이 아니라 소름 돋고 무섭다".

20스텝 base와 얼굴을 크롭해 나란히 놓으면 명확하다.

| | 20스텝 base | 4스텝 + Turbo |
|---|---|---|
| 눈 | 하이라이트가 살아 있는 애니메 눈 | **캐치라이트 없는 시커먼 구멍** |
| 피부·채색 | 따뜻하고 균일한 플랫 셀 | 얼룩진 채색, 탁한 톤 |
| 선화 | 일정한 굵기 | 끊기고 지저분함, 목·턱선 왜곡 |
| 배경 | 구름·건물 형태 유지 | 뭉개진 덩어리 |
| 인상 | 살아 있음 | **언캐니, 불쾌** |

> ⚠️ **평가 방식의 실수 — 이게 진짜 교훈이다.**
> "세일러복 있음 ✓ 리본 있음 ✓ 지시한 동작 수행 ✓ → 구조 정상"이라고 판정했다.
> **요소 체크리스트를 채웠는지와 결과물이 보기 좋은지는 전혀 다른 축이다.**
> 생성 결과를 평가할 때 항목 대조로 끝내지 마라. 눈에 보기 좋은가를 먼저 물어라.
> 특히 얼굴은 **크롭해서 확대해 보라** — 축소된 스트립에서는 눈의 캐치라이트가
> 사라진 것도, 선화가 끊긴 것도 보이지 않는다.

**결론: Turbo LoRA는 최종 산출물에 쓰지 마라.** 구도만 대충 보는 프리뷰 용도라면
모르되, 그 정도 목적이면 해상도를 낮추는 편이 부작용이 없다.

**품질을 지키면서 시간을 줄이는 남은 카드**
1. 해상도 하향 (832×480 → 그 이하). 초선형 이득이 있고 증류 부작용이 없다
2. length를 124(5초) 중심으로 운용. 15초는 필요할 때만
3. RAM 증설 → 오프로딩 스트리밍 구간 축소
4. **미탐색: sampler/scheduler 조합.** 현재 `res_multistep` + `simple`은 템플릿
   기본값을 그대로 쓰고 있을 뿐이다. 다른 조합이 더 적은 스텝에서 수렴할 수 있다.
   증류 LoRA 없이 스텝을 줄이는 유일한 정공법이므로 여기부터 탐색할 것

**가속 여지**: `lightx2v` Turbo LoRA가 **4~8스텝**을 표방한다. 현재 20스텝 기준
5초 158초 / 15초 738초이므로, 적용 시 2~4배 단축 가능성이 있다. 미검증 — 품질 대조군을
반드시 두고 시험할 것.

## 4-Q. ⭐ 대사의 수신자와 감정의 단계 (2026-08-11)

브이로그처럼 **인물이 계속 카메라에 말하는 형식**에서는 두 가지가 자동으로 무너진다.

### ① 모든 대사가 "시청자에게 하는 말"로 들린다

클립1 실측. 배를 향해 외치는 대사 `야, 잠깐! 서라고!`가 **카메라를 보고 시청자에게
하는 말처럼** 나왔다. 첫 대사 `흐응~ 결국 따라왔네?`도 마찬가지였다.

**원인**: 인물이 렌즈를 보고 말하는 상태가 기본값이므로, **대사의 수신자를 바꾸려면
명시해야 한다.** 대사 내용만으로는 모델이 방향을 바꾸지 않는다.

**처방 — 대사마다 수신자를 지정하라**

```
카메라(시청자)에게:
  ... turns to the lens and says straight into the camera: <d>[Korean] ...</d>

화면 밖 대상에게:
  ... turns away from the lens toward the departing boat at screen-left and
  shouts off-screen at it, not to the camera: <d>[Korean] ...</d>

혼잣말:
  ... looks down at her own feet and mutters to herself, not to the camera:
  <d>[Korean] ...</d>
```

**시선 + 몸의 방향 + "not to the camera"** 세 가지를 같이 써야 실제로 바뀐다.

### ② 감정 변화가 표현되지 않는다

같은 클립에서 **배가 떠나는 것을 보며 실망하는 감정선**이 전혀 안 나왔다.
원인은 두 겹이다.

- **감정을 한 단어로만 줬다.** `gasps twice, straightens, waves, lets it drop` 같은
  동작 나열은 있었지만 **얼굴이 어떻게 변하는지**는 안 적었다
- **프레이밍이 무릎 위였다.** 실망은 얼굴에서 읽히는데 얼굴이 작으면 보일 자리가 없다
  (4-N절 얼굴 픽셀 규칙의 확장)

**처방 — 감정은 "단계"로 쓰고, 그 단계를 담을 프레이밍을 붙여라**

```
Her face changes in three stages: first her smirk holds as she waves, then her
eyebrows tilt up and her mouth opens slightly as the boat keeps going, and
finally her eyes lower, her shoulders drop and her mouth closes into a flat
line. She is framed from the chest up so her face fills the upper half of the
vertical frame.
```

- **시작 표정 → 무너지는 순간 → 끝 표정** 세 단계로 쓴다
- 눈썹·입·눈꺼풀·어깨를 **각각** 지목한다. `sad`, `disappointed` 같은 감정 이름만으로는
  거의 안 먹는다
- **감정이 핵심인 컷은 반드시 가슴 위 이상**으로 잡는다
- 목소리 딜리버리도 같이 바꾼다 — `her voice drops and flattens, the teasing lilt gone`

**일반 규칙**: 이 모델은 **관찰 가능한 것**(눈썹이 올라간다, 어깨가 내려간다)은 그리지만
**해석**(실망한다)은 못 그린다. **감정을 근육의 움직임으로 번역해서 적어라.**

## 4-P. ⭐ 캐릭터 성격은 4축을 전부 지정해야 산다 (2026-08-11)

**레퍼런스 이미지가 외형을 잡아줘도 성격은 안 따라온다.** 메스가키(새침하고 도발적인)
캐릭터로 설계된 인물이 영상에서는 그냥 해맑은 아이로 나왔다. 원인은 **성격을 지정하는
네 개의 축 중 하나도 안 썼기 때문**이다.

| 축 | 어디에 쓰나 | 안 쓰면 |
|---|---|---|
| ① **표정** | 샷의 시각 서술 | 기본 미소로 수렴 |
| ② **자세·제스처** | 샷의 시각 서술 | 차렷 자세로 수렴 |
| ③ **대사 어투** | `<d>` 태그 **안** | 밋밋한 표준어 |
| ④ **목소리** | `<d>` 태그 **밖** | 무난한 기본 음색 |

### ④ 목소리 — 공식 지원 항목이 명확하다

공식 가이드가 지정 가능한 속성을 못 박고 있다: **화자가 처음 발화할 때 태그 밖에
character type, age, gender, on-screen 여부, pitch, timbre, speaking rate, accent,
그리고 delivery(전달 방식)를 적어라.**

공식 예시:
```
The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>
The two children (S1,S2) shout together, <d>[English] Wait for us!</d>
The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d> while his lips remain completely closed.
```

- 화자 ID는 `(S1)`, `(S2)`. **동시 발화는 `(S1,S2)` 복합 ID**
- **화면 밖 내레이션이 가능하다** — `in an off-screen voiceover` + `while his lips
  remain completely closed`
- 발성하지 않는 인물에게는 ID를 주지 마라
- 목소리 묘사는 **첫 발화 때** 붙이고, 이후 샷에서는 ID로 참조한다

### 성격별 목소리 서술 예시

```
높고 도발적인 소녀 (메스가키)
  a high, bright, slightly nasal girlish voice (S1), fast and clipped, with a
  sing-song teasing lilt that drags out the last syllable of each sentence and
  a short snorting laugh

차분한 성인 여성
  a low, warm, breathy voice (S1), slow and even, with almost no inflection

지친 중년 남성
  a low gravelly male voice (S1), slow with long pauses, trailing off at the
  end of each phrase
```

### ①②③ 나머지 세 축도 같이 써야 한다

목소리만 바꾸면 **말투는 도발적인데 얼굴은 해맑은** 어긋난 결과가 나온다.
성격은 네 축이 같은 방향을 가리켜야 성립한다.

메스가키 캐릭터를 예로 들면:

- **표정**: `half-lidded eyes`, `a smug closed-mouth smirk`, `one eyebrow raised`,
  `a wide toothy grin with the tip of her tongue showing`
- **자세·제스처**: `both fists on her hips`, `leaning forward into the lens`,
  `head tilted`, `chin tipped up`, `jabbing a finger at the camera`,
  `waving a hand dismissively`
- **대사 어투**: 반말·도발형 어미로 쓴다. `<d>[Korean] 뭐야, 아직도 그거 몰랐어?</d>`
  같은 식. **번역하지 말고 그 언어의 화법으로 직접 쓴다**

> ⚠️ 참고: **음성 레퍼런스는 음색만 전이한다.** 억양·감정·속도는 전이되지 않으므로
> 중요하면 프롬프트에 따로 써라(RunDiffusion 가이드).

**출처**: [MiniMax-H3 공식 프롬프트 가이드](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md),
[RunDiffusion 프롬프트 가이드](https://www.rundiffusion.com/minimax-h3-prompt-guide)

## 4-D. ⭐ 대사 — `<d>` 태그가 전부다 (검증 완료)

**Soundscape에 소리만 적고 대사를 지정하지 않으면, 모델은 어느 언어도 아닌 웅얼거림을
만들어낸다.** 실제로 그렇게 나왔고 사용자가 "무슨 언어인지 인지가 안 된다"고 지적했다.
대사를 넣고 싶으면 전용 태그를 써라.

```
The girl (S1), a bright cheeky teenage voice with a teasing sing-song delivery,
says: <d>[Korean] 뭐야, 아직도 그거 못 했어?</d> then adds: <d>[Korean] 내가 도와줄까?</d>
```

- **태그 안**: 언어 태그 + 발화 내용만. 문장부호 포함 원문 그대로, 번역하지 마라
- **태그 밖**: 화자 ID(`(S1)`, `(S2)`), 목소리 묘사, 동작, 딜리버리
- 대사는 클립 길이에 들어갈 만큼 짧게. 5초에 짧은 두 문장이 적당하다

### 실측 — 한국어/영어 대조 (2026-08-10, 1152x640 / L124 / 시드 551122 / 동일 장면)

| 언어 태그 | 소요 | 판정 |
|---|---|---|
| `[Korean]` | 332초 | **깔끔하게 발화됨 (사용자 청취 확인)** |
| `[English]` | 329초 | **깔끔하게 발화됨 (사용자 청취 확인)** |

**한국어가 된다.** 중국 계열 모델이라 한국어 지원을 기대하지 않았으나 두 언어 모두
알아들을 수 있는 수준으로 나왔다. 파형상 영어는 연속형, 한국어는 산발형으로 보였으나
청취 판정은 둘 다 합격이었다 — **파형 분포로 발화 품질을 판정하지 마라.**

## 4-R. ⭐ 무대사 샷의 웅얼거림 — 그림이 소리를 만든다 (2026-08-13 실측)

**증상**: 대사 없는 샷에서 정체불명(일본어풍) 웅얼거림이 생성됨. 가슴 위 프레이밍 +
감정 연기(미소, 숨 들이쉬기)가 있는 인물 샷에서 발생.

**A/B/C/D 실측** (같은 시드·같은 샷, ref2va 20스텝, 사용자 청취 판정):

| 조건 | 조작 | 웅얼거림 |
|---|---|---|
| A | 원본 | 발생 |
| B | Soundscape에 부정문만 ("she does not speak; no voice, no humming...") | **잔존** |
| C | 그림 서술 수정 — `her lips stay gently closed throughout` + "breathes in slowly"→"her chest rises as she takes a quiet breath" | **소멸** |
| D | B+C | 소멸 |

**결론: 발성은 오디오 지시가 아니라 시각 서술이 유발한다.** 같은 트랜스포머가 픽셀과
파형을 함께 뱉으므로, 소리도 그림 서술을 따른다(0절 원칙 2의 오디오 확장).
Soundscape 부정문 단독은 무효 — 입과 호흡의 **시각 상태**를 지정해야 한다.

### ⭐ 예외 — **입이 열리는 비발화 동작은 억제 문구로 못 막는다** (2026-08-13 추가 실측)

먹기·하품·헐떡임처럼 **입이 열려야 성립하는 동작**을 지시하면, 발성 억제 문구를 정확히
넣어도 정체불명 언어의 발화가 생성된다. 4-R의 인과("시각 상태가 발성을 결정한다")가
그대로 작동하는 것이며, 여기서는 시각 상태 자체가 열린 입이므로 부정문이 무력하다.

실측 (음성대역 300~3400Hz 에너지 비율, 같은 씬):

| 샷 | tier | 입 열림 | 평균 / 최대 |
|---|---|---|---|
| 무인 와이드 | ambient | ✗ | 0.436 / 0.592 |
| 대사 샷 2개 | talk | (발화) | 0.57 / 0.995 |
| **먹는 샷** | ambient | **✓** | **0.695 / 0.993** — 대사 샷보다도 높다 |

**처방은 프롬프트가 아니라 파이프라인이다**: 먹기·하품 등 입이 열리는 무대사 샷은
**오디오 폐기 대상**으로 분류하고 폴리를 post에서 얹어라. `Her mouth opens only to take
the food in and stays closed while she chews` 같은 문구는 화면상 씹는 동작을 정돈하는
효과는 있으나 **오디오는 막지 못한다.**

**무대사 인물 샷 표준 문구**:
1. `Her lips stay gently closed throughout the shot.` (필수)
2. 발성 인접 동사 금지: breathes in / sighs / gasps / hums / murmurs →
   보이는 신체로 번역: `her chest rises slowly`, `her shoulders lift and settle`
3. Soundscape 부정문은 이중 안전장치로 병기 가능 (단독 의존 금지)

참고: 정량 지표(음성대역 300~3400Hz 비율)는 파도·바람이 같은 대역을 점유해 **판별
실패**. 웅얼거림 판정은 청취로 하라. (수치 게이트 ≠ 최종 판정 — turbo 교훈과 동일)

## 4-K. ⭐ 오버레이 그래픽 — 된다 (2026-08-11 검증)

**H3는 비디제시스(non-diegetic) 오버레이 레이어를 그린다.** 로어서드 자막바, 코너
시계, 슬라이드 인 애니메이션까지 지시대로 나온다.

### 실측 (832×480 / L124 / 여행 브이로그 샷)

지시한 것과 결과:

| 요구 | 결과 |
|---|---|
| 좌하단 흰 라운드 사각 바 + 검은 대문자 `HARBOR TOWN` | ✅ 정확 |
| 그 아래 작은 줄 `DAY 2` | ✅ 정확 |
| 우상단 디지털 시계 `11:42` | ✅ 정확 |
| **왼쪽 가장자리에서 슬라이드 인** | ✅ 0.8초에 절반만 들어와 있고 2.0초에 완착 |
| **카메라가 트래킹해도 그래픽은 고정** | ✅ 화면에 붙어 있고 씬과 함께 움직이지 않음 |

**텍스트 정확도·위치·진입 애니메이션·비디제시스 거동이 전부 성립했다.**

### 쓰는 법 — "화면 위에 합성된 평면 UI"라고 못 박아라

```
Composited on top of the footage as a flat non-diegetic motion-graphics
overlay layer: a lower-third title card slides in from the left edge in the
bottom-left corner, a solid white rounded rectangle bar containing the black
capital text "HARBOR TOWN" with a smaller line under it reading "DAY 2", and
in the top-right corner a small white digital clock readout showing "11:42".
These graphics are flat 2D UI elements drawn over the picture, not objects
inside the scene, and they do not move with the camera.
```

필수 요소 넷:
1. **`Composited on top of the footage as a flat non-diegetic ... overlay layer:`** —
   장면 안의 간판·표지판이 되지 않게 하는 선언
2. **모양·색·위치** — `solid white rounded rectangle bar`, `bottom-left corner`
3. **문구를 따옴표로** — `the black capital text "HARBOR TOWN"`
4. **`they do not move with the camera`** — 카메라에 딸려가지 않게 고정

### 한계와 미검증

- **미검증**: 한글 오버레이, 긴 문장, 3개 초과 동시 요소, 진입/퇴장 **시각 지정**
  (`fades out at 00:04.000`), 세이프 에어리어 준수
- **수정이 불가능하다.** 픽셀에 구워지므로 오타 하나에 재생성(수십 분)이다
- **폰트·자간·브랜드 컬러를 정확히 맞춰야 하면 후반 합성이 정답이다.**
  `ffmpeg drawtext`나 편집 툴로 얹으면 즉시 수정되고 비용이 0이다

**판단 기준**: 분위기용 러프 그래픽이면 프롬프트로, **정확성이 요구되면 후반 합성으로.**

## 4-L. ⭐ 오디오 디렉팅 — 교과서 기준을 프롬프트로 옮기기 (2026-08-11)

H3는 **스템(dialogue/music/SFX 분리 트랙)을 주지 않는다.** 완성된 스테레오 믹스 하나가
나온다. 따라서 **믹스 판단을 사후에 못 고치고, 프롬프트 안에서 미리 지시해야 한다.**
아래는 영화 사운드의 표준 원칙을 H3 프롬프트로 번역한 것이다.

### ① 3층 위계 — 대사 > 효과·앰비언스 > 음악

교과서 원칙: **대사가 최상위이며 가장 보호받는 요소다. 무엇이 양보하더라도 대사는
아니다.** 음악은 그 아래 깔리는 감정의 침대이고, 목소리와 경쟁해서는 안 된다.
효과음과 앰비언스는 화면에 현실감을 판다.

프롬프트 번역:
```
Her voice is the clearest and most present element in the mix, always in front.
The ambience sits behind it and the music sits furthest back.
```

### ② 더킹 — 대사 구간에서 음악을 3~5dB 내린다

교과서에서는 사이드체인 컴프레서로 자동 처리한다(대사가 트리거, 음악 버스가 3~5dB
하강). H3에는 버스가 없으므로 **말로 지시한다.**
```
The music drops back and thins out whenever she speaks, then returns to full
level in the gaps between her lines.
```

### ③ 씬 전환 — J컷 / L컷 / 스팅어

- **J컷**: 다음 씬의 소리가 그림보다 **먼저** 들어온다
- **L컷**: 이전 씬의 소리가 그림이 바뀐 뒤에도 **이어진다**
- 둘 다 전환을 매끄럽게 하고 씬을 정서적으로 묶는 표준 기법이다

프롬프트 번역 (컷 타임스탬프와 짝지어 쓴다):
```
The harbor ambience of the next shot fades in about half a second before the
cut at 00:05.200 (J-cut), while the alley footsteps continue for a moment
after the cut (L-cut).
```

스팅어·크로스페이드:
```
A short bright cymbal swell lands exactly on the cut at 00:10.400.
The two ambiences crossfade across the cut rather than switching abruptly.
```

### ④ 음악 스타일 지시 — 악기·템포·역할·변화 시점

`Music:` 문단에는 **장르 이름 대신 악기와 사건**을 써라.
```
Music: A bright ukulele strum with soft hand claps enters at 0s; a warm brass
line joins at 5s as the harbor opens up; a light shaker joins at 10s; the
arrangement thins to a single ukulele line from 12s.
```

> ⚠️ **실측 — 진입은 지켜지고 감쇠는 약하다.** `from 13s ... fades out`,
> `stops dead on the last frame` 같은 **종료·페이드 지시는 무시되는 경우가 많았다.**
> 시작 시점은 신뢰해도 되지만, **끝맺음이 중요하면 후반에서 페이드아웃을 걸어라**
> (`ffmpeg afade=t=out`). 시작 지시조차 안 먹으면 악기 수를 줄여라.

### ⑤ 디제시스 / 비디제시스 구분

화면 안 음원(라디오, 노점 그릴, 인물의 발소리)과 화면 밖 스코어를 **문장에서 구분**하라.
섞어 쓰면 모델이 스코어를 환경음처럼 처리해 위계가 무너진다.
```
Diegetic: oil sizzling on the grill right in front of her, close and dry.
Non-diegetic: the ukulele score sits behind everything, room-less and wide.
```

### ⑥ 최종 레벨 — 생성이 아니라 마스터링에서 잡는다

`NormalizeAudioLoudness`는 **integrated LUFS만 맞추고 트루피크를 제한하지 않는다.**
자세한 것은 4-H절과 5절 참조. 요약하면:
- 그래프 안 노드는 **-23** (폭주 방지)
- 내보낼 때 **ffmpeg loudnorm 2패스 + TP=-1.5**로 트루피크 제한

**출처**: 사운드 위계·더킹·J컷/L컷의 정의는 아래 자료의 표준 서술을 따랐다 —
[Sound Design for Film: A Complete Guide](https://pixflow.net/blog/sound-design-for-film/),
[How to Mix Dialogue, Music & Sound Effects](https://pixflow.net/blog/audio-mixing-premiere-pro/),
[The Hierarchy of Sound in Film](https://admi.africa/resources/an-insiders-perspective-the-power-of-sound-in-film-and-music),
[Film Appreciation — Sound (OpenALG)](https://alg.manifoldapp.org/read/film-appreciation/section/fa330673-c6e5-4a63-9e35-eef1a299091b).

## 4-N. ⭐ 픽셀이 모자라면 안 그려진다 — 입과 화면 속 화면 (2026-08-11)

같은 클립에서 **말하는 입**과 **폰 액정 내용**이 둘 다 뭉갰다. 원인은 같다 —
**그 요소에 할당된 픽셀이 너무 적다.**

### ① 입이 안 움직인다

832×480 / 무릎 위 프레이밍 실측. 얼굴 세로가 약 90px, **입은 15~20px**이다.

| 시각 | 입 |
|---|---|
| 0.8~1.8초 | **닫힌 미소 — 말하는 중인데 거의 안 움직인다** |
| 2.3~3.3초 | 벌린 입 하나를 **그대로 유지**. 음소별 변화 없음 |

두 겹의 문제다.

- **초반 1~2초는 원래 뻣뻣하다.** 모션 워밍업 구간이라 입도 늦게 열린다.
  **대사를 세그먼트 첫 1초에 배치하지 마라.** 체인이면 `context_length`(기본 22프레임
  ≈ 0.92초)만큼 앞이 잘려나가므로 더욱 그렇다
- **입이 15px면 음소를 그릴 자리가 없다.** 열림/닫힘 두 상태를 오갈 뿐 립싱크가 아니다

**처방**
- **말하는 샷은 프레이밍을 올려라.** 무릎 위(knees-up)가 아니라 **가슴 위(chest-up)나
  클로즈업**. 얼굴 세로가 최소 화면의 1/3은 되어야 입이 산다
- 대사는 샷 **중반 이후**에 배치한다
- 입 동작을 명시한다 — `her mouth opens and closes clearly on each syllable as she
  speaks` 정도는 넣어라. 다만 위 실측상 프레이밍만큼 효과가 크진 않다
- 립싱크가 정말 중요하면 **얼굴 클로즈업 컷을 따로 잡아라.** 걸어오면서 말하는
  풀샷에 립싱크까지 기대하지 마라

### ② 화면 속 화면(폰 액정, 모니터, TV)은 뭉갠다

같은 클립에서 폰 액정은 **약 40×70px**이었다. 셀피 프리뷰가 있어야 할 자리에
얼굴 비슷한 얼룩과 파란 UI 띠만 남았다.

**원인 둘**
- 절대 픽셀이 부족하다. 40×70px에 UI를 그릴 수 없다
- **무엇이 떠 있어야 하는지 지정하지 않았다.** 미지정 = 매 프레임 임의 생성 = 얼룩

**⭐ 기본 방침 — 화면을 보여주지 마라 (2026-08-11 확정)**

액정 내용을 프롬프트에 넣지 않는 것을 **기본값**으로 삼는다. 이득보다 위험이 크다.
얻는 것은 작은 디테일 하나인데, 실패하면 **화면 한복판에 얼룩이 박힌 채로 수십 분짜리
렌더가 끝난다.**

```
the phone is turned away from the observing camera so only its flat black back
is visible; its screen is never seen
```

**예외 — 화면이 서사상 반드시 보여야 할 때만**
1. **단순 고대비 내용으로 지정한다** — `the phone screen shows a plain bright blue
   screen with a single white circular record button in the centre`. 형태가 단순할수록
   작은 픽셀에서도 읽힌다
2. **후반 합성한다** — 액정 영역에 별도로 만든 UI를 얹는다. 정확한 UI가 필요하면 이것뿐

같은 원칙이 모니터·TV·간판·계기판·명찰에도 적용된다. **작은 화면과 작은 글자는
기본적으로 "안 보이게" 설계하고, 꼭 필요할 때만 크게 잡아라.**

**일반화**: 화면 안의 글자·아이콘·계기판·간판 등 **작고 구조적인 요소는 크게 잡히지
않으면 포기하라.** 오버레이 그래픽(4-K절)이 잘 나오는 이유는 **화면 전체 좌표계에
큼직하게 그려지기 때문**이다. 같은 텍스트라도 폰 액정 안에 넣으면 뭉갠다.

## 4-M. ⭐ 자유로운 손은 얼굴·머리에서 떼어 놓아라 (2026-08-11)

**손이 얼굴이나 머리카락과 겹치는 구간에서 손가락이 뭉개진다.** 1344×768 실측에서
인물의 자유로운 손이 공중에 있을 때는 손가락 다섯 개가 또렷했는데, **머리카락을 귀
뒤로 넘기려고 얼굴 쪽으로 올라간 순간부터 손이 덩어리로 무너졌다.**

| 시각 | 손 위치 | 상태 |
|---|---|---|
| 1.0초 | 공중에서 손 흔들기 | ✅ 손가락 5개 또렷 |
| 1.6초 | 머리카락에 접근 | ⚠️ 손가락이 붙기 시작 |
| 2.2~3.8초 | **얼굴·머리와 겹침** | ❌ 덩어리, 손가락 소실 |

### 원인 셋

1. **오클루전 구간의 모호성** — 손과 머리카락이 겹치면 어느 픽셀이 손가락이고 어느
   픽셀이 머리카락인지 경계가 무너진다. 둘 다 곡선이고 색 대비도 낮다
2. **해상도 대비 손이 너무 작다** — 1344×768에서도 손은 60~80px다. 손가락 하나가
   10px 남짓이라 미세 관절이 표현될 자리가 없다
3. **한 샷에 손 동작을 여러 개 시켰다** — "두 번 흔들기 → 머리 넘기기 → 앞을 가리키기"
   를 8.7초에 넣었다. 자세 전환이 잦을수록 중간 프레임이 뭉개진다

### 처방

- **자유로운 손의 일감을 얼굴에서 떨어진 위치로 준다.** 가슴 높이에서 흔들기, 슬링백
  끈에 얹기, 바깥쪽을 가리키기는 안전하다. **머리 넘기기·턱 괴기·볼에 손대기는 위험하다**
- **손 모양을 명시한다** — `fingers together, palm flat, thumb tucked` 처럼 적으면
  관절 자유도가 줄어 뭉개짐이 덜하다
- **한 샷에 손 동작은 하나.** 여러 개가 필요하면 샷을 나눠라
- 손을 클로즈업에서 얼굴 옆에 두어야 한다면(엄지척 등) **손이 얼굴과 겹치지 않는
  위치**임을 명시하라 — `beside her cheek but not overlapping her face or hair`

## 4-O. ⭐⭐ 짧은 세그먼트일수록 동작을 촘촘히 적어라 (2026-08-11)

**5초 세그먼트에 동작 지시를 하나씩만 줬더니 대부분 무시됐다.** 6세그먼트 26초
클립에서 지시한 동작 12개 중 화면에서 확인되는 것은 3~4개뿐이었고, 나머지는 전부
"걸어오면서 폰 들고 웃기"라는 기본 자세로 수렴했다.

| 세그먼트 | 지시 | 결과 |
|---|---|---|
| 1 | 손 두 번 흔들기 | ❌ 왼손이 그냥 내려가 있음 |
| 2 | 왼손으로 앞을 가리킴 | ⚠️ 가리키는 게 아니라 팔만 벌림 |
| 3 | 바다를 봤다가 렌즈로, 머리 넘기기 | ⚠️ 머리 넘기기만 |
| 4 | 속도 줄이며 손차양 | ❌ 손차양 없음 |
| 5 | 멈춰서 몸 4분의 1 회전 | ❌ 계속 정면 |
| 6 | 손 흔들며 작별 | ❌ 폰 든 정면 유지 |

사용자 체감: **"진행이 너무 느리다."** 정확한 지적이었다.

### ⚠️ "5초라서 안 되는 것"이 아니다 — 반례가 있다

같은 832×480 / L124(5.17초) 세그먼트 체인인데 **동작이 전부 수행된 판이 있다.**
칠판 낙서 판(4세그먼트)은 5초짜리 한 세그먼트 안에서
`책상에서 밀어내기 → 몸 세우기 → 걷기 시작 → 손이 책상을 훑기`를 전부 해냈다.

**차이는 길이가 아니라 동사 밀도였다.**

| | 동작 서술 길이 | 동사 수 | **100자당 동사** |
|---|---|---|---|
| 실패한 chain6 | 1,833자 | 5개 | **0.3** |
| 성공한 칠판 판 | 143자 | 5개 | **3.5** |

**7~10배 차이다.** chain6의 동작 문장은 길기만 했지 그 안에 배경 배치
(`moored boats at screen-right`), 프레이밍(`framed from the knees up, fills the centre
third`), 거리 고정 문구가 섞여 있었고 **실제 동사는 다섯 개뿐**이었다. 반대로 칠판 판은
143자가 통째로 동사 나열이었다.

성공한 칠판 판의 동작 문장 전문:
```
S1 pushes off a school desk, straightens up and starts walking steadily to her
left along the row of desks, one hand trailing across the desktops.
```

### 규칙 — 동작 문장은 짧고 동사가 촘촘해야 한다

**분량을 늘리지 말고 밀도를 올려라.**

- **동작 문장에 배경·프레이밍·의상·거리 고정 문구를 섞지 마라.** 그것들은 별도 문장으로
  분리한다. 섞으면 동사가 묻힌다
- 5초 세그먼트에도 **동사 3~5개**를 연속으로 나열한다 — `she does A, then B, then C`
- 목표치: **동작 문장 100자당 동사 2개 이상.** 0.5 아래면 거의 확실히 무시된다
- **카메라를 세그먼트마다 바꿔라.** 전부 Tracking이면 컷이 바뀐 줄도 모른다
- 롱테이크 연속성(`no cut`)은 **브이로그·정보 전달물에는 오히려 독이다.** 진행감이
  사라진다. 컷을 허용하고 샷 사이즈를 바꾸는 편이 낫다

**판정법**: 완성본을 보고 **"내가 지시한 동작을 하나씩 손가락으로 짚을 수 있는가"**를
물어라. 못 짚는 지시가 절반을 넘으면 **동사 밀도를 재라.**

### ★ 더 심각한 축 — 손목시계 너머에서 새 손이 돋아난다

뭉개짐보다 치명적인 결함이 뒤이어 나왔다. **손목시계 너머에서 손이 새로 생성되어,
한 팔에 손이 두 개처럼 보이는 프레임이 나온다.** 6.9~7.9초 구간에서 관찰됐다.

발생 조건 — 네 가지가 겹쳤을 때 나왔다:

1. **레퍼런스 이미지에는 손목시계**(스트랩 + 원형 페이스)가 그려져 있다
2. 그런데 **텍스트에서는 그것을 `wristband`(밋밋한 밴드)라고 불렀다** ← ★
3. 그 손이 **얼굴·머리 근처로 올라가 경계가 모호한 상태**다
4. 그 손에 **연속된 일감이 없어 자세가 애매하게 유지**된다

**가설 두 겹**

- **① 레퍼런스와 텍스트가 다른 물건을 가리켰다.** `<Picture 1>`에는 시계인데 텍스트는
  밴드라고 했다. 모델이 그 부위를 무엇으로 그려야 할지 확신하지 못한 채 매 프레임
  재해석한다. **레퍼런스에 있는 것을 텍스트에서 다른 이름으로 부르지 마라.**
- **② 손목의 강한 가로 구조가 "팔의 끝" 분절 신호로 작동한다.** 특히 시계는 스트랩에
  더해 **원형 페이스**까지 있어서, 그 원형 덩어리가 작은 손·주먹으로 재해석되기 쉽다.
  그 너머가 오클루전으로 모호해지면 토폴로지가 리셋되어 새 손을 다시 생성한다.

실제로 **시계가 없는 쪽 손(폰을 든 손)에서는 8.7초 내내 이 결함이 0회였다.**

**대응**
- **레퍼런스에 있는 액세서리는 텍스트에서도 같은 이름으로 부르라.** 시계면 시계,
  밴드면 밴드
- 얼굴 근처로 올라가는 손에는 **손목 액세서리를 채우지 마라.** 필요하면 정적인 쪽
  (소품을 든 손) 손목에 채운다
- 유지해야 하면 **그 손을 얼굴에서 떨어뜨려라**(위 처방과 동일)
- 부정 지시를 병기하라 — `she has exactly two hands, one on each arm; no extra hand and no duplicated hand at her wrist`

⚠️ 미검증 가설이다. **시계 유무 A/B, 그리고 명칭 일치 A/B로 확인할 것.**

### ⚠️ 곁들여 발견 — 액세서리도 좌우가 바뀐다

같은 클립에서 `a black wristband on her right wrist`라고 지정했는데 **실제로는 왼손목에
채워져 나왔고, 물건도 밴드가 아니라 손목시계로 나왔다**(레퍼런스가 시계였다). 소품-손 결합과 같은 문제이며, 액세서리도 좌우 지정이 필요하다면
**화면 방향까지 같이 적어라** — `a black wristband on her right wrist, which appears on
the LEFT side of frame`.

이 좌우 반전이 위 "새 손" 결함을 키웠을 가능성도 있다 — **모델이 어느 손목에 밴드가
있어야 하는지 확신하지 못한 상태**였기 때문이다.

## 4-J. ⭐⭐ 장면 명세 프로토콜 — 생성 전 필수 절차 (2026-08-11)

> **이 절은 선택이 아니다.** 15초 1152×640 한 판이 36분, 30초 두 판이 2시간 14분이다.
> **리테이크 비용이 프롬프트 작성 비용의 수백 배**이므로, "돌려보고 고친다"는 전략이
> 성립하지 않는다. 생성 버튼을 누르기 전에 **화면에 나타날 모든 것을 사진 찍듯이
> 기술**해 두어야 한다.

### 원칙 — 모델이 고르게 두지 마라

프롬프트에 명시되지 않은 요소는 **매 프레임 모델이 새로 고른다.** 정체성처럼 강하게
붙잡히는 축도 있지만, 대부분은 자유롭게 흔들린다. 실제로 겪은 사례:

- 손을 안 정해서 → **폰이 좌우 손을 오가고 회전 중 사라짐**
- 컷마다 의상을 다시 안 써서 → **보타이가 대형 리본으로, 셔츠가 조끼로 변형**
- 거리를 안 고정해서 → **인물이 스스로 멀어져 연기가 소실**
- 촬영 주체를 안 정해서 → 셀피인데 폰이 화면에 보이는 **논리적 모순**

### ⚠️ 길이는 지표가 아니다 — 실측

실패한 30초 브이로그의 실제 전달 프롬프트는 **세그먼트당 2966자 / 2922자**였다.
`prompt_prefix` 1202자 + 씬 프롬프트 약 1700자. **분량은 충분했는데도 위 네 가지가
전부 터졌다.** 길이가 아니라 **축의 누락**이 문제다.

- **하한선 2000자**는 지키되(그 아래면 반드시 뭔가 빠져 있다), **통과 기준으로 삼지 마라**
- 통과 기준은 아래 체크리스트 16축을 **전부 명시적으로 채웠는가**이다

### 장면 명세 체크리스트 — 16축

**샷 하나마다** 아래를 채운다. 값이 "굳이 안 정해도 되는 것"이라도 **의도적으로
비운다고 적어라**(예: `the background crowd is irrelevant and may vary`).

| # | 축 | 반드시 적을 것 | 빠뜨리면 |
|---|---|---|---|
| 1 | **피사체 정체성** | 얼굴·머리 모양/색/장식, 체형, 나이대 | 인물이 다른 사람으로 바뀜 |
| 2 | **의상 전체** | 상의·하의·신발·양말·액세서리 + **가방 등의 착용 위치** | 컷마다 옷이 재해석됨 |
| 3 | **소품 ↔ 손 결합** | 어느 손인지, 나머지 손의 역할, 회전·가림 구간 처리 | 소품이 손을 바꾸고 사라짐 (4-I절) |
| 4 | **자세와 시선** | 몸이 향한 방향, 시선 방향, 무게중심, 팔다리 위치 | 어정쩡한 포즈로 수렴 |
| 4-b | **자유로운 손의 위치** | 얼굴·머리에서 떨어진 곳에 일감을 주고 손 모양까지 명시 | 손가락이 덩어리로 뭉개짐 (4-M절) |
| 5 | **동작의 진행** | 시작 → 중간 → 끝. **동작 문장은 동사만 촘촘히**(100자당 2개 이상), 배경·프레이밍은 분리 | 모션 데드락, 기본 자세로 수렴 (4-O절) |
| 6 | **카메라** | 무브·속도·진폭 + **높이와 거리** | 인물이 멀어지거나 구도가 흔들림 |
| 7 | **프레이밍** | 샷 사이즈, 인물이 화면에서 차지하는 비율, 여백 방향 | 목적한 연기가 안 보임 |
| 7-b | **말하는 샷의 얼굴 크기** | 대사가 있으면 가슴 위 이상. 얼굴 세로가 화면 1/3 이상 | 입이 안 움직인다 (4-N절) |
| 7-c | **화면 속 화면** | **기본은 안 보이게 돌린다.** 꼭 보여야 하면 단순 고대비 내용을 지정 | 액정이 얼룩으로 뭉갠다 (4-N절) |
| 8 | **공간과 배경** | 장소, **인물 뒤/좌/우에 각각 무엇이**, 지면 재질 | 배경이 매번 다른 곳이 됨 |
| 9 | **조명** | 광원 방향, 시간대, 그림자가 지는 방향, 역광/순광 | 컷 사이 조명이 튐 |
| 10 | **색 팔레트** | 지배색 2~3개 | 색 드리프트 |
| 11 | **부수 요소의 움직임** | 바람·물·연기·군중·동물·천의 흔들림 | 배경이 정지 사진처럼 죽음 |
| 12 | **시간축** | 타임스탬프별 사건 (`At 00:05.200, hard cut to ...`) | 컷 타이밍이 뭉개짐 |
| 13 | **촬영 주체** | 누가 찍고 있는가. **POV면 그 장비는 화면에 없어야 한다** | 논리적 모순 → 소품 불안정 |
| 14 | **오디오 위계** | 지배음 → 폴리의 상대 크기 → 원치 않는 성질 부정 | 발소리가 믹스를 지배 (4-H절) |
| 15 | **대사** | `(S1)` + 목소리 묘사(태그 밖) + `<d>[Korean] ...</d>` | 정체불명 웅얼거림 (4-D절) |
| 16 | **부정 지시** | 매체·의상·인원수·화풍에 대한 금지 | 3D화, 인원 증식, 의상 변형 |
| 19 | **오버레이 그래픽** | 로어서드·코너 HUD의 모양·위치·문구·진입 방식, 비디제시스 선언 | 장면 안 간판이 되거나 카메라에 딸려감 (4-K절) |
| 20 | **믹스 위계와 전환** | 대사>앰비언스>음악, 더킹, J/L컷, 스팅어 (4-L절) | 음악이 대사를 덮고 컷에서 소리가 뚝 끊김 |
| 21 | **캐릭터 성격 4축** | 표정 / 자세·제스처 / 대사 어투 / 목소리(pitch·timbre·rate·accent·delivery) | 성격이 사라지고 기본 미소로 수렴 (4-P절) |
| 22 | **대사의 수신자** | 렌즈에게 / 화면 밖 대상에게 / 혼잣말. 시선+몸 방향+부정문 3종 세트 | 모든 대사가 시청자에게 하는 말로 들린다 (4-Q절) |
| 23 | **감정의 단계** | 시작 표정 → 무너지는 순간 → 끝 표정. 눈썹·입·눈꺼풀·어깨를 각각 지목 + 가슴 위 프레이밍 | 감정선이 통째로 사라진다 (4-Q절) |

**연속 세그먼트라면 추가 2축**
- **17. 경계 연속성** — 이전 세그먼트 마지막 동작을 **같은 속도·같은 방향으로** 이어라.
  새 장소를 서술하면 씬 점프가 된다
- **18. 불변 선언** — 세그먼트가 바뀌어도 유지될 것들(`prompt_prefix`)과 바뀔 것들(씬
  `prompt`)을 분리한다

### ⭐ 필수 검토 단계 — 다른 에이전트에게 반드시 리뷰받는다

**자기가 쓴 프롬프트의 구멍은 자기 눈에 안 보인다.** 위 실패 네 건 전부 "다 적었다"고
생각한 상태에서 나왔다. 생성 전에 **반드시 별도 에이전트에게 검토를 받아라.**

절차:
1. 프롬프트 초안 작성 (16축 자체 점검)
2. **서브에이전트에 아래 검토 지시문 + 초안 전달**
3. 반환된 지적을 **전부 반영**하거나, 반영하지 않을 근거를 명시
4. **blocking 항목이 0이 될 때까지 2~3을 반복**
5. 그 다음에 생성

검토는 `Agent` 도구 또는 `bridge_delegate`로 띄운다. **검토자에게는 "좋다/나쁘다"를
묻지 말고 "무엇이 미지정인가"를 물어라.**

```
너는 영상 생성 프롬프트 감사자다. 아래 프롬프트로 MiniMax H3 영상을 생성하려 한다.
한 번 생성에 36분~2시간이 걸리므로 리테이크가 사실상 불가능하다. 네 임무는
칭찬이 아니라 결함 적출이다.

[검토 원칙]
- 프롬프트에 명시되지 않은 모든 요소는 모델이 매 프레임 임의로 고른다고 가정하라.
- "적혀 있으니 되겠지"가 아니라 "이 문장만 읽고 그림을 그린다면 어디가 흔들릴까"를 물어라.
- 애매어를 색출하라. 크다/작다/천천히/자연스럽게 같은 상대어는 기준이 없으면 결함이다.
- 서로 모순되는 지시를 색출하라. 특히 촬영 주체와 화면에 보이는 것의 모순.
- 각 지적은 반드시 (a) 어느 축이 (b) 왜 위험하고 (c) 어떤 문장을 추가/수정하면
  해결되는지 구체적 대체 문장까지 제시하라. 추상적 조언은 금지한다.

[16축 점검표 — 각 샷마다 빠짐없이 확인하고 표로 보고하라]
1 피사체 정체성 / 2 의상 전체(가방 착용 위치 포함) / 3 소품과 손의 결합
4 자세와 시선 / 5 동작의 진행(3~4박자) / 6 카메라(무브·속도·진폭·높이·거리)
7 프레이밍(샷 사이즈·인물 점유 비율) / 8 공간(인물 뒤/좌/우 각각) / 9 조명(광원 방향·그림자)
10 색 팔레트 / 11 부수 요소의 움직임 / 12 시간축 타임스탬프 / 13 촬영 주체
14 오디오 위계 / 15 대사 화자·언어 / 16 부정 지시 / 19 오버레이 그래픽 / 20 믹스 위계·전환 / 21 캐릭터 성격 4축 / 22 대사의 수신자 / 23 감정의 단계
(연속 세그먼트면 17 경계 연속성 / 18 불변·가변 분리 추가)

[특히 집요하게 볼 것]
- 인물이 무언가를 들고 있다면: 어느 손인가? 반대 손은 무엇을 하는가?
  회전하거나 팔이 몸에 가려지는 구간에서 그 물건은 어떻게 되는가?
- 카메라가 물러나거나 인물이 이동하는데, 근접 연기를 요구하고 있지는 않은가?
- 컷이 바뀌는데 의상·소품·조명·배경을 다시 명시했는가?
- 셀피/POV라면 촬영 장비가 화면에 보이도록 서술하고 있지는 않은가?
- 폰 액정·모니터·간판·명찰처럼 작은 화면이나 작은 글자를 보여주도록 서술하고 있지는 않은가? (기본은 안 보이게 돌리는 것이다)
- 대사가 있는 샷의 프레이밍이 가슴 위 이상인가? 무릎 위·전신에서 말하게 시키고 있지는 않은가?
- 동작이 정적으로 서술되어 5초 이상 유지될 수 없지는 않은가?
- 각 샷의 동작 문장에 배경·프레이밍·의상 설명이 섞여 동사가 묻히고 있지는 않은가? 동작 문장 100자당 동사가 2개 이상인가? (0.5 아래면 무시된다)
- 카메라 무브가 여러 샷에서 동일하게 반복되고 있지는 않은가?
- 소리 묘사가 크기만 있고 위계가 없지는 않은가?
- 캐릭터에 고유한 성격이 있다면 표정·자세·대사 어투·목소리 네 축이 모두 같은 방향을 가리키는가? 하나라도 비면 기본 미소로 수렴한다
- 각 대사의 수신자가 지정돼 있는가? 화면 밖 대상에게 하는 말인데 렌즈를 보고 말하도록 서술하고 있지는 않은가?
- 감정 변화가 필요한 컷에서 감정 이름만 적고 눈썹·입·어깨의 움직임을 안 적지는 않았는가? 그 컷의 프레이밍이 가슴 위 이상인가?

[출력 형식]
1) 축별 점검표: 샷 × 16축, 각 칸에 ✅명시 / ⚠️모호 / ❌미지정
2) blocking 결함 목록: 이대로 생성하면 반드시 문제가 되는 것. 각각 대체 문장 포함
3) non-blocking 개선 제안
4) 수정된 프롬프트 전문

blocking이 하나도 없다고 판단되면 그 근거를 축별로 명시하라.
단, 안이하게 통과시키지 마라 — 실제로 네 번의 생성이 이 검토 없이 실패했다.
```

**검토자가 "괜찮다"만 말하면 검토가 실패한 것이다.** 축별 표를 요구하는 이유가 이것이다.

## 4-I. ⭐ 손에 든 소품은 "손을 지정"해야 붙는다 (2026-08-11)

인물이 뭔가를 들고 있는 장면에서 **소품이 좌우 손을 오가고 회전 중에 사라진다.**
30초 브이로그 실측에서 스마트폰이 5초 안에 세 번 손을 바꾸고 8.5초에 완전히 사라졌다.

| 시각 | 폰 위치 |
|---|---|
| 0.5s | 오른손(낮게) |
| 2.0s | 오른손(높게) |
| 5.0s | **왼손** ← 교체 |
| 7.0s | 오른손 |
| **8.5s** | **없음** ← 소실 |
| 10.5s | **왼손** |

### 원인 1 — 손을 지정하지 않았다

프롬프트가 `holding her phone out at arm's length`였다. **어느 손인지 말한 적이 없다.**
모델은 매 프레임 자유롭게 고른다. 인물 정체성과 달리 **소품-손 결합은 자동으로
유지되지 않는다.**

### 원인 2 — 셀피는 논리적 모순을 안고 있다 ⚠️

`filming herself on a smartphone`이라고 써 놓고 **화면에는 폰을 든 그녀를 보여줬다.**
셀피 시점이면 **폰이 곧 카메라**이므로 화면에 보일 수 없다. 모델이 두 조건을 동시에
만족시키려다 폰이 불안정해진다.

**촬영 주체를 먼저 정하라.**

- **(A) 3인칭 관찰 카메라 + 폰은 소품** → 폰이 보여도 된다. 반드시 손을 지정하라
- **(B) 폰 = 카메라(진짜 셀피 POV)** → **폰을 화면에 등장시키지 마라.** 팔이 뻗어
  있는 각도와 살짝 흔들리는 핸드헬드로만 암시한다

브이로그를 만들 때 (A)와 (B)를 섞어 쓰지 마라. 하나를 고르고 전 샷에 일관되게 적용한다.

### 처방 — 결합·유지·역할 3종 세트

**① `prompt_prefix`에 소품-손 결합을 박는다** (전 샷에 자동 적용)
```
S1 holds the smartphone in her right hand at all times. It never changes hands
and never leaves her right hand. Her left hand is free.
```

**② 샷마다 다시 명시한다** — 컷이 바뀌면 의상과 마찬가지로 소품도 재해석된다
```
[Shot 2] ... still holding the smartphone in her right hand, ...
```

**③ 나머지 손에 일거리를 준다** — 비워두면 모델이 그 손에 소품을 옮겨 놓는다
```
she waves with her free left hand
her free left hand rests on the strap of her sling bag
```

**④ 회전·가림 구간을 명시적으로 넘긴다** — 소실이 일어나는 지점이다
```
she keeps her right arm extended with the phone throughout the turn,
the phone staying in frame the whole time
```

**⑤ 양손이 필요한 동작 뒤에는 소품 위치를 다시 말한다**
```
she claps once, then takes the phone back into her right hand
```

**교훈**: 정체성(얼굴·의상)은 레퍼런스와 `prompt_prefix`로 잘 유지되지만,
**소품과 손의 결합은 별개의 축이고 훨씬 약하다.** 소품이 등장하는 순간부터
그것도 "이름으로 지목해야 할 대상" 목록에 넣어라.

## 4-E. ⭐ 멀티샷 연출 — 컷은 프레임 단위로 지켜진다

**하나의 15초 클립 안에 3컷 서사를 넣을 수 있다.** 실측 2건에서 지시한 타임스탬프가
그대로 지켜졌다.

| 지시 | 실제 검출 | 프레임 간 차이 |
|---|---|---|
| 5.2초 hard cut | 5.08 / 4.92초 | 70.0 / 75.4 (주변 평균 4.8~7.5) |
| 10.6초 hard cut | 10.33 / 10.29초 | 64.1 / 69.0 |

컷 판정은 눈이 아니라 **프레임 간 평균 절대차**로 하라. 주변 대비 10배 이상 튀는 지점이
실제 컷이다.

### 카메라 무브 크기는 "샷의 목적"으로 정한다

같은 `large amplitude`가 한 번은 실패, 한 번은 성공했다. 크기 자체가 문제가 아니었다.

| 샷 목적 | 무브 | 결과 |
|---|---|---|
| 근접 연기 (렌즈에 손가락질) | `Push Out at fast speed with large amplitude` | ❌ **인물이 멀어져 연기가 통째로 소실** |
| 근접 연기 (동일 장면 재시도) | `Static Shot` + 거리 고정 문구 | ✅ 손가락질·손등으로 밀치기까지 전부 살아남 |
| 풍경 리빌 (바다 공개) | `Pan Right at slow speed with large amplitude` | ✅ 항구 전경이 제대로 드러남 |

**거리 고정 문구를 반드시 같이 써라**: `stays close to the camera`,
`fills the frame`, `at arm's length from the lens`, `never walks away from it`.
인물은 카메라가 가만히 있어도 **스스로 멀어진다.**

### 컷이 바뀌면 의상을 다시 해석한다

첫 문단에서 의상을 아무리 상세히 지목해도, `[Shot 2]`에서 청록 보타이가 대형 리본으로,
흰 셔츠+멜빵이 조끼풍으로 바뀌었다.

→ **해결: 샷마다 의상 태그를 반복 명시하라.** `[Shot 2] ... the same blonde twintailed
girl, still in the white shirt with black suspenders, the teal bowtie and the navy
pleated skirt, ...` 이렇게 넣자 3컷 내내 유지됐다. (잔여 문제: 소매 길이가 일부
프레임에서 흔들린다)

### 15초의 앞 3초는 뻣뻣하다

프레임 간 움직임 실측: 0~3초 0.58 → 12~15초 2.60 (**4.5배**). 특히 i2v는 1번 프레임이
레퍼런스에 못 박혀 있어 모션이 붙기까지 워밍업이 필요하다.

앞뒤를 여유로 잡고 잘라 쓰는 기법이 유효하나, **H3에서는 362(15.08초)가 훈련 상한**이라
19초를 뽑을 수 없다. 362 안에서 앞을 버리고 **11초를 쓰는 방식**이 정답이다(추가 비용 0).
동작을 3~4박자로 이어 쓰면 뻣뻣함 자체가 크게 줄어든다.

## 4-F. ⭐ 프롬프트 이해도의 한계선 (실측 3판)

832×480 L124 세 판으로 10개 축을 채점했다. **한계선은 "수량과 개체 추적"에 그어져 있고,
나머지는 대부분 뚫린다.**

| 축 | 결과 |
|---|---|
| **칠판 텍스트 렌더링** | ✅ `HELLO` 5글자를 판서체로 정확히. 분필로 하트를 그리게 시키면 **그리고 나서 지워지지 않고 유지**된다 |
| 좌우 소품 배치 | ✅ "오른쪽에 빨간 사과 / 왼쪽에 초록 물뿌리개", 끝까지 미접촉 지시까지 준수 |
| 부정 지시 | ✅ "등을 카메라에 보이지 않음" 5초 내내 유지 |
| 타임스탬프 동작 지시 | ✅ 1.5초 낙하 지시 → 실제 1.6~1.8초 |
| 4단계 인과 순서 | ✅ 걷기→낙하→응시→줍기→기립 전부 순서대로 |
| **오디오-비주얼 싱크** | ✅ 충격음 2회가 낙하 시점에 검출 |
| **다중 인물 속성 결합** | ✅ 좌=검은단발+빨간리본+우산 / 우=은발땋기+멜론빵. 교차 오염 0 |
| 위치 교환 추적 | ✅ 두 인물이 실제로 지나쳐 좌우가 바뀜 |
| 반응 억제 지시 | ✅ "한쪽은 반응 없이 계속 먹는다" 준수 |
| **정확한 수량** | ❌ "종이비행기 정확히 세 대" → 연속 스트림으로 무한 유입 |
| **개체별 역할 부여** | ❌ "두 번째 것만 잡아라" → 개체 식별 자체가 안 됨 |

**운용**: 개수가 중요하면 프롬프트로 통제하지 말고 첫 프레임(i2v)으로 고정하거나
후처리로 해결하라. 반대로 텍스트·좌우 배치·다중 인물·타임스탬프·오디오 싱크는
적극적으로 활용해도 된다.

## 4-G. `MiniMaxH3ReferenceToVideo` — 영상을 레퍼런스로 넣는 경로 (미검증)

`MiniMaxH3ImageToVideo` 말고 **레퍼런스 전용 노드가 따로 있다.**

```
MiniMaxH3ReferenceToVideo
  required: clip, vae, audio_vae, prompt, width, height, length, ref_image_size
  optional: ref_images(최대 9) / ref_videos(최대 3) / ref_video_audios(3) / ref_audios(9)
```

- **`ref_videos`는 24fps 2~15초 IMAGE 시퀀스를 받는다.** 정지 이미지가 아니라 영상을
  레퍼런스로 넣어 정체성·모션 스타일을 전이시킬 수 있다
- `ref_image_size`: `match`(생성 픽셀 면적에 맞춰 축소) / `max`(2048 short edge, 정체성
  최상). **레퍼런스 토큰이 매 샘플링 스텝을 통과하므로 `max`는 수 배 느려진다**
- `audio_vae`가 required로 올라와 있어 ImageToVideo와 배선이 다르다
- 대응 가중치로 보이는 `minimax_h3_ref2va_pruned_w4a8_mixed`(11.77GB)가
  `Kijai/MiniMax-H3-experimental`에 있다
- **미검증**: 체이닝 이음새(측정치 4.51) 감소에 쓸 수 있는지

## 5. 15초를 넘길 때 — 체이닝

> ## ⭐ 먼저 읽어라 — 이 절은 2026-08-10에 대체되었다
>
> **15초 초과는 `h3-longtake` 스킬을 따르라.** ConText-Loop 커스텀 노드 팩이
> 이전 세그먼트의 **compact AV latent를 다음 세그먼트 conditioning에 직접 주입**해
> 이음새를 구조적으로 없앤다. 실측: 이음새 프레임차 **4.51 → 1.89**(국소 평균 이하).
>
> 아래 K 레시피·ColorMatch 계열 서술은 **그 팩이 없던 시절의 우회책**이다.
> 팩을 못 쓰는 상황에서만 참고하라. 아래의 "오디오 이음새 앵커 수단이 현재 없다"는
> 서술도 무효다 — `MiniMaxH3LoopTrim`의 `match_tail`이 처리한다.

(이하 구 레시피 — 참고용)

15초 초과가 필요하면 `long-video-chaining` 스킬의 **K 레시피(교정-확정 2패스)**를 따르되,
H3 고유 사항 두 가지를 반영하라.

**유리한 점**: `MiniMaxH3ImageToVideo`에 `first_frame`/`last_frame`이 **둘 다 옵셔널
입력으로 존재**한다. K 레시피가 노드 개조 없이 그대로 성립한다.

```
1) 탐색 패스   A → (자유 생성, last_frame 없음) → 마지막 프레임 B
2) 교정        B → ColorMatch(고정 앵커, method=mkl, strength=1.0) → B'
3) 확정 패스   A → B' (first_frame=A, last_frame=B')   ← 이 클립을 채택
4) 확정 클립의 실제 마지막 프레임이 다음 구간의 A
```

### 실측 — 5초 ×3 체이닝 vs 15초 단발 (2026-08-07, 832×480 / 20step / 시드 고정)

| | 단발 L362 | 체이닝 124×3 |
|---|---|---|
| 출력 | 15.08초 | 15.49초 |
| **소요** | **738초** | **451초** (142+157+152) |
| 배수 | 1× | **0.61× — 체이닝이 39% 빠르다** |

체이닝 쪽이 39% 싸 보인다. **그러나 이 451초는 쓸 수 없는 결과물의 값이다** —
오디오가 죽었고 이음새가 튄다(아래 참조). 고치는 비용까지 넣으면 결론이 뒤집힌다.

| | 단발 L362 | 체이닝(실사용 가능하게 보정) |
|---|---|---|
| 생성 | 738초 | 451초 |
| K 레시피 2패스 (이음새) | 불필요 | **×2.1 → 약 950초** |
| MMAudio 후처리 (오디오) | 불필요 | **+α** |
| 이음새 | 없음 | 남음(0이 되지 않음) |
| **합계** | **738초** | **950초+** |

### ⭐ 결론 — 15초 이하는 무조건 단발이다

체이닝은 **15초를 넘길 때만** 쓴다. 그 이하에서 쪼개는 것은 시간도 더 들고 품질도
나쁘다. "체이닝이 더 빠르다"는 중간 관측은 **보정 비용을 빼먹은 값**이었다.

**ColorMatch 앵커는 H3에 불필요했다.** 앵커 없이 진행형 프롬프트만으로 3세그먼트를
이었을 때 휘도가 단조 드리프트하지 않았다.

| | seg1 | seg2 | seg3 |
|---|---|---|---|
| 첫 프레임 YAVG | 58.76 | 63.70 | 61.23 |
| 끝 프레임 YAVG | 67.17 | 64.11 | 65.32 |

58~67 사이에서 진동할 뿐 한 방향으로 밀리지 않는다. WAN에서 필수였던 ColorMatch를
**H3에서는 먼저 붙이지 마라.** 붙이면 정당한 조명 변화까지 눌린다.
(단, 어두워지는 프롬프트를 넣은 경우는 미검증 — `long-video-chaining` 함정 4 참조)

### ⚠ 그러나 순진한 체이닝은 실패한다 — 실측 2건

**(1) 오디오가 죽는다. 원인은 두 축이고 둘 다 독립적으로 작용한다.**

전 클립 `mean_volume` 실측:

| length | 모드 | mean_volume |
|---|---|---|
| 73 (3초) | t2v | -22.6 / -20.4 dB |
| **124 (5초)** | **t2v** | **-16.6 / -17.0 dB ← 가장 좋음** |
| 124 | **i2v** (`first_frame`) | **-45.6 / -49.7 dB — 사실상 무음** |
| **362 (15초)** | t2v | **-29.5 / -49.4 dB — 열화, 편차 큼** |

- **i2v 조건화가 오디오를 죽인다.** `first_frame`을 주면 30dB 내려간다.
- **길이가 길어져도 죽는다.** t2v인데도 362에서는 -29.5 ~ -49.4로 무너지고 시드별
  편차가 크다. 처음에 "i2v 탓"으로만 결론지었다가, t2v 15초에서도 같은 현상이 나와
  정정했다.

**⚠ 위 표만 보고 "길이가 오디오를 죽인다"고 결론짓지 마라 — 프롬프트가 교란 변수다.**
길이별 비교에 쓴 15초 프롬프트가 전부 조용한 소리(숨소리·빗소리·실크) 묘사였다.
소리 묘사를 강하게 바꿔 재측정한 결과:

| 길이 | 소리 프롬프트 | LUFS |
|---|---|---|
| 5초 | 조용 (숨소리·빗소리) | **-14.2** |
| 5초 | 큼 (경적·사이렌·착암기) | -20.8 |
| 15초 | 큼 (수증기·컵·그라인더·잡담) | **-29.0** |
| 15초 | 조용 (숨소리·실크·빗소리) | -47.5 |

**같은 15초에서 프롬프트만 바꿔 18.5 LUFS가 올라왔다.** 즉 두 요인이 독립적으로 작용한다.

- **프롬프트의 소리 묘사 강도가 1차 변수다.** 소리를 구체적이고 크게 주문하면 그만큼 나온다
- **길이는 그 위에 얹히는 페널티다.** 5초 묶음 -14~-21 vs 15초 묶음 -29~-47.
  프롬프트를 아무리 세게 써도 15초는 5초 수준에 못 미친다
- **-29 LUFS는 실사용 가능하다** (청취 확인됨). 15초에서도 소리 묘사만 충실히 쓰면
  후처리 없이 쓸 만하다
- 미해결: 5초에서 큰 소리 프롬프트가 오히려 mean이 낮았다(-14.2 → -20.8). 간헐적
  소리(사이렌·경적)라 평균이 내려간 것으로 추정 — max_volume은 오히려 높았다(-9.4).
  표본 5개라 단정 불가

### ⭐ 해결책 — `NormalizeAudioLoudness`를 그래프에 박아라

레벨이 요청마다 -14 ~ -47 LUFS로 튀는 문제는 **워크플로우 안에서 끝난다.**
ComfyUI 내장 `NormalizeAudioLoudness` 노드를 `VAEDecodeAudio`와 `CreateVideo` 사이에
끼우면 매 생성이 목표 LUFS로 고정되어 나온다.

```json
"25": { "class_type": "NormalizeAudioLoudness",
        "inputs": { "audio": ["23", 0], "lufs": -16 } },
"91": { "class_type": "CreateVideo",
        "inputs": { "images": ["10", 0], "audio": ["25", 0], "fps": 24, "bit_depth": 8 } }
```

- 노드 입력은 `audio`(AUDIO) + `lufs`(FLOAT, 기본 -23)뿐이다. **-16**이 실용 기본값
- 실측: 같은 애니메 프롬프트가 정규화 전 -45.3 → 정규화 후 **-16.0 LUFS** 정확히 착지
- `minimax-h3-video` 워크플로우 패키지에는 이미 반영되어 있다

**이미 뽑아둔 mp4를 고칠 때** — 비디오는 무손실 복사, 오디오만 재인코딩:

```bash
ffmpeg -y -i in.mp4 -c:v copy \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" -c:a aac -b:a 192k out.mp4
```

실측 결과: -47.5 → -15.7 / -29.0 → -16.1 / -45.3 → -14.8 LUFS.
**-47 LUFS짜리도 정상 레벨로 살아난다** — 신호 자체는 있고 게인만 낮았다는 뜻이다.
즉 "오디오가 죽는다"는 표현은 부정확했고, **레벨이 불안정한 것**이 정확하다.

→ **실무**: 오디오가 중요하면 prompt 꼬리의 소리 묘사를 **한 덩어리로 구체적으로** 써라.
`"Loud room tone: overlapping chatter, the hiss of a steam wand, cups clattering,
the grinder whirring"` 처럼. 그래도 부족하면 `video-sound-design` 스킬의 MMAudio로
완성본에 덧입힌다.

**단, i2v(`first_frame` 지정)에서 -45~-49dB로 죽는 것은 프롬프트로 회복되지 않았다.**
체이닝 시 세그먼트 오디오는 여전히 버려야 한다.

**(2) 이음새는 눈으로 볼 때 튄다. 정지 프레임 비교로는 못 잡는다.**

연속 프레임 간 평균 절대차(0~255 스케일) 실측:

| 구간 | 값 |
|---|---|
| seg1 내부 연속 프레임 | 0.70 ~ 0.91 |
| seg2 내부 연속 프레임 | 0.92 ~ 1.73 |
| **★ 이음새 (seg1끝 → seg2첫)** | **4.51 — 정상의 약 5배** |

**정지 프레임을 나란히 놓으면 이음새가 멀쩡해 보인다.** 구도·조명·포즈가 비슷하기
때문이다. 하지만 움직임의 속도와 방향은 정지컷에 안 담긴다. **이음새 판정은 반드시
프레임 간 차이 수치로 하라.** (이 실수를 실제로 저질렀다 — 스틸 비교로 "이어졌다"고
오판했고, 사용자가 영상을 재생해 보고 잡아냈다.)

**원인 후보 1순위 — 손실 압축된 mp4에서 프레임을 뜯었다.**
`ffmpeg`로 h264 mp4의 마지막 프레임을 PNG로 뽑아 `first_frame`에 넣으면, 이미 crf
인코딩으로 열화된 이미지를 조건으로 쓰게 된다. → **ComfyUI 워크플로우 안에서
`VAEDecode` 직후에 `SaveImage`로 마지막 프레임을 무손실 PNG로 저장**하고 그것을
넘겨라. 미검증이나 가장 유력하다.

원인 후보 2순위 — `first_frame`만으로는 부족. `long-video-chaining`의 K 레시피
(탐색→ColorMatch 교정→`first_frame`+`last_frame` 확정 2패스)를 적용한다.

**⚠ 신규 실패 축 — 오디오 이음새.** WAN 체이닝에는 없던 문제다. 세그먼트마다 오디오를
독립 생성하므로 이어붙이면 앰비언스 레벨과 톤이 튄다. 비디오의 ColorMatch에 해당하는
오디오 앵커 수단이 **현재 없다.**

대응 후보(전부 미검증):
1. 세그먼트 오디오는 버리고 **전체 길이 오디오를 별도로 한 번** 생성해 덮어쓰기 ← 유력
2. 이음새에 0.2~0.3초 크로스페이드
3. 세그먼트별 RMS 정규화

## 6. 라이선스

오픈웨이트 라이선스가 **미국·EU·영국·한국을 로컬 배포 대상에서 제외**한다(2026-08-03).
기술적으로는 구동되지만 사용자가 알고 판단해야 할 사항이므로, 이 모델을 처음 제안할
때 반드시 명시하라. 호스팅 API는 전 지역 개방(초당 $0.13).

## 7. 함정

### 함정 1 — 공식 UI 템플릿은 API 변환이 안 된다

`video_minimax_h3_t2v.json` 등 동봉 템플릿은 노드 하나가 **subgraph(UUID 타입)**로
묶여 있다. `/prompt`에 그대로 POST할 수 없고, `definitions.subgraphs[0]`의 15개 노드를
API 포맷으로 직접 펼쳐야 한다.

→ 그 작업은 이미 끝나 있다. `minimax-h3-video` 워크플로우 패키지와
`scripts/h3-run.js`를 쓰면 된다.

```
node h3-run.js [seed] [prompt] [width] [height] [length]
```

### 함정 2 — ComfyUI를 백그라운드 태스크로 띄우면 로그가 죽는다

에이전트가 ComfyUI를 백그라운드 셸로 spawn하고 stdout을 파일로 리다이렉트한 경우,
그 태스크가 stopped 처리되면 **파이프가 끊겨 로그 파일이 더 이상 갱신되지 않는다.**
ComfyUI 본체는 멀쩡히 계속 돈다.

증상: 진행바도 `Prompt executed`도 안 찍히는데 GPU는 99%. **행(hang)으로 오독하기 쉽다.**

→ 진행 판정은 로그가 아니라 아래로 하라.
```
curl -s http://127.0.0.1:8188/prompt      → exec_info.queue_remaining
ls -lt <comfyui>/output/video/            → 출력 파일 mtime
```

### 함정 3 — 프로세스 실행파일 경로는 그 프로세스의 환경이 아니다

Windows venv의 `Scripts\python.exe`는 `venvlauncher.exe`이며 **base 인터프리터를
자식으로 띄운다.** 자식의 커맨드라인은 시스템 파이썬 경로로 보이지만 `sys.prefix`와
site-packages는 venv 것이다. 부모가 수 MB짜리로 남는 것도 정상이다.

시스템 파이썬을 직접 실행해 `import torch` 해 본 결과를 "구동 환경의 torch"라고
단정하면 틀린다. 구동 환경 판정은 **반드시** 아래 둘 중 하나로 하라.

```
curl -s http://127.0.0.1:8188/system_stats
ComfyUI 콘솔의 "** Python executable:" 줄
```

### 함정 4 — 훈련 범위 아래 length로 기준선을 잡지 마라

`length=73`은 17k+5 그리드에 맞으므로 에러 없이 통과한다. 하지만 훈련 범위(124~362)
아래이므로 품질 판정의 기준선으로는 부적절하다. 정식 벤치마크는 **124 이상**에서 잡아라.
