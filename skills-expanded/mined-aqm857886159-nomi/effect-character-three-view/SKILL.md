---
name: effect-character-three-view
description: 人物三视图：使用连接的参考，保留主体一致性。 用户要求人物三视图时使用。
license: Apache-2.0
disable-model-invocation: true
metadata:
  nomi:
    version: 1.0.0
    label: 人物三视图
    selectable-in-workbench: false
    tools: []
    required-providers:
    - image
    library:
      kind: effect
      title:
        zh-CN: 人物三视图
        en: Character turnaround
      summary:
        zh-CN: 人物三视图：使用连接的参考，保留主体一致性。
        en: 'Character turnaround: Apply the effect to connected references while preserving the subject.'
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
        author: https://x.com/Error_HTTP_404/status/1960405116701303294
        changes: Nomi-authored adaptation of the cited reference-editing pattern, with subject, composition and continuity
          constraints; the exact adapted formula has not been tested in Nomi. Upstream media demonstrates the original case
          only.
        evidence:
        - https://x.com/Error_HTTP_404/status/1960405116701303294
        - https://x.com/Error_HTTP_404
      preview:
        path: assets/cover.png
        type: image
        provenance: illustration
---

以参考中的{角色名}为唯一角色，在纯白背景上并排呈现正面、侧面和背面全身站姿。character sheet, three views turnaround, reference sheet style。三格人物等高，发型、服装、鞋和配饰一致；不添加文字。
