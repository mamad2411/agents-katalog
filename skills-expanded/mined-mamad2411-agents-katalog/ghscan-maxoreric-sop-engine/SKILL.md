# health-data-collect

**用途**: 收集用户的每日健康数据

**输入**:
```yaml
date: string        # 日期，格式 YYYY-MM-DD
user_id: string     # 用户 ID
```

**输出**:
```yaml
status: string      # 状态：success / error
date: string        # 数据日期
data:
  temperature: number   # 体温（摄氏度）
  heart_rate: number    # 心率（次/分钟）
  steps: number         # 步数
timestamp: string   # 采集时间戳
```

## 执行逻辑

### 模拟模式（当前）
返回模拟的健康数据，用于测试和演示。

### 生产模式（待实现）
1. 连接健康设备 API
2. 获取用户的实时健康数据
3. 验证数据有效性
4. 返回标准化的数据格式

## 数据范围

- **体温**: 35.0 - 39.0°C（正常范围：36.0 - 37.5°C）
- **心率**: 50 - 120 bpm（正常范围：60 - 100 bpm）
- **步数**: 0 - 20000（建议：≥ 5000）
