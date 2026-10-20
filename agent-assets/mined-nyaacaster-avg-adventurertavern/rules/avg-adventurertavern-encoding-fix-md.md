---
alwaysApply: false
---

# 编码修复 Agent

当用户遇到文件编码问题、HTML 实体错误、构建时出现 `=&gt;` 等异常字符时，按以下流程处理。

## 诊断流程

### 第一步：扫描编码问题
```powershell
npm run check-encoding
```
查看输出，确认哪些文件存在 HTML 实体（`&gt;` `&lt;` `&amp;` `&quot;`）。

### 第二步：自动修复
```powershell
npm run fix-encoding
```

### 第三步：验证修复
```powershell
npm run build
```
构建成功则修复完成，直接进入提交流程。

### 第四步：提交
```powershell
git add .
git commit -m "fix: 修复文件编码问题"
git push
```

## 首次环境配置（新克隆仓库时）

```powershell
git config --global core.autocrlf false
git config --global core.eol lf
git config --global core.safecrlf false
git config core.hooksPath .githooks
git add --renormalize .
git commit -m "chore: 规范化文件编码"
```

## 问题持续时的完全重置

```powershell
# 清除 Git 缓存
git rm --cached -r .
git reset --hard
git add .
git commit -m "fix: 重新添加所有文件"

# 清除 Docker 构建缓存
docker builder prune -af
```

## 参考文档

详细技术说明见 `Doc/WorkStandard/ENCODING-FIX/ENCODING-FIX.md`
开发规范和提交流程见 `Doc/WorkStandard/ENCODING-FIX/CONTRIBUTING.md`