---
name: naver-photo-review
description: Use this skill when the user says "/naver photo review" or asks to analyze a folder of photos/videos for a Korean Naver Blog review, choose which images and videos belong in the post, map media to review sections, create a 10/15/20-photo composition, rename files for review use, copy selected media into a clean assets folder, or prepare photo/video evidence for sponsored product review campaigns.
---

# Naver Photo Review

## Purpose

Analyze a media folder before writing a Korean Naver Blog review. Select the strongest photos/videos, assign each item to a review role, and prepare clean review-ready filenames.

Default behavior: preserve originals and copy selected files into `naver_review_assets/` or `html_assets/` with ordered names. Rename originals only when the user explicitly asks.

## Quick Workflow

1. Inspect the folder with `rg --files`, `find`, or the bundled inventory script.
2. Generate media metadata with `scripts/media_inventory.py`.
3. Visually inspect representative images and videos.
4. Match media to campaign-required evidence.
5. Build the photo/video order for the review.
6. Create a rename/copy plan.
7. Copy selected files into a review assets folder with ordered filenames.
8. Report unused, duplicate, blurry, dark, or risky files.

Use this skill after `naver-unmet-need-item-survey` and before `naver-review-writing-ko`.

## Inventory Script

Run the bundled script first when a folder is provided:

```bash
python3 /Users/eiden/.codex/skills/naver-photo-review/scripts/media_inventory.py "/path/to/media-folder" --output "/path/to/media-folder/media_inventory.json" --csv "/path/to/media-folder/media_inventory.csv"
```

The script reports:

- media type: image or video
- filename and absolute path
- extension
- file size
- image width/height when available
- video duration/resolution when `ffprobe` is available
- orientation guess
- modified time

The script does not modify source files.

## Visual Inspection Rules

Inspect enough files to make reliable assignments. For small folders, inspect all images. For large folders, inspect thumbnails/contact sheets or representative files first, then open uncertain candidates.

Use local image viewing tools when needed. For videos, use metadata first, then inspect thumbnails or play/screenshot if the content choice matters.

Judge media on:

- clarity: no blur, shake, or heavy noise
- lighting: no harsh reflection, blown highlights, or dark shadows
- composition: product/scene is centered and easy to understand
- evidence value: shows a required step or product feature
- Naver fit: works as vertical mobile content when possible
- uniqueness: avoid near-duplicate photos unless showing before/after or sequence

## Review Slot Mapping

For a 15-photo sponsored product review, prefer this structure:

```text
01_representative_product
02_package_outer
03_package_open
04_components_overview
05_product_front
06_product_detail
07_size_or_texture
08_usage_step_1
09_usage_step_2
10_before
11_after
12_result_closeup
13_lifestyle_use
14_information_or_summary
15_final_recommendation
```

Adjust names by category:

- Beauty: `texture`, `dropper`, `before_skin`, `after_skin`, `application`
- Food: `menu_board`, `dish_overview`, `texture_closeup`, `table_scene`
- Digital goods: `download_email`, `file_import`, `cover_page`, `index_page`, `planner_page`, `writing_sample`, `app_use`
- Tech: `box`, `ports`, `setup`, `screen`, `desk_use`, `comparison`
- Place: `exterior`, `interior`, `menu`, `main_service`, `detail`, `result`

For campaign-required media, prioritize evidence over aesthetics.

## Digital Product Mapping

For GoodNotes, PDF templates, study planners, and digital notes, use this 15-photo/video structure:

```text
01_representative_screen
02_product_page_or_cover
03_download_or_file_received
04_import_to_goodnotes
05_cover_options
06_index_or_hyperlink
07_monthly_or_weekly_planner
08_study_planner_page
09_note_template
10_writing_sample
11_sticker_or_design_elements
12_color_variants
13_ipad_real_use
14_galaxy_or_noteshelf_note
15_final_use_scene
video_01_screen_recording
```

If the user provides screen recordings, choose the video that best shows a real interaction such as hyperlink navigation, page switching, writing, sticker use, or planner setup.

## Campaign Evidence Checklist

Create this table before renaming:

```text
| 캠페인 요구사항 | 선택 파일 | 역할 | 부족 여부 |
|---|---|---|---|
| 대표 썸네일 | | | |
| 사진 n장 이상 | | | |
| 영상/움짤 1개 | | | |
| 제품 상세/디자인 | | | |
| 사용 방법/실사용 | | | |
| BEFORE/AFTER 또는 결과 | | | |
| 링크/공정배너용 위치 | 별도 삽입 | | |
```

## Rename Plan

Before copying or renaming, output a plan:

```text
| 순서 | 원본 파일명 | 새 파일명 | 본문 역할 | 캡션 방향 |
|---|---|---|---|---|
| 01 | IMG_0001.JPG | 01_representative_product.jpg | 대표 이미지 | 제품이 한눈에 보이는 컷 |
```

Filename rules:

- Use lowercase English and numbers.
- Prefix with two digits: `01_`, `02_`, ...
- Use descriptive nouns: `package`, `detail`, `texture`, `usage`, `before`, `after`, `final`.
- Keep extensions appropriate. Do not change the extension unless converting format.
- Avoid spaces, Korean, parentheses, and special characters in final asset names.
- For videos, use `video_01_usage.mp4` or `video_01_screen_recording.mp4`.

## File Handling Rules

Default:

1. Create `naver_review_assets/` inside the given folder.
2. Copy selected files there using review-ready names.
3. Leave original files untouched.

Only rename originals when the user explicitly says to rename originals. If renaming originals, create a reversible rename table first.

If a target file exists, do not overwrite silently. Add a suffix or ask the user if overwrite is intended.

## Output Format

Use this order:

```text
## 결론
## 폴더 미디어 현황
## 캠페인 요구사항 매칭
## 추천 사진/영상 구성
## 파일명 변경/복사 계획
## 제외할 파일
## 부족한 촬영컷
## 다음 단계
```

After copying files, include the output folder path and a concise summary:

```text
선택 사진: 15장
선택 영상: 1개
출력 폴더: /absolute/path/naver_review_assets
```

## Quality Warnings

Flag these issues clearly:

- too few photos for the campaign requirement
- no video or weak video evidence
- missing required evidence such as texture, usage, before/after, or screen recording
- duplicate shots
- blurry, dark, reflected, or cropped photos
- filenames that will be confusing during HTML or Notion copy-paste work
