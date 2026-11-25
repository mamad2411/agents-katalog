---
name: effect-transfer-expression
description: 参考表情：使用连接的参考，保留主体一致性。 用户要求参考表情时使用。
license: Apache-2.0
disable-model-invocation: true
metadata:
  nomi:
    version: 1.0.0
    label: 参考表情
    selectable-in-workbench: false
    tools: []
    required-providers:
    - image
    library:
      kind: effect
      title:
        zh-CN: 参考表情
        en: Reference expression
      summary:
        zh-CN: 参考表情：使用连接的参考，保留主体一致性。
        en: 'Reference expression: Apply the effect to connected references while preserving the subject.'
      appliesTo:
      - image
      group:
        zh-CN: 角色设定
        en: Character
      slots:
      - token: '{角色名}'
        reference: character
      source:
        url: https://github.com/PicoTrex/Awesome-Nano-Banana-images/blob/2558bf0bb825be150c5d1aeab918cd90004882d3/README.md
        revision: 2558bf0bb825be150c5d1aeab918cd90004882d3
        author: https://x.com/ZHO_ZHO_ZHO/status/1963156830458085674
        changes: Nomi-authored adaptation of the cited reference-editing pattern, with subject, composition and continuity
          constraints; the exact adapted formula has not been tested in Nomi. Upstream media demonstrates the original case
          only.
        evidence:
        - https://x.com/ZHO_ZHO_ZHO/status/1963156830458085674
        - https://x.com/ZHO_ZHO_ZHO
      preview:
        path: assets/cover.png
        type: image
        provenance: illustration
---

保持第一张参考图中{角色名}的身份、服装和构图，仅借用第二张参考图的表情。核对眼睛、嘴角与眉毛的变化，不把第二个人的五官迁移过来。
