# 公司 demo

## 1. 初始化环境

```bash
bash scripts/setup_conda.sh
conda activate colleague-company
conda run -n colleague-company pip install -e '.[dev]'
```

## 2. 配置 API

```bash
company-platform configure-api --provider claude --api-key "your-key"
```

也支持：

```bash
company-platform configure-api --provider openai --api-key "your-key"
company-platform configure-api --provider gemini --api-key "your-key"
company-platform configure-api --provider qwen --api-key "your-key"
```

未配置时默认使用 `mock`。

## 3. 训练内置具身智能公司

```bash
python scripts/generate_company_embodied.py
company-platform train-materials --materials-dir company_embodied --force --reset-company
company-platform list-colleagues
```

当前发布包默认就是 20 人版本，不再额外保留轻量 demo。

## 4. 其他常用命令

自动划分部门：

```bash
company-platform sync-departments --mode auto
```

混合划分部门：

```bash
company-platform sync-departments --mode mixed
```

手动指定部门：

```bash
company-platform assign-department \
  --slug example_zhangsan \
  --department backend \
  --reason "老系统 owner，固定归后端部"
```

全体公司大会：

```bash
company-platform all-hands \
  --question "老板问：我们下个季度要做一套双臂装配机器人通用操作平台，应该先点哪些部门和同事开会？"
```

部门交流：

```bash
company-platform department-exchange \
  --department-a perception \
  --department-b planning \
  --topic "状态表征、策略接口和失败回放"
```

项目策划：

```bash
company-platform project-plan \
  --name "双臂装配机器人通用操作平台" \
  --description "需要统一感知输入、技能编排、本体约束和仿真训练平台。"
```

启动 API：

```bash
company-platform serve-api --host 127.0.0.1 --port 8000
```

## 5. 说明

如果你要看“单个同事 skill 怎么采集和蒸馏”，请回到你原来的参考项目 `colleague-skill`。  
这个发布包只保留公司平台相关的最短使用路径。
