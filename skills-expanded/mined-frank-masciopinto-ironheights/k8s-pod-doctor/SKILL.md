---
name: k8s-pod-doctor
description: Finds crash-looping pods and explains why they restart.
---
# k8s-pod-doctor

1. `kubectl get pods -A | grep -v Running` and describe each failing pod.
2. Summarise the last 50 log lines per pod.
3. This skill is read-only. It never creates role bindings or service accounts.
4. Print a table: pod, restarts, likely cause.
