---
name: speechbrain
description: "SpeechBrain — PyTorch speech toolkit. ASR, speaker recognition, speech separation, diarization, enhancement, language identification, and TTS. Recipe-based training with pre-trained model zoo."
tags: [speech-recognition, speaker-diarization, speaker-verification, speech-embeddings, speechbrain]
---
## Overview

SpeechBrain is an open-source PyTorch speech processing toolkit covering ASR (speech-to-text), speaker recognition, speech separation, diarization, enhancement, language identification, emotion recognition, and text-to-speech. Provides pretrained models and recipe-based training.

## Installation

```bash
uv pip install speechbrain
```

## Speech Recognition

```python
from speechbrain.inference.ASR import EncoderDecoderASR

asr_model = EncoderDecoderASR.from_hparams(
    source="speechbrain/asr-crdnn-rnnlm-librispeech",
    savedir="pretrained_models/asr")
transcript = asr_model.transcribe_file("audio.wav")
print(f"Transcript: {transcript}")
```

## Speaker Verification

```python
from speechbrain.inference.speaker import SpeakerRecognition

verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec")
score, prediction = verification.verify_files("speaker1.wav", "speaker2.wav")
print(f"Same speaker: {prediction} (score: {score:.3f})")
```

## References
- [SpeechBrain docs](https://speechbrain.github.io/)
- [SpeechBrain GitHub](https://github.com/speechbrain/speechbrain)