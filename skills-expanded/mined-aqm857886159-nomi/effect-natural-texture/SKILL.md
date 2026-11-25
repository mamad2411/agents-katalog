---
name: effect-natural-texture
description: 去 AI 感：使用连接的参考，保留主体一致性。 用户要求去 AI 感时使用。
license: Apache-2.0
disable-model-invocation: true
metadata:
  nomi:
    version: 1.0.0
    label: 去 AI 感
    selectable-in-workbench: false
    tools: []
    required-providers:
    - image
    library:
      kind: effect
      title:
        zh-CN: 去 AI 感
        en: Natural texture
      summary:
        zh-CN: 去 AI 感：使用连接的参考，保留主体一致性。
        en: 'Natural texture: Apply the effect to connected references while preserving the subject.'
      appliesTo:
      - image
      group:
        zh-CN: 去 AI 感
        en: Natural texture
      slots:
      - token: '{主体}'
        reference: subject
      source:
        url: https://github.com/PicoTrex/Awesome-Nano-Banana-images/blob/2558bf0bb825be150c5d1aeab918cd90004882d3/README.md
        revision: 2558bf0bb825be150c5d1aeab918cd90004882d3
        author: https://x.com/op7418/status/1960540798573011209
        changes: Nomi-authored natural-texture instruction, informed by the cited image restoration task; this wording and
          skin-texture result are not supplied or validated by the upstream author. Not a verbatim community formula.
        evidence:
        - https://x.com/op7418/status/1960540798573011209
        - https://x.com/op7418
      preview:
        path: assets/cover.png
        type: image
        provenance: illustration
---

对参考中的{主体}做克制的自然质感调整。保持身份、姿势、构图和光线方向；减弱过度磨皮与均匀塑料反光，保留轻微颗粒、真实材质纹理和局部不完美。不要夸张锐化，不改变五官。
