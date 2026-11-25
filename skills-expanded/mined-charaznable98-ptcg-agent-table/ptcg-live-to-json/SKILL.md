---
name: ptcg-live-to-json
description: 将 PTCG Live 文本卡表（数量、英文卡名、系列码、编号）通过 duanxr 简中卡牌数据转换为本项目可导入的卡组 JSON。用户提供 Live 导出代码、分享卡表并要求转换或导入时使用；只有微信小程序卡组 ID 时需取得实际卡表。
---

# PTCG Live 卡表转简中 JSON

交付当前仓库 `DeckSchema` 接受的 `name + cards[{count,card}]`，保留输入顺序和每项数量。简中卡文来自 [duanxr/PTCG-CHS-Datasets](https://github.com/duanxr/PTCG-CHS-Datasets) 及所选简中原卡图。英文卡牌资料只用于识别系列/编号和交叉核对数值，不用翻译文本替代简中说明文。

## 转换

从仓库根目录工作。先读项目 `AGENTS.md` 和 [本地规则入口](../../../rules/README.md)；数据结构以 [运行期 CardSchema / DeckSchema](../../../packages/protocol/src/cards.ts) 为准。脚本使用 Python 3 标准库；GitHub API 限流时通过 Git 查询远端 HEAD，不克隆仓库。验证使用项目 Node.js 与现有 npm 依赖。

1. 将用户给出的完整卡表保存为本次 `source.txt`。支持 `#` 注释、Live 的宝可梦/训练家/能量分区头和 `Total Cards:` 页尾。小程序 ID 仅是来源标记，不能由 ID 凭空还原卡表。
2. 转换器优先检查 `data/import-cache/duanxr/`：缓存缺失时从 GitHub 获取 duanxr `main` 的最新提交，再按该提交下载 `ptcg_chs_infos.json`，仅获取本次所需卡图。英文参考从索引指定的 GitHub 提交按系列下载。已有缓存可离线复用；需要更新简中数据时加 `--refresh`。数据、英文参考及卡图均核对散列并留在被 Git 忽略的缓存，不克隆上游仓库，也不将完整数据当成应用卡池。
3. 运行转换工具，使用新的审计目录，避免改写旧证据：

```sh
python3 .agents/skills/ptcg-live-to-json/scripts/convert.py convert \
  --input /path/to/source.txt \
  --work-dir data/conversions/run-001 \
  --name '卡组名称'
```

内置 **42 个英文系列/编号的身份索引**，仅保存简中印刷身份、英文记录 ID、来源 URL、数值指纹和必要补录的散列，不包含真实卡组、英文卡牌原始记录或规则框原文。索引不依赖本机验收目录，也不代表任意新卡均能自动转换。

成功输出 `deck.json`、`conversion.json` 和所需源记录，记录实际使用的提交、数据散列和卡图来源。退出码 2 表示存在 `pending.json`：此时不生成可导入卡组，也不能称为完成。首次使用需要规则框补录的卡时，按 pending 中的 `cardImage` 查看缓存原图，将核对后的文本合并到 `supplementsFile` 指定的本地文件，再用新的工作目录重跑；具体格式见[转换与核验细节](references/conversion.md)。不得改散列绕过核验，也不得将补录原文回填进仓库。

未知编号、名称与编号冲突、记录或卡图指纹变化、未核验进化来源等都应解决后再重跑。上游仅新增其他卡牌不会使未变更的既有索引失效。不要选“最新同名卡”代替具体效果版本。

默认核对 60 张；若用户明确指定其他张数，使用 `--expected-total` 并如实说明采用的规格，不能自动补牌、删牌。条目无需统一限制为 1–4；数据格式校验与赛事构筑合法性是不同结论。

## 验证和交付

```sh
node .agents/skills/ptcg-live-to-json/scripts/verify.ts \
  data/conversions/run-001/deck.json \
  --report data/conversions/run-001/verification.json
```

该命令调用当前前后端校验和隔离服务导入、导出、建局；不读取模型凭证或开展 AI 对战。非 60 张规格需同样传 `--expected-total`。已有报告不覆盖，选择新的报告文件。

核验通过后，将 JSON 保存到用户指定位置；没有指定时可以交付本次目录的 `deck.json`。给出文件链接、条目/张数、实际验证范围，保留源卡表、数据散列、映射及卡图补录证据。新快照与新映射只能按实际核验范围描述，不能扩大成全部卡文或完整规则认证。

## 用户要求导入时

只有用户要求保存到应用资料库时，才在验证命令上增加 `--import-url`。地址使用当前确认的服务，不把某端口写死：

```sh
node .agents/skills/ptcg-live-to-json/scripts/verify.ts /path/to/deck.json \
  --report /path/to/new-import-verification.json \
  --import-url http://127.0.0.1:3001
```

内容完全相同的已有记录复用；同名但内容不同的记录不自动覆盖。用户已有明确替换授权时按该授权处理，无需重复确认。创建请求结果不明时先重新查询资料库，不能盲目再次创建。最后检查导出 JSON 与交付文件一致，并在真实浏览器确认名称和张数。报告“已导入”必须有对应 API/页面证据；仅隔离测试通过不能算正式导入。

## 数据来源与致谢

感谢 **duanxr** 维护 [PTCG-CHS-Datasets](https://github.com/duanxr/PTCG-CHS-Datasets)，提供简中卡牌资料、字段字典和卡图索引。遵循其 README 中的用途与再分发限制；本项目的 MIT 代码许可不授予第三方卡图、卡文或数据的使用权。英文编号参考来自 [PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data)，原始字段在本地按需获取。
