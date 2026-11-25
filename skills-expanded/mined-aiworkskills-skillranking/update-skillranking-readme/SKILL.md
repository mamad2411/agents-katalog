---
name: "update-skillranking-readme"
description: "从 clawhub 数据库重查并更新当前仓库 README.md（每类 Top 8）"
---

# Update Skillranking README

## 适用场景

- 用户要求“重查数据库并更新 README”
- 需要基于 `clawhub_skills` + `clawhub_skill_classifications` 重新生成榜单

## 成功标准

- 当前仓库 `README.md` 被覆盖为最新数据版本
- 每个主类输出 8 条，按 `stars desc, downloads desc, installs_current desc` 排序
- 链接统一为新窗口打开（`target="_blank"`）
- 不执行 `git commit` / `git push`（除非用户明确要求）

## 执行步骤

1. 从 `clawhub/.env` 读取 `DATABASE_URL`（及 SSL 配置）
2. 查询：
   - `clawhub_skills`（仅 `deleted_at IS NULL`）
   - `clawhub_skill_classifications`
3. 以 `COALESCE(c.primary_domain, '其他')` 分组，每组取 Top 8
4. 覆盖写入当前仓库 `README.md`
5. 回报结果与变更文件

## 参考命令（在 skillranking 仓库执行）

```bash
python3 << 'PY'
import os, ssl
from pathlib import Path
from urllib.parse import urlparse, unquote
from datetime import date
import pymysql

clawhub_env = Path('/Users/longsen/Documents/code/aiworkskills/clawhub/.env')
env = {}
for line in clawhub_env.read_text(encoding='utf-8').splitlines():
    line = line.strip()
    if line.startswith('export '):
        line = line[len('export '):]
    if not line or line.startswith('#') or '=' not in line:
        continue
    k, _, v = line.partition('=')
    env[k.strip()] = v.strip().strip('"').strip("'")

db_url = env.get('DATABASE_URL') or os.environ.get('DATABASE_URL')
if not db_url:
    raise SystemExit('DATABASE_URL missing')

scheme, _, rest = db_url.partition('://')
p = urlparse(f"{scheme.split('+',1)[0]}://{rest}")
cfg = dict(
    host=p.hostname,
    port=p.port or 3306,
    user=unquote(p.username) if p.username else '',
    password=unquote(p.password) if p.password else '',
    database=p.path.lstrip('/')
)
ssl_args = {}
if (env.get('DATABASE_SSL') or os.environ.get('DATABASE_SSL', '')).lower() in ('1', 'true', 'yes', 'on'):
    ctx = ssl.create_default_context()
    if (env.get('DATABASE_SSL_VERIFY') or os.environ.get('DATABASE_SSL_VERIFY', '1')).lower() in ('0', 'false', 'no', 'off'):
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    ssl_args['ssl'] = ctx

conn = pymysql.connect(charset='utf8mb4', autocommit=True, **cfg, **ssl_args)

PRIMARY_DOMAINS = [
    '视频内容创作','图像与设计','音频与语音','文档与办公','内容分发与营销','AI Agent 编排','AI Agent 基础设施',
    '软件开发与运维','网络安全与合规','数据采集与情报','金融投资与交易','电商运营与选品','旅行与本地服务','教育与学术','人力资源与协同','健康与生活顾问','其他'
]
ANCHORS = {
    '视频内容创作':'video-content','图像与设计':'image-design','音频与语音':'audio-speech','文档与办公':'docs-office',
    '内容分发与营销':'content-marketing','AI Agent 编排':'agent-orchestration','AI Agent 基础设施':'agent-infrastructure',
    '软件开发与运维':'devops-swe','网络安全与合规':'security-compliance','数据采集与情报':'data-intelligence',
    '金融投资与交易':'finance-trading','电商运营与选品':'ecommerce','旅行与本地服务':'travel-local','教育与学术':'education',
    '人力资源与协同':'hr-collaboration','健康与生活顾问':'health-lifestyle','其他':'other-misc'
}

sql = """
SELECT
  COALESCE(c.primary_domain, '其他') AS primary_domain,
  s.slug,
  COALESCE(NULLIF(TRIM(c.display_name_zh), ''), s.display_name) AS display_name,
  s.owner_handle,
  s.stars,
  s.downloads,
  s.installs_current,
  COALESCE(NULLIF(TRIM(c.summary_zh), ''), s.summary) AS summary,
  ROW_NUMBER() OVER (
      PARTITION BY COALESCE(c.primary_domain, '其他')
      ORDER BY s.stars DESC, s.downloads DESC, s.installs_current DESC
  ) AS rk
FROM clawhub_skills s
LEFT JOIN clawhub_skill_classifications c ON c.slug = s.slug
WHERE s.deleted_at IS NULL
"""

with conn.cursor() as cur:
    cur.execute(sql)
    rows = cur.fetchall()
conn.close()

by_domain = {d: [] for d in PRIMARY_DOMAINS}
for r in rows:
    domain, slug, name, owner, stars, dl, inst, summary, rk = r
    if domain not in by_domain:
        domain = '其他'
    if rk <= 8 and len(by_domain[domain]) < 8:
        by_domain[domain].append((slug, name, owner, stars or 0, dl or 0, inst or 0, (summary or '').replace('\n', ' ')))

lines = []
lines.append('# Clawhub 品类精选 Skill 清单 · Curated Agent Skills')
lines.append('')
lines.append('面向 <a href="https://clawhub.ai" target="_blank" rel="noopener noreferrer">Clawhub</a> 与 AI Agent / Codex / Cursor 等环境的精选 skill 推荐：按业务场景分品类，每类 8 条，综合站内星级（stars）、下载量、历史安装排序，便于按场景快速选用。')
lines.append('')
lines.append('> EN / for search: Curated Clawhub agent skills by use-case (8 per category), ranked by stars, downloads, and install history.')
lines.append('')
lines.append(f'- **清单生成日期**：{date.today().isoformat()}')
lines.append('')
lines.append('## 目录')
lines.append('')
lines.append('| 品类 | 锚点 |')
lines.append('|------|------|')
for d in PRIMARY_DOMAINS:
    a = ANCHORS[d]
    lines.append(f'| {d} | <a href="#{a}" target="_blank" rel="noopener noreferrer">#{a}</a> |')
lines.append('')
lines.append('---')
lines.append('')

for d in PRIMARY_DOMAINS:
    a = ANCHORS[d]
    lines.append(f'<a id="{a}"></a>')
    if d == '视频内容创作':
        lines.append(f'## {d}')
    else:
        lines.append('<details>')
        lines.append(f'<summary><strong>{d}</strong></summary>')
        lines.append('')
    items = by_domain.get(d, [])
    for idx, (slug, name, owner, stars, dl, inst, summary) in enumerate(items, start=1):
        url = f'https://clawhub.ai/{owner}/{slug}' if owner else f'https://clawhub.ai/{slug}'
        lines.append(f'### {idx}. <a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>')
        lines.append('')
        lines.append(f'- **热度**：⭐ {stars} · 下载 {dl} · 历史安装 {inst}')
        lines.append(f'- **简介**：{summary[:300] + ("..." if len(summary) > 300 else "")}')
        lines.append('')
    if d != '视频内容创作':
        lines.append('</details>')
        lines.append('')
    else:
        lines.append('---')
        lines.append('')

lines.append('## 本仓库 Star 趋势')
lines.append('')
lines.append('<a href="https://github.com/aiworkskills/skillranking/stargazers" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/github/stars/aiworkskills/skillranking?style=social" alt="GitHub Repo stars"></a> <a href="https://github.com/aiworkskills/skillranking/network/members" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/github/forks/aiworkskills/skillranking?style=social" alt="GitHub forks"></a>')
lines.append('')
lines.append('<a href="https://www.star-history.com/#aiworkskills/skillranking&Date" target="_blank" rel="noopener noreferrer"><img src="https://api.star-history.com/svg?repos=aiworkskills/skillranking&type=Date" alt="Star History Chart"></a>')

Path('README.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('README.md updated')
PY
```
