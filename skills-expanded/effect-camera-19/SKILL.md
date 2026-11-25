---
name: effect-camera-19
description: 用明确的画面结构组织视觉重点。 用户要求后景虚化时使用。
license: MIT
disable-model-invocation: true
metadata:
  nomi:
    version: 1.0.0
    label: 后景虚化
    selectable-in-workbench: false
    tools: []
    required-providers:
    - image
    library:
      kind: effect
      title:
        zh-CN: 后景虚化
        en: Background bokeh
      summary:
        zh-CN: 用明确的画面结构组织视觉重点。
        en: 'Background bokeh: Add a precise camera or composition instruction to the scene.'
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

Shallow depth of field, {主体} sharp, background melted to soft bokeh
