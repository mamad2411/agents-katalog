---
name: ddd-strategic-design
version: 2.0.0
description: "Use when starting new projects, designing system architecture, identifying bounded contexts, mapping context relationships, system refactoring, system redesign, or when user mentions 'DDD', 'domain-driven design', 'bounded context', 'context mapping', 'microservices design', 'business modeling', 'system boundaries', 'domain thinking', '领域思维', '领域驱动', '重构项目', '重构系统', '重新设计系统', '优化重构系统'."

# 技能分类
category: "design"

# 复杂度标识
complexity: "high"

# 预计执行时长
typical_duration: "1hour"

# 依赖关系
dependencies: []
benefits-from: [goal-oriented, first-principles]
conflicts-with: []

# 工件配置
output_artifact: "memory/artifacts/ddd-strategic-design/"

# 工具权限
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob

# 标签（用于技能推荐）
tags:
  - "系统设计"
  - "架构设计"
  - "领域驱动设计"
  - "微服务"
  - "DDD"
---

# Domain-Driven Design: Strategic Design

## 前置协议

### 环境检测

```bash
# 检测当前项目信息
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "unknown")
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

echo "PROJECT: $PROJECT_ROOT"
echo "BRANCH: $BRANCH"
echo "COMMIT: $COMMIT"
```

### 前置技能检查

**benefits-from 检查**（推荐但非必须）：

```bash
# 检查 goal-oriented 工件
GOAL_ARTIFACT="memory/artifacts/goal-oriented/latest.json"

if [ -f "$GOAL_ARTIFACT" ]; then
  echo "FOUND: goal-oriented artifact"
  # 提取目标信息，确保设计符合目标
fi

# 检查 first-principles 工件
FP_ARTIFACT="memory/artifacts/first-principles/latest.json"

if [ -f "$FP_ARTIFACT" ]; then
  echo "FOUND: first-principles artifact"
  # 提取第一性原理分析结果，用于指导设计
fi
```

**工件目录初始化**：

```bash
# 确保工件目录存在
mkdir -p memory/artifacts/ddd-strategic
```

### 用户意图确认

根据用户消息判断：

**检查点**：
- [ ] 是否需要设计新系统或重构现有系统
- [ ] 是否涉及多个业务领域或团队
- [ ] 是否需要识别系统边界和上下文关系

**意图分类**：
1. **新系统设计**：从零开始设计系统架构
2. **系统重构**：将单体拆分为微服务
3. **架构优化**：重新梳理上下文边界
4. **业务建模**：梳理业务领域

## Overview

Strategic design focuses on defining bounded contexts and their relationships. A bounded context is a boundary within which a domain model is defined and applicable. Inside the boundary, all terms, rules, and logic have a specific, consistent meaning. Different contexts may use the same terms with different meanings.

**Why it matters:** Without clear boundaries, teams talk past each other. "Customer" means something different to Sales vs Support vs Billing. Strategic design makes these boundaries explicit.

**Core principle:** Language consistency within a boundary, explicit translation between boundaries.

Tactical design happens within each bounded context. See `ddd-tactical-design` skill for implementation details.

## When to Use

**Applicable:**
- Starting a new project or system
- Decomposing a monolith into microservices
- Multiple teams working on the same domain
- Domain logic is complex and domain experts are available
- Language confusion across teams (same term, different meanings)

**Not applicable:**
- Simple CRUD operations with minimal logic
- Single-team small projects (< 3 developers)
- Technical-only domains (no business experts needed)
- Existing well-defined bounded contexts

## The Process

```dot
digraph strategic_design {
    rankdir=TB;
    "Event Storming" [shape=box, style=filled, fillcolor="#c8e6c9"];
    "Identify Bounded Contexts" [shape=box, style=filled, fillcolor="#bbdefb"];
    "Define Context Map" [shape=box, style=filled, fillcolor="#fff9c4"];
    "Architecture Decisions" [shape=box, style=filled, fillcolor="#f8bbd0"];
    "保存工件" [shape=box, style=filled, fillcolor="#81c784"];

    "Event Storming" -> "Identify Bounded Contexts";
    "Identify Bounded Contexts" -> "Define Context Map";
    "Define Context Map" -> "Architecture Decisions";
    "Architecture Decisions" -> "保存工件";
}
```

### Step 1: Event Storming

Gather domain experts and developers. Use sticky notes to explore the domain:

**Domain Events** (orange): Something that happened
- "Order Placed", "Payment Processed", "Inventory Reserved"
- Write in past tense

**Commands** (blue): What triggers events
- "Place Order", "Process Payment", "Reserve Inventory"
- Write in imperative mood

**Aggregates** (yellow): What handles commands and emits events
- "Order", "Payment", "Inventory"

**External Systems** (pink): Outside dependencies
- "Payment Gateway", "Email Service"

**Actors** (green): Who initiates commands
- "Customer", "Admin", "System"

Process: Start with events, work backward to commands, identify what's needed.

### Step 2: Identify Bounded Contexts

Group related events, commands, and aggregates into contexts:

**Principles:**
- **Semantic consistency**: Same term means same thing within a context
- **Independent evolution**: Each context can change independently
- **Team alignment**: One team owns one context (Conway's Law)

**Questions to ask:**
- Where does language change? (Customer in Sales vs Support)
- Where can we draw a clean boundary?
- What can be deployed independently?
- What team owns this capability?

**Start coarse, refine later.** Too many contexts = integration complexity. Too few = coupling.

### Step 3: Define Context Map

Document relationships between contexts:

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Partnership** | Teams succeed or fail together | Tight coordination needed |
| **Customer-Supplier** | Downstream depends on upstream | Upstream serves downstream needs |
| **Conformist** | Downstream conforms to upstream | Upstream cannot be influenced |
| **Anti-Corruption Layer** | Downstream translates upstream model | Protect domain model purity |
| **Open Host Service** | Publish API for multiple consumers | Shared capability |
| **Shared Kernel** | Shared subset of model | Carefully controlled coupling |

**Draw the map:** Which contexts talk to each other? What patterns apply?

### Step 4: Architecture Decisions

Based on context map, decide:

- **Team structure**: One team per context (ideally)
- **Communication**: Synchronous (RPC) vs asynchronous (events)
- **Data ownership**: One context owns data, others subscribe
- **Deployment**: Monolith or microservices? Start monolith-first.

## Thinking Framework

Use this table during Event Storming:

| Question | What to Look For | Example |
|----------|------------------|---------|
| **What events?** | Business-critical things that happened | "OrderPlaced", "PaymentFailed" |
| **What triggers events?** | Commands from users or systems | "PlaceOrder", "RetryPayment" |
| **What boundaries?** | Where language changes | Sales "Customer" ≠ Support "Customer" |
| **Who owns what?** | Team responsibility boundaries | Team A: Orders, Team B: Inventory |
| **How do they communicate?** | Sync vs async, contracts | Events for loose coupling, RPC for tight |

**Bounded Context Checklist:**
- [ ] Language is consistent within the context
- [ ] Can evolve independently (deployable on own schedule)
- [ ] One team can own it (matches Conway's Law)
- [ ] Clear boundaries with other contexts
- [ ] Defined relationships on context map

## Examples

### Case 1: E-commerce System

**Event Storming reveals:**
- Events: OrderPlaced, InventoryReserved, PaymentProcessed, OrderShipped
- Commands: PlaceOrder, ReserveInventory, ProcessPayment, ShipOrder
- Aggregates: Order, Inventory, Payment, Shipment

**Bounded Contexts identified:**

1. **Order Context**
   - Language: Order, OrderItem, Customer (buyer), OrderStatus
   - Team: Order Management Team
   - Events: OrderPlaced, OrderCancelled

2. **Inventory Context**
   - Language: Product, Stock, Warehouse, Reservation
   - Team: Warehouse Team
   - Events: InventoryReserved, StockDepleted

3. **Payment Context**
   - Language: Payment, Transaction, PaymentMethod, Refund
   - Team: Finance Team
   - Events: PaymentProcessed, PaymentFailed

**Context Map:**
- Order → Inventory: Customer-Supplier (Order needs Inventory to reserve)
- Order → Payment: Customer-Supplier (Order needs Payment to process)
- Order publishes OrderPlaced event → Inventory subscribes (async)
- Payment publishes PaymentProcessed event → Order subscribes (async)

**Architecture:** Start as modular monolith. Deploy as microservices if teams scale.

### Case 2: Healthcare System

**Bounded Contexts:**

1. **Patient Management Context**
   - Language: Patient, MedicalRecord, Diagnosis
   - Team: Clinical Team

2. **Appointment Context**
   - Language: Appointment, Schedule, Availability, Slot
   - Team: Scheduling Team

3. **Billing Context**
   - Language: Invoice, Payment, Insurance, Claim
   - Team: Billing Team

**Context Map:**
- Patient Management → Appointment: Shared Kernel (Patient ID)
- Appointment → Billing: Customer-Supplier (Appointments trigger billing)
- Billing has Anti-Corruption Layer for Insurance Provider's external model

## Common Pitfalls

### Pitfall 1: Too Fine-Grained Contexts

**Mistake:** Creating a context for every aggregate or entity.

**Problem:** Excessive integration complexity. Every change touches multiple contexts.

**Solution:** Start with fewer, larger contexts. Split only when you feel coupling pain.

**Rule of thumb:** Can you deploy this independently without coordinating with 3+ other teams? If no, merge contexts.

### Pitfall 2: Ignoring Team Structure

**Mistake:** Designing contexts based on domain purity, ignoring Conway's Law.

**Problem:** One team owns multiple contexts → coupling. Multiple teams own one context → conflict.

**Solution:** Align context boundaries with team boundaries. One team, one context.

### Pitfall 3: Missing Anti-Corruption Layer

**Mistake:** Letting upstream context's model leak into downstream context.

**Problem:** Downstream model becomes polluted with concepts that don't fit its domain.

**Solution:** Add Anti-Corruption Layer. Translate upstream model to downstream model at the boundary.

**Example:** External "User" → ACL translates → Internal "AccountHolder" with different attributes.

## 后置协议

### 工件输出

保存战略设计结果到工件文件：

```bash
# 生成工件文件名
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARTIFACT_FILE="memory/artifacts/ddd-strategic/result-$TIMESTAMP.json"

# 写入工件
cat > "$ARTIFACT_FILE" <<EOF
{
  "skill": "ddd-strategic-design",
  "version": "2.0.0",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "project": "$PROJECT_ROOT",
  "branch": "$BRANCH",
  "commit": "$COMMIT",
  "input": {
    "user_request": "用户的原始请求"
  },
  "output": {
    "bounded_contexts": [
      {
        "name": "上下文名称",
        "language": ["术语1", "术语2"],
        "team": "团队名称",
        "events": ["Event1", "Event2"]
      }
    ],
    "context_map": {
      "Order → Inventory": "Customer-Supplier",
      "Order → Payment": "Customer-Supplier"
    },
    "architecture_decisions": [
      "Start as modular monolith",
      "Deploy as microservices when teams scale"
    ]
  },
  "next_skills": [
    "ddd-tactical-design",
    "mvp-first"
  ]
}
EOF

echo "ARTIFACT SAVED: $ARTIFACT_FILE"

# 创建 latest.json 符号链接
ln -sf "$ARTIFACT_FILE" memory/artifacts/ddd-strategic/latest.json
```

### 目标文件更新

如果存在目标文件，记录设计完成：

```bash
# 检查是否有 pending 目标
GOAL_FILE=$(ls -t memory/goals/*.md 2>/dev/null | head -1)

if [ -n "$GOAL_FILE" ]; then
  GOAL_STATUS=$(grep "状态：" "$GOAL_FILE" | awk '{print $2}')

  if [ "$GOAL_STATUS" = "pending" ]; then
    echo "Adding milestone: DDD 战略设计完成"

    # 使用 Edit 工具添加里程碑
  fi
fi
```

### 建议后续技能

根据设计结果，推荐后续技能：

**推荐格式**：
```markdown
## 后续建议

基于 DDD 战略设计结果，建议继续执行：

**推荐技能链**：
1. /ddd-tactical-design - 在限界上下文内进行战术设计
2. /mvp-first - 进行 MVP 功能筛选

**根据设计阶段选择**：
- **战术实现** → /ddd-tactical-design（设计聚合、实体、值对象）
- **功能规划** → /mvp-first（筛选 MVP 功能）
- **迭代执行** → /pdca-cycle（进入 PDCA 循环）

是否继续执行？
- A) 执行推荐的技能链
- B) 只执行第一个技能
- C) 不继续，结束当前任务
```

## References

- **Domain-Driven Design** by Eric Evans - The original DDD book
- **Implementing Domain-Driven Design** by Vaughn Vernon - Practical implementation guide
- **Event Storming** by Alberto Brandolini - Collaborative domain exploration
- **Context Mapping** patterns: https://www.infoq.com/articles/ddd-contextmapping/