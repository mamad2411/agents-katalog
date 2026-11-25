---
tags: [frontend, mfa, federated, component, loader]
name: mfa-federated-component-loader
description: Three-layer dynamic component loading for Webpack 5 Module Federation with retry logic, script caching, and error boundaries
triggers:
  - module federation
  - federated component
  - remote component loading
  - dynamic import remote
  - RemoteApp
category: frontend
version: 1.0.0
source_project: lucida-ui
---

# MFA Federated Component Loader

## Purpose

Implement a robust three-layer dynamic component loading system for Webpack 5 Module Federation. Handles script loading failures gracefully with retry logic, prevents duplicate script injection, and provides type-safe remote consumption.

## When to Use

- Building a micro-frontend architecture with Webpack 5 Module Federation
- Need resilient remote component loading with retry and caching
- Want type-safe consumption of dynamically loaded remote components
- Need to handle network failures when loading remote entries

## Pattern

See `content.md` for full implementation.
