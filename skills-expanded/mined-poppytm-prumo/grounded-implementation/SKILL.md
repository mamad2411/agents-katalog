---
name: grounded-implementation
description: Enforces grounded implementation: inspect before claim, anti-invention, and fail-closed missing authority handling.
---
# Grounded Implementation & Anti-Invention

## 1. Inspect Before Claim
Never claim that a file, directory, symbol, function, interface, command, flag, or test exists without first inspecting the repository with tools.

## 2. Never Invent Requirements or APIs
Absence of information is not authorization to invent APIs, generic "best practices", or conventions. When required information is missing, transition: UNKNOWN -> search authoritative source -> resolve -> explicit assumption OR block dependent slice.

## 3. Strict Scope Adherence
Do not perform opportunistic refactoring outside the Task scope. Materialize IN, OUT, and INCIDENTAL boundaries. Never mutate files listed under OUT.

## 4. Fail Closed on Missing Authority
If an action is destructive, security-sensitive, or mutates public contracts and canonical authority is missing, fail closed immediately.
