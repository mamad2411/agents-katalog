# XHS Topic Strategist Skill

## 1. Purpose

This is a cross-agent Skill for Xiaohongshu intelligent topic strategy and content planning. Any Agent that can read Markdown files may invoke this Skill directly.

This Skill is used to complete:

- Lightweight account profile reading
- Hotspot discovery or hotspot interpretation
- Niche matching
- Topic generation
- Topic scoring
- Xiaohongshu content planning
- Xiaohongshu tone and style optimization
- Risk review
- Markdown + JSON-like output

## 2. Recommended Input Mode

The default recommended input mode is:

```text
lightweight_account_profile:
User fills in a lightweight account profile table.
```

The account profile should include at least:

- 账号主赛道
- 细分赛道
- 账号定位
- 目标用户
- 用户核心痛点
- 内容风格
- 账号阶段
- 商业化目标
- 内容禁区
- 最近表现好的内容
- 不想做的内容
- 可用素材

## 3. Supported Input Modes

### A. lightweight_account_profile Mode, Default Recommended

The user fills in a lightweight account profile table. The Skill automatically obtains recent hotspots and generates topic plans.

### B. short_account_description Mode, Backup

The user provides only a one-sentence account description. The Agent may generate topics with low confidence.

### C. full_account_profile Mode, Advanced

Suitable for MCNs, teams, and refined account operations.

### D. account_url Mode, Optional Enhancement

Use only when the user explicitly provides an account homepage URL and the Agent can access public information.

If the homepage cannot be accessed, do not interrupt the task. Ask the user to fill in the lightweight account profile. If the user does not provide more information, continue with low confidence.

### E. user_provided_hotspots Mode, Optional

The user may provide hotspots, but this is not required.

## 4. Missing Input Handling

If information is missing, do not interrupt the task. Use safe defaults:

```text
output_count: 5
time_range: recent
content_format: mixed
account_stage: growth
hotspot_mode: live_search_or_evergreen
risk_level: cautious
```

If key account information is missing:

- First generate a low-confidence profile based on available information.
- Clearly mark: `账号画像置信度：低`.
- Do not fabricate account information.

## 5. Execution Protocol

The Agent must execute strictly in this order:

1. Read the lightweight account profile filled in by the user.
2. Identify the account main niche, sub-niche, target audience, and content restrictions.
3. If the user only provides `account_url`, read `ACCOUNT_DISCOVERY.md` and try to analyze the account profile.
4. If the account homepage is inaccessible, ask the user to fill in the lightweight account profile. If the user does not add information, continue with low confidence.
5. Determine the active niche.
6. Obtain hotspot candidates:
   - If the Agent has internet access, read `HOTSPOT_SOURCES.md` and automatically obtain recent hotspots.
   - If the Agent has no internet access, use Evergreen Mode.
   - If the user provides hotspots, prioritize user-provided hotspots.
7. Standardize hotspots.
8. Determine hotspot types.
9. Match hotspots to suitable niches.
10. Generate 20-50 candidate topics.
11. Score topics according to `SCORING_RULES.md`.
12. Select Top topics and backup topics.
13. Generate a content planning package for each selected topic.
14. Optimize Xiaohongshu tone and style according to `XHS_STYLE_GUIDE.md`.
15. Perform risk review according to `RISK_RULES.md`.
16. Output a Markdown report.
17. Output JSON-like structured results.
18. Mark all parts that require human confirmation.

## 6. Hotspot Handling Rules

The Agent must follow these rules:

- Do not fabricate real-time hotspots.
- Do not fabricate heat rankings.
- Do not claim to have fetched data that was not actually fetched.
- Mark unverifiable hotspots as `待核实`.
- If the Agent has no internet access, use Evergreen Mode.
- Evergreen Mode must be marked as: `非实时热点，基于常青需求生成`.

## 7. Account Discovery Rules

Refer to `ACCOUNT_DISCOVERY.md`.

The Agent must follow these rules:

- Account URL analysis is only an optional enhancement, not the default workflow.
- If the user has already filled in an account profile, prioritize the user-provided information.
- Do not fabricate account information.
- Do not claim to have read homepage information that was not actually read.
- If only partial information can be read, mark the account profile confidence level.
- If the homepage cannot be accessed, ask the user to provide the homepage bio or recent note titles.
- If the user does not provide more information, the Agent may generate based on minimal information, but must mark: `账号画像置信度：低`.

## 8. Topic Scoring

Refer to `SCORING_RULES.md`.

Use the following scoring formula:

```text
Total Score =
trend_heat × 15%
+ pain_point_strength × 20%
+ account_fit × 20%
+ search_value × 15%
+ differentiation × 10%
+ monetization × 10%
+ execution_cost_inverse × 5%
+ risk_inverse × 5%
```

The score is an internal planning score. It is not an official platform ranking and must not be described as one.

## 9. Risk Review

The following niches require mandatory risk review:

- 医美轻医美
- 财商理财
- 母婴育儿
- 亲子教育
- K12 教育
- 健康养生
- 护肤功效类
- 职场收入类
- 婚恋情感冲突类

The following are prohibited:

- 医疗诊断
- 投资收益承诺
- 提分承诺
- 产品绝对功效
- 焦虑式育儿
- 攻击品牌或个人
- 伪造个人体验
- 伪造平台排名

For high-risk content, prefer conservative rewriting and clear human review notes.

## 10. Output Requirements

Each selected topic must include:

- Topic
- Score
- Recommendation level
- Hotspot source
- Hotspot verification status
- Suitable niche
- Target audience
- User pain point
- Content angle
- Recommended format
- Commercial potential
- Risk level
- Title options
- Cover concept
- Note structure
- Draft copy
- Tags
- Comment prompt
- Risk notes
- Differentiation advice
- Human edits needed

The final response must include both:

1. A Markdown report
2. A JSON-like structured result

## 11. Human-in-the-Loop Boundary

This Skill may generate a planning package, but it must not automatically publish content.

The creator must provide or complete:

- Real experience
- Real images or videos
- Final fact-checking
- Final compliance judgment
- Publishing decision

## 12. Agent Behavior Rules

- Do not fabricate data sources.
- Do not fabricate heat rankings.
- Do not fabricate account information.
- Do not claim access to information that was not actually accessed.
- If uncertain, mark as `待核实`.
- For high-risk content, prefer conservative rewriting.
- Output must be executable, not generic advice.

