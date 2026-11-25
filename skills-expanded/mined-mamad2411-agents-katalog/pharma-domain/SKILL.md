---
name: pharma-domain
description: >
  Domain-specific guidance, business terminology, workflow definitions, state transition models, and business invariants for the PharmaBranch pharmacy branch management system, ensuring rigorous domain reasoning without inventing unsupported business rules or mandating technical implementations.
---

# SKILL 11 — PHARMA DOMAIN

## 1. Objective & Domain Scope

### 1.1. Objective
Skill này thiết lập chuẩn mực phương pháp luận và hướng dẫn chuyên biệt về nghiệp vụ dược (**Domain-Specific Guidance & Business Reasoning**) cho hệ thống quản lý chuỗi nhà thuốc đa chi nhánh **PharmaBranch**.

Mục tiêu cốt lõi của Skill 11 là giúp Agent:
1. **Hiểu đúng bản chất nghiệp vụ (Understand Domain Semantics):** Nắm vững ý nghĩa thực tế của các thực thể, thuật ngữ, quy trình và ràng buộc trong ngành bán lẻ dược phẩm đa chi nhánh.
2. **Phân tích và suy luận miền đúng đắn (Analyze & Reason Rigorously):** Suy luận logic nghiệp vụ dựa trên bằng chứng vật lý và đặc tả chính thức, loại trừ hoàn toàn việc tự suy diễn hoặc áp đặt các quy định pháp lý / y tế không được dự án phê duyệt.
3. **Thiết kế và triển khai chuẩn mực (Design & Implement Accurately):** Xây dựng mô hình nghiệp vụ, luồng công việc (workflows), và máy trạng thái (state machines) phản ánh chính xác yêu cầu dự án.
4. **Kiểm thử và xác minh toàn vẹn (Test & Verify Domain Integrity):** Nhận diện các bất biến nghiệp vụ (business invariants) và ca kiểm thử nghiệp vụ then chốt (boundary conditions, state transitions, consistency).
5. **Tái cấu trúc an toàn (Refactor Safely):** Phân biệt hành vi ngẫu nhiên của code (accidental implementation artifacts) với quy tắc nghiệp vụ chủ đích (intentional business rules), tránh làm sai lệch ngữ nghĩa kinh doanh khi tối ưu hóa mã nguồn.

### 1.2. Scope & Governance Boundary
Skill 11 là một **DOMAIN SKILL** (Kỹ năng chuyên môn về Miền nghiệp vụ). Skill 11:
- **SỞ HỮU (OWNS):** Diễn giải miền nghiệp vụ, khái niệm thực thể, mối quan hệ nghiệp vụ, bất biến kinh doanh, quy trình nghiệp vụ, máy trạng thái, điều kiện biên, ngoại lệ nghiệp vụ và khả năng truy vết nghiệp vụ.
- **TUYỆT ĐỐI KHÔNG SỞ HỮU HOẶC THAY THẾ (DOES NOT OWN OR REPLACE):**
  - Quản trị dự án: `Rule 00` (Project Governance).
  - Kiến trúc hệ thống: `Rule 01` (Architecture).
  - Chất lượng giao dịch, đồng thời và chữ ký số: `Rule 02` (Architecture Quality).
  - An ninh hệ thống và mật mã: `Rule 03` (Security).
  - Mô hình phân quyền: `Rule 04` (RBAC Model).
  - Thực thi kiểm soát truy cập runtime: `Rule 05` (Authorization Enforcement).
  - Cô lập dữ liệu chi nhánh và RLS: `Rule 06` (Branch Isolation).
  - Toàn vẹn cơ sở dữ liệu và ràng buộc SQL: `Rule 07` (Database Integrity).
  - Hợp đồng API và chuẩn giao tiếp: `Rule 08` (API Contract).
  - Khả năng quan sát và vận hành: `Rule 09` (Observability & Operations).
  - Kỹ năng kỹ thuật: `Skill 01` đến `Skill 10`.

Skill 11 định nghĩa **Ý NGHĨA KINH DOANH (WHAT IT MEANS TO THE BUSINESS)**, không áp đặt công nghệ triển khai hoặc cơ chế bảo mật kỹ thuật.

---

## 2. Evidence-First Domain Principle

### 2.1. Phân định mười bốn khía cạnh thực tế (Fourteen Reality Facets)
Theo nguyên tắc **Evidence > Assumption**, Agent bắt buộc phải phân định minh bạch 14 khía cạnh khi tiếp cận hoặc đánh giá bất kỳ chức năng nào:

1. **Business Requirement (Yêu cầu nghiệp vụ):** Nhu cầu cốt lõi được mô tả tường minh bởi khách hàng hoặc bài toán đồ án tốt nghiệp.
2. **Business Policy (Chính sách nghiệp vụ):** Quy tắc vận hành tổ chức (ví dụ: chính sách đổi trả trong vòng 48h, chính sách chiết khấu, chính sách kiểm kê).
3. **Domain Rule (Quy tắc miền):** Logic nghiệp vụ quyết định tính hợp lệ của một hành động (ví dụ tham khảo: đơn thuốc yêu cầu thông tin người kê đơn khi có quy định áp dụng).
4. **Business Invariant (Bất biến nghiệp vụ):** Điều kiện nghiệp vụ cần được bảo toàn trong mọi trạng thái bền vững của miền dữ liệu (ví dụ tham khảo: tồn kho khả dụng không được âm, tổng tiền hóa đơn phải khớp tổng chi tiết dòng khi được quy định trong business specification).
5. **Workflow Definition (Định nghĩa quy trình):** Chuỗi các bước nghiệp vụ liên kết từ khởi tạo đến hoàn tất.
6. **State Transition Definition (Định nghĩa chuyển trạng thái):** Bản đồ quy định trạng thái hiện tại, hành động hợp lệ, điều kiện tiên quyết và trạng thái kế tiếp.
7. **Approved Architecture (Kiến trúc được phê duyệt):** Cấu trúc phân tầng và phân định trách nhiệm đã được quy định trong Rules 00–09.
8. **ERD / Data Model (Sơ đồ dữ liệu):** Thiết kế quan hệ thực thể, phản ánh cấu trúc lưu trữ dự kiến.
9. **API Contract (Hợp đồng API):** Giao diện trao đổi dữ liệu công khai giữa Client và Server.
10. **UI Behavior (Hành vi giao diện người dùng):** Trải nghiệm hiển thị, luồng nhập liệu và điều hướng trên Web/Mobile.
11. **Physical Implementation (Mã nguồn triển khai vật lý):** Code thực tế đang tồn tại trong controller, service, repository, database script.
12. **Automated Test Evidence (Bằng chứng kiểm thử tự động):** Các ca kiểm thử unit, integration, end-to-end đang chạy và kiểm chứng logic.
13. **Runtime Evidence (Bằng chứng thời gian chạy):** Nhật ký log, database records, audit trail ghi nhận hành vi khi hệ thống vận hành.
14. **Assumption (Giả định):** Suy đoán chủ quan của Agent khi chưa có bằng chứng xác thực.

### 2.2. Quy tắc cấm suy diễn (Non-Inference Rules)
Agent tuyệt đối **KHÔNG ĐƯỢC** đồng nhất các khái niệm sau:
- `ERD = implemented business rule`: Có bảng hoặc cột trong ERD không chứng minh logic nghiệp vụ đã được thực thi.
- `UI = backend business rule`: Nút bị ẩn, trường bị disabled hoặc validate form trên React/Flutter không chứng minh backend có quy tắc tương ứng.
- `API = domain truth`: API endpoint tồn tại không đồng nghĩa với việc nó phản ánh toàn bộ sự thật nghiệp vụ của domain.
- `Documentation = implementation proof`: Tài liệu mô tả không phải bằng chứng rằng mã nguồn đã hiện diện.
- `Test = complete business correctness`: Một test case pass chỉ chứng minh kịch bản cụ thể đó pass, không chứng minh toàn bộ nghiệp vụ đã hoàn hảo.
- `Absence of code evidence = business rule does not exist`: Không tìm thấy code có thể do tính năng chưa được cài đặt, không có nghĩa là quy tắc nghiệp vụ không tồn tại trong yêu cầu đề tài.

### 2.3. Hệ thống phân loại trạng thái bằng chứng (Evidence Status Distinctions)
Mọi kết luận đánh giá nghiệp vụ phải bảo toàn 4 cặp trạng thái chuẩn mực:
```text
NOT FOUND      ≠ NOT IMPLEMENTED
NOT VERIFIED   ≠ FAIL
PROPOSED       ≠ IMPLEMENTED
IMPLEMENTED    ≠ VERIFIED
```
- **NOT FOUND:** Không tìm thấy tài liệu hoặc mã nguồn tại vị trí đang kiểm tra (nhưng có thể nằm ở nơi khác hoặc đang được yêu cầu).
- **NOT IMPLEMENTED:** Xác nhận bằng chứng vật lý rằng chức năng chưa được lập trình.
- **NOT VERIFIED:** Tính năng có mã nguồn nhưng chưa được kiểm chứng runtime hoặc chưa chạy automated test.
- **FAIL:** Đã kiểm chứng thực tế và phát hiện lỗi sai lệch so với đặc tả.
- **PROPOSED:** Bản thiết kế hoặc đề xuất mới, chưa áp dụng vào codebase.
- **IMPLEMENTED:** Mã nguồn đã tồn tại trong repository.
- **VERIFIED:** Mã nguồn đã tồn tại VÀ đã vượt qua bộ kiểm thử xác minh độc lập.

Khi có xung đột giữa các nguồn thông tin, Agent phải ghi nhận rõ mâu thuẫn và truy vết về nguồn có độ ưu tiên cao hơn.

---

## 3. Priority Hierarchy

Khi phân tích, thiết kế hoặc giải quyết bất kỳ bài toán miền nào, Agent phải tuân thủ nghiêm ngặt thứ tự ưu tiên sau:

```text
1. Rules 00–09 (Governing Architectural & Security Rules)
   ↓
2. Explicit task requirements (Yêu cầu trực tiếp từ prompt của người dùng)
   ↓
3. Approved business/domain requirements (Đặc tả nghiệp vụ đã được phê duyệt)
   ↓
4. Approved architecture (Tài liệu kiến trúc chính thức)
   ↓
5. Existing repository conventions and implementation evidence (Mã nguồn thực tế)
   ↓
6. Existing API/database contracts (Hợp đồng API & Schema cơ sở dữ liệu hiện có)
   ↓
7. Existing tests (Bộ kiểm thử hiện hành)
   ↓
8. Project documentation / ERD / diagrams (Tài liệu mô tả, sơ đồ thiết kế)
   ↓
9. Generic pharmacy knowledge (Kiến thức dược phẩm / bán lẻ tổng quát ngoài đời)
   ↓
10. Agent assumptions (Giả định chủ quan của Agent)
```

> [!CAUTION]
> **Kiến thức dược thực tế không được ghi đè yêu cầu dự án:**
> Tri thức tổng quát về ngành dược (GPP, quy chế kê đơn Bộ Y Tế, bảo quản lạnh, hạn dùng) chỉ đóng vai trò tham khảo ngữ cảnh. Nếu dự án PharmaBranch không yêu cầu hoặc có định nghĩa tinh giản, Agent **KHÔNG ĐƯỢC** tự ý áp đặt các quy định pháp luật phức tạp vào hệ thống.
> Nếu một khái niệm chưa rõ ràng trong hồ sơ dự án, phải gắn nhãn: `UNKNOWN`, `ASSUMPTION`, `PROPOSED`, hoặc `NEEDS BUSINESS CONFIRMATION`.

---

## 4. Technology Neutrality

Skill 11 mô tả ngữ nghĩa miền nghiệp vụ hoàn toàn độc lập với công nghệ lập trình và framework:
- **KHÔNG BẮT BUỘC:** Entity Framework Core, Dapper, ADO.NET, hay bất kỳ ORM cụ thể nào.
- **KHÔNG BẮT BUỘC:** ASP.NET Core, ReactJS, Flutter, Next.js, Redux, Riverpod, BLoC, MediatR.
- **KHÔNG BẮT BUỘC:** Clean Architecture, Hexagonal Architecture, CQRS, Event Sourcing, hay Repository Pattern.
- **ĐỘC LẬP VỚI ENGINE:** Logic nghiệp vụ (ví dụ: trừ tồn kho, tính tiền chiết khấu) là chân lý miền, không phụ thuộc vào việc tính toán diễn ra trong SQL Stored Procedure, C# Domain Service, hay TypeScript utility.

Các chi tiết kỹ thuật trên thuộc quyền sở hữu của các Skills công nghệ (`Skill 03`, `Skill 04`, `Skill 05`, `Skill 07`) và các Rules kiến trúc (`Rule 01`, `Rule 02`).

---

## 5. Domain Ownership Model

### 5.1. Những gì Skill 11 SỞ HỮU (Owns)
- **Domain Terminology:** Định nghĩa chuẩn hóa các thuật ngữ nghiệp vụ (Thuốc, Lô, Hạn dùng, Toa thuốc, Phiếu nhập, v.v.).
- **Domain Concepts & Entity Meaning:** Ý nghĩa kinh doanh của từng thực thể, tránh nhầm lẫn giữa khái niệm danh mục và hàng hóa thực tế.
- **Business Relationships:** Bản chất mối quan hệ nghiệp vụ giữa Chi nhánh, Nhân viên, Thuốc, Tồn kho, Hóa đơn, Khách hàng, Nhà cung cấp.
- **Business Invariants:** Các bất biến nghiệp vụ bảo vệ tính toàn vẹn của nghiệp vụ dược.
- **Workflows:** Các bước tiến hành quy trình bán hàng, nhập hàng, đổi trả, kiểm kê.
- **State Transition Models:** Máy trạng thái hợp lệ và bất hợp lệ của đơn hàng, hóa đơn, phiếu nhập, thanh toán.
- **Domain Constraints & Actors:** Vai trò tham gia nghiệp vụ và giới hạn quyền hạn theo góc nhìn nghiệp vụ.
- **Domain Exceptions:** Các tình huống lỗi nghiệp vụ (hết hàng, thuốc hết hạn, đơn hàng đã hủy, v.v.).
- **Domain Traceability:** Khả năng truy vết từ yêu cầu nghiệp vụ đến kiểm thử.

### 5.2. Những gì Skill 11 KHÔNG SỞ HỮU (Does NOT Own)
- Cơ chế xác thực JWT, session context (`Rule 03`).
- Cơ chế thực thi RBAC và Authorization kỹ thuật (`Rule 04`, `Rule 05`).
- Cơ chế kỹ thuật của SQL Server Row-Level Security (RLS) (`Rule 06`, `Rule 07`).
- Cú pháp câu lệnh SQL, Index, Foreign Key script (`Skill 07`).
- Thiết kế URI, HTTP method, DTO casing, Problem Details (`Rule 08`, `Skill 06`).
- Quản lý state frontend, giao diện UI component (`Skill 04`, `Skill 05`).
- Hạ tầng logging Serilog, Prometheus, Health Checks (`Rule 09`).
- Quy trình triển khai Docker, CI/CD, Backup/Restore (`Rule 02`, `Rule 09`).

---

## 6. PharmaBranch Domain Context

Hệ thống **PharmaBranch** được mô hình hóa là hệ thống quản lý chuỗi nhà thuốc đa chi nhánh phục vụ bán lẻ dược phẩm, thiết bị y tế và chăm sóc sức khỏe.

Các phân hệ nghiệp vụ chính bao gồm:
- **Quản lý Chi nhánh (Branch Management):** Quản lý thông tin mạng lưới chi nhánh, thiết lập giới hạn kinh doanh theo từng địa điểm.
- **Quản lý Nhân sự Chi nhánh (Branch Staff & Management):** Quản lý nhân sự làm việc tại chi nhánh (Chủ nhà thuốc/Quản lý, Dược sĩ bán thuốc, Thủ kho).
- **Danh mục Dược phẩm (Medicine Catalog):** Quản lý định danh thuốc, hoạt chất, đường dùng, đơn vị tính, quy cách đóng gói.
- **Quản lý Lô & Hạn dùng (Batch / Lot & Expiration):** Theo dõi số lô sản xuất, ngày hết hạn và xuất xứ hàng hóa.
- **Quản lý Kho & Tồn kho (Inventory & Warehouse):** Kiểm soát số lượng khả dụng, điều chỉnh tồn kho, kiểm kê, lịch sử biến động kho.
- **Quản lý Mua hàng & Nhập kho (Procurement & Receiving):** Mua hàng từ nhà cung cấp, tiếp nhận hàng, lập phiếu nhập kho.
- **Quản lý Bán hàng & Hóa đơn (Sales & Invoicing):** Bán lẻ tại quầy, xuất hóa đơn, trừ tồn kho, ký số hóa đơn điện tử (nếu có yêu cầu).
- **Quản lý Thanh toán (Payment):** Đa dạng phương thức thanh toán (tiền mặt, chuyển khoản, ví điện tử), đối soát giao dịch.
- **Quản lý Đổi trả (Returns & Refunds):** Tiếp nhận thuốc đổi trả, kiểm định khả năng nhập lại kho hoặc hủy bỏ, xử lý hoàn tiền.
- **Quản lý Khách hàng & Toa thuốc (Customer & Prescription):** Lưu trữ thông tin khách hàng, lịch sử mua thuốc, liên kết đơn thuốc do bác sĩ kê đơn.
- **Quản trị & Nhật ký Kiểm toán (Audit & Administration):** Ghi vết các thao tác trọng yếu đảm bảo tính minh bạch.

> [!NOTE]
> Không suy diễn rằng toàn bộ các phân hệ trên đều đã được code hoàn thiện. Mọi khái niệm phải được truy vết:
> `Requirement → Domain Concept → Data Model → API → UI → Implementation → Test`.

---

## 7. Domain Actors

Trong góc nhìn nghiệp vụ, Actor là người hoặc hệ thống tham gia vào quy trình kinh doanh. Cần phân định rạch ròi 3 khái niệm:
- **Actor:** AI tham gia vào tiến trình kinh doanh (WHO).
- **RBAC:** Quyền hạn nghiệp vụ được gán cho vai trò của Actor (`Rule 04`).
- **Authorization:** Cơ chế kỹ thuật kiểm soát và chặn truy cập phía server (`Rule 05`).

Các Actor chính trong hệ thống PharmaBranch (Vai trò và trách nhiệm tham chiếu miền nghiệp vụ; quyền hạn thực tế thuộc sở hữu của `Rule 04`, `Rule 05` và `Skill 12`):
1. **Pharmacy Owner / Branch Manager (Chủ nhà thuốc / Quản lý chi nhánh - Vai trò quản trị tham chiếu):**
   - Giám sát hoạt động kinh doanh, nhân sự, kho bãi và tài chính của chi nhánh theo phân công.
   - Thẩm quyền phê duyệt (như điều chỉnh tồn kho, đơn hủy, hoặc chi phí chi nhánh) mang tính chất tham chiếu nghiệp vụ; quyền hạn chính thức phải được xác nhận theo ma trận quyền được duyệt (`Rule 04` / `Skill 12`).
   - Xem báo cáo tổng hợp doanh thu, lợi nhuận, biến động kho thuộc phạm vi chi nhánh.
2. **Sales Staff / Pharmacist (Nhân viên bán lẻ / Dược sĩ tư vấn):**
   - Trực tiếp tiếp xúc khách hàng, tra cứu danh mục thuốc, kiểm tra tồn kho khả dụng.
   - Tạo đơn bán hàng, lập hóa đơn, thu tiền, in hóa đơn cho khách theo quy trình bán lẻ.
   - Tiếp nhận yêu cầu đổi trả hàng từ khách hàng trong phạm vi thẩm quyền được cấp.
3. **Warehouse Staff (Nhân viên quản lý kho):**
   - Tiếp nhận hàng giao từ Nhà cung cấp theo đơn nhập hàng.
   - Kiểm đếm thực tế, đối soát số lô, hạn dùng, lập phiếu nhập kho.
   - Thực hiện kiểm kê định kỳ, báo cáo chênh lệch tồn kho và đề xuất xử lý thuốc hết hạn theo phân công.
4. **Customer / Patient (Khách hàng / Người bệnh):**
   - Đối tượng thụ hưởng sản phẩm và dịch vụ tư vấn.
   - Cung cấp thông tin triệu chứng hoặc đơn thuốc từ cơ sở khám chữa bệnh.
   - Thực hiện thanh toán và nhận hóa đơn / chứng từ mua hàng.
5. **Supplier (Nhà cung cấp / Đối tác phân phối):**
   - Đơn vị cung ứng dược phẩm, thiết bị y tế cho chuỗi nhà thuốc.
   - Xuất hóa đơn giao hàng, giao hàng thực tế tới kho chi nhánh.
6. **System / Automated Background Process (Tiến trình tự động của hệ thống):**
   - Tự động quét và cảnh báo thuốc sắp hết hạn.
   - Tự động đồng bộ đối soát thanh toán điện tử định kỳ.
   - Tự động sao lưu dữ liệu và kiểm tra tính toàn vẹn hệ thống.

---

## 8. Branch Domain

Chi nhánh (`CHI_NHANH`) là ranh giới tổ chức và kinh doanh cốt lõi của PharmaBranch.

### 8.1. Dữ liệu thuộc sở hữu chi nhánh (Branch-Owned Data)
Dữ liệu gắn liền với hoạt động vận hành của một địa điểm vật lý xác định:
- Tồn kho (`TON_KHO`) và các bản ghi biến động kho (`GIAO_DICH_KHO`).
- Đơn bán hàng (`DON_DAT_THUOC`), Hóa đơn (`HOA_DON`), Chi tiết hóa đơn (`HOA_DON_ITEM`).
- Phiếu nhập kho (`PHIEU_NHAP`), Đơn nhập hàng (`DON_NHAP_HANG`).
- Yêu cầu đổi trả (`DON_TRA_HANG`), Chi phí chi nhánh (`YEU_CAU_CHI`).
- Nhân viên làm việc tại chi nhánh (`NGUOI_DUNG`).

### 8.2. Dữ liệu dùng chung / Toàn cục (Global / Shared Master Data)
Dữ liệu có giá trị tham chiếu chung trong toàn bộ hệ thống chuỗi:
- Danh mục thuốc chuẩn (`THUOC`), Nhóm thuốc (`NHOM_THUOC`), Đơn vị tính (`DON_VI_TINH`).
- Danh mục Nhà cung cấp dùng chung (trừ khi dự án có quy định nhà cung cấp riêng theo chi nhánh).
- Bảng tham chiếu mã định danh chuẩn, quy cách đóng gói.

> [!IMPORTANT]
> **Tuân thủ ranh giới Rule 06:**
> Phân loại trên là mô hình nghiệp vụ tham chiếu. Thiết kế schema vật lý cụ thể (bảng nào có `chi_nhanh_id`, bảng nào truy vết qua quan hệ cha-con) phải dựa trên ERD và tuân thủ tuyệt đối `Rule 06` (Branch Isolation). Chi nhánh A tuyệt đối không được phép thao tác hoặc nhìn thấy dữ liệu nghiệp vụ của Chi nhánh B.

---

## 9. Medicine Domain

Thuốc và sản phẩm y tế là đối tượng kinh doanh trung tâm của hệ thống.

### 9.1. Khái niệm và thuộc tính nghiệp vụ
Một sản phẩm thuốc trong danh mục chuẩn thường mang các thuộc tính:
- **Mã thuốc (Medicine Code / Barcode):** Mã định danh duy nhất để quản lý và quét mã vạch.
- **Tên thương mại (Brand Name / Commercial Name):** Tên thuốc lưu hành trên thị trường (ví dụ minh họa: Panadol Extra).
- **Hoạt chất & Hàm lượng (Active Ingredient & Strength):** Thành phần dược học chính (ví dụ minh họa: Paracetamol 500mg, Caffeine 65mg).
- **Dạng bào chế (Dosage Form):** Viên nén, viên nang, siro, hỗn dịch, dung dịch tiêm, mỡ bôi da (ví dụ tham khảo).
- **Đơn vị tính cơ bản (Base Unit):** Viên, vỉ, hộp, chai, ống, gói.
- **Nhóm / Phân loại (Category):** Thuốc kháng sinh, giảm đau - hạ sốt, tim mạch, tiêu hóa, thực phẩm chức năng.
- **Yêu cầu đơn thuốc (Prescription Flag):** Phân định thuốc kê đơn (ETC - Ethical Drugs, thường yêu cầu đơn thuốc khi áp dụng) và không kê đơn (OTC - Over The Counter) nếu được project specification quy định.
- **Trạng thái kinh doanh (Status):** Đang kinh doanh (Active), Ngừng kinh doanh (Inactive / Discontinued).

### 9.2. Phân định rõ 5 cấp độ thực thể liên quan đến Thuốc
Agent tuyệt đối không được nhầm lẫn giữa 5 khái niệm nghiệp vụ sau:
1. **Medicine Master (Danh mục thuốc chuẩn):** Khái niệm định danh thuốc tổng thể, không chứa số lượng tồn kho (ví dụ: "Amoxicillin 500mg").
2. **Inventory Stock (Tồn kho thuốc theo chi nhánh):** Bản ghi theo dõi tổng số lượng thuốc đang có tại một chi nhánh cụ thể.
3. **Stock Batch / Lot (Lô hàng trong kho):** Khối lượng thuốc cụ thể gắn với một số lô sản xuất và một hạn sử dụng xác định tại chi nhánh.
4. **Sale Item (Mặt hàng trong đơn bán):** Một dòng trong hóa đơn bán lẻ, ghi nhận số lượng bán, đơn giá, chiết khấu và lô được trừ.
5. **Purchase Item (Mặt hàng trong đơn nhập):** Một dòng trong phiếu nhập hàng từ nhà cung cấp, ghi nhận số lượng nhập, giá nhập và thông tin số lô hạn dùng khai báo.

---

## 10. Medicine Batch / Lot Domain

Trong nghiệp vụ quản lý dược phẩm, việc quản lý theo Số lô (`Batch / Lot Number`) và Hạn sử dụng (`Expiration Date`) thường được áp dụng nhằm hỗ trợ kiểm soát chất lượng và theo dõi vòng đời hàng hóa (khi được project requirement xác nhận).

### 10.1. Các yếu tố của Lô thuốc
- **Số lô (Batch Number):** Ký hiệu do nhà sản xuất quy định cho một đợt sản xuất đồng nhất.
- **Ngày sản xuất (Manufacturing Date):** Thời điểm thuốc xuất xưởng.
- **Hạn dùng (Expiry Date):** Mốc thời gian giới hạn lưu hành hoặc sử dụng theo khuyến cáo/quy chuẩn (ví dụ tham khảo).
- **Số lượng nhập / Tồn hiện tại:** Số lượng viên/hộp thuộc lô đó đang nằm trong kho.
- **Trạng thái lô:** Đủ điều kiện bán (Active), Sắp hết hạn (Near Expiry), Đã hết hạn (Expired), hoặc Bị thu hồi (Recalled).

### 10.2. Chính sách xuất kho: FEFO vs. FIFO
- **FEFO (First Expired, First Out - Hết hạn trước, Xuất trước):** Ưu tiên xuất các lô có ngày hết hạn gần nhất để giảm thiểu nguy cơ thuốc hỏng trong kho. Đây là thông lệ phổ biến trong phân phối dược phẩm (ví dụ tham khảo).
- **FIFO (First In, First Out - Nhập trước, Xuất trước):** Xuất theo thứ tự thời gian nhập kho.

> [!WARNING]
> **Chính sách FEFO/FIFO không tự động bắt buộc:**
> Agent không được mặc định tuyên bố FEFO hoặc FIFO là bắt buộc trừ khi có quy định tường minh trong yêu cầu dự án hoặc bằng chứng mã nguồn đã triển khai. Hệ thống có thể cho phép nhân viên bán hàng tự chọn lô thuốc thực tế trên kệ quầy.

---

## 11. Inventory Domain

### 11.1. Bản chất của Tồn kho
Tồn kho là sự hiện diện vật lý của hàng hóa tại một địa điểm kinh doanh, sẵn sàng phục vụ bán lẻ hoặc điều chuyển.
- **Physical Quantity (Tồn thực tế):** Lượng hàng đang có mặt trong tủ, kệ, kho của chi nhánh.
- **Available Quantity (Tồn khả dụng):** Lượng hàng thực tế trừ đi lượng hàng đang được giữ chỗ (reserved) cho các đơn hàng đang xử lý hoặc chờ xuất.
- **Damaged / Expired Quantity (Hàng hỏng / Hết hạn):** Thuốc bị ẩm mốc, vỡ, hết hạn sử dụng đang chờ thủ tục hủy hoặc trả lại nhà cung cấp, không được đưa vào kinh doanh.

### 11.2. Phân định giữa Trạng thái hiện tại và Lịch sử giao dịch kho
- **Current Inventory State (`TON_KHO`):** Ảnh chụp nhanh số dư hiện tại của từng mặt hàng / lô hàng tại thời điểm truy vấn.
- **Inventory Transaction History (`GIAO_DICH_KHO`):** Sổ cái bất biến ghi nhận mọi sự biến động (tăng, giảm) của kho cùng lý do nghiệp vụ (nhập hàng, bán lẻ, khách trả lại, xuất hủy, điều chỉnh kiểm kê).

### 11.3. Bất biến nhất quán tồn kho (Inventory Consistency Invariant)
Khi áp dụng cơ chế quản lý sổ cái kho theo yêu cầu nghiệp vụ, mọi thay đổi trên `Current Inventory State` cần tương ứng với một bản ghi hợp lệ trong `Inventory Transaction History`:
$$\Delta \text{Stock} = \text{Quantity}_{\text{Transaction}}$$
Tồn kho không được phép thay đổi một cách tùy tiện mà không có chứng từ hoặc lý do giao dịch hợp lệ khi hệ thống triển khai kiểm soát biến động kho.

---

## 12. Stock Receiving Workflow

Quy trình nhập kho thể hiện việc bổ sung hàng hóa từ Nhà cung cấp vào kho của chi nhánh.

```text
[Nhà cung cấp giao hàng]
       ↓
[Tạo Phiếu Nhập / Receiving Doc (DRAFT)]
       ↓
[Kiểm đếm thực tế: Số lượng, Số lô, Hạn dùng]
       ↓
[Xác thực nghiệp vụ & Phê duyệt (CONFIRMED / COMPLETED)]
       ↓
[Cập nhật Tồn kho (Inventory Balance Increase)]
       ↓
[Ghi sổ Giao dịch kho (Inventory Transaction Log)]
       ↓
[Hoàn tất & Cập nhật Công nợ Nhà cung cấp]
```

### Minh họa trạng thái chứng từ nhập kho
Các trạng thái sau chỉ mang tính chất minh họa chuẩn nghiệp vụ:
- `DRAFT`: Phiếu nhập mới tạo, đang nhập liệu, chưa ảnh hưởng tồn kho.
- `PENDING_APPROVAL`: Đang chờ quản lý kho duyệt.
- `COMPLETED / RECEIVED`: Đã nhận đủ hàng, tồn kho đã chính thức tăng lên.
- `CANCELLED`: Phiếu bị hủy, không có biến động kho nào xảy ra.

*(Trạng thái thực tế của hệ thống phải dựa trên schema và code hiện hành).*

---

## 13. Sales Workflow (Reference Sales Workflow)

Quy trình bán hàng tại quầy dưới đây là **workflow tham chiếu / minh họa cho phân tích domain**; quy trình thực tế của hệ thống phải được xác nhận từ yêu cầu nghiệp vụ đã phê duyệt (approved business requirements), mã nguồn triển khai (implementation evidence) và/hoặc bằng chứng kiểm thử (test evidence):

```text
1. Khách hàng yêu cầu thuốc / Tư vấn triệu chứng / Cung cấp đơn thuốc
   ↓
2. Dược sĩ tìm kiếm thuốc, kiểm tra Tồn kho khả dụng & Lô thuốc
   ↓
3. Thêm mặt hàng vào Đơn bán (Chọn số lượng, kiểm tra đơn vị tính, áp dụng chiết khấu)
   ↓
4. Tính toán tổng thanh toán (Tổng tiền hàng, Giảm giá, Thuế VAT nếu có)
   ↓
5. Khách hàng lựa chọn Phương thức thanh toán (Tiền mặt, Chuyển khoản, Thẻ)
   ↓
6. Xác nhận thanh toán thành công
   ↓
7. Tạo và xuất Hóa đơn bán lẻ (Invoice Creation)
   ↓
8. Khấu trừ Tồn kho & Ghi nhận Giao dịch xuất kho (Stock Deduction)
   ↓
9. In hóa đơn & Bàn giao thuốc cho khách hàng
```

> [!IMPORTANT]
> **Tính chất tham chiếu & Tách bạch giữa các khái niệm:**
> 1. **Thứ tự thực hiện không tự động là bất biến:** Thứ tự giữa các bước (ví dụ: thanh toán trước khi tạo hóa đơn hay ngược lại, tạo hóa đơn trước khi trừ tồn kho hay trừ kho khi giao hàng) chỉ là mô hình tham chiếu. Agent không được mặc định coi thứ tự này là business invariant bắt buộc trừ khi được đặc tả dự án hoặc mã nguồn xác nhận.
> 2. **Tách bạch khái niệm:** Giỏ hàng tạm thời (Cart) ≠ Đơn đặt thuốc (Order) ≠ Hóa đơn (Invoice) ≠ Bản ghi thanh toán (Payment) ≠ Biến động trừ kho (Inventory Mutation). Các bước này có thể diễn ra trong cùng một transaction hoặc tách rời tùy theo kiến trúc triển khai, nhưng về mặt nghiệp vụ là các khái niệm độc lập.

---

## 14. Order Domain

Đơn hàng (`DON_DAT_THUOC` / `Sale Order`) là cam kết thương mại ghi nhận yêu cầu mua hàng của khách hàng trước hoặc trong khi thanh toán.

### 14.1. Cấu trúc thực thể Đơn hàng
- **Header:** Mã đơn hàng, Ngày đặt, Khách hàng, Chi nhánh bán, Nhân viên tạo đơn, Trạng thái đơn, Tổng giá trị dự kiến.
- **Items:** Danh sách các dòng mặt hàng, số lượng yêu cầu, đơn giá niêm yết, tỷ lệ chiết khấu, thành tiền từng dòng.

### 14.2. Vòng đời đơn hàng
Tùy theo nghiệp vụ dự án, đơn hàng có thể có các trạng thái:
- `PENDING` (Chờ xử lý / Chờ thanh toán).
- `PAID` / `PROCESSING` (Đã thanh toán / Đang xuất kho).
- `COMPLETED` (Đã giao hàng và hoàn tất).
- `CANCELLED` (Khách hủy mua hoặc hết hàng).

---

## 15. Invoice Domain

Hóa đơn (`HOA_DON` / `Invoice`) là chứng từ kế toán và thương mại chính thức chứng nhận giao dịch mua bán đã diễn ra hoặc hoàn tất.

### 15.1. Đặc trưng nghiệp vụ của Hóa đơn
- Là căn cứ thương mại và kế toán của giao dịch bán thuốc giữa Chi nhánh và Khách hàng.
- **Bất biến sau khi hoàn tất (Immutability):** Khi hóa đơn đã ở trạng thái hoàn tất (`COMPLETED` / `FINALIZED`) và bàn giao hàng hóa, các thông tin tài chính và mặt hàng thường không được phép chỉnh sửa tùy tiện trực tiếp. Mọi điều chỉnh sau bán hàng cần thông qua nghiệp vụ đổi trả hoặc hóa đơn điều chỉnh theo quy định dự án.
- **Liên kết đối soát và đổi trả:** Yêu cầu đổi trả thuốc sau bán hàng cần đối chiếu trực tiếp với mã hóa đơn gốc hoặc chứng từ liên kết hợp lệ.

### 15.2. Chữ ký số trong ngữ cảnh nghiệp vụ (Digital Signature Business Semantics)
- **Ý nghĩa kinh doanh (Business Meaning):** Chữ ký số là cơ chế xác thực nguồn gốc phát hành, đảm bảo tính toàn vẹn nội dung của chứng từ thương mại và chống chối bỏ trách nhiệm nghiệp vụ của đơn vị bán hàng.
- **Lý do chứng từ yêu cầu ký (Why Signing is Needed):** Đảm bảo tính xác thực và minh bạch của chứng từ với cơ quan quản lý và khách hàng, hỗ trợ giá trị pháp lý theo quy định hoặc yêu cầu dự án áp dụng (nếu có), đồng thời ngăn chặn việc can thiệp trái phép sau khi chốt giao dịch.
- **Chứng từ liên kết (Associated Document):** Thường gắn liền với Hóa đơn (`HOA_DON`) khi giao dịch được chốt hoặc xuất hóa đơn điện tử.
- **Tác động vòng đời nghiệp vụ (Lifecycle Implications):** Khi được ký số hợp lệ, hóa đơn chuyển sang trạng thái đã ký/bất biến (`SIGNED` / `COMPLETED`); mọi hành vi sửa đổi dữ liệu sau đó đều làm vô hiệu hóa giá trị nghiệp vụ của chữ ký.
- **Khả năng truy vết (Traceability):** Cho phép kiểm tra và đối soát tính xác thực của hóa đơn trong quá trình kiểm toán và giải quyết khiếu nại.
- **Ranh giới kỹ thuật & an ninh (Technical & Security Boundary):**
  - Skill 11 chỉ định nghĩa ý nghĩa nghiệp vụ và tác động vòng đời của việc ký số.
  - Các khía cạnh kỹ thuật như thuật toán băm (ví dụ minh họa: SHA-256), thuật toán khóa (ví dụ minh họa: RSA/ECDSA), chuẩn hóa dữ liệu chuẩn tắc (canonicalization), quản lý và bảo vệ khóa bí mật (private key storage), và kiến trúc thực thi ký số phía server là mối quan tâm kiến trúc và an ninh thuộc sở hữu của `Rule 02` (Architecture Quality) và `Rule 03` (Security). Skill 11 không áp đặt hoặc sở hữu việc triển khai mật mã này.

---

## 16. Payment Domain

Thanh toán (`PAYMENT`) là nghiệp vụ chuyển giao giá trị tài chính để thanh toán cho nghĩa vụ của đơn hàng hoặc hóa đơn.

### 16.1. Các phương thức thanh toán phổ biến
- **Tiền mặt (Cash):** Thu ngân nhận tiền mặt, tính tiền thối (change) cho khách.
- **Chuyển khoản ngân hàng (Bank Transfer / VietQR):** Khách quét mã QR chuyển khoản vào tài khoản chi nhánh.
- **Ví điện tử / Cổng thanh toán (VNPay, MoMo, ZaloPay):** Tích hợp thanh toán qua API đối tác bên thứ ba.

### 16.2. Trạng thái thanh toán
- `PENDING` (Đang chờ giao dịch hoàn tất).
- `SUCCESS / COMPLETED` (Thanh toán thành công).
- `FAILED` (Giao dịch thất bại / Khách hủy giao dịch).
- `REFUNDED` (Đã hoàn lại tiền cho khách do hủy đơn hoặc trả hàng).

*(Chỉ coi một cổng thanh toán là được hỗ trợ khi có bằng chứng mã nguồn hoặc cấu hình tích hợp thực tế).*

---

## 17. Return / Refund Domain

Quy trình Đổi trả & Hoàn tiền là một trong những nghiệp vụ nhạy cảm và phức tạp nhất trong ngành bán lẻ thuốc.

```text
[Khách hàng yêu cầu đổi trả]
       ↓
[Đối soát Hóa đơn gốc & Điều kiện đổi trả (Hạn dùng, Bao bì, Thời gian)]
       ↓
[Tạo Phiếu Đổi Trả / Return Request]
       ↓
[Kiểm định dược phẩm: Đủ chuẩn tái nhập kho HAY Phải xuất hủy?]
       ↓
┌──────────────────────┴──────────────────────┐
[Đạt chuẩn: Nhập lại Kho]       [Hỏng/Hết hạn: Chuyển khu chờ hủy]
       ↓                                      ↓
[Tăng tồn kho khả dụng]                [Không tăng tồn kho bán lẻ]
       └──────────────────────┬───────────────┘
                              ↓
             [Xử lý Hoàn tiền / Trừ công nợ]
                              ↓
                     [Hoàn tất Đổi trả]
```

### 17.1. Các nguyên tắc nghiệp vụ đổi trả cốt lõi (Tham khảo miền & Chính sách dự án)
- **Không tự động hoàn tiền:** Không phải mọi trường hợp đổi trả đều hoàn tiền mặt; hình thức xử lý (đổi hàng tương đương, phát hành voucher, hoặc hoàn tiền) phụ thuộc vào chính sách nghiệp vụ của dự án.
- **Không tự động tái nhập kho:** Hàng trả lại có thể phải qua bước kiểm định hoặc phân loại trước khi quyết định tái nhập kho. Ví dụ tham khảo trong ngành dược: các sản phẩm yêu cầu điều kiện bảo quản khắt khe (như bảo quản lạnh $2-8^\circ\text{C}$) khi đã mang ra khỏi nhà thuốc có thể không được phép tái nhập vào kho bán lẻ nếu chính sách dự án có quy định.
- **Không trả vượt số lượng mua:** Số lượng trả lại của một mặt hàng thường được giới hạn không vượt quá số lượng đã mua trên chứng từ gốc trừ đi các lần trả trước đó (nếu applicable theo business policy của dự án).

---

## 18. Prescription Domain

Đơn thuốc (`Prescription`) là văn bản chỉ định điều trị y tế (khái niệm nghiệp vụ tham chiếu).

### 18.1. Các yếu tố nghiệp vụ của Đơn thuốc (Ví dụ tham khảo miền)
- **Thông tin người kê đơn:** Họ tên người kê đơn, mã hành nghề/chứng chỉ, cơ sở y tế (ví dụ tham khảo).
- **Thông tin người bệnh:** Họ tên, tuổi/ngày sinh, giới tính, chẩn đoán (ví dụ tham khảo).
- **Chỉ định thuốc:** Tên hoạt chất/biệt dược, liều dùng, đường dùng, số lần uống, thời gian dùng.

*(Lưu ý: Các thuộc tính trên là ví dụ tham khảo từ thực tế y tế; phạm vi dữ liệu thực tế lưu trữ trong hệ thống phải căn cứ vào đặc tả và yêu cầu được duyệt của dự án).*

### 18.2. Quy tắc nghiệp vụ liên quan đến Thuốc kê đơn (ETC)
- Thuốc được đánh dấu là `Kê đơn (Prescription Required, nếu có cờ này trong đặc tả dự án)` có thể yêu cầu liên kết với thông tin đơn thuốc hợp lệ khi được project requirement xác nhận.
- **Xử lý phạm vi:** Nếu chức năng đơn thuốc chưa có trong repository, đánh dấu là `NOT VERIFIED` hoặc `OUT OF CURRENT SCOPE`, tuyệt đối không tự bịa đặt bảng biểu hoặc API khi chưa có bằng chứng.

---

## 19. Customer / Patient Domain

Hệ thống phân định rõ hai khái niệm liên quan đến người nhận dịch vụ:
- **Customer (Khách hàng):** Người trực tiếp giao dịch, trả tiền và nhận hóa đơn (ví dụ minh họa: người thân mua thuốc hộ).
- **Patient (Bệnh nhân / Người dùng thuốc):** Người thực tế sử dụng thuốc, gắn với tiền sử bệnh, thể trạng hoặc đơn chỉ định y tế.

Ví dụ minh họa: Trong giao dịch bán lẻ thông thường, Khách hàng và Bệnh nhân thường là một; trong mô hình quản lý nâng cao (nếu dự án yêu cầu), việc phân tách này có thể hỗ trợ theo dõi lịch sử điều trị và thông tin cảnh báo.

> [!CAUTION]
> **Bảo vệ dữ liệu y tế nhạy cảm:**
> Không thu thập hoặc lưu trữ thông tin bệnh lý riêng tư của khách hàng trừ khi đặc tả dự án có yêu cầu rõ ràng. Dữ liệu y tế (nếu có) phải tuân thủ nghiêm ngặt bảo mật theo `Rule 03` và Column-Level Security theo `Rule 07`.

---

## 20. Supplier Domain

Nhà cung cấp (`NHA_CUNG_CAP` / `Supplier`) là đối tác bán buôn cung ứng dược phẩm và vật tư y tế cho chuỗi nhà thuốc.

### 20.1. Các thuộc tính nghiệp vụ
- Tên công ty / nhà phân phối dược phẩm.
- Mã số thuế, thông tin giấy phép kinh doanh (ví dụ tham khảo khi có yêu cầu).
- Địa chỉ, Số điện thoại liên hệ, Đại diện thương mại.
- Lịch sử cung ứng và tình trạng công nợ mua hàng.

### 20.2. Ranh giới sở hữu nhà cung cấp
Nhà cung cấp thường là danh mục dùng chung toàn chuỗi (Global Supplier Catalog) hoặc do Hội đồng mua hàng trung tâm quản lý. Tuy nhiên, nếu nghiệp vụ dự án cho phép từng chi nhánh tự tìm kiếm nhà cung cấp địa phương, quyền sở hữu sẽ được phân định theo chứng từ nhập hàng của từng chi nhánh.

---

## 21. Business Invariants

Bất biến nghiệp vụ (**Business Invariant**) là các điều kiện và quy tắc nghiệp vụ cốt lõi cần được bảo toàn nhằm duy trì tính toàn vẹn của dữ liệu và quy trình kinh doanh.

### 21.1. Phân loại bất biến nghiệp vụ theo bằng chứng (Invariant Evidence Classification)
Để tránh nhầm lẫn giữa thông lệ ngành tổng quát và quy tắc bắt buộc của dự án, mọi bất biến phải được phân loại thành 3 nhóm rõ ràng:
1. **Confirmed Project Invariant (Bất biến dự án đã xác nhận):** Bất biến đã được khẳng định tường minh trong tài liệu đặc tả yêu cầu được duyệt, quy định quản trị dự án, hoặc có bằng chứng kiểm thử/mã nguồn xác thực.
2. **Domain Reference / Illustrative Invariant (Bất biến tham khảo miền / Minh họa):** Các mô hình bất biến phổ biến trong phân phối và bán lẻ dược phẩm, đóng vai trò khuôn mẫu tham chiếu khi phân tích hoặc thiết kế, không tự động coi là quy định bắt buộc của PharmaBranch nếu thiếu bằng chứng dự án.
3. **Proposed Invariant Requiring Business Confirmation (Bất biến đề xuất cần xác nhận nghiệp vụ):** Bất biến do Agent hoặc kỹ sư đề xuất để bịt lỗ hổng dữ liệu/logic, bắt buộc phải được người dùng hoặc tài liệu yêu cầu phê duyệt trước khi áp dụng.

### 21.2. Các bất biến tham khảo miền tiêu biểu (Illustrative Domain Invariants)
Các bất biến dưới đây là mô hình tham khảo tiêu biểu trong nghiệp vụ nhà thuốc; quy tắc cụ thể, phạm vi áp dụng, ngoại lệ và cơ chế thực thi phải được dẫn xuất từ đặc tả yêu cầu, kiến trúc được duyệt và mã nguồn thực tế của dự án:

1. **Bất biến Tồn kho khả dụng (Available Stock Invariant - Mô hình tham khảo):**
   Số lượng thuốc xuất bán hoặc điều chuyển trong điều kiện vận hành chuẩn không được vượt quá số lượng tồn kho khả dụng hiện có của mặt hàng / lô hàng đó tại chi nhánh:
   $$\text{Quantity}_{\text{Sale}} \le \text{Quantity}_{\text{Available}}$$
   *(Quy tắc xuất kho, trừ âm hay cho phép đặt trước phụ thuộc vào business policy của dự án).*

2. **Bất biến Giới hạn chỉnh sửa chứng từ đã hoàn tất (Completed Document Immutability - Mô hình tham khảo):**
   Hóa đơn hoặc chứng từ nhập kho khi đã chuyển sang trạng thái hoàn tất (`COMPLETED` / `FINALIZED`) không được sửa đổi trực tiếp các chỉ số tài chính hoặc danh mục hàng; các biến động phát sinh sau đó được xử lý qua quy trình hủy hoặc chứng từ điều chỉnh theo quy định dự án.

3. **Bất biến Tính toán tài chính dòng và tổng (Monetary Sum Invariant - Mô hình tham khảo):**
   Tổng tiền thanh toán của hóa đơn/đơn hàng cần khớp với tổng giá trị các dòng chi tiết sau khi trừ chiết khấu và cộng thuế theo công thức nghiệp vụ được dự án phê duyệt:
   $$\text{TotalAmount} = \sum (\text{ItemQuantity} \times \text{UnitPrice} - \text{Discount}) + \text{Tax}$$

4. **Bất biến Ranh giới chi nhánh (Branch Scope Invariant - Bất biến bắt buộc theo Rule 06):**
   Một giao dịch bán lẻ, phiếu nhập hoặc đơn đổi trả của Chi nhánh A chỉ được phép tương tác với tài nguyên và tồn kho thuộc Chi nhánh A, không được phép thao tác chéo sang Chi nhánh B.

5. **Bất biến Đổi trả hợp lệ (Valid Return Invariant - Mô hình tham khảo):**
   Số lượng hàng đổi trả của từng dòng mặt hàng không vượt quá số lượng hàng đã bán thực tế trên chứng từ gốc trừ đi các lần đổi trả trước đó:
   $$\text{Quantity}_{\text{Returned}} \le \text{Quantity}_{\text{OriginalSold}} - \text{Quantity}_{\text{PreviouslyReturned}}$$

6. **Bất biến Kiểm soát hạn dùng (Expiry Handling - Mô hình tham khảo):**
   Thuốc đã quá hạn sử dụng (`ExpiryDate` < `CurrentDate`) bị chặn hoặc cảnh báo khi tạo đơn bán lẻ thông thường theo chính sách kiểm soát chất lượng của chi nhánh nếu áp dụng.

7. **Bất biến Giá trị không âm (Non-Negative Values - Mô hình tham khảo):**
   Đơn giá bán, đơn giá nhập, số lượng tồn kho và số tiền thanh toán không mang giá trị âm trong các nghiệp vụ giao dịch tiêu chuẩn (ngoại trừ các bút toán điều chỉnh kế toán được định nghĩa riêng nếu dự án có quy định).

### 21.3. Phân định quyền sở hữu và thực thi bất biến
- **Skill 11 (Domain):** Sở hữu **Ý NGHĨA KINH DOANH** và phân loại bất biến.
- **Rule 02 & Tầng Ứng dụng/Nghiệp vụ:** Sở hữu phạm vi giao dịch ACID, kiểm soát đồng thời và thực thi bất biến theo kiến trúc.
- **Rule 06:** Sở hữu cơ chế cách ly dữ liệu chi nhánh.
- **Rule 07 & Database:** Sở hữu việc thiết lập các ràng buộc SQL (`CHECK`, `FOREIGN KEY`, `UNIQUE`) nhằm cung cấp cơ chế phòng thủ chiều sâu nơi phù hợp.

---

## 22. State Transition Model

Các thực thể có vòng đời hoặc trạng thái nghiệp vụ ý nghĩa (chẳng hạn như đơn bán, phiếu nhập, yêu cầu đổi trả hoặc thanh toán) nên được phân tích bằng mô hình chuyển trạng thái (state-transition model) khi áp dụng:

$$\text{Current State} + \text{Business Action} + \text{Actor} + \text{Preconditions} \longrightarrow \text{Next State}$$

> [!NOTE]
> **Phạm vi áp dụng mô hình trạng thái:**
> Không phải mọi thực thể trong miền nghiệp vụ đều bắt buộc phải có một máy trạng thái tường minh (ví dụ: các thực thể danh mục dùng chung thuần túy như đơn vị tính, nhóm thuốc thường không đòi hỏi máy trạng thái phức tạp). Các trạng thái như `DRAFT`, `PENDING`, `APPROVED`, `COMPLETED`, `CANCELLED` là các ví dụ minh họa chuẩn về mặt nghiệp vụ trừ khi được xác nhận cụ thể bởi bằng chứng mã nguồn hoặc tài liệu yêu cầu của dự án.

### 22.1. Quy trình phân tích máy trạng thái 7 bước
Khi thiết kế hoặc rà soát một máy trạng thái cho thực thể có trạng thái nghiệp vụ, Agent nên:
1. **Identify States:** Liệt kê đầy đủ các trạng thái khả dĩ trong phạm vi nghiệp vụ (ví dụ minh họa: DRAFT, SUBMITTED, APPROVED, REJECTED, COMPLETED, CANCELLED).
2. **Identify Allowed Actions:** Xác định các hành động hợp lệ từ mỗi trạng thái.
3. **Identify Preconditions:** Xác định các điều kiện tiên quyết (ví dụ: đủ tồn kho, thanh toán đã thành công).
4. **Identify Resulting State:** Xác định trạng thái đích sau khi hành động thành công.
5. **Identify Invalid Transitions:** Liệt kê rõ các bước nhảy bị cấm (ví dụ: từ CANCELLED chuyển sang COMPLETED là BỊ CẤM).
6. **Identify Cancellation / Reversal Behavior:** Quy định cách thức hoàn tác (ví dụ: hủy đơn thì hoàn trả lại số lượng giữ chỗ).
7. **Identify Side Effects:** Ghi nhận các tác động phụ (gửi thông báo, ghi nhật ký kiểm toán, cập nhật công nợ).

### 22.2. Minh họa ma trận chuyển trạng thái Đơn hàng (Illustrative State Matrix)

| Trạng thái hiện tại | Hành động (Action) | Điều kiện tiên quyết (Preconditions) | Trạng thái kế tiếp | Tác động phụ nghiệp vụ |
|---|---|---|---|---|
| `DRAFT` | Submit / Checkout | Giỏ hàng có ít nhất 1 mặt hàng hợp lệ | `PENDING_PAYMENT` | Khóa giữ chỗ tồn kho (Reserve Stock) |
| `DRAFT` | Cancel / Discard | Không có | `CANCELLED` | Hủy đơn nháp |
| `PENDING_PAYMENT` | Confirm Payment | Cổng thanh toán báo SUCCESS hoặc thu đủ tiền mặt | `PAID` | Tạo Hóa đơn chính thức |
| `PENDING_PAYMENT` | Payment Timeout / Fail | Hết thời gian chờ hoặc khách hủy | `CANCELLED` | Giải phóng giữ chỗ tồn kho (Release Stock) |
| `PAID` | Fulfill / Dispense | Nhân viên đã đóng gói thuốc và giao khách | `COMPLETED` | Trừ kho chính thức, ghi sổ kho |
| `COMPLETED` | Request Return | Có hóa đơn gốc, trong hạn đổi trả | `RETURN_PENDING` | Khởi tạo quy trình đổi trả |
| `CANCELLED` | Bất kỳ hành động nào | Không áp dụng | *BỊ CẤM (DENY)* | Ném lỗi Invalid State Transition |

> [!CAUTION]
> Bảng trên là mô hình minh họa chuẩn. Trạng thái thực tế trong mã nguồn phải được dán nhãn: `IMPLEMENTED`, `VERIFIED`, hoặc `PROPOSED`.

---

## 23. Business Workflow Analysis

Khi phân tích hoặc đặc tả một quy trình nghiệp vụ mới hoặc hiện có, Agent bắt buộc phải sử dụng **Mẫu Phân Tích Quy Trình 12 Điểm (Standard Workflow Analysis Template)**:

```markdown
### 1. Trigger (Sự kiện kích hoạt)
Điều gì hoặc ai bắt đầu quy trình này? (Ví dụ: Khách đến quầy, Nhà cung cấp giao hàng, Cron job quét nửa đêm).

### 2. Actor (Đối tượng thực hiện)
Ai là người chủ trì hành động? (Ví dụ: Dược sĩ bán hàng, Thủ kho, Quản lý).

### 3. Preconditions (Điều kiện tiên quyết)
Những điều kiện nào bắt buộc phải thỏa mãn trước khi bắt đầu? (Ví dụ: Người dùng đã đăng nhập đúng chi nhánh, ca làm việc đang mở).

### 4. Main Flow (Luồng xử lý chính từng bước)
Các bước tuần tự diễn ra từ bước 1 đến bước cuối cùng.

### 5. Business Validation (Xác thực nghiệp vụ)
Những quy tắc và bất biến nào được kiểm tra? (Ví dụ: Kiểm tra hạn dùng, kiểm tra số lượng tồn, kiểm tra đơn thuốc kê toa).

### 6. State Changes (Thay đổi trạng thái thực thể)
Những thực thể nào chuyển đổi trạng thái? (Ví dụ: Đơn hàng từ PENDING -> COMPLETED).

### 7. Data Changes (Thay đổi dữ liệu)
Những bảng dữ liệu nào được ghi, cập nhật hoặc xóa? (Ví dụ: Tăng TON_KHO, chèn bản ghi GIAO_DICH_KHO).

### 8. Side Effects (Tác động phụ nghiệp vụ)
Những hiệu ứng nào phát sinh ngoài luồng chính? (Ví dụ: Gửi SMS tích điểm, sinh chữ ký số).

### 9. Failure Path (Kịch bản thất bại)
Hệ thống xử lý ra sao nếu một bước bị lỗi? (Ví dụ: Thanh toán thất bại, không đủ hàng trong kho).

### 10. Cancellation / Reversal (Quy trình hủy / hoàn tác)
Thao tác này có thể bị hủy không? Cơ chế bồi hoàn dữ liệu là gì?

### 11. Auditability (Khả năng kiểm toán)
Hành vi này có cần ghi vết vào nhật ký kiểm toán không? Cần ghi thông tin gì?

### 12. Postconditions (Điều kiện sau khi hoàn tất)
Trạng thái bền vững của hệ thống sau khi quy trình thành công là gì?
```

---

## 24. Domain Error Model

Lỗi nghiệp vụ (**Domain Errors**) xuất hiện khi một hành động của người dùng vi phạm quy tắc kinh doanh hoặc bất biến của miền. Cần phân biệt rõ lỗi nghiệp vụ với lỗi hệ thống kỹ thuật (500 Internal Server Error, Database Connection Timeout).

### 24.1. Các lỗi nghiệp vụ tiêu biểu
- **`INSUFFICIENT_STOCK`:** Số lượng yêu cầu vượt quá tồn kho khả dụng tại chi nhánh.
- **`EXPIRED_MEDICINE`:** Thuốc đã quá hạn sử dụng, không nên đưa vào luồng bán hàng; việc chặn bán là domain/business requirement cần được xác nhận theo quy định áp dụng và project specification.
- **`INVALID_STATE_TRANSITION`:** Yêu cầu chuyển trạng thái không hợp lệ (ví dụ: cố gắng hủy một đơn hàng đã hoàn tất giao hàng).
- **`PRESCRIPTION_REQUIRED`:** Thuốc thuộc danh mục kê đơn nhưng thiếu thông tin đơn thuốc hợp lệ.
- **`CROSS_BRANCH_VIOLATION`:** Thao tác dữ liệu ngoài phạm vi chi nhánh được phép hoạt động.
- **`RETURN_QUANTITY_EXCEEDED`:** Số lượng trả lại vượt quá số lượng đã mua ban đầu.
- **`PAYMENT_AMOUNT_MISMATCH`:** Số tiền thanh toán không khớp với tổng tiền hóa đơn.
- **`INACTIVE_PRODUCT`:** Thuốc đã bị ngừng kinh doanh hoặc đang bị tạm khóa lưu hành.

### 24.2. Ranh giới với các kỹ năng khác
- **Skill 11:** Định nghĩa **Ý NGHĨA VÀ NGUYÊN NHÂN NGHIỆP VỤ** của lỗi.
- **Skill 06 / Rule 08:** Định nghĩa cách biểu diễn lỗi ra API (Mã HTTP 400/422/409, cấu trúc RFC 7807 Problem Details).
- **Rule 05:** Quyết định xử lý từ chối quyền truy cập (401 Unauthorized, 403 Forbidden).
- **Skill 07 / Rule 07:** Bắt và dịch các vi phạm ràng buộc SQL (`CHECK constraint violation`, `FOREIGN KEY conflict`).

---

## 25. Domain Traceability & Governance

Để đảm bảo không có tính năng nào bị triển khai sai lệch hoặc "bỏ quên" logic nghiệp vụ, hệ thống đòi hỏi chuỗi truy vết nghiệp vụ xuyên suốt:

$$\text{Business Requirement} \longrightarrow \text{Domain Concept} \longrightarrow \text{Business Rule} \longrightarrow \text{Workflow} \longrightarrow \text{State Transition} \longrightarrow \text{API Contract} \longrightarrow \text{Implementation} \longrightarrow \text{Test} \longrightarrow \text{Verification}$$

### 25.1. Xử lý khoảng trống nghiệp vụ (Domain Gaps)
Khi phát hiện một quy tắc nghiệp vụ bị thiếu ở bất kỳ tầng nào (ví dụ: tài liệu có ghi nhưng code chưa cài đặt, hoặc API có endpoint nhưng thiếu validate nghiệp vụ):
1. **Tuyệt đối không kết luận bừa bãi:** Không được vội vàng tuyên bố hệ thống sai hỏng hoàn toàn.
2. **Gắn nhãn phân loại chuẩn xác:**
   - `NOT FOUND`: Chưa tìm thấy tài liệu/code.
   - `NOT VERIFIED`: Có code nhưng chưa kiểm chứng.
   - `PROPOSED`: Giải pháp do Agent đề xuất bổ sung.
   - `IMPLEMENTED`: Đã lập trình.
   - `VERIFIED`: Đã kiểm chứng độc lập.
   - `CONFLICTING EVIDENCE`: Có sự mâu thuẫn giữa các tài liệu / tầng code.
3. **Báo cáo tường minh:** Chỉ rõ vị trí đứt gãy trong chuỗi truy vết để người dùng phê duyệt trước khi hành động.

---

## 26. Domain Audit Method

Khi được giao nhiệm vụ rà soát hoặc đánh giá một chức năng nghiệp vụ dược đã có trong hệ thống, Agent phải tiến hành phương pháp kiểm toán 16 bước:

1. **Xác định mục đích kinh doanh (Business Purpose):** Chức năng này giải quyết bài toán gì cho nhà thuốc?
2. **Xác định các Actor tham gia:** Ai là người thao tác và ai là người chịu ảnh hưởng?
3. **Xác định các thực thể miền (Domain Entities):** Những thực thể nào tham gia (Thuốc, Lô, Hóa đơn, Khách hàng)?
4. **Xác định các quy tắc nghiệp vụ (Business Rules):** Các điều kiện kiểm tra hợp lệ là gì?
5. **Xác định các bất biến nghiệp vụ (Invariants):** Điều kiện nào bắt buộc không bao giờ được sai?
6. **Xác định luồng quy trình (Workflow):** Các bước xử lý tuần tự diễn ra như thế nào?
7. **Xác định chuyển đổi trạng thái (State Transitions):** Máy trạng thái có chặt chẽ và xử lý đủ các nhánh rẽ không?
8. **Truy vết thay đổi dữ liệu (Data Changes):** Dữ liệu nào được ghi xuống database? Có sót sổ cái kho không?
9. **Truy vết ranh giới API (API Boundary):** API có expose đúng DTO nghiệp vụ không? Có bị mass assignment không?
10. **Truy vết ranh giới ủy quyền (Authorization Boundary):** Backend có kiểm tra quyền hay phó mặc cho Frontend?
11. **Truy vết phạm vi chi nhánh (Branch Scope):** Dữ liệu có bị rò rỉ hoặc thao tác chéo chi nhánh không?
12. **Truy vết tầng lưu trữ (Persistence):** Các ràng buộc SQL có bảo vệ được bất biến khi code ứng dụng gặp lỗi không?
13. **Truy vết kiểm thử (Tests):** Có test case kiểm tra cả ca thành công và ca thất bại nghiệp vụ không?
14. **Nhận diện điểm không nhất quán (Inconsistencies):** Đối chiếu xem ERD, Code, UI và Tài liệu có đá nhau không.
15. **Phân loại bằng chứng (Classify Evidence):** Dán nhãn trạng thái bằng chứng theo Mục 2.3.
16. **Báo cáo kết quả kiểm toán (Report Findings):** Trình bày rõ ràng bằng chứng, rủi ro nghiệp vụ và kiến nghị khắc phục.

---

## 27. Cross-Layer Domain Trace

Mô hình phân tích dòng chảy nghiệp vụ từ ý định người dùng đến kết quả thực thi:

```text
[User / Staff]
      ↓ (Khởi xướng)
[Business Intent (Ý định kinh doanh)]
      ↓ (Thực thi)
[Domain Workflow (Quy trình nghiệp vụ)]
      ↓ (Kiểm tra)
[Business Rules & Invariants (Quy tắc & Bất biến)]
      ↓ (Xác thực quyền)
[Authorization Check (Thẩm định RBAC & Thao tác)]
      ↓ (Bảo vệ ranh giới)
[Branch Scope Enforcement (Cô lập chi nhánh)]
      ↓ (Đảm bảo ACID)
[Transaction & Concurrency Boundary (Giao dịch & Đồng thời)]
      ↓ (Lưu trữ an toàn)
[Persistence & Database Constraints (Cơ sở dữ liệu)]
      ↓ (Ghi nhận vết)
[Audit Logging & Telemetry (Kiểm toán & Quan sát)]
      ↓ (Phản hồi)
[API / UI Result (Kết quả hiển thị cho người dùng)]
```

> [!NOTE]
> Đây là **Mô hình Phân tích Khái niệm (Conceptual Analysis Model)** để kiểm tra sự liên kết nghiệp vụ, không phải là quy định bắt buộc về kiến trúc phần mềm vật lý.

---

## 28. Domain vs Security Boundary

Cần phân định rạch ròi giữa Quy tắc nghiệp vụ và Chốt chặn an ninh:

| Khía cạnh | Domain Rule (Quy tắc Miền) | Security / Authorization Rule (Quy tắc An ninh) |
|---|---|---|
| **Câu hỏi cốt lõi** | *"Hành động này có hợp lệ trong nghiệp vụ bán lẻ thuốc không?"* | *"Ai được phép thực hiện hành động này và trên chi nhánh nào?"* |
| **Ví dụ** | "Thuốc hết hạn không được xuất bán." *(Ví dụ minh họa quy tắc miền)* | "Nhân viên kho không được phép tạo hóa đơn bán lẻ." |
| **Phân tách trách nhiệm (SoD)** | "Nhân viên tạo phiếu điều chỉnh kiểm kê không được tự duyệt phiếu của chính mình." *(Nguyên tắc nghiệp vụ)* | Cơ chế kiểm tra `Actor.Id != Document.CreatedById` và thẩm định role `MANAGER` tại server-side (`Rule 04`, `Rule 05`). |
| **Trách nhiệm Skill** | `Skill 11` định nghĩa yêu cầu nghiệp vụ về SoD và tính hợp lệ. | `Skill 10`, `Rule 04`, `Rule 05` kiểm tra việc thực thi chốt chặn an ninh và phòng chống bypass. |

Skill 11 **TUYỆT ĐỐI KHÔNG** tự cài đặt các cơ chế bảo mật hoặc thay thế các quy định trong `Rule 03`, `Rule 04`, `Rule 05`, `Rule 06`.

---

## 29. Domain vs Database Boundary

- **Skill 11 (Domain):** Định nghĩa ý nghĩa kinh doanh, mối quan hệ giữa các thực thể, các bất biến logic (ví dụ: tồn kho không được âm, hóa đơn đã xong là bất biến).
- **Skill 07 (Database SQL Server) & Rule 07:** Chịu trách nhiệm hiện thực hóa các bất biến đó thành các cấu trúc vật lý trên SQL Server (`CHECK (SoLuongTon >= 0)`, Foreign Keys `ON DELETE NO ACTION`, Unique Index, Triggers, RLS Security Policies).

Một bất biến miền có thể được bảo vệ ở tầng ứng dụng, tầng database, hoặc cả hai (Defense in Depth). Việc lựa chọn phương thức nào phải dựa trên bằng chứng kiến trúc dự án, không áp đặt cảm tính.

---

## 30. Domain vs API Boundary

- **Skill 11 (Domain):** Sở hữu khái niệm kinh doanh của việc "Đặt hàng", "Thanh toán", "Hoàn tiền".
- **Skill 06 (API Design) & Rule 08 (API Contract):** Quyết định việc đặt tên URI (`/api/v1/sale-orders`), phương thức HTTP (`POST`, `GET`), cấu trúc JSON Request/Response DTO, chuẩn phân trang (`page`, `pageSize`), và mã lỗi HTTP (`400 Bad Request`, `422 Unprocessable Entity`).

Skill 11 **KHÔNG ĐƯỢC** tự ý áp đặt tên trường DTO hoặc cấu trúc JSON trừ khi điều đó đã được chuẩn hóa trong hợp đồng API của dự án.

---

## 31. Domain vs Frontend / Mobile Boundary

Frontend (ReactJS) và Mobile (Flutter) là các ứng dụng giao diện trình diễn quy trình nghiệp vụ cho người dùng cuối:
- **Giao diện không phải nguồn chân lý nghiệp vụ (UI is NOT Domain Truth):**
  - Việc Frontend ẩn nút "Duyệt đơn" không chứng minh Backend đã chặn quyền duyệt đơn.
  - Việc Frontend kiểm tra form "Số lượng nhập > 0" không chứng minh Backend có kiểm tra điều này.
  - Việc Frontend hiển thị tổng tiền tự tính không chứng minh Backend sẽ chấp nhận số tiền do client gửi lên.
  - Việc Frontend cho phép chọn chi nhánh trên dropdown không chứng minh ngữ cảnh chi nhánh được tin cậy.
- **Ranh giới thực thi có thẩm quyền (Authoritative Enforcement Boundary):**
  - Business-critical rules must have an authoritative enforcement point appropriate to the approved architecture (các quy tắc nghiệp vụ trọng yếu phải có điểm thực thi có thẩm quyền phù hợp với kiến trúc đã được phê duyệt).
  - Client-side validation alone does not establish authoritative business correctness (kiểm tra hợp lệ phía client chỉ phục vụ trải nghiệm người dùng, không tạo nên tính đúng đắn nghiệp vụ có thẩm quyền).
  - Tầng Server / Application / Domain service chịu trách nhiệm thực thi các quy tắc và hành vi nghiệp vụ theo kiến trúc; Database enforcement có thể cung cấp cơ chế phòng thủ chiều sâu (defense-in-depth) tại các vị trí phù hợp, không bắt buộc mọi bất biến đều phải sao chép vật lý ở cả hai nơi (nhất quán với nguyên tắc tại Mục 29).

---

## 32. Domain Testing

Kiểm thử miền nghiệp vụ (Domain Testing) nhằm xác minh logic kinh doanh và tính toàn vẹn của quy trình hoạt động phù hợp với đặc tả yêu cầu và kiến trúc hệ thống.

### 32.1. Các chiều kích kiểm thử miền trọng yếu (Key Domain Test Dimensions & Illustrative Scenarios)
Các kịch bản kiểm thử dưới đây là các chiều kích kiểm thử tham khảo; kết quả kỳ vọng (expected outcomes) phải được xác định dựa trên đặc tả yêu cầu nghiệp vụ, hợp đồng API (`Rule 08`), cơ chế an ninh (`Rule 03`, `Rule 05`), kiến trúc giao dịch (`Rule 02`) và bộ kiểm thử hiện hành của dự án:

1. **Kiểm thử Bất biến nghiệp vụ (Invariants Testing):** Thử nghiệm các thao tác có nguy cơ vi phạm bất biến (ví dụ minh họa: mua quá số lượng tồn khả dụng, sửa đổi thông tin của chứng từ đã hoàn tất) và xác minh kết quả xử lý theo business rule và expected outcome đã được xác định bởi project requirements / domain specification.
2. **Kiểm thử Luồng hợp lệ & Không hợp lệ (Valid & Invalid Workflows):** Kiểm thử luồng quy trình bán hàng, nhập kho, đổi trả trong điều kiện bình thường và các kịch bản bất thường/gián đoạn giữa chừng nhằm đánh giá tính nhất quán dữ liệu.
3. **Kiểm thử Chuyển trạng thái (State Transition Testing):** Kiểm thử các bước chuyển trạng thái hợp lệ và xác minh việc ngăn chặn các bước chuyển trạng thái không được phép theo mô hình trạng thái của thực thể.
4. **Kiểm thử Giá trị biên (Boundary Conditions):** Kiểm thử các giá trị biên của số lượng tồn kho (ví dụ: xuất bán hết số lượng còn lại về 0) và kiểm thử các giá trị biên của chiết khấu trong phạm vi giá trị được business specification cho phép.
5. **Kiểm thử Tính nhất quán số học (Calculations & Consistency):** Kiểm tra độ chính xác của công thức chiết khấu, thuế, làm tròn tiền tệ, đối soát số dư tồn kho với sổ giao dịch kho theo đặc tả toán học của dự án.
6. **Kiểm thử Đổi trả & Hoàn tiền (Returns Consistency):** Kiểm thử các tình huống đổi trả một phần, đổi trả toàn bộ, hoặc trả hàng vượt quá số lượng mua ban đầu để đánh giá việc cập nhật tồn kho và xử lý dòng tiền theo chính sách dự án.
7. **Kiểm thử Nhận thức chi nhánh (Branch-Aware Business Scenarios):** Đảm bảo giao dịch của Chi nhánh A không làm ảnh hưởng hoặc thay đổi dữ liệu/tồn kho của Chi nhánh B (tuân thủ Rule 06).

*(Phương pháp luận kiểm thử chung tuân thủ `Skill 08`; Vòng lặp xác minh tuân thủ `Skill 09`).*

---

## 33. Domain Refactoring

Khi thực hiện tái cấu trúc mã nguồn liên quan đến miền nghiệp vụ dược:
1. **Xác định hành vi nghiệp vụ hiện hữu (Identify Existing Business Behavior):** Đọc code để hiểu chức năng đang phục vụ mục đích gì.
2. **Nắm bắt quy tắc miền thực tế (Capture Current Domain Rules):** Ghi nhận các điều kiện kiểm tra đang chạy.
3. **Phân biệt hành vi ngẫu nhiên và nghiệp vụ chủ đích (Separate Accidental from Intentional):** Một đoạn code lặp lại hoặc biến phụ có thể là giải pháp tình thế của lập trình viên, nhưng một lệnh `if (stock < requested) throw` là quy tắc nghiệp vụ chủ đích.
4. **Bảo toàn bất biến nghiệp vụ (Preserve Valid Business Invariants):** Không được làm suy yếu hoặc vô tình xóa bỏ các điều kiện kiểm tra nghiệp vụ khi tối ưu hóa code.
5. **Nhận diện hành vi chưa có tài liệu (Identify Undocumented Behavior):** Nếu code có một logic xử lý biên đặc biệt chưa được ghi trong tài liệu, phải ghi nhận lại để xác minh, không tự ý xóa bỏ.
6. **Không âm thầm thay đổi ngữ nghĩa nghiệp vụ (No Silent Semantic Changes):** Không tự ý đổi công thức tính tiền, đổi thứ tự trừ kho, hoặc đổi thông điệp lỗi nghiệp vụ.
7. **Cập nhật kiểm thử tương ứng (Update Tests Intentionally):** Khi nghiệp vụ có sự thay đổi chủ đích được phê duyệt, phải cập nhật test case đồng bộ.
8. **Tái xác minh liên tầng (Re-verify Cross-Layer Behavior):** Chạy lại bộ kiểm thử để đảm bảo việc refactor không gây lỗi hồi quy (regression) sang API hoặc Database.

> [!WARNING]
> "Mã nguồn trông sạch hơn (cleaner code)" không đồng nghĩa với "Mã nguồn đúng nghiệp vụ hơn". Đúng đắn về nghiệp vụ luôn luôn đứng trước sự thuận tiện trong lập trình.

---

## 34. Domain Discovery Checklist

Trước khi bắt tay vào triển khai một tính năng hoặc phân hệ nghiệp vụ dược mới, Agent bắt buộc phải thực hiện khảo sát toàn diện và ghi nhận trạng thái:

- [ ] **Requirements:** Đã rà soát yêu cầu nghiệp vụ chính thức chưa? (`FOUND` / `NOT FOUND` / `CONFLICTING`)
- [ ] **Existing ERD:** Đã kiểm tra sơ đồ dữ liệu hiện tại chưa? (`FOUND` / `NOT FOUND` / `NOT VERIFIED`)
- [ ] **Existing Database Schema:** Đã kiểm tra cấu trúc bảng và ràng buộc SQL thực tế chưa? (`FOUND` / `NOT FOUND` / `NOT VERIFIED`)
- [ ] **Existing API:** Đã rà soát các endpoints và DTOs liên quan chưa? (`FOUND` / `NOT FOUND` / `NOT VERIFIED`)
- [ ] **Existing Backend Services:** Đã kiểm tra mã nguồn tầng Application / Service chưa? (`FOUND` / `NOT FOUND` / `NOT VERIFIED`)
- [ ] **Existing Frontend / Mobile Flows:** Đã kiểm tra màn hình và luồng thao tác trên UI chưa? (`FOUND` / `NOT FOUND` / `NOT VERIFIED`)
- [ ] **Existing State Fields:** Các trường trạng thái (`status`, `state`) đã được định nghĩa ở đâu? (`FOUND` / `NOT FOUND` / `PROPOSED`)
- [ ] **Existing Tests:** Có test case nào cho nghiệp vụ này chưa? (`FOUND` / `NOT FOUND` / `NOT VERIFIED`)
- [ ] **Existing Audit Behavior:** Đã có ghi vết nhật ký cho hành vi này chưa? (`FOUND` / `NOT FOUND` / `NOT VERIFIED`)
- [ ] **Branch Relationships:** Mối quan hệ với thực thể Chi nhánh được thiết lập như thế nào? (`FOUND` / `NOT FOUND` / `PROPOSED`)
- [ ] **Existing Business Terminology:** Thuật ngữ trong code có khớp với thuật ngữ ngành dược của dự án không? (`FOUND` / `CONFLICTING` / `PROPOSED`)

---

## 35. Domain Quality Checklist

Bảng kiểm định chất lượng miền nghiệp vụ được sử dụng trong quá trình rà soát và kiểm toán:

| Khía cạnh kiểm tra (Area) | Trạng thái đánh giá (Status) |
|---|---|
| 1. Mục đích kinh doanh được xác định rõ ràng (Business purpose identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 2. Các Actor tham gia được định danh đầy đủ (Actors identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 3. Các thực thể miền được mô hình hóa chính xác (Domain entities identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 4. Các quy tắc nghiệp vụ được định nghĩa tường minh (Business rules identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 5. Các bất biến nghiệp vụ được bảo toàn (Invariants identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 6. Luồng quy trình được phân tích chi tiết (Workflow identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 7. Máy trạng thái và điều kiện chuyển đổi được xác định (State transitions identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 8. Ranh giới chi nhánh được tôn trọng đầy đủ (Branch scope identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 9. Biến động dữ liệu được truy vết toàn vẹn (Data changes traced) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 10. Sự phụ thuộc ủy quyền được nhận diện (Authorization dependency identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 11. Sự phụ thuộc giao dịch & khóa đồng thời được nhận diện (Transaction dependency identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 12. Sự phụ thuộc hợp đồng API được nhận diện (API dependency identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 13. Sự phụ thuộc ràng buộc cơ sở dữ liệu được nhận diện (Database dependency identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 14. Bộ ca kiểm thử nghiệp vụ được thiết lập (Tests identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 15. Bằng chứng xác minh độc lập được ghi nhận (Verification evidence identified) | `PASS` / `FAIL` / `NOT VERIFIED` |
| 16. Mọi mâu thuẫn nghiệp vụ được ghi nhận và giải quyết (Conflicts documented) | `PASS` / `FAIL` / `NOT APPLICABLE` |

---

## 36. Governance & Cross-Skill Boundary

Bản đồ phân định thẩm quyền giữa Skill 11 và hệ thống Quản trị (Rules 00–09):

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           RULES 00–09 (GOVERNANCE)                              │
│  - Rule 02: Transaction boundaries, Concurrency, Idempotency, Arch Quality      │
│  - Rule 03: Security, Cryptography, Secrets, Key Protection, Signing Security   │
│  - Rule 04: RBAC Model (Role, Permission, Resource, Action, Scope / WHO)        │
│  - Rule 05: Runtime Authorization Enforcement, IDOR defense (HOW)               │
│  - Rule 06: Branch Isolation Boundary, Session Context, RLS (WHICH DATA)        │
│  - Rule 07: Database Integrity, Constraints, Keys, Precision                    │
│  - Rule 08: API Contract, URIs, DTOs, HTTP status, Errors                       │
│  - Rule 09: Observability, Logging Hygiene, Metrics, Health Checks              │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │
         ┌───────────────────────────────┴───────────────────────────────┐
         ▼                                                               ▼
┌────────────────────────────────┐              ┌────────────────────────────────┐
│     TECHNICAL SKILLS 01–10     │              │        DOMAIN SKILL 11         │
│ - Skill 06: API Design         │              │        (PHARMA-DOMAIN)         │
│ - Skill 07: SQL Server Impl    │◄────────────►│ - Business Meaning & Concepts  │
│ - Skill 08: Testing Practices  │              │ - Domain Workflows & Actors    │
│ - Skill 09: Verification Loop  │              │ - State Models & Invariants    │
│ - Skill 10: Security Review    │              │ - Digital Signing Semantics    │
└────────────────────────────────┘              └────────────────────────────────┘
```

### Phân định trách nhiệm cụ thể:
- **Rule 02 (Architecture Quality):** Sở hữu ranh giới transaction, kiểm soát đồng thời, cơ chế idempotency và các mối quan tâm chất lượng kiến trúc liên quan đến quy trình ký số/chứng từ.
- **Rule 03 (Security):** Sở hữu an ninh mật mã, quản lý bí mật, bảo vệ khóa riêng tư và các khía cạnh an ninh kỹ thuật của chữ ký số.
- **Rule 04 (RBAC Model):** Sở hữu mô hình phân quyền vai trò (WHO: Role, Permission, Resource, Action, Scope).
- **Rule 05 (Authorization):** Sở hữu cơ chế thực thi kiểm soát truy cập runtime tại server-side (HOW: IDOR defense, state checks).
- **Rule 06 (Branch Isolation):** Sở hữu ranh giới cô lập dữ liệu chi nhánh và SQL Server RLS (WHICH DATA).
- **Rule 07 (Database Integrity):** Sở hữu toàn vẹn quan hệ, khóa chính, khóa ngoại, ràng buộc CHECK, Unique, kiểu dữ liệu tiền tệ/số lượng.
- **Rule 08 (API Contract):** Sở hữu thiết kế URI RESTful, DTO Request/Response, mã trạng thái HTTP, RFC 7807 Problem Details.
- **Rule 09 (Observability & Operations):** Sở hữu structured logging, correlation ID, metrics, health checks và quy trình khôi phục.
- **Skill 11 (Pharma Domain):** Sở hữu **Ý NGHĨA KINH DOANH** và yêu cầu miền của các quy trình nghiệp vụ dược phẩm, thực thể, bất biến và ngữ nghĩa nghiệp vụ của việc ký số chứng từ. Skill 11 tuyệt đối không sở hữu hoặc áp đặt việc triển khai mật mã kỹ thuật.

---

## 37. Final Self-Audit

> [!NOTE]
> **Ranh giới thẩm quyền của Self-Audit:**  
> Bảng tự kiểm toán này là quy trình kiểm tra chất lượng nội bộ (internal authoring quality check, structural check, pre-audit readiness check).  
> **Self-audit KHÔNG PHẢI là kiểm định độc lập (independent audit), KHÔNG PHẢI là bằng chứng triển khai mã nguồn (implementation evidence), KHÔNG PHẢI là bằng chứng runtime hay kiểm thử, và KHÔNG chứng minh rằng mọi khái niệm miền đã được hiện thực hóa trong code.**  
> Trạng thái "READY FOR FINAL AUDIT" chỉ xác nhận Skill 11 đã hoàn thành rà soát nội bộ và sẵn sàng cho đợt thẩm định độc lập tiếp theo.

Bảng tự kiểm toán phương pháp luận trước khi đưa Skill 11 vào vận hành, yêu cầu đánh giá thực tế theo từng tiêu chuẩn:

| STT | Tiêu chí rà soát (Audit Criterion) | Trạng thái (Status) | Ghi chú bằng chứng (Evidence Notes) |
|---|---|---|---|
| 1 | Cấu trúc đủ 37 mục cấp cao nhất (`## 1.` đến `## 37.`) | `PASS` | Kiểm tra thứ tự liên tục từ Mục 1 đến Mục 37, không thiếu mục nào. |
| 2 | Không trùng lặp số mục | `PASS` | Kiểm tra tính duy nhất của từng tiêu đề `## 1` đến `## 37`, không có mục trùng. |
| 3 | Tách bạch giữa nghiệp vụ và kỹ thuật | `PASS` | Ngữ nghĩa kinh doanh được phân định rõ ràng khỏi các cơ chế kỹ thuật. |
| 4 | Các khẳng định miền/pháp lý được gắn điều kiện phù hợp | `PASS` | Các khái niệm ETC/OTC, bảo quản lạnh, đơn thuốc, chữ ký số được gắn nhãn tham khảo miền hoặc phụ thuộc quy định áp dụng. |
| 5 | Không bắt buộc quy tắc nghiệp vụ khi chưa xác nhận | `PASS` | FEFO/FIFO và các quy trình vận hành (kể cả Sales Workflow) là mô hình tham chiếu/minh họa trừ khi có bằng chứng dự án. |
| 6 | Phân loại bất biến nghiệp vụ 3 cấp độ | `PASS` | Đã phân loại thành Confirmed, Domain Reference/Illustrative, và Proposed. |
| 7 | Giới hạn phạm vi mô hình máy trạng thái | `PASS` | Phân tích trạng thái áp dụng cho thực thể có vòng đời, không ép buộc mọi thực thể. |
| 8 | Ranh giới kiểm thử miền không gán cứng kết quả | `PASS` | Kiểm thử miền định hình theo test dimensions và kịch bản tham chiếu, phụ thuộc đặc tả. |
| 9 | Ranh giới thực thi máy chủ và cơ sở dữ liệu | `PASS` | Thẩm quyền thực thi tại server/application; database cung cấp defense-in-depth phù hợp. |
| 10 | Ranh giới chữ ký số và phân định an ninh | `PASS` | Skill 11 sở hữu ngữ nghĩa kinh doanh ký số; Rule 02 & Rule 03 sở hữu an ninh mật mã. |
| 11 | Phân định ranh giới quản trị và Rules 00–09 | `PASS` | Bản đồ phân định rõ thẩm quyền của Rules 00–09, Skills 01–10 và Skill 11. |
| 12 | Tính trung lập công nghệ (Technology Neutrality) | `PASS` | Không áp đặt ORM, framework web/mobile, thư viện mật mã hay kiến trúc cụ thể. |
| 13 | Bảo toàn hệ thống phân loại bằng chứng | `PASS` | Giữ nguyên các cặp trạng thái: NOT FOUND ≠ NOT IMPLEMENTED, NOT VERIFIED ≠ FAIL, v.v. |
| 14 | Phân định phạm vi chi nhánh (Branch Scope) | `PASS` | Dữ liệu chi nhánh và danh mục dùng chung tuân thủ tuyệt đối Rule 06. |
| 15 | Phục tùng hợp đồng API (Rule 08) | `PASS` | Ranh giới API tuân thủ hợp đồng và chuẩn DTO/HTTP của dự án. |
| 16 | Phục tùng toàn vẹn cơ sở dữ liệu (Rule 07) | `PASS` | Bất biến miền gắn kết với ràng buộc SQL theo kiến trúc được duyệt. |
| 17 | Phục tùng phương pháp luận kiểm thử (Skill 08) | `PASS` | Kiểm thử miền phối hợp với quy trình kiểm thử hệ thống. |
| 18 | Phục tùng vòng lặp xác minh (Skill 09) | `PASS` | Xác minh nghiệp vụ độc lập dựa trên bằng chứng vật lý. |
| 19 | Phân định trách nhiệm Actor với thẩm quyền RBAC/Auth | `PASS` | Trách nhiệm tham chiếu của Actor được tách bạch khỏi chính sách RBAC (Rule 04/Skill 12) và thực thi Authorization (Rule 05). |
| 20 | Phạm vi sửa đổi nghiêm ngặt (Strict File Scope) | `PASS` | Chỉ cập nhật file Skill 11, không tác động đến code, DB, Rules 00–09 hay Skills khác. |

---
**Trạng thái hoàn thành:** READY FOR FINAL AUDIT

