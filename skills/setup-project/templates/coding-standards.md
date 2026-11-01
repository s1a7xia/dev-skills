# Project Coding Standards

This file registers the project's coding conventions. Consumer skills load it through the Skill Entry Protocol; it supplements the existing workflow and does not grant execution permissions.

## Applicability

- **Scope**: `<repository / modules / file types>`
- **Stack and version**: `<observed framework and version, with source file>`
- **Technical profile**: `<installed skill name, e.g. ruoyi-plus-dev; or none>`
- **Additional standards**: `<project-relative paths to maintained team conventions, or none>`
- **Source of API truth**: `<actual module, generator templates, and reference implementations>`

Choose a profile only when the project or user identifies it. A Java/Vue dependency alone does not establish that the project uses RuoYi-Vue-Plus. Do not leave placeholders in generated configuration.

## Verification

| Stage / affected change | Required check and applicability | Command and working directory | Evidence |
|---|---|---|---|
| `<delivery stage and affected code / schema / frontend>` | `<check, why it applies, and completion condition>` | `<real repo command from build files or CI>` | `<exit status and relevant result for final changes>` |

Drop inapplicable rows. For a RuoYi profile, inspect the POM, Maven wrapper, profiles, frontend package scripts and lockfile before selecting commands; an example such as `mvn test-compile` is not proof that this exact command works in this repo.

The installed Skill Entry Protocol's Standards Gate governs prerequisite loading and completion. Keep the actual paths of configuration, profile and original rules read in the task evidence. A stage/scope exclusion needs a reason; an unavailable dependency or a failed required check remains unresolved.

## Project decisions and exceptions

Record explicit exceptions with scope, rationale, and the relevant ADR or user decision. Read existing standards before merging this configuration. Link detailed rules to their maintained source instead of copying them into every workflow skill.
