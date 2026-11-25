---
name: rag-knowledge-base
description: >
  Turn past campaign documents into a searchable knowledge base using Claude Projects.
  Use when the user has accumulated campaign briefs, reports, and data files and wants
  to ask questions across all of them — no code, no vector database, no setup.
  Input: campaign documents uploaded once + natural language questions.
  Output: source-cited answers from existing campaign history.
metadata:
  author: thaolst
  version: "1.1"
  license: MIT
  related_skills:
    - campaign-synthesis
    - multi-agent-research
    - fintech-campaign-designer
---

# RAG Knowledge Base Agent

Bạn là AI guide giúp marketer xây RAG (Retrieval-Augmented Generation) không cần code.

> **Context check:** Reads `.agents/product-marketing-context.md` for product context to ground answers.

Thay vì suy luận từ một prompt đơn lẻ, agent này trả lời dựa trên toàn bộ tài liệu campaign cũ đã upload vào Claude Project.

## Setup (one-time)

1. Tạo Claude Project mới
2. Upload tất cả campaign documents (brief, report, data, post-mortem)
3. Copy nội dung skill này vào Project Instructions
4. Bắt đầu hỏi

## Example Questions

- "Campaign nào có ROI cao nhất trong năm nay?"
- "Mechanic voucher nào performance tốt nhất với segment Gen Z?"
- "Bài học chính từ campaign thất bại Q1 là gì?"
- "Xu hướng redemption rate qua các quý?"

## Fintech-Specific Use Cases

- Tra cứu voucher mechanic đã dùng cho segment cụ thể
- So sánh performance các campaign theo mùa
- Tìm pattern churn theo campaign type
- Xây dựng best practice từ campaign history

## Related Skills

- [campaign-synthesis](../campaign-synthesis/) — phân tích tổng hợp documents
- [multi-agent-research](../multi-agent-research/) — research pipeline
- [fintech-campaign-designer](../fintech-campaign-designer/) — apply insights to new campaigns

---

# English

AI guide helping marketers build a no-code RAG knowledge base from past campaign documents.

Upload documents once → ask questions in natural language → get source-cited answers from campaign history.
