---
name: emlog-app-dev
description: 协助开发 Emlog 应用（包括插件和主题）。当用户想要创建新插件或主题、修改迭代现有插件或主题、询问 Emlog 应用开发规范、查找模板变量、使用系统通用函数或挂载点时调用。Make sure to use this skill whenever the user mentions emlog plugins, emlog themes, emlog templates, php emlog, Emlog插件, Emlog主题, Emlog模板, 插件开发, 主题开发, 或者 Emlog 相关开发需求。
---

# Emlog 应用开发助手 (插件与主题)

此 Skill 旨在协助您开发 Emlog 应用，包括插件 (Plugin) 和主题 (Theme/Template)。它包含最新的开发规范、目录结构、接口文档及最佳实践。

## 目录与文件查找指南

根据用户的开发目标，可以快速查阅以下更详细的参考文档：
- **系统调用与通用函数**：[develop_func.md](./references/develop_func.md) (包含 Input/Output 类、数据存储、支付/AI 对接、用户/积分操作、全局函数等)
- **插件开发完整规范**：[plugin.md](./references/plugin.md) (包含后台配置、钩子机制、数据库操作、回调等)
- **主题开发完整规范**：[template.md](./references/template.md) (包含模板结构、变量列表、常用常量、公共页面调用等)

---

## 核心开发规范（通用）

### 1. 防止直接访问
所有 PHP 文件头部必须包含以下安全检查，防止被直接运行：
- **插件代码** 头部：
  ```php
  defined('EMLOG_ROOT') || exit('access denied!');
  ```
- **主题代码** 头部：
  ```php
  if(!defined('EMLOG_ROOT')) {exit('error!');}
  ```

### 2. 环境兼容性
- 所有的 PHP 代码开发必须适配 PHP 7.4+ 版本，避免使用高版本专有且在 7.4 不支持的语法。

### 3. 注意事项

- 避免过多的使用emoji表情，保持内容简洁明了
- 避免直接引用外部网络css、js、字体文件资源，需要时可以下载到应用内使用
- 避免使用过多字体文件导致安装包超过5MB，尽量控制在1MB左右
- 在UI配色上禁止使用紫色渐变、高饱和度的纯色艳丽配色。
- 尽量使用emlog自身支持的核心数据库表（如，点赞、评论、订单、用户等数据表），避免创建过多额外的数据库表。

---

## Emlog 插件开发指南

### 1. 目录结构
插件位于 `content/plugins/<plugin_alias>/` 目录下：
- `<plugin_alias>.php`：核心主文件。包含插件元数据（Header）和钩子注册。
- `<plugin_alias>_callback.php`：生命周期回调。定义激活(`callback_init`)、更新(`callback_up`)、删除(`callback_rm`)时的逻辑。
- `<plugin_alias>_setting.php`：后台设置页。包含 `plugin_setting_view` 函数。
- `<plugin_alias>_show.php`：前台独立页面构建。
- `preview.jpg`：预览图（75x75 像素，JPG格式）。

### 2. 命名规范与数据清理
- **插件别名**：只能包含小写字母、数字、下划线、横杠，且以字母开头。
- **函数命名**：必须使用插件别名作为前缀（如 `my_tool_func`），防止冲突。
- **绿色卸载**：严禁随意修改系统核心表；卸载时（`callback_rm`）务必清理所有自建数据（如使用 `Storage::getInstance('plugin_alias')->deleteAllName('YES')`）。

```php
/**
 * 插件激活回调函数：用于在插件激活时初始化数据
 * @return void
 */
function callback_init() {
    $storage = Storage::getInstance('my_plugin');
    $storage->setValue('status', 'active');
}

/**
 * 插件卸载回调函数：用于在插件卸载时清理所有数据，保持系统干净
 * @return void
 */
function callback_rm() {
    $storage = Storage::getInstance('my_plugin');
    $storage->deleteAllName('YES');
}
```

### 3. 常用钩子 (Hooks)
使用 `addAction('hook_name', 'function_name')` 注册。
- **后台**：`adm_head`, `adm_footer`, `adm_main_top`, `save_log` (参数: `$blogid, $pubPost, $logData`), `del_log` (参数: `$blogid`), `adm_writelog_head`, `adm_writelog_side`
- **前台**：`index_head`, `index_footer`, `log_related` (参数: `$logData`), `comment_post`, `comment_saved`

---

## Emlog 主题开发指南

### 1. 目录结构
模板位于 `content/templates/<template_alias>/` 目录下：
- `header.php`：站点头部信息（包含 head 信息、顶部标题、导航栏，开头必须包含模板信息注释）
- `log_list.php`：首页/列表页（展示文章列表）
- `echo_log.php`：文章详情页（展示单篇文章内容）
- `footer.php`：站点底部信息
- `page.php`：自定义页面（非必须）
- `module.php`：功能模块（定义侧边栏组件、自定义函数等，非必须）
- `options.php`：模板设置（后台选项，非必须）
- `preview.jpg`：预览图（500x300 像素，JPG格式）

### 2. 引用模板文件
在模板中引入其他组件时，**必须**使用系统自带的 `View::getView` 方法：
```php
require_once View::getView('header');
require_once View::getView('side');
require_once View::getView('footer');
```

### 3. 常用变量与常量
- **常量**：`BLOG_URL` (站点首页 URL), `TEMPLATE_URL` (当前模板文件夹 URL)
- **列表页变量**：`$value['logid']`, `$value['log_title']`, `$value['log_url']`, `$value['log_cover']`
- **详情页变量**：`$logid`, `$log_title`, `$log_content`, `$date`

---

## 系统调用与通用函数 (通用)

插件和主题开发均可使用以下核心类与全局方法：

### 1. 获取输入 (Input 类)
禁止使用 `$_GET` / `$_POST` / `$_REQUEST`，防止 SQL 注入。
```php
// 获取 POST 提交的字符型变量，默认值为空
$str = Input::postStrVar('name', '');
// 获取 GET 提交的整型变量，默认值为 0
$int = Input::getIntVar('id', 0);
// 获取 POST 提交的整型数组，例如 ids[]
$ids = Input::postIntArray('ids');
```

### 2. 输出响应 (Output 类)
主要用于插件接口或 AJAX 交互，避免直接 `echo json_encode(...)`。
```php
// 输出操作成功带回数据并终止脚本
Output::ok(['id' => 1]);
// 输出操作失败提示信息并终止脚本
Output::error('Permission denied');
```

### 3. 存储配置 (Storage 类)
使用 `Storage` 类存储键值对，禁止使用写文件的方式保存配置。
```php
// 获取插件专属的 Storage 单例
$storage = Storage::getInstance('my_plugin_or_theme');
// 保存配置项的值
$storage->setValue('key', 'value');
// 读取配置项的值
$val = $storage->getValue('key');
```

### 4. 其它常用全局函数
- **友好时间**：`smartDate($timestamp)` -> 返回 "1分钟前" 等
- **截取内容**：`subContent($content, 180, 1)` -> 截取180字并过滤HTML标签
- **首图获取**：`getFirstImage($content)` -> 获取内容首张图片 URL
- **提示消息**：`emMsg($msg)` -> 输出友好提示，支持 HTML
