---
name: voice-interface-manager
description: Manages the SARAH Voice Interface lifecycle, including setup, audio health checks, volume normalization, and remote control of STT/TTS scripts. Use when debugging audio recording/playback, configuring voice-ui.py, or managing the wake-word listener.
---

# Voice Interface Manager

## Overview
This skill provides a unified workflow for managing the SARAH voice interface stack. It automates health checks, volume normalization, and remote execution of voice commands.

## Core Tasks

### 1. Health & Dependency Check
Before running the voice interface, verify that all CLI tools (ALSA, jq, curl) and Python libraries (tkinter, pyaudio) are correctly configured.
- **Action:** Run `python3 scripts/health_check.py` within the skill directory.
- **Goal:** Ensure `arecord` and `aplay` have access to the hardware and the Gemini API key is present.

### 2. Audio Normalization
If audio is too quiet or clipping, use the normalization utility to reset system levels.
- **Reset to 70%:** `python3 scripts/audio_ctrl.py --normalize`
- **Set Specific Level:** `python3 scripts/audio_ctrl.py --volume 80`

### 3. Remote Triggers
Trigger voice actions directly from the CLI without using the GUI.
- **Start Listening:** `python3 scripts/audio_ctrl.py --trigger listen`
- **Speak Text:** `python3 scripts/audio_ctrl.py --trigger speak --text "Hello, I am SARAH."`

### 4. Troubleshooting
If you encounter "Permission denied" or "Command not found" errors, consult the troubleshooting guide:
- **Reference:** See `references/troubleshooting.md` for fixes related to ALSA, groups, and missing packages.

## Resources

### scripts/
- `health_check.py`: Validates environment, tools, and API keys.
- `audio_ctrl.py`: Handles volume normalization and remote script triggers.

### references/
- `troubleshooting.md`: Detailed solutions for common Linux audio and API issues.

### assets/
- `config_template.json`: Standard configuration for models and directories.