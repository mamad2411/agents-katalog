---
name: domain-audio-speech
description: "Use for audio and speech tasks: speech recognition (speech to text, ASR, transcription), audio or sound classification and tagging, keyword spotting, speaker identification or verification, sound event detection, and music or audio analysis. Picks the best model per sub-task and the right features, splits, and metrics. Triggers on 'speech to text', 'transcribe', 'ASR', 'audio classification', 'sound', 'keyword spotting', 'speaker recognition', 'voice', 'audio dataset'."
---

# Audio and Speech - Method Selection

Represent audio as a log-mel spectrogram for most classifiers, or feed the raw waveform to self-supervised speech models. Resample to the model's rate (16 kHz is common).

## Decision table
| Sub-task | Recommended | Notes |
|---|---|---|
| Speech recognition (ASR) | Whisper (large-v3, or turbo for speed); wav2vec2 or HuBERT with CTC | Whisper is strong and multilingual zero-shot. Metric is WER, never accuracy. |
| Audio or sound classification and tagging | AST or PaSST (spectrogram transformers, AudioSet-pretrained); PANNs (CNN) | log-mel input. Multi-label tagging uses mAP; single-label uses accuracy or macro F1. |
| Keyword spotting | small CNN or MatchboxNet on log-mel | on-device. Track accuracy and false-alarm rate. |
| Speaker verification or ID | ECAPA-TDNN or x-vector embeddings + cosine similarity | metric-learning. Metrics are EER and minDCF. Split by speaker. |
| Sound event detection | CRNN or PaSST with framewise output | event-based F1, PSDS. |

## Cross-cutting practice
- Augment with SpecAugment, time and pitch shift, and noise or room-impulse mixing. Normalize levels.
- Leakage: split by speaker, recording, or session, not by clip. The same speaker in train and test inflates results.
- Metrics: WER (and CER) for ASR; mAP for multi-label tagging; EER for verification. Do not report plain accuracy for ASR.
- Explainability: saliency or Grad-CAM on the spectrogram for classifiers; attention or confidence and alignment for ASR.
- Improve accuracy: use `accuracy-improvement-loop`. Evaluate with `rigorous-evaluation` using the metric that fits the sub-task.
