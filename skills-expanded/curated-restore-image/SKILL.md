---
name: curated-restore-image
description: 重新诠释旧图细节；结果可能改变原纹理。 用户要求旧图重新绘制时使用。
license: Apache-2.0
metadata:
  nomi:
    version: 1.0.0
    label: 旧图重新绘制
    selectable-in-workbench: true
    tools: []
    required-providers:
      - image
    library:
      kind: skill
      title:
        zh-CN: 旧图重新绘制
        en: Restore an illustrated image
      summary:
        zh-CN: 重新诠释旧图细节；结果可能改变原纹理。
        en: Increase resolution and reinterpret an old image using modern anime rendering.
      appliesTo:
        - image
      group:
        zh-CN: 角色与场景
        en: Character and scene
      slots: []
      source:
        url: https://github.com/PicoTrex/Awesome-Nano-Banana-images/blob/2558bf0bb825be150c5d1aeab918cd90004882d3/README.md
        revision: 2558bf0bb825be150c5d1aeab918cd90004882d3
        author: https://x.com/op7418/status/1960540798573011209
        changes: >-
          Nomi adds Chinese task labels, reference slots and review criteria; fixed subjects are parameterized where
          noted.
        evidence:
          - https://x.com/op7418/status/1960540798573011209
          - https://x.com/op7418
      preview:
        path: assets/preview.png
        type: image
        provenance: upstream-output
        sourceUrl: https://raw.githubusercontent.com/PicoTrex/Awesome-Nano-Banana-images/main/images/case74/output.png
---

# 旧图重新绘制

重新诠释旧图细节；结果可能改变原纹理。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

增强这张老图像的分辨率并添加适当的纹理细节，用现代动漫技术重新诠释它。

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
