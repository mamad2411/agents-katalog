# AGENTS.md - Android 阅读器应用开发指南

## 构建与测试命令

### 运行应用
```bash
# 连接 Android 设备或启动模拟器
# 从 Android Studio 或 IDE 运行
```

### 清理构建
```bash
./gradlew clean
```

### 构建调试版 APK
```bash
./gradlew assembleDebug
```

### 构建发布版 APK
```bash
./gradlew assembleRelease
```

### 运行所有测试
```bash
./gradlew test
```

### 运行设备测试
```bash
./gradlew connectedAndroidTest
```

### 运行单个测试类
```bash
./gradlew test --tests BookshelfViewModelTest
```

### 运行单个测试方法
```bash
./gradlew test --tests BookshelfViewModelTest.testLoadBooks
```

### 代码检查
```bash
./gradlew lint
```

### 代码分析
```bash
./gradlew ktlintCheck
./gradlew detekt
```

## 代码风格规范

### Kotlin 风格

**文件组织**
- 源文件按模块组织：`presentation/ui/`、`data/`、`parser/` 等
- 保持文件在 200 行以内，大文件拆分为更小的模块
- 使用包名：`com.reader.app.{module}.{submodule}`

**命名约定**
- 类名：PascalCase（如 `BookshelfScreen`、`ReaderViewModel`）
- 函数名：camelCase（如 `loadBooks`、`parseContent`）
- 变量名：camelCase（如 `books`、`fontSize`）
- 常量：UPPER_SNAKE_CASE（如 `MAX_CACHE_SIZE`）
- 私有函数：以 `_` 开头（如 `_handleError`）

**文件结构**
1. 包声明
2. 导入（按组排序：标准库 → 第三方库 → 内部模块）
3. 类声明
4. 伴生对象（如果有）
5. 私有辅助函数
6. 公共接口方法
7. 实现

**导入顺序**
```kotlin
// 顺序：标准库 → androidx → 第三方库 → 内部模块

import android.content.Intent
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.reader.app.data.model.Book
import com.reader.app.di.AppModule
```

**格式化**
- 使用 2 空格缩进（不使用制表符）
- 函数开括号在同一行，类开括号在新行
- 行宽：最大 120 字符
- 函数之间添加空行
- 无尾随空格

### Compose UI 风格

**组件结构**
```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScreenName(
    viewModel: ViewModel = hiltViewModel(),
    onAction: () -> Unit
) {
    val state by viewModel.state.collectAsState()
    
    Scaffold(...) {
        Content(state, onAction)
    }
}
```

**状态管理**
- 始终在 Composable 函数中收集 StateFlow/Flow
- 使用 `collectAsState()` 并提供初始值
- 将 UI 状态与 ViewModel 中的业务逻辑分离
- 避免在 Composable 中直接产生副作用

### 架构风格

**MVVM 模式**
- **表现层**：Screens (Compose) + ViewModels
- **数据层**：Repositories + DAOs + Models
- **领域层**：（目前保留，暂无用例）
- **依赖关系**：表现层注入仓库；仓库注入 DAO

**ViewModel 指南**
```kotlin
@HiltViewModel
class BookshelfViewModel @Inject constructor(
    private val bookRepository: BookRepository,
    private val context: Application
) : ViewModel() {
    
    private val _books = MutableStateFlow<List<Book>>(emptyList())
    val books: StateFlow<List<Book>> = _books.asStateFlow()
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()
    
    fun loadBooks() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                _books.value = bookRepository.getAllBooks()
            } catch (e: Exception) {
                // 处理错误
            } finally {
                _isLoading.value = false
            }
        }
    }
}
```

**Repository 指南**
- 在 `data/repository/` 中实现接口（如 `RepositoryImpl`）
- 对 ViewModels 使用 `@ViewModelScoped`
- 对 Database/Preferences 使用 `@Singleton`
- 需要时用 Flow 转换包装 DAO 调用

**数据库层**
- 使用 `fallbackToDestructiveMigration()` 进行初始开发
- 实体类在 `data/local/database/entity/`
- DAO 在 `data/local/database/dao/`
- 转换函数（to/from entity）在 `data/model/`

### 错误处理

**ViewModel 错误**
```kotlin
private val _error = MutableStateFlow<String?>(null)
val error: StateFlow<String?> = _error.asStateFlow()

private fun handleError(e: Exception) {
    _error.value = e.message ?: "发生错误"
    // 记录错误
    e.printStackTrace()
}

fun clearError() {
    _error.value = null
}
```

**Composable 错误处理**
```kotlin
@Composable
fun ErrorBanner(
    message: String,
    onDismiss: () -> Unit
) {
    if (message.isNotBlank()) {
        Box(...) {
            Text(message)
            IconButton(onClick = onDismiss) {
                Icon(Icons.Default.Close)
            }
        }
    }
}
```

**网络错误**
- 用 try-catch 包装 API 调用
- 显示用户友好的消息
- 不要向 UI 暴露堆栈跟踪

### 类型安全

**数据类**
```kotlin
data class Book(
    val id: String,
    val title: String,
    val author: String,
    val filePath: String,
    val fileType: FileType,
    val coverPath: String?,
    val totalPages: Int,
    val addedTime: Long,
    val lastReadTime: Long,
    val isOnline: Boolean
)
```

**枚举类**
```kotlin
enum class FileType {
    EPUB,
    TXT,
    MOBI
}

enum class ThemeMode {
    LIGHT,
    EYE_CARE,
    DARK
}
```

**可空类型**
- 对可空值显式使用 `?`
- 对易出错操作使用 `runCatching`
- 使用 Elvis 运算符 `?:` 或 `run` 安全处理 null

### 依赖注入

**Hilt 指南**
- 用 `@AndroidEntryPoint` 标记 Application 类
- 对 ViewModels 使用 `@HiltViewModel`
- 使用 `@Inject constructor(...)` 进行手动注入
- 在模块类中使用 `@Provides`
- 对单例使用 `@Singleton`

**模块结构**
- 分离模块：`DatabaseModule`、`PreferencesModule`、`RepositoryModule`、`AppModule`
- 放置在 `di/` 包中
- 对单例使用 `@InstallIn(SingletonComponent::class)`

### 文件命名

**界面**
- `<ScreenName>Screen.kt`（如 `BookshelfScreen.kt`）
- `<ScreenName>ViewModel.kt`（如 `BookshelfViewModel.kt`）

**模块**
- `<Name>Parser.kt`（如 `TxtParser.kt`）
- `<Name>Worker.kt`（如 `ChapterCacheWorker.kt`）

**工具类**
- `UtilityName.kt`（如 `FileManager.kt`）
- `StateFlowExtensions.kt`（用于共享扩展函数）

### 注释与文档

**公共 API 的 KDoc**
```kotlin
/**
 * 解析 TXT 文件并提取书籍内容
 * 
 * @param filePath TXT 文件的路径
 * @return 包含标题、作者和章节的 Book 对象
 * @throws IOException 如果无法读取文件
 */
fun parseTxtFile(filePath: String): Book
```

**逻辑的内联注释**
- 使用 `//` 作为内联注释
- 解释"为什么"而不是"是什么"
- 避免注释显而易见的代码

### 并发指南

**协程**
```kotlin
// 在 ViewModel 中
viewModelScope.launch {
    // 长时间运行的操作
    val result = withContext(Dispatchers.IO) {
        // 后台工作
    }
    _state.value = result
}

// 在 Repository 中
suspend fun getData(): Result = withContext(Dispatchers.IO) {
    // 数据库/网络工作
}
```

**避免**
- 主线程上的阻塞操作
- 不带上下文启动新协程
- 从后台线程更新 MutableStateFlow

### Android 特定指南

**权限**
- 在 `AndroidManifest.xml` 中声明
- 对敏感权限在运行时请求
- 对 API 33+ 使用 `ActivityResultContracts`

**生命周期**
- 在 `onCleared()` 中释放资源
- 使用 `LaunchedEffect` 处理副作用
- 遵循生命周期感知组件

**性能**
- 对 Compose 性能使用 `remember` 和 `key`
- 长列表使用 Lazy 布局
- 内存高效的数据结构
- 使用 Coil 加载图片

### 测试指南

**单元测试**
- 放置在 `src/test/java/`
- 测试 ViewModels、repositories、parsers
- 对协程使用 `TestDispatcher`
- 使用 `MockK` 模拟依赖

**集成测试**
- 放置在 `src/androidTest/java/`
- 使用 `ComposeTestRule` 测试 UI 界面
- 测试数据库操作

### 代码审查检查清单

- [ ] 遵循命名约定
- [ ] 正确的错误处理
- [ ] 无未使用的导入
- [ ] 无死代码
- [ ] 正确的 MVVM 架构
- [ ] Hilt 依赖正确注入
- [ ] StateFlow 在后台线程更新
- [ ] Composable 函数纯净（无副作用）
- [ ] 无魔法数字（使用常量）
- [ ] 资源文件可访问
- [ ] 测试覆盖充分

### 版本控制

**提交消息**
- 使用约定式提交：`feat: 添加章节缓存`
- 简洁而描述性
- 如适用，引用问题编号

**分支**
- `main` 用于生产
- `develop` 用于集成
- 功能分支：`feature/xxx`
- 修复分支：`fix/xxx`
