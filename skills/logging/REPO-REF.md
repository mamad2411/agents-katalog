# Repo Referensi: codewithmukesh/dotnet-claude-kit

Repo: https://github.com/codewithmukesh/dotnet-claude-kit
Ref lokal: /Users/chaali0324/.agents/repo-refs/codewithmukesh_dotnet-claude-kit
API: curl "localhost:27126/repos/readme?name=codewithmukesh_dotnet-claude-kit"
Dibuat: 2026-09-16

## Cuplikan README
# codewithmukesh/dotnet-claude-kit

Source: https://github.com/codewithmukesh/dotnet-claude-kit
Fetched: 2026-09-16

## README
<p align="center">
  <h1 align="center">dotnet-claude-kit</h1>
  <p align="center">
    <strong>Make Claude Code an expert .NET developer.</strong>
    <br />
    47 skills &bull; 10 specialist agents &bull; 16 slash commands &bull; 10 rules &bull; 5 project templates &bull; 22 MCP tools &bull; automation hooks
    <br />
    Built for .NET 10 / C# 14. Architecture-aware. Token-efficient.
  </p>
</p>

<p align="center">
  <a href="https://codewithmukesh.com/blog/dotnet-claude-kit-guide/">
    <img src="https://img.shields.io/badge/%F0%9F%93%96%20Read%20the%20Complete%20Guide-codewithmukesh.com-512BD4?style=for-the-badge&logoColor=white" alt="Read the complete dotnet-claude-kit guide" />
  </a>
</p>

<p align="center">
  <a href="https://codewithmukesh.com/blog/dotnet-claude-kit-guide/"><strong>📖 Full Guide</strong></a> &bull;
  <a href="#installation">Installation</a> &bull;
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#what-makes-this-10x">10x Features</a> &bull;
  <a href="#slash-commands-14">Commands</a> &bull;
  <a href="#knowledge-skills-31">Skills</a> &bull;
  <a href="#agents-10">Agents</a> &bull;
  <a href="#rules-10">Rules</a> &bull;
  <a href="#templates-5">Templates</a> &bull;
  <a href="#roslyn-mcp-server">MCP Server</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

---

> ### 📖 New here? Start with the guide
>
> **[How I Use dotnet-claude-kit: Making Claude Code Write Senior-Level .NET →](https://codewithmukesh.com/blog/dotnet-claude-kit-guide/)**
>
> The complete walkthrough: install and update the plugin, what happens in your first session, the everyday feature workflow, how the Roslyn MCP server cuts token usage, which commands keep a codebase healthy, plus FAQ and troubleshooting.
>
> *This README is the reference. The guide is how to actually use it.*

## The Problem

Claude Code is powerful, but out of the box it doesn't know **your** .NET conventions. It generates `DateTime.Now` instead of `TimeProvider`. It wraps EF Core in repository abstractions. It picks an architecture without asking about your domain. It reads entire source files when a Roslyn query would cost 10x fewer tokens.

**dotnet-claude-kit fixes all of that.**

## What This Is

A curated knowledge and action layer that sits between Claude Code and your .NET project. Drop a single `CLAUDE.md` into your repo and Claude instan
