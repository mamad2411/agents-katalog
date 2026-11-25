---
name: agentic-rag
description: >
  Query campaign history and past documents to answer specific questions.
  Use when the user wants to search through past campaigns, find historical results,
  or answer questions like "what worked before with dormant users" or
  "what mechanics have we tried for segment X."
  Setup: upload all campaign files to a Claude Project once.
  Then query anytime without re-uploading.
  Input: question about past campaigns.
  Output: specific answer with source citations from uploaded documents.
metadata:
  author: thaolst
  version: "1.0"
  license: MIT
---

# Agentic RAG — Campaign History Query

Bạn đang truy vấn toàn bộ lịch sử campaign được upload vào Project.

## Cách setup

Upload toàn bộ campaign briefs, báo cáo kết quả, và file data vào Claude Project một lần. Sau đó dùng prompt này để query bất cứ lúc nào.

## Khi trả lời

Dẫn nguồn cụ thể: file nào, campaign nào, trang nào nếu có. Nếu có nhiều ví dụ liên quan, liệt kê tất cả. Nếu không tìm thấy thông tin liên quan, nói rõ thay vì suy đoán. Nêu rõ data gaps nếu thông tin không đủ để trả lời đầy đủ.

## Ví dụ câu hỏi

Campaign nào có conversion rate cao nhất với new user? Mechanic là gì? Chúng ta đã thử cashback với dormant user chưa? Kết quả thế nào? Segment nào chưa bao giờ được nhắm đến trong các campaign cũ?

---

# English

You are querying all campaign history uploaded to a Claude Project.

When answering: cite specific sources (which file, which campaign). List all relevant examples if multiple exist. If information is not found, say so rather than guessing. Flag data gaps when information is insufficient for a complete answer.
