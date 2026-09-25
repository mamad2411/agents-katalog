# Repo Referensi: lukasniessen/kubernetes-skill

Repo: https://github.com/lukasniessen/kubernetes-skill
Ref lokal: /Users/chaali0324/.agents/repo-refs/lukasniessen_kubernetes-skill
API: curl "localhost:27126/repos/readme?name=lukasniessen_kubernetes-skill"
Dibuat: 2026-09-16

## Cuplikan README
# lukasniessen/kubernetes-skill

Source: https://github.com/lukasniessen/kubernetes-skill
Fetched: 2026-09-16

## README
# Kubernetes Skill for Claude Code and Codex: KubeShark

<div align="center" name="top">
  <img align="center" src="assets/logo.png" width="180" height="180" alt="KubeShark Logo">

<!-- spacer -->
<p></p>

[![Claude Skill](https://img.shields.io/badge/Claude-Skill-6272F5)](https://docs.claude.ai/docs/agent-skills)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-10A37F)](https://developers.openai.com/codex/skills/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/LukasNiessen/kubernetes-skill.svg)](https://github.com/LukasNiessen/kubernetes-skill)

</div>

The #1 Kubernetes skill for Claude Code and Codex, measured by GitHub stars.

### Fixes Hallucinations.

LLMs hallucinate a lot when it comes to Kubernetes. They omit security contexts, generate deprecated APIs, use wildcard RBAC, forget resource limits, and produce probes that cause cascading failures. This skill fixes it. It includes best practices for Kubernetes -- good, bad, and neutral examples so the AI avoids common mistakes. Using KubeShark, the AI keeps proven practices in mind, eliminates hallucinations, and defaults to secure, reliable, production-ready manifests.

KubeShark is built as the production-grade Kubernetes skill for Claude Code and Codex: broader than resource-template skills, safer than generic Kubernetes prompts, and tuned for hallucination prevention instead of raw tutorial volume.

### Very Token-Efficient.

Most Kubernetes skills dump huge walls of text onto the agent and burn expensive tokens -- with no upside. LLMs don't need the entire Kubernetes docs again. KubeShark was aggressively de-duplicated and optimized for maximum quality per token.

### Based on Official Best Practices.

KubeShark is primarily based on the [official Kubernetes documentation](https://kubernetes.io/docs/), the [NSA/CISA Kubernetes Hardening Guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF), [OWASP Kubernetes Top 10](https://owasp.org/www-project-kubernetes-top-ten/), [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/), and the [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes). When guidance conflicts, it prioritizes official Kube
