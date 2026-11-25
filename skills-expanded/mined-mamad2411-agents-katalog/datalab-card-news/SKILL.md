---
name: datalab-card-news
description: 글이나 주제를 여러 장짜리 캔버스로 기획해 데이터랩툴즈 사진 편집기에 실제로 만들어 넣는다. 카드뉴스·캐러셀·발표자료·PT 슬라이드에 사용한다. 빈 프로젝트로 시작하거나 저장 프로젝트를 열 수 있고 AI 이미지 생성은 유료라 매수를 먼저 확인한다.
license: Proprietary
metadata:
  surfaces: both
  install: optional
  tools: photo_project_get, photo_project_new, photo_project_list, photo_project_open, photo_canvas_get, photo_canvas_resize, photo_page_add, photo_page_reorder, photo_background_set, photo_text_add, photo_shape_add, photo_sticker_add, photo_frame_add, photo_template_apply, photo_node_arrange, photo_node_update, photo_gallery_list, photo_image_add_from_gallery, generate_images, my_content_read, my_content_info
---

## MCP 도구 연결

요청에 필요한 실제 도구가 현재 목록에 직접 보이면 그 도구를 사용한다. 보이지 않으면
사용자의 원래 의도를 `datalab_find_tools`에 보내고, 반환된 스키마와 도구 이름만 사용해
`datalab_call`로 실행한다. 도구 이름이나 인자를 지어내지 않는다. 결과가
`awaiting_confirm`이면 원래 호출을 반복하지 말고 ticket을 `datalab_confirm_status`로
확인한다.


# 카드뉴스 기획과 제작

글이나 주제 하나를 인스타그램 카드뉴스로 기획하고, 데이터랩툴즈 사진 편집기 캔버스에
슬라이드마다 실제로 만들어 넣는다. 산출물은 다른 곳에 붙여넣을 텍스트가 아니라 완성된
캔버스 그 자체다.

## 시작하기 전에 — 프로젝트를 정한다

새 작업이면 `photo_project_new`로 빈 프로젝트를 만든다. 이 호출은 관리 탭을 직접 열 수 있다.
저장된 작업을 이어가면 `photo_project_list`로 찾고 `photo_project_open`으로 연다. 현재 문서를
바꾸는 호출이므로 사용자 확인을 거친다.

`photo_project_get`과 `photo_canvas_get`으로 현재 project ref, revision과 기존 페이지를 확인한다.
기존 내용이 있으면 이어서 쓸지 새 프로젝트로 바꿀지 묻는다. 이후 변경 호출에는 가능하면
같은 editor session, project ref와 expected revision을 넘겨 대상이 바뀌면 멈추게 한다.

## 무엇을 읽고 시작하나

1. 사용자가 글이나 주제를 직접 줬으면 그것이 기준이다.
2. "이 글을 카드뉴스로" 처럼 이미 발행한 글을 가리키면 `my_content_read` 로 본문을 읽는다.
   제목만 알고 있으면 `my_content_info` 로 먼저 찾는다.
3. 둘 다 없으면 무슨 주제인지 묻고 멈춘다. **지어내지 않는다.**

## 기획은 짧게 확인만 한다

설문을 순서대로 재생하지 않는다. 다음 세 가지만 확인되면 바로 만든다.

- **플랫폼** — 인스타그램(1:1 또는 4:5)이 기본. 다르면 물어본다.
- **슬라이드 수** — 안 정했으면 본문 분량 기준으로 5~7장을 제안하고 확인만 받는다.
- **스타일 방향** — 색·톤을 한두 마디로. 몰라도 진행하고 기본값(단색 배경 + 절제된 톤)을
  쓴다.

슬라이드 역할과 텍스트 요소별 글자수 가이드는 `references/slide-structure.md`.

## 만들기

첫 페이지 전에 `photo_canvas_resize` 로 플랫폼 비율을 맞춘다. 이후 슬라이드마다:

1. `photo_page_add` 로 페이지를 만든다.
2. `photo_background_set` 으로 배경을 정한다 — 단색·그라데이션이 기본값이다.
3. 이미지가 필요하면 `photo_gallery_list` 로 갤러리를 먼저 본다. 쓸 이미지가 있으면
   `photo_image_add_from_gallery` 로 넣는다. 없고 사용자가 원하면 아래 "이미지 생성은
   유료다"를 따른다.
4. `photo_text_add` 로 타이틀·서브타이틀·본문·CTA 텍스트를 넣는다.
5. 장식이 필요하면 `photo_shape_add` · `photo_sticker_add` · `photo_frame_add`. 여러
   페이지에 같은 레이아웃을 반복하려면 `photo_template_apply`.
6. 배치는 `photo_node_arrange`, 슬라이드 순서는 `photo_page_reorder` 로 조정한다.

수정 요청이 오면 `photo_node_update` 로 기존 요소를 고친다.

**이 스킬은 페이지나 요소 삭제를 사용하지 않는다.** 삭제 요청은 별도의 파괴적 확인이 필요한
작업이라고 안내하고, 카드 제작 흐름에서 임의로 실행하지 않는다.

## 이미지 생성은 유료다

`generate_images` 는 사용자에게 과금된다. 슬라이드마다 하나씩 생성하면 N장이 N번 과금이다.

- 기본은 색·그라데이션 배경 + 텍스트만으로 시안을 제안한다. 과금이 없다.
- AI 이미지를 원하면 **몇 장을 생성할지 먼저 확인한다.** 예: "8슬라이드 전부 AI 이미지로
  만들면 8번 과금돼요. 몇 장이나 할까요?"
- 실제 단가는 알 수 없다 — 매수만 명확히 확인하고, 승인 없이 슬라이드 수만큼 자동으로
  돌리지 않는다.

## 없는 것 (찾지 마라)

- 외부 이미지 생성기에 복사해 붙여넣을 프롬프트 형식은 만들지 않는다. 이 표면은 도구를
  직접 부른다.
- 저장 수·공유 수·완독률 같은 성과를 읽어오는 도구는 없다. 캡션에 "저장을 유도하는 문구를
  넣으라"는 제안은 할 수 있지만 그 결과 수치를 지어내거나 예측하지 않는다.
- 프롬프트나 디자인에 품질 점수를 매기지 않는다.

## 슬라이드에 숫자를 지어내지 않는다

발표자료 요청은 사용자가 실제 판단에 쓸 가능성이 높다. 그런데 이 스킬에는 차트 도구도,
데이터를 캔버스에 자동 반영하는 도구도 없다 — 숫자는 전부 손으로 적히는 텍스트다.

- 사용자가 준 숫자만 옮긴다. 출처를 함께 적는다.
- 현재값·목표값·ROI·성장률·시장규모 같은 칸을 **채워 넣지 않는다.** 빈칸으로 두고 "이
  숫자는 확인해서 채워 주세요"라고 말한다.
- 그럴듯한 예시 수치로 자리를 메우지 않는다 — 붙여넣는 순간 사실처럼 보인다.

## 산출물

- 완성된 캔버스 — 열려 있던 그 캔버스에 페이지가 채워진 상태.
- 복사용 텍스트 요약 — 슬라이드별 헤드라인과 서브텍스트, 캔버스에 넣은 내용 그대로.
- 원하면 해시태그 제안. 예상 도달·참여 수치는 붙이지 않는다.
