# Attachments 폴더

## 목적과 역할

이미지, PDF, 오디오 파일 등 노트에 첨부되는 미디어 파일을 보관하는 폴더입니다. 노트와 첨부 파일을 분리하여 관리합니다.

## 어떤 파일이 들어가는지

- 이미지 파일 (PNG, JPG, GIF, SVG)
- PDF 문서
- 오디오 파일
- 비디오 파일
- 기타 첨부 파일
- 스크린샷
- 다이어그램, 차트

## 작업 방식과 규칙

1. **자동 저장 설정**
   - Obsidian 설정: Files & Links
   - "Default location for new attachments" → "In the folder specified below"
   - 폴더 지정: `Attachments/`
   - 이미지 드래그&드롭 시 자동으로 이 폴더에 저장

2. **파일 명명**
   - 설명적인 이름 사용: `concept-diagram.png`
   - 날짜 포함: `2024-01-15-screenshot.png`
   - 또는 Obsidian의 자동 명명 활용
   - 한글 파일명 사용 가능하나 영문 권장

3. **하위 폴더 구조 (선택사항)**
   - 파일이 많아지면 연도별/월별 분류
   - `Attachments/2024/01/`
   - 또는 타입별: `Attachments/images/`, `Attachments/pdfs/`
   - 하지만 Obsidian이 자동으로 링크를 관리하므로 필수는 아님

4. **파일 관리**
   - 정기적으로 사용하지 않는 첨부 파일 확인
   - 대용량 파일 주의 (Git 저장소 크기 증가)
   - 중요한 이미지는 설명적인 alt 텍스트 추가

## Obsidian 설정 권장사항

```
Settings → Files & Links
- Default location for new attachments: "In the folder specified below"
- Attachment folder path: "Attachments"
- Automatically update internal links: ON
```

## 링크 사용법

Obsidian에서 이미지 첨부:
```markdown
![[image-name.png]]
![[image-name.png|300]] # 크기 조정
![[image-name.png|설명]] # alt 텍스트
```

## 주의사항

1. **저작권**
   - 타인의 이미지 사용 시 출처 표시
   - 저작권 확인

2. **용량 관리**
   - Git 저장소에 포함될 경우 크기 주의
   - 대용량 파일은 .gitignore 고려
   - 외부 이미지 호스팅 고려 (큰 파일의 경우)

3. **백업**
   - Attachments 폴더도 함께 백업
   - 노트만 백업하면 이미지 손실

## 명명 규칙

- 설명적이고 간결하게
- 공백 대신 하이픈(-) 사용 권장
- 소문자 사용 권장
- 날짜 포함 시: `YYYY-MM-DD-` 접두사

예: `2024-01-15-zettelkasten-workflow.png`
