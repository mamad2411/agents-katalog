---
name: egovframe-compatibility
description: Use when reviewing or writing eGovFrame 4.x or 5.x Java code — Controller, Service, DAO, configuration, or library usage. Covers inheritance requirements, forbidden call patterns, and architecture constraints. Assumes Spring Framework knowledge.
---

# eGovFrame Compatibility Rules

## Overview

eGovFrame 4.x/5.x adds constraints on top of Spring conventions for government system development. Only eGovFrame-specific rules are documented here — Spring Framework knowledge assumed.

**Scope:** Java projects using `org.egovframe.rte.*` (eGovFrame 4.x+). Excludes `egovframework.rte.*` (3.10 and earlier), non-Java code, and frontend concerns.

---

## Controller Layer

**Target:** `@Controller`, `@RestController`, and Servlet code only when Spring MVC is impractical and justified.

**Rules:**
1. Map handlers with Spring MVC annotations.
2. Do not inject or call DAO classes directly, including subclasses of `SqlMapClientDaoSupport`, `SqlSessionDaoSupport`, and `HibernateDaoSupport`.
3. No direct NoSQL, MQ, or cache access from controllers.
4. Route business logic through an injected service interface.

```java
// ✅ Correct
@Controller
@RequestMapping("/sample")
public class SampleController {
    @Autowired
    private SampleService sampleService;

    @GetMapping("/list")
    public String list(Model model) {
        model.addAttribute("list", sampleService.selectList());
        return "sample/list";
    }
}

// ❌ DAO injected directly — forbidden
@Controller
public class SampleController {
    @Autowired
    private SampleMapper sampleMapper; // ❌ inject Service, not DAO
}

// ❌ Business logic handled inside controller — forbidden
@GetMapping("/calc")
public String calc(Model model) {
    int result = heavyBusinessCalculation(); // ❌ delegate to Service
    model.addAttribute("result", result);
    return "sample/result";
}
```

---

## Service Layer

**Target:** `@Service` or `@Component` business classes, excluding tests.

**Rules:**
1. Each service implementation must extend `EgovAbstractServiceImpl`, directly or through a base class.
2. Each service implementation must implement a dedicated service interface.

**Why the interface matters:** eGovFrame AOP relies on Java Dynamic Proxy, not CGLIB — class-only services cannot be proxied.

```java
// ✅ Correct — interface + implementation pair
public interface SampleService {
    List<SampleVO> selectList(SampleVO vo) throws Exception;
}

@Service("sampleService")
public class SampleServiceImpl extends EgovAbstractServiceImpl implements SampleService {
    @Autowired
    private SampleMapper sampleMapper;

    @Override
    public List<SampleVO> selectList(SampleVO vo) throws Exception {
        return sampleMapper.selectList(vo);
    }
}

// ❌ No interface — Java Proxy cannot proxy a class-only service
@Service
public class SampleService extends EgovAbstractServiceImpl { }

// ❌ Missing EgovAbstractServiceImpl
@Service
public class SampleServiceImpl implements SampleService { }
```

---

## DAO / Data Access Layer

**Target:** `@Repository` classes and mapper/repository code.

| Technology | Required pattern |
|------------|------------------|
| iBatis | `extends EgovAbstractDAO` |
| MyBatis class mapper | `extends EgovAbstractMapper` |
| MyBatis interface mapper | `@Mapper` plus eGovFrame `MapperConfigurer` |
| JPA | `extends JpaRepository`, `CrudRepository`, or `PagingAndSortingRepository` |
| JPA alternative | Inject `HibernateTemplate` or `EntityManager` directly or via a base class |

**Forbidden:** Direct calls to `insert`, `delete`, `update`, `select`, or `list` on `SqlMapClientDaoSupport` or `SqlSessionDaoSupport`.

```java
// ✅ MyBatis class mapper
@Repository
public class SampleMapper extends EgovAbstractMapper {
    public List<SampleVO> selectList(SampleVO vo) {
        return selectList("sample.selectList", vo);
    }
}

// ✅ MyBatis interface mapper
@Mapper
public interface SampleMapper {
    List<SampleVO> selectList(SampleVO vo);
}

// ✅ JPA
public interface SampleRepository extends JpaRepository<Sample, Long> {
    List<Sample> findByStatus(String status);
}

// ❌ Direct SqlSessionDaoSupport call — forbidden
@Repository
public class SampleDAO extends SqlSessionDaoSupport {
    public List<SampleVO> selectList(SampleVO vo) {
        return getSqlSession().selectList("sample.selectList", vo); // ❌
    }
}
```

---

## Configuration Layer

**Target:** XML config plus equivalent Java Config or Spring Boot config.

**Required inclusions:**
- Transaction handling via AOP config (`<tx:advice>` plus `<aop:config>`) or `@Transactional`
- A connection pool such as DBCP or HikariCP

```xml
<!-- ✅ AOP transaction + DBCP -->
<tx:advice id="txAdvice" transaction-manager="transactionManager">
    <tx:attributes>
        <tx:method name="*" rollback-for="Exception"/>
    </tx:attributes>
</tx:advice>
<aop:config>
    <aop:pointcut id="txPointcut" expression="execution(* *..*ServiceImpl.*(..))"/>
    <aop:advisor advice-ref="txAdvice" pointcut-ref="txPointcut"/>
</aop:config>

<bean id="dataSource" class="org.apache.commons.dbcp2.BasicDataSource" destroy-method="close"/>
```

```java
// ✅ Java Config
@Configuration
@EnableTransactionManagement
public class AppConfig {
    @Bean
    public DataSource dataSource() {
        return new HikariDataSource();
    }
}
```

```xml
<!-- ❌ No transaction configuration — eGovFrame feature not applied -->
<!-- ❌ Using JDBC DriverManager directly — no connection pool -->
```

---

## Library and Extension Rules

**Required libraries:** use the same version for all of these:

```text
org.egovframe.rte.ptl.mvc-[version].jar
org.egovframe.rte.fdl.cmmn-[version].jar
org.egovframe.rte.psl.dataaccess-[version].jar
org.egovframe.rte.fdl.logging-[version].jar
```

**Library rules:**
- Do not modify `org.egovframe.rte.*` JARs — MD5/SHA1 must match original distribution.
- Do not change Spring Framework or Spring Boot versions through transitive deps, except for a justified patch upgrade.

**Extension rules:** if extending an eGovFrame RTE class:

```java
// ❌ Forbidden package
package org.egovframe.rte.custom; // ❌ must not define classes inside rte packages
public class MyDAO extends EgovAbstractDAO { }

// ❌ Forbidden naming
public class EgovCustomDAO extends EgovAbstractDAO { } // ❌ must not start with "Egov"

// ✅ Correct extension
package com.example.common.dao;
public class CommonDAO extends EgovAbstractDAO { }
```

---

## Overall Application Rules

- Keep the request path as `Controller → Service → DAO`; do not skip layers.
- Every project must contain all three layers, with service interface/implementation pairs.

**Package layout** — choose one and apply consistently across the entire project:

```
// ✅ Domain-first (applied consistently)
com.example.sample.controller.SampleController
com.example.sample.service.SampleService
com.example.sample.dao.SampleMapper

// ✅ Layer-first (applied consistently)
com.example.controller.sample.SampleController
com.example.service.sample.SampleService
com.example.dao.sample.SampleMapper

// ❌ Mixed layout — forbidden
com.example.sample.controller.SampleController   // domain-first
com.example.service.other.OtherService           // layer-first (mixed)
```

**Naming convention** — choose one and apply consistently:

```java
// ✅ Business-code style (applied consistently)
AA0011Controller, AA0011ServiceImpl, AA0011Mapper

// ✅ Word style (applied consistently)
MemberController, MemberServiceImpl, MemberMapper

// ❌ Mixed styles — forbidden
AA0011Controller    // business-code style
MemberServiceImpl   // word style (mixed)
```
