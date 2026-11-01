---
name: ruoyi-plus-dev
description: RuoYi-Vue-Plus 6.X 后端（SpringBoot3/MyBatis-Plus/Sa-Token）与 plus-ui 前端（Vue3/TS/ElementPlus）及数据库 SQL 的核心开发技能。当任务涉及编写或修改 Java 后端代码（Entity/BO/VO/Mapper/Service/Controller）、Vue3 前端页面与 API、设计数据库表结构（含 JSON 扩展字段）、配置数据字典（sys_dict）或系统参数（sys_config）时，必须加载并严格遵循本技能。
---

# RuoYi-Vue-Plus 6.X 标准开发技能

适用本仓库 RuoYi-Vue-Plus 6.X 与 `plus-ui/` Vue 工程。业务规则由使用项目确定，技术用法以当前源码为准。

## 一、 强制执行工作流 (Standard Operating Procedure)

接收开发或修改任务时，**必须严格按以下 4 步顺序执行，严禁跳步直接生成代码**：

1. **Step 1：探查底座与参考模板（先读后写）**
   - 检查需求中的枚举、配置项、基础实体是否可复用框架现有的字典（`sys_dict_*`）、系统参数（`sys_config`）、用户/部门/文件表。
   - 修改现有模块前，先读取目标模块的 Controller/Service/Mapper 及调用点；新增标准 CRUD 前，先按【代码与模板入口】读取 `ruoyi-demo` 或 `fm/` 模板。
2. **Step 2：数据表与领域模型对齐**
   - 核对 DDL 与 Entity/BO/VO 字段。主干查询字段落列，可变低频扩展详情使用 JSON 字段并配置同构类型与 `JacksonTypeHandler`。
   - 区分审计字段（`create_by/create_dept`）与实际业务归属字段。
3. **Step 3：按规范编写前后端与 SQL 代码**
   - 严格遵循【开发约定】与【CRUD 通用编码规范】，只实现当前任务所需接口与交互，不机械生成全套无用 CRUD。
4. **Step 4：编译生成与红线自检（交付门禁）**
   - **必须执行编译**：新增或修改 Entity/BO/VO 映射字段后，必须触发 Maven 编译（如 `mvn test-compile`）让 MapStruct 生成实现类，确认无编译错误。
   - 对照文末【交付前自检清单】逐项核销后再输出结果。

---

## 二、 开发约定与防幻觉红线

- 按已确认需求做最小充分改动；优先复用、配置、局部适配，确认底座存在缺口后才新增。
- 调用前读取相关接口、实现及必要调用点，不臆造类、方法、字段或配置，不重复封装已有公共能力。
- **严禁混入原版 RuoYi 语法（绝对禁用 `SecurityUtils`、`@PreAuthorize`、`AjaxResult`、`TableDataInfo`、`BeanUtils.copyProperties`）。**
- 新标准 CRUD 参考实际生成器模板；修改已有功能保留其契约、权限、校验、事务与交互。
- 只实现所需操作，不机械生成全套 CRUD，不为假想需求新增中间件、框架或抽象。
- 范围、执行权限和交付遵循 `AGENTS.md`。

---

## 三、 功能模块目录

`<module>`、`<business>`、`Xxx` 为占位符，按已有模块边界归类，不为每个功能创建 Maven 子模块。

```text
ruoyi-admin/                          # 启动、应用依赖与环境配置
ruoyi-modules/ruoyi-<module>/
├─ pom.xml
└─ src/main/
   ├─ java/org/dromara/<module>/
   │  ├─ controller/XxxController.java
   │  ├─ domain/Xxx.java
   │  ├─ domain/bo/XxxBo.java
   │  ├─ domain/vo/XxxVo.java
   │  ├─ mapper/XxxMapper.java
   │  ├─ service/IXxxService.java
   │  └─ service/impl/XxxServiceImpl.java
   └─ resources/mapper/<module>/XxxMapper.xml  # 按需
ruoyi-api/src/main/java/               # 跨模块接口与 DTO
ruoyi-common/                         # 后端通用能力
ruoyi-extend/                         # 独立扩展服务
plus-ui/src/
├─ api/<module>/<business>/{index.ts,types.ts}
├─ views/<module>/<business>/index.vue
├─ components/                        # 公共组件
├─ hooks/                             # 交互与状态复用
└─ utils/                             # 公共工具
script/sql/                           # 按数据库提供配套脚本
```

新增模块核对父 POM 聚合、依赖管理和主应用依赖；新增页面按需接入菜单、组件路径及按钮权限。

---

## 四、 CRUD 通用编码规范

### 后端

- **对象职责与转换**：Entity、BO、VO 分工为持久化字段、请求/查询与校验、展示/翻译/导出；不直接对外暴露 Entity。沿用模块的 `BaseEntity`、`@TableName/@TableId`、`@AutoMapper` 和校验分组（`AddGroup/EditGroup`）；BO 转换统一复用 `MapstructUtils`，**修改映射字段后须经编译触发注解处理器生成代码**。
- **JSON 字段映射**：若映射为对象或 Map/集合，Entity 须开启 `@TableName(value = "...", autoResultMap = true)` 且字段标注 `@TableField(typeHandler = JacksonTypeHandler.class)`，Entity/BO/VO 字段类型保持同构以兼容 `@AutoMapper`；若定义为 `String` 则前后端统一按 JSON 字符串或手动序列化处理。
- **Mapper 层**：优先 `BaseMapperPlus<Entity, Vo>`；查询沿用现有 Wrapper/QueryBuilder/MPJ，复杂 SQL 按需使用 XML，数据权限列与 SQL 别名一致。**批量写入优先使用 `baseMapper.insertBatch`，允许清空的字段更新时须通过 `LambdaUpdateWrapper.set(Xxx::getField, null)` 显式置空。**
- **Service 层**：承载业务校验和编排，**不直接返回 `R<T>`，业务阻断统一抛出 `ServiceException`**；保留保存/删除校验、原子写入事务和缓存失效。列表关联数据优先批量读取（配合 `StreamUtils`）**或复用 `@Translation`**，空 ID 集合不得退化为全表查询，分页在数据库完成。
- **上下文与后台任务**：获取当前登录人/部门统一使用 `LoginHelper`；集合与字符串优先复用 `StreamUtils`、`StringUtils` 及 Hutool 工具。**定时任务、异步线程或外部回调等无登录态场景，不得强依赖 `LoginHelper`**，需显式赋值审计/归属字段并按需使用 `DataPermissionHelper.ignore` 绕过数据权限。
- **Controller 层**：沿用 `BaseController`、`@Validated`、`@SaCheckPermission`、`@Log`，按需防重（`@RepeatSubmit`）；权限标识与前端、菜单一致。普通响应 `R<T>`；**分页入参分离接收 `XxxBo` 与 `PageQuery`**，分页 Service 返回 `PageResult<Vo>`，Controller 返回 `R<PageResult<Vo>>`；树表通常返回 `R<List<Vo>>`。文件流直接写响应。
- **跨模块调用**：路由沿用目标模块契约，新标准接口参考模板。跨模块调用优先 `ruoyi-api` 的接口与 DTO，不直接依赖其他模块实现类。
- **字典与系统参数**：枚举选项复用 `sys_dict_*`，保存 `dict_value`，前后端类型一致，状态转换仍在服务层校验；**全局阈值、开关、同步周期、运行策略等键值配置复用 `sys_config`（后端通过 `ConfigService` 读取，前端通过参数接口读取），提供配套初始化 SQL，严禁单独建配置表或将可变业务参数硬编码到 yml。**
- **导入导出与日志**：复用 `ExcelBuilder` 与当前 Fesod 注解；范围与数据权限和查询一致。操作日志不记录密码、令牌或密钥。
- **注释与格式**：公共 API、Entity/BO/VO 字段和业务方法使用简洁 JavaDoc；格式、命名与注解顺序遵循 `.editorconfig` 和所在模块。

### Vue 前端

- 使用 Vue 3、TypeScript、Element Plus 与 `<script setup name="Xxx" lang="ts">`（**组件 `name` 与菜单路由 `name` 保持一致以支持缓存**）；API、types、页面分别维护。
- 请求使用 `@/utils/request`；`AxiosPromise` 从 `@/utils/api-types` 引入，`PageResult` 从 `@/api/types` 引入。分页读取 `res.data.rows/total`，树表读取 `res.data` 数组。
- VO/Form/Query 按接口职责定义，**雪花 ID 字段使用 `string | number` 防止精度丢失**，字典、状态和日期类型与后端一致；查询走 `params`，请求体走 `data`，下载复用请求工具。
- 表单、查询、日期、选择和弹窗优先复用已有 hooks；`openDialog` 会重置表单，编辑回填后使用 `showDialog`。失败保留输入并恢复加载状态，状态开关失败时回滚。
- 字典使用 `useDict/DictTag`；按钮使用所在页面的权限指令（`v-hasPermi`）或 `checkPermi`；已有复杂页面保留树筛选、导入导出、列显隐、抽屉及授权交互。
- 组件与样式优先复用现有实现，单页需求不修改全局样式；包管理和格式化工具遵循 `package.json` 与锁文件。

---

## 五、 业务数据表设计规范

- **先复用组织、账号、角色、字典（`sys_dict_*`）、系统参数（`sys_config`）、文件（`sys_oss`）等框架基础表**，按明确语义引用其 ID 或编码，不另建同义体系或冗余配置表。
- 表与列使用小写下划线，Entity 与 DDL 对齐；主键、业务唯一性、引用、可空性、默认值与实际查询索引按需求确定。
- 继承 `BaseEntity` 时对齐五个审计字段：`create_dept/create_by/update_by` 对应 `Long`，`create_time/update_time` 对应 `LocalDateTime`；创建信息不充当业务归属或外部事件时间。
- 主键不由基类提供；`@TableId` 策略与数据库一致。全局 `ASSIGN_ID` 与显式 `AUTO` 按目标表选用，前端传输保留 ID 精度。
- `status/del_flag/version/remark/tenant_id` 均按需添加，不视为基类自带；逻辑删除、版本锁与租户字段须配套相应机制。
- 身份、状态、权限、唯一键和常用查询字段落列；可变低频详情按需使用 JSON，类型与查询语法按目标数据库选择。独立生命周期、权限或约束需要独立建模时再拆表。
- 业务归属字段与 `create_dept/create_by` 分开；数据范围接入实际业务字段，覆盖相关查询、导出与写操作。
- 明确删除及历史保留规则、并发更新条件和冲突处理；不只依赖应用先查后写保证唯一性。核对 `NOT_NULL` 更新策略，允许清空字段时显式处理。
- 审计自动填充、DDL 默认值和自定义 SQL 分别核对；时间类型、时区、字典值与前后端契约一致。
- 表结构、字典、**系统参数**和菜单变更提供目标数据库脚本，**XML 与脚本避免绑定单一数据库专属语法或反引号**，执行权限遵循 `AGENTS.md`。
  入口：[BaseEntity](ruoyi-common/ruoyi-common-mybatis/src/main/java/org/dromara/common/mybatis/core/domain/BaseEntity.java) · [自动填充](ruoyi-common/ruoyi-common-mybatis/src/main/java/org/dromara/common/mybatis/handler/InjectionMetaObjectHandler.java) · [MyBatis 配置](ruoyi-common/ruoyi-common-mybatis/src/main/resources/common-mybatis.yml) · [初始化脚本](script/sql/)。

---

## 六、 代码模板与复用能力入口

### 1. 代码与模板入口
生成器实际加载 classpath 下的 `fm/`；`plus-ui/gen/` 为前端参考模板。可直接参考模板写代码，无需先运行生成器：

| 用途                      | 入口                                                         |
| ------------------------- | ------------------------------------------------------------ |
| Java 分层                 | `ruoyi-modules/ruoyi-gen/src/main/resources/fm/java/`        |
| Vue API、类型、列表与树表 | `ruoyi-modules/ruoyi-gen/src/main/resources/fm/vue/`         |
| Mapper XML                | `ruoyi-modules/ruoyi-gen/src/main/resources/fm/xml/`         |
| 数据库配套脚本            | `ruoyi-modules/ruoyi-gen/src/main/resources/fm/sql/`         |
| 模板选择与输出路径        | `ruoyi-modules/ruoyi-gen/src/main/java/org/dromara/gen/util/TemplateEngineUtils.java` |
| 标准后端示例              | `ruoyi-modules/ruoyi-demo/src/main/`                         |
| 标准 Vue 页面与 API       | `plus-ui/src/views/demo/`、`plus-ui/src/api/demo/`           |

### 2. 按需复用能力入口
按需求在以下目录查找实际实现，读取后复用；不因目录存在而默认接入对应模块或依赖：

| 查找范围                                     | 入口                                                         |
| -------------------------------------------- | ------------------------------------------------------------ |
| 后端通用能力                                 | `ruoyi-common/`                                              |
| 跨模块接口与 DTO                             | `ruoyi-api/src/main/java/`                                   |
| 用户、组织、权限、字典、参数、文件等系统功能 | `ruoyi-modules/ruoyi-system/src/main/`、`plus-ui/src/views/system/` |
| 工作流                                       | `ruoyi-modules/ruoyi-workflow/`                              |
| 定时任务                                     | `ruoyi-modules/ruoyi-job/`                                   |
| 其他功能模块及示例                           | `ruoyi-modules/`                                             |
| 独立扩展服务                                 | `ruoyi-extend/`                                              |
| 前端组件、hooks、工具及公共样式              | `plus-ui/src/components/`、`plus-ui/src/hooks/`、`plus-ui/src/utils/`、`plus-ui/src/assets/styles/` |

---

## 七、 交付前自检清单 (Delivery Checklist)

输出代码或提交任务前，必须逐项核对以下 6 条红线：
- [ ] **零原版幻觉**：代码中无 `SecurityUtils`、`@PreAuthorize`、`AjaxResult`、`TableDataInfo`、`BeanUtils.copyProperties`。
- [ ] **配置与字典复用**：业务配置项已走 `sys_config`（未乱建配置表），枚举已走 `sys_dict_*`，并附带了配套 SQL。
- [ ] **JSON 与转换编译**：JSON 对象字段已配 `autoResultMap = true` 与 `JacksonTypeHandler`，且修改 Entity/BO/VO 后已执行编译生成 MapStruct 代码。
- [ ] **分页与返回值契约**：Controller 分页入参已拆分为 `(XxxBo bo, PageQuery pageQuery)`，Service 未直接返回 `R<T>`。
- [ ] **无登录态安全**：定时任务/外部数据同步逻辑未强依赖 `LoginHelper.getUserId()`，必要时已加 `DataPermissionHelper.ignore`。
- [ ] **前端精度与缓存**：TS 类型中主键/关联 ID 已定义为 `string | number`，Vue 组件 `name` 与菜单路由 `name` 一致。