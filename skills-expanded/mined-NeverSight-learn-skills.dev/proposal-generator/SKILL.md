---
name: proposal-generator

description: "Tạo proposal/đề án có research, business case, technical solution. Trigger: RFP, bid, draft proposal, đề xuất dự án."
---

# Proposal Generator

Biến bất kỳ input nào (một ý tưởng vài dòng, một brief 1 trang, một RFP, một transcript, hay một dossier nghiên cứu) thành một proposal/đề án dự án hoàn chỉnh, có nghiên cứu, bao quát cả **business case** lẫn **technical solution**.

Skill này có cấu trúc cụ thể, không hand-wave. Sản phẩm tạo ra trông giống deliverable của một firm tư vấn / solution provider thực sự gửi cho khách hàng, không phải bài essay AI generic.

## Khi nào dùng skill này

Dùng khi user muốn một **deliverable độc lập** tổng hợp:

- Vấn đề và bối cảnh (business)

- Giải pháp đề xuất (technical)

- Vì sao dự án này có ý nghĩa tài chính (ROI / business case)

- Sẽ thực sự được build và delivery như thế nào (technical execution + plan)

KHÔNG dùng skill này cho:

- Hỏi đáp ngắn về một khía cạnh đơn lẻ (ví dụ "database nào tốt nhất cho X?"): trả lời inline

- Spec kỹ thuật thuần túy không có business framing: dùng workflow source-code spec

- Marketing copy hoặc email bán hàng: dùng message composition

## Quy trình tổng quát

Skill chạy theo 4 phase. Không bỏ qua phase nào: kể cả input mỏng cũng cần phase research, vì đó là chỗ proposal có được độ tin cậy.

```
Phase 1: Intake & Gap Analysis     →  Hiểu input, xác định thiếu gì
Phase 2: Research                   →  Lấp khoảng trống bằng web search + suy luận
Phase 3: Structured Drafting        →  Áp dụng template (business + technical)
Phase 4: Deliverable                →  Markdown trước; .docx/.pptx sau khi confirm
```

---

## Phase 1: Intake & Gap Analysis

Đọc kỹ input và phân loại:

| Mức độ đầy đủ | Ví dụ | Cần làm gì |

|---|---|---|

| **Thin** (mỏng) | "Tôi muốn build chatbot AI cho customer support" | Cần research nhiều. State assumptions rõ ràng và hỏi 2-3 câu trọng tâm trước khi draft nếu có gì thực sự blocking. |

| **Medium** | Brief 1 trang hoặc đoạn RFP ngắn | Research nhẹ để lấp gap cụ thể (market size, giải pháp tương đương, lựa chọn công nghệ). |

| **Rich** | RFP đầy đủ, dossier nghiên cứu, hoặc transcript chi tiết | Research tối thiểu; tập trung vào synthesis và structure. |

**Checklist intake bắt buộc**: trước khi draft, confirm hoặc infer mỗi mục dưới đây. Nếu vẫn còn 3+ mục chưa rõ sau khi đọc input, hỏi user ngắn gọn. Còn lại thì infer và state assumption rõ ràng.

1. **Audience là ai?** (lãnh đạo nội bộ, khách hàng ngoài, nhà đầu tư, khu vực nhà nước)

2. **Mục tiêu của proposal là gì?** (thắng thầu, xin duyệt budget, kickoff dự án, gọi vốn)

3. **Domain / ngành** (fintech, healthcare, e-commerce, manufacturing, v.v.)

4. **Quy mô ước lượng** (POC nhỏ, dự án mid-size, enterprise rollout)

5. **Ràng buộc** (trần ngân sách, deadline, regulatory, on-prem vs cloud)

Ghi rõ các giả định đã suy luận ở đầu phần reasoning trước khi draft. User phải thấy được mình đã giả định gì.

### Win Themes (xác định trước khi draft)

Trước khi bước sang Research, xác định 2-3 "win themes" cho proposal. Win theme là lý do cốt lõi vì sao team/công ty này là lựa chọn tốt nhất cho dự án này. Ví dụ:

- "Đã deliver 3 dự án cùng domain trong 18 tháng qua"
- "Practice QA automation in-house giảm defect rate"
- "Accelerator framework giảm 40% thời gian setup"

Win themes phải xuyên suốt các section liên quan. Nếu theme là QA thì Architecture section nhấn testability, Team section highlight QA engineer, Timeline có QA gate mỗi phase. Proposal không có win theme đọc như tài liệu mô tả. Proposal có win theme đọc như lập luận thuyết phục.

Nếu user không cung cấp differentiator, infer từ context (ngành nghề, tech stack quen thuộc, dự án tương tự) và state rõ assumption.

### Stakeholder Mapping

Proposal tốt điều chỉnh depth và tone theo người đọc. Map section chính với reader:

| Section | Reader chính | Điều chỉnh |
|---|---|---|
| Executive Summary | C-level, sponsor | Ngắn gọn, số liệu tài chính, không jargon kỹ thuật |
| Problem + Market Context | Business sponsor | Pain point bằng ngôn ngữ kinh doanh |
| Business Case / ROI | CFO, Finance | Số cụ thể, sensitivity analysis, payback |
| Proposed Approach (business view) | Decision maker phi kỹ thuật | Không code, không jargon, focus vào kết quả |
| Architecture + Stack + NFR | CTO, Tech Lead | Chi tiết kỹ thuật, justify lựa chọn, diagram |
| Timeline + Team | PM, Operations | Gantt, FTE, dependency, escalation |
| Pricing | Procurement, Finance | Rõ ràng, không surprise, scope in/out |

Nếu biết audience cụ thể (ví dụ: proposal cho CTO), tăng depth phần technical, giảm phần business overview. Nếu audience là board (chỉ đọc 5 phút), Executive Summary phải self-contained.

---

## Phase 2: Research

Research là thứ tách biệt một proposal thực sự với boilerplate generic. Dùng tool tìm kiếm web hiện có. Nếu có connector nội bộ như Drive, Gmail, hoặc CRM, kiểm tra thêm context liên quan khi được cấp quyền.

**Research checklist**: tối thiểu phải search:

- **Market context**: Đây có phải vấn đề đã được biết đến không? Quy mô thị trường? Xu hướng tăng trưởng?

- **Giải pháp tương đương**: Ai khác đang giải quyết vấn đề này? Họ tính giá ra sao? Architecture của họ ra sao?

- **Technical state-of-the-art**: Stack/pattern best-practice hiện tại cho loại hệ thống này là gì? Với tech thay đổi nhanh, luôn verify bằng nguồn mới.

- **Regulatory / compliance**: GDPR, HIPAA, PCI-DSS, **Nghị định 13/2023 (PDP) của Việt Nam**, Luật An ninh mạng 2018, tùy domain

- **Case study hoặc benchmark gần đây**: số liệu thực tế từ deployment tương tự

Số lượt search theo `references/research_checklist.md`. Cite nguồn trong proposal cuối cùng tại các chỗ có claim định lượng cụ thể như market size, benchmark numbers, regulatory facts.

**Lưu ý copyright**: paraphrase research findings; không paste verbatim từ source. Direct quote dưới 15 từ và không quá một quote/nguồn.

---

## Phase 3: Structured Drafting

Đọc template trong `references/proposal_template.md` ngay nếu chưa đọc.

Template **bắt buộc về cấu trúc** nhưng **linh hoạt về độ sâu**: điều chỉnh độ dài section theo độ đầy đủ của input và quy mô dự án. Proposal POC có thể có section 2 trang; bid enterprise có thể có section 5 trang.

**Cover cả hai phần đều nhau:**

- **Phần Business**: Executive Summary, Problem Statement, Market Context, Proposed Approach (high-level), Business Case / ROI (kèm Cost of Inaction, TCO, Sensitivity), Risks & Mitigation, Timeline, Pricing & Commercial Terms

- **Phần Technical**: Solution Architecture, Tech Stack, Data Model & Integration, Non-functional Requirements (performance, security, scalability), Delivery Plan, Team Structure, Quality Assurance Approach

- **Phần Quản trị & Thay đổi** (cho dự án mid-size trở lên): Assumptions & Dependencies, Governance Model, Change Management

Proposal mạnh một bên yếu một bên là output không chấp nhận được. Nếu input technical mỏng, research thêm; không cắt xén phần technical. Phần Quản trị & Thay đổi có thể giản lược cho POC nhưng không bỏ hoàn toàn cho dự án >=6 tháng.

**Xuyên suốt: reinforce win themes.** Kết nối win themes ở nơi tự nhiên và có bằng chứng. Không ép mọi section nhắc lại cùng một ý. Không chỉ liệt kê ở "Why Us" cuối cùng.

### Style cho proposal

- **Cụ thể, không generic**: viết "giảm thời gian xử lý ticket từ ~12 phút xuống dưới 4 phút" thay vì "cải thiện hiệu quả"

- **Định lượng khi có thể**: phần trăm, tiền, thời gian, headcount

- **Voice chủ động, thì hiện tại/tương lai**

- **Mặc định ngôn ngữ tiếng Việt**: nếu input bằng tiếng Anh và hướng đến khách hàng quốc tế thì viết bằng tiếng Anh; nếu user yêu cầu rõ thì làm theo. Mixed input → hỏi user.

- **Tránh AI-tells**: không "trong thời đại số phát triển nhanh chóng", không "hãy cùng đi sâu vào", không bullet 5 ý ở chỗ prose hợp hơn, không "điều quan trọng cần lưu ý là"

### Thuật ngữ tiếng Việt thường dùng (giữ nhất quán)

Một số thuật ngữ kỹ thuật có thể giữ nguyên tiếng Anh để chính xác và quen thuộc với reader Việt làm tech:

- API, REST, microservices, container, Kubernetes, CI/CD, DevOps, SLA, RTO/RPO → giữ nguyên

- Architecture, framework, stack, deployment → có thể giữ nguyên hoặc dịch tùy ngữ cảnh

- Test pyramid, unit test, integration test → giữ nguyên là chuẩn

Một số thuật ngữ business nên dịch để tự nhiên hơn:

- Executive Summary → Tóm tắt điều hành (hoặc giữ nguyên trong heading)

- Stakeholder → bên liên quan

- Deliverable → sản phẩm bàn giao

- Roadmap → lộ trình

- ROI → ROI (giữ nguyên, có thể giải thích "tỷ suất lợi nhuận đầu tư" trong ngoặc lần đầu)

Mục tiêu: đọc tự nhiên với reader Việt làm tech, không quá Anh hóa, không quá dịch máy.

### Hướng dẫn từng section

Xem `references/section_guidance.md` để có hướng dẫn chi tiết theo section, kèm ví dụ tốt vs xấu.

---

## Phase 4: Deliverable

### Mặc định: Markdown để review trước

**Đây là default behavior. Luôn xuất Markdown trước, KHÔNG jump thẳng sang .docx/.pptx.**

Lý do: proposal đầu là draft. User cần đọc nhanh, comment, sửa nội dung, trước khi tốn công format thành Word/PowerPoint. Markdown render tốt trong chat, dễ copy, dễ chỉnh, và sẽ convert nhanh sang format khác sau.

**Thư mục output:**

Tạo folder `proposal-generator/` trong thư mục làm việc hiện tại (hoặc thư mục user chỉ định). Tất cả deliverable của proposal lưu vào đây:

```
proposal-generator/
├── proposal-<tên-dự-án-ngắn>.md      # Draft Markdown (luôn tạo trước)
├── proposal-<tên-dự-án-ngắn>.docx    # Word document (sau khi user confirm)
├── proposal-<tên-dự-án-ngắn>.pptx    # Pitch deck (nếu user yêu cầu)
└── research-notes.md                  # Ghi chú research (tùy chọn, nếu research nhiều)
```

Tạo folder nếu chưa tồn tại: `mkdir -p proposal-generator`

Nếu môi trường không cho ghi file, xuất Markdown inline trong câu trả lời và ghi rõ rằng chưa tạo file.

**Cách tạo Markdown deliverable:**

1. Tạo file `proposal-generator/proposal-<tên-dự-án-ngắn>.md`

2. Cấu trúc theo `references/proposal_template.md`, đầy đủ tất cả section

3. Dùng heading hierarchy chuẩn (H1 cho tiêu đề proposal, H2 cho section, H3 cho subsection)

4. Dùng table Markdown cho stack, team, risks, pricing, NFRs, milestones

5. Cuối file ghi rõ một dòng: `*Bản nháp v1, sẵn sàng review*`

6. Thông báo cho user đường dẫn file và hỏi 2 câu ngắn:

   - "Có chỗ nào cần chỉnh nội dung không?"

   - "Sau khi confirm nội dung, bạn muốn export sang .docx, .pptx, hay cả hai?"

### Sau khi user confirm: Word document (.docx)

Khi user yêu cầu Word/docx, dùng skill `docx` (nếu có) hoặc dùng python-docx để sinh file. Tuân theo convention về heading, table, page break, table of contents.

Proposal .docx phải có:

- Trang bìa với tên dự án, tên khách hàng (nếu có), ngày, version

- Table of contents (mục lục)

- Tất cả section của template theo thứ tự

- Phụ lục cho diagram architecture chi tiết, bảng pricing chi tiết, CV team (nếu liên quan)

Lưu vào `proposal-generator/` cùng file Markdown.

### Tùy chọn: Pitch deck (.pptx)

Nếu user yêu cầu pitch deck, slide deck, presentation, hoặc "bản executive", tạo .pptx 10-15 slide tóm lược proposal:

1. Trang bìa

2. Vấn đề (1 slide)

3. Vì sao bây giờ / Market context (1 slide)

4. Giải pháp đề xuất, high level (1-2 slide)

5. Solution architecture diagram (1 slide)

6. Tech stack & approach (1 slide)

7. Business case / ROI (1 slide)

8. Timeline & milestones (1 slide)

9. Team & delivery model (1 slide)

10. Pricing summary (1 slide)

11. Risks & mitigation (1 slide)

12. Why us / differentiators (1 slide)

13. Next steps / call to action (1 slide)

Dùng skill `pptx` hoặc `pptx-creator` (nếu có) để sinh slide. Nếu không có skill, dùng PptxGenJS hoặc python-pptx. Lưu vào `proposal-generator/`.

---

## Đề xuất giả định và đặt câu hỏi

Trước khi research, nếu 3+ mục trong intake checklist chưa rõ VÀ câu trả lời sẽ thay đổi đáng kể hướng đi của proposal, hỏi 1-3 câu trọng tâm. Ví dụ câu hỏi tốt:

- "Proposal này dùng nội bộ hay gửi cho khách hàng ngoài?"

- "Quy mô ước chừng: POC cho một team, hay rollout enterprise cho hàng trăm user?"

- "Có ràng buộc cứng nào tôi cần biết không: bắt buộc dùng tech nào, trần budget cố định, hay yêu cầu pháp lý cụ thể?"

Nếu user đưa input mỏng nhưng nói "cứ chạy đi", bỏ qua câu hỏi, ghi giả định rõ ràng trong subsection "Giả định" của proposal, và tiếp tục.

---

## Reference files

- `references/proposal_template.md`: Cấu trúc proposal đầy đủ, từng section
- `references/section_guidance.md`: Hướng dẫn viết chi tiết và ví dụ tốt/xấu cho mỗi section
- `references/research_checklist.md`: Search gì khi gặp domain và loại dự án khác nhau

Đọc khi cần; không load tất cả lên trước cho task ngắn.
