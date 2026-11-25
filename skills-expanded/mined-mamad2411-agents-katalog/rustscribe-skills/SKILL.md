# Qwen3 ASR — Voice Transcription

Transcribe speech from audio files to text.

## Binary

- `{baseDir}/scripts/asr` — Speech-to-text transcription.

## Models

- `{baseDir}/scripts/models/Qwen3-ASR-0.6B` — Speech recognition model (0.6B parameters).

## Transcription

Transcribe an audio file to text.

```shell
{baseDir}/scripts/asr \
  {baseDir}/scripts/models/Qwen3-ASR-0.6B \
  <audio_file>
```

### Parameters

| Parameter  | Required | Description                                        |
|------------|----------|----------------------------------------------------|
| model_path | Yes      | Path to the model directory (0.6B or 1.7B)         |
| audio_file | Yes      | Path to the audio file (any FFmpeg-supported format)|

### Output

Prints the transcribed text to standard output.

### Example

```shell
{baseDir}/scripts/asr \
  {baseDir}/scripts/models/Qwen3-ASR-0.6B \
  recording.wav
```

## Supported Audio Formats

Any format supported by FFmpeg: WAV, MP3, M4A, FLAC, OGG, and more. Audio is automatically resampled to 16 kHz mono internally.

## Workflow

### 1. Identify the Audio File

Get the path to the audio file the user wants to transcribe.

### 2. Run the Command

Run the `asr` binary with the full paths to the binary and model directory.

```shell
{baseDir}/scripts/asr \
  {baseDir}/scripts/models/Qwen3-ASR-0.6B \
  /path/to/audio.wav
```

### 3. Return the Transcription

The transcribed text is printed to stdout. Return it to the user.
