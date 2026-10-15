---
name: whisperkit
description: "Apple Silicon에서 오디오·영상 파일을 WhisperKit용 오디오로 정규화한 뒤 음성-텍스트 변환과 화자 분리를 수행한다. 사용자가 미디어를 받아쓰기하거나, 녹취록·자막을 만들거나, 화자를 구분하거나, 회의 녹음을 요약하기 전에 전사본이 필요하거나, inbox에 미디어 파일을 넣었을 때 사용한다. '트랜스크립션 해줘', '이 영상에서 음성 추출해줘', '텍스트로 변환해줘', '화자 분리해줘', 'inbox에 파일 넣었어' 등의 요청에 트리거된다. 회의 내용의 요약·결정 사항·액션 아이템 작성은 meeting-summary 스킬에 맡긴다."
---

# WhisperKit STT + 화자 분리

WhisperKit CLI 기반 음성-텍스트 변환 스킬이다. 입력 미디어를 FFmpeg로 표준 WAV로 정규화하고 Apple Silicon Neural Engine에서 온디바이스로 전사한다. 이 스킬의 책임은 `transcript.txt` 생성까지이며 회의 요약은 작성하지 않는다.

## 실행 요구사항

- Apple Silicon 및 macOS 14+
- `whisperkit-cli`, `ffmpeg`, `ffprobe`

환경 판정은 `setup/scripts/check-env.sh`만 사용한다. 이 스킬에서 `which`, `uname`, 버전 검사 등을 따로 반복하지 않는다.

```bash
bash setup/scripts/check-env.sh --json
```

- `platform_ok=false` 또는 `has_fail=true`면 `setup` 스킬의 결과별 조치를 먼저 수행한다.
- `warn`은 `detail`에 따라 처리하되 STT를 자동으로 중단하지 않는다.
- 환경을 변경했다면 스크립트를 다시 실행하고 통과 결과를 확인한다.

## 책임 경계

- 입력: FFmpeg가 디코딩할 수 있고 오디오 스트림이 있는 미디어 파일
- 출력: 화자와 타임스탬프가 포함된 `transcript.txt`
- 하지 않는 일: 회의 요약, 결정 사항, 액션 아이템 작성
- 회의록까지 요청받은 경우: 이 스킬을 완료한 뒤 `meeting-summary` 스킬에 `transcript.txt`를 전달

## 플로우 요약

```text
저장 루트 선택 → inbox/ → 미디어 검사 → 날짜 추출 → rec_{날짜}_{번호}/ 생성 → 원본 이동
→ 16 kHz mono PCM WAV 정규화 → whisperkit-cli 실행 → 화자 파싱 → transcript.txt
```

## 출력 구조

```text
recordings/                         # 권장 루트; 플랫 선택 시 생략
├── inbox/
└── rec_2026-03-30_001/
    ├── audio.mov                   # 원본 미디어, 원래 확장자 유지
    ├── transcript.txt              # 화자 분리된 최종 전사본
    └── data/
        ├── audio.wav               # STT용 16 kHz mono PCM 정규화 파일
        ├── raw.txt                 # whisperkit-cli stdout 전체 캡처
        ├── audio.json              # 워드 단위 타임스탬프, 신뢰도 점수
        └── audio.srt               # SRT 자막 파일
```

`meeting-summary`를 이어서 실행하면 같은 폴더에 `summary.md`가 추가된다.

## 에이전트 실행 가이드

### Step 1: 저장 루트 선택 및 inbox 확인

사용자가 출력 루트를 명시했다면 그대로 사용한다. 명시하지 않았다면 기존 구조를 먼저 감지한다.

1. `recordings/inbox/` 또는 `recordings/rec_*` 흔적만 있으면 `recordings`를 루트로 사용한다.
2. 현재 폴더에 `inbox/` 또는 `rec_*` 흔적만 있으면 기존 플랫 구조를 유지하고 `.`을 루트로 사용한다.
3. 두 구조가 모두 있으면 어느 쪽을 사용할지 사용자에게 확인한다.
4. 어느 구조도 없으면 최초 한 번만 현재 폴더에 플랫하게 저장할지, `recordings/` 아래에 모을지 묻는다. `recordings/`를 권장값으로 제시한다.

첫 결과 폴더가 생성된 뒤에는 위 감지 규칙으로 선택이 유지되므로 매번 다시 묻지 않는다. 선택한 값을 이후 모든 경로의 기준으로 사용한다.

```bash
WK_ROOT="recordings"  # 플랫 구조는 ".", 사용자 지정 경로도 가능
WK_INBOX="${WK_ROOT}/inbox"
mkdir -p "$WK_INBOX"
ls "$WK_INBOX"
```

inbox가 비어 있으면 사용자에게 파일을 넣어달라고 안내한다. 사용자가 파일 경로를 직접 지정했다면 inbox로 옮기지 않고 해당 파일을 입력으로 사용할 수 있지만, 결과는 선택한 루트에 저장한다.

### Step 2: 미디어와 오디오 스트림 검사

```bash
# 아래 둘 중 입력 방식에 맞는 경로 하나만 선택한다.
WK_SOURCE="${WK_INBOX}/파일명"  # inbox 파일
# WK_SOURCE="/사용자가/직접/지정한/파일.mov"
WK_AUDIO_TRACK=0                # 0부터 시작하는 오디오 트랙 순번

ffprobe -v error -show_entries format=format_name,duration \
  -show_entries stream=index,codec_type,codec_name,channels,sample_rate \
  -of json "$WK_SOURCE"
```

- 오디오 스트림이 없으면 중단하고 사용자에게 알린다.
- 오디오 스트림이 하나면 그대로 사용한다.
- 여러 오디오 스트림이 있으면 기본적으로 첫 번째를 사용하되, 언어·해설 등 트랙 선택이 결과에 영향을 줄 수 있으면 사용자에게 선택을 요청하고 `WK_AUDIO_TRACK`에 0부터 시작하는 순번을 설정한다.
- DRM 보호, 손상 파일, FFmpeg 미지원 코덱은 우회하지 말고 변환 불가 사유를 알린다.

### Step 3: 녹음 날짜 추출

```bash
ffprobe -v quiet -show_entries format_tags=creation_time -of csv=p=0 "$WK_SOURCE"
```

`creation_time`이 없으면 다음 순서로 처리한다.

1. 파일 수정일(`stat -f "%Sm" -t "%Y-%m-%d"`) 사용
2. 수정일도 신뢰할 수 없으면 오늘 날짜 사용
3. 추정한 날짜를 사용자에게 알린다

### Step 4: 폴더 생성 및 원본 이동

- 날짜는 `YYYY-MM-DD` 형식을 사용한다.
- 선택한 루트 안에서 같은 날짜 폴더가 있으면 `_001`, `_002` 순으로 사용되지 않은 번호를 선택한다.
- 원본 확장자를 유지해 `audio.<원본확장자>`로 이동한다.
- 확장자가 없으면 `audio.source`를 사용한다.

```bash
WK_RECORD_DIR="${WK_ROOT}/rec_2026-03-30_001"
mkdir -p "${WK_RECORD_DIR}/data"
mv "$WK_SOURCE" "${WK_RECORD_DIR}/audio.mov"
```

이동 전에 사용자에게 확인한다. 원본을 삭제하거나 덮어쓰지 않는다.

### Step 5: WhisperKit용 오디오 정규화

스킬에 포함된 `scripts/prepare-media.sh`를 사용한다.

```bash
bash scripts/prepare-media.sh \
  "${WK_RECORD_DIR}/audio.mov" \
  "${WK_RECORD_DIR}/data/audio.wav" \
  "$WK_AUDIO_TRACK"
```

정규화 규격:

| 항목 | 값 | 이유 |
|------|----|------|
| 컨테이너 | WAV | Apple 플랫폼에서 안정적으로 디코딩 가능 |
| 코덱 | PCM signed 16-bit little-endian | 무손실·비압축 표준 입력 |
| 샘플레이트 | 16 kHz | Whisper 입력 샘플레이트에 맞춤 |
| 채널 | mono | 음성 인식 입력을 일관되게 유지 |
| 영상 | 제거 | STT에 불필요한 데이터 제외 |

정규화는 손실된 음질을 복구하는 작업이 아니다. 다양한 입력을 동일하고 예측 가능한 STT 입력으로 만드는 단계다. 원본 미디어는 그대로 보존한다.

### Step 6: 트랜스크립션 + 화자 분리

```bash
whisperkit-cli transcribe \
  --audio-path "${WK_RECORD_DIR}/data/audio.wav" \
  --model large-v3 \
  --language ko \
  --diarization \
  --report \
  --report-path "${WK_RECORD_DIR}/data/" \
  2>&1 | tee "${WK_RECORD_DIR}/data/raw.txt"
```

stdout을 반드시 캡처한다. 화자 분리 결과는 JSON/SRT가 아니라 stdout의 `SPEAKER` 라인에서 파싱한다.

| 파라미터 | 설명 | 비고 |
|----------|------|------|
| `--model` | Whisper 모델 | `large-v3` 권장 |
| `--language` | 언어 코드 | `ko`, `en`, `ja`, `zh` 등 |
| `--diarization` | 화자 분리 활성화 | 없으면 화자 구분 불가 |
| `--report` | JSON/SRT 리포트 생성 | |
| `--report-path` | 리포트 저장 경로 | 디렉토리를 미리 생성해야 함 |

- 한국어가 기본이며 다른 언어면 `--language`를 변경한다.
- 언어를 모르면 자동 감지를 사용한다.
- 다국어 혼용 음성은 주요 언어 하나를 지정하는 편이 일반적으로 안정적이다.
- 45분 오디오는 Apple Silicon에서 모델 캐시 후 약 12분이 걸릴 수 있다.
- 첫 실행 시 `large-v3` 모델 약 1.5GB를 다운로드할 수 있다.

### Step 7: transcript.txt 생성

`scripts/parse-speakers.sh`를 사용한다.

```bash
bash scripts/parse-speakers.sh \
  "${WK_RECORD_DIR}/data/raw.txt" \
  > "${WK_RECORD_DIR}/transcript.txt"
```

출력 형식:

```text
[화자 A] (00:00:03)
첫 번째 발화 내용

[화자 B] (00:00:11)
두 번째 발화 내용
```

- 시작 시간을 `HH:MM:SS`로 표시한다.
- 화자가 바뀔 때만 새 라벨을 출력한다.
- 화자 라벨은 원본의 `A`, `B`, `C` 등을 그대로 유지한다.

## 실패 대응

| 상황 | 원인 | 대응 |
|------|------|------|
| `whisperkit-cli: command not found` | 미설치 | `setup` 스킬 실행 |
| `ffmpeg` 또는 `ffprobe` 없음 | 미설치 | `setup` 스킬 실행 |
| 오디오 스트림 없음 | 무음 영상 또는 잘못된 입력 | 전사하지 않고 사용자에게 알림 |
| 변환 실패 | 손상, DRM, 미지원 코덱 | FFmpeg 오류를 보존하고 원본을 확인 |
| 여러 오디오 트랙 | 언어·해설 트랙 혼재 | 필요한 트랙을 확인한 뒤 선택 |
| `Error: Could not load model` | 모델 미다운로드 | 네트워크 확인 후 재실행 |
| stdout에 `SPEAKER` 라인 없음 | 화자 1명 또는 diarization 실패 | 플래그 확인 후 단일 화자 처리 여부 판단 |
| 한국어인데 영어로 인식 | 언어 미지정 | `--language ko` 명시 |
| `--report-path` 에러 | 디렉토리 미존재 | `mkdir -p` 먼저 실행 |

## 하면 안 되는 것

- 원본 미디어를 정규화 파일로 덮어쓰지 않는다.
- 오디오 스트림을 확인하지 않고 FFmpeg나 WhisperKit을 실행하지 않는다.
- `grep -P`를 사용하지 않는다. macOS 기본 grep은 PCRE를 지원하지 않는다.
- JSON/SRT에서 화자 정보를 추출하지 않는다.
- stdout 캡처 없이 화자 분리를 실행하지 않는다.
- `--report-path`에 파일 경로를 지정하지 않는다.
- 사용자의 확인 없이 inbox 원본을 이동하거나 삭제하지 않는다.
- 기존 저장 구조가 있는데 다른 루트를 임의로 선택하거나 혼합하지 않는다.
