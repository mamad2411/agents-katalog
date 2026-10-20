---
name: antipattern-text-vi
description: Antipatterns for text generation/retrieval/usage in Vietnamese context. Use when reviewing AI-generated text for use in Vietnamese projects, especially those with historical or cultural content. Focuses on common failure modes, cultural sensitivity, and technical quality thresholds specific to the Vietnamese context.
---

# I.vi Text Antipatterns

Skill này rà soát văn bản để loại các dấu hiệu văn xuôi do AI tạo. Mục tiêu là nhận diện pattern khiến văn bản nghe rỗng, đồng phục, hoặc giả thẩm quyền.

Dùng skill này khi người dùng yêu cầu:

- kiểm tra một đoạn viết có giống AI không
- sửa văn bản cho tự nhiên hơn
- làm sạch draft trước production
- rà soát tài liệu song ngữ Việt - Anh
- biến một instruction appendix thành skill hoặc checklist viết
- tìm lỗi giọng văn trong narrative, slide, sample, spec, prompt, hoặc documentation

# I.en Text Antipatterns

This skill reviews prose to remove recognizable generated-text patterns. It is not a general style guide. Its purpose is to identify patterns that make writing sound hollow, uniform, or falsely authoritative.

Use this skill when the user asks to:

- check whether a passage sounds generated
- make prose more natural
- clean a draft before production
- review Vietnamese-English bilingual text
- turn an instruction appendix into a writing skill or checklist
- find voice problems in narratives, slides, samples, specs, prompts, or documentation

---

## I.1.vi Quy trình làm việc

1. Xác định chế độ đầu ra người dùng muốn:
   - `audit`: nêu lỗi, không viết lại toàn bộ
   - `rewrite`: viết lại đoạn văn
   - `audit+rewrite`: nêu lỗi chính rồi đưa bản sửa
   - `checklist`: chuyển quy tắc thành checklist dùng lại
2. Giữ tiếng Việt làm bản sơ cấp nếu văn bản song ngữ. Bản Anh phải dẫn xuất từ nghĩa, không dịch từng chữ.
3. Không thêm claim mới. Nếu bản sửa cần bổ sung thông tin nhưng chưa có bằng chứng, gắn `[UNVERIFIED]` hoặc hỏi người dùng.
4. Giữ cấu trúc cần thiết của tài liệu gốc. Chỉ đổi cấu trúc khi chính cấu trúc đó tạo anti-pattern.
5. Không dùng emoji trong câu trả lời, checklist, heading, ví dụ, hoặc bản sửa.

## I.1.en Workflow

1. Determine the user's desired output mode:
   - `audit`: identify issues without rewriting the whole text
   - `rewrite`: rewrite the text
   - `audit+rewrite`: identify the main issues, then provide a cleaned version
   - `checklist`: convert the rules into a reusable checklist
2. Treat Vietnamese as primary when the text is bilingual. The English version must derive from meaning, not word-for-word translation.
3. Do not add new claims. If a rewrite needs information not supported by evidence, tag it `[UNVERIFIED]` or ask the user.
4. Preserve the necessary structure of the original document. Change structure only when the structure itself creates the anti-pattern.
5. Do not use emoji in answers, checklists, headings, examples, or rewrites.

---

## I.2.vi Danh sách anti-pattern

### I.2.1 Từ vựng chết

Xóa hoặc thay bằng từ cụ thể. Các từ bị dùng đến mức mất nghĩa gồm:

`delve` `intricate` `tapestry` `pivotal` `underscore` `landscape` khi dùng nghĩa bóng `foster` `testament` `enhance` `crucial` `captivating` `fascinating` `groundbreaking` `transformative` `innovative` `seamless` `robust` `holistic` `nuanced`

Cũng loại bỏ các cụm:

- "serves as a testament to"
- "plays a vital/significant/key role"
- "watershed moment" hoặc "key turning point"
- "deeply rooted", "rich cultural heritage", "rich tapestry"
- "enduring legacy" hoặc "lasting legacy"
- "solidifies its place"
- "stands as a symbol of"

Quy tắc: Nếu cụm từ có thể mô tả bất kỳ chủ đề nào mà không cần thay đổi, nó là cliché.

### I.2.2 Phủ định song song

Pattern: "It's not X, it's Y", "Not just X -- it's Y", "It is not merely X; it is Y."

Nếu câu dùng phủ định để tạo drama, viết lại bằng khẳng định thẳng.

### I.2.3 Thổi phồng ý nghĩa

AI thường không mô tả sự kiện. Nó tuyên bố tầm quan trọng của sự kiện rồi dừng lại.

Cắt các tín hiệu sau khi chúng không mang thông tin:

- "It is important to note / remember / consider that..."
- "It is worth noting that..."
- "This matters because..."
- "No discussion of X would be complete without..."
- "Importantly, ..." khi chỉ là tín hiệu, không phải nội dung

Để sự kiện cụ thể tự tạo trọng lượng.

### I.2.4 Phân tích đuôi với -ing

Pattern: `[sự kiện], [verb]-ing [hệ quả rõ ràng]`.

Các đuôi thường rỗng: `ensuring...`, `highlighting...`, `reflecting...`, `emphasizing...`, `demonstrating...`, `showcasing...`, `illustrating...`, `reinforcing...`.

Nếu phần sau dấu phẩy chỉ nhắc lại điều câu đã nói, xóa nó.

### I.2.5 Quy tắc ba phần

AI thường liệt kê theo bộ ba: tính từ, lợi ích, bài học, hoặc phạm vi giả.

Ví dụ lỗi:

- "innovative, transformative, and groundbreaking"
- "informed, inspired, and empowered"
- "From intimate gatherings to global movements"

Dùng số lượng cần thiết: một nếu đủ; hai nếu có tương phản thật; ba chỉ khi có ba thứ thật sự khác nhau.

### I.2.6 Trích dẫn mờ

Các cụm như "Industry reports suggest", "Observers have noted", "Many experts believe", "Studies show", "According to some sources" không phải nguồn.

Nếu không có tên nguồn cụ thể, claim đó không có nguồn. Xóa claim hoặc gắn `[UNVERIFIED]`.

### I.2.7 Tóm tắt bắt buộc

Cắt kết luận chỉ nhắc lại phần đã nói:

- "In summary, ..."
- "In conclusion, ..."
- "To summarize, ..."
- "Overall, ..." khi không có tổng hợp thật
- "As we have seen, ..."
- "This article has explored..."

Đoạn cuối nên kết thúc bằng thông tin mới hoặc hệ quả, không phải echo.

### I.2.8 Từ nối dư thừa

Cắt `Moreover`, `Furthermore`, `Additionally`, `In addition`, `It should also be noted that` khi chúng chỉ làm đệm.

Giữ `However` khi có tương phản thật. Giữ `Therefore` khi có suy luận thật.

### I.2.9 Nhịp đều

Tránh mọi câu cùng độ dài và mọi đoạn cùng cấu trúc. Dùng câu ngắn khi cần nhấn. Dùng câu dài khi cần triển khai. Đoạn một câu hợp lệ.

### I.2.10 Định dạng thặng dư

Bold chỉ khi người đọc cần dừng lại tại chỗ đó. Nếu mọi thứ đều bold, không thứ gì bold.

### I.2.11 Emoji

Không dùng emoji trong tài liệu, câu trả lời, checklist, tiêu đề, bảng, ghi chú, hoặc ví dụ. Nếu cần nhãn, dùng chữ. Nếu cần phân cấp, dùng heading, số thứ tự, hoặc bullet thường.

## I.2.en Antipattern List

### I.2.1 Dead vocabulary

Cut or replace with specific wording. These words have been overused into meaninglessness:

`delve` `intricate` `tapestry` `pivotal` `underscore` figurative `landscape` `foster` `testament` `enhance` `crucial` `captivating` `fascinating` `groundbreaking` `transformative` `innovative` `seamless` `robust` `holistic` `nuanced`

Also cut these phrases:

- "serves as a testament to"
- "plays a vital/significant/key role"
- "watershed moment" or "key turning point"
- "deeply rooted", "rich cultural heritage", "rich tapestry"
- "enduring legacy" or "lasting legacy"
- "solidifies its place"
- "stands as a symbol of"

Rule: If the phrase could describe any subject without modification, it is a cliché.

### I.2.2 Negative parallelism

Pattern: "It's not X, it's Y", "Not just X -- it's Y", "It is not merely X; it is Y."

If a sentence uses negation to manufacture drama, rewrite it as a direct positive statement.

### I.2.3 Significance inflation

Generated prose often does not describe the event. It announces the event's importance and stops there.

Cut these signals when they do not carry information:

- "It is important to note / remember / consider that..."
- "It is worth noting that..."
- "This matters because..."
- "No discussion of X would be complete without..."
- "Importantly, ..." when it works as a signal rather than content

Let the specific fact carry the weight.

### I.2.4 Trailing -ing analysis

Pattern: `[event], [verb]-ing [obvious consequence]`.

Common empty tails: `ensuring...`, `highlighting...`, `reflecting...`, `emphasizing...`, `demonstrating...`, `showcasing...`, `illustrating...`, `reinforcing...`.

If the material after the comma only restates the sentence, cut it.

### I.2.5 Rule of threes

Generated prose often defaults to triads: adjectives, benefits, lessons, or false ranges.

Bad examples:

- "innovative, transformative, and groundbreaking"
- "informed, inspired, and empowered"
- "From intimate gatherings to global movements"

Use the number needed: one if enough; two if there is a real contrast; three only when there are three distinct things.

### I.2.6 Weasel attribution

Phrases such as "Industry reports suggest", "Observers have noted", "Many experts believe", "Studies show", and "According to some sources" are not sources.

No named source means no source. Cut the claim or tag it `[UNVERIFIED]`.

### I.2.7 Compulsive summary

Cut endings that only restate what has already been said:

- "In summary, ..."
- "In conclusion, ..."
- "To summarize, ..."
- "Overall, ..." when there is no real synthesis
- "As we have seen, ..."
- "This article has explored..."

The final paragraph should end with a new implication, not an echo.

### I.2.8 Connective filler

Cut `Moreover`, `Furthermore`, `Additionally`, `In addition`, and `It should also be noted that` when they only pad the prose.

Keep `However` when there is real contrast. Keep `Therefore` when there is real inference.

### I.2.9 Mechanical rhythm

Avoid making every sentence the same length and every paragraph the same shape. Use short sentences for emphasis. Use longer sentences for development. A one-sentence paragraph is valid.

### I.2.10 Excessive formatting

Use bold only when the reader needs to stop at that point. If everything is bold, nothing is.

### I.2.11 Emoji

Do not use emoji in documents, answers, checklists, headings, tables, notes, or examples. Use words for labels. Use headings, numbering, or ordinary bullets for hierarchy.

---

## I.3.vi Định dạng báo cáo audit

Khi người dùng yêu cầu audit, dùng mẫu này:

```markdown
## Kết luận ngắn
<1-3 câu. Nêu văn bản có vấn đề chính gì. Không tóm tắt lại toàn bộ input.>

## Findings
- [TYPE] <vấn đề cụ thể> | đoạn: "<trích ngắn>" | xử lý: <cắt/sửa/giữ có điều kiện>

## Bản sửa đề xuất
<nếu người dùng muốn rewrite hoặc audit+rewrite>
```

Các `TYPE` hợp lệ:

`DEAD-VOCAB`, `NEGATIVE-PARALLELISM`, `SIGNIFICANCE-INFLATION`, `TRAILING-ING`, `FALSE-THREE`, `WEASEL-ATTRIBUTION`, `COMPULSIVE-SUMMARY`, `CONNECTIVE-FILLER`, `MECHANICAL-RHYTHM`, `EXCESSIVE-FORMATTING`, `EMOJI`, `UNVERIFIED-CLAIM`.

## I.3.en Audit Report Format

When the user asks for an audit, use this template:

```markdown
## Short finding
<1-3 sentences. State the main prose problem. Do not summarize the whole input.>

## Findings
- [TYPE] <specific issue> | passage: "<short quote>" | treatment: <cut/rewrite/keep conditionally>

## Proposed rewrite
<only when the user wants rewrite or audit+rewrite>
```

Valid `TYPE` values:

`DEAD-VOCAB`, `NEGATIVE-PARALLELISM`, `SIGNIFICANCE-INFLATION`, `TRAILING-ING`, `FALSE-THREE`, `WEASEL-ATTRIBUTION`, `COMPULSIVE-SUMMARY`, `CONNECTIVE-FILLER`, `MECHANICAL-RHYTHM`, `EXCESSIVE-FORMATTING`, `EMOJI`, `UNVERIFIED-CLAIM`.

---

## I.4.vi Quick-check trước khi xuất văn bản

```markdown
[ ] Không có dead vocabulary.
[ ] Không có "not X, it's Y" hoặc biến thể phủ định tạo drama.
[ ] Không có câu tuyên bố tầm quan trọng thay cho bằng chứng.
[ ] Không có đuôi -ing rỗng.
[ ] Không có bộ ba giả hoặc phạm vi giả.
[ ] Mọi claim có nguồn cụ thể hoặc được gắn [UNVERIFIED].
[ ] Không có "In summary", "In conclusion", hoặc echo kết bài.
[ ] Không có từ nối đệm.
[ ] Câu và đoạn có nhịp biến thiên.
[ ] Bold dùng có chủ đích.
[ ] Không có emoji.
```

## I.4.en Quick-check before output

```markdown
[ ] No dead vocabulary.
[ ] No "not X, it's Y" or drama-making negation variant.
[ ] No sentence that announces significance in place of evidence.
[ ] No empty trailing -ing analysis.
[ ] No false triad or false range.
[ ] Every claim has a specific source or is tagged [UNVERIFIED].
[ ] No "In summary", "In conclusion", or echo ending.
[ ] No padding transitions.
[ ] Sentence and paragraph rhythm varies.
[ ] Bold is intentional.
[ ] No emoji.
```
