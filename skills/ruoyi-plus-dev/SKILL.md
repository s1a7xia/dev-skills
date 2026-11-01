---
name: ruoyi-plus-dev
description: "Use when writing or changing Java business code, plus-ui Vue/TypeScript, or SQL in a confirmed RuoYi-Vue-Plus 6.X project, or when project configuration selects this coding profile. Provides team framework conventions and verification gates. For diagnosis, diff review or planning, keep debug/review/think/grill as the active workflow and load this profile as context. Trigger words: ruoyi-plus-dev, RuoYi-Vue-Plus, 若依Plus, 若依编码规范."
---

# RuoYi-Vue-Plus Development Profile

## Outcome Contract

- **Outcome**: The current task follows the team's RuoYi-Vue-Plus 6.X backend, plus-ui frontend, and database conventions.
- **Done when**: The original applicable rules have been read, relevant conventions checked against the target source, reuse decisions supported by the [Repository Reuse Check](REFERENCE.md#repository-reuse-check), and every check required for the active stage has passed under the [Standards Gate](../rules/entry-protocol.md#standards-gate). A blocked/failed check leaves the affected deliverable unfinished.
- **Evidence**: Actual standard/profile/source paths read, reused methods or justified gaps, applicable checks, and command working directories, exit statuses and results for the final changes. Planning produces a design and records why code checks do not yet apply.
- **Output**: Attach the applicable profile findings to the current workflow's output. This profile does not create a second PRD/specification or auto-start another skill.

## Process Summary

1. Apply the [Skill Entry Protocol](../rules/entry-protocol.md). If it already selected this profile, continue without recursively restarting the protocol. Read the target project's coding-standards configuration and actual framework version.
2. Read [REFERENCE.md](REFERENCE.md) for integration and the [complete original team standard](references/ry-coding.md) for the rules. Read the original sections relevant to the current stage in full; a summary does not replace them. Treat its code paths as target-project lookup hints, not files inside this skill package.
3. Before writing affected code, complete the [Repository Reuse Check](REFERENCE.md#repository-reuse-check): for backend work inspect `ruoyi-common/ruoyi-common-core/src/main/java/org/dromara/common/core/utils/` (including subpackages) and relevant project utilities/services; for frontend work inspect shared utilities/hooks/components. Read matching implementations and existing callers. Inspect generator/demo templates for CRUD work. Verify API and behavioral fit from source; resolve baseline/version mismatches explicitly.
4. Apply the profile at the current stage using the table below. Check only the affected scope, preserving existing API, authorization, validation, transaction, and UI contracts.
5. Apply the [Standards Gate](../rules/entry-protocol.md#standards-gate) before declaring completion or approving compliance. Report checks and evidence using the active workflow's output; if used directly, use the compact output below.

## Stage Integration

| Active stage | Profile contribution |
|---|---|
| think / grill | Inventory framework reuse; resolve physical-column vs JSON needs, ownership vs audit fields, background execution identity, permissions, nullable updates, uniqueness and state transitions. Preserve the workflow's one-decision-at-a-time interview discipline. |
| story | Put agreed SQL, Entity/BO/VO, API, permissions, frontend interactions and verification into the existing issue's build scope and acceptance criteria. Use the existing `ready-for-agent` / `ready-for-human` triage roles when relevant. |
| implement / tdd | Check reuse before production edits, inspect templates, implement the agreed slice, and compile after mapping changes to generate MapStruct code. Test behavior at public interfaces and preserve the active workflow's gates. |
| debug | Inspect the affected framework layer while reproducing the defect; use the debugging workflow's evidence before changing code. |
| review | Test perspective checks observable contracts; Code checks reuse evidence and framework/mapping/frontend conventions; Impact checks permissions, background identity, schema migration, and cross-module effects. Preserve the three independent perspectives. |

## Gotchas

| What happened | Rule |
|---|---|
| Original RuoYi APIs mixed into Plus code | Do not introduce `SecurityUtils`, `@PreAuthorize`, `AjaxResult`, `TableDataInfo`, or `BeanUtils.copyProperties`; follow the verified Plus interfaces. |
| Every setting becomes a new table | Check `sys_config`, `sys_dict_*`, and existing framework entities first; classify domain records separately. |
| Existing tools are bypassed by a new helper or inline business-code implementation | Apply the [Repository Reuse Check](REFERENCE.md#repository-reuse-check); identify the existing method or document the concrete gap before adding equivalent logic. |
| Every background task bypasses permissions | Define service identity and data scope; `DataPermissionHelper.ignore` requires an explicit, justified scope. |
| Required mappings have not compiled | Run the project's actual Maven compile/test-compile command; an unavailable or failed required compilation leaves the deliverable blocked/failed, not complete. |
| Unrelated project receives RuoYi constraints | Apply only in a confirmed RuoYi project or when explicitly selected in project configuration. |

## Output

```text
Profile: ruoyi-plus-dev — <scope and observed version>
Status: <verified for this stage / blocked / failed>
Standards read: <configuration, profile and original reference paths>
Source/template evidence: <paths>
Reuse evidence: <searched scope/terms; reused path#method or concrete gap and chosen implementation>
Applicable checks: <passed / findings / not applicable>
Verification: <command, working directory, exit status, relevant output>
Unfinished requirements: <none / failed or blocked checks and next action>
```
