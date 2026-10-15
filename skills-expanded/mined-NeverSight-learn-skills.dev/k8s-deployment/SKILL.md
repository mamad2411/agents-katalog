---
name: k8s-deployment
description: Deploy services to Kubernetes with Docker multi-stage builds, kustomize overlays, and Makefile automation. Use when creating Dockerfiles, writing k8s manifests, or setting up deployment pipelines.
---

# Kubernetes Deployment

Deploy services using Docker multi-stage builds, kustomize overlays, and Makefile-driven automation.

## Directory Layout

```
.
├── Dockerfile
├── Makefile
├── server/
│   └── k8s/
│       └── prod/
│           ├── server.yaml
│           ├── ingress.yaml
│           └── kustomization.yaml
└── worker/
    └── k8s/
        └── prod/
            ├── worker.yaml
            └── kustomization.yaml
```

## Makefile

```Makefile
SHELL := /bin/bash

define setup_env
        $(eval ENV_FILE := $(1))
        $(eval include $(1))
        $(eval export)
endef

build-push-cli: ## Build and push Docker image with git hash tag
	$(call setup_env, .env.server.prod)
	$(eval GIT_HASH := $(shell git rev-parse --short HEAD))
	$(eval DYNAMIC_TAG := your-registry/your-app:$(GIT_HASH))
	docker build -f Dockerfile -t $(DYNAMIC_TAG) .
	docker push $(DYNAMIC_TAG)

deploy-server: ## Deploy server to Kubernetes (prod)
	$(call setup_env, .env.server.prod)
	@$(MAKE) build-push-cli
	$(eval GIT_HASH := $(shell git rev-parse --short HEAD))
	kustomize build --load-restrictor=LoadRestrictionsNone server/k8s/prod | \
	sed -e "s;{{DOCKER_REPO}};your-registry/your-app;g" \
		-e "s;{{GIT_COMMIT_SHA}};$(GIT_HASH);g" | \
		kubectl apply -f -

deploy-worker: ## Deploy worker to Kubernetes (prod)
	$(call setup_env, .env.worker.prod)
	@$(MAKE) build-push-cli
	$(eval GIT_HASH := $(shell git rev-parse --short HEAD))
	kustomize build --load-restrictor=LoadRestrictionsNone worker/k8s/prod | \
	sed -e "s;{{DOCKER_REPO}};your-registry/your-app;g" \
		-e "s;{{GIT_COMMIT_SHA}};$(GIT_HASH);g" | \
		kubectl apply -f -
```

## Dockerfile (Go)

```Dockerfile
# ---- Builder Stage ----
FROM golang:1.24-alpine AS builder

RUN apk update && apk add --no-cache git build-base ca-certificates
RUN update-ca-certificates

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY cmd/ ./cmd/
COPY server/ ./server/
COPY worker/ ./worker/

RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /bin/app cmd/app/*.go

# ---- Final Stage ----
FROM alpine:latest

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
WORKDIR /app
COPY --from=builder /bin/app /app

EXPOSE 8080
CMD ["/app", "run", "http-server"]
```

## Dockerfile (Python)

```Dockerfile
FROM python:3.13-slim AS base

RUN pip install uv
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ ./src/
COPY server/ ./server/

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Key Patterns

- **Git hash tags**: Tag images with `git rev-parse --short HEAD` for traceability
- **kustomize overlays**: Use `kustomize build` with sed substitution for env-specific deploys
- **Multi-stage builds**: Separate builder and runtime stages for minimal images
- **Layer caching**: Copy dependency files first, then source code
- **Frontend on Vercel**: Deploy frontend via Vercel; only backend goes to k8s
