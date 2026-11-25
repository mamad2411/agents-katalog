---
name: effect-restore-drawing
description: 旧图重绘：使用连接的参考，保留主体一致性。 用户要求旧图重绘时使用。
license: Apache-2.0
disable-model-invocation: true
metadata:
  nomi:
    version: 1.0.0
    label: 旧图重绘
    selectable-in-workbench: false
    tools: []
    required-providers:
    - image
    library:
      kind: effect
      title:
        zh-CN: 旧图重绘
        en: Restore drawing
      summary:
        zh-CN: 旧图重绘：使用连接的参考，保留主体一致性。
        en: 'Restore drawing: Apply the effect to connected references while preserving the subject.'
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
        author: https://x.com/op7418/status/1960540798573011209
        changes: Nomi-authored adaptation of the cited reference-editing pattern, with subject, composition and continuity
          constraints; the exact adapted formula has not been tested in Nomi. Upstream media demonstrates the original case
          only.
        evidence:
        - https://x.com/op7418/status/1960540798573011209
        - https://x.com/op7418
      preview:
        path: assets/cover.png
        type: image
        provenance: illustration
---

增强参考旧图的可读性，保留{主体}的轮廓、构图与原有风格，重新绘制受损细节。不要加入原图不存在的物体。结果属于生成式重绘，并非无损恢复。
