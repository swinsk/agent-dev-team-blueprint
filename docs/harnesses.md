# Harness notes

One source of truth (`roles/*.md` plus `roles/_shared-rules.md`), thin generated adapters per harness. Formats below were checked against the official docs on the date in each section; re-check them when you adopt this, because these surfaces change often.

## Universal: AGENTS.md

`AGENTS.md` at the repo root is the entry point any agent can read. GitHub Copilot and OpenAI Codex read it natively; Claude Code reads it through the `@AGENTS.md` import in `CLAUDE.md`.

## Claude Code

Checked: 2026-10-06. Docs: https://code.claude.com/docs/en/sub-agents

- Subagents: Markdown files in `.claude/agents/` with YAML frontmatter. `name` and `description` are required; `tools`, `model`, and others are optional.
- `model` accepts an alias (`sonnet`, `opus`, `haiku`, ...), a full model ID, or `inherit`.
- **Omitting `tools` inherits every tool.** A value is parsed as a list of literal tool names, so a phrase like `All tools` binds nothing. The generator never writes a tools line for roles that should inherit all tools (the dev manager needs the Agent tool to dispatch its team).
- Subagents can spawn subagents up to a configurable depth. Background subagent results arrive as a completion notification in the session; in our experience that notification goes to the top-level session, so the dev manager dispatches in the foreground.
- `CLAUDE.md` supports `@path` imports; ours imports `AGENTS.md`.
- Worktree isolation is available per dispatch and per agent (`isolation: worktree`).

Adapter: `.claude/agents/<role>.md`. The orchestrator is the main session (driven by `CLAUDE.md`), so it has no agent file.

## GitHub Copilot

Checked: 2026-10-06. Docs:
- Custom agents configuration: https://docs.github.com/en/copilot/reference/custom-agents-configuration
- Creating custom agents: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents
- Repository custom instructions: https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot
- Prompt files: https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/your-first-prompt-file

What the docs say:
- Custom agents: `.github/agents/<name>.agent.md`, YAML frontmatter plus a Markdown prompt (max 30,000 characters). `description` is required; `name`, `target` (`vscode`, `github-copilot`, or unset for both), `tools`, `model`, `disable-model-invocation`, `user-invocable`, `mcp-servers`, and `metadata` are optional.
- `tools`: omitted or `["*"]` means all available tools; `[]` disables all. Aliases include `read`, `edit`, `search`, `execute` (shell), `web`, `todo`, and `agent` (invoke other custom agents).
- Repository instructions: `.github/copilot-instructions.md`; path-specific `.github/instructions/*.instructions.md` with `applyTo`. Copilot also reads `AGENTS.md` (nearest in the tree wins) and a root `CLAUDE.md`.
- Prompt files: `.github/prompts/*.prompt.md`, frontmatter such as `agent` (a built-in mode or a custom agent name) and `description`, with `${input:name:hint}` variables. The IDE prompt-file docs list further optional keys (`name`, `argument-hint`, `model`, `tools`); support varies by surface.

Running with Claude Opus 5.5: the generated agents carry no `model` line, so they use the model selected in Copilot. Choose Claude Opus 5.5 in the model picker, or add a `model:` line to the role adapter with the exact model name your Copilot surface lists (names differ between surfaces, so we did not hard-code one). If you add it, add it in the generator so it survives regeneration.

Topology on Copilot: whether a custom agent can invoke other custom agents as subagents depends on the surface and its `agent` tool support. If your surface supports it, select `dev-manager` and let it invoke the others. If it does not, use the **flattened topology** in `README.md`: you act as the orchestrator, and you run each role in turn by selecting its agent (or assigning the issue to it), with `dev-manager` as the session that reviews and decides.

Adapters: `.github/agents/<role>.agent.md` (the six team roles only; there is deliberately NO orchestrator agent, because your existing main assistant is the orchestrator, see `INSTALL.md`), `.github/copilot-instructions.md`, `.github/prompts/*.prompt.md`.

## OpenAI Codex

Checked: 2026-10-06. Docs:
- AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- Subagents and custom agents: https://developers.openai.com/codex/subagents
- Configuration reference: https://developers.openai.com/codex/config-reference

What the docs say:
- Codex builds an instruction chain once per run: global `AGENTS.override.md` or `AGENTS.md` in the Codex home, then from the project root down to the working directory, checking `AGENTS.override.md`, then `AGENTS.md`, then any names in `project_doc_fallback_filenames`. Files are concatenated root first, so closer files override broader ones. The combined size is capped (32 KiB by default, `project_doc_max_bytes`). Keep `AGENTS.md` lean; this blueprint's is well under the cap.
- Custom agents: one TOML file each in `.codex/agents/` (project) or the personal agents folder in the Codex home. Required keys: `name`, `description`, `developer_instructions`. Other config keys (such as `model`, `model_reasoning_effort`, `sandbox_mode`, MCP servers) may be added.
- Subagents are spawned when you ask Codex to delegate (for example, "spawn the backend-dev agent for issue 42"). Concurrency is configurable under `[agents]`.
- The docs we checked do not state whether a spawned agent can itself spawn agents. So on Codex, run the **dev manager as the top-level session** and let it spawn the team; do not rely on an orchestrator to manager to team chain.

Adapters: `.codex/agents/<role>.toml`. See `codex/README.md` for a run recipe.

## Keeping adapters in sync

```
python3 scripts/build_adapters.py          # regenerate
python3 scripts/build_adapters.py --check  # fail if anything drifted (CI runs this)
```

Never edit a generated file by hand; edit `roles/` and regenerate.
