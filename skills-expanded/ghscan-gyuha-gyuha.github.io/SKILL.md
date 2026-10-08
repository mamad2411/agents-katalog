---
title: "Image Prompt Reverse: 마음에 드는 이미지를 프롬프트로 역공학하는 Codex 스킬"
date: 2026-09-11T22:45:00+09:00
draft: false
categories:
  - Developer Tools
tags:
  - prompt-engineering
  - skills
  - ai
description: "참조 이미지를 분석하여 12가지 비주얼 요소와 3~5개 시각적 앵커를 추출하고, 450~700자 자연어 프롬프트와 15개 네거티브 프롬프트로 고재현율 복제를 지원하는 오픈소스 Codex 스킬을 살펴봅니다."
---

웹서핑을 하거나 핀터레스트, SNS를 둘러보다 보면 "도대체 어떤 프롬프트를 썼길래 이런 분위기가 나왔을까?" 감탄하게 되는 이미지를 자주 마주합니다. 하지만 막상 직접 프롬프트를 작성해 보면 조명이나 렌즈 화각, 질감 디테일이 달라 전혀 다른 결과물이 나오기 일쑤입니다.

`@doitnowbtbt` 님이 추천한 **Image Prompt Reverse** 는 OpenAI 코덱스(Codex) 환경에서 작동하는 오픈소스 스킬(Skill)로, **사용자가 이미지를 업로드하면 전문 프롬프트 디렉터 수준으로 비주얼을 분해하여 고재현율(High-fidelity)의 프롬프트와 네거티브 프롬프트를 역공학** 해냅니다.

<!--more-->

## Sources

- [Threads 원문 포스트: doitnowbtbt](https://www.threads.com/share/_6YTTbNvu/)
- [공식 GitHub 저장소: LunarXuan/image-prompt-reverse](https://github.com/LunarXuan/image-prompt-reverse)

---

## 1. 이미지 역공학 분석 파이프라인

```mermaid
flowchart TD
    classDef inNode fill:#c5dcef,stroke:#2b6cb0,stroke-width:1.5px,color:#333;
    classDef deconstructNode fill:#e0c8ef,stroke:#6b46c1,stroke-width:1.5px,color:#333;
    classDef anchorNode fill:#fde8c0,stroke:#d69e2e,stroke-width:1.5px,color:#333;
    classDef outNode fill:#c0ecd3,stroke:#38a169,stroke-width:1.5px,color:#333;

    Img["사용자 참조 이미지 업로드"] --> Decon["12대 비주얼 요소 정밀 분해<br>(매체, 구도, 렌즈 언어, 조명, 텍스처, 공간감)"]
    Decon --> Anchor["3~5대 핵심 시각적 앵커(Visual Anchors) 추출<br>(환각 방지 & 결정적 유사도 보장)"]

    Anchor --> Pos["Positive Prompt<br>(450~700자 자연어 정밀 묘사)"]
    Anchor --> Neg["Negative Prompt<br>(10~15개 필수 배제 키워드)"]

    Pos --> Gen["AI 이미지 모델 (Midjourney / SD / DALL-E)"]
    Neg --> Gen
    Gen --> Out["원본과 90% 이상 일치하는 고품질 재현작"]

    class Img inNode;
    class Decon deconstructNode;
    class Anchor anchorNode;
    class Pos,Neg,Gen,Out outNode;
```

---

## 2. 3대 차별화 핵심 기술

1. **12요소 다각도 비주얼 분해**:
   * 이미지의 용도, 매체(실사 사진/3D 렌더/일러스트), 주 피사체, 구도, 카메라 렌즈 화각, 조명 셋업, 색상 팔레트, 표면 재질, 배경 심도, 감정선 등 12가지 레이어를 체계적으로 분석합니다.
2. **시각적 앵커(Visual Anchors) 우선 추출**:
   * 보이지 않는 사소한 디테일을 억지로 지어내지 않고, 이미지 전체의 화풍과 분위기를 좌우하는 **3~5개의 핵심 시각적 앵커** 에 집중하여 환각을 차단합니다.
3. **텍스트 및 로고의 시각적 분리**:
   * 이미지 내에 포함된 영문/한글 텍스트나 로고를 시스템 프롬프트 명령어로 혼동하지 않고 순수 디자인 그래픽 요소로 완벽히 분리 처리합니다.

---

## 3. 설치 및 호출법
Codex의 로컬 Skills 폴더에 클론하여 `$image-prompt-reverse` 명령어로 즉시 호출할 수 있습니다:
```bash
git clone https://github.com/LunarXuan/image-prompt-reverse.git ~/.codex/skills/image-prompt-reverse
```
