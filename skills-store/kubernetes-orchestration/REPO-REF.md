# Repo Referensi: manutej/luxor-claude-marketplace

Repo: https://github.com/manutej/luxor-claude-marketplace
Ref lokal: /Users/chaali0324/.agents/repo-refs/manutej_luxor-claude-marketplace
API: curl "localhost:27126/repos/readme?name=manutej_luxor-claude-marketplace"
Dibuat: 2026-09-16

## Cuplikan README
# manutej/luxor-claude-marketplace

Source: https://github.com/manutej/luxor-claude-marketplace
Fetched: 2026-09-16

## README
# LUXOR Claude Code Marketplace

> Professional Claude Code plugins covering the complete software development lifecycle

[![Plugins](https://img.shields.io/badge/plugins-10-blue)](https://github.com/luxor/luxor-claude-marketplace)
[![Skills](https://img.shields.io/badge/skills-67-green)](https://github.com/luxor/luxor-claude-marketplace)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

## 🌩️ LUXOR: Cheat Codes for Claude Code

> **"Don't just chat with code. Equip it."**

We've all been there. You ask Claude to scaffold a backend, and it gives you a generic Express server from 2021. You ask for a "modern" frontend, and it hallucinates a library that doesn't exist anymore.

**Claude is a genius, but it's a generalist.** It lacks the *domain-specific context*—the "muscle memory"—of a Senior Engineer who has spent 10 years in the trenches.

**We built this LUXOR plugin to fix that.**

Think of this repository as a curated collection of "Cheat Codes" (Plugins, Skills, Agents) that force Claude to adhere to **production-grade standards** across every part of the stack.

When you install these plugins, you aren't just adding tools. You are unlocking **God Mode** for specific domains.

---


## 🚀 Quick Start

### Install Entire Marketplace

```bash
# Clone marketplace
git clone https://github.com/luxor/luxor-claude-marketplace.git
cd luxor-claude-marketplace

# Install all plugins (one-liner)
for plugin in plugins/*/; do (cd "$plugin" && ./install.sh); done
```

### Install Individual Plugin

```bash
# Install just frontend skills
cd luxor-claude-marketplace/plugins/luxor-frontend-essentials
./install.sh

# Restart Claude Code
```

### Install Featured Bundle

```bash
# Install top 4 featured plugins
cd luxor-claude-marketplace/plugins
for plugin in luxor-frontend-essentials luxor-backend-toolkit luxor-devops-suite luxor-skill-builder; do
    (cd "$plugin" && ./install.sh)
done
```

---
## 🎮 Choose Your Skill Tree

I've organized the marketplace into specialized "cartridges" you can load into Claude. Install them all to become a full-stack army, or pick the specific cheat codes you need right now.

### 🎨 The Frontend Master

*Unlock the ability to ship pixel-perfect UIs without fighting the CSS.*

> **The Problem:** Claude struggles with consistent design systems and modern frameworks.
> **The Cheat Code:** `luxor-
