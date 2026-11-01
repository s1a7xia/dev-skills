# RuoYi-Vue-Plus Profile Integration

## Authoritative Team Standard

Read [the complete supplied ry-coding standard](references/ry-coding.md) before affected design, implementation or review. It is preserved verbatim, including its directory tree, API names, template paths, four-step development procedure and six delivery checks. This reference is an integration guide, not a condensed replacement for that standard.

All source paths and code links inside the standard refer to the **target RuoYi project root**, not this skill's directory. Inspect the target checkout to verify those paths and APIs. The source itself establishes that business rules belong to the project and technical usage follows its current source. Resolve a version mismatch explicitly instead of fabricating an API or silently dropping a requirement.

## Reading Map

The original Chinese section titles are retained so agents can find each section exactly.

| Original section | Read for | Integrated responsibility |
|---|---|---|
| 一、强制执行工作流 | All development/modification work | Preserve the original order: inspect reuse/templates → align DDL and models → code the required operations → compile mappings and complete delivery checks. |
| 二、开发约定与防幻觉红线 | Every affected stage | Enforce the named API prohibitions, minimal sufficient changes, source inspection, contract preservation and project AGENTS.md execution boundaries. |
| 三、功能模块目录 | New or modified modules/pages | Use the complete directory tree; check Maven aggregation/dependency management/application dependencies and page menu/component/button-permission integration. |
| 四、CRUD 通用编码规范 | Backend / frontend work and review | Read the relevant backend and Vue sections in full, including JSON type consistency, explicit nullable updates, pagination/return types, hooks, permissions, imports/exports and error states. |
| 五、业务数据表设计规范 | Data modeling, SQL, ownership, concurrency | Check all schema rules, audit and business ownership distinctions, primary-key strategy, optional mechanism fields, uniqueness, null handling, database compatibility and script execution boundaries. |
| 六、代码模板与复用能力入口 | Before choosing a template or shared capability | Follow every applicable path in the source tables, including the generator's classpath `fm/`, `plus-ui/gen/`, other modules and system/common capabilities. A directory's presence does not authorize adding a dependency. |
| 七、交付前自检清单 | Before delivering code or completing a code task | Apply all six original checks; record pass/fail/not applicable with evidence. A mapping-field change requires actual Maven compilation, not only a claimed check. |

## Repository Reuse Check

Operationalize the original Step 1 and section 六 before writing common operations in business code or adding a utility, helper, service wrapper, or frontend hook. Perform the same check when reviewing such additions. This check supplements the original six delivery checks; it does not replace them.

1. **Discover candidates before coding.** Use `rg --files` (or an equivalent file search) to inspect the target checkout's `ruoyi-common/ruoyi-common-core/src/main/java/org/dromara/common/core/utils/`, including nested packages. Search by the required capability and method names, not only `*Utils` filenames. Check relevant `service/`, `constant/`, other `ruoyi-common` modules, and project-specific shared or business modules. For frontend work, inspect `plus-ui/src/utils/`, `hooks/`, `components/`, and existing API modules. Treat these as target-relative lookup hints; discover relocated packages from source instead of treating a missing default path as proof that no capability exists.
2. **Read the matching implementation and usage.** Inspect method signatures, overloads, relevant superclass/delegated methods, and representative callers. Verify null/empty handling, duplicate-key policy, ordering, collection mutability, exceptions, time zones, side effects, and permission/transaction behavior as relevant. Confirm the correct import and that the target module can use the dependency. A same-named third-party class is not evidence that it preserves the project's wrapper behavior.
3. **Choose reuse by verified fit.** When an existing project method satisfies the requirement, call it directly or compose it with the required business rules. Check project wrappers before using an underlying library directly; use JDK or already-present library APIs when no project method fits. A changed name, a private method, an inline loop/stream/recursion, or a one-line forwarding wrapper does not justify duplicating an existing capability. Keep task-specific business validation and orchestration in its existing service boundary; generic helpers do not replace business rules.
4. **Establish the gap before adding code.** Record searched paths/terms and the concrete missing behavior or dependency constraint. Then implement only the uncovered part. Extend a shared utility only when the shared contract warrants it and existing callers remain compatible; otherwise keep the smallest suitable implementation in the owning module. Do not introduce a new library or cross-module implementation dependency merely to obtain reuse. If the required source cannot be inspected, report the evidence gap under the Standards Gate rather than claiming the capability is absent.
5. **Check the final additions.** Inspect the diff, or the final changed files when Git is unavailable, for duplicated common operations, including logic embedded in Service/Controller code. Replace equivalent implementations with the verified existing method. Include compact reuse evidence in the current workflow's output: searched scope/terms, selected `path#method` and caller, or the reason each new common operation was necessary. Missing reuse evidence leaves this profile check unfinished.

### Backend Lookup Hints

Start at `ruoyi-common/ruoyi-common-core/src/main/java/org/dromara/common/core/`; the table is a search aid, not an exhaustive API catalog. Inspect the actual checkout before using a name or assuming a method's behavior.

| Needed capability | Inspect first |
|---|---|
| Collection mapping, filtering, grouping, joining, Map/Set conversion | `utils/StreamUtils.java` and its callers |
| Tree construction, multiple roots, leaf nodes, tree-path maps | `utils/TreeBuildUtils.java` and its callers |
| String splitting/joining, blank checks, naming conversion | `utils/StringUtils.java`, including inherited APIs |
| Date formatting, intervals, range validation | `utils/DateUtils.java`, including inherited APIs |
| Object conversion, validation, masking | `utils/MapstructUtils.java`, `utils/ValidatorUtils.java`, `utils/DesensitizedUtils.java` |
| File, IP, regex, reflection, request/context helpers | Nested `utils/` packages and the matching helper implementation |
| Existing business capability or shared contract | Owning module's service/API, core `service/` and `constant/`, and the relevant common module |

For example, collection-to-map work starts by inspecting `StreamUtils.toMap` / `toIdentityMap`; verify the duplicate-key policy against the requirement. A multi-root tree or tree-path lookup starts by inspecting `TreeBuildUtils.buildMultiRoot` / `buildTreeNodeMap` and existing callers, before writing another traversal. These are candidate methods, not permission to change observable behavior to fit them.

## Workflow Integration

- **think / grill:** Use the standard to investigate reuse, data fields, JSON, ownership, permissions, background identity, nullable updates and uniqueness. Preserve their interview discipline and planning-only output. Development/compilation steps apply when implementation starts, not before code exists.
- **story:** Carry the agreed DDL, Entity/BO/VO fields/types, API and permission contracts, frontend behavior, nullable-field semantics and verification into the existing issue scope and acceptance criteria. The workflow and task formats remain the existing ones.
- **implement / tdd / debug:** Load the original standard before affected code work. Follow its reuse/model alignment, implementation and delivery requirements within the active workflow. Debugging still needs root-cause evidence. TDD designs tests and reaches RED before production implementation; the original compilation and delivery checks apply after GREEN, not as a reason to bypass RED. Sub-agents independently re-read the configured profile and original reference.
- **review:** Each perspective reads the original standard for its scope. Test Review checks behavior and boundaries; Code Review checks framework/mapping/frontend conventions; Impact Review checks data scope, background identity, schema scripts and cross-module effects. The original six checks supplement these perspectives.

Apply the shared [Standards Gate](../rules/entry-protocol.md#standards-gate) for missing rules, verification evidence and completion decisions. Its stage boundaries govern planning, TDD intermediate phases and reviews; do not maintain a separate exception policy here.

## Clarifications Applied Alongside the Original

These explain how to verify the original requirements; they do not rename its APIs or remove any rule:

- The specified TypeScript `string | number` type remains required. Also inspect actual ID serialization: the union type cannot recover precision after a large JSON number has already been rounded.
- The original says to use `DataPermissionHelper.ignore` **as needed** in background work. Establish the operation's intended identity, ownership and data scope before deciding whether a bypass is needed; absence of a login session alone does not define that scope.
- Select Maven wrapper/module/profile and frontend commands from the actual POM, package scripts, lockfiles and CI. The original `mvn test-compile` example triggers annotation processing; it is not evidence that a particular checkout compiled, nor a replacement for its tests.
- Apply checks to the affected task. Report unrelated historical violations separately rather than expanding the implementation scope.

## Source Maintenance

The bundled `references/ry-coding.md` is the single maintained definition of the team's framework conventions within this skill. Edit that source when conventions change, then re-check integration and installation. Keep profile-specific workflow wiring here and in SKILL.md; do not maintain a second translated rule catalog. The source alignment record is repository-only under `docs/evals/results/` and is not needed at runtime.
