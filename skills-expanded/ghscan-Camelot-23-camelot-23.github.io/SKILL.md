---
title: vim备份
date: 2024-08-07T09:01:38+08:00
lastmod: 2024-08-07T09:01:38+08:00
author: elot
# avatar: /img/author.jpg
# authorlink: https://author.site
cover: /img/wallpaper/blue_sky&lake&forest.jpg
# images:
#   - /img/cover.jpg
categories:
  - vim
tags:
  - 技巧
# nolastmod: true
draft: false
---


<!--more-->

### 替换
替换当前行，或者块模式选中的行  
`:s/a/b/g` g替换为s  
`:s/\\/\//g` 正斜杠替换为反斜杠  
`:s/\//\\/g` 反斜杠替换为正斜杠  

替换指定行  
`:10,20 s/a/b/g` 10至20行g替换为s  