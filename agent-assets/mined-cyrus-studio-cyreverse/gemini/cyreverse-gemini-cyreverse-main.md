# Project Guidelines

为了保持项目结构的整洁和一致性，请遵循以下开发规范：

1. **示例入口**：`app/src/main/java/com/cyrus/example/MainActivity.kt` 是所有示例代码的统一入口类。
2. **新增案例**：
   - 如需增加新的案例，请在 `app/src/main/java/com/cyrus/example` 目录下创建一个独立的子包（package）。
   - 在该子包内创建对应的 `Activity`。
3. **技术栈要求**：新增的案例 Activity 必须使用 **Kotlin** 编写，并使用 **Jetpack Compose UI** 实现界面。
