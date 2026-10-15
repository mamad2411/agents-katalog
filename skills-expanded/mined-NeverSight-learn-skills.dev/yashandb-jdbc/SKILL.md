---
name: yashandb-jdbc
name_for_command: yashandb-jdbc
description: 指导用户完成 YashanDB Java 语言开发环境搭建。当用户提到 Java 开发、JDBC 驱动、Java 连接 YashanDB 或需要使用 JDBC 操作 YashanDB 时，必须使用此技能。
---

# YashanDB Java 开发环境搭建

本技能指导用户完成 YashanDB Java 开发环境的完整搭建流程。

> **重要提示**：YashanDB JDBC 驱动支持 JDK 1.8 及以上版本。

## 步骤概览

1. 检查环境（JDK、Maven/Gradle）
2. 安装 JDBC 驱动
3. 测试连接

## 第一步：检查环境

```bash
# 检查 Java 版本
java -version

# 检查 Maven（如使用 Maven）
mvn --version

# 检查 Gradle（如使用 Gradle）
gradle --version
```

## 第二步：安装 JDBC 驱动

### 使用 Maven（推荐）

在项目的 `pom.xml` 中添加依赖：

```xml
<dependency>
    <groupId>com.yashandb</groupId>
    <artifactId>yashandb-jdbc</artifactId>
    <version>1.6.1</version>
</dependency>
```

> **注意**：版本号 `1.6.1` 为示例版本，请访问 [Maven Central](https://mvnrepository.com/artifact/com.yashandb/yashandb-jdbc) 获取最新版本。

### 使用 Gradle

```groovy
dependencies {
    implementation 'com.yashandb:yashandb-jdbc:1.6.1'
}
```

## 第三步：测试连接

### 基础连接示例

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class App {
    public static void main(String[] args) {
        String driver = "com.yashandb.jdbc.Driver";
        String url = "jdbc:yasdb://127.0.0.1:1688/yasdb";
        String user = "system";
        String password = "oracle";

        try {
            Class.forName(driver);
            Connection conn = DriverManager.getConnection(url, user, password);
            System.out.println("连接成功！");

            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT 1 FROM dual");

            if (rs.next()) {
                System.out.println("查询结果: " + rs.getInt(1));
            }

            rs.close();
            stmt.close();
            conn.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### URL 格式

```
jdbc:yasdb://host:port/database?param1=value1&param2=value2
```

## 参考文档

- [installation](skills/yashandb-jdbc/references/installation.md)
- [connection](skills/yashandb-jdbc/references/connection.md)
- [troubleshooting](skills/yashandb-jdbc/references/troubleshooting.md)

## 相关资源

- YashanDB 官方文档：https://doc.yashandb.com
- JDBC 驱动下载：https://download.yashandb.com
- Maven Central：https://mvnrepository.com/artifact/com.yashandb/yashandb-jdbc