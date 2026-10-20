---
name: jeecg-dev
description: "JeecgBoot 开发规范（仅手动触发）。⚠️ 本技能只在用户显式输入 /jeecg-dev 或 $jeecg-dev 命令时使用，禁止自动触发——编写/修改 JeecgBoot 代码、应用 GitHub PR/issue 改动、修复 bug、新增功能、重构、代码生成等场景都不要自动调用本技能。内容涵盖 update-begin/end 痕迹注释、命名规范、实体/控制器/服务模式、API 约定、建表规则、MyBatis 多数据库兼容与修改日志实践。MANUAL ONLY: invoke ONLY when the user explicitly runs the /jeecg-dev command. Do NOT auto-trigger on any code editing, bug fix, PR/issue application, refactoring, or code generation."
---

# JeecgBoot 开发规范

在 JeecgBoot 项目中编写或修改代码时，必须遵循以下规范。本 skill 是强制性的——任何代码变更都必须符合这些标准。
简单收尾直接复用当前线程结果，不重复扫描和构建。

---

# 一、必做事项（每次代码修改必须完成，缺一不可）

## 1. 代码修改痕迹注释（内联注释）

**针对原有核心逻辑代码的修改，请统一增加头尾日志，并使用 update-begin / update-end 注释进行代码块标识，方便后续代码追踪、维护和差异定位。**

```java
//update-begin---author:作者名 ---date:YYYYMMDD  for：【bug号/需求号】修改说明-----------
// 已有方法体中被修改的核心逻辑
//update-end---author:作者名 ---date:YYYYMMDD  for：【bug号/需求号】修改说明-----------
```
**业务核心逻辑（必须标记）**
   核心业务流程处理
   状态流转逻辑
   业务规则计算
   权限校验
   审批流程
   数据转换和业务组装逻辑

**规则：**
- `author` 填实际修改人，`date` 格式 `YYYYMMDD`（无横线），`for` 填 bug号/需求号 + 简要说明
- **只在修改已有方法体内的核心逻辑时包裹**：`update-begin` / `update-end` 只包裹被修改的代码段
- 只针对核心逻辑加，简单修改不要加
- 用户未提供 bug 号时，必须主动询问；如果用户明确回复“无号”或“无编号”，视为已确认没有 bug/需求号，不再询问
- **无编号时，`for` 直接填写修改说明，禁止生成 `【无号】`、`【无编号】` 或空的 `【】`**。例如：`for：图片模型测试连接使用快速参数`

### 前端轻量化规则（优先级高于通用判断）

Vue、React、JavaScript、TypeScript 等前端代码默认不加 `update-begin/end`。前端变化通常可直接通过 SVN diff 识别，避免为局部交互和状态更新增加大量头尾注释。

前端只有以下关键逻辑修改需要标记：

- 权限、鉴权、数据脱敏、安全校验
- 审批、支付、订单等不可逆或跨步骤的核心业务状态流转
- 直接决定提交数据或业务结果的复杂规则计算、数据转换
- 影响多个模块的公共核心逻辑，且修改原因无法从代码和 diff 直接判断

以下常见前端改动一律不加：

- 模板、样式、文案、字段展示、显隐和布局调整
- `loading`、弹窗、页签、选中项、列表刷新、事件 `emit` 等页面状态或交互更新
- 简单的请求参数组装、响应字段兼容、过滤、排序、计数、格式化和默认值处理
- 普通增删改按钮事件、成功回调、错误提示、表单校验和局部 bug 修复
- 仅因方法体中出现 `if`、循环、`async/await` 或多行代码；这些语法本身不构成核心逻辑

例如，保存成功后补充 `emit('success')` 刷新列表，或通过 `filter` 统计启用项数量，均不需要 `update-begin/end`。

**⚠️ 不需要加痕迹注释的改动（以下一律不加）：**

以下改动 **不要** 加 `update-begin/end` 注释，否则徒增 diff 噪音、破坏代码整洁：

- **新增的类**（VO、Entity、DTO、枚举等整个新文件）：类 Javadoc 必须包含 `@author 创建人`、`@since YYYY-MM-DD 原因`，有 TB号/BUG号/issue号时一并写入；无需 update-begin/end 包裹
- **新增的方法**（Mapper 接口新增方法声明、Service/Controller 新增方法）：方法 Javadoc 必须包含 `@author 创建人`、`@since YYYY-MM-DD 原因`，有 TB号/BUG号/issue号时一并写入；无需 update-begin/end 包裹
- **新增的 XML SQL 块**（MyBatis Mapper XML 新增 `<select>/<insert>/<update>/<delete>`）：在 `<!-- -->` 注释里写明用途、author 和 since 日期即可，无需 update-begin/end
- `import` 语句的新增 / 删除 / 排序
- 包声明 `package` 调整
- 纯格式化、空行、缩进调整
- 注释的错别字修正
- 未使用 import / 变量的清理
- IDE 自动生成的 `@Override`、`serialVersionUID` 等
- **单行注解的新增 / 修改**：例如给已有方法补 `@RequiresPermissions("xxx")`、`@Transactional`、`@Deprecated`、Swagger/Knife4j `@Operation`、`@Schema(description=...)`、`@TableField(...)`、`@JsonProperty(access=...)`、Lombok 类级注解（`@Slf4j`/`@Data` 等）
- 字段访问修饰符微调（如 `private` → `protected`）、`final` 添加等单行属性变更
- 删除单个 `@Excel`/`@Schema` 之类不影响调用方的注解
- **YAML / properties 配置文件（`.yml`/`.yaml`/`.properties`）的任何改动**：需要说明修改原因时，直接用普通 `#` 注释写在被改的配置项旁边即可

判断标准：**"这行改动是在修改已有方法体的核心逻辑吗？"**
- 后端修改已有方法体内的 if/loop/异常处理、多行核心业务逻辑 → **加** `update-begin/end`
- 前端修改 → **先按“前端轻量化规则”判断**，不得仅凭 if/loop/异步结构或代码行数添加
- 新增类、新增方法、新增 XML SQL、单行声明性变更 → **不加**，用注释或 Javadoc 说明即可

举例：
- 新增 `SysUserDepartIdVo` VO 类 → **不加**，新文件 diff 一眼可见
- 新增 Mapper 接口方法 `queryDepartIdVosByUserIds` → **不加**，在 Javadoc 注明时间和原因即可
- 在 `queryPageList` 方法体里把循环内 N 次查询改为批量预加载 → **加** `update-begin/end`，后人需要知道这段重构的来由
- 给 `/queryById` 方法补一行 `@RequiresPermissions(...)` → **不加**

**Java 示例（用 `//` 行注释，允许 `---` 分隔）：**
```java
//update-begin---author:chenrui ---date:20250606  for：[issues/8337]关于ai工作列表的数据权限问题 #8337------------
if (MybatisPlusSaasConfig.OPEN_SYSTEM_TENANT_CONTROL) {
    AiragApp app = airagAppService.getById(id);
    String currentTenantId = TokenUtils.getTenantIdByRequest(request);
    if (null == app || !app.getTenantId().equals(currentTenantId)) {
        return Result.error("删除AI应用失败，不能删除其他租户的AI应用！");
    }
}
//update-end---author:chenrui ---date:20250606  for：[issues/8337]关于ai工作列表的数据权限问题 #8337------------
```

### XML / MyBatis Mapper XML 特殊规则（重要）

**XML 注释内严禁出现 `--`（XML 规范禁止 double-hyphen 出现在 `<!-- -->` 内）**，因此在 `.xml` 文件（如 Mapper XML、`pom.xml`、Flyway xml 等）中写痕迹注释时：

- ❌ 错误：`<!-- update-begin---author:scott ---date:20260421  for：【xxx】说明----------- -->`（含 `--`，解析器可能报错或告警）
- ✅ 正确：`<!-- update-begin author:scott date:20260421 for：【xxx】说明 -->`（用空格或单 `-` 分隔，避免任何连续两个及以上的 `-`）

**XML 痕迹注释模板：**
```xml
<!-- update-begin author:作者名 date:YYYYMMDD for：【bug号/需求号】修改说明 -->
<if test="processApplyUserId != null and processApplyUserId !=''">
    AND ahp.START_USER_ID_ = #{processApplyUserId}
</if>
<!-- update-end author:作者名 date:YYYYMMDD for：【bug号/需求号】修改说明 -->
```

其他同样要求避免 `--` 的注释场景：HTML（`.html`/`.vue` template）、SVG、XSL 等所有基于 XML 的文件类型。

## 2. 代码修改日志（历史记录文件）

在对应模块的日志文件**末尾**追加记录，格式：

> ⚠️ **强制要求：只允许在文件最末尾追加，禁止插入到文件开头或中间任何位置。**

```
-- author:作者名---date:YYYYMMDD--for: 【bug号/PR号】修改说明 ---
涉及的文件路径（每行一个，新增文件末尾加 (+) 标记）
-- author:作者名---date:YYYYMMDD--for: 【bug号/PR号】修改说明 ---
```

用户明确回复“无号”或“无编号”时，省略编号及其书名号：

```
-- author:作者名---date:YYYYMMDD--for: 修改说明 ---
涉及的文件路径（每行一个，新增文件末尾加 (+) 标记）
-- author:作者名---date:YYYYMMDD--for: 修改说明 ---
```

**文件标记规则**：
- 新增的文件在路径末尾加 ` (+)`
- 删除的文件在路径末尾加 ` (-)`
- 重命名的文件写成 `原文件名 --> 新文件名完整路径`
- 修改的文件不加标记
- **注意：`代码修改日志` 文件本身（如 `doc/代码修改日志.log`）不应出现在“涉及的文件路径”列表中，避免自我引用。**

各模块日志文件位置：
- `jeecg-boot-base-core/doc/修改日志.log`
- `jeecg-module-system/jeecg-system-biz/docs/代码修改日志`
- `jeecg-boot-module/jeecg-module-demo/doc/代码修改日志.log`
- 其他模块在各自 `doc/` 或 `docs/` 目录下查找

## 3. SVN 提交日志

代码和日志文件都修改完成后，提醒用户进行 SVN 提交（**修改日志文件必须和源代码一起提交，不得遗漏**）。**提交日志格式必须与 `代码修改日志` 文件条目保持一致**：

```
--author:作者名--date:YYYYMMDD--for:【bug号/PR号】简要说明
```

用户明确回复“无号”或“无编号”时，使用以下格式，禁止写成 `【无号】`：

```
--author:作者名--date:YYYYMMDD--for:简要说明
```

**示例：**
```
--author:scott--date:20251030--for:【issues/9450】online导入数据库表时，如果字段有两个下划线则会报错
--author:scott--date:20260424--for:【JHHB-1336】我发起的流程-当前办理人支持多人展示
```

**格式要点：**
- 开头必须是 `--author:` 三段式：`--author:xxx--date:xxx--for:xxx`（短横线 `--` 作分隔）
- `date` 为 `YYYYMMDD`（无横线）
- `for` 字段内 bug 号用中文书名号 `【】` 包裹，常见形式：`【issues/XXXX】`（GitHub 开源）、`【JHHB-XXXX】`（内部 Jira）、`【VUEN-XXXX】`（VUE 专项）、`【QQYUN-XXXX】` 等
- bug 号后直接接简要说明，不加空格也可接空格（两种历史风格都存在，推荐无空格紧贴 `】`）
- 无 bug/需求号时不添加中文书名号，`for:` 后直接接简要说明

### ⚠️ Windows 中文 commit 消息防乱码（强制遵守）

**禁止用 `svn commit -m "<中文>"` + `--encoding utf-8` 的写法**。在 Windows (Git Bash/MSYS) 下，shell 会把参数按 GBK (CP936) 传给 svn.exe，而 `--encoding utf-8` 又告诉 SVN "这是 UTF-8"，结果服务端存的是乱码（形如 `�ҷ�...`）。

**✅ 正确做法：commit message 先写入 UTF-8 文件，再用 `-F` 提交**

```bash
# 1. 写入 UTF-8 文件（用 Write 工具，或 printf + iconv）
cat > /tmp/svn_msg.txt <<'EOF'
JHHB-XXXX 简要说明
EOF

# 2. 用 -F 提交，--encoding 指定文件的编码
svn commit -F /tmp/svn_msg.txt --encoding utf-8 "<file1>" "<file2>" 2>&1 | iconv -f GBK -t UTF-8

# 3. 提交完成后删除临时文件
rm /tmp/svn_msg.txt
```

**提交后必须验证**：用 `svn log -l 1 --xml <path> | iconv -f GBK -t UTF-8` 或直接看命令行输出，**肉眼确认** commit message 中的中文没有变成 `�?` 之类的乱码；一旦发现乱码立即用 `svn propset --revprop -r <rev> svn:log "<新msg>"` 修复（需服务端开启 `pre-revprop-change` hook）。

**变通方案（如果服务端不允许改 revprop）**：改用纯 ASCII commit message，中文说明写在 `代码修改日志` 里，例如 `svn commit -m "JHHB-1336 fix multi-assignee display"`。

---

# 二、建表规范

| 规则 | 说明 |
|------|------|
| 主键 | 必须是 `id`，字符串 varchar(32)，唯一索引 |
| 标准字段 | 必须有 `create_by`、`create_time`、`update_by`、`update_time` |
| 字段注释 | 每个字段必须有注释，状态字段注明取值规则如 `'性别 0/男,1/女'` |
| 命名 | 英文单词，多词用下划线连接如 `school_id`，禁止拼音 |
| 类型字段 | 优先用 `varchar(1)` / `varchar(2)`，少用 `int` |
| 索引 | 高频查询字段加索引 |
| 逻辑删除 | 设计 `del_flag` 字段 |

---

# 三、代码质量规范

1. 只做最少的改动，不要破坏SVN对比
2. 禁止提交与功能无关的变更（格式化、空格、缩进调整等）
3. 修改代码同步写好 `代码修改日志（历史记录文件）`
4. 功能变化同步更新文档
5. 方法超过 50 行拆分，抽取共通

---

# 四、MyBatis 多数据库兼容规范（必须遵守）

JeecgBoot 同时支持 MySQL、Oracle、PostgreSQL、SQL Server、达梦（DM8）等多种数据库，**任何 MyBatis 查询写法都必须在所有数据库上行为一致**。

## ❌ 严禁：普通 SQL 以分号结尾

MyBatis Mapper XML 以及 `@Select`、`@Insert`、`@Update`、`@Delete` 等注解中的普通 `SELECT`、`INSERT`、`UPDATE`、`DELETE` SQL，末尾严禁添加分号 `;`。

部分数据库或 JDBC 驱动会容忍末尾分号，但 Oracle JDBC 会将分号作为 SQL 内容交给数据库解析，可能触发 `ORA-00911: 无效字符`。禁止依赖某个数据库或驱动的宽松处理行为。

```xml
<!-- ❌ 错误：Oracle JDBC 可能报 ORA-00911 -->
<select id="queryUser" resultType="org.jeecg.modules.system.entity.SysUser">
    SELECT * FROM sys_user WHERE id = #{id};
</select>

<!-- ✅ 正确：普通 SQL 不写结尾分号 -->
<select id="queryUser" resultType="org.jeecg.modules.system.entity.SysUser">
    SELECT * FROM sys_user WHERE id = #{id}
</select>
```

**检查要求：**
- 新增或修改 Mapper SQL 时，必须检查语句最后一个有效字符不是 `;`。
- 可使用 `rg -n ';\s*$' <模块路径> -g '*Mapper.xml'` 辅助检索，但必须人工排除 XML 实体（如 `&gt;`）、注释等非 SQL 内容。
- 不得通过数据库连接参数、Druid/MyBatis 全局拦截器统一删除分号；全局处理可能破坏 PL/SQL/DMSQL 语句块。
- Oracle PL/SQL、达梦 DMSQL 等语法本身要求分号的语句块属于例外，必须按数据库方言隔离（如 `databaseId` 或独立 Mapper），禁止放入通用 SQL 后依赖所有数据库执行。

## ❌ 严禁：`CONCAT` 传入三个及以上参数

Oracle 的 `CONCAT` 函数严格只接受两个参数。MySQL 等数据库允许的多参数写法放入通用 Mapper SQL 后，在 Oracle 下会触发 `ORA-00909: 参数个数无效`。

```xml
<!-- ❌ 错误：Oracle 下报 ORA-00909 -->
AND r.name LIKE CONCAT('%', #{keyword}, '%')

<!-- ✅ 正确：嵌套调用，每个 CONCAT 都只有两个参数 -->
AND r.name LIKE CONCAT(CONCAT('%', #{keyword}), '%')
```

统一使用嵌套双参数 `CONCAT`，不要改成仅适用于部分数据库的字符串连接语法。前缀或后缀匹配本身只有两个参数时，可直接调用：

```xml
AND org_code LIKE CONCAT(#{orgCode}, '%')
```

**检查要求：**
- 新增或修改 Mapper XML、Mapper 注解 SQL、MiniDao SQL 模板时，检查每个 `CONCAT` 的顶层参数数量，确保不超过两个。
- 修复一处多参数 `CONCAT` 后，必须扫描当前模块；涉及公共功能或数据库兼容专项修复时，扫描整个项目源码，并排除 `target`、`.svn`、`node_modules`、`dist` 等生成目录。
- 可先使用 `rg -n -i 'concat\s*\(' <检查路径>` 找出候选项，再按括号层级人工确认顶层参数数量；合法的嵌套 `CONCAT(CONCAT(...), ...)` 不得误报。
- 注释示例、应用层自定义可变参数函数、明确隔离的单数据库方言 SQL 不属于通用 Mapper SQL，必须结合上下文判断，禁止机械替换。

## ❌ 严禁：`resultType="map"` + 字符串 key 直接访问

各数据库对 `resultType="map"` 的列名/别名 key 大小写处理不同：

| 数据库 | `AS procInstId` 返回的 key |
|--------|--------------------------|
| MySQL | `procInstId`（保持别名原样） |
| Oracle | `PROCINSTID`（全部大写，丢失驼峰） |
| PostgreSQL | `procinstid`（全部小写） |

因此以下写法**在 Oracle/PostgreSQL 下 `m.get(...)` 返回 `null`，必须禁止**：

```java
// ❌ 禁止：Oracle 下 key 是 "PROCINSTID"，取不到值
List<Map<String, Object>> rows = mapper.queryXxx();
rows.stream().collect(Collectors.toMap(
    m -> String.valueOf(m.get("procInstId")),  // Oracle 下为 null
    m -> String.valueOf(m.get("text"))         // Oracle 下为 null
));
```

## ✅ 正确做法：使用 DTO 类接收结果

用专门的 DTO 类替代 `Map`，MyBatis 映射到 Java 类时采用**大小写不敏感**的属性匹配，`PROCINSTID`（Oracle）/ `procinstid`（PostgreSQL）/ `procInstId`（MySQL）均能正确映射到 `procInstId` 字段：

```java
// DTO 类（简单 POJO，无需注解）
public class BizTitleSimpleDTO {
    private String procInstId;
    private String text;
    // getter / setter ...
}
```

```xml
<!-- Mapper XML：resultType 指向 DTO，所有数据库均兼容 -->
<select id="getBatchHisVarinst" resultType="org.jeecg.modules.bpm.dto.BizTitleSimpleDTO">
    SELECT EXECUTION_ID_ AS procInstId, TEXT_ AS text
    FROM act_hi_varinst
    WHERE NAME_ = #{name}
    AND EXECUTION_ID_ IN
    <foreach collection="ids" item="id" open="(" separator="," close=")">
        #{id}
    </foreach>
</select>
```

```java
// Service 中通过 getter 访问，类型安全且跨数据库
List<BizTitleSimpleDTO> rows = mapper.getBatchHisVarinst(name, ids);
Map<String, String> result = rows.stream().collect(Collectors.toMap(
    BizTitleSimpleDTO::getProcInstId,
    r -> oConvertUtils.getString(r.getText()),
    (a, b) -> a
));
```

## 适用 `resultType="map"` 的例外场景

以下情况可以使用 `Map`，但**必须通过固定大写 key** 访问（Oracle 风格，所有库均返回大写时一致）：
- 只在单一数据库环境下运行的内部工具脚本（明确标注数据库类型）
- MyBatis `@Select` 注解查询且只需判断是否为空（不关心 key 名称）

其他所有情况一律使用 DTO。
