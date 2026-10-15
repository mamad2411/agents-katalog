---
name: korean-code-comments
description: Write Korean comments on complex code sections whenever writing, editing, or creating code. Trigger on any code modification (feature implementation, bug fixes, refactoring, file creation, or code review). If you're touching code, consult this skill for commenting guidelines. Also applies when explaining code in conversation responses.
---

# Korean Code Comment Guide

## Core Rule

When writing or modifying code, always add Korean comments to complex sections that meet the criteria below, even without an explicit request. Once this skill is triggered, commenting is default behavior, not optional. These guidelines apply the moment you touch code, regardless of whether the user asks for comments.

Do not comment self-evident code. Comments are valuable when they explain "why" or "in what context."

## When to Write Comments

- Complex business logic or sections requiring domain knowledge
- Multi-step algorithms or data transformations
- Workarounds or edge case handling where intent is not obvious from code alone
- Non-intuitive usage of external APIs or libraries
- Unusual patterns used for performance optimization

Do NOT comment obvious code (variable assignments, simple conditionals, standard CRUD, etc.).

## Comment Style Rules

These rules apply to inline comments (`//`, `#`) and block comments (`/* */`).

### Tone

- **No formal/polite speech (존댓말 금지).** Use terse noun-phrase endings (명사형 종결).
- Write concise noun phrases focused on key terms. Omit unnecessary particles and predicates.

```
// 파일이 없으면 생성함        ← (X) verbose predicate
// 파일 부재 시 생성           ← (O) noun-phrase ending

// 관리자 권한이 필요할 때 팝업을 띄움  ← (X) verbose
// 관리자 권한 필요 시 팝업 표시       ← (O) concise
```

- Use parentheses () for supplementary details or conditions.

```typescript
// 세션 만료 시 리다이렉트 (로그인 페이지로)
```

### Numbered Steps

When explaining complex logic, use `1. 2. 3.` numbering for readability. Do NOT use `[1] [2]` or any other format.

```typescript
// 결제 프로세스
// 1. 재고 확인
// 2. 결제 금액 계산 (할인·쿠폰 적용)
// 3. PG사 결제 요청
// 4. 결제 결과에 따른 주문 상태 갱신
```

### Punctuation

- **No colons (`:`) inside comments.** Replace with natural Korean expressions.

```
// 기본값: 30초      ← (X) colon
// 기본값은 30초     ← (O) particle
// 기본값 30초       ← (O) omit particle
// 기본값 (30초)     ← (O) parentheses
```

- **Never use the em dash character (Unicode U+2014).** It is not a natural Korean punctuation mark. This applies to all output: code comments, markdown headings, error messages, and explanation text. Use parentheses, particles, commas, or restructure the sentence.

```
// 재고 확인 (품절 시 중단)       ← (O) parentheses
// 재고 확인, 품절 시 중단        ← (O) comma
// 재고 확인 후 품절 시 중단      ← (O) restructure

## `use cache` (새로운 방식)      ← (O) parentheses in heading
```

### No AI Authorship Traces

Do not use words like '사용자' or '요청' that imply AI authorship. Exception: '사용자' is allowed when referring to the software's end user.

## Additional Rules for Code Explanations in Conversation

When explaining code in conversation text (not in-code comments), follow these as well:

- Add comments to example code snippets to aid understanding
- When a before/after comparison is possible (new syntax, new API, etc.), show both versions
- When file path matters, place it as a comment on the first line of the code block

```typescript
// apps/web/src/lib/auth.ts
export function getSession() {
  // ...
}
```
