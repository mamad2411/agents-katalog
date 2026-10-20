---
name: axios-refresh-queue-zustand
description: Axios response interceptor that intercepts 401, queues concurrent failed requests, refreshes the token once, and replays queued requests with the new token. Prevents thundering-herd refresh calls.
category: frontend
tags:
  - axios
  - jwt
  - refresh-token
  - interceptor
  - zustand
  - auth
triggers:
  - axios 401 refresh
  - token refresh queue
  - isRefreshing flag
  - axios interceptor zustand
  - refresh thundering herd
  - retry original request
source_project: veda-chronicles
version: 0.1.0-draft
---
