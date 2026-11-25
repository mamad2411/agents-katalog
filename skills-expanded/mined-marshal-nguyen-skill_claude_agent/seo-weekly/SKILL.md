---
name: seo-weekly
description: Chạy báo cáo SEO định kỳ cho citeflow.io bằng cách ghép dữ liệu Google Search Console và GA4, xuất file markdown tiếng Việt. Dùng khi người dùng nói "báo cáo SEO", "seo tuần", "seo tháng", "check SEO", "tình hình search", "traffic organic tuần này", hoặc gọi /seo-weekly. Cũng dùng khi cần so sánh hiệu suất tìm kiếm giữa hai khoảng thời gian, tìm cơ hội CTR, hoặc phát hiện query/trang bị tụt hạng.
---

# Báo cáo SEO tuần — CiteFlow

Ghép GSC (chuyện xảy ra trước cú click) với GA4 (chuyện xảy ra sau cú click) thành một báo cáo có thể hành động được, không phải một bảng số liệu.

## Cấu hình

Sửa các giá trị này nếu đổi site hoặc property:

```
GSC_SITE      = "https://www.citeflow.io/"
GA4_PROPERTY  = "properties/536342158"
OUTPUT_DIR    = "~/reports"
```

MCP server: `gsc` (Search Console) và `ga4` (Analytics). Nếu tool báo không tồn tại, gọi `get_capabilities` của server `gsc` để lấy danh sách tool thật thay vì đoán.

## Bước 0 — Xác định khoảng thời gian

**Quan trọng: GSC trễ dữ liệu 2–3 ngày.** Không bao giờ lấy đến ngày hôm nay, số liệu sẽ thiếu và tạo ra cảnh báo sụt giảm giả.

Mặc định (khi người dùng không nói gì):

- Kỳ này: từ `hôm nay − 10 ngày` đến `hôm nay − 4 ngày` (7 ngày)
- Kỳ trước: từ `hôm nay − 17 ngày` đến `hôm nay − 11 ngày` (7 ngày liền trước)

Nếu người dùng nói "tháng" thì dùng 28 ngày cho mỗi kỳ, giữ nguyên độ trễ 4 ngày. Nếu người dùng đưa ngày cụ thể thì tôn trọng, nhưng cảnh báo nếu kỳ này chạm vào 3 ngày gần nhất.

Lấy ngày hôm nay bằng `date +%F` chứ đừng tự suy đoán.

Dùng cùng một khoảng ngày cho cả GSC và GA4 để phần ghép dữ liệu có ý nghĩa.

## Bước 1 — Kéo dữ liệu GSC

Gọi song song khi có thể:

1. `get_performance_overview` — tổng quan kỳ này
2. `compare_search_periods` — so sánh 2 kỳ, lấy cả cấp query và cấp page
3. `get_search_analytics` với chiều `query`, lấy top 100 kỳ này
4. `get_search_analytics` với chiều `page`, lấy top 50 kỳ này

Giới hạn số dòng như trên. Đừng kéo vài nghìn hàng thô vào context — tốn token mà không cải thiện kết luận.

## Bước 2 — Kéo dữ liệu GA4

Dùng `run_report` trên `GA4_PROPERTY`:

**Report A — theo landing page**

- dimensions: `landingPagePlusQueryString`, `sessionDefaultChannelGroup`
- metrics: `sessions`, `engagementRate`, `averageSessionDuration`, `keyEvents`
- filter: `sessionDefaultChannelGroup` = `Organic Search`
- limit: 50, sắp xếp theo `sessions` giảm dần

**Report B — theo kênh (để đặt organic vào bối cảnh)**

- dimensions: `sessionDefaultChannelGroup`
- metrics: `sessions`, `engagementRate`, `keyEvents`
- so sánh cả 2 kỳ

Nếu metric `keyEvents` bị từ chối, thử lại với `conversions`. Nếu cả hai đều lỗi, bỏ cột conversion và ghi rõ trong báo cáo là property chưa cấu hình key event — đừng bịa số.

## Bước 3 — Ghép dữ liệu

Nối GSC page với GA4 landing page. Lưu ý chuẩn hoá trước khi so khớp:

- GSC trả URL tuyệt đối (`https://www.citeflow.io/pricing`), GA4 trả đường dẫn tương đối (`/pricing`)
- Bỏ query string và dấu `/` cuối khi so khớp
- Ghi lại số trang không khớp được; nếu trên 30% thì báo động, thường là do property GSC dạng URL-prefix bỏ sót subdomain

## Bước 4 — Phân tích

Bốn phần, theo đúng thứ tự này. Mỗi phát hiện phải kèm con số và một việc cần làm cụ thể — không viết "cần tối ưu nội dung" chung chung.

### 4.1 Tăng trưởng & xu hướng

Tổng click, impression, CTR, vị trí trung bình, kèm % thay đổi so với kỳ trước. Query mới nổi (kỳ trước không có, kỳ này lọt top 50). Nhận định ngắn: đang tăng nhờ đâu, hay chỉ là dao động mùa vụ.

### 4.2 Cơ hội hành động

Ba loại, xếp theo click tiềm năng thu được:

- **CTR thấp bất thường**: impression ≥ 300, vị trí ≤ 10, CTR thấp hơn ít nhất 30% so với CTR trung vị của các query cùng khoảng vị trí. → sửa title/meta description.
- **Sắp lên trang 1**: vị trí trung bình 11–20, impression ≥ 200. → bổ sung nội dung, internal link.
- **Nội dung bị SEO bỏ quên**: GA4 engagement rate cao (top 25%) nhưng GSC impression thấp. → trang tốt mà Google chưa hiểu chủ đề, cần tối ưu on-page.

Với mỗi mục ước lượng số click có thể thu thêm, dùng CTR trung bình theo vị trí làm mốc, và nói rõ đó là ước lượng.

### 4.3 Cảnh báo sụt giảm

- Query tụt trên 3 bậc **và** mất trên 20% click (cả hai điều kiện, tránh nhiễu)
- Trang mất trên 30% click
- Trang từng có traffic mà kỳ này biến mất hoàn toàn

Với 5 URL tụt mạnh nhất, gọi `inspect_url_enhanced` để kiểm tra có phải vấn đề index không. Đây là bước phân biệt "Google phạt/lỗi kỹ thuật" với "đối thủ vượt lên" — đừng bỏ qua.

Bỏ qua các dao động dưới 10 click, đó là nhiễu.

### 4.4 Chất lượng traffic

Organic có mang lại người dùng thật không:

- Engagement rate và conversion của organic so với các kênh khác
- Landing page có nhiều click nhưng engagement rate dưới trung bình site → vấn đề nằm ở trang, không phải ở SEO
- Landing page có conversion tốt nhưng ít traffic → đáng đẩy mạnh

Chỉ ra rõ khi một trang "thắng ở GSC nhưng thua ở GA4" — đây là insight mà nhìn riêng từng công cụ không thấy được.

## Bước 5 — Xuất file

Ghi ra `OUTPUT_DIR/seo-<YYYY-MM-DD>.md` (ngày chạy). Tạo thư mục nếu chưa có.

Cấu trúc file:

```markdown
# Báo cáo SEO — citeflow.io
**Kỳ này:** <ngày> → <ngày> · **So với:** <ngày> → <ngày>

## Tóm tắt
3–5 gạch đầu dòng. Điều quan trọng nhất trước. Có số.

## 1. Tăng trưởng & xu hướng
| Chỉ số | Kỳ này | Kỳ trước | Thay đổi |

## 2. Cơ hội hành động
Bảng xếp theo click tiềm năng, kèm cột "Việc cần làm".

## 3. Cảnh báo sụt giảm
Bảng, kèm kết quả kiểm tra index cho các URL tụt mạnh.

## 4. Chất lượng traffic
Bảng landing page: click (GSC) · session · engagement · conversion (GA4).

## Việc nên làm tuần này
Tối đa 5 việc, xếp theo tác động ÷ công sức. Mỗi việc một dòng, cụ thể đến mức
bắt tay làm được ngay.

---
*Nguồn: GSC + GA4 property 536342158. GSC trễ dữ liệu ~3 ngày.*
```

Viết toàn bộ bằng tiếng Việt. Thuật ngữ chuyên ngành (query, impression, CTR, landing page, engagement rate) giữ nguyên tiếng Anh, đừng dịch gượng ép.

## Bước 6 — Tự kiểm tra

Trước khi báo cáo xong, kiểm lại:

- [ ] Số ở phần tóm tắt có khớp với bảng bên dưới không
- [ ] % thay đổi tính đúng chiều chưa (vị trí giảm là **tốt**, đây là chỗ hay sai nhất)
- [ ] Mọi con số đều có nguồn từ tool call, không có số nào tự suy ra
- [ ] Tỉ lệ ghép GSC↔GA4 có được ghi lại không
- [ ] Mỗi cơ hội và cảnh báo đều có việc cần làm cụ thể
- [ ] File đã ghi thành công, in đường dẫn ra cho người dùng

## Nguyên tắc

**Không bịa số.** Tool nào lỗi thì ghi rõ phần đó thiếu dữ liệu và vì sao. Báo cáo thiếu một mục vẫn tốt hơn báo cáo có số sai.

**Không lặp lại giao diện Google.** Nếu một phát hiện chỉ cần mở GSC lên là thấy, nó không đáng nằm trong báo cáo. Giá trị nằm ở chỗ ghép hai nguồn và ở việc xếp hạng ưu tiên.

**Cẩn thận với suy luận nhân quả.** Traffic giảm trùng thời điểm với một thay đổi không có nghĩa là thay đổi đó gây ra. Nêu giả thuyết kèm cách kiểm chứng, đừng khẳng định.

**Ngắn gọn.** Người đọc cần biết làm gì tiếp theo, không cần đọc lại toàn bộ dữ liệu.
