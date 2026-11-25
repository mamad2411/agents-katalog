---
name: vietnamese-technical-writing
description: Use when drafting, reviewing, or rewriting Vietnamese prose in this Coppice repository — README.vi.md, Vietnamese website docs, and Vietnamese UI strings. On a style pass, leave commands, keys, URLs, permissions, and locked positioning unchanged. Not for other languages, product behavior, or end-user agent skills.
---

# Viết kỹ thuật tiếng Việt trong Coppice

## Phạm vi và nguyên tắc

Dùng cho nội dung tiếng Việt được giao biên soạn trong repo Coppice: hướng dẫn, README, giải thích, tài liệu tra cứu và lời giao diện. Đây là hướng dẫn tác giả **cục bộ trong repo**, không thay skill tiếng Anh, không phải thành phần sản phẩm chạy lúc thực thi, plugin marketplace hay skill toàn cục. Hướng dẫn không tự cấp quyền sửa, cài đặt hoặc xuất bản nội dung.

Mục tiêu là giúp người đọc hiểu đúng và làm đúng, không phải bắt chước một blogger, giả trải nghiệm cá nhân hay qua mặt bộ nhận diện AI. Không cố tình thêm lỗi, tiếng lóng hoặc câu vụng để có vẻ "do người viết".

Cơ sở: người rà soát đọc toàn bộ phần văn bản chính của 31 bài ứng viên, rồi giữ 30 bài có ngày xuất bản đầu tiên trước 2020-11-07, từ 7 nơi xuất bản và 8 danh tính được ghi công; phần lớn là bài giải thích/hướng dẫn trên blog. E03 bị loại vì lời giải thích bám bản dịch/chuyển thể tiếng Anh; N02 thay E03. Chỉ 30 bài được giữ mới được tính. E03 không phải căn cứ quy tắc, và không tính cả hai. Xem [repo-references.md](repo-references.md), [repo-reference-manifest.json](repo-reference-manifest.json) và [review-evidence.md](review-evidence.md). Đây không phải thống kê về mọi người viết tiếng Việt hay xác nhận tiếng mẹ đẻ của tác giả. E05 chỉ có bằng chứng về nơi xuất bản đã được biết đến, chưa xác nhận mức độ nổi tiếng riêng của người viết. Văn bản đang trực tuyến có thể đã được sửa sau ngày xuất bản; không phải mọi câu hiện tại đều được chứng minh là có trước 2020. Không dùng các bài cũ để suy ra chức năng Coppice hoặc lệnh hiện hành.

Các lựa chọn ngôn ngữ dưới đây được minh họa trong nguồn. Bố cục riêng cho README/UI, giọng sản phẩm, giữ nguyên chuỗi kỹ thuật và đặt cảnh báo sát thao tác là **quy ước biên tập/an toàn của tài liệu**, không phải kết luận rằng cả 30 tác giả đều làm như vậy.

## Nơi áp dụng

Dùng skill này khi sửa tiếng Việt trong repo này:

- [README.vi.md](../../../README.vi.md)
- Tài liệu tiếng Việt trong [website/src/content/docs/vi/](../../../website/src/content/docs/vi/)
- Chuỗi giao diện tiếng Việt trong [website/src/i18n/pages/vi.ts](../../../website/src/i18n/pages/vi.ts) và [website/src/i18n/ui/vi.ts](../../../website/src/i18n/ui/vi.ts)

Skill nằm ở `.agents/skills/vietnamese-technical-writing/`. `.claude/skills` trỏ tới cùng thư mục, nên agent nào làm việc trong repo này cũng nạp được. Không chép sang thư mục `skills/` ở gốc repo, `server/builtin-plugins/` hay `server/marketplace/`. Đó là layout skill mà server có thể đưa vào agent của người dùng cuối.

Skill tiếng Anh là [english-technical-writing](../english-technical-writing/SKILL.md). Không áp thói quen tiếng Anh sang tiếng Việt, và không dùng skill này để sửa văn tiếng Anh. Tiếng Trung giản thể có skill riêng: [zh-cn-technical-writing](../zh-cn-technical-writing/SKILL.md). Tiếng Trung phồn thể Đài Loan có skill riêng: [zh-tw-technical-writing](../zh-tw-technical-writing/SKILL.md). Tiếng Trung phồn thể Hồng Kông có skill riêng: [zh-hk-technical-writing](../zh-hk-technical-writing/SKILL.md). Tiếng Nhật có skill riêng: [ja-technical-writing](../ja-technical-writing/SKILL.md). Tiếng Pháp có skill riêng: [fr-technical-writing](../fr-technical-writing/SKILL.md). Các ngôn ngữ khác vẫn chờ vòng nghiên cứu riêng; không phác chúng từ skill này.

Khi chỉ sửa văn phong, giữ nguyên định vị đã khóa trong [docs/milestones/M12-beta-release.md](../../../docs/milestones/M12-beta-release.md) và [docs/web/DESIGN.md](../../../docs/web/DESIGN.md), nhãn Beta, cùng tên cổng **Plan Review** và **Wait for Human Review**.

## Trước khi sửa

1. Xác định người đọc, loại văn bản và việc họ cần hiểu/làm. Đọc thuật ngữ và quy ước đang có trong repo; ưu tiên chúng hơn sở thích cá nhân.
2. Ghi lại điều không được đổi: ai làm gì, đối tượng nào, điều kiện/phạm vi, thứ tự, số lượng, phủ định, mức chắc chắn, quyền hạn và cảnh báo. Phân biệt sự thật đã được cung cấp với chỗ chưa biết.
3. Giữ nguyên các tên và chuỗi kỹ thuật cần khớp chính xác (literal): API, tên biến, khóa cấu hình, đường dẫn, lệnh, cờ, số phiên bản, mã lỗi và nhãn giao diện được trích dẫn. Chỉ sửa kỹ thuật khi nhiệm vụ cho phép và có căn cứ. Phát hiện lệnh có vẻ sai/nguy hiểm thì báo riêng, không đoán cách sửa rồi coi đó là sửa văn phong.

## Mười hai quy tắc

### 1. Cho người đọc biết mục đích và phạm vi đủ sớm

Nói rõ đoạn này giúp làm gì và cần biết/có gì trước đó. Với một thao tác, nêu điều kiện liên quan trước bước cần dùng. Bài giải thích có thể mở bằng tình huống nếu nó thực sự giúp hiểu vấn đề; không ép mọi bài thành câu trả lời cụt ngay đầu. [H01, H04, M03; đối chiếu phần dẫn M02, T02]

### 2. Để người đọc nhận ra ai làm gì

Gọi đúng thành phần khi chúng có vai trò khác nhau: người dùng chọn, máy chủ kiểm tra, worker xử lý. Khi đổi tác nhân, nhắc lại tên thay vì nối nhiều "nó".

Câu có chủ đề như "Với bộ nhớ đệm này, …", "Riêng bước nhập dữ liệu, …" là tự nhiên nếu phần sau rõ nghĩa. Không bắt mọi vế lặp một chủ ngữ. Dùng bị/được khi đối tượng chịu tác động đáng chú ý hơn hoặc tác nhân chưa được xác định; đừng tự bổ sung tác nhân để biến câu bị động thành chủ động. [H03, G02, T05]

### 3. Giữ đúng điều kiện, kết quả và mức khẳng định

Nối rõ "nếu/khi… thì…", "chỉ… khi…", "trước/sau…". Không biến điều kiện đủ thành điều kiện cần, hoặc ngược lại. Giữ phạm vi hệ điều hành, phiên bản, quyền và môi trường ở đúng kết luận mà chúng giới hạn. [E02, E04, M01]

**Bất biến khi sửa:** phải ≠ nên ≠ có thể; không ≠ chưa; không bảo đảm ≠ chắc chắn có lần thất bại. "Có thể nhanh hơn" không thành "sẽ nhanh hơn". Không bỏ sẽ/đã/đang/chưa chỉ để rút gọn nếu chúng mang thông tin thời gian/trạng thái.

### 4. Chọn quan hệ xưng hô có chủ đích

Tài liệu sản phẩm thường có thể viết trung tính; dùng "bạn" khi cần chỉ rõ người đọc. Không mở mọi bước bằng "Bạn hãy…". Trong bài có tác giả thực sự, tôi/mình có thể phù hợp; không áp đặt mình là cách xưng hô duy nhất tự nhiên. [M01, M02, C03, N01]

Giữ vai người nói và người nghe nhất quán theo ngữ cảnh, không đếm số lần đổi đại từ. Không bịa "mình đã thử", "đội ngũ chúng tôi thường…" hay kinh nghiệm của người được trích dẫn.

### 5. Lược phần đã rõ, không lược trách nhiệm

Có thể viết "Chạy `git status`, rồi đọc danh sách tệp đã thay đổi" khi cả hai việc đều do người đọc làm. Nếu bước sau do máy chủ hoặc tiến trình khác thực hiện, nêu lại tác nhân. Không bỏ tên đối tượng trong cảnh báo có thể bị tách ra khỏi đoạn. [E02, G03, T01]

### 6. Chia theo tải thông tin, không theo số từ

Một bước chỉ dẫn nên dễ theo dõi. Một câu giải thích vẫn có thể dài nếu điều kiện và lập luận cần đi cùng nhau. Tách khi người đọc phải giữ quá nhiều đối tượng hoặc phạm vi; không tách làm rơi "nếu", "chỉ", "trên Linux" hay nguyên nhân của kết quả. [M01, H06, N01]

Không đặt trần độ dài bằng cách đếm khoảng trắng: khoảng trắng tiếng Việt còn phân tách âm tiết. Đọc lại thành lời để nghe nhịp; không vì muốn câu ngắn mà cắt mất nội dung.

### 7. Dùng từ nối đúng quan hệ

Dùng "nhưng/tuy nhiên" khi có đối lập, "vì/do đó/nên" khi có nguyên nhân hoặc suy ra, "trong khi" khi so sánh. Nếu chưa có quan hệ ấy, đừng thêm từ nối cho trơn. "Và", "Vậy" đầu câu không tự động là lỗi; "Tuy nhiên" cũng không phải dấu hiệu văn máy. [H01, E05, M02]

### 8. Lặp đúng thuật ngữ thay vì đổi tên cho đẹp

Kết quả không nhất thiết là giá trị trả về; bộ nhớ đệm không phải dữ liệu được lưu trong nó; Promise không phải mảng chứa Promise. Dùng cùng tên cho cùng khái niệm. Có thể dùng đại từ hoặc cách gọi tương đương sau khi đã xác định rõ, nhưng không đổi danh từ khi điều đó làm mờ tham chiếu. [H03, G02, T03]

### 9. Chọn động từ rõ; giải thích thuật ngữ cần thiết

Ưu tiên "cài", "kiểm tra", "lưu" hơn "thực hiện việc cài đặt/kiểm tra/lưu" khi nghĩa không đổi. Không cấm mọi việc/sự hoặc từ Hán–Việt: cách diễn đạt phải hợp nghĩa và quy ước lĩnh vực. [T01, T03]

Với thuật ngữ khó dịch, dùng thuật ngữ dự án đã chọn; có thể chú thích tên tiếng Anh ở lần đầu để tra cứu. Nếu chưa có cách dịch ổn định, giữ tên tiếng Anh và giải thích vai trò bằng tiếng Việt, đừng ép dịch từng chữ. Không loại thuật ngữ đã được chấp nhận chỉ vì một tác giả không thích nó. [M03; quan điểm riêng ở M04 không phải chuẩn thuật ngữ]

### 10. Giữ nguyên tên và chuỗi kỹ thuật; giải thích vai trò

Không đổi tên API, chuỗi ký tự, lệnh hoặc cấu hình để câu "thuần Việt". Giải thích đầu vào, đầu ra, tác dụng và giới hạn bằng lời quanh chúng. Ví dụ cũ có thể sai; dẫn nguồn không thay thế kiểm tra kỹ thuật. [E02, E05, T05]

Nếu nhiệm vụ chỉ sửa văn phong, nhãn UI/thông báo được trích dẫn phải khớp sản phẩm. Nếu được giao sửa chính lời UI, nhãn đó là nội dung có thể sửa: cập nhật các chỗ tham chiếu tương ứng và vẫn giữ mã/định danh không thuộc phạm vi sửa.

### 11. Cho ví dụ đủ nhỏ và nói rõ nó chứng minh điều gì

Khi cần, đưa đầu vào/thao tác, kết quả dự kiến và lời giải thích. Phân biệt kết quả quan sát ở một ví dụ với bảo đảm chung; tách lời quảng cáo được dẫn lại khỏi nhận xét hay kết quả của tác giả. Nếu đề bài không cung cấp hành vi sản phẩm, ghi giả định hoặc hỏi lại thay vì bịa ví dụ như một tính năng thật. [H02, E05, M02, N02]

Ví dụ lỗi có chủ đích trong bài dạy kiểm thử được phép nếu ghi rõ mục đích và kết quả mong đợi. Điều đó khác với cố tình thêm lỗi văn bản hoặc lỗi lệnh để giả phong cách con người.

### 12. Giữ giọng bình tĩnh, giới hạn và cảnh báo

Không cần sao chép chuyện đùa, tục ngữ chế, giọng quảng cáo hay phán đoán tuyệt đối của blog. Nêu đánh đổi và điều chưa kiểm chứng. Đừng làm một câu cảnh báo "nhẹ nhàng hơn" bằng cách giảm mức nguy hiểm hoặc bỏ trách nhiệm. [C04, H01, H05, M01]

Theo quy ước an toàn, đặt cảnh báo trước/sát thao tác có hậu quả; đây là lựa chọn biên tập, dù nhiều nguồn để hạn chế ở cuối bài. Mất kết nối không chứng minh yêu cầu chưa được lưu; chỉ hướng dẫn thử lại khi đã có căn cứ cho thấy làm vậy an toàn.

## Áp dụng theo loại văn bản

Đây là cách chuyển các nguyên tắc vào Coppice, không phải các thể loại đã được khảo sát đại diện:

- **README:** cho biết mục đích, đối tượng, điều kiện chạy và các bước tối thiểu để dùng thử; dẫn tới giải thích dài hơn. Không thêm lời hứa hiệu năng.
- **Hướng dẫn:** điều kiện → bước → kết quả kiểm tra; gọi rõ thành phần ở mỗi lần đổi tác nhân; cảnh báo trước bước gây tác động.
- **Tra cứu:** dễ quét; tên chính xác, kiểu/giá trị mặc định/phạm vi chỉ ghi khi có dữ kiện; không hy sinh điều kiện để ép mỗi mục thành một câu.
- **Trang giới thiệu:** nói rõ ích lợi và giới hạn có căn cứ; không lấy lời khen chung thay cho hành vi cụ thể.
- **UI/lỗi:** ngắn nhưng giữ trạng thái biết/chưa biết, đối tượng và mức nghiêm trọng. Chỉ nêu hành động khôi phục đã được xác nhận an toàn.

## Ví dụ biên tập tổng hợp

Đây là các dữ kiện giả định dùng để thử cách biên tập, **không mô tả tính năng Coppice**.

- Cho biết: ứng dụng sẽ chỉ lưu `config.json` khi người dùng bấm nhãn "Lưu". Viết: "Ứng dụng sẽ chỉ lưu tệp `config.json` khi bạn bấm Lưu." Giữ sẽ, chỉ, điều kiện và nhãn.
- Cho biết: trên Linux có thể khởi động nhanh hơn, phụ thuộc dữ liệu, không có bảo đảm cho mọi lần chạy. Viết: "Trên Linux, tính năng này có thể giảm thời gian khởi động. Tuy nhiên, kết quả trên Linux còn phụ thuộc vào dữ liệu nên không có bảo đảm rằng lần chạy nào cũng nhanh hơn." **Không** đổi thành "không phải lần chạy nào cũng nhanh hơn": câu đó khẳng định đã có ngoại lệ.
- Cho biết: kết nối thất bại; người nói không biết chắc yêu cầu đã được lưu. Viết: "Không kết nối được. Chúng tôi không biết chắc yêu cầu đã được lưu hay chưa." Không đổi thành chưa lưu hoặc thêm lời mời thử lại.
- Cho biết: tệp trong `out/` sẽ bị ghi đè khi xuất; phải sao lưu tệp cần giữ trước đó. Viết: "Các tệp hiện có trong `out/` sẽ bị ghi đè khi xuất dữ liệu. Phải sao lưu các tệp cần giữ trước khi xuất." Câu bị động ở đây giữ đúng điều chưa xác định về tác nhân.

## Rà soát trước khi giao

- So từng ý trước/sau: cùng tác nhân, đối tượng, chuỗi kỹ thuật, số lượng, phạm vi và thứ tự?
- Còn nguyên chỉ/mọi/ít nhất, phủ định, trạng thái, phải/nên/có thể và điều chưa biết?
- Có chỗ lược chủ ngữ khiến không rõ ai làm? Có đổi thuật ngữ khiến tưởng là khái niệm khác?
- Có thêm tính năng, quan hệ nhân quả, hiệu năng, bảo đảm an toàn hoặc bước khôi phục không có căn cứ?
- Đọc thành lời: nhịp có tự nhiên, câu dài có cần thiết, câu ngắn có làm đứt điều kiện không?
- Nếu mâu thuẫn kỹ thuật chưa giải quyết được, ghi rõ để người phụ trách kiểm tra. Không che nó bằng câu văn trôi chảy.
