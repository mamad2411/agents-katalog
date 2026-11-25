---
name: effect-object-six-view
description: 物件六视图：使用连接的参考，保留主体一致性。 用户要求物件六视图时使用。
license: Apache-2.0
disable-model-invocation: true
metadata:
  nomi:
    version: 1.0.0
    label: 物件六视图
    selectable-in-workbench: false
    tools: []
    required-providers:
    - image
    library:
      kind: effect
      title:
        zh-CN: 物件六视图
        en: Object views
      summary:
        zh-CN: 物件六视图：使用连接的参考，保留主体一致性。
        en: 'Object views: Apply the effect to connected references while preserving the subject.'
      appliesTo:
      - image
      group:
        zh-CN: 角色设定
        en: Character
      slots:
      - token: '{主体}'
        reference: subject
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

为{主体}生成前、后、左、右、上、下六个视图。白色背景，均匀分布，相同主体、比例与材质，等距透视；不添加文字。
