---
alwaysApply: true
description: "QA测试规则 - 固定目录和模型要求"
---

# 🧪 QA测试强制规则

## 📁 测试目录要求（强制性）

### 输入视频目录
- **必须使用**: [test_videos/](mdc:test_videos/) 
- ⚠️ **绝对禁止**：使用其他目录作为视频输入源
- 📋 包含20个真实Figma教学视频文件(.mp4)

### 输出文件目录  
- **必须使用**: [test_output/](mdc:test_output/)
- ⚠️ **绝对禁止**：输出到其他目录
- 🧹 每次测试前确保目录为空或清理旧文件

## 🤖 AI模型要求（强制性）

### Gemini模型版本
- **必须使用**: `Gemini 2.5 Pro`
- ⚠️ **绝对禁止**：使用其他版本(如1.5 Pro, Flash等)
- 🔧 确保[config.yaml](mdc:config.yaml.example)中model设置正确

## 📝 测试命令规范

### 单视频测试
```bash
python -m src.gs_video_report.cli.app single test_videos/[视频文件] --output test_output --verbose
```

### 批量处理测试
```bash  
python -m src.gs_video_report.cli.app batch test_videos --output test_output --verbose
```

### 并发控制验证
- 🔒 默认最大并发: **2个视频**
- 🚫 防止无限线程增长
- 💰 避免API Token浪费
- 🌐 防止网络拥塞

## 🎯 测试重点验证

### 核心功能
1. **Gemini 2.5 Pro API集成**
2. **批量处理机制**
3. **长时间运行稳定性**
4. **并发控制有效性**

### 质量门控
- ✅ 所有[test_videos/](mdc:test_videos/)中的视频都能成功处理
- ✅ 输出文件正确保存到[test_output/](mdc:test_output/)
- ✅ 并发数严格控制在2个以内
- ✅ 失败恢复机制正常工作

## ⚠️ 违规后果

如果测试时发现：
- 使用了错误的输入/输出目录
- 使用了错误的AI模型版本
- 没有按照并发控制要求

**立即停止测试，修正配置后重新开始！**

---
*此规则确保QA测试的一致性和有效性*