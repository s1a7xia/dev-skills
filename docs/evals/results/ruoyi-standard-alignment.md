# 若依编码规范集成对齐记录

核对日期：2026-10-31。来源为用户提供的桌面 `ry-coding.md`，不是合并方案里的缩写版。

## 原文完整性

- 原文大小：14,466 字节，154 行。
- 原文 SHA-256：`840b21d8a8b05cc139e5bdd4ac7ce877ed2a95deee3c01f5557c5ead68a1f74a`。
- 技能内的 [references/ry-coding.md](../../../skills/ruoyi-plus-dev/references/ry-coding.md) 直接保留原始字节，已与来源文件比较一致。
- [SKILL.md](../../../skills/ruoyi-plus-dev/SKILL.md) 要求加载完整原文；[REFERENCE.md](../../../skills/ruoyi-plus-dev/REFERENCE.md) 维护章节导航和流程衔接，不再维护另一份翻译规则清单。

## 七个章节的衔接

| 原文章节 | 集成位置与执行要求 |
|---|---|
| 一、强制执行工作流 | 开发和修改保留“探查复用与模板 → 对齐表与模型 → 编码 → 编译和自检”的四步顺序；嵌入现有 implement / tdd / debug 流程。 |
| 二、开发约定与防幻觉红线 | 五项原版 RuoYi API 禁令、先查接口和实现、保留既有契约、最小改动及 AGENTS.md 执行边界均保留。 |
| 三、功能模块目录 | 原目录树完整保留，包括接口与实现分层、XML、API/types/view、SQL；新增模块的 POM 与依赖检查、新页面的菜单/组件/权限接入均保留。 |
| 四、CRUD 通用编码规范 | 后端和前端规则原样读取：Entity/BO/VO、JSON 同构、MapStruct 编译、批量和置空更新、Service/Controller 分工、分页、后台身份、字典参数、导出日志、前端类型/hooks/权限及失败交互。 |
| 五、业务数据表设计规范 | 五个审计字段和类型、独立主键、按需机制字段、物理列/JSON、业务归属、唯一性/并发/历史、NOT_NULL、时间时区、数据库适配与脚本权限均保留。 |
| 六、代码模板与复用能力入口 | classpath `fm/`、`plus-ui/gen/`、全部模板与复用路径原样保留；按需读取，不因存在目录而接入依赖。 |
| 七、交付前自检清单 | 六条原始自检全部保留；交付前按适用性记录通过/失败/不适用及实际证据。 |

共享入口读取项目的 `docs/agents/coding-standards.md`，据此加载技术规范。TDD 与三视角审查的子代理独立重新读取；think / grill 使用规范约束方案，story 将已确认契约写入现有任务。`store` 按 `story` 的拼写错误处理，没有新增或替换工作流技能。

## 核对中修正的压缩问题

最初的英文整理版压缩了四步顺序、classpath 模板语义、部分目录和新页面接入要求。现改为完整原文随技能分发，英文只保留衔接说明，消除摘要遗漏和双份规则漂移。

补充说明独立列在 REFERENCE 中：`string | number` 不会恢复已经丢失的 JSON 数字精度；后台任务按原文“按需”判断权限处理；编译命令从业务项目实际构建配置选择。这些说明没有删改原文规则。

## 验证边界

字节一致性证明原文内容完整保留；安装副本校验用于确认它随技能分发。当前未提供目标若依业务源码，因此不能据此宣称业务项目已编译或框架 API 已联调通过。

## 2026-11-01：工具复用执行要求补全

用户反馈：开发时绕过项目已封装的工具类，另写同类逻辑。本次只读检查了用户指定若依项目的 `ruoyi-common/ruoyi-common-core/src/main/java/org/dromara/common/core/`，以及系统模块中的代表性调用点。

原规范已有“优先复用”和宽泛的 `ruoyi-common/` 入口，但没有明确要求检索 `common-core/utils/` 及子包、核对方法语义、说明新增实现的缺口；原六项交付自检也没有单独核对工具复用。这是文档中可以确认的执行缺口，不能据此还原此前 agent 未复用的全部运行原因。

补充集中在 [REFERENCE.md 的 Repository Reuse Check](../../../skills/ruoyi-plus-dev/REFERENCE.md#repository-reuse-check)，由技能入口在编码前及完成条件中引用：检索能力 → 读取实现与调用点 → 核对语义和依赖 → 复用或说明缺口 → 检查最终新增逻辑并提交复用证据。检查包含业务方法内联的循环、流处理和递归，也覆盖项目自定义能力与前端公共实现。原始 `references/ry-coding.md` 本次保持不变；该补充是对原文 Step 1 和第六章的执行细化，不是替换团队标准。

### 源码核对案例

以下为本次人工读取源码后的候选能力核对，不是独立模型行为测试，也没有执行或修改若依业务代码。

| 场景 | 已读源码依据 | 补充规则要求的判断 |
|---|---|---|
| 从列表提取字段或生成 Map | `utils/StreamUtils.java` 的 `toList`、`toSet`、`toMap`、`toIdentityMap`；`SysDeptMapper` 的现有调用 | 语义满足时直接调用；不能另写同义工具方法或内联通用转换来绕过检查。 |
| 多根树和树路径映射 | `utils/TreeBuildUtils.java` 的 `buildMultiRoot`、`buildTreeNodeMap`；`SysDeptServiceImpl`、`DeptExcelOptions` 的调用 | 先核对已有树方法和调用方式，再判断是否存在未覆盖的遍历需求。 |
| 字符串或日期的继承能力 | `StringUtils` 继承 Apache Commons 的 `StringUtils`，`DateUtils` 继承 Hutool 的 `DateUtil` | 只搜索本类声明会漏掉继承方法；应继续检查相关父类能力和项目封装。 |
| 重复键要求与现有方法不同 | `StreamUtils.toMap` / `toIdentityMap` 使用保留首值的合并函数 | 如果需求是求和或拒绝重复键，须记录具体语义差异，再选择合适实现；不能为复用而改变业务契约。 |
| 项目专属校验或业务编排 | 原规范 Service 层职责，以及工具方法的实际能力边界 | 通用步骤复用工具，业务校验和编排留在所属 Service；复用规则不要求把全部业务逻辑搬入工具类。 |

### 验证

- `python scripts/check-docs.py`：全部文档检查通过。
- `python .../skill-creator/scripts/quick_validate.py skills/ruoyi-plus-dev`：`Skill is valid!`。
- [iteration-060.json](iteration-060.json)：静态硬检查 232/232、静态软检查 79/79、工作流检查 39/39；触发代理训练集 45.5%、保留集 64.3%，与第 59 轮一致，17 项既有触发软失败未变化。本次未修改 description 或路由。
- 没有执行目标若依项目编译、独立模型业务任务回放或更新已安装技能副本；后续真实业务任务仍需核对工具调用及复用证据。
