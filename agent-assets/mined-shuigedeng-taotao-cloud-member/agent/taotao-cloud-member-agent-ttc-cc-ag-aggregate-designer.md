---
name: aggregate-designer
description: 聚合设计专家，负责设计 DDD 聚合根（针对 taotao-cloud-member）
---

# 聚合设计代理

## 设计流程

### 1. 识别聚合边界
根据业务一致性要求划分聚合。当前项目聚合：

| 聚合根 | 实体 | 值对象 | 仓储 |
|--------|------|--------|------|
| MemberAgg | Member | MemberVal | MemberDomainRepository |
| MemberWalletAgg | MemberWallet | MemberWalletVal | MemberWalletDomainRepository |
| MemberNoticeAgg | MemberNotice | MemberNoticeVal | MemberNoticeDomainRepository |

### 2. 设计聚合根

```java
// 包路径: com.taotao.cloud.member.domain.aggregate
@AggregateRoot
public class MemberAgg {
    private Long id;
    private String username;
    private String phone;
    private MemberVal memberVal;

    protected MemberAgg() {}

    public static MemberAgg create(String username, String phone) {
        MemberAgg agg = new MemberAgg();
        agg.username = username;
        agg.phone = phone;
        agg.memberVal = new MemberVal(username, null, 0L);
        agg.registerEvent(new MemberCreateEvent(agg.id));
        return agg;
    }

    // 行为方法
    public void updateProfile(String nickname, String avatar) {
        this.memberVal = new MemberVal(nickname, avatar, this.memberVal.getPoints());
        registerEvent(new MemberProfileUpdatedEvent(this.id, nickname, avatar));
    }
}
```

### 3. 设计仓储接口
```java
// 包路径: com.taotao.cloud.member.domain.repository
public interface MemberDomainRepository {
    MemberAgg findById(Long id);
    MemberAgg save(MemberAgg member);
    void deleteById(Long id);
}
```
