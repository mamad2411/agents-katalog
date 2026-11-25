---
name: deploy-jvm
description: Deploy a Java Spring Boot app fast. Use when deploying JVM, Java, or Spring applications, or when Vercel is not an option for the backend.
---

# JVM Deploys Under a Clock

Vercel does not host Spring. Options ranked:

1. **Railway** — `railway login` (browser), `railway init`, `railway up`. Buildpacks detect
   Maven/Gradle automatically. One requirement: respect the injected port —
   `server.port=${PORT:8080}` in application.properties. With an existing account,
   budget 15-25 min for the first successful build.
2. **Render** — dashboard-driven web service from the repo; simple but first builds are slow.
3. **Local demo + Dockerfile as artifact** — legitimate under a clock. Demo on localhost,
   commit a two-stage Dockerfile (`eclipse-temurin:21` build → `21-jre` run), and note:
   "deployable by `docker build`; I spent the deploy minutes on features — happy to walk
   through the pipeline I'd stand up."

## Decision rule

Decide early — around the skeleton checkpoint — whether a real JVM deploy is happening.
Past that point, option 3 beats a half-configured cloud deploy every time. A working local
demo with a clean Dockerfile and a clear explanation beats a broken prod URL.
