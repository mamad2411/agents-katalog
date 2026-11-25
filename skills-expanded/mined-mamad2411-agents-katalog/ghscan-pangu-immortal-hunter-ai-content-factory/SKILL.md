# 微信公众号自动化工作流 (WeChat Official Account Automation Workflow)

本文档概述了自动化微信公众号内容创作的 5 个 Skill 的顺序执行流程。

## 工作流伪代码 (Workflow Pseudocode)

```python
def run_wechat_automation_workflow(initial_input):
    # 加载配置
    config = load_json("config.json")

    # 1. 选题 (Topic Selection)
    # 输入: 当前趋势, 细分领域
    # 输出: 选定的主题、切入角度、目标读者、拟定标题、关键词
    topic_output = execute_skill(
        name="Topic",
        input={
            "niche": initial_input.niche,
            "trends": initial_input.trends
        },
        config=config
    )

    # 2. 研究 (Research)
    # 输入: 选定的主题、关键词
    # 输出: 研究笔记、核心洞察、关键事实、来源、Twitter情报
    # 工具: 需要网页搜索、浏览器访问、Twitter猎取
    research_output = execute_skill(
        name="Research",
        tools=["web_search", "browser", "read_url", "twitter_hunter"],  # 新增 twitter_hunter
        input={
            "topic": topic_output.selected_topic,
            "keywords": topic_output.keywords,
            "twitter_config": config.twitter  # ← 传入 Twitter 配置
        },
        config=config
    )

    # 3. 结构化 (Structure)
    # 输入: 研究数据、目标读者、切入角度、语气
    # 输出: 文章大纲（含 hook、outline、closing）
    structure_output = execute_skill(
        name="Structure",
        input={
            "research_data": {
                "key_insights": research_output.key_insights,
                "notes": research_output.notes,
                "facts": research_output.facts
            },
            "target_audience": topic_output.target_audience,  # ← 从 Topic 传递
            "angle": topic_output.angle,                      # ← 从 Topic 传递
            "tone": config.account_tone
        },
        config=config
    )

    # 4. 写作 (Write)
    # 输入: 大纲、研究数据、目标读者、切入角度、开篇钩子、结尾设计
    # 输出: 完整初稿、实际字数、可读性评分
    write_output = execute_skill(
        name="Write",
        input={
            "outline": structure_output.outline,
            "hook": structure_output.hook,                    # ← 从 Structure 传递
            "closing": structure_output.closing,              # ← 从 Structure 传递
            "research_data": research_output.notes,
            "target_audience": topic_output.target_audience,  # ← 从 Topic 传递
            "angle": topic_output.angle,                      # ← 从 Topic 传递
            "length_constraints": config.article_length,
            "banned_words": config.banned_words
        },
        config=config
    )

    # 5. 封装 (Package)
    # 输入: 初稿、拟定标题、目标读者、语气
    # 输出: 最终标题、摘要、封面图提示词、嵌入图片的文章、SEO关键词
    final_package = execute_skill(
        name="Package",
        input={
            "draft": write_output.draft,
            "potential_titles": topic_output.potential_titles,  # ← 从 Topic 传递
            "target_audience": topic_output.target_audience,    # ← 从 Topic 传递
            "tone": config.account_tone
        },
        config=config
    )

    # 6. 发布 (Publish) - 推送到微信
    # 输入: 最终标题、摘要、完整文章
    # 输出: 推送状态、推送时间、消息ID
    if config.push.enabled:
        publish_output = execute_skill(
            name="Publish",
            input={
                "title": final_package.title,
                "summary": final_package.summary,
                "draft_with_images": final_package.draft_with_images,
                "pushplus_token": config.push.pushplus_token
            },
            config=config
        )

    return final_package, publish_output
```

## 数据流图 (Data Flow)

```
┌─────────┐
│  Topic  │
└────┬────┘
     │ selected_topic, keywords
     │ target_audience, angle, potential_titles
     ▼
┌──────────┐
│ Research │
└────┬─────┘
     │ key_insights, notes, facts, references
     ▼
┌───────────┐  ← target_audience, angle (from Topic)
│ Structure │
└────┬──────┘
     │ hook, outline, closing
     ▼
┌─────────┐  ← target_audience, angle (from Topic)
│  Write  │  ← research_data (from Research)
└────┬────┘
     │ draft, actual_word_count
     ▼
┌─────────┐  ← potential_titles, target_audience (from Topic)
│ Package │
└────┬────┘
     │ title, summary, draft_with_images
     ▼
┌─────────┐  ← pushplus_token (from config)
│ Publish │
└────┬────┘
     │ push_status, push_time, message_id
     ▼
  [推送完成]
```

## 数据传递原则 (Data Passing Principles)

1. **完整传递**: Topic 的输出（target_audience, angle, potential_titles）需要贯穿整个工作流
2. **层级聚合**: Research 的输出在 Structure 和 Write 阶段均被使用
3. **配置注入**: `config.json` 中的 tone、banned_words、article_length、push 注入到相关 Skill
4. **质量联检**: 每个 Skill 都有质量自检机制，确保输出符合预期
5. **可选推送**: Publish Skill 仅在 `config.push.enabled = true` 时执行

