---
tags: [devops, dual, jre, docker, report]
name: dual-jre-docker-oz-report
description: Package a Java 21 Spring Boot app that bundles a legacy JRE 8 + sidecar Tomcat (OZ Report engine) in one Alpine container
trigger: User is containerizing an app that must run both a modern Spring Boot JAR and a legacy JRE-bound reporting/servlet engine side-by-side
category: devops
source_project: lucida-report
version: 1.0.0
---

# Dual JRE Docker (Modern + Legacy engine sidecar)

See `content.md`.
