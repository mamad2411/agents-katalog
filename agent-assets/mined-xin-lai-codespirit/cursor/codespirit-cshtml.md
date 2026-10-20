---
description: 
globs: *.cshtml
alwaysApply: false
---
# 通用要求

- 资源引用必须使用resource标签 [ResourceTagHelper.cs](mdc:Src/CodeSpirit.Web/TagHelpers/ResourceTagHelper.cs)
- 优先将样式、脚本写入到对应的样式、脚本文件
- 请不要引入Amis SDK的相关资源，模板页中已经引入。
