---
name: bookstyle-html
description: 대표님이 "bookstyle-html", "북스타일", "책 양식", "플립북", "인사이트북" 이라고 하면 쓴다. 자료·URL·문서를 600×820 쪽 펼침 넘김 책(인사이트북 양식) 단일 HTML로 만들거나 고칠 때. 책 프레임이 화면을 가득 채운다. PDF는 만들지 않는다.
---

# bookstyle-html

자료를 화면을 가득 채우는 플립북(인사이트북 양식) 단일 HTML로 만든다.

이 SKILL.md와 같은 폴더를 `$SKILL_DIR`라 한다. **작업 전에 `$SKILL_DIR/GUIDE.md`를 끝까지 읽고** 하우스 규칙과 작업 순서를 따른다.

## 요약
1. `assets/template`을 작업 폴더로 복사하고 `book.json`(id, 제목, og 절대 URL)을 고친다.
2. `references/writing.md`, `patterns.md`, `components.md`를 보고 `pages/`를 쓴다(표지 → 목차 → 본문 → 부 표지 → 이야기+근거 → 정리 → 뒤표지).
3. `python3 scripts/build_book.py <폴더> -o <out.html>`로 빌드하고, `scripts/preview.py check|shot|view`로 넘침 0건과 화면을 확인한다.
4. `scripts/og_image.py`로 1200×675 JPG를 만들고 배포한다.

## 핵심 규칙
- 책 프레임은 화면을 가득 채운다(키트 viewer.js·book.css 그대로).
- 반응형, 글보다 도식, 원문 그림은 키우고 출처 캡션, 사실은 원문 그대로.
- HTML만, PDF 파일은 만들지 않는다.
