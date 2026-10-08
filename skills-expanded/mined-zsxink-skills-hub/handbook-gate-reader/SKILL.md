---
name: handbook-gate-reader
description: 当用户需要卡「目标读者读不读得下去」时调用（由 handbook-paper-writer 在 ④ 写作循环、四道技法门禁全过后调度）；以 book_brief 的读者画像身份通读 chapter_laid_out，产出读者卡点清单（理解/顺序/动机三维），打回 handbook-draft 或 handbook-outline。这是体验层门禁，补四道技法门禁的盲区。
---

# 真人读者门禁（handbook-gate-reader）

卡「体验层」：四道技法门禁（structure/plain/consistency/fact）查的是「技法是否落实」，本门禁查的是「目标读者当读物读一遍，卡不卡」。审稿 ≠ 试读——合规的章节读者照样可能读不下去。

## 唤醒条件

主技能在 ④ 写作循环、四道技法门禁（gate-structure → gate-plain → gate-consistency → gate-fact）全部通过后唤醒；或打回 draft / outline。

## 输入

- `book_brief` 的读者画像（谁在读、他卡在哪、非专家反差在哪）
- `chapter_laid_out`（本章定稿）
- 本章在 `outline` 中的位置（第几章、前后章是什么）

## 输出

`reader_verdict`：pass / 打回（附卡点清单），写回 `book_state.review_log`。

verdict 结构：
```
{ status: pass|reject,
  stuck_points: [
    { dim: comprehension|order|motivation,
      location: <章节/小节>,
      reader_says: <读者第一人称原话，如「我看到这里不知道为什么要学这个」>,
      owner_skill: handbook-draft|handbook-outline,
      fix_hint: <一句话> } ] }
```

## 引用原子（见 references/kernel_skills.md）

本技能**不拥有也不检查**任何 K 原子——它是横切体验检查，与技法门禁正交（同 anti-slop 先例：有自己的维度体系，不挤占原子编号）。

## 三个卡点维度

### 1) 理解卡点（comprehension）

以画像身份读，哪里有「字都认识，连起来不知道在说什么」的地方。典型：新概念出现但读者此时还没有理解它所需的前置知识；术语用了但画像读者没听过；句子逻辑跳步（A→C 缺了 B）。

**读者原话模板**：「§X 第 Y 段我读了两遍，还是不知道 Z 是什么」。

### 2) 顺序卡点（order）

哪里有「这个内容放这里，读者还没有足够的上下文接住它」的地方。典型：前置引用读者还没读过的章节（后向引用 OK，前向引用危险）；结论先于动机出现；难度曲线突然跳变。

**读者原话模板**：「§X 一上来就讲 W，可我连 V 都没见过」。

### 3) 动机卡点（motivation）

哪里有「读者不知道为什么要继续读」的地方。典型：一章读了一半还不知道这章能解决自己的什么问题；讲了机制没讲「这跟我有什么关系」；契约承诺了但迟迟不兑现。

**读者原话模板**：「读到 §X 中段我开始走神，不知道这章能帮我干什么」。

## 完成判定

- [ ] 以画像身份通读，模拟的是「没用过本书主题工具的新手」，不是作者、不是审者
- [ ] 每个卡点带「读者第一人称原话」（stuck_points 的 reader_says），不带 K 编号
- [ ] 卡点按 dim 分流：comprehension/motivation → handbook-draft；order → handbook-outline
- [ ] 全文无卡点 → pass；任一动机卡点 → reject（动机卡点是读者流失点，不妥协）

## 做法步骤

1. 从 `book_brief` 读读者画像，把身份切换到画像（「我是没用过 X 的开发者，我知道 Y，不知道 Z」）。
2. 按章节顺序通读，每到一段自问：「此刻的我知道 X 吗？我知道为什么要读这段吗？」
3. 卡住就记一条 stuck_point：位置 + 读者原话 + dim + owner_skill。
4. 读完按 dim 归类，产出 verdict。动机卡点一票否决；理解/顺序卡点允许 pass 但须在 review_log 留痕（供 ⑥ 修订参考）。

## 反例

- ❌ 以审者身份读：「本章 K05 小节标题合规」——这是技法门禁的活，不是读者门禁的活。
- ✅ 以读者身份读：「§03 我第一次见 PTC 这个词，前面两章都没出现过」——这是读者卡点。
- ❌ 卡点带 K 编号（「违反 K14」）——读者不知道 K14 是什么，读者只会说「我看不懂」。
- ✅ 卡点带读者原话（「我看到这里不知道为什么要学这个」）。
- ❌ 动机卡点记为 warning 放行。
- ✅ 动机卡点直接 reject，回 draft 补「这章能解决你的什么问题」。
