# LLM Deployment Template

## Overview

A template for deploying LLM applications to production environments. This covers containerization, health checks, scaling strategies, monitoring integration, and deployment patterns (blue-green, canary, rolling) specific to LLM services. The template works for both API-based deployments (using cloud LLM providers) and self-hosted model serving.

## Key Concepts

- **Containerization** — Docker-based packaging with multi-stage builds for minimal image size
- **Health checks** — Startup, liveness, and readiness probes for orchestration platforms
- **Scaling** — Horizontal scaling based on request rate, latency, and queue depth
- **Deployment strategies** — Blue-green for zero-downtime, canary for gradual rollout
- **Environment management** — Separate configs for dev, staging, and production
- **Secrets management** — Secure handling of API keys and credentials

## Implementation Patterns

### Dockerfile

```dockerfile
FROM python:3.12-slim AS base
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

FROM base AS production
COPY src/ ./src/
COPY prompts/ ./prompts/
COPY configs/ ./configs/
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Kubernetes Deployment

```python
from dataclasses import dataclass

@dataclass
class K8sDeployment:
    name: str
    image: str
    replicas: int = 3
    cpu_request: str = "500m"
    cpu_limit: str = "2000m"
    memory_request: str = "1Gi"
    memory_limit: str = "4Gi"
    env_vars: dict = None

    def to_yaml(self) -> str:
        env_section = ""
        if self.env_vars:
            env_section = "\n".join(
                f'            - name: {k}\n              value: "{v}"'
                for k, v in self.env_vars.items()
            )

        return f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {self.name}
spec:
  replicas: {self.replicas}
  selector:
    matchLabels:
      app: {self.name}
  template:
    metadata:
      labels:
        app: {self.name}
    spec:
      containers:
        - name: {self.name}
          image: {self.image}
          ports:
            - containerPort: 8000
          resources:
            requests:
              cpu: {self.cpu_request}
              memory: {self.memory_request}
            limits:
              cpu: {self.cpu_limit}
              memory: {self.memory_limit}
          env:
{env_section}
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5"""

def generate_deployment(name: str, env: str = "production") -> str:
    """Generate deployment YAML for an environment."""
    config = {
        "development": K8sDeployment(name=name, image=f"{name}:dev", replicas=1),
        "staging": K8sDeployment(name=name, image=f"{name}:staging", replicas=2),
        "production": K8sDeployment(name=name, image=f"{name}:latest", replicas=3),
    }
    return config[env].to_yaml()
```

### Deployment Script

```python
import subprocess
import sys

def deploy(environment: str, image_tag: str, strategy: str = "rolling"):
    """Deploy LLM service to specified environment."""
    print(f"Deploying to {environment} with strategy: {strategy}")

    # Build and push image
    subprocess.run(["docker", "build", "-t", f"llm-app:{image_tag}", "."], check=True)
    subprocess.run(["docker", "push", f"llm-app:{image_tag}"], check=True)

    if strategy == "blue-green":
        # Deploy to green slot
        subprocess.run(["kubectl", "apply", "-f", f"k8s/{environment}-green.yaml"], check=True)
        # Wait for green to be ready
        subprocess.run(["kubectl", "rollout", "status", "deployment/llm-app-green"], check=True)
        # Switch traffic
        subprocess.run(["kubectl", "apply", "-f", f"k8s/{environment}-service.yaml"], check=True)
        # Scale down blue
        subprocess.run(["kubectl", "scale", "deployment/llm-app-blue", "--replicas=0"], check=True)
    else:
        # Rolling update
        subprocess.run(["kubectl", "set", "image", "deployment/llm-app",
                        f"llm-app=llm-app:{image_tag}"], check=True)
        subprocess.run(["kubectl", "rollout", "status", "deployment/llm-app"], check=True)

    print(f"Deployment to {environment} complete")

if __name__ == "__main__":
    deploy(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "rolling")
```

## Best Practices

1. **Use multi-stage Docker builds** — Separate build dependencies from runtime for smaller images
2. **Implement all three health probes** — Startup, liveness, and readiness for proper orchestration
3. **Use blue-green for zero downtime** — Deploy new version alongside old, switch traffic atomically
4. **Canary new models** — Route 5-10% of traffic to new models before full rollout
5. **Externalize all configuration** — Use environment variables and config maps, not baked-in values

## Common Pitfalls

- **No health checks** — Orchestrators can't detect unhealthy containers without probes
- **Hardcoded secrets in images** — API keys must come from secrets management, not Dockerfiles
- **No rollback plan** — Always keep the previous deployment ready for instant rollback
- **Ignoring resource limits** — LLM services need adequate CPU/memory; set proper requests and limits

## References

- Docker Best Practices: docs.docker.com/develop/develop-images/dockerfile_best-practices
- Kubernetes Deployment: kubernetes.io/docs/concepts/workloads/controllers/deployment
