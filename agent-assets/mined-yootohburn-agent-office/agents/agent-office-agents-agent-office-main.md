# AGENTS.md

## Project overview

Agent-office is an AI-assisted affiliate commerce operating system for Thai short-form content.

The system helps select products, build trust-based content, and measure results. It is NOT an AI spam factory. It is NOT a fully automated system. Human approval is required before any content is published.

## The 6 production agents

### 1. ฝ่ายวิจัยสินค้า (product-research)
Collects and normalizes product opportunities. Checks category, price, seller info, rating, sold count, review count. Identifies product risk and short-form content fit.

### 2. ฝ่ายวิเคราะห์กำไรและข้อเสนอ (offer-analyst)
Scores commission potential, price attractiveness, and profit opportunity. Checks return/refund risk. Decides whether a product is worth promoting.

### 3. ฝ่ายกลยุทธ์คอนเทนต์ (content-strategy)
Selects audience, product angle, hook framework, and CTA. Decides platform mix: TikTok, Shopee Video, Lazada Live, Facebook, IG, YouTube Shorts.

### 4. ฝ่ายสคริปต์และสตอรี่บอร์ด (script-writer)
Creates 20–30 second Thai video scripts with scene-by-scene storyboard, caption draft, on-screen text, and shot list. No hallucinated specs. No overclaiming.

### 5. ฝ่ายผลิตชิ้นงาน (creative-production)
Prepares Canva/CapCut-ready creative brief. Suggests thumbnail layout, image/video asset structure, comparison cards, and edit-ready asset checklist.

### 6. ฝ่ายโซเชียลและวิเคราะห์ผล (social-performance)
Prepares post versions for each platform. Manages hashtag sets, pinned comment text, and UTM links. Tracks performance. Recommends scale/pause/revise. Feeds results back to Product Research.

## Approval and compliance

- Human Approval Gate (`human_approved` stage): mandatory before publishing. No automation bypasses this stage.
- Compliance checkpoint is built into the workflow — risk_flags are checked at every stage.
- CEO / Executive Dashboard: reviews and approves the full workflow before publish. Not a production agent — a human oversight role.

## Platforms (channels, not departments)

Shopee, Lazada, and TikTok are revenue channels — not departments. Each campaign/product is assigned to one primary channel.

## Pipeline stages (11 total)

| ID | Thai label | Owner |
|---|---|---|
| `new_product` | รับสินค้าใหม่ | product-research |
| `verified` | ยืนยันข้อมูลสินค้า | product-research |
| `scored` | ประเมินคะแนน | offer-analyst |
| `selected` | เลือกโปรโมท | offer-analyst |
| `brief_ready` | Brief พร้อม | content-strategy |
| `script_ready` | Script พร้อม | script-writer |
| `asset_ready` | ชิ้นงานพร้อม | creative-production |
| `human_approved` | รอผู้บริหารอนุมัติ | social-performance |
| `published` | โพสต์แล้ว | social-performance |
| `analyzed` | วิเคราะห์ผลลัพธ์ | social-performance |
| `learned` | บันทึกบทเรียน | product-research |

## Repository structure

```text
AGENTS.md
CLAUDE.md

.claude/
  agents/

src/
  agents/
    agentRegistry.ts
    campaignRegistry.ts
    agentTaskRouter.ts
    campaignWorkflow.ts
    mockWorkflowEngine.ts
    agentSessionStore.ts
    agentChatRouter.ts
    productRegistry.ts
    contentFramework.ts
    companyGoals.ts
    financeRegistry.ts
    platformRegistry.ts
  components/
    AgentOffice/

docs/
prototypes/
```
