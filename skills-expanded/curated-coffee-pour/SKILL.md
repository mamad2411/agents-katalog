---
name: curated-coffee-pour
description: 把注入、油脂和蒸汽拆成清楚的镜头节拍。 用户要求咖啡倾注特写时使用。
license: CC-BY-4.0
metadata:
  nomi:
    version: 1.0.0
    label: 咖啡倾注特写
    selectable-in-workbench: true
    tools: []
    required-providers:
      - video
    library:
      kind: skill
      title:
        zh-CN: 咖啡倾注特写
        en: Espresso Pour, Crema Physics
      summary:
        zh-CN: 把注入、油脂和蒸汽拆成清楚的镜头节拍。
        en: Adapt Espresso Pour, Crema Physics to the supplied references and check continuity.
      appliesTo:
        - video
      group:
        zh-CN: 广告
        en: Advertising
      slots:
        - token: '{品牌名}'
          reference: text
      source:
        url: >-
          https://github.com/LichAmnesia/awesome-ad-video-prompts/blob/ac5b61177a81343e958f63212c4df7f25dc4c265/README.md
        revision: ac5b61177a81343e958f63212c4df7f25dc4c265
        author: LichAmnesia
        changes: >-
          Nomi adds Chinese task labels, reference slots and review criteria; fixed subjects are parameterized where
          noted.
        evidence:
          - >-
            https://github.com/LichAmnesia/awesome-ad-video-prompts/blob/ac5b61177a81343e958f63212c4df7f25dc4c265/README.md
      preview:
        path: assets/preview.png
        type: image
        provenance: upstream-output
        sourceUrl: >-
          https://raw.githubusercontent.com/LichAmnesia/awesome-ad-video-prompts/main/images/espresso-pour-crema-physics.png
---

# 咖啡倾注特写

把注入、油脂和蒸汽拆成清楚的镜头节拍。

确认已有参考素材与目标尺寸。缺少决定人物身份、产品外观或故事内容的输入时，先让用户补齐。按下面的原仓配方组织生成描述；把显式槽位替换成用户内容，不虚构品牌。

## 配方

A matte ceramic cup sits centered on warm travertine, hard morning side-window light slanting across the scene. 0-2s: top-down macro of a thick crema-rich espresso stream falling from a polished portafilter, the surface blooming into a tiger-striped crema as steam curls off it. 2-3s: tilt to a low table-level angle, golden backlight igniting the rising vapor against deep shadow. 3-5s: a slow lateral truck around the cup as a single sugar cube drops, concentric ripples spreading through the crema in slow motion. 5-8s: settle on a hero three-quarter with the {品牌名} foil bag glinting behind. Liquid keeps believable viscosity and the crema reads as a continuous skin — no smearing, ghosting, broken-stream artifacts, or boil-up. Sound: gurgle of extraction, hiss of steam, a single ceramic clink.

## 验收

核对主体身份、数量、结构、光影和镜头连续性。原仓媒体是配方来源证据，不是 Nomi 本次实测结果。多视角图不保证真实三维几何；生成式修复可能重新绘制细节。完成前展示产物，指出可见偏差。

来源和更改说明见 frontmatter；保留随包许可证。
