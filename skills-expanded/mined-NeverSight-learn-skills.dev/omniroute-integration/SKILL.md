---
name: omniroute-integration
description: Configure OpenCode to work with OmniRoute AI gateway service
author: OpenCode Community
version: 1.0.0
---

# OmniRoute Integration Skill

Configures OpenCode to work with the OmniRoute AI gateway service, enabling access to multiple AI models from various providers including Qwen, Codex, GitHub and Kiro.

## When to use

Use this skill when you want to:
- Connect OpenCode to the OmniRoute AI gateway
- Access multiple AI models through a single interface
- Configure all available OmniRoute models in OpenCode
- Switch between different AI providers easily

## Prerequisites

- OpenCode version 1.2.0 or higher
- Valid OmniRoute API key
- Network access to OmniRoute service at http://138.2.29.190:20128

## Instructions

1. Obtain your OmniRoute API key
2. Run the skill to initiate configuration
3. Enter your API key when prompted
4. Confirm the OmniRoute service endpoint (default: http://138.2.29.190:20128)
5. Allow the script to configure OpenCode settings
6. Verify configuration by testing a model

## Configuration Details

The skill will:
- Create/update ~/.config/opencode/opencode.json with OmniRoute provider
- Add all available models (Qwen, Codex, GitHub, Kiro) to the configuration
- Update authentication credentials in ~/.local/share/opencode/auth.json
- Set up default model omniroute/qw/qwen3-coder-plus

## Available Models

After successful configuration, you can use models such as:
- omniroute/kr/claude-sonnet-4.5
- omniroute/kr/claude-haiku-4.5
- omniroute/qw/qwen3-coder-plus
- omniroute/qw/qwen3-coder-flash
- omniroute/cx/gpt-5.2-codex
- omniroute/gh/gpt-4o
- And over 100 other models available through OmniRoute

## Verification

The skill will automatically test the configuration with a simple API call to verify the connection works properly.
