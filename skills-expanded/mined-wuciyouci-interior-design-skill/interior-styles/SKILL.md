---
name: interior-styles
description: 室内设计风格库——28种风格"风格关键词+配色方案+灯光方案"三位一体触发表（v1.5.0 配色校准版：全部配色行按 60/30/10 分档 + 天地壁明度序 + 高饱和面积上限重写；v1.4.0 补「色系判据」三条硬判据 + 冷暖色区 + 朝向选冷暖 + 风格冷暖归属）+市场融合形态列+6个降级风格标注+5×5分空间词库+易混淆区分。触发：选风格、什么风格、XX风格怎么搭、风格关键词、风格对比、风格色板、配色、配什么颜色、冷暖色、色系、色温倾向、灯光、灯光方案、光指纹。由 interior-design 主 SKILL 按需调用。
metadata:
  version: "1.5.0"
---

# 室内设计风格库

> 本 SKILL 为 interior-design 主 SKILL 的子包。**核心职责：任何一个风格被触发时，必须同时给出该风格的「关键词 + 配色方案 + 灯光方案」三位一体配方**——禁止只给风格不给配色和灯光。

---

## 一、风格触发规则（强制）

**触发即三件套**：出现任意风格名 → 必须同时输出：
1. **英文关键词**（喂给 AI 生图）
2. **配色方案**（主色 60% + 辅色 30% + 点缀色 10%，用颜色词不用色号）
3. **灯光方案**（色温K + 主光方向 + 补光做法，光源可追溯）

**强制原则**：
- 风格 × 配色 × 灯光 **三者绑定**，禁止拆分输出
- 配色用相对比例（主色 60%/辅色 30%/点缀色 10%），不用 HEX
- 灯光必须"光源可追溯"（来源/方向/色温K），禁止泛泛"柔和灯光"

---

## 二、28 种风格三位一体配方表（v1.3.0 市场实况校准版）

> v1.3.0 变更：配方内容按 2026-08 五平台市场实况重写（欧模网/小红书官方月报/知末网/3d溜溜/建E网，详见 `[ref:市场实况]`）。新增"市场融合形态"列——**市场没有"纯风格"，触发风格名时默认带该风格最常见融合形态**（P0 用户指定优先）。⚠️ 标记的行为"市场判词"（热度低/转型/降级），触发时需同步提示。
>
> **灯光校准总则**：**无主灯（筒射灯+磁吸轨道+线性灯带）+ 2700-3000K 暖光为 2025-2026 家装市场跨风格默认灯光语言**（"见光不见灯"）；下方"明暗基调表"保留专业照明来源值，**冲突时以本配方表（市场版）为准**。

| # | 风格 | 英文关键词 | 配色（主60/辅30/点10·视觉占比参考） | 灯光（色温K/主光/补光） | 市场融合形态（2025-26） |
|---|---|---|---|---|---|
| 1 | 现代简约 | modern minimalist, no-main-light, premium gray, warm wood accent | 暖白/浅灰 60%（墙地顶，非纯黑白灰）+ 深灰与原木 30%（柜体家具）+ 深色系与金属 10%；默认暖调，采光差改冷灰 | 无主灯 2700-3000K：筒射灯+磁吸轨道+线性灯带，双眼皮吊顶（层高≥2.6m）｜吊顶灯：默认灯槽 | 现代奶油/现代轻奢（"现代"是万能基座，纯现代少见） |
| 2 | 北欧风 | Scandinavian, 文艺复古北欧, natural light | 6:3:1 —— 白/浅木/莫兰迪灰 60%（墙顶地）+ 雾霾蓝与奶咖 30%（柜体沙发）+ 焦糖棕与绿植 10%；莫兰迪依赖采光，采光差改大地色 | 自然光为主；人工光 2700-3000K 暖光分层；"光照不足也明亮柔和"｜吊顶灯：默认灯槽（可选·层高不足可退） | 北欧奶油/北欧波西米亚/极简原木中古北欧（纯北欧被批"滤镜疲劳"） |
| 3 | 新中式 | modern Chinese, 宋式美学, tea space, oriental zen | 米白/汝窑白/浅灰 60–70%（墙顶地）+ 黑胡桃木 25–30%（家具骨架/门套/格栅）+ 黛蓝/朱砂/铜 5–10%；**深色木作超 30% 显压抑** | 暖白自然光 3000K；长条形壁灯+纸灯；茶室重点光｜吊顶灯：不用灯槽（主灯/吊灯体系） | 新中式轻奢/宋式美学/新中式侘寂/新中式+欧式混搭（慎用红木=显老气） |
| 4 | 轻奢风 | modern luxury（万能后缀）, premium gray, marble + metal | 米白/高级灰/奶咖 60–70%（墙顶地）+ 深灰或驼色 20–30%（柜体家具）+ 香槟金 5–10%（仅灯具/拉手/线脚）；**金属硬上限 10%** | 3000K 暖光+线性灯带；无主灯重点照明｜吊顶灯：默认灯槽 | 法式轻奢/意式轻奢/奶油轻奢/港式轻奢/新中式轻奢（轻奢是后缀不是独立风格） |
| 5 | 美式风 | American classic, 简美/轻美式, cozy | 米白/燕麦 60% + 深棕 30%（家具）+ 酒红 15%/墨绿 10%/黄铜 5%（软装）；**墨绿与酒红合计不得超 15%，不许进 30% 位** | 2700-3000K；壁炉+无主灯；台灯+落地灯组合｜吊顶灯：不用灯槽（主灯/吊灯体系） | 美式复古/小美式/现代美式轻奢（"美式土味感"靠现代混搭7:3解决） |
| 6 | 欧式古典 | European classical, 新欧式/简欧（去繁）, palace style | 象牙白/米白 60–70%（墙顶）+ 胡桃木或深棕 20–30%（家具）+ 香槟金与皇家蓝 ≤10%（线脚/灯具/软装） | 2700K 水晶吊灯（简欧化：简约线条吊顶+水晶灯）｜吊顶灯：不用灯槽（主灯/吊灯体系） | 简欧/新欧式/法式轻奢古典——⚠️市场判词：被年轻人抛弃（"暴发户""洗浴中心"），替代=酒店风 |
| 7 | 日式风 | Japanese, 日式原木+榻榻米+茶室, natural harmony | 白/淡黄 60%（墙顶地留白）+ 原木 30%（家具，全屋木色统一不混）+ 黑/米/棕/绿 10% | 3000K 全屋暖光+纸灯/藤编吊灯；壁龛藏光｜吊顶灯：默认灯槽（可选·层高不足可退） | 日式原木/日式奶油/日式侘寂（障子/枯山水教科书元素基本退场） |
| 8 | 工业风 | industrial loft（商业主导）, raw materials | 深灰/水泥灰 60%（墙顶地）+ 红棕与浅灰 30%（家具）+ 金属黑 10%；铁锈红只做跳色不许进 30% 位，勿全屋黑白灰=秒变毛坯房 | 轨道射灯必须 3000K 暖光（否则像审讯室）；保留暗部｜吊顶灯：不用灯槽（主灯/吊灯体系） | 复古工业/工业波西米亚（70%冷感+30%暖调软装）——⚠️主战场=餐饮/酒吧工装 |
| 9 | 田园风 | country, 美式田园/英式田园, floral | 70%奶白+20%原木+10%莫兰迪（回暖版），辅浅绿/粉，点碎花 | 暖光 2700-3000K；复古玻璃吊灯+黄铜壁灯层叠｜吊顶灯：不用灯槽（主灯/吊灯体系） | 美式田园/奶油田园（纯碎花田园退出主流；勿全屋藤编=积灰） |
| 10 | 地中海 | Mediterranean, coastal（≠蓝白）, arch | 奶白与低饱和雾霾蓝 60%（墙顶地，**蓝 ≤30%**，忌大面积纯蓝=廉价）+ 陶土棕 30%（家具）+ 橄榄绿与藤编 10% | 暖光；藤编/陶瓷吊灯+壁灯｜吊顶灯：不用灯槽（主灯/吊灯体系） | ⚠️市场判词：被判过气（"只学到造型没学到生活"）；全屋拱形视觉疲劳 |
| 11 | 法式风 | French cream, PU molding, arched doorway, herringbone floor | 奶油白 60%（墙顶通刷，菱花白/奶杏）+ 焦糖棕 30%（柜体沙发）+ 哑光黑 10%（灯具五金）；**缺这一层深色就是"腻"的正因** | 3000K 无主灯重点照明+氛围灯；云朵灯/花朵吊灯｜吊顶灯：默认灯槽 | 法式奶油（市场90%爆款）/轻法式（小户型去雕花去罗马柱）/法式中古 |
| 12 | 混搭风 | eclectic（组合标签）, XX混搭XX | 主风格 70% + 辅风格 30% + 点缀 10%；撞色须**面积悬殊（主 70 : 对比 10）**，面积没拉开不许撞；"茶系"四折中：红茶（灰+木）/凉茶（黑白+红砖）/乌龙（手办+黄铜侘寂）/黑茶（巧克力棕木墙） | 无主灯+重点照明；主风格70%+辅风格30%｜吊顶灯：默认灯槽（可选·层高不足可退） | 中古混搭/新中式混搭/后现代混搭（混搭是方法不是风格） |
| 13 | 意式极简 | Italian minimalist（主流=意式轻奢）, 门墙柜一体化, sourceless light | 黑白灰 90%（墙顶地 + 软装基底）+ 大地色/炭黑/高级灰 辅 + 莫兰迪/古铜金/墨绿 ≤10%；**明度必须留中间层，不许纯白直跳深黑** | 无主灯+灯带是灵魂（格栅灯带/悬浮顶灯带/柜内灯带），3000K 暖光｜吊顶灯：默认灯槽 | 意式轻奢（平台主流词）/简奢（唐忠汉） |
| 14 | 侘寂风 | wabi-sabi（=微水泥代名词）, microcement, quiet | 大地灰/素米白/陶土 80%（墙顶地）+ 沙石色/浅赤褐/亚麻 辅 + 雾蓝/橄榄绿 ≤10%（点缀） | 2700K 低照度暖光；纸/麻透光极软｜吊顶灯：默认灯槽 | 侘寂奶油/中古侘寂/新中式侘寂（"新侘寂"=去破旧+现代精致） |
| 15 | 新古典 | neoclassical（≈简欧）, line-based simplicity | 象牙白/米黄 60–70%（墙顶）+ 胡桃木 20–30%（家具）+ 浅蓝绿石膏线、金线、暗红古铜 ≤10% | 2700-3000K 五层照明；壁炉+大型水晶灯+成对壁灯｜吊顶灯：不用灯槽（主灯/吊灯体系） | 简欧（市场实际标签，CAD 图纸直接标"简欧"）/欧式新古典 |
| 16 | 现代美式 | modern American（并入美式≈美式轻奢）, casual comfort | 米白/浅灰/原木奶油色 60%（墙顶地）+ 焦糖与墨绿 30%（家具，二者择一不并重）+ 黄铜 10%；浅色系显大 | 主灯+辅助+氛围三阶；北欧无主灯+美式黄铜壁灯混用｜吊顶灯：不用灯槽（主灯/吊灯体系） | 美式轻奢/北欧美式混搭（3:3:4 配色） |
| 17 | ArtDeco | Art Deco, geometric patterns ⚠️市场基本退出 | 主宝石色（祖母绿或宝蓝）60% + 中性（黑/白/奶油）30% + 金属 10%；**金属超 15% 变"珠宝盒"**；两强色须同调，不许对立撞 | 2700-3000K 几何装饰灯具+重点照明｜吊顶灯：不用灯槽（主灯/吊灯体系） | 无——⚠️降级：市场仅高层住宅立面/轻奢装饰画纹样残留，触发时提示 |
| 18 | 极简主义 | minimalism（已溶解进意式极简/侘寂）, warm minimal | 灰白 60%（墙顶地）+ 原木与奶咖/水泥灰 30%（家具）+ 单色 10% | 无主灯 3000K 全屋统一；见光不见灯｜吊顶灯：默认灯槽 | 意式极简/极简美式/原木极简（独立词条少） |
| 19 | 现代港式 | HK modern（=港式轻奢）, 老钱风 | 灰与咖 60%（硬装墙顶地）+ 燕麦米 30%（家具）+ 爱马仕橙与金属 10%（点缀） | 无主灯+金属/水晶吊灯；哑光墙面约70%｜吊顶灯：默认灯槽（可选·层高不足可退） | 港式轻奢（精装房交付默认）/港式老钱风/茶餐厅场景 |
| 20 | 奶油风 | cream style（万能底色）, 乳胶漆色号：可可蛋奶/珍珠白/菱花白/汝窑/杏子灰/布莱垦棕 | 带灰调奶咖/米白 60%（墙顶地）+ 比墙深半度的暖灰或燕麦 30%（家具柜体）+ 陶土/焦糖/深棕/哑光黑 10%（**深色压底，缺它必腻**） | 无主灯 2700-3000K 暖光；云朵灯+漫反射｜吊顶灯：默认灯槽 | 奶油原木（爆款）/法式奶油/中古奶油/侘寂奶油——必须深色/黑色压底防腻 |
| 21 | 复古风 | retro vintage（"复古"是形容词）, 美拉德配色 | 深浅棕 70%（墙顶地）+ 焦糖/卡其 25%（家具）+ 橘红/黄铜 5%（点缀）；墨绿酒红若加，并入这 5% | 2700-3000K 暖光；铁艺吊灯+爱迪生灯丝｜吊顶灯：不用灯槽（主灯/吊灯体系） | 法式复古/美式复古/复古工业（永远"XX复古"定语出现） |
| 22 | 现代农舍 | modern farmhouse ⚠️市场无家装概念 | 纯白 60%（墙顶地）+ 原木 30%（家具）+ 深蓝与编织 10% | 3000K 自然光+吊灯+壁灯｜吊顶灯：不用灯槽（主灯/吊灯体系） | 无——⚠️降级：市场对应=乡村自建房/老宅改造/民宿外观，触发时提示 |
| 23 | 波西米亚 | bohemian ⚠️降级为软装元素层（平台归"民族风"） | 米白 60%（基底）+ 低饱和雾霾蓝与焦糖棕 30%（家具织物）+ 陶土粉/莫兰迪绿/琥珀金 10%；**全屋色系 ≤3**，靠织物做触觉对比而不是堆色 | 2700K 藤编吊灯/纸灯+串灯｜吊顶灯：不用灯槽（主灯/吊灯体系） | 北欧波西米亚/工业波西米亚（卧室主题爆火；装饰品8-12件以内） |
| 24 | 赛博朋克 | cyberpunk ⚠️改定位：商业空间主题（非住宅风格） | 黑/深灰 60% + 霓虹紫蓝 30%（**仅作局部光源，不做大面积饰面**）+ 金属与屏幕光 10%；冷色 ≤3 种 | 4000-6000K 冷色线性灯带隐藏+磨砂扩散罩；"光线控制而非堆砌"｜吊顶灯：特殊·冷色线性灯带隐藏（非暖光洗顶槽） | 国潮赛博朋克/新中式赛博朋克（酒吧/夜市/剧本杀/奶茶店） |
| 25 | 沙漠风 | desert modern ⚠️市场=建筑外观/庭院/民宿 | 大地色/沙土 70%（墙顶地）+ 陶土橙 20%（家具）+ 灰绿/石材 10% | 3500K 天窗+大面积窗，陶土/石灰墙反射｜吊顶灯：特殊·天窗自然光为主，不做灯槽 | 无——⚠️降级：家装实装极少，触发时提示改用侘寂/原木替代 |
| 26 | 野兽派 | brutalist ⚠️市场基本无需求 | 水泥灰 70%（墙顶地）+ 原木 20%（家具）+ 金属与锈蚀 10%（点缀） | 2700K 暖光为主（肌理漆墙面）｜吊顶灯：默认灯槽（可选·层高不足可退） | 无——⚠️降级：市场仅商业店设计（成都太古里灰玫瑰粉案例），触发时提示 |
| 27 | 中古风 | mid-century modern（2025 最强新势力 TOP1）, 骨骼线柜门, 洞石, 胡桃木 | 奶油白/燕麦/奶咖灰 60–70%（墙顶通刷）+ 胡桃木 25–30%（柜体门框，**木色 ≤30% 且全屋统一不混橡木/红木**）+ 酒红地毯/黄铜 5–10%；地面浅橡木偏黄不偏红；**须有黑色元素压重心** | 3000-3500K；明装射灯/吊灯/氛围灯；**不要水晶灯**；黄铜落地灯｜吊顶灯：默认灯槽（可选·层高不足可退） | 法式中古（最强绑定）/中古奶油/黑色中古变体——精装房改造首选 |
| 28 | 原木风 | natural wood（=奶油原木）, warm minimal | 暖白/米杏 60%+（**留白 ≥60%，忌冷白纯白**）+ 原木 ≤30%（家具；木色:涂料约 3:1）+ 浅灰/石材/绿植 10% | 中性偏亮 1:1 冷暖比，3000-3500K；侧窗自然光｜吊顶灯：默认灯槽（可选·层高不足可退） | 奶油原木（固定组合词）/日式原木/原木极简 |

> ⚠️ **配色列已按 v1.4.0「色系判据」全量校准（v1.5.0）**：每行都写明 60/30/10 三档落在哪一层，高饱和一律压在 10% 点缀位，木色 ≤30%，并补齐天地壁明度序（天花 ≥ 墙 ≥ 地 ＞ 家具）。配色为常见搭配通用描述，非精确色号。AI 生图用颜色词即可。灯光为市场实况归纳（v1.3.0 已按无主灯+暖光市场主流校准）。**⚠️ 标注分两类，不可混为一谈：①降级标注（6 个：17 ArtDeco / 22 现代农舍 / 23 波西米亚 / 24 赛博朋克 / 25 沙漠风 / 26 野兽派）——条目保留可出，但触发时必须同步提示市场热度与替代建议，禁止当成主流风格默认输出；②市场判词（3 个：6 欧式古典 / 8 工业风 / 10 地中海）——仅记录市场现状（含"主战场=餐饮工装"这类特定定位），不等于降级，不需要替代建议。表内 ⚠️ 合计 9 处。**

---

## 二·五、市场通用加成层 [v1.3.0新增]

> 来源：五平台市场实况（详见 `[ref:市场实况]`）。这些是 2025-2026 家装市场**跨风格高频实操语言**，教科书配方缺失。出任何风格提示词时按需加入（与风格不冲突的词可叠加，冲突词按 P2 风格 DNA 裁决）：

| 层 | 市场通用词 | 使用说明 |
|---|---|---|
| 灯光 | **无主灯**（筒射灯+磁吸轨道+线性灯带）、见光不见灯、双眼皮吊顶（层高≥2.6m）、2700-3000K 暖光 | 除冷/功能风格（野兽派/赛博朋克）外默认适用；用户明确指定色温时用户优先 |
| 配色 | **高级灰**、乳胶漆色号（可可蛋奶/珍珠白/菱花白/汝窑/杏子灰/布莱垦棕）、**美拉德配色**（焦糖/卡其/深浅棕） | 高级灰=轻奢/意式/极简标志；乳胶漆色号=奶油系落地语言；美拉德=复古系热点 |
| 材质 | **微水泥**（侘寂代名词·翻车点：先做1㎡小样）、**PU线条+虎头石膏线**（法式）、**岩板**（轻奢/意式核心·光泽度≥4级厚度≥15mm）、**骨骼线柜门+洞石**（中古标志）、**长虹玻璃**、肤感哑光柜体、木纹砖平替木地板（600×1200通铺不做过门石）、鱼骨拼/人字拼 | 材质细节最终以 `[skill:interior-materials]` 配方表为准，此处为市场语境补充 |
| 结构 | 精装房改造（软装换风格）、去客厅化、LDK一体化、门墙柜一体化、岛台+餐厨一体 | 出方案时优先考虑"在既有硬装上软装换风格"的真实市场约束 |
| 场景 | 民宿/精装房改造/小户型（这些是市场高频出图场景） | 用户未指定场景时按空间类型默认带入 |

**融合规则（强制）**：触发任何风格名，默认带该风格配方表"市场融合形态"列中最常见 1-2 种形态（如"法式"→ 默认按法式奶油出）；用户明确要纯风格/指定融合 → P0 用户优先。

---

### 配色 60/30/10 使用规则 [v1.2.0修订]

**60/30/10 是"视觉占比目标 / 视觉层级参考 / Prompt 配色组织工具 / 风格配色的默认起点"——不是 CAD 面积计算、不是像素级比例、不是必须严格执行的硬约束。**

允许根据空间面积、采光、材质面积、家具数量调整。

示例（Modern Minimalist）不必强迫"黑/白/灰"占 60% 主色，可以按真实设计语言组织：
```
Dominant: warm white / off-white
Secondary: light natural oak + light gray
Accent: black steel + subtle metal
```

**Style DNA 章节（本文件下方）的 MUST_HAVE/PREFERRED/AVOID 是配色取舍的依据**：优先满足风格 DNA，再参考 60/30/10 组织层次。

---

### 色系判据（与风格无关，28 风格共用）[v1.4.0新增]

> 上方配方表给的是**28 个答案**；本节给的是**判据**——配方表里没有的风格、客户临时改的色、混搭出来的组合，全靠本节判断对不对。
> **强制**：任何配色输出前先过本节三判据，再看配方表。冲突裁决：P0 用户要求 > 本节判据 > 配方表默认值。

#### 三套分法（不要混用）

| 分法 | 类别 | 用途 |
|---|---|---|
| **按色温** | 冷色（蓝/蓝绿/蓝紫）· 暖色（红/橙/黄/棕）· 中性（黑白灰） | 定基调。**冷=后退色**，空间显大显冷静；**暖=前进色**，空间显小显暖 |
| **按命名逻辑** | **莫兰迪**（掺灰降饱和，冷暖都能做）· **大地色**（取自土/木/石，不要求低饱和）· **木质调**（材料色，非涂装色） | 定选色方式。莫兰迪**依赖采光**，采光差会读成脏灰；大地色对光宽容、最不易后悔 |
| **按视觉角色** | 主角色 60% / 配角色 30% / 背景色 / 点缀色 10% | 定面积 |

口语选色：**采光好→莫兰迪；采光一般→大地色；拿不准→暖中性。**

#### 三条硬判据

**判据 1 · 高饱和只能做点缀（≤10%）**

中高饱和色（墨绿/酒红/芥末黄/爱马仕橙/祖母绿/宝蓝/朱砂）一旦进入 **30% 辅色位**，画面立刻俗。
30% 辅色位只允许：低彩中性、同色系暗一档、木色。

**判据 2 · 天地壁明度序（上浅下深）**

```
天花（最亮） ≥ 墙面 ≥ 地面 ＞ 家具（最深）
```

行业口径为「墙浅、地中、家私深」；另有硬规矩：**天花必须浅于墙面，或与墙面同色，不得比墙深**。
至少拉开**两级明度**。三级同明度 = 空间平、闷、没有纵深。
要打破此序（如日式全木、奶油全屋米白）必须**同时补一条深色压底**（深色地毯 / 深木家具 / 黑色金属构件），否则整间会"腻"。
⚠️ 常见翻车：奶油风、法式风全屋米白，天花/墙面/地面全是高明度 → 这才是"腻"的物理成因，不是"不够高级"。

**判据 3 · 冷暖必须有一个主调**

- 允许：**主冷 + 暖压制**（灰+木，靠木色回温）、**主暖 + 冷收口**（暖木 + 灰蓝点缀）
- 禁止：冷暖各占一半、两个都够格叫主色 → 没有主调，读作"杂"
- 暖色是前进色：**小户型大面积暖高饱和 = 压抑**，不是温馨

#### 出词前五问

```
① 主角色 60%：___（冷暖 ___ / 明度 ___ / 彩度 ___）
② 配角色 30%：___（是否低彩？高饱和不许进这一层）
③ 点缀 10%：___（高饱和只放这里）
④ 天地壁明度序：地面___ / 墙面___ / 天花___（至少两级差，或已补深色压底）
⑤ 冷暖主调：___（另一温度在做什么？压制/点缀，说得出才算成立）
```

#### 冷暖色区（完整分级）

| 温度 | 颜色 | 依据 |
|---|---|---|
| **暖** | 红、橙、黄、棕、红棕、黄棕、大地色、偏黄木色 | 长波长；联想太阳、火焰、热血 |
| **冷** | 蓝、青、蓝紫、蓝绿、冷灰 | 短波长；联想冰雪、大海、晴空 |
| **中** | 绿、紫（归属有争议）、黑白灰（无彩色） | 不冷不暖，须搭配其他色才显温度 |

三条补充：
1. **相对性**——紫比红冷、比蓝暖；玫红比大红冷。冷暖只在对比中成立。
2. **明度纯度会改变冷暖**——加白提高明度→偏冷；加黑降低明度→偏暖；高纯度→偏暖。
3. **无彩色也分冷暖**——白偏冷、黑偏暖，灰看配比。

#### 按朝向 / 采光选冷暖

| 朝向 / 条件 | 建议色调 |
|---|---|
| 朝北（无直射、易阴冷） | **明调暖色**：奶黄、米黄、燕麦、浅木 |
| 朝南（日照长） | 中性或**冷色**：绿灰、浅蓝灰、湖绿；层高低时冷色更显开敞 |
| 朝东（早晒早暗） | 浅暖色（较稳妥） |
| 朝西（西晒强、热） | **冷调**：浅灰蓝、雾绿 |
| 采光不足 / 低楼层 | 高明度浅色调 |
| 采光充足 / 高层 | 可上冷暖深沉色 |
| 小户型 | 冷色或浅色做主色，暖色只做点缀（暖是前进色，会挤小） |

#### 28 风格冷暖归属（粗档，非硬标准）

| 倾向 | 风格 |
|---|---|
| **偏冷** | 现代简约、北欧、工业、极简、意式极简、轻奢（灰调） |
| **偏暖** | 新中式、日式、美式、复古、侘寂、中古、法式、奶油、田园、地中海（陶土） |
| **中性可调** | 现代港式、原木、现代美式、混搭 |
| **特殊** | ArtDeco（宝石色高饱和，冷暖并存）、赛博朋克（冷） |

> 此表只用于**判断某个色彩提案是否跑偏**（如给偏暖的侘寂塞大面积冷灰 = 明显跑偏），不是限制。用户指定冷暖时 P0 优先。

---

## 三、风格明暗基调（光比）[v1.1.3 全量补齐]

> 来源：专业验证（摄影课程/照明设计/设计师访谈，见文末来源）。**光比（key-to-fill）= 主光:补光比，决定画面明暗性格**：
> 低光比 2:1 = high-key 明亮 / 中光比 4:1 = 平衡 / 高光比 8:1 = low-key 暗调戏剧。
> **核心认知：暗 ≠ 少光**——暗调=多层柔和光+刻意暗部（光池），不是单光源压暗。

### 通用铁律（所有风格适用，专业共识）[v1.2.0去绝对化修订]

1. **灯光层次原则（Lighting Layer Principle）**：优先保证三个**功能层次**——ambient（环境）+ task（任务）+ accent（点缀）；**不要求必须由三种独立灯具实现**，允许一个系统承担多个层次（线性灯+洗墙 / 吊灯+环境反射 / 柜下灯+主照明 / 自然光+人工补光）。住宅效果图应避免只依赖单一光源造成平板照明，优先形成有层次的光环境（HomeFurnishings/Yulan）
2. **"Moody 不等于暗"**：暗色空间需要**更多光源**不是更少，多层柔和光（HomeFurnishings）
3. **光池（pools of light）**：刻意制造光影池而非均匀照亮 = 深度和戏剧感（Sherwin-Williams）
4. **色温服从风格**：色温由风格决定，不是所有风格统一暖光——见下方 **Lighting Temperature Rule**；5000K+ 不得默认作为住宅通用光源（Catch41/Erylin）
5. **哑光吸光 + 反射点缀**：暗调用哑光漆+金属反射防"洞穴感"（Engineerfix）
6. **暗部比例动态调整**：暗部比例是摄影/渲染表现参考，须根据风格、空间采光、光比、材质、用户需求动态调整——High-key 风格**不需要**强行保留 30-40% 暗部；Low-key/moody 风格可增加暗部；**暗部必须保留材质细节，不允许因追求 low-key 形成纯黑死区**（diyashley）
7. **材质-色温协调**：深暖木材在高色温冷白光下容易发灰、失去温度；浅色中性浅木材（light oak / white oak / ash）可与 3500-4000K 中性光配合。最终判断须综合木材颜色、光源色温、自然光、墙面反射、白平衡（Parrot Uncle）

### Lighting Temperature Rule（色温服从风格）[v1.2.0新增]

**色温不能单独决定氛围**——必须综合：材质色温、自然光、墙面反射、光源方向、光比、局部重点照明。

建议范围（**风格优先；用户明确指定色温时用户要求优先**）：
| 风格类型 | 色温范围 |
|---|---|
| 暖氛围风格（侘寂/欧式古典/复古/沙漠/美式等） | 2200–3000K |
| 暖中性风格（法式/中古/现代美式/农舍/波西米亚等） | 3000–3500K |
| 当代中性风格（现代简约/极简/港式/意式等） | 3500–4000K |
| 冷/功能风格（野兽派/赛博朋克等） | 4000K 及以上，仅在风格和功能合理时使用 |

示例：
- Modern Minimalist：允许 3500–4000K；**用户明确指定 4000K 时必须优先执行**
- Mid-Century Modern：优先 2700–3000K；用户指定其他色温则用户要求优先

> ⚠️ 与配方表的关系（避免读成两套互斥值）：配方表「灯光」列给的是**无主灯**色温（如现代简约 无主灯 2700–3000K），本表给的是**有主灯**色温范围（现代简约 3500–4000K）。两者是同一条规则的**两档**，按方案实际采用的布光方式择一即可；配方表为归属处（见 SKILL.md 事实归属表），冲突时以配方表为准。

### 已验证风格明暗基调表（专业来源）

> ⚠️ [v1.3.0] 本表保留专业照明来源值；**与上方配方表（市场版）色温冲突时，以配方表为准**——市场主流为无主灯+2700-3000K 暖光（如现代简约配方表已改为 2700-3000K）。

| 风格 | 明暗基调（光比） | 色温 | 灯具特征 | 来源 |
|---|---|---|---|---|
| 北欧 | 低光比 high-key，明亮通透 | 中性冷白 + 暖 2700K | 大窗+反光面，多层柔和光 | illustrarch/SOKO |
| 日式/侘寂 | 高光比 low-key，暗调沉静 | 暖深 2200-2700K | 纸灯/障子漫射，阴影即深度 | illustrarch |
| 轻奢/意式 | 中高光比，重点照明明暗对比 | 3000K + 金属反射 | 层叠光+眩光控制，"低调奢华" | Gusurelighting |
| 法式 | 低中光比，浪漫柔和 | 2700K | 水晶吊灯+烛形灯 | Liccoled |
| 新中式 | 中光比，平衡雅致 | 3000K | 木框灯笼/米纸灯 | Liccoled |
| 工业 | 高光比，硬光高对比 | 2200-3000K | 轨道灯+有意造阴影 | Engineerfix |
| 波西米亚 | 低光比，温暖包裹 | 暖色（无硬亮） | 藤编/编织/彩色玻璃，多层次 | Lightopia |
| 中古风 | 中低光比，复古温暖 | 2700K（Edison 灯丝） | Sputnik/球形吊灯，黄铜+黑钢 | Lightopia MCM |
| 美式传统 | 中低光比，温暖正式 | 2700K | 黄铜+Empire灯罩，成对台灯 | exoticdecor |
| 现代简约 | 中光比，中性明亮 | 4000K（可暖） | 线性灯带+无主灯，简洁几何 | exoticdecor |
| 原木/Japandi | 低光比，自然温和 | 2700-3000K | 天然木/麻布灯罩，手作质感 | exoticdecor |
| 欧式古典 | 高光比，暗调戏剧宫廷感 | 2700-3000K | 烛台式水晶吊灯+镀金壁灯，三级照明60/25/15，大镜面倍增 | L&L Luce&Light/Exenia |
| 新古典 | 中光比，柔和漫射弱阴影 | 2700-3000K | 中心水晶吊灯焦点+成对壁灯/台灯对称，金框大镜反射 | ionosfera/MyModernCave |
| 极简主义 | 中低光比，均匀克制 | 3000K 全屋统一 | 无主灯：筒射灯+线性灯带+磁吸轨道，见光不见灯，洗墙 | GRNLED/Vakkerlight |
| 现代港式 | 中高光比，克制奢华 | 3000K 暖光 | 无主灯+反光灯槽/悬浮顶，隐藏防眩射灯+暖色灯带 | VogueHK/Dezeen |
| 意式极简 | 中低光比，立体光影 | 3000K 全光谱 | 无主灯三层（基础50+氛围30+重点20），"无源光"品牌哲学 | Catellani&Smith/ALPHALUCE |
| 地中海 | 中光比，暖调通透 | 2700-3000K | 藤编/陶瓷吊灯+壁灯+烛光四层，镂空铁艺灯笼光影，壁龛藏光 | P-robinson/中照网 |
| 复古风 | 中光比，暗调氛围 | 2700K | Sputnik/蘑菇灯/钓鱼灯锚点+爱迪生灯丝，簇状吊灯，无主灯间接 | Nauradika/LightForm |
| 现代美式 | 中光比，温暖松弛 | 2700-3000K 分区 | 黄铜/铁艺主灯+无主灯，洗墙射灯36°，餐厅吊灯距桌面55-70cm | Coohom/中照网 |
| ArtDeco | 高光比，暗调戏剧 | 2700-3000K | 几何定制灯具+天花暗槽+压花玻璃背透，CRI95射灯三层 | 中照网/Dwell |
| 田园风 | 中光比，温润层叠 | 2700-3000K | 复古玻璃吊灯+黄铜壁灯+爱迪生灯丝，低位光源层叠 | Pooky/Homebuilding |
| 沙漠风 | 中低光比，暖氛围暗部为本 | 2200K 烛光感 | 地埋漫射+洗墙"沙浪"，低置地面光，沙丘造型灯 | LineaLight/CID |
| 野兽派 | 高光比，暗调戏剧 | 2700-3000K 暖白 | 混凝土铸造灯雕塑+裸露灯丝，轨道/洗墙勾轮廓 | NookCollections/TheLocalProject |
| 混搭风 | 中光比，层次照明 | 2700-3000K 统一 | 三层布光+高度错落，混搭年代材质+统一五金串联，焦点灯≤3款 | Lightopia/Karman |
| 现代农舍 | 中光比，温暖均匀 | 2700-3000K | 黑铁艺/做旧青铜+玻璃藤编罩，岛台成排吊灯，三层+调光 | Lightopia/Homebuilding |
| 赛博朋克 | 高光比，暗调 | 3000-4000K+霓虹彩 | 70%暗部+霓虹≤15%，RGB灯带藏式布光，分路调光 | smzdm/中照网/Dwell |

> ⚠️ 本表当前 **26 行**（组合行如「日式/侘寂」「轻奢/意式」各计 1 行）；**奶油风尚未补齐**，待补专业来源后方可恢复「28 风格全部补齐」表述（原 2026-08-09 分批搜索验证；2026-09-12 核实并改注）。

### 出提示词时的用法

```
光比 + 色温 + 灯光层次（ambient/task/accent）+ 光池/暗部 → 组合进灯光段：
奶油风（低光比）→ "低光比明亮温馨，多层柔和光源，局部暗角光池，留暗部层次"
侘寂风（高光比）→ "高光比暗调沉静，多层柔和光，刻意光影池，暗部保留细节"
```

---

## 三·五、Style DNA 系统 [v1.2.0新增 · v1.2.1统一]

> **每种风格的五个字段**：
> - **MUST_HAVE**：风格身份不可缺失的特征（没有则身份失真）——不得把"常见/高兼容"写成 MUST_HAVE
> - **PREFERRED**：常见/高兼容特征，推荐使用但不强制
> - **OPTIONAL**：可选增强，不作为风格判断依据
> - **AVOID**：过多出现导致风格漂移
> - **STYLE_BOUNDARY**：与相邻风格的边界
>
> **单一事实源规则**：Style DNA（风格身份核心）> Style Recipe（配方表推荐表达）> Material Recipe（材质候选库）。三者冲突时以 DNA 为准；但 DNA 中有 PREFERRED 材料 ≠ 该材料必须出现。
>
> **用途**：① 出提示词时按 DNA 选词 ② 跨规则一致性检查（主 SKILL Consistency Matrix）③ 风格漂移检测（目标风格 AVOID 特征出现 ≥3 个 → HIGH DRIFT）。
> DNA 与上方配方表（关键词/配色/灯光）及 `[skill:interior-materials]` 材质表保持一致，冲突时以 DNA 为准并修正配方表。

### 1. Modern Minimalist 现代简约
MUST_HAVE: clean architectural lines, restrained material palette, integrated storage, simple geometric furniture, visually quiet surfaces
PREFERRED: light oak, matte white, light gray, slim black metal, concealed lighting, linear lighting
OPTIONAL: glass, subtle stone, limited greenery, abstract artwork
AVOID: excessive rattan, caramel leather as dominant material, ornate brass decoration, heavy vintage furniture, strong retro patterns, dark walnut as dominant wood, warm 2700K mood lighting as dominant lighting language
STYLE_BOUNDARY: 克制+干净几何+集成收纳+当代材质表达；可有暖木，但视觉上不得变成 Mid-Century / Japandi / Rustic / Wabi-Sabi
COLOR_NOTE [v1.2.1]: **"black/white/gray" 不是现代简约唯一主配色**——现代简约可暖可冷。允许的配色组合：warm white + light oak + black / off-white + light gray + oak / white + stone + dark wood / gray + oak + black。不要自动把现代简约变成冷灰极简；用户指定颜色组合 > 风格默认配色。

### 2. Scandinavian 北欧风 [v1.2.1修正]
MUST_HAVE: natural daylight, light wood, natural textiles, functional simplicity, hygge/cozy atmosphere
PREFERRED: white, light oak, pale gray, gray-blue, plants, wool/linen, warm 2700-4000K layered artificial light with natural daylight
OPTIONAL: rattan, ceramics, candles, sheepskin
AVOID: heavy dark wood dominance, ornate molding, cold gray industrial palette, dense ornament
STYLE_BOUNDARY: 自然光+功能主义+浅木+自然织物+舒适氛围；灯光以自然日光为主，人工光按空间氛围在 2700-4000K 间选择，暖色人工光与自然光结合时优先保持舒适层次——**4000K 不是北欧固定身份**；别变奶油风（暖奶油色阶+圆润+低对比）或原木风（木色主导）

### 3. Modern Chinese 新中式 [v1.2.1修正]
MUST_HAVE: contemporary Chinese spatial language, restrained traditional references, natural/dark wood, cultural identity, controlled negative space
PREFERRED: walnut, ink gray, vermilion accents, lattice/screen elements, balanced composition, restrained symmetry, paper lanterns, empty white space
OPTIONAL: bonsai, tea set, silk cushions, calligraphy
AVOID: western classical columns, excessive gold, full European ornament, neon, industrial rawness
STYLE_BOUNDARY: 当代中式空间语言+克制传统符号（水墨/格栅/朱砂）+留白；**"严格左右对称"不是必要条件**——对称是 PREFERRED 的克制使用，不对称留白同样成立；别变日式（更简白）或欧式古典

### 4. Modern Luxury 轻奢风
MUST_HAVE: refined metallic accents (brass/gold), sophisticated neutral base, high-end material mix
PREFERRED: gray/cream base, champagne gold, deep blue, marble, velvet, wall-washing accent light
OPTIONAL: crystal accents, fluted glass, decorative mirrors
AVOID: palace-level gold overload, crystal chandelier dominance, ornate classical carving, Rococo excess
STYLE_BOUNDARY: 现代+克制金属点缀；别变欧式古典（金过量）或意式极简（无色金属感）

### 5. American Classic 美式风
MUST_HAVE: classic American proportions, cozy warmth, wood + upholstery mix
PREFERRED: dark wood, beige, deep red, dark green, brass, leather, table/floor lamp layers
OPTIONAL: plaid textiles, framed artwork, bar cart, wicker
AVOID: stark minimal sterility, excessive white, industrial steel, Scandinavian light palette
STYLE_BOUNDARY: 传统厚重+温暖正式；别变现代简约或田园（更朴素碎花）

### 6. European Classical 欧式古典
MUST_HAVE: palace-style opulence, crystal chandelier, gilded details, classical symmetry, layered light
PREFERRED: gold, cream, wine red, dark green, marble, velvet, sculpted molding
OPTIONAL: silk drapery, fresco, antique mirrors, candle wall lights
AVOID: minimalism, bare walls, modern flat lighting, industrial rawness, low-key moody restraint
STYLE_BOUNDARY: 金碧辉煌+繁复古典；别变轻奢（克制版）或新古典（简化版）

### 7. Japanese 日式风
MUST_HAVE: natural harmony, low furniture, wood + paper materials, tatami aesthetics
PREFERRED: light wood, white, gray, paper lamps, plants, sliding doors
OPTIONAL: calligraphy, ceramics, tea ceremony items
AVOID: heavy ornate furniture, bright saturated colors, western sofa dominance, luxury gold
STYLE_BOUNDARY: 自然简洁+低矮家具+障子纸光；别变原木风（更重木色）或侘寂（更粗拙残缺）

### 8. Industrial 工业风
MUST_HAVE: raw materials, exposed elements (concrete/brick/steel), utilitarian character
PREFERRED: cement gray, black, rust red, brown, Edison lights, metal frames, track lights
OPTIONAL: old leather, reclaimed wood, pipes, factory artifacts
AVOID: refined luxury, soft pastel palette, heavy drapery, delicate molding, cozy floral
STYLE_BOUNDARY: 粗犷原料+暴露构造；别变野兽派（纯混凝土体块）或混搭风

### 9. Country 田园风
MUST_HAVE: floral freshness, country warmth, natural charm
PREFERRED: light green, cream yellow, pink, white, floral patterns, soft window light
OPTIONAL: gingham, wicker baskets, porcelain, lace
AVOID: industrial, cold gray minimalism, glass/metal dominance, neon, urban density
STYLE_BOUNDARY: 碎花+田园暖调；别变法式（更精致）或波西米亚（更自由叠搭）

### 10. Mediterranean 地中海
MUST_HAVE: blue & white identity, ocean spirit, coastal light, arch forms
PREFERRED: cobalt blue, white, terracotta, rattan, stucco, forged iron
OPTIONAL: rope details, ceramics, driftwood, lanterns
AVOID: dark heavy palette, alpine/forest aesthetics, excessive gold, dense urban luxury
STYLE_BOUNDARY: 蓝白+陶土+拱形+白墙反射光；别变田园或波西米亚

### 11. French Elegant 法式风
MUST_HAVE: elegant curves, romantic charm, vintage softness, wall paneling
PREFERRED: cream, blush pink, champagne gold, gray-blue, crystal accents, moldings, canopy silhouettes
OPTIONAL: toile fabric, floral details, antique brass, perfume bottles
AVOID: industrial, brutalist, excessive minimalism, heavy dark wood dominance
STYLE_BOUNDARY: 柔美线条+护墙板+浪漫；别变欧式古典（更繁复宫廷）或轻奢（更硬朗现代）

### 12. Eclectic 混搭风
MUST_HAVE: intentional mix with hierarchy, personal expression, layered composition
PREFERRED: 主风格70% + 辅风格30% 呼应, metal ≤2 种 (brass + black iron)
OPTIONAL: any curated pieces, vintage finds, art
AVOID: 无序堆砌无主次, uncontrolled materials, >2 种金属色, theme-less randomness
STYLE_BOUNDARY: 有主次的混搭（70/30）；别变纯堆砌或波西米亚（更织物自由风）

### 13. Italian Minimalist 意式极简
MUST_HAVE: ultimate restraint, seamless surfaces, premium material quality, "sourceless light"
PREFERRED: premium gray, black, white, beige, metal accents, microcement, 3-layer lighting (50/30/20)
OPTIONAL: marble, glass, single statement piece
AVOID: clutter, ornate decor, busy patterns, excessive colors, visible light sources
STYLE_BOUNDARY: 高级灰+无缝一体+材质奢华感；别变现代简约（更轻量）或港式（更多玻璃金属）

### 14. Wabi-Sabi 侘寂风
MUST_HAVE: imperfection as beauty, natural aging, handmade texture, quiet humility
PREFERRED: beige, plaster gray, linen, light terracotta, dried branches, low warm light 2700K
OPTIONAL: pottery, raw stone, weathered wood, paper/metal diffusers
AVOID: glossy surfaces, bright saturated color, polished luxury, symmetrical formality, neon
STYLE_BOUNDARY: 拙朴+时间感+不对称；别变极简（干净精确）或工业（冷硬原料）

### 15. Neoclassical 新古典
MUST_HAVE: simplified classical, balanced symmetry, elegance without palace excess
PREFERRED: cream, champagne gold, walnut, gold line details, wall sconces, center chandelier
OPTIONAL: marble, silk, crystal, gold-frame mirrors
AVOID: full palace opulence, heavy carving, dark drama, industrial rawness
STYLE_BOUNDARY: 古典简化版+对称光；别变欧式古典（繁复）或现代简约（无古典线脚）

### 16. Modern American 现代美式
MUST_HAVE: casual comfort, modern proportions, relaxed warmth
PREFERRED: light wood, beige, gray-blue, pottery, ceiling fan, layered casual light
OPTIONAL: leather, linen, decorative accents
AVOID: heavy traditional carving, ornate gilding, industrial raw, stark minimal emptiness
STYLE_BOUNDARY: 现代比例+美式松弛感；别变传统美式（厚重）或北欧（更冷白）

### 17. ArtDeco
MUST_HAVE: geometric patterns, roaring 20s glamour, bold symmetry, decorative lighting fixtures
PREFERRED: black gold, emerald green, royal blue, wine red, geometric fixtures, metal reflection lines
OPTIONAL: marquetry, lacquer, sunburst mirrors, fan details
AVOID: soft pastel palette, rural/rustic, minimal white emptiness, industrial roughness
STYLE_BOUNDARY: 几何装饰感+暗调戏剧；别变轻奢（无几何符号）或欧式古典

### 18. Minimalism 极简主义 [v1.2.1修正]
MUST_HAVE: reduction to essential elements, strong negative space, restrained form, visual hierarchy, minimal decorative noise, disciplined material palette
PREFERRED: white/off-white, neutral tones, concealed lighting, integrated storage, simple sculptural elements
OPTIONAL: one artwork, one plant, one sculptural piece
AVOID: ≥3 色主导, decor accumulation, ornate furniture, busy textures, visible clutter
STYLE_BOUNDARY: 少到极致+留白+形态比例主导；**"纯白"不是必要条件**——允许 warm minimalism / dark minimalism / material-driven minimalism；别变现代简约（可多材质层次、可有装饰物）——多维区分见"易混淆区分规则"

### 19. Hong Kong Modern 现代港式
MUST_HAVE: premium gray, urban polish, glass & metal expression
PREFERRED: dark gray, black, silver, glass, wood veneer, linear lights, grille spotlights
OPTIONAL: leather, stone, mirrors
AVOID: rustic, floral, excessive warm retro, cottage elements, soft pastel coziness
STYLE_BOUNDARY: 深灰+玻璃金属+都市克制；别变意式极简（更无缝）或轻奢（加金色）

### 20. Cream Style 奶油风
MUST_HAVE: soft healing mood, cream tones, curved/rounded shapes, gentle light
PREFERRED: cream white, milk apricot, milk coffee, beige, cloud lamps, diffuse light
OPTIONAL: fluffy textures, arch details, rattan, dried flowers
AVOID: cold gray dominance, stark black/white contrast, sharp angular minimalism, industrial, glossy tiles
STYLE_BOUNDARY: 奶白奶杏+圆润+低光比；别变北欧（尖角硬线/冷白）或原木（木色主导）

### 21. Retro Vintage 复古风 [v1.2.1修正]
MUST_HAVE: nostalgic atmosphere, vintage character pieces, historical visual references, warm aged palette
PREFERRED: mustard yellow, dark green, dark brown, brass, Edison-style lighting, vintage lamps, mushroom/sputnik lights
OPTIONAL: globe lamps, geometric rugs, vintage posters, arc floor lamps
AVOID: sterile all-white, futuristic neon, palace gold, over-polished brand-new look
STYLE_BOUNDARY: 复古怀旧+年代特征物件+暖老化色阶；**Retro Vintage 是宽泛类别，mid-century 只是其中一种复古方向，不得等同**；别变中古风（经典设计款比例语言）或田园

### 22. Modern Farmhouse 现代农舍
MUST_HAVE: rustic chic, wood + white balance, farmhouse warmth with modern lines
PREFERRED: white, light wood, deep blue, woven textures, shiplap, pendant rows
OPTIONAL: checkered fabric, barn doors, mason jars, greenery
AVOID: urban industrial, luxury gold, ornate classical, cold minimal emptiness
STYLE_BOUNDARY: 现代结构+农舍元素；别变美式传统（厚重）或田园（碎花多）

### 23. Bohemian 波西米亚
MUST_HAVE: free-spirited, global eclectic, layered textiles, handcrafted feel
PREFERRED: red, orange, blue, purple, woven fabrics, macrame, tassels
OPTIONAL: vintage rugs, plants, hanging chairs, candles
AVOID: sterile minimal, corporate gray, rigid symmetry, single-tone palette, glass/metal dominance
STYLE_BOUNDARY: 自由叠搭+织物漫射光；别变田园（朴素）或混搭（无主题方向）

### 24. Cyberpunk 赛博朋克
MUST_HAVE: neon noir, futuristic atmosphere, high contrast dark base
PREFERRED: neon pink, neon blue, black, screen glow, RGB accent strips, ~70% shadow
OPTIONAL: holographic, chrome, digital patterns, smart devices
AVOID: cozy cottage, warm pastoral, all-natural materials, antique elegance, soft daylight warmth
STYLE_BOUNDARY: 霓虹+未来+高对比暗调；别变工业风（无霓虹）或现代港式（无色彩光）

### 25. Desert Modern 沙漠风
MUST_HAVE: earthy tones, sunbaked materials, desert modern calm
PREFERRED: sand, terracotta orange, gray-green, stone, limewash, low ground light
OPTIONAL: cacti, leather, wool, clay vessels
AVOID: cool coastal palette, dense green, glossy luxury, dark urban steel
STYLE_BOUNDARY: 沙土陶土+暖氛围暗部为本；别变侘寂（更粗拙）或地中海（蓝白）

### 26. Brutalist 野兽派
MUST_HAVE: raw concrete, monolithic form, brutalist mass, exposed structure
PREFERRED: cement gray, black, rust accents, concrete cast lights, exposed filaments
OPTIONAL: wood warmth, steel, sculptural concrete furniture
AVOID: cozy softness, floral, ornate detail, warm cream palette dominance, delicate molding
STYLE_BOUNDARY: 混凝土体块+粗犷；别变工业风（混合材质更杂）或现代简约（细腻）

### 27. Mid-Century Modern 中古风
MUST_HAVE: furniture with recognizable mid-century proportions, natural wood, tapered or sculptural legs, restrained retro geometry
PREFERRED: walnut or teak, leather, rattan/cane, brass, mustard yellow, deep green, warm layered lighting
OPTIONAL: vintage posters, geometric rugs, globe or glass pendant lights
AVOID: excessive ornate classical decoration, palace-style symmetry, excessive luxury gold, futuristic neon, overly sterile all-white minimalism
STYLE_BOUNDARY: 身份来自家具语言+材质组合+比例+克制复古现代感——不是简单"深色木"；别变 Classic / Japandi / Rustic

### 28. Natural Wood 原木风
MUST_HAVE: natural wood as dominant material, warm minimal, wood harmony (全屋木色统一≤2种)
PREFERRED: light oak, white oak, beige, light gray, plants, linen, small tapered legs + large panels
OPTIONAL: rattan, ceramics, paper lamps
AVOID: 木色>2种混用, heavy dark dominance, cold gray palette, plastic textures, glass-heavy
STYLE_BOUNDARY: 木色统一+暖+自然；别变日式（更极简白）或北欧（白多于木）

---

| 风格 | 客厅 | 卧室 | 厨房 | 卫生间 | 书房 |
|------|------|------|------|--------|------|
| 现代简约 | 悬浮电视柜·无主灯·通顶平板柜 | 低饱和床品·隐藏灯带·床头背景极简 | 平板柜门·岩板台面·隐形拉手 | 壁挂浴室柜·无边框镜·墙排 | 悬浮书桌·开放格+封闭柜 |
| 轻奢 | 岩板背景墙·金属线条·皮质沙发 | 软包床头·黄铜壁灯·丝绒窗帘 | 深色柜门·金色拉手·大理石纹台面 | 金属框镜·大理石台面·暗装花洒 | 皮革书桌椅·玻璃书柜·装饰画 |
| 北欧 | 布艺沙发·浅木地板·绿植角 | 棉麻床品·木质床头·纸质吊灯 | 白色柜门·木台面·小白砖 | 小白砖·黑色五金·木色浴室柜 | 浅木书桌·开放书架·舒适阅读角 |
| 新中式 | 实木沙发·水墨挂画·博古架 | 架子床·窗棂元素·丝绸床品 | 深木色柜门·仿古铜拉手 | 青花瓷洗手盆·木质镜框 | 明式书桌·文房四宝·茶席 |
| 侘寂 | 微水泥地面·亚麻沙发·枯枝花器 | 低矮床架·棉麻床品·陶罐台灯 | 手工釉面砖·拙朴陶器 | 水泥洗手盆·原木置物架 | 粗陶花瓶·旧木书桌·自然光 |

---

## 四、易混淆风格区分规则 [v1.2.0多维判断]

> **原则：风格判断 = 多维特征，不使用单一阈值判断。** 以下旧规则保留为辅助判断（heuristic），不是专业定义。

- **现代简约 vs 极简主义**：**多维判断（v1.2.0）**——Modern Minimalist：当代、功能、干净几何、集成收纳、克制装饰，**可含多种材质/色彩层次**，可有木/织物/艺术品/植物；Minimalism：减到本质元素、材质更少、物件更少、负空间更强、视觉噪音更低，形态与比例成为主导表达。旧规则"≥3种颜色+有无装饰物"降级为辅助判断
- **轻奢风 vs 意式极简**：辅助判断=是否有金色点缀+主色调是否偏灰；多维看金属是否刻意点缀（轻奢）vs 无缝一体（意式）
- **新中式 vs 日式风**：辅助判断=是否对称+是否有中式文化符号；多维看文化符号密度与对称性
- **北欧风 vs 奶油风** [v1.2.1]：**Scandinavian = 自然光 + 功能主义 + 浅木 + 自然织物 + 舒适氛围**；**Cream Style = 暖奶油色阶 + 圆润形体 + 低对比度 + 柔软材质**。"尖角硬线条"不是北欧核心定义，不作为主要区分依据
- **中古风 vs 复古风**：中古=经典设计款家具语言（比例/锥形腿）+材质组合；复古=更随性的怀旧混搭+爱迪生光（见 Style DNA 27/21）

---

## 五、风格来源说明

数据整合自：酷家乐平台官网公开的风格分类和搜索关键词 / AI生图工具实战测试（Midjourney/DALL-E/SD/Flux）/ 室内设计行业教材和专业社区公开资源 / GB 50096-2011《住宅设计规范》（部分已被 GB 55031-2022 替代）/ GB/T 50034《建筑照明设计标准》

