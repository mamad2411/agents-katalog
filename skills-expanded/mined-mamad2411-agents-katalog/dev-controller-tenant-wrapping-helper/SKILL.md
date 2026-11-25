---
tags: [backend, dev, controller, tenant, wrapping, helper]
name: dev-controller-tenant-wrapping-helper
description: Dev/로컬 전용 컨트롤러의 테넌트+JWT 반복 래핑을 함수형 인터페이스 + 헬퍼 컴포넌트로 추출
type: skill
category: backend
version: 1.0.0
source_project: lucida-domain-automation
source_ref: b0cf1adb
trigger: @Profile("local") Dev 컨트롤러마다 TenantContextHolder.set + JWT 생성 + try-finally가 반복될 때
archived: true
archived_reason: "metadata-empty: no tags, no triggers, description < 60 chars"
archived_at: 2026-04-17
---

See `content.md`.
