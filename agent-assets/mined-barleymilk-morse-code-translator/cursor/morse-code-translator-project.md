---
description: 
globs: 
alwaysApply: false
---
# Morse Code Translator Project Rules

## Project Overview
- 프로젝트명: Morse Code Translator
- 목적: 텍스트와 모스 부호 간의 실시간 변환 웹 애플리케이션

## Tech Stack
- Frontend: React + JavaScript
- Styling: Material-UI (MUI)
- State Management: React Context API
- Build Tool: Vite

## Project Structure
```
src/
├── components/
│   ├── Header/         # 헤더 컴포넌트
│   ├── TranslatorPanel/# 변환 패널
│   ├── AudioControls/ # 오디오 제어
│   ├── VisualMorse/   # 시각적 모스 부호
│   └── Footer/        # 푸터 컴포넌트
├── hooks/
│   ├── useTranslator  # 변환 로직
│   └── useAudioPlayer # 오디오 재생
├── utils/
│   ├── morseCodeMap   # 모스 부호 매핑
│   └── audioUtils     # 오디오 유틸리티
└── contexts/
    └── ThemeContext   # 테마 컨텍스트
```

## Features
1. 기본 기능
   - 텍스트 → 모스 부호 변환
   - 모스 부호 → 텍스트 변환
   - 실시간 변환

2. 오디오 기능
   - 모스 부호 소리 재생
   - 재생 속도 조절
   - 음높이 조절

3. UI/UX
   - 반응형 디자인
   - 다크/라이트 모드
   - 접근성 고려

## Coding Conventions
1. JavaScript
   - ES6+ 문법 사용
   - PropTypes를 통한 props 타입 검증
   - 함수형 컴포넌트만 사용

2. Styling
   - MUI 컴포넌트 우선 사용
   - 커스텀 스타일링:
     1. styled 컴포넌트 활용
     2. sx prop 사용 (간단한 수정)
     3. makeStyles 사용 (복잡한 스타일)
   - Theme 커스터마이징:
     1. 색상 팔레트
     2. 타이포그래피
     3. 컴포넌트 기본 스타일
   - 반응형 디자인은 MUI Breakpoints 활용

3. File Naming
   - 컴포넌트: PascalCase
   - 유틸리티/훅: camelCase
   - 테스트: *.test.js

## Git Conventions
- Branches:
  - main: 프로덕션
  - develop: 개발
  - feature/*: 기능
  - fix/*: 버그수정

- Commits:
  - feat: 새 기능
  - fix: 버그 수정
  - docs: 문서
  - style: 포맷팅
  - refactor: 리팩토링
  - test: 테스트
  - chore: 기타

## Implementation Priority
1. 기본 변환 기능
2. UI/UX 구현
3. 오디오 기능
4. 추가 기능 (다크모드 등)

## Quality Standards
- 컴포넌트 테스트 필수
- 코드 커버리지 80% 이상
- ESLint 규칙 준수

- 접근성 WCAG 2.1 준수