---
description: custom rules
globs:
alwaysApply: false
---

# 文件匹配
@file **/*.py
@file notebooks/**/*.ipynb

# 语言与交互
- 所有代码注释、函数说明、交互对话必须使用中文
- 所有 Cursor AI 的解释和建议必须全程中文，不允许英文输出

# 编程风格
- 遵循 PEP8 基础规范，但在科学计算、量化建模中允许适当调整
- 所有函数必须明确类型注解（包括参数和返回值）
- 严格避免使用裸 `except:`，必须指定异常类型, 发生异常时直接抛出，禁止使用failback等任何降级策略
- 使用 f-string 替代 `%` 或 `str.format()` 拼接字符串
- 禁止在核心模型逻辑中使用魔法数字，使用常量或 config 显式定义


# 数据处理规范
- 使用 `pandas` 进行表格数据处理，避免使用 `for` 遍历 DataFrame 行
- 使用 `numpy` / `scikit-learn` / `torch` 等库处理向量化特征
- 对时间序列数据，使用 `.resample()`、`.rolling()` 等高阶操作而非手工遍历
- 明确区分训练集、验证集、测试集，并以变量名明确表达（如 `X_train`, `y_test`）

# 机器学习模型训练
- 机器学习模型需封装为类（class），并至少包含以下方法：
  - `fit()`: 模型训练
  - `predict()`: 模型预测
  - `evaluate()`: 性能评估
- 所有模型必须支持保存与加载（`joblib`, `torch.save`, `pickle` 等）
- 优先使用 sklearn pipeline / Lightning / 自定义 class 封装参数与流程
- 所有超参数配置集中在 config 或 YAML 文件中管理，便于复现实验

# 可转债量化策略规则（示例性）
- 策略逻辑必须模块化，每个信号或因子单独封装为函数或类
- 回测模块需支持可视化分析（如使用 matplotlib、plotly、bt）
- 交易执行逻辑与因子计算逻辑分离，便于策略复用与调参
- 所有历史数据分析必须指定时间范围，避免未来函数问题（Look Ahead Bias）

# 文件与函数命名规范
- 文件、模块命名使用 snake_case（如 `signal_generator.py`）
- 函数和变量使用简洁明了的英文名（如 `generate_signal`, `filter_data`）
- 机器学习模型类使用 PascalCase（如 `LSTMRegressor`、`TimesNetModel`）

# Notebook 规范（用于研究）
- 每个 notebook 仅用于一个核心实验（如：某策略研究或模型调优）
- notebook 开头使用 markdown 说明实验背景、数据来源、目标
- 每段代码使用注释说明处理逻辑，必要时用 markdown 分层解释
- notebook 生成结果应支持自动保存（如通过 `mlflow`、`wandb`、或本地路径）

# 输出规范与日志
- 所有模型/策略输出应写入日志（如 `loguru`, `logging`）
- 日志信息包括时间、模块名、策略名、重要参数、结果摘要
- 实验结果如有图表，应保存为文件（.png 或 .pdf）

# 单元测试与代码质量
- 核心函数必须编写单元测试，测试文件放在 `tests/` 目录
- 重要模块建议使用 `pytest` 编写断言
- 对于数据处理、指标计算、策略回测等高风险模块建议测试覆盖率超过 80%
- 在模型上线或发布前运行 flake8/pylint 做静态检查

# 交互规范总结（必须中文）
- 所有交互内容必须为中文，包括代码注释、函数文档、模型解释
- Cursor AI 输出时必须使用中文，英文交互/注释一律禁止