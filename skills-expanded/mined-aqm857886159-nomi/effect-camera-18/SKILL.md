---
name: effect-camera-18
description: 用明确的画面结构组织视觉重点。 用户要求前景遮挡时使用。
license: MIT
disable-model-invocation: true
metadata:
  nomi:
    version: 1.0.0
    label: 前景遮挡
    selectable-in-workbench: false
    tools: []
    required-providers:
    - image
    library:
      kind: effect
      title:
        zh-CN: 前景遮挡
        en: Foreground occlusion
      summary:
        zh-CN: 用明确的画面结构组织视觉重点。
        en: 'Foreground occlusion: Add a precise camera or composition instruction to the scene.'
      appliesTo:
      - image
      group:
        zh-CN: 构图
        en: Composition
      slots:
      - token: '{主体}'
        reference: subject
      source:
        url: https://github.com/jnMetaCode/ai-shortfilm-prompts/blob/f21500e5946973949c6bbf02e67e0c21b2e63a35/templates/camera-move-library.md
        revision: f21500e5946973949c6bbf02e67e0c21b2e63a35
        author: jnMetaCode
        changes: Nomi adds Chinese task labels, reference slots and review criteria; fixed subjects are parameterized where
          noted.
        evidence:
        - https://github.com/jnMetaCode/ai-shortfilm-prompts/blob/f21500e5946973949c6bbf02e67e0c21b2e63a35/templates/camera-move-library.md
      preview:
        path: assets/cover.png
        type: image
        provenance: illustration
---

A foreground element slides through frame, partially blocking {主体}
