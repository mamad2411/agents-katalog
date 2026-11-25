---
name: effect-fill-outpaint
description: 自然扩图：使用连接的参考，保留主体一致性。 用户要求自然扩图时使用。
license: Apache-2.0
disable-model-invocation: true
metadata:
  nomi:
    version: 1.0.0
    label: 自然扩图
    selectable-in-workbench: false
    tools: []
    required-providers:
    - image
    library:
      kind: effect
      title:
        zh-CN: 自然扩图
        en: Natural outpainting
      summary:
        zh-CN: 自然扩图：使用连接的参考，保留主体一致性。
        en: 'Natural outpainting: Apply the effect to connected references while preserving the subject.'
      appliesTo:
      - image
      group:
        zh-CN: 修图
        en: Editing
      slots:
      - token: '{主体}'
        reference: subject
      source:
        url: https://github.com/PicoTrex/Awesome-Nano-Banana-images/blob/2558bf0bb825be150c5d1aeab918cd90004882d3/README.md
        revision: 2558bf0bb825be150c5d1aeab918cd90004882d3
        author: https://x.com/bwabbage/status/1962903212937130450
        changes: Nomi-authored adaptation of the cited reference-editing pattern, with subject, composition and continuity
          constraints; the exact adapted formula has not been tested in Nomi. Upstream media demonstrates the original case
          only.
        evidence:
        - https://x.com/bwabbage/status/1962903212937130450
        - https://x.com/bwabbage
      preview:
        path: assets/cover.png
        type: image
        provenance: illustration
---

为参考中的{主体}补齐画面外部空白。保持原构图内的身份、比例和光线；让新区域自然衔接纹理、颗粒、焦点和透视，不加入额外主体或文字。
