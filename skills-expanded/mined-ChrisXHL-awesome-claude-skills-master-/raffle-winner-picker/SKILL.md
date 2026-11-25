---
name: raffle-winner-picker
description: 从列表、电子表格或 Google Sheets 中随机挑选赢家，用于赠品、抽奖和竞赛。确保公平、公正的选择并具有透明度。
---

# 抽奖赢家选择器

此技能从列表、电子表格或 Google Sheets 中随机选择赢家，用于赠品和竞赛。

## 何时使用此技能

- 运行社交媒体赠品活动
- 在活动中挑选抽奖赢家
- 随机选择调查或测试的参与者
- 从竞赛提交中选择赢家
- 公平分配有限的名额或资源
- 随机团队分配

## 此技能做什么

1. **随机选择**: 使用加密级随机选择
2. **多源**: 适用于 CSV, Excel, Google Sheets 或普通列表
3. **多个赢家**: 可以挑选一个或多个赢家
4. **防止重复**: 确保同一个人不能赢两次
5. **透明结果**: 清晰显示选择过程
6. **赢家详细信息**: 显示有关赢家的所有相关信息

## 如何使用

### 从 Google Sheets

```
Pick a random row from this Google Sheet to select a winner 
for a giveaway: [Sheet URL]
```

### 从本地文件

```
Pick 3 random winners from entries.csv
```

### 从列表

```
Pick a random winner from this list:
- Alice (alice@email.com)
- Bob (bob@email.com)
- Carol (carol@email.com)
...
```

### 多个赢家

```
Pick 5 random winners from contest-entries.xlsx, 
make sure no duplicates
```

## 示例

**用户**: "Pick a random row from this Google Sheet to select a winner for a giveaway."

**输出**:
```
正在访问 Google Sheet...
找到的总条目数: 247

正在随机选择赢家...

🎉 赢家已选出! 🎉

行 #142
姓名: Sarah Johnson
电子邮件: sarah.j@email.com
输入日期: March 10, 2024
评论: "Love your newsletter!"

选择方法: 加密级随机
时间戳: 2024-03-15 14:32:18 UTC

您想要:
- 挑选另一个赢家 (排除 Sarah)?
- 导出赢家详细信息?
- 挑选亚军?
```

**灵感来源:** Lenny 的用例 - 从他的订阅者 Slack 社区中挑选 Sora 2 赠品赢家

## 功能

### 公平选择
- 使用安全随机数生成
- 无偏见或模式
- 透明过程
- 可重复的种子 (用于验证)

### 排除
```
Pick a random winner excluding previous winners: 
Alice, Bob, Carol
```

### 加权选择
```
Pick a winner with weighted probability based on 
the "entries" column (1 entry = 1 ticket)
```

### 亚军
```
Pick 1 winner and 3 runner-ups from the list
```

## 示例工作流

### 社交媒体赠品
1. 从 Google Form 导出条目到 Sheets
2. "Pick a random winner from [Sheet URL]"
3. 验证赢家详细信息
4. 带有时间戳公开宣布

### 活动抽奖
1. 创建参加者姓名和电子邮件的 CSV
2. "Pick 10 random winners from attendees.csv"
3. 导出赢家列表
4. 直接通过电子邮件发送给赢家

### 团队分配
1. 拥有参与者列表
2. "Randomly split this list into 4 equal teams"
3. 审查分配
4. 分享团队名单

## 提示

- **记录过程**: 保存时间戳和方法
- **公开宣布**: 分享选择细节以保持透明度
- **检查资格**: 验证赢家是否符合竞赛规则
- **拥有备份**: 挑选亚军以防赢家不合格
- **导出结果**: 保存赢家列表以供记录

## 隐私与公平

✓ 使用加密级安全随机性
✓ 不可能操纵
✓ 记录时间戳以供验证
✓ 可以为第三方验证提供种子
✓ 尊重数据隐私

## 常见用例

- 时事通讯订阅者赠品
- 产品发布抽奖
- 会议门票抽奖
- Beta 测试员选择
- 焦点小组参与者选择
- 活动中的随机奖品分发
