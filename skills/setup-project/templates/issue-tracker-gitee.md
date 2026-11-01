# Issue tracker: Gitee

Issues and pull requests live in the configured Gitee repository. Use an already-connected **official Gitee MCP** when its tools cover the operation; otherwise use the **Gitee OpenAPI v5** below. `gh` and `glab` do not operate on Gitee.

## Repository and authentication

- Repository: `<owner>/<repo>`, inferred from the selected `git remote -v` entry (`https://gitee.com/<owner>/<repo>.git` or `git@gitee.com:<owner>/<repo>.git`). Record the selected remote; a GitHub mirror does not change the tracker.
- API base: `https://gitee.com/api/v5`. For Gitee Enterprise/private deployments, record and verify their actual API and MCP service; do not assume the public API applies.
- REST credential: environment variable `GITEE_ACCESS_TOKEN`; MCP credentials are configured in the host. Never write a token into tracked configuration or print authenticated request URLs.
- Read the current MCP tool schemas before calling them. If no MCP is connected, REST is a supported fallback; do not invent a `gitee` CLI or install/configure a server without the user's request.
- Gitee **Issue numbers are case-sensitive strings** (for example `IABC12`), distinct from numeric database `id` and numeric PR numbers. Preserve the returned `number` and `html_url` in PRDs, dependencies, and reports.

## Conventions

Use the same issue lifecycle and Story Format as the GitHub tracker template. The operation map supplies Gitee's platform-specific calls; consumer skills keep their existing workflow.

Paths below are relative to the API base. Supply `access_token` from the environment as documented by OpenAPI; keep it out of command output. Use the HTTP client's structured path/query/body parameters. Ordinary writes use named JSON fields (the published operations declare `application/json`); read authentication uses the documented query parameter. Send multiline Markdown from a UTF-8 file/string, never shell interpolation.

| Operation | Method and path | Parameters / handling |
|---|---|---|
| Read repository | `GET /repos/{owner}/{repo}` | Verify the selected repository and access before writes |
| List issues | `GET /repos/{owner}/{repo}/issues` | `state=open|progressing|closed|rejected|all`, optional `labels`, `page`, `per_page` (max 100) |
| Read issue | `GET /repos/{owner}/{repo}/issues/{number}` | Fetch comments separately |
| Read comments | `GET /repos/{owner}/{repo}/issues/{number}/comments` | Paginate; include comments when interpreting requirements |
| Create issue | `POST /repos/{owner}/issues` | **`repo` is a body parameter**, along with `title`, `body`, optional comma-separated `labels` |
| Update / close issue | `PATCH /repos/{owner}/issues/{number}` | `repo`, changed fields; `state=open|progressing|closed` |
| Comment on issue | `POST /repos/{owner}/{repo}/issues/{number}/comments` | `body` |
| Read repository labels | `GET /repos/{owner}/{repo}/labels` | Map the project's triage vocabulary before assigning labels |
| Add issue labels | `POST /repos/{owner}/{repo}/issues/{number}/labels` | JSON array of label names, not GitHub's `{labels: [...]}` object |
| Remove one label | `DELETE /repos/{owner}/{repo}/issues/{number}/labels/{name}` | Encode the label name; preserve unrelated labels |
| Create PR | `POST /repos/{owner}/{repo}/pulls` | `title`, `head`, `base`, `body`; derive branches from Git/repository metadata |
| Read PR | `GET /repos/{owner}/{repo}/pulls/{number}` | Read base/head metadata before fetching a local diff |
| PR changed files | `GET /repos/{owner}/{repo}/pulls/{number}/files` | API returns at most 300 diffs; missing patches / limit reached require a local Git diff or an explicit incomplete-review report |
| Read PR comments | `GET /repos/{owner}/{repo}/pulls/{number}/comments` | Paginate reads |
| Comment on PR | `POST /repos/{owner}/{repo}/pulls/{number}/comments` | `body` |
| Read release | `GET /repos/{owner}/{repo}/releases/latest` | Or list `/releases` and select the requested tag |

For label-array writes, use the documented JSON array body with authentication in a separate query parameter, rather than wrapping the array in an object. Paginate collection endpoints that expose `page`/`per_page` until exhausted. Check HTTP status and response before recording success; on 401/403, report the missing access, and on 429 respect retry timing. After a timeout on a create/comment request, read back/search before retrying to avoid duplicates.

## When a skill says "publish to the issue tracker"

Create a Gitee issue using the configured MCP or `POST /repos/{owner}/issues`, with the repository in `repo`. Use the Story Format (`## What to build`, `## Acceptance Criteria`, `## Blocked by`). Record the returned Issue number and URL in the existing PRD/Story traceability fields.

## When a skill says "fetch the relevant ticket"

Read `GET /repos/{owner}/{repo}/issues/{number}` and its current comments and labels, or use equivalent configured MCP tools. Preserve the returned string identifier and URL.

## PRs and traceability

- **Parent and child issues:** use `parent_id` only when supported and the parent's numeric `id` was fetched. Otherwise keep explicit parent/child URLs in the issue bodies and PRD. Dependencies remain explicit Markdown links; do not assume GitHub sub-issue APIs or closing keywords work here.
- **Review a PR:** use the operations above, or fetch the verified base/head branches and run `git diff <base>...<head>`. Check completeness against PR metadata. Reading a PR authorizes no merge or publication of comments by itself.
- **Unavailable remote access:** prepare the issue/PR text locally and report that it has not been published. Do not silently change the configured tracker to local Markdown or GitHub.

## Sources

Verified against Gitee OpenAPI **5.4.93**, 2026-10-31: [interactive API reference](https://gitee.com/api/v5/swagger), [machine-readable schema](https://gitee.com/api/v5/doc_json). Official MCP setup and capabilities: [oschina/mcp-gitee](https://github.com/oschina/mcp-gitee), with a separate [Enterprise server](https://github.com/oschina/mcp-gitee-ent).
