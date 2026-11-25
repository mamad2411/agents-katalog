---
name: ai-gateway-operator-manifest-update
description: Update batch-gateway manifests in opendatahub-io/ai-gateway-operator when the pinned llm-d-batch-gateway-operator main commit changes.
---

# Ai Gateway Operator Manifest Update

Use this skill for updating the batch-gateway manifests in the local
ai-gateway-operator checkout.

Run the helper:

~~~bash
bash scripts/update_manifests.sh
~~~

Run it from the ai-gateway-operator checkout, or pass another checkout with
`--repo PATH`. Automation should pass its local checkout path explicitly.

The helper reads the [batchgateway] SHA from
hack/scripts/get-manifests.sh, resolves refs/heads/main from
https://github.com/opendatahub-io/llm-d-batch-gateway-operator, and compares
commit ancestry. It exits without changes when the SHAs match or when the
OpenDataHub commit is not newer than the local pin. When OpenDataHub has a
newer commit, it updates the ODH SHA and runs make get-manifests.

After a change:

- Inspect the diff. Keep the pin and generated files under
  config/manifests/batchgateway/; do not include unrelated component output.
- Run git diff --check and
  kustomize build config/manifests/batchgateway/default.
- Report the old SHA, new SHA, changed files, and validation results.

The helper updates local files only. Committing and publishing changes are
outside this skill's scope.
