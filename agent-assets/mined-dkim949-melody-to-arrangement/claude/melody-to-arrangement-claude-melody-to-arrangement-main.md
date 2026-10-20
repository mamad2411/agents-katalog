# Melody-to-Arrangement Project

## Project Overview
- 멜로디 입력 → AI 편곡 생성 (MusicGen Melody Large 기반)
- 환경: Mac Silicon (MPS) + Vertex AI (CUDA L4 GPU)
- 도메인: 재즈 쿼텟 편곡, 오디오 신호 처리

## Project-Specific Agent Auto-Dispatch Rules
아래 에이전트는 이 프로젝트에서만 활성화. 해당 맥락에서 자동 호출할 것.

- 오디오 찢어짐/clipping 진단, sample rate 변환, normalization 전략, 오디오 포맷(WAV/FLAC/MP3) 최적화, librosa/soundfile 사용 → **audio-engineer**
- MusicGen/음악 생성 모델 파라미터 튜닝, guidance_scale/temperature/top_k 최적화, 음악용 텍스트 프롬프트 엔지니어링, 모델 출력 품질 비교, 새 음악 AI 모델 도입 검토 → **music-ai-specialist**
- 코드 보이싱, 스케일/모드 선택, 편곡 스타일 가이드(재즈/클래식/팝), 생성 결과의 음악적 평가, music21 활용 → **music-theorist**

## Audio Engineer Auto-Trigger Rules
audio-engineer는 아래 상황에서 자동 호출:
- 오디오 파일 생성/변환 코드 작성 시
- "clipping", "distortion", "찢어짐", "노이즈", "sample rate", "normalization" 키워드
- WAV/오디오 품질 이슈 디버깅 시
- float16↔float32 오디오 데이터 변환 시

## Music AI Specialist Auto-Trigger Rules
music-ai-specialist는 아래 상황에서 자동 호출:
- MusicGen 파라미터 변경 또는 생성 품질 논의 시
- 새로운 음악 생성 모델(MusicGen, AudioCraft, Stable Audio 등) 비교/도입 시
- 생성 프롬프트 작성/개선 시

## Music Theorist Auto-Trigger Rules
music-theorist는 아래 상황에서 자동 호출:
- 멜로디/코드 진행 생성 또는 수정 시
- 편곡 스타일 변경 (재즈→클래식 등)
- music21 코드 작성 시
- 생성 결과의 음악적 품질 평가 시

## Project Structure
```
src/
  config.py              — 프리셋, 파라미터 범위, GenerationConfig
  melody_input.py        — 입력 처리 (변환, BPM 감지)
  jazz_melody_generator.py — 재즈 멜로디 자동 생성 (music21)
  jazz_prompts.py        — MusicGen 프롬프트 빌더/변형
  generator.py           — MusicGen Melody 래퍼
  evaluator.py           — 품질 평가 (기본 + jazz 특화)
  auto_tuner.py          — Rule-based 파라미터 자동 조정
  experiment_tracker.py  — JSON 기반 실험 추적
  experiment.py          — 오케스트레이터 (run_experiment, auto_tune)
audio_pipeline.py        — 전처리/후처리/진단 (기존, 독립 모듈)
scripts/
  run_experiment.py      — CLI 진입점
docs/
  design_auto_tuning.md  — 자가개선 루프 설계
  design_jazz_quality.md — 재즈 품질/멜로디 설계
  design_experiment_tracking.md — 실험 추적 설계
```

## Usage
```bash
# 단일 실험
python scripts/run_experiment.py --preset swing

# 자가개선 루프
python scripts/run_experiment.py --preset swing --auto-tune --target-score 75

# 입력 파일 지정 + Large 모델
python scripts/run_experiment.py --preset bebop --input melody.opus --large
```

## Known Issues
- Mac Silicon (MPS) → Vertex AI (CUDA) 전환 시 오디오 찢어짐 발생 가능
  - 추정 원인: float16 정밀도, SoundFont 차이, GPU 커널 수치 차이
  - 관련 에이전트: audio-engineer + mlops-engineer (GPU 호환성)
