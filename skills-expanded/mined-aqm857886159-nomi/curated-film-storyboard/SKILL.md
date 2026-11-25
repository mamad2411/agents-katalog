---
name: curated-film-storyboard
description: 把用户提供的剧本文字整理成宽屏分镜。 用户要求电影分镜时使用。
license: Apache-2.0
metadata:
  nomi:
    version: 1.0.0
    label: 电影分镜
    selectable-in-workbench: true
    tools: []
    required-providers:
      - image
    library:
      kind: skill
      title:
        zh-CN: 电影分镜
        en: Film storyboard
      summary:
        zh-CN: 把用户提供的剧本文字整理成宽屏分镜。
        en: Turn the supplied script into a coherent sequence of film storyboard panels.
      appliesTo:
        - image
      group:
        zh-CN: 角色与场景
        en: Character and scene
      slots:
        - token: '{剧本文字}'
          reference: text
      source:
        url: https://github.com/PicoTrex/Awesome-Nano-Banana-images/blob/2558bf0bb825be150c5d1aeab918cd90004882d3/README.md
        revision: 2558bf0bb825be150c5d1aeab918cd90004882d3
        author: https://x.com/jamesyeung18/status/1992597408128045462?s=20
        changes: >-
          Nomi adds Chinese task labels, reference slots and review criteria; fixed subjects are parameterized where
          noted.
        evidence:
          - https://x.com/jamesyeung18/status/1992597408128045462?s=20
          - https://x.com/jamesyeung18
      preview:
        path: assets/preview.jpg
        type: image
        provenance: upstream-output
        sourceUrl: https://raw.githubusercontent.com/PicoTrex/Awesome-Nano-Banana-images/main/images/pro_case27/output.jpg
---

# 电影分镜

把用户提供的剧本文字整理成宽屏分镜。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

使用宽屏面板，为以下用户提供的剧本创作电影分镜：{剧本文字}。保持同一角色的服装和场景空间关系，每格只表现一个镜头。

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
