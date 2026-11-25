---
name: curated-cross-view
description: 把参考画面转成另一机位，核对空间关系。 用户要求跨视角构图时使用。
license: Apache-2.0
metadata:
  nomi:
    version: 1.0.0
    label: 跨视角构图
    selectable-in-workbench: true
    tools: []
    required-providers:
      - image
    library:
      kind: skill
      title:
        zh-CN: 跨视角构图
        en: Change viewpoint
      summary:
        zh-CN: 把参考画面转成另一机位，核对空间关系。
        en: Show the reference scene from another camera viewpoint.
      appliesTo:
        - image
      group:
        zh-CN: 角色与场景
        en: Character and scene
      slots: []
      source:
        url: https://github.com/PicoTrex/Awesome-Nano-Banana-images/blob/2558bf0bb825be150c5d1aeab918cd90004882d3/README.md
        revision: 2558bf0bb825be150c5d1aeab918cd90004882d3
        author: https://x.com/op7418/status/1960896630586310656
        changes: >-
          Nomi adds Chinese task labels, reference slots and review criteria; fixed subjects are parameterized where
          noted.
        evidence:
          - https://x.com/op7418/status/1960896630586310656
          - https://x.com/op7418
      preview:
        path: assets/preview.jpg
        type: image
        provenance: upstream-output
        sourceUrl: https://raw.githubusercontent.com/PicoTrex/Awesome-Nano-Banana-images/main/images/case9/output.jpg
---

# 跨视角构图

把参考画面转成另一机位，核对空间关系。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

将照片转换为俯视角度并标记摄影师的位置

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
