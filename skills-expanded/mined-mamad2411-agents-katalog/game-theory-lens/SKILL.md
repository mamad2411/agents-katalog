---
name: game-theory-lens
description: "Phân tích chủ đề bằng Lý thuyết Trò chơi (Game Theory): người chơi, payoff, chiến lược, cơ chế."
---

# Game Theory Lens — Phân tích qua Lý thuyết Trò chơi

> *"Trò chơi là bất kỳ tình huống nào mà con người tương tác với nhau."*
> — Ken Binmore

Skill này giúp phân tích BẤT KỲ chủ đề nào — kinh doanh, quan hệ, chính trị, đời sống, xã hội — qua lăng kính Lý thuyết Trò chơi. Mục tiêu: nhìn thấu cấu trúc chiến lược ẩn sau mọi tương tác giữa các bên.

## Triết lý phân tích

Lý thuyết Trò chơi không phải về "thắng thua" — mà về **hiểu cấu trúc tương tác**:

- Ai là người chơi? Họ có lựa chọn gì?
- Kết quả phụ thuộc vào hành động của TẤT CẢ các bên, không chỉ một bên
- Chiến lược tối ưu phụ thuộc vào chiến lược của đối phương
- Đời thực hiếm khi là trò chơi tổng-bằng-không (zero-sum) — thường có cả xung đột lẫn hợp tác

## Quy trình phân tích

### Bước 0: Thu thập & Làm giàu thông tin

Trước khi phân tích, cần đủ dữ liệu. Hỏi user (chỉ hỏi những gì chưa có):

1. **Chủ đề/tình huống** cần phân tích là gì?
2. **Các bên tham gia** (players) chính là ai?
3. **Mục đích phân tích**: hiểu bản chất? ra quyết định? tư vấn chiến lược? dự đoán kết quả?

**Quy tắc làm giàu thông tin**: Khi user cung cấp ít thông tin (chỉ 1-2 câu mô tả chung), chủ động dùng WebSearch để:

- Tìm dữ liệu thực tế, số liệu, case study liên quan
- Xác định các bên tham gia và lợi ích từng bên
- Tìm quan điểm đa chiều (các bên khác nhau nghĩ gì)
- Tìm ví dụ tương tự đã xảy ra trong lịch sử

Gộp tất cả câu hỏi vào MỘT lượt hỏi duy nhất. Không hỏi lại nhiều lần.

### Bước 1: Nhận diện Trò chơi (Game Identification)

Đây là bước quan trọng nhất — xác định đúng "trò chơi" quyết định chất lượng toàn bộ phân tích.

**1.1. Xác định thành phần:**

- **Players**: Liệt kê tất cả bên tham gia có quyền ra quyết định
- **Strategies**: Mỗi player có những lựa chọn hành động nào?
- **Payoffs**: Kết quả (lợi ích/thiệt hại) cho mỗi tổ hợp chiến lược

**1.2. Map sang Game Archetype:**
Đọc `references/strategic-games.md` để map tình huống sang trò chơi mẫu phù hợp nhất:

| Đặc điểm tình huống                                     | Game Archetype      |
| ------------------------------------------------------- | ------------------- |
| Hợp tác có lợi nhưng ai cũng muốn "ăn free"             | Prisoner's Dilemma  |
| Ai nhường trước thì thua, nhưng cùng cứng thì cùng chết | Chicken             |
| Hợp tác có lợi nhất nhưng cần tin tưởng lẫn nhau        | Stag Hunt           |
| Muốn phối hợp nhưng bất đồng về cách thức               | Battle of the Sexes |
| Cần cùng chọn một chuẩn/quy ước                         | Coordination Game   |
| Một bên hoàn toàn đối lập lợi ích bên kia               | Zero-sum Game       |


Một tình huống có thể kết hợp nhiều archetype. Nếu không map chính xác, mô tả trò chơi mới với payoff matrix tự xây dựng.

**1.3. Trực quan hoá:**

- Vẽ **payoff matrix** (2 players, chiến lược hữu hạn) — dùng bảng markdown
- Hoặc **game tree** (trò chơi tuần tự) — dùng Mermaid flowchart
- Gán giá trị payoff ước lượng dựa trên phân tích lợi ích thực tế

Đọc `references/core-concepts.md` khi cần tra cứu cách xây dựng payoff matrix, tính utility, và lý thuyết nền.

### Bước 2: Phân tích Cấu trúc Chiến lược (Strategic Analysis)

**2.1. Tìm chiến lược trội (Dominant Strategy):**

- Có player nào có chiến lược tốt nhất BẤT KỂ đối phương làm gì?
- Nếu có → đó là chiến lược trội, player lý trí sẽ chọn nó

**2.2. Tìm Nash Equilibrium:**

- Tổ hợp chiến lược mà KHÔNG ai muốn đơn phương thay đổi
- Có thể có nhiều Nash equilibrium → cần phân tích thêm (focal point, convention)
- Đọc `references/core-concepts.md` cho phương pháp tìm

**2.3. Phân tích thông tin:**

- Ai biết gì? Ai không biết gì? (thông tin bất đối xứng)
- Có signaling không? (hành động gửi tín hiệu về ý định/năng lực)
- Có bluffing không? (gửi tín hiệu sai)
- Đọc `references/information-signaling.md` khi tình huống có yếu tố thông tin phức tạp

**2.4. Cân nhắc Mixed Strategy:**

- Nếu không có Nash equilibrium thuần → có thể có mixed equilibrium (ngẫu nhiên hoá)
- Ý nghĩa: player tối ưu khi đối phương không đoán được hành động

### Bước 3: Phân tích Động lực (Dynamic Analysis)

**3.1. Một lần hay lặp lại?**
Câu hỏi then chốt thay đổi hoàn toàn kết quả phân tích:

| Loại trò chơi      | Đặc điểm                     | Hệ quả                                  |
| ------------------ | ---------------------------- | --------------------------------------- |
| Một lần (one-shot) | Gặp 1 lần, không tái diễn    | Khó hợp tác, chiến lược ngắn hạn        |
| Lặp lại hữu hạn    | Biết chính xác bao nhiêu lần | Backward induction → thường bất hợp tác |
| Lặp lại vô hạn     | Không biết khi nào kết thúc  | Folk theorem → hợp tác khả thi          |


Đọc `references/repeated-games-trust.md` khi phân tích tương tác dài hạn, niềm tin, danh tiếng.

**3.2. Tiến hoá chiến lược:**

- Trong nhóm lớn, chiến lược nào sẽ lan rộng theo thời gian?
- ESS (Evolutionary Stable Strategy) — chiến lược không bị xâm lấn
- Đọc `references/evolution-cooperation.md` khi phân tích xu hướng xã hội, thị trường, văn hoá

**3.3. Thiết kế cơ chế (Mechanism Design):**

- Nếu có thể THAY ĐỔI LUẬT CHƠI: thiết kế incentive sao cho kết quả mong muốn trở thành equilibrium
- Đọc `references/mechanism-design.md` khi phân tích auction, policy, quy chế

### Bước 4: Đàm phán & Liên minh (nếu áp dụng)

Áp dụng khi tình huống có yếu tố chia phần, thương lượng, hoặc nhiều hơn 2 bên:

**4.1. Phân tích vị thế đàm phán:**

- BATNA (phương án tốt nhất nếu đàm phán thất bại) của mỗi bên
- Ai kiên nhẫn hơn? Ai sợ rủi ro hơn?
- Disagreement point (kết quả nếu không đạt thoả thuận)

**4.2. Coalition dynamics (3+ players):**

- Liên minh nào có thể hình thành?
- Liên minh nào ổn định? (Core, Shapley value)
- Có Condorcet paradox không? (vòng xoáy bất ổn)

Đọc `references/bargaining-coalitions.md` cho chi tiết.

### Bước 5: Đúc kết & Khuyến nghị

**5.1. Tổng hợp insight:**

- Bản chất cấu trúc tương tác là gì?
- Equilibrium dự đoán kết quả gì?
- Kết quả đó có hiệu quả (Pareto efficient) không?

**5.2. Cảnh báo ngụy biện:**
Đọc `references/paradoxes-fallacies.md` và kiểm tra xem phân tích có rơi vào:

- Ngụy biện mệnh lệnh phạm trù (Categorical Imperative): "nếu ai cũng làm vậy thì..."
- Ngụy biện trò chơi tổng-bằng-không: giả sử một bên được = bên kia mất
- Ngụy biện cam kết trong suốt: tin rằng tuyên bố chiến lược = thực hiện
- Bỏ qua yếu tố thời gian/lặp lại

**5.3. Khuyến nghị chiến lược:**

- Cho từng player: chiến lược tối ưu là gì? Vì sao?
- Nếu kết quả dự đoán không tốt cho xã hội: đề xuất thay đổi luật chơi (mechanism design)
- Nếu là trò chơi lặp lại: chiến lược xây dựng niềm tin nào hiệu quả?

**5.4. Sơ đồ tổng hợp:**
Vẽ Mermaid diagram tổng hợp toàn bộ phân tích:

- Flowchart logic chiến lược
- Hoặc mindmap các yếu tố ảnh hưởng

## Bảng tra cứu Reference

| Khi cần phân tích...                                          | Đọc file                              |
| ------------------------------------------------------------- | ------------------------------------- |
| Nash equilibrium, payoff matrix, utility, chiến lược trội     | `references/core-concepts.md`         |
| Map tình huống sang Prisoner's Dilemma, Chicken, Stag Hunt... | `references/strategic-games.md`       |
| Thông tin bất đối xứng, bluffing, costly signaling            | `references/information-signaling.md` |
| Tương tác lặp lại, niềm tin, danh tiếng, TIT-FOR-TAT          | `references/repeated-games-trust.md`  |
| Thiết kế cơ chế, đấu giá, incentive alignment                 | `references/mechanism-design.md`      |
| Tiến hoá chiến lược, ESS, kin selection                       | `references/evolution-cooperation.md` |
| Đàm phán, Nash bargaining, Shapley value, liên minh           | `references/bargaining-coalitions.md` |
| Ngụy biện, nghịch lý, common knowledge                        | `references/paradoxes-fallacies.md`   |


Chỉ load reference khi thực sự cần tra cứu cho bước phân tích đang thực hiện. Không load tất cả cùng lúc.

## Quy tắc output

- Lưu bài phân tích vào `{CWD}/game-theory-lens/{topic-slug}-{YYMMDD}.md`
- Dùng template từ `templates/analysis-output.md`
- Luôn có payoff matrix hoặc game tree trực quan
- Luôn có Mermaid diagram tổng hợp
- Ngôn ngữ: tiếng Việt, thuật ngữ game theory giữ nguyên tiếng Anh trong ngoặc
- Giải thích dễ hiểu, tránh jargon không cần thiết
- Mỗi insight phải có "VÌ SAO" (reasoning) và "NGHĨA LÀ GÌ" (implication)

## Ví dụ tình huống áp dụng

- Đàm phán lương với sếp → Bargaining + Information asymmetry
- Hai quán cà phê cạnh nhau cạnh tranh giá → Bertrand + Repeated game
- Biến đổi khí hậu giữa các quốc gia → Tragedy of Commons + Prisoner's Dilemma
- Quyết định ly hôn/chia tài sản → Bargaining + Coalition
- Startup chọn thị trường → Coordination Game + First-mover advantage
- Đội nhóm ai cũng đùn đẩy việc → Free-rider + Volunteer's Dilemma
- Chiến tranh giá giữa các hãng bay → Chicken + Repeated game
