---
name: h3-longtake
description: MiniMax H3로 15초를 넘는 롱테이크 영상을 만들 때 사용한다. ConText-Loop 커스텀 노드 팩(MiniMaxH3Chain* 13종)으로 이전 세그먼트의 compact AV latent를 다음 세그먼트 conditioning에 주입해 모션·오디오·정체성을 이어붙인다. 레퍼런스 스틸 준비, plan.json 포맷, prompt_prefix와 <Picture N> 마커 문법, 체크포인트 재개, 이음새 측정 프로토콜을 다룬다. "롱테이크", "긴 영상", "1분 영상", "체이닝", "이음새", "ConText-Loop", "H3 Chain", "레퍼런스 준비", "정체성 유지" 키워드에 트리거된다.
---

# MiniMax H3 롱테이크

## 한 줄 요약

**H3의 15.08초 상한은 ConText-Loop으로 깨진다.** 이전 세그먼트의 compact AV latent를
다음 세그먼트의 conditioning에 직접 주입하므로, 정지 프레임을 다시 인코딩해 넘기던
방식의 이음새 문제가 **구조적으로 사라진다.**

모델 자체의 성질(length 그리드, 해상도별 소요, 4단 필드 프롬프트, `<d>` 대사 태그)은
`minimax-h3` 스킬을 먼저 읽어라. 이 문서는 **여러 세그먼트를 잇는 부분만** 다룬다.

## 1. 실측 — 이 팩이 실제로 무엇을 고쳤나

832×480 / 5초 × 2세그먼트 / 20스텝 / Turbo 없음 / generated_audio / 총 306초

| | 순진한 체이닝 (mp4 마지막 프레임 → first_frame) | **ConText-Loop** |
|---|---|---|
| 이음새 프레임차 | **4.51** (내부 0.70~1.73 → 5배 스파이크) | **1.89** (내부 평균 2.86~5.39) |
| 육안 판정 | 움직임 속도·방향이 튄다 | **이음새를 못 찾는다** |
| 오디오 | i2v에서 -45~-49dB로 죽음 | 연속 (레벨 정상) |
| 색 드리프트 | 발생 | latent 슬라이스로 우회 |

**이음새 값이 오히려 국소 평균보다 낮다.** 최대 스파이크는 세그먼트 내부의 회전 동작
구간에서 나왔고, 그건 정상 모션이다.

출력 길이는 5초 × 2 = 10초가 아니라 **9.417초**다. `context_length`(기본 22프레임)만큼
겹침이 제거되기 때문. 총 길이를 계산할 때 반영하라.

> ⚠️ **이음새 이상 판정은 반드시 전체 분포와 비교하라.** 이음새 근처만 확대해 보고
> "오디오가 30배 튄다"고 오판한 적이 있다. 전 구간을 재보니 RMS 300 이상 구간이 18곳
> 흩어져 있었고 이음새 값은 오히려 작은 축이었다 — 그냥 발소리였다.

## 2. 설치

```
cd <ComfyUI>/custom_nodes
git clone https://github.com/ethanfel/ComfyUI-MiniMaxH3-Contex-Loop.git
```

- **requirements.txt 없음** — 추가 파이썬 의존성 0
- ffmpeg가 PATH에 있으면 리뷰·조립에 사용, 없으면 PyAV 폴백
- `ethanfel/ComfyUI-H3-Motion-Context`는 **같은 저장소의 다른 이름**이다(커밋 해시 동일).
  둘 다 깔면 노드가 중복 등록되므로 **하나만** 설치하라
- 설치 후 노드 수가 13개 늘어난다(1961 → 1975 실측)

> ⚠️ **`patch_layout.py`가 ComfyUI 내부를 몽키패치한다.** 스톡은 키프레임 앵커를
> first/last만 허용하는데 그 제약을 풀어낸다. **ComfyUI 버전을 올릴 때마다 이 패치가
> 살아 있는지 확인하라.**

## 3. 노드 구성

| 노드 | 역할 |
|---|---|
| `MiniMaxH3ChainPlan` | plan.json 편집 → `H3_CHAIN_PLAN` |
| `MiniMaxH3ChainLoopStart` | 루프 진입. `plan`, `start_clip`, 옵션 `scene_range`/`source_audio`/`external_context` |
| `MiniMaxH3ChainCurrent` | 현재 씬 상태. width/height/length/seed/steps를 출력해 다른 노드에 공급 |
| **`MiniMaxH3ChainContext`** | **핵심.** `state`+`conditioning`+`vae`+`latent`(+`audio_vae`) → 컨텍스트가 주입된 CONDITIONING, trim_frames, is_first |
| `MiniMaxH3LoopTrim` | 디코드 후 겹침 제거. `match_tail=true` 유지할 것 |
| `MiniMaxH3ChainSegmentSave` | 세그먼트 mp4 + safetensors 체크포인트 저장 |
| `MiniMaxH3ChainLoopEnd` | 루프 종료 → `H3_CHAIN_MANIFEST` |
| `MiniMaxH3ChainAssemble` | 최종 조립. `audio_source`: plan/source/generated/none |
| `MiniMaxH3ChainReview` | mp4 미리보기 + 승인/재시도 게이트 |
| `MiniMaxH3ChainExternalVideo` | 기존 영상을 이어 확장할 때의 어댑터 |
| `MiniMaxH3ChainManifestLoad` / `ChainExportPNG` / `ChainScenePromptEditor` | 재개 / 무손실 PNG 추출 / 대형 프롬프트 편집기 |

**배선의 요점**: `ChainContext`의 `conditioning`은 **스톡 H3 노드
(`MiniMaxH3ReferenceToVideo` 또는 `MiniMaxH3ImageToVideo`)의 출력**을 받고, `latent`는
같은 노드의 두 번째 출력(빈 AV latent)을 받는다. 기존 워크플로우를 버리는 게 아니라
**그 뒤에 끼워 넣는** 구조다. 씬 1은 컨텍스트 없이 통과하고, 2번째부터 주입이 시작된다.

`generated_audio` / `source_plus_timeline` 모드에서는 **`audio_vae`를 반드시 연결**하라.
`source_track` 모드에서는 첫 소스 윈도우에 이미 tail이 들어 있어 불필요하다.

## 4. ⭐ 정체성은 3중으로 유지된다

**"처음 넣은 레퍼런스 몇 장으로 끝까지 버틴다"가 아니다.**

| 층 | 무엇 | 주기 |
|---|---|---|
| ① 레퍼런스 이미지 | `ref_images`가 Ref2VA에 물려 있음 | **매 세그먼트 재공급** |
| ② `prompt_prefix` | 정체성·의상·스타일·연속성 규칙 | **모든 씬 프롬프트 앞에 자동 삽입** |
| ③ compact AV latent | 이전 세그먼트의 모션·조명·기하 | 직전 세그먼트 |

루프가 돌 때마다 레퍼런스가 다시 들어가므로 **드리프트가 누적되는 구조가 아니다.**
100번째 세그먼트도 1번째와 같은 그림을 본다.

**따라서 레퍼런스 스틸의 품질이 전 구간을 좌우한다.** 여기에 시간을 써라.

## 5. 레퍼런스 스틸 준비

### 5-1. 캐릭터 LoRA로 뽑을 때

- **의상을 바꾸려면 기존 의상 태그를 전부 빼라.** 캐릭터 LoRA는 학습된 의상 태그와
  충돌하면 학습된 쪽이 이긴다. 교복 캐릭터에 사복을 입히려면 교복 태그를 지우고
  새 의상만 넣는다
- 반대로 **시그니처 의상을 원하면 정확한 태그 세트를 통째로** 부르거나 의상 칸을
  아예 비워라(학습 데이터 쪽으로 강하게 바이어스된다)
- 스타일 LoRA와 병용할 때는 **캐릭터 LoRA를 항상 위 강도로** 둔다

### 5-2. 구도 — 실패하는 조합이 있다

`arm outstretched toward viewer` + `upper body`를 같이 주면 다리가 붕 뜨고 신발이
두 켤레 나오는 식으로 무너졌다. **`standing, cowboy shot`처럼 전신 기준 구도 태그를
명시**하면 안정된다. 첫 판이 이상하면 시드만 바꾸지 말고 **구도 태그를 의심하라.**

### 5-3. 해상도 — 업스케일해서 넣지 마라

첫 프레임은 **생성 해상도로 직접 크롭**해서 만든다. 832×480짜리를 1152×640으로
업스케일해 넣으면 **1번 프레임부터 흐릿하게 시작**한다. 원본 스틸(예: 1216×832)에서
목표 종횡비로 crop → 목표 해상도로 lanczos 리스케일이 정답이다.

```bash
# 1216x832 원본 → 1152x640(16:9)용 크롭
ffmpeg -i still.png -vf "crop=1216:695:0:25,scale=1152:640:flags=lanczos" ref.png
```

### 5-4. 소품이 있으면 레퍼런스에서부터 손을 정해라

레퍼런스 스틸에서 인물이 뭔가를 들고 있다면 **어느 손에 들렸는지 확인하고, 그 손을
`prompt_prefix`에 못 박아라.** 레퍼런스와 프롬프트가 다른 손을 가리키면 소품이 매
프레임 좌우를 오간다. 상세는 `minimax-h3` 스킬 4-I절.

### 5-5. ComfyUI에 올리기

파일을 input 디렉토리에 직접 복사하려 하지 말고 **업로드 API를 써라.** 출력 디렉토리가
설치 경로 밖에 있는 경우가 흔해서 경로 추측이 빗나간다.

```bash
curl -F "image=@ref.png;filename=ref.png" -F "overwrite=true" \
     http://127.0.0.1:8188/upload/image
```

## 5-6. ⭐ 생성 전 필수 — 장면 명세 프로토콜

체인은 리테이크가 특히 비싸다(30초 2시간 14분 실측). **`minimax-h3` 스킬 4-J절의
16축 체크리스트와 서브에이전트 검토를 반드시 거친 뒤에 큐에 올려라.** 연속
세그먼트에는 17(경계 연속성)·18(불변·가변 분리) 두 축이 추가된다.

- `prompt_prefix`에 **불변 축**(정체성·의상·소품-손 결합·화풍·촬영 주체)을 전부 넣는다
- 씬 `prompt`에는 **변화분만** — 단 의상·소품은 컷마다 재해석되므로 짧게라도 재명시한다
- 세그먼트 2 이후의 첫 문장은 **이전 세그먼트 마지막 동작의 연장**으로 시작한다.
  `[Shot 1]`로 새 장소를 서술하면 씬 점프가 된다(실측: 이음새 프레임차 69.3)

## 6. plan.json 포맷

```json
{
  "prompt_prefix": [
    "Use <Picture 1> for her facial identity, hairstyle, skin tone, age, body proportions, and distinctive physical features.",
    "",
    "<Subject 1> (S1) wears the same white long-sleeved shirt, teal bowtie, black suspenders and navy pleated skirt in every scene.",
    "",
    "2D-animated Japanese anime, hand-inked line art, flat cel-shading. Continue subject motion, camera momentum, lighting and geometry across every boundary. No cuts."
  ],
  "defaults": { "duration_seconds": 5, "steps": 20 },
  "shots": [
    { "id": "seg_01", "prompt": ["장면별 변화분만 적는다."] },
    { "id": "seg_02", "prompt": ["같은 속도로 계속 걷다가 서서히 멈춘다."] }
  ]
}
```

- **`prompt_prefix`(별칭 `global_prompt`)가 모든 씬 프롬프트 앞에 자동으로 붙는다.**
  정체성·의상·스타일·연속성 규칙은 전부 여기. 씬 `prompt`에는 **변화분만** 적어라
- 프롬프트는 **문자열 배열**로 쓰면 실제 개행으로 join된다. 빈 문자열이 빈 줄
- `<Picture N>`으로 레퍼런스 이미지를, `<Subject N>`/`(S1)`로 인물을 지목한다.
  대사는 `minimax-h3` 스킬의 `<d>[Korean] ...</d>` 태그를 그대로 쓴다
- `prompt_prefix`가 비어 있지 않으면 씬 `prompt`는 생략 가능하다

### ChainPlan 노드 설정값

| 필드 | 기본 | 메모 |
|---|---|---|
| `context_length` | 22 | 겹침 프레임 수. 출력 길이가 이만큼 줄어든다 |
| `encode_mode` | `video` | |
| `anchor_mode` | `head` | |
| `crop` | `disabled` | 레퍼런스와 출력 프레이밍이 같으면 disabled |
| `audio_mode` | `source_track` / `generated_audio` / `source_plus_timeline` | |
| `generation_fingerprint` | — | **모델·VAE·LoRA·레퍼런스·CFG·샘플러 버전을 넣어라.** 바뀌면 체크포인트 재사용이 무효화된다 |

## 7. 산출물 구조와 재개

```
output/h3_chains/{run_name}/
  plan.json  manifest.json  api_prompt.json
  segments/    clip_0001.<hash>.mp4  + .prompt.txt
  checkpoints/ clip_0001.<hash>.safetensors  + .json
  final/       {filename}.mp4
```

**체크포인트가 safetensors로 남으므로 중단 후 재개가 된다.** 긴 체인을 돌리다 끊겨도
처음부터 다시 하지 않는다. 재개할 때는 **같은 Plan·소스 영상·어댑터를 다시 연결**하라.

씬 범위는 연속이어야 한다. `1,3,5:8` 같은 불연속 선택은 **거부된다** — 건너뛴 씬이
모션 의존성을 끊기 때문이다.

## 8. ⭐ 이 도구를 쓸 자리와 쓰지 말 자리

**쓸 자리**: 같은 공간에서 카메라와 인물이 계속 움직이는 **롱테이크**. 모션·조명·기하가
경계를 넘어 이어져야 하는 경우.

**쓰지 말 자리**: **씬이 점프하는 편집.** 장소가 바뀌거나 시간이 건너뛰는 컷은
클립을 따로 뽑아 붙이는 편이 싸고 자유롭다. 이 팩은 애초에 연속성을 전제로 설계돼
있어서 불연속을 요구하면 거부하거나 품질이 나빠진다.

**15초 이하**: 체이닝 자체가 불필요하다. `minimax-h3`의 단발(L362)이 정답이다.

## 9. 워크플로우 변환 — 예제는 UI 포맷이다

예제 워크플로우 5종이 `example_workflows/`에 들어 있으나 **전부 UI 포맷**이라
`/prompt`에 그대로 POST할 수 없다. 변환기가 필요하다.

> ⚠️ **Reroute 노드를 그냥 건너뛰면 입력이 조용히 누락된다.** Reroute의 입력 타입은
> `*`라서 출력 타입과 매칭되지 않는다. **"링크된 첫 입력을 따라간다"로 처리**하라.
> 이걸 안 해서 `ChainContext`의 `vae` 입력이 통째로 사라진 적이 있다.
> mode 4(bypass)/2(mute) 노드와 미설치 노드도 같은 패스스루 규칙으로 처리한다.

변환 후에는 **모든 링크가 존재하는 노드를 가리키는지 검증**하고 POST하라.

### 예제가 요구하는 자산 (없으면 대응물로 교체)

| 예제 | 대응 |
|---|---|
| `minimax_h3_ref2va_pruned_bf16` | `Kijai/MiniMax-H3-experimental`의 `ref2va_pruned_w4a8_mixed`(11.77GB). fl2va nvfp4와 같은 VRAM 급 |
| `qwen3vl_32b_..._int8_convrot` | `qwen3vl_32b_..._nvfp4_awq` (역할 동일) |
| `lightx2v_turbo_4step` | 보유한 Turbo 4step LoRA로 대체 가능 |
| `PathchSageAttentionKJ` | **`sageattention` 미설치면 이 노드에서 죽는다.** 속도 패치일 뿐이니 빼도 결과는 같다 |
| 소스 wav | `audio_mode`를 `generated_audio`로 바꾸고 `audio_vae` 연결 |

**예제는 Turbo 4스텝 전제로 짜여 있다.** 품질을 볼 목적이면 LoRA를 빼고 steps를
20으로 올려라. 그대로 두면 이음새가 아니라 증류 화질을 보게 된다.

## 10. 측정 프로토콜

1. **프레임 간 평균 절대차**를 전 구간에 대해 구한다(그레이 축소 후 계산)
2. 세그먼트 내부 평균/최대와 **이음새 지점 값을 같은 축에서** 비교한다
3. **국소 확대 금지** — 반드시 전체 분포에서 이음새가 상위 몇 번째인지 본다
4. 오디오도 같은 원칙. 0.1초 RMS를 전 구간 뽑아 이음새가 특별한지 확인한다
5. 마지막에 **재생해서 눈으로 본다.** 정지 프레임 비교로는 속도·방향 불연속이 안 잡힌다
