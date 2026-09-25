# Repo Referensi: larksuite/cli

Repo: https://github.com/larksuite/cli
Ref lokal: /Users/chaali0324/.agents/repo-refs/larksuite_cli
API: curl "localhost:27126/repos/readme?name=larksuite_cli"
Dibuat: 2026-09-16

## Cuplikan README
# larksuite/cli

Source: https://github.com/larksuite/cli
Fetched: 2026-09-16

## README
# lark-cli

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Go Version](https://img.shields.io/badge/go-%3E%3D1.23-blue.svg)](https://go.dev/)
[![npm version](https://img.shields.io/npm/v/@larksuite/cli.svg)](https://www.npmjs.com/package/@larksuite/cli)

[中文版](./README.zh.md) | [English](./README.md)

The official [Lark/Feishu](https://www.larksuite.com/) CLI tool, maintained by the [larksuite](https://github.com/larksuite) team — built for humans and AI Agents. Covers core business domains including Messenger, Docs, Base, Sheets, Slides, Calendar, Mail, Tasks, Meetings, Markdown, and more, with 200+ commands and 26 AI Agent [Skills](./skills/).

[Install](#installation--quick-start) · [AI Agent Skills](#agent-skills) · [Auth](#authentication) · [Commands](#three-layer-command-system) · [Advanced](#advanced-usage) · [Enterprise](#personal-or-enterprise) · [Security](#security--risk-warnings-read-before-use) · [Contributing](#contributing)

## Why lark-cli?

- **Agent-Native Design** — 24 structured [Skills](./skills/) out of the box, compatible with popular AI tools — Agents can operate Lark with zero extra setup
- **Wide Coverage** — 18 business domains, 200+ curated commands, 26 AI Agent [Skills](./skills/)
- **AI-Friendly & Optimized** — Every command is tested with real Agents, featuring concise parameters, smart defaults, and structured output to maximize Agent call success rates
- **Open Source, Zero Barriers** — MIT license, ready to use, just `npm install`
- **Up and Running in 3 Minutes** — One-click app creation, interactive login, from install to first API call in just 3 steps
- **Secure & Controllable** — Input injection protection, terminal output sanitization, OS-native keychain credential storage
- **Three-Layer Architecture** — Shortcuts (human & AI friendly) → API Commands (platform-synced) → Raw API (full coverage), choose the right granularity

## Personal or Enterprise?

| You are... | Recommended path |
| ---------- | ---------------- |
| **An individual developer** — using lark-cli in your terminal or with your own AI Agent | Follow the [Quick Start](#installation--quick-start) below |
| **Enterprise IT / ISV** — embedding lark-cli into your own Agent or platform, with centralized credentials (database / Vault / config center), unified audit logging, and a restricted command surface |
