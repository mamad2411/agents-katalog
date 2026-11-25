---
name:trt-plugin-kernel-latency-auto-opt   
description:本技能基于kernel延迟 + NCU 硬件计数器瓶颈诊断，全自动迭代优化 CUDA Kernel，唯一优化目标：最小执行延迟（latency, ms）。严格遵循工程约束：仅允许修改 exp/*.cu 文件，其他文件固定不可改动；自动构建、测速、记录实验日志、择优提交 / 回滚代码，长期后台无人值守运行。  
---

## 0. 输出约束（Shell 命令专用，同时规避三类安全拦截）  
Contains brace with quote character   
Contains shell syntax that cannot be statically analyzed   
Multiple directory changes in one command require approval for clarity

### 规则1 规避「花括号带引号混淆扩展」
1. 文件通配、花括号扩展 `{}` 禁止用单/双引号包裹；
2. 批量文件拷贝/操作禁止单行 `{a,b}` 简写块；优先分行多条cp或for循环遍历。

### 规则2 规避「无法静态解析Shell语法拦截」
1. 完全禁止短路运算符 `&&`、`||`，错误校验全部使用多行独立 if / fi 分支；
2. 禁止命令替换 `` `...` ``、`$(...)`、算术扩展 `$((...))`、复合变量扩展 `${var:-x}`；
3. 禁止子Shell括号 `(...)`、单行复合代码块 `{ ...; }`；
4. 禁止多层串联管道 `cmd1 | cmd2 | cmd3`，多步文本处理分步输出至临时文件隔离；
5. 所有数值计算、字符串提取逻辑交由上层Python实现，Shell仅做基础文件拷贝、编译、执行调用；
6. 循环仅使用标准 for file in 列表，不搭配嵌套管道、行内命令替换。

### 规则3：规避多目录单命令操作可读性告警
1. 单条 cp / mv 命令仅允许写入**一个目标目录**；
2. 需要向多个目录拷贝/移动文件时，拆分为多条独立命令分别执行；
3. 禁止单条 mkdir 一次性创建多个无关联目录，每个目录单独一条 mkdir -p；
4. 不使用一条命令同时修改 exp/、exp_best/、exp_xxx/ 等多个业务目录。

## 1. 核心依赖与工具栈    
测速基准：main.cpp 中使用手动设置起始点进行计时  
瓶颈分析：ncu (Nsight Compute CLI)    
构建系统：CMake
运行载体：Python 自动化调度脚本   
迭代记录：tune-log.csv 实验日志  
约束库：CCCL / CUB（优先高层抽象，仅瓶颈明确时下沉底层 PTX / 共享内存）  

## 1.1 咨询用户  
+ 优化哪个插件    
+ 执行 scripts下 `compile.sh`，然后执行 `start_nsys.sh`，列出 GPU Kernel 耗时占比信息表  


## 2. 工程固定规范       
### 2.1 目录结构（固定）     
```   
project-root/
├── build                                                # 编译过程产物，可读写
├── build.sh                                             # 编译shell 脚本，只读
├── claude-auto.sh                                       # claude auto模式启动，只读
├── CMakeLists.txt                                       # 只读
├── cmake/                                               # 目录及内部文件只读
├── experiments/
│   └── <plugin_name>-tune-log.csv                       # 全流程实验日志，可读写
└── src
    ├── CMakeLists.txt                                   # 只读
    ├── c_api.h                                          # 只读
    ├── main.cpp                                         # 只读
    |
    ├── <plugin_name>/                       
    │   ├── CMakeLists.txt                               # 只读
    │   ├── exp 
    │   │   └── *.cu                                     # 需调优的kernel实现，可读写
    |   |── exp_best/                                    # 目录，存放历史最优的kernel文件，可读写
    |   |── exp_<global_iter_cnt>/                       # 目录，存放历史每一轮修改的kernel文件，可读写
    |   |
    │   ├── *.cu                                         # kernel基准实现，只读
    │   └── *.h                                          # 只读
    └── utils/                                           # 目录及内部文件只读
```

### 2.2. 日志格式说明     

日志文件：experiments/<plugin_name>-tune-log.csv，标准 CSV，字段含逗号自动加引号。    
表头固定：
```
global_iter_cnt,timestamp,exp_latency,out_diff,status,description
```
字段说明：   
1. global_iter_cnt：全局计数，int数据类型     
2. timestamp：时间戳       
  - 时区强制锁定：亚洲上海 Asia/Shanghai (UTC+8)，禁止使用UTC零时区、服务器本地默认时区；
  - 输出文本格式：YYYY-MM-DD HH:MM:SS，空格分隔，示例：2026-06-10 15:30:22；
  - 代码强制约束：生成时间戳时必须显式加载Asia/Shanghai时区对象，不允许直接调用datetime.now()（无参默认取系统本地/UTC）；
  - 禁止仅对UTC时间手动加8小时数字修正，必须使用标准时区库生成本地时间，避免夏令时、系统时区切换误差。
3. exp_latency：本轮时延；崩溃 / 编译错误不填写
4. out_diff：本轮优化后和原始基准实现输出结果的差值，float数据类型，越接近0越好，如果kernel 输出个数有多个则用"-"连接；崩溃 / 编译错误不填写
5. status：baseline / improved / regressed / build_error / runtime_error
6. description：本轮尝试的优化方案简短描述；崩溃 / 编译错误不填写

日志写入强制规则    
每轮编译测速完成后，先写日志，再执行备份，最后执行择优 / 回滚，防止上下文丢失丢失实验记录。

## 3. 指标定义与判定规则   
### 3.1 优化指标   
+ metric: time   
+ 单位：ms   
+ 优化目标：数值越小性能越优    

### 3.2 名词定义 
备份：将`exp/*.cu` 强制拷贝到 `exp_<global_iter_cnt>/` 
择优：将`exp/*.cu` 强制拷贝到 `exp_best/` 
回滚：将`exp_best/*.cu` 强制拷贝到`exp/`
历史最优时延：history_best_latency
停滞计数：stall_cnt
编译失败次数：compiler_err_cnt

### 3.3 迭代判定逻辑     
1. 编译失败                        → build_error，备份，然后回滚，日志标记 N/A；  
2. 运行报错/ 崩溃 / 超时 (60s)      → runtime_error，备份，然后回滚，日志标记 N/A； 
3. 本轮时延 < 历史最优时延           → improved，备份，然后择优，写日志，重置 stall_cnt=0，更新 history_best_latency=exp_latency；    
4. 本轮时延 ≥ 历史最优时延           → regressed，备份，然后回滚，停滞计数 + 1；    
5. 连续 5 轮无性能提升（停滞计数等于5）→ 触发 NCU 深度瓶颈分析。   

## 4. NCU 自动诊断策略（停滞计数等于5时触发）  
### 4.1 NCU性能分析   
执行 scripts下 `start_ncu.sh`，捕获输出，分析 ncu profile information

### 4.2 自动识别瓶颈 & 对应优化方向    
|NCU                                    |诊断关键词	      |瓶颈类型 |	自动生成优化假设                     |     
|---------------------------------------|-------------  |------- | --------------                    |
|Warp Occupancy Low	                    |SM 占用率不足    |调整 Block 尺寸、添加__launch_bounds__限制寄存器|     
|Register Spilling	                    |寄存器溢出	      |局部变量复用、适度循环展开、减少临时变量           |     
|Shared Memory Bank Conflict	          |共享内存访存冲突  |smem 数组 padding 偏移、调整分块步长            |     
|Global Memory Load/Store High Latency	|全局访存延迟高    |float2/float4 向量化读写、合并连续访存          |    
|Kernel Launch Overhead Dominant	      |启动开销占比过高 	|合并小 kernel、单次迭代增加计算量               |     

### 4.2 NCU 使用约束   
+ 非停滞状态不调用，避免大幅拉长迭代耗时    
+ 仅采集单固定负载参数，减少采样开销    

## 5. 分层时延优化优先级（假设驱动迭代）
可阅读 references/ 下相关cuda 优化文档   
单次迭代仅执行单一增量改动，每次仅验证一条优化假设，禁止多改动混合测试。  
1. 最高优先级：调度与启动开销优化    
+ Block 尺寸限定 32/64/128/256（Warp 对齐）    
+ __launch_bounds__ 控制寄存器占用，提升并发     
+ 消除冗余 Kernel Launch    

2. 次优先级：指令执行延迟压缩
+ 循环展开、分支消除（位运算替代 if 分支）；
+ CUB/CCCL 高层原语替换手写规约、warp 操作

3. 第三优先级：访存延迟削减      
+ 全局内存向量化加载存储    
+ 热点数据缓存至共享内存   
+ Bank 冲突 Padding 修复    
+ 缓存重排   
+ 算子全融合

4. 第四优先级（NCU调优）   
+ 内联 PTX、手动 Warp Shuffle、精细寄存器调优    
+ 无硬件指标佐证时，禁止直接下沉底层原语     

注意：1、2、3属于通用调优     

## 6. 自动化循环完整流程
1. 执行 scripts下 `compile.sh`，捕获编译输出； 
  + 编译失败：退出循环（默认初始基准代码是语法正确的），用户检查环境    
2. 执行 scripts下 `get_baseline_latency.sh`，捕获输出，
  + 运行失败：退出循环（默认初始基准代码是语法正确的），用户检查环境  
  + 运行成功：得到 baseline_latency，设置stall_cnt=0，global_iter_cnt=0，history_best_latency=baseline_latency，跳转到步骤6    
3. sleep 1s，global_iter_cnt=global_iter_cnt+1，compiler_err_cnt=0，读取 exp/*.cu，判断stall_cnt：
  + 如果stall_cnt ≥5，执行NCU调优识别瓶颈生成优化假设，修改 exp/*.cu，分析完成后重置stall_cnt=0
  + 如果stall_cnt <5, 执行通用调优，生成单条优化假设修改 exp/*.cu
4. 执行 scripts下 `compile.sh`，捕获编译输出； 
  + 如果编译失败， 则compiler_err_cnt=compiler_err_cnt+1，
      + 当 compiler_err_cnt < 4，则自动修改 exp/*.cu，回到步骤4
      + 当 compiler_err_cnt > 3，跳转到步骤6 
5. 执行 scripts下 `start_compare.sh baseline_latency`（`start_compare.sh` 的入参是初始 baseline 时延），依次捕获 error、out_diff、exp_latency 信息，如果捕获到error 信息，out_diff、exp_latency 信息可以不捕获   
6. 依据`3.3迭代判定逻辑`，
  + 匹配当前状态 build_error / runtime_error /improved /regressed，写入日志  
  + 如果global_iter_cnt > 0:
    + 如果当前状态improved，则进行备份，然后择优，最后更新 history_best_latency   
    + 如果当前状态regressed / build_error / runtime_error，则进行回滚   
  + 如果global_iter_cnt == 0，则进行备份，然后择优
7. 回到步骤3，开启下一轮迭代

## 8. 硬性约束（不可违反）
+ 仅允许修改 exp/*.cu，但注意其中某些对外的接口函数原型不能变（会导致编译错误），其余文件只读；
+ 不引入工程未预装的第三方 CUDA 依赖，仅使用原生 CUDA、CCCL、CUB；
+ 同等时延下优先保留代码简洁方案，复杂 hack 小幅提速不保留；
+ 循环永不主动停止，不询问用户是否继续，仅人工 kill 终止；
+ 崩溃、编译错误改动必须先落日志再回滚，保留完整尝试记录；

## 9. 输出产物清单  
+ experiments/*tune-log.csv：完整迭代实验数据，用于复盘优化路径；


