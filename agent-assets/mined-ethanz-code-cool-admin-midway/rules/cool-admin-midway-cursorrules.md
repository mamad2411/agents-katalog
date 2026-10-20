# 项目背景
- 数据库：MySQL、Sqlite、Postgres、Typeorm（0.3.20版本， 不使用外键方式，如@ManyToOne、@OneToMany等）
- 语言：TypeScript、JavaScript、CommonJS
- 框架：Koa.js、midway.js、cool-admin-midway
- 项目版本：8.x

# 目录
项目目录：
 ├── .vscode(代码片段，根据关键字可以快速地生成代码)
 ├── public(静态资源文件，如js、css或者上传的文件)
 ├── src
 │   └── comm(通用库)
 │   └── modules(项目模块)
 │   └── config
 │   │    └── config.default.ts(默认配置，不区分环境，都生效)
 │   │    └── config.local.ts(本地开发配置，对应npm run dev)
 │   │    └── config.prod.ts(生产环境配置，对应npm run start)
 │   └── configuration.ts(midway的配置文件)
 │   └── welcome.ts(环境的controller)
 │   └── interface.ts(类型声明)
 ├── package.json(依赖管理，项目信息)
 ├── bootstrap.js(生产环境启动入口文件，可借助pm2等工具多进程启动)
 └── ...

 模块目录
 ├── modules
 │   └── base(基础的权限管理系统)
 │   │    └── controller(api接口)
 │   │    └── dto(参数校验)
 │   │    └── entity(实体类)
 │   │    └── middleware(中间件)
 │   │    └── schedule(定时任务)
 │   │    └── service(服务，写业务逻辑)
 │   │    └── config.ts(必须，模块的配置)
 │   │    └── db.json(可选，初始化该模块的数据)
 │   │    └── menu.json(可选，初始化该模块的菜单)

 # 其它
- 始终使用中文回复，包括代码注释等
- `@midwayjs/decorator`，已弃用，使用`@midwayjs/core`
- 不要使用自定义sql来操作数据库，而是使用typeorm的api，统计相关的可以考虑使用原生sql
- Controller中不允许重写`add`、`delete`、`update`、`info`、`list`、`page`方法
- Controller不需要加@Provide()注解
- page接口关联表查询一般写在Controller的pageQueryOp中，尽量不要使用自定义sql
- Entity字段使用驼峰命名，如：studentNo
- Entity不允许使用@ManyToOne、@OneToMany等外键关系
- Entity的BaseEntity引用固定为：`import { BaseEntity } from '../../base/entity/base';`，禁止修改层级
- 创建api接口时，不要多层级如：`/student/detail`，改为`/studentDetail`，用驼峰法；
- 本项目是版本8.x，所有代码都需要按照新的写法进行编写，如Entity字典的配置
- 文件的命名不要使用驼峰法，而是使用下划线法，如：student_info.entity.ts，另外禁止太啰嗦，比如：student模块下的学生信息，不要写成：student_info， 而是写成info.ts，班级信息：class.ts，不要写成student_class.ts 
- 创建模块代码需要读取.cursor/rules的module.mdc、controller.mdc、service.mdc、db.mdc，其它的rules根据需要进行参考