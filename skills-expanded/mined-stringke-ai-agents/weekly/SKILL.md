---
name: weekly
description: 生成本周工作周报。仅在用户显式触发 /weekly 时执行，不自动运行。
disable-model-invocation: true
argument-hint: [可选补充说明，如"下周重点是支付模块上线"]
allowed-tools: Bash, Write, Read, Glob
---

# /weekly — 生成本周工作周报

按以下步骤依次执行，不要跳过任何步骤。

---

## 第一步：确定本周时间范围

```bash
DOW=$(date +%u)
MONDAY=$(date -v-$((DOW - 1))d +%Y-%m-%d)
TODAY=$(date +%Y-%m-%d)
echo "周一: $MONDAY"
echo "今天: $TODAY"

current="$MONDAY"
while [[ "$current" < "$TODAY" ]] || [[ "$current" == "$TODAY" ]]; do
  echo "$current"
  current=$(date -j -f "%Y-%m-%d" "$current" -v+1d +%Y-%m-%d)
done
```

---

## 第二步：收集本周日报

使用 Glob 工具查找 `~/docs/reports/*/report-daily-*.txt`，筛选本周一到今天范围内的日报文件。

使用 Read 工具逐个读取。

---

## 第三步：补充 /done 记录

对本周每一天，使用 Glob 工具查找 `~/docs/[DATE]/*.md`。

使用 Read 工具读取，用于补充没写日报那天的工作。

---

## 第四步：合并归纳生成周报

数据合并策略：
1. 以已有日报为主要素材
2. /done 记录补充遗漏
3. 合并去重

归纳规则：
- 将一周的工作按方向归纳
- 最终 3 到 6 条
- 每条一句话，简短直白
- 不写项目名
- 不写具体数字、不写技术名词
- 只描述做了什么事，用最通俗的话说
- 如果用户通过 $ARGUMENTS 提供了补充说明，融入对应板块

内容板块：
1. 「本周工作：」— 必填
2. 「需要协助：」— 可选，有则写，无则不写
3. 「下周计划：」— 可选，能推断则写，否则不写

好的周报示例：

```
本周工作：
1. 完成接口层时区统一和文档补充
2. 测试环境基础设施迁移
3. 数据映射层规范化重构
4. 代码质量全量复查与修复
```

---

## 第五步：写入文件

先创建目录：

```bash
mkdir -p ~/docs/reports/$(date +%Y-%m-%d)
```

使用 Write 工具将周报写入 `~/docs/reports/[TODAY]/report-weekly-[TODAY].txt`。

格式要求：
- 纯文本，不用任何 markdown 标记
- 每条用数字编号（1. 2. 3.）
- 板块之间空一行
- 没有内容的可选板块直接省略
- 不加日期、作者、页眉页脚
- 简洁直白，像在群聊里发消息

---

## 第六步：输出确认

完成后输出：

```
周报已生成：~/docs/reports/[TODAY]/report-weekly-[TODAY].txt
```

并将周报内容完整展示给用户，方便直接复制粘贴到群聊。
