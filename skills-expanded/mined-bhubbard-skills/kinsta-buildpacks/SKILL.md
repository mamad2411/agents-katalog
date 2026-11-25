---
name: kinsta-buildpacks
description: "Instructions for configuring Buildpacks and Nixpacks on Kinsta. Use this when the user asks about Dockerfiles, Nixpacks, Buildpacks, or customizing the build process on Kinsta."
---

# Kinsta Buildpacks and Dockerfiles

When an application is deployed to Kinsta, it needs to be built into a container image. Kinsta supports two primary ways to do this: Buildpacks (specifically Nixpacks) and Dockerfiles.

## 1. Nixpacks (Default)
- Nixpacks is the default builder on Kinsta. It automatically detects the language and framework and creates a build environment for it.
- **Configuration**: You can customize Nixpacks by adding a `nixpacks.toml` file to your repository root.
- **Use Cases**: Best for standard applications (Node.js, Python, PHP, Ruby, Go, Rust, etc.) where you don't need advanced OS-level customization.
- **Overrides**: You can set environment variables to tell Nixpacks which language version to use (e.g., `NIXPACKS_NODE_VERSION=18`).

## 2. Dockerfile
- If you need complete control over the container, you can provide your own `Dockerfile`.
- Kinsta will build the Dockerfile and deploy the resulting image.
- **Configuration**: Place the `Dockerfile` in the root of your repository (or specify its path in MyKinsta).
- **Listening on PORT**: Your Docker container must listen on the port specified by the `PORT` environment variable (usually 8080).

## 3. Build Configuration
- Ensure your `package.json`, `requirements.txt`, `Gemfile`, or `go.mod` is properly configured so Nixpacks or the Dockerfile can install the required dependencies.
- During the build phase, memory and CPU limits apply. Large builds may require more resources.

## 4. Troubleshooting Builds
- If a build fails, check the "Build Logs" in MyKinsta.
- Common issues include missing dependencies, out-of-memory errors, or syntax errors in configuration files.
