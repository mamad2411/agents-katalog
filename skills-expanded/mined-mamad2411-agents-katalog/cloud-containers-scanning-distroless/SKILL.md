---
name: cloud-containers-scanning-distroless
description: "Cloud Containers Scanning Distroless."
domain: cybersecurity
---

--|
| Shell (bash/sh) | Yes | Yes | No |
| Package manager | apt | apk | No |
| coreutils | Full | BusyBox | No |
| curl/wget | Yes | Yes | No |
| User management | Yes | Yes | No |
| Known CVEs (typical) | 50-200+ | 5-20 | 0-5 |
| Image size (base) | ~77MB | ~7MB | ~2-20MB |

### Security Implications

- **No shell**: Attackers cannot exec into containers to run commands
- **No package manager**: Cannot install additional tools or malware
- **No coreutils**: No `cat`, `ls`, `find`, `curl` for reconnaissance
- **Minimal CVEs**: Fewer packages means fewer vulnerabilities to patch
- **Non-root by default**: `:nonroot` tag runs as UID 65534

## Debugging Distroless Containers

Since distroless has no shell, use these techniques for debugging:

### Debug Image Variant

```dockerfile
# Use debug variant in non-production environments only
FROM gcr.io/distroless/base-debian12:debug
# Includes busybox shell at /busybox/sh
```

```bash
# Exec into debug variant
kubectl exec -it pod-name -- /busybox/sh
```

### Ephemeral Debug Containers (Kubernetes 1.25+)

```bash
# Attach a debug container with full tooling
kubectl debug -it pod-name --image=busybox:1.36 --target=app-container
```

### Crane/Dive for Image Inspection

```bash
# Inspect image layers without running
crane export gcr.io/distroless/static-debian12 - | tar -tf - | head -50

# Analyze image layers
dive gcr.io/distroless/static-debian12
```

## Image Scanning Results

Typical vulnerability comparison using Trivy:

```bash
# Scan Ubuntu-based image
trivy image myapp:ubuntu
# Result: 47 vulnerabilities (3 CRITICAL, 12 HIGH)

# Scan Distroless-based image
trivy image myapp:distroless
# Result: 2 vulnerabilities (0 CRITICAL, 0 HIGH)
```

## References

- [GoogleContainerTools/distroless GitHub](https://github.com/GoogleContainerTools/distroless)
- [Distroless Images - Docker Documentation](https://docs.docker.com/dhi/core-concepts/distroless/)
- [Alpine, Distroless, or Scratch? - Google Cloud](https://medium.com/google-cloud/alpine-distroless-or-scratch-caac35250e0b)
- [Docker Hardened Images](https://www.infoq.com/news/2025/12/docker-hardened-images/)
