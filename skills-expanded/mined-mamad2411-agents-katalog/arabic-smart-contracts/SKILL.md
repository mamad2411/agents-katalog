---
name: arabic-smart-contracts
name_ar: عقود ذكية
description: Master smart contracts development in Arabic
description_ar: إتقان تطوير العقود الذكية بالعربية
category: blockchain
language: ar
dialect: msa
rtl: true
platform_all: true
version: 1.0.0
author: salman-shaikh
---

## الهدف

إتقان أساسيات تطوير العقود الذكية على Ethereum و blockchain.

## مفاهيم أساسية

### ١. ما هو العقد الذكي؟

**الوصف:**
- كود على blockchain
- ينفذ تلقائياً
- لا مركزي
- غير قابل للتعديل

### ٢. Solidity أساسيات

```solidity
// مثال بسيط
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 storedData;
    
    function set(uint256 x) public {
        storedData = x;
    }
    
    function get() public view returns (uint256) {
        return storedData;
    }
}
```

### ٣. معايير Tokens

| المعيار | الوصف |
|---------|-------|
| **ERC-20** | عملات قابلة للاستبدال |
| **ERC-721** | NFTs - فريدة |
| **ERC-1155** | متعددة الأنواع |

## أدوات التطوير

| الأداة | الوصف |
|--------|-------|
| **Remix** | IDE عبر الإنترنت |
| **Hardhat** | بيئة تطوير |
| **Truffle** | إطار تطوير |
| **Foundry** | تطوير واختبار |

## أفضل الممارسات

✅ اختبر extensively
✅ تدقيق أمني
✅ Gas optimization
✅ اتبع المعايير

❌ لا تنشر بدون تدقيق
❌ لا تهمل reentrancy
❌ لا تبالغ في التعقيد

---

## الكلمات المفتاحية

عربي: "عقود ذكية", "Solidity", "blockchain", "Ethereum"
English: "smart contracts arabic", "Solidity", "Ethereum", "blockchain development"

---

## سجل التغييرات

### v1.0.0
- الإصدار الأولي
