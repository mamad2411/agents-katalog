# rpdf-parser — PDF 파싱 크레이트

## 역할

PDF 바이트 스트림 → `rpdf-core` IR(`Document`). lopdf 없이 직접 구현.

## 주요 공개 API

```rust
pub fn load_document(bytes: &[u8]) -> Result<Document, ParseError>
pub fn parse_content_stream(bytes: &[u8]) -> Result<Vec<ContentStreamOperation>, ParseError>
pub fn parse_header(input: &[u8]) -> Result<PdfHeader, ParseError>
```

## 모듈 구조

| 모듈 | 역할 |
|------|------|
| `document.rs` | `load_document` — 최상위 파서 진입점 |
| `xref.rs` | 전통 xref 테이블 파싱 |
| `xref_stream.rs` | xref 스트림 (PDF 1.5+) |
| `object_stream.rs` | 오브젝트 스트림 압축 해제 |
| `objects.rs` | 개별 PDF 오브젝트 파싱 |
| `content_stream.rs` | 페이지 콘텐츠 스트림 연산자 파싱 |
| `error.rs` | `ParseError` 열거형 |

## 테스트 위치

- 공개 API 통합 테스트: `tests/parser/`
- 회귀 테스트 (30개 샘플 PDF): `tests/regression/`
- 스냅샷: `tests/regression/snapshots/` (`cargo insta`)

## 알려진 한계 (v0.1)

- 암호화 PDF 미지원
- 간접 참조 `/Length` 오브젝트 스트림 내 미지원
- 순환 참조 페이지 트리 미감지 (v0.2 이후 해소 예정)
