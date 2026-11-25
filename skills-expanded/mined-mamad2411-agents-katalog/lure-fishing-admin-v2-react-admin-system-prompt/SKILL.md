# React B端管理系统标准化提示词

## 项目概述

请创建一个基于React + TypeScript + Vite + Ant Design + Tailwind CSS的现代化B端管理系统，具备完整的用户认证、系统管理和数据展示功能。

## 技术栈要求

### 核心技术栈
- **前端框架**: React 18.3.1 + TypeScript 5.8.3
- **构建工具**: Vite 6.3.5
- **UI组件库**: Ant Design 5.26.7
- **图标库**: @ant-design/icons 6.0.0 + lucide-react 0.511.0
- **路由管理**: React Router DOM 7.7.1
- **状态管理**: Zustand 5.0.3
- **样式框架**: Tailwind CSS 3.4.17
- **工具库**: clsx 2.1.1 + tailwind-merge 3.0.2
- **通知组件**: sonner 2.0.2
- **图表库**: echarts 5.5.1

### 开发工具配置
- **代码检查**: ESLint 9.25.0 + TypeScript ESLint 8.30.1
- **样式处理**: PostCSS 8.5.3 + Autoprefixer 10.4.21
- **路径别名**: vite-tsconfig-paths 5.1.4
- **类型定义**: @types/react 18.3.12 + @types/react-dom 18.3.1 + @types/node 22.15.30

## 项目结构要求

```
src/
├── components/          # 通用组件
│   ├── Breadcrumb.tsx  # 面包屑导航组件
│   └── Empty.tsx       # 空状态组件
├── hooks/              # 自定义Hook
│   └── useTheme.ts     # 主题Hook
├── lib/                # 工具库
│   └── utils.ts        # 通用工具函数
├── pages/              # 页面组件
│   ├── Home.tsx        # 首页
│   ├── Login.tsx       # 登录页
│   ├── SystemManagement.tsx  # 系统管理主页
│   └── system/         # 系统管理子页面
│       ├── UserManagement.tsx     # 用户管理
│       ├── RoleManagement.tsx     # 角色管理
│       └── PermissionManagement.tsx # 权限管理
├── assets/             # 静态资源
├── App.tsx            # 应用主组件
├── main.tsx           # 应用入口
├── index.css          # 全局样式
└── vite-env.d.ts      # Vite类型定义
```

## 核心配置文件

### package.json 脚本配置
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "eslint .",
    "preview": "vite preview",
    "check": "tsc -b --noEmit"
  }
}
```

### vite.config.ts 配置
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [
    react(),  // 使用默认配置，避免babel-plugin-react-dev-locator依赖问题
    tsconfigPaths()
  ],
})
```

### postcss.config.js 配置
```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### tailwind.config.js 配置
```javascript
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    container: {
      center: true,
    },
    extend: {},
  },
  plugins: [],
};
```

### tsconfig.json 路径别名配置
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## 应用架构设计

### 主应用布局 (App.tsx)

**布局结构**:
- 左侧可折叠导航栏 (Sider)
- 顶部标题栏 (Header) 包含折叠按钮和用户菜单
- 主内容区域 (Content) 包含路由页面

**关键特性**:
- 响应式侧边栏折叠
- 用户登录状态管理
- React Router导航集成
- 统一的页面布局容器

**样式规范**:
- 侧边栏: 白色背景，浅色主题，品牌标识居中显示
- 顶部栏: 白色背景，阴影效果，用户头像和下拉菜单
- 内容区: 透明背景，模块化布局，16px外边距

### 主内容区模块化布局规范

**设计原则**:
- 主内容区背景设为透明 (`background: 'transparent'`)
- 功能模块独立分离，每个模块使用白色背景卡片
- 同行模块高度必须保持一致
- 模块间距统一，视觉效果整齐专业

**模块分离策略**:
1. **筛选操作区**: 包含搜索框、筛选条件、操作按钮等
2. **数据列表区**: 包含表格、分页等数据展示组件
3. **统计信息区**: 包含数据统计卡片、图表等
4. **功能操作区**: 包含快捷操作、工具按钮等

**高度对齐解决方案**:
```typescript
// 使用 Row 和 Col 实现同行模块高度对齐
<Row gutter={[16, 16]} style={{ display: 'flex', alignItems: 'stretch' }}>
  <Col xs={24} lg={12} style={{ display: 'flex' }}>
    <Card 
      style={{ 
        width: '100%',
        display: 'flex', 
        flexDirection: 'column' 
      }}
      bodyStyle={{ 
        flex: 1, 
        display: 'flex', 
        flexDirection: 'column' 
      }}
    >
      {/* 模块内容 */}
    </Card>
  </Col>
  <Col xs={24} lg={12} style={{ display: 'flex' }}>
    <Card 
      style={{ 
        width: '100%',
        display: 'flex', 
        flexDirection: 'column' 
      }}
      bodyStyle={{ 
        flex: 1, 
        display: 'flex', 
        flexDirection: 'column' 
      }}
    >
      {/* 模块内容 */}
    </Card>
  </Col>
</Row>
```

**CSS样式规范**:
```typescript
// 主内容区容器样式
const contentStyle = {
  background: 'transparent',  // 透明背景
  margin: '16px',            // 统一外边距 (重要：距离标题栏、导航栏、屏幕右侧)
  minHeight: 'calc(100vh - 112px)' // 最小高度
};

// 模块卡片样式
const moduleCardStyle = {
  background: '#ffffff',      // 白色背景
  borderRadius: '8px',       // 圆角
  boxShadow: '0 1px 4px rgba(0,21,41,.08)', // 阴影
  border: '1px solid #f0f0f0', // 边框
  marginBottom: '16px'       // 底部间距
};

// 页面容器样式 (重要：禁止使用内间距)
const pageContainerStyle = {
  background: 'transparent',  // 透明背景
  // 重要：禁止设置 padding，页面布局完全依靠模块间 margin 控制
};

// Flex布局确保高度一致
const flexRowStyle = {
  display: 'flex',
  alignItems: 'stretch'      // 拉伸对齐
};

const flexColStyle = {
  display: 'flex'
};
```

**模块背景设计原则**:
- **模块外部**: 透明背景，不设置任何颜色
- **模块内部**: 白色背景 (`#ffffff`)
- **模块边框**: 浅灰色边框 (`#f0f0f0`)
- **模块阴影**: 轻微阴影效果增强层次感
- **模块圆角**: 8px圆角保持现代感

**响应式布局要求**:
- 大屏幕 (≥992px): 多列并排显示
- 中等屏幕 (768px-991px): 2列显示
- 小屏幕 (<768px): 单列堆叠显示
- 使用 Ant Design 的 `Row` 和 `Col` 组件实现响应式

**间距和布局最新规范** (重要更新):

1. **主内容区外间距**: 
   - App.tsx 中 Content 组件设置 `margin: '16px'`
   - 确保主内容区距离标题栏、导航栏、屏幕右侧有统一的16px间距

2. **页面内间距规范**:
   - 所有页面容器（Home.tsx、UserManagement.tsx等）禁止设置 `padding`
   - 页面布局完全依靠模块间的 `margin` 和 Card 组件内部间距控制

3. **布局控制策略**:
   - 外层容器：透明背景 + 无内间距
   - 模块间距：通过 Card 组件的 `marginBottom: '16px'` 控制
   - 模块内容：依靠 Card 组件默认的内间距

**实际应用示例**:
```typescript
// 用户管理页面模块化布局 (最新规范)
return (
  <div style={{ background: 'transparent' }}> {/* 禁止设置 padding */}
    {/* 筛选操作区 */}
    <Card style={moduleCardStyle} className="mb-4">
      <Row gutter={16} align="middle">
        <Col flex="auto">
          <Input.Search placeholder="搜索用户..." />
        </Col>
        <Col>
          <Button type="primary">新增用户</Button>
        </Col>
      </Row>
    </Card>
    
    {/* 数据列表区 */}
    <Card style={moduleCardStyle}>
      <Table dataSource={users} columns={columns} />
    </Card>
  </div>
);

// App.tsx 主内容区配置 (最新规范)
<Content style={{
  background: 'transparent',
  margin: '16px',  // 重要：外间距设置
  minHeight: 'calc(100vh - 112px)'
}}>
  <Routes>
    {/* 路由配置 */}
  </Routes>
</Content>
```

### 导航菜单配置
```typescript
const menuItems = [
  {
    key: '/',
    icon: <HomeOutlined />,
    label: '首页',
  },
  {
    key: '/system',
    icon: <SettingOutlined />,
    label: '系统管理',
    children: [
      { key: '/system/users', label: '用户管理' },
      { key: '/system/roles', label: '角色管理' },
      { key: '/system/permissions', label: '权限管理' },
    ],
  },
];
```

### 侧边栏样式配置
```typescript
// 侧边栏组件配置 - 白色背景主题
<Sider trigger={null} collapsible collapsed={collapsed} style={{ background: '#fff' }}>
  {/* Logo区域 - 白色背景 */}
  <div style={{ 
    height: 32, 
    margin: 16, 
    background: '#f0f2f5',  // 浅灰背景区分logo区域
    borderRadius: 6,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: '#1890ff',       // 蓝色文字
    fontWeight: 'bold'
  }}>
    {collapsed ? 'MS' : '管理系统'}
  </div>
  
  {/* 菜单组件 - 浅色主题 */}
  <Menu
    theme="light"          // 使用浅色主题替代深色主题
    mode="inline"
    defaultSelectedKeys={['/']}
    items={menuItems}
    onClick={({ key }) => {
      navigate(key);
    }}
    style={{ 
      background: '#fff',    // 确保菜单背景为白色
      border: 'none'         // 移除默认边框
    }}
  />
</Sider>
```

## 页面设计规范

### 面包屑导航组件 (Breadcrumb.tsx)

**位置和布局**:
- 位于主内容区域 (Content) 内部，Routes 组件之前
- 在 App.tsx 中的 MainLayout 组件内集成
- 作为页面导航的统一入口，提供路径指引

**样式规范**:
```typescript
// 面包屑容器样式
const breadcrumbContainerStyle = {
  borderBottom: '1px solid #f0f0f0',  // 底部边框分隔线
  marginBottom: '16px'                // 与下方内容保持16px间距
  // 注意：无背景色、无外边距
};

// 面包屑组件样式
const breadcrumbStyle = {
  fontSize: '14px'                    // 标准字体大小
};
```

**功能特性**:
- **动态路径生成**: 根据当前路由自动生成面包屑路径
- **图标支持**: 每个路径节点配备对应图标 (HomeOutlined, SettingOutlined, UserOutlined, SafetyOutlined, KeyOutlined)
- **导航功能**: 点击面包屑项可直接跳转到对应页面
- **路径配置**: 支持多级路径映射和标题自定义

**路由配置映射**:
```typescript
const routeConfig: Record<string, { title: string; icon?: React.ReactNode }> = {
  '/': { title: '首页', icon: <HomeOutlined /> },
  '/system': { title: '系统管理', icon: <SettingOutlined /> },
  '/system/users': { title: '用户管理', icon: <UserOutlined /> },
  '/system/roles': { title: '角色管理', icon: <SafetyOutlined /> },
  '/system/permissions': { title: '权限管理', icon: <KeyOutlined /> },
};
```

**集成方式**:
```typescript
// 在 App.tsx 的 Content 组件内集成
<Content style={{
  background: 'transparent',
  margin: '16px',
  minHeight: 'calc(100vh - 112px)'
}}>
  <Breadcrumb />  {/* 面包屑组件位置 */}
  <Routes>
    {/* 路由配置 */}
  </Routes>
</Content>
```

**交互规范**:
- 当前页面项不可点击，显示为普通文本
- 非当前页面项可点击，具有 pointer 光标样式
- 图标与文字间距为 4px，保持视觉平衡
- 使用 Ant Design Breadcrumb 组件作为基础

### 登录页面 (Login.tsx)

**设计要求**:
- 全屏渐变背景 (linear-gradient(135deg, #667eea 0%, #764ba2 100%))
- 居中白色卡片布局，宽度400px
- 卡片阴影效果: boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
- 表单字段: 用户名、密码、记住密码选项
- 大尺寸表单组件 (size="large")
- 全宽主按钮，加载状态支持
- 测试账号信息展示

**功能要求**:
- 表单验证 (必填字段)
- 模拟登录请求 (1秒延迟)
- 成功/失败消息提示
- 默认测试账号: admin/123456

### 首页 (Home.tsx)

**布局结构**:
1. **欢迎信息卡片**: 问候语 + 当前日期 + 系统状态
2. **数据统计区域**: 4列栅格布局，展示关键指标
3. **功能区域**: 2列布局
   - 左侧: 快捷操作卡片网格
   - 右侧: 最近活动列表
4. **系统状态区域**: 3列布局，展示系统监控信息

**数据统计卡片**:
- 总用户数 (绿色上升箭头)
- 在线用户 (蓝色)
- 系统角色 (紫色)
- 权限数量 (橙色)

**快捷操作**:
- 3x1网格布局的小卡片
- 图标 + 标题 + 描述
- 悬停效果和点击跳转

**最近活动**:
- 列表形式展示用户操作
- 用户头像 + 操作类型标签 + 时间戳
- 操作类型颜色编码 (登录-蓝色, 编辑-橙色, 新增-绿色, 删除-红色)

### 系统管理页面

**路由结构**:
- `/system/users` - 用户管理
- `/system/roles` - 角色管理  
- `/system/permissions` - 权限管理

**通用表格设计规范**:

#### 表格样式要求
- **对齐方式**: 所有列标题和内容必须居中对齐 (`align: 'center'`)
- **列宽规范**:
  - 时间列: 160px
  - 用户列: 180px
  - 状态列: 100px
  - 操作列: 200px
  - 邮箱列: 200px
  - 角色列: 120px

#### 用户信息显示格式
```typescript
render: (text: string, record: User) => (
  <Space size={4} style={{ whiteSpace: 'nowrap' }}>
    <UserOutlined style={{ color: '#1890ff', fontSize: '14px' }} />
    <span style={{ fontWeight: 500 }}>{text}</span>
    <Tag size="small" style={{ margin: 0, fontSize: '11px', padding: '0 4px' }}>
      {record.userId}
    </Tag>
  </Space>
)
```

#### 状态标签规范
```typescript
const getStatusTag = (status: string) => {
  const statusMap = {
    'active': { color: 'success', text: '启用' },
    'inactive': { color: 'error', text: '禁用' }
  };
  const config = statusMap[status] || { color: 'default', text: '未知' };
  return <Tag color={config.color}>{config.text}</Tag>;
};
```

#### 操作按钮规范
```typescript
render: (_: any, record: User) => (
  <Space size={8}>
    <Button type="link" icon={<EyeOutlined />} onClick={() => handleViewDetail(record)} size="small">
      详情
    </Button>
    <Button type="link" icon={<EditOutlined />} onClick={() => handleEdit(record)} size="small">
      编辑
    </Button>
    <Button type="link" danger icon={<DeleteOutlined />} onClick={() => handleDelete(record)} size="small">
      删除
    </Button>
  </Space>
)
```

#### 表格功能要求
- 时间列支持排序 (`sorter: true`)
- 搜索筛选功能
- 分页组件配置:
  ```typescript
  pagination={{
    showSizeChanger: true,
    showQuickJumper: true,
    showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条/共 ${total} 条`
  }}
  ```
- 响应式横向滚动 (`scroll={{ x: 'max-content' }}`)

### 用户管理页面具体要求

**数据结构**:
```typescript
interface User {
  id: string;
  userId: string;        // 用户ID (U001格式)
  userName: string;      // 用户名
  email: string;         // 邮箱
  role: string;          // 角色
  status: 'active' | 'inactive';  // 状态
  createTime: string;    // 创建时间
  lastLogin: string;     // 最后登录
}
```

**功能要求**:
- 用户列表展示 (表格形式)
- 新增用户 (模态框表单)
- 编辑用户 (模态框表单)
- 删除用户 (确认对话框)
- 查看用户详情 (信息模态框)
- 搜索筛选功能

**模拟数据**:
```typescript
const mockUsers = [
  {
    id: '1',
    userId: 'U001',
    userName: '张三',
    email: 'zhangsan@example.com',
    role: '管理员',
    status: 'active',
    createTime: '2024-01-15 10:30:00',
    lastLogin: '2024-07-30 09:15:00'
  },
  // ... 更多用户数据
];
```

### 角色管理页面要求

**数据结构**:
```typescript
interface Role {
  id: string;
  roleName: string;      // 角色名称
  roleCode: string;      // 角色代码
  description: string;   // 角色描述
  userCount: number;     // 用户数量
  permissions: string[]; // 权限列表
  status: 'active' | 'inactive';
  createTime: string;
}
```

**功能特性**:
- 角色列表管理
- 权限分配 (多选框)
- 角色用户关联显示
- CRUD操作完整支持

### 权限管理页面要求

**数据结构**:
```typescript
interface Permission {
  id: string;
  permissionName: string;  // 权限名称
  permissionCode: string;  // 权限代码
  permissionType: 'menu' | 'button' | 'api';  // 权限类型
  parentId: string | null; // 父级权限
  description: string;     // 权限描述
  status: 'active' | 'inactive';
  createTime: string;
}
```

**功能特性**:
- 树形权限结构展示
- 权限类型标签区分
- 父子权限关联管理
- 权限代码唯一性验证

## 样式和主题规范

### 颜色系统
- **主色调**: #1890ff (Ant Design蓝)
- **成功色**: #52c41a (绿色)
- **警告色**: #faad14 (黄色)
- **错误色**: #ff4d4f (红色)
- **文字色**: #262626 (主要文字), #8c8c8c (次要文字)
- **背景色**: #f0f2f5 (页面背景), #ffffff (卡片背景)
- **侧边栏**: #ffffff (白色背景), #f0f2f5 (Logo区域背景), #1890ff (Logo文字颜色)
- **菜单**: #ffffff (菜单背景), #262626 (菜单文字), #1890ff (选中状态)

### 间距规范
- **主内容区外边距**: 16px (App.tsx Content组件的margin)
- **页面容器内边距**: 0px (所有页面不设置padding，依靠模块间距控制)
- **模块间距**: 16px (Card组件的marginBottom)
- **卡片内边距**: 24px (Card组件默认内间距)
- **组件间距**: 16px (垂直), 8px (水平)
- **表格行高**: 默认 (Ant Design标准)

**重要说明**:
- 主内容区通过 `margin: '16px'` 与标题栏、导航栏、屏幕边缘保持距离
- 页面级容器不使用 `padding`，布局完全依靠模块的 `margin` 控制
- 这种设计确保了模块化布局的灵活性和视觉一致性

### 字体规范
- **标题**: 24px (h1), 20px (h2), 16px (h3)
- **正文**: 14px
- **辅助文字**: 12px
- **字重**: 500 (中等), 400 (常规)

### 圆角和阴影
- **卡片圆角**: 8px
- **按钮圆角**: 6px (Ant Design默认)
- **卡片阴影**: 0 1px 4px rgba(0,21,41,.08)
- **登录卡片阴影**: 0 4px 12px rgba(0, 0, 0, 0.15)

## 交互和动效要求

### 按钮交互
- 主按钮: 蓝色背景，白色文字
- 次要按钮: 白色背景，蓝色边框
- 危险按钮: 红色文字，悬停时红色背景
- 链接按钮: 蓝色文字，无背景

### 表格交互
- 行悬停效果 (Ant Design默认)
- 排序图标显示
- 分页器完整功能
- 加载状态支持

### 模态框交互
- 遮罩层点击关闭
- ESC键关闭支持
- 表单验证实时反馈
- 提交按钮加载状态

### 消息提示
- 使用 Ant Design message 组件
- 成功: 绿色图标，2秒自动关闭
- 错误: 红色图标，3秒自动关闭
- 警告: 黄色图标，2秒自动关闭

## 数据管理规范

### 状态管理
- 使用 Zustand 进行全局状态管理
- 页面级状态使用 React useState
- 表单状态使用 Ant Design Form

### 数据模拟
- 所有页面使用本地模拟数据
- 模拟异步请求 (setTimeout 1秒延迟)
- 数据操作本地更新，无后端依赖

### 表单验证
- 必填字段验证
- 邮箱格式验证
- 用户名长度限制 (2-20字符)
- 密码强度要求 (6-20字符)

## 响应式设计要求

### 断点设置
- 桌面端: ≥1200px (主要适配)
- 平板端: 768px-1199px (基本适配)
- 移动端: <768px (侧边栏自动收缩)

### 适配策略
- 侧边栏在小屏幕自动折叠
- 表格支持横向滚动
- 栅格布局响应式调整
- 卡片在小屏幕堆叠显示

## 性能优化要求

### 代码分割
- 页面级组件懒加载 (可选)
- 第三方库按需引入
- 图标库按需导入

### 渲染优化
- 表格数据使用 React.memo 优化
- 避免不必要的重新渲染
- 合理使用 useCallback 和 useMemo

## 开发和构建要求

### 开发环境
- 热重载支持
- TypeScript 严格模式
- ESLint 代码检查
- 开发服务器端口: 5173

### 构建配置
- TypeScript 编译检查
- 生产环境优化
- 静态资源压缩
- 现代浏览器支持

### 代码质量
- TypeScript 类型安全
- ESLint 规则遵循
- 组件单一职责原则
- 代码注释完整性

## 部署要求

### 构建产物
- 静态文件输出到 `dist` 目录
- 资源文件哈希命名
- 支持 CDN 部署

### 环境兼容
- 现代浏览器支持 (Chrome 90+, Firefox 88+, Safari 14+)
- 移动端浏览器基本支持
- 不支持 IE 浏览器

---

## 常见问题和解决方案

### 配置问题解决方案

#### 问题1: babel-plugin-react-dev-locator 依赖错误
**错误信息**: `Cannot find package 'babel-plugin-react-dev-locator'`

**原因**: vite.config.ts 中配置了不存在的 babel 插件

**解决方案**: 
```typescript
// ❌ 错误配置 - 会导致依赖错误
export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: ['react-dev-locator'],  // 这个插件不存在
      },
    }),
    tsconfigPaths()
  ],
})

// ✅ 正确配置 - 使用默认配置
export default defineConfig({
  plugins: [
    react(),  // 使用默认配置，避免依赖问题
    tsconfigPaths()
  ],
})
```

#### 问题2: PostCSS 配置语法错误
**错误信息**: `Failed to load PostCSS config: [SyntaxError] Invalid or unexpected token`

**原因**: postcss.config.js 文件内容错误，使用了 CSS 语法而不是 JavaScript 配置

**解决方案**:
```javascript
// ❌ 错误配置 - CSS 语法在 JS 文件中
@tailwind base;
@tailwind components;
@tailwind utilities;

// ✅ 正确配置 - JavaScript 配置对象
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

**注意**: Tailwind CSS 的指令应该写在 `src/index.css` 文件中，而不是 `postcss.config.js` 文件中。

#### 问题3: CSS 文件正确配置
**src/index.css 正确内容**:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#root {
  height: 100vh;
}
```

### 运行时问题解决方案

#### 问题4: 登录成功但无法进入系统
**错误现象**: 点击登录按钮提示登录成功，但页面没有跳转到系统内部

**原因**: Login组件和App组件中的localStorage键名不一致

**解决方案**:
```typescript
// ❌ 错误配置 - Login.tsx 和 App.tsx 使用不同的键名
// Login.tsx 中
localStorage.setItem('isLoggedIn', 'true')  // 使用 'isLoggedIn'

// App.tsx 中的 useAuth
const [isAuthenticated, setIsAuthenticated] = useState(() => {
  return localStorage.getItem('isAuthenticated') === 'true'  // 检查 'isAuthenticated'
})

// ✅ 正确配置 - 统一使用相同的键名
// Login.tsx 中
localStorage.setItem('isAuthenticated', 'true')  // 统一使用 'isAuthenticated'

// App.tsx 中的 useAuth
const [isAuthenticated, setIsAuthenticated] = useState(() => {
  return localStorage.getItem('isAuthenticated') === 'true'  // 检查 'isAuthenticated'
})
```

**重要提醒**: 确保整个应用中的认证状态管理使用统一的localStorage键名 `'isAuthenticated'`

#### 问题5: TypeScript 类型错误 - 权限管理树形数据
**错误信息**: `类型"Permission"不能分配给类型"Permission & { children: Permission[]; }"`

**原因**: buildTreeData 函数中的类型定义过于复杂，导致类型推断错误

**解决方案**:
```typescript
// ❌ 错误实现 - 复杂的类型断言和映射
const buildTreeData = (permissions: Permission[]): DataNode[] => {
  const convertToTreeNode = (node: Permission & { children: Permission[] }): DataNode => ({
    title: node.name,
    key: node.id,
    children: node.children?.map(convertToTreeNode)
  })
  
  const roots = permissions.filter(p => !p.parentId).map(root => ({
    ...root,
    children: permissions.filter(p => p.parentId === root.id)
  })) as (Permission & { children: Permission[] })[]
  
  return roots.map(convertToTreeNode)
}

// ✅ 正确实现 - 简化类型定义，使用递归方式
const buildTreeData = (permissions: Permission[]): DataNode[] => {
  const convertToTreeNode = (node: Permission, children: Permission[] = []): DataNode => ({
    title: node.name,
    key: node.id,
    children: children.length > 0 ? children.map(child => {
      const grandChildren = permissions.filter(p => p.parentId === child.id)
      return convertToTreeNode(child, grandChildren)
    }) : undefined
  })

  const roots = permissions.filter(p => !p.parentId)
  
  return roots.map(root => {
    const children = permissions.filter(p => p.parentId === root.id)
    return convertToTreeNode(root, children)
  })
}
```

**重要提醒**: 在处理复杂的树形数据结构时，避免使用复杂的类型断言，优先使用简单直观的递归实现

### 启动问题排查步骤

1. **检查配置文件**:
   - 确认 `vite.config.ts` 使用默认 react() 配置
   - 确认 `postcss.config.js` 使用正确的 JavaScript 语法
   - 确认 `src/index.css` 包含 Tailwind 指令

2. **重启开发服务器**:
   ```bash
   # 停止当前服务器 (Ctrl+C)
   # 重新启动
   npm run dev
   ```

3. **清理缓存** (如果问题持续):
   ```bash
   # 删除 node_modules 和 package-lock.json
   rm -rf node_modules package-lock.json
   # 重新安装依赖
   npm install
   # 启动服务器
   npm run dev
   ```

### 配置文件检查清单

在创建项目时，请确保以下配置文件内容正确：

- [ ] `vite.config.ts`: 使用 `react()` 默认配置
- [ ] `postcss.config.js`: 使用 JavaScript 对象语法
- [ ] `src/index.css`: 包含 Tailwind CSS 指令
- [ ] `tailwind.config.js`: 正确的内容路径配置
- [ ] `tsconfig.json`: 正确的路径别名配置

---

## 执行指令

请严格按照以上规范创建一个完整的React B端管理系统，确保:

1. ✅ 所有技术栈版本严格匹配
2. ✅ 项目结构完全一致
3. ✅ 页面布局和样式规范完全遵循
4. ✅ 表格样式严格按照规范实现
5. ✅ 所有功能模块完整实现
6. ✅ 交互效果和用户体验一致
7. ✅ 响应式设计完整支持
8. ✅ 代码质量和性能优化到位
9. ✅ **间距和布局最新规范严格执行**
10. ✅ **配置文件正确性检查完成**

**重要提醒**: 
- 表格的所有列都设置 `align: 'center'`，列宽度严格按照规范设置
- 用户信息显示格式、状态标签样式、操作按钮布局完全按照示例代码实现
- **关键布局要求**：
  - App.tsx 中 Content 组件必须设置 `margin: '16px'`
  - 所有页面容器（Home.tsx、UserManagement.tsx等）不得设置 `padding`
  - 页面布局完全依靠模块间 `margin` 和 Card 组件内部间距控制
  - 同行模块必须使用 flexbox 实现高度对齐
- **配置文件要求**：
  - 严格按照"常见问题和解决方案"部分的正确配置创建文件
  - 避免 babel 插件依赖问题和 PostCSS 语法错误