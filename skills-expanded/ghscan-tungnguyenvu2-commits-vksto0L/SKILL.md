# 🎯 VKS_BOT Agent Skill & Development Guidelines (`docs/skill.md`)

Tệp tin này đóng vai trò là **Bộ kỹ năng chỉ thị (Skill File)** và **Cẩm nang nguyên tắc phát triển bắt buộc** dành riêng cho các AI Agent (như Antigravity) và Lập trình viên khi làm việc trên dự án **VKS_BOT**.

> [!IMPORTANT]
> **LUẬT TỐI CAO CỦA REPOSITORY:**
> Khi thực hiện **BẤT KỲ** sự thay đổi, thêm mới, chỉnh sửa, hoặc xóa bỏ mã nguồn nào trong toàn bộ dự án, AI Agent và Lập trình viên **BẮT BUỘC** phải cập nhật lại thông tin thay đổi vào tệp tin này (`docs/skill.md`) và tệp tin [docs/README.md](file:///c:/Users/Admin/OneDrive/ACK/VKS_BOT/docs/README.md) ngay lập tức để đồng bộ tri thức hệ thống.

---

## 🧭 1. Bản Đồ Ràng Buộc Kiến Trúc (Architecture Constraints)

Mọi chỉnh sửa mã nguồn phải tuân thủ nghiêm ngặt các nguyên tắc thiết kế cốt lõi sau:

### 🧠 Tầng Phân Loại AI (AI & NLP Triage)
*   **100% Generative AI:** Tuyệt đối không phục hồi mô hình học máy truyền thống cục bộ (`logistic_model.pkl` và `vectorizer.pkl` phải giữ nguyên là stubs trống 134 bytes).
*   **Gemma Dual Fallback:** Phải duy trì luồng gọi song song đa luồng (`ThreadPoolExecutor`) lên **Gemma 4 31B-it** (chính) và **Gemma 4 26B-it** (dự phòng khi nghẽn hoặc lỗi API) với thời gian chờ thử lại từ 3s - 4s.
*   **Robust JSON loads:** Mọi hàm xử lý kết quả phân loại từ Gemini API phải đi qua bộ lọc `robust_json_loads` sử dụng regex để tự làm sạch markdown backticks, sửa kiểu dữ liệu Booleans (Python sang JSON), dọn dấu phẩy thừa trước dấu ngoặc đóng và tự động giải cứu các cấu trúc dictionary bị hỏng.

### 🗄️ Tầng Dữ Liệu & Khớp Nối (Database Abstractions)
*   **Database Dialect Adapter:** Tuyệt đối không viết các câu truy vấn SQL cứng phụ thuộc vào một loại CSDL cụ thể. Phải luôn sử dụng lớp trừu tượng [db_adapter.py](file:///c:/Users/Admin/OneDrive/ACK/VKS_BOT/db_adapter.py) để tự động dịch câu lệnh giữa SQLite (Local) và PostgreSQL (Render/Actions):
    *   Sử dụng `%s` hoặc `?` thông qua hàm chuyển đổi dialect.
    *   Hỗ trợ `ON CONFLICT DO NOTHING` (Postgres) vs `INSERT OR IGNORE` (SQLite).
    *   Hỗ trợ `NOW()` (Postgres) vs `datetime('now')` (SQLite).
*   **Table Cloning Engine:** Giữ nguyên vẹn cơ chế tự động nhân bản bảng động (`raw_articles_clone`, `classified_articles_clone`...) trong [db_adapter_github.py](file:///c:/Users/Admin/OneDrive/ACK/VKS_BOT/db_adapter_github.py) khi chạy CI với biến môi trường `DB_CLONE_MODE="true"`. Không để dữ liệu chạy CI đè lên các bảng thật của môi trường Production.
*   **Đồng bộ SQLite qua Telegram:** Giữ nguyên cơ chế lưu trữ SQLite không máy chủ (`telegram_db_storage.py`) thông qua việc tải database lên và kéo database về từ tin nhắn ghim trên Telegram.

### 📡 Tầng Thu Thập Tin Tức (Crawlers & Scrapers)
*   **Bypass SSL & Cookie:** Duy trì việc bọc requests bằng `LegacySSLAdapter` để chấp nhận chứng chỉ SSL cũ của các trang tin nhà nước, cùng cơ chế tự giải quyết Cookie `D1N` của Báo Lao Động.
*   **Bypass WAF (Web Application Firewall):**
    *   *Selective Proxy Routing:* Khi chạy trên môi trường CI (hoặc các mạng bị chặn), phải tự động định tuyến các domain nhà nước (`hanoimoi.vn`, `kinhtemoitruong.vn`, `qdnd.vn`...) qua dải IP proxy dân dụng Việt Nam (`VIETNAM_PROXY`).
    *   *Google Web Cache Fallback:* Tự động bọc URL qua dịch vụ Google Cache Proxy khi kết nối trực tiếp hoặc qua proxy thường bị trả về mã lỗi không phải `200`.
    *   *Smart Fallback Extractor:* Phải luôn giữ bộ bóc tách dự phòng thông minh dựa trên thẻ liên kết `<a>` và khoảng cách văn bản lân cận để cứu hộ cào HTML DOM khi giao diện web nguồn thay đổi hoàn toàn.

---

## 🛠️ 2. Hướng Dẫn Phát Triển Chi Tiết (Development & Editing Rules)

Khi chỉnh sửa bất kỳ module nào, AI Agent và Lập trình viên phải tuân theo các chỉ thị kỹ thuật cụ thể dưới đây:

### 🔴 Quy tắc chỉnh sửa Mã Nguồn Python
1.  **Thread-Safe Logging:** Tuyệt đối không dùng hàm `print()` mặc định trong các hàm đa luồng (như crawlers RSS). Bắt buộc phải dùng hàm `safe_print` sử dụng `threading.Lock` để tránh đè chữ.
2.  **Postgres Connection Handling:** Khi mở kết nối PostgreSQL, luôn bọc trong khối lệnh `try...except psycopg2.Error` kèm theo thiết lập TCP Keepalives và Connection Timeout (15 giây) để tránh treo luồng trên môi trường mạng WAN không ổn định. Bắt buộc sử dụng `SAVEPOINT` khi chèn dữ liệu lô lớn để cô lập dòng lỗi.
3.  **PyQt UI State Handling:** Khi thay đổi giao diện [post_verifier_ui.py](file:///c:/Users/Admin/OneDrive/ACK/VKS_BOT/post_verifier_ui.py), phải đảm bảo các tiến trình cào tin hoặc gọi AI chạy ẩn trên `QThread` độc lập, tránh gây đơ/treo luồng giao diện chính (Main GUI Thread).

### 🟢 Quy tắc bảo mật & Bảo trì chất lượng mã
4.  **Bảo mật thông tin nhạy cảm:** Tuyệt đối **không được hardcode** API Keys, Tokens, Passwords, hoặc URL database (như `GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `DATABASE_URL`) vào bất kỳ file mã nguồn nào. Mọi thông tin bảo mật phải được lấy từ biến môi trường (`os.getenv`).
5.  **Kiểm thử trước khi bàn giao:** Khi sửa đổi code crawler hoặc Database Adapter, AI Agent bắt buộc phải chạy các kịch bản kiểm thử giả lập hoặc tạo file script test độc lập trong thư mục `scratch/` để kiểm tra lỗi cú pháp và ngoại lệ trước khi bàn giao.
6.  **Đóng gói lỗi & Đảm bảo kết nối:** Mọi yêu cầu kết nối mạng hoặc gọi API bên ngoài bắt buộc phải cấu hình `timeout` rõ ràng (tối đa 15 giây) và được bao bọc bởi khối lệnh `try...except Exception`. Khi luồng cào tin bị lỗi đơn lẻ, hệ thống phải ghi log cảnh báo và tiếp tục xử lý các phần khác, không được làm sập toàn bộ tiến trình.
7.  **Giữ vững thẩm mỹ giao diện UI:** Duy trì thiết kế giao diện PyQt Admin Dashboard hiện đại, sang trọng (Premium Dark Mode, căn lề đồng đều, nút bấm hover mượt mà) và giải phóng mọi luồng xử lý chạy ngầm khi đóng cửa sổ ứng dụng.

### 🟡 Quy tắc chỉnh sửa Tài Liệu (`docs/`)
8.  **Tính Nhất Quán:** Mọi tính năng mới được đưa vào code phải được mô tả chi tiết cả về kiến trúc lẫn quy trình hoạt động trong [docs/README.md](file:///c:/Users/Admin/OneDrive/ACK/VKS_BOT/docs/README.md).
9.  **Định dạng Mermaid:** Khi thay đổi quy trình, hãy cập nhật sơ đồ trạng thái (`stateDiagram-v2`) hoặc sơ đồ khối (`graph TD`) trong tài liệu tương ứng để phản ánh chính xác 100% thực tế.

---

## ⚡ 3. Kỹ Năng Chỉ Định Đặc Biệt Của AI Agent (Specialized Agent Skills)

Để nâng cao khả năng cộng tác và tối ưu chi phí vận hành, AI Agent được cung cấp 02 kỹ năng đặc biệt sau đây:

### 💬 Kỹ năng `/grill-me` (Vấn đáp làm rõ giải pháp)
> [!TIP]
> **KÍCH HOẠT:** Khi người dùng yêu cầu thay đổi kiến trúc hoặc thực hiện các task phức tạp có nhiều nhánh quyết định.
*   **Hành vi của Agent:** 
    *   Agent **tuyệt đối không được code ngay**. Thay vào đó, Agent phải chủ động chất vấn người dùng bằng các câu hỏi ngắn gọn, thực tế nhằm làm rõ: *Đầu ra mong muốn là gì? Có ảnh hưởng đến các module hiện có không? Ràng buộc dữ liệu ra sao?*
    *   Sau khi người dùng trả lời và hai bên thống nhất 100% giải pháp, Agent mới bắt đầu lập kịch bản và thực thi code.
*   **Mục đích:** Đảm bảo tính chính xác ngay từ lần gõ phím đầu tiên, triệt tiêu sai lệch ý đồ thiết kế.

### 🦖 Kỹ năng `/caveman` (Giao tiếp tối giản - Tiết kiệm Token)
> [!TIP]
> **KÍCH HOẠT:** Khi người dùng yêu cầu chuyển sang chế độ `/caveman` để fix code nhanh hoặc refactor hàng loạt tệp tin.
*   **Hành vi của Agent:**
    *   Agent sẽ lược bỏ toàn bộ các câu chào hỏi, cảm ơn, lịch sự xã giao thừa thãi.
    *   Agent chỉ giao tiếp bằng các từ khóa kỹ thuật nén cực gọn, hiển thị trực tiếp sơ đồ hoặc diff code.
*   **Mục đích:** Giảm thiểu tới **75% lượng token** tiêu hao của hội thoại, giúp tốc độ phản hồi nhanh gấp 3 lần và tiết kiệm tối đa chi phí gọi API.

---

## 📝 4. Tiêu Chuẩn Ghi Chép Nhật Ký Thay Đổi & Commit (Conventional Commit & Logging)

Để bảo đảm tính minh bạch, đồng bộ tri thức và dễ dàng theo dõi lịch sử cập nhật của hệ thống, mọi nhà phát triển và AI Agent phải tuân thủ nghiêm ngặt chuẩn định dạng sau:

### ⚙️ 1. Định dạng Thông điệp Commit (Git Commit Message)
Mọi commit đẩy lên Git repository phải tuân theo chuẩn **Conventional Commits**:
```text
<type>(<scope>): <description>

[Optional body explaining the 'why' behind the change]
```
*   **`<type>` bắt buộc phải thuộc danh sách sau:**
    *   `feat`: Thêm một tính năng mới (ví dụ: cào trang tin mới, thêm nút duyệt UI).
    *   `fix`: Sửa lỗi hệ thống (ví dụ: bypass lỗi 403, sửa lỗi cú pháp SQL).
    *   `docs`: Cập nhật tài liệu hướng dẫn (ví dụ: bổ sung `skill.md`, sửa sơ đồ Mermaid).
    *   `refactor`: Cơ cấu lại mã nguồn nhưng không thay đổi tính năng hay sửa lỗi.
    *   `perf`: Cải tiến mã nguồn giúp tối ưu hiệu năng chạy.
*   **`<scope>` chỉ rõ khu vực bị tác động:** `crawler`, `db`, `ui`, `ai`, `pipeline`, `security`.
*   **Ví dụ chuẩn:** `feat(crawler): tích hợp proxy dân dụng việt nam và google cache bypass`

### 📊 2. Ghi nhận Nhật ký Thay đổi (Change Log & Sync Status)
Mỗi khi chỉnh sửa bất kỳ tệp tin nào, bạn phải ghi nhận lại một dòng thông tin chi tiết vào bảng dưới đây để cập nhật trạng thái đồng bộ tri thức:

| Thời gian | Người thực hiện | Các File bị tác động | Mục tiêu & Nội dung thay đổi | Trạng thái đồng bộ `README.md` & `skill.md` |
| :--- | :--- | :--- | :--- | :--- |
| **2026-05-23** | **Antigravity (AI)** | `docs/README.md` | Viết lại toàn bộ cẩm nang mô tả mã nguồn chuyên sâu, dọn dẹp triệt để các phần trùng lặp, chuẩn hóa Mermaid diagram cho cả hai môi trường Local và GitHub Actions CI/CD. | **Đồng bộ 100%** |
| **2026-05-23** | **Antigravity (AI)** | `docs/skill.md` | Khởi tạo và tích hợp 10 luật thực chiến, chuẩn hóa Conventional Commit và bổ sung 02 kỹ năng đặc biệt `/grill-me` và `/caveman`. | **Đồng bộ 100%** |
| **2026-05-24** | **Antigravity (AI)** | `.github/workflows/test_403_rss.yml` | Khởi tạo workflow độc lập kiểm thử bypass WAF 403 cho 3 trang báo bằng 4 phương thức (Direct, Headers, Web Cache, Translate Proxy). | **Đồng bộ 100%** |
| **2026-05-24** | **Antigravity (AI)** | `crawler_db.py`, `crawler_db_github.py`, `docs/README.md`, `docs/skill.md` | Tích hợp bổ sung 96 kênh RSS từ Báo Bảo vệ pháp luật (BVPL) và đồng bộ hóa an toàn sang SQLite cục bộ & PostgreSQL đám mây (Render). | **Đồng bộ 100%** |
| **2026-05-24** | **Antigravity (AI)** | `.github/workflows/test_403_rss.yml`, `docs/skill.md` | Mở rộng targets lên 15 nguồn, cấu hình workflow_dispatch chạy thủ công, xóa bỏ hoàn toàn schedule cron, xử lý lỗi cú pháp thụt lề YAML bằng textwrap.dedent. | **Đồng bộ 100%** |
| **2026-05-24** | **Antigravity (AI)** | `.github/workflows/test_403_rss.yml`, `docs/skill.md` | Nâng cấp kịch bản kiểm thử bypass WAF: Tự động tải targets từ `crawler_data.db` (hoặc `DEFAULT_SOURCES`), tích hợp cơ chế `crawl_rss` (Legacy SSL) và tích hợp Newspaper4k NLP để tóm tắt bài viết mới nhất từ Google Web Cache. | **Đồng bộ 100%** |
| **2026-05-24** | **Antigravity (AI)** | `.github/workflows/test_403_rss.yml`, `docs/skill.md` | Chuyển đổi trích xuất động sang dữ liệu tĩnh: Đọc 160 nguồn RSS từ `crawler_data.db` cục bộ và nhúng trực tiếp dưới dạng từ điển/danh sách Python tĩnh tự chứa trong workflow, kèm cơ chế trích mẫu deterministic thông minh để tối ưu thời gian chạy. | **Đồng bộ 100%** |
| **2026-05-24** | **Antigravity (AI)** | `.github/workflows/test_403_rss.yml`, `docs/skill.md` | Loại bỏ hoàn toàn cơ chế 'Trích Chọn Bộ Mẫu Đại Diện', chuyển sang kiểm thử tuần tự toàn diện qua tất cả 160+ nguồn tin; đồng thời đồng bộ hóa hoàn hảo các tham số headers, timeouts, và logic Google Web Cache giống hệt `test_crawler_github.py`. | **Đồng bộ 100%** |
| **2026-05-24** | **Antigravity (AI)** | `.github/workflows/test_403_rss.yml`, `docs/skill.md` | Khắc phục lỗi `No Entries`: Tự động nhận diện trường hợp WAF trả về trang HTML thử thách có HTTP status 200 (khiến feedparser không đọc được entry nào), từ đó kích hoạt thông minh cơ chế dự phòng Google Web Cache để lấy RSS đầy đủ. | **Đồng bộ 100%** |
| **2026-05-25** | **Antigravity (AI)** | `classifier_api_github.py`, `classifier_hybrid.py`, `docs/skill.md` | Nâng cấp prompt phân loại của mô hình Gemini/Gemma để mở rộng và chi tiết hóa 12 lĩnh vực bảo vệ dân sự công ích theo tinh thần mới, đồng bộ đồng thời cho cả môi trường Local và GitHub Actions CI/CD. | **Đồng bộ 100%** |
| **2026-05-26** | **Antigravity (AI)** | `migrate_sqlite_to_postgres.py`, `docs/skill.md` | Giải quyết lỗi đụng độ khóa chính `id` khi đồng bộ lên Postgres bằng giải thích cơ chế, đồng thời bổ sung hàm `migrate_pg_to_sqlite()` để kéo dữ liệu từ Postgres Cloud về đè/đồng bộ SQLite cục bộ (lấy Cloud làm gốc) kèm menu chọn hướng tương tác. | **Đồng bộ 100%** |
| **2026-05-26** | **Antigravity (AI)** | `migrate_sqlite_to_postgres.py`, `docs/skill.md` | Khắc phục lỗi `canceling statement due to statement timeout` bằng cách tăng timeout lên 10 phút, tự động `rollback()` giao dịch Postgres khi có lỗi để tránh nghẽn luồng liên đới, và thiết kế cơ chế giao dịch an toàn (chỉ xóa và ghi đè SQLite khi tải dữ liệu Postgres thành công). | **Đồng bộ 100%** |
| **2026-05-27** | **Antigravity (AI)** | `non_rss_scraper.py`, `non_rss_scraper_github.py`, `run_pipeline_local.py`, `docs/README.md`, `docs/skill.md` | Tích hợp script điều phối pipeline local (`run_pipeline_local.py`) chạy cào dữ liệu, phân loại AI, đồng bộ Postgres hằng ngày; nâng cấp hệ thống logs trực quan bằng icon status cho cả bản local (`non_rss_scraper.py`) và bản GitHub Actions (`non_rss_scraper_github.py`) kèm báo cáo lỗi tổng kết ở cuối đợt chạy. | **Đồng bộ 100%** |
| **2026-05-29** | **Antigravity (AI)** | `crawl_congdanso.py`, `classifier_hybrid.py`, `run_pipeline_local.py`, `docs/skill.md`, `docs/README.md` | Tích hợp trực tiếp dữ liệu cào từ Cổng Dân Số iHanoi vào CSDL thô (`raw_articles`), nâng cấp Prompt phân loại AI (Gemma 4 31B/26B) để đánh giá Kết quả xử lý hành chính theo NQ 205, và tự động hóa toàn bộ luồng cào-phân loại trong `run_pipeline_local.py`. | **Đồng bộ 100%** |
| **2026-05-29** | **Antigravity (AI)** | `classifier_hybrid.py`, `crawl_congdanso.py`, `run_pipeline_local.py`, `docs/skill.md`, `docs/README.md` | Tối ưu bộ cào iHanoi bằng cơ chế check CSDL để tự động bỏ qua các bài đã trùng trước khi cào chi tiết; sửa đổi `robust_json_loads` để bảo vệ nháy đơn trong văn bản Tiếng Việt; dọn dẹp lỗi double-spacing trong `classifier_hybrid.py`; cấu hình lượng trang cào mặc định lên 20 trang để bao phủ trọn vẹn 5 ngày gần nhất. | **Đồng bộ 100%** |
| **2026-05-29** | **Antigravity (AI)** | `spatial_analyzer.py`, `crawler_db.py`, `run_pipeline_local.py`, `post_verifier_ui.py`, `docs/skill.md`, `docs/README.md` | Triển khai toàn bộ **Spatial Triage Pipeline**: (1) Mở rộng schema `matched_cases` với 5 cột địa lý + self-healing migration; (2) Module `spatial_analyzer.py` dùng **Gemini 2.5 Flash Lite + Google Search Grounding** (miễn phí) để geocode, thuật toán **Haversine** đo khoảng cách thực mét, gom cụm điểm nóng bán kính 150m; (3) Bước 4.5 trong `run_pipeline_local.py` + cảnh báo Telegram tự động khi phát hiện hotspot; (4) Tab **"🗺️ Bản đồ Điểm nóng"** trong Dashboard dùng Leaflet.js (OpenStreetMap, miễn phí) với vòng tròn đỏ cảnh báo + API `/api/hotspots`; (5) Tab **"📋 iHanoi / Cổng Dân Số"** lọc riêng các phản ánh từ nguồn congdanso. | **Đồng bộ 100%** |
| **2026-05-29** | **Antigravity (AI)** | `post_verifier_ui.py`, `docs/skill.md` | Hoàn thiện 3 nâng cấp quan trọng cho iHanoi: (1) Cách ly quy trình duyệt iHanoi ra khỏi tab chờ duyệt chung, biến tab iHanoi thành nơi kiểm duyệt độc lập cho congdanso; (2) Tự động hóa đồng bộ bản đồ real-time, tô điểm marker đơn lẻ iHanoi bằng màu xanh Cyan neon phát sáng cực sang trọng, đính kèm đầy đủ popup chi tiết và nút Google Maps tiện lợi; (3) Gửi tọa độ địa lý thông qua Telegram Alert cho các bài viết thuộc nguồn congdanso/iHanoi kèm link định vị Google Maps một chạm. | **Đồng bộ 100%** |
| **2026-05-30** | **Antigravity (AI)** | `crawl_congdanso.py`, `docs/skill.md`, `docs/README.md` | Tích hợp cơ chế Dừng Cào Sớm (Early Stopping) dựa trên cửa sổ trượt 10 trang gần nhất (nếu >= 2 trang chứa tin trùng trong CSDL thì dừng), đồng thời nâng cấp so khớp địa bàn 12 phường mục tiêu không phân biệt dấu tiếng Việt (accent-insensitive) và chữ hoa chữ thường. | **Đồng bộ 100%** |
| **2026-06-01** | **Antigravity (AI)** | `post_verifier_ui.py`, `docs/skill.md` | Tích hợp cơ chế sao chép báo cáo vào Clipboard (đơn lẻ & hàng loạt) bằng plain text có cấu trúc, tích hợp geocode iHanoi với bản đồ Google Maps, tự động loại bỏ tag AI, và khắc phục lỗi `.get()` của đối tượng `sqlite3.Row` trên Flask API. | **Đồng bộ 100%** |

---

## 💡 Mẹo đọc nhanh dành cho AI Agent thế hệ tiếp theo
> Khi nhận được một task phát triển/sửa lỗi từ người dùng:
> 1. Sử dụng công cụ `view_file` with cờ `IsSkillFile: true` để đọc tệp tin [docs/skill.md](file:///c:/Users/Admin/OneDrive/ACK/VKS_BOT/docs/skill.md) này trước tiên.
> 2. Đọc tệp tin [docs/README.md](file:///c:/Users/Admin/OneDrive/ACK/VKS_BOT/docs/README.md) để nắm toàn bộ cấu trúc các file.
> 3. Tiến hành code theo đúng các ràng buộc kiến trúc ở Mục 1 và Hướng dẫn ở Mục 2.
> 4. Tự động áp dụng linh hoạt 2 kỹ năng đặc biệt ở Mục 3 dựa trên ngữ cảnh trò chuyện.
> 5. Sau khi hoàn thành và kiểm thử, cập nhật lại cả [docs/README.md](file:///c:/Users/Admin/OneDrive/ACK/VKS_BOT/docs/README.md) và Mục 4 của tệp tin này trước khi kết thúc task.
