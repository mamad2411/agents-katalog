---
name: inventory-alert
description: 电商库存预警 - 监控库存水位，低于阈值自动告警。支持多平台库存同步，防止断货超卖。
version: 1.0.0
author: auto-company
tags:
  - ecommerce
  - inventory
  - alert
  - stock-management
  - automation
price: 0
triggers:
  - 库存预警
  - 库存提醒
  - 库存管理
  - 库存告警
  - 防止断货
---

# Inventory Alert

电商库存预警技能 - 帮你告别断货烦恼。

## 功能特性

### 1. 库存监控
- 实时监控商品库存数量
- 支持多平台：Shopify、WooCommerce、淘宝、京东
- 库存同步延迟 < 5 分钟

### 2. 智能告警
- 低于安全库存时自动通知
- 多级预警：提醒 → 警告 → 紧急
- 告警渠道：邮件、微信、Discord、Telegram

### 3. 补货建议
- 基于销售速度预测补货时间
- 智能推荐补货数量
- 避免过度库存

## 使用方法

### 设置告警
```
SKU: [商品SKU]
安全库存: [数量]
告警渠道: [邮件/微信]
```

### 查看库存
```
显示所有低库存商品
按紧急程度排序
```

### 补货预测
```
预测 [商品SKU] 还能卖几天
根据最近 [X] 天销售数据
```

## 约束

- 需要电商平台 API 授权
- 不修改任何库存数据
- 仅读取和监控
