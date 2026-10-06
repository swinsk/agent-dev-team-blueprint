# CLAUDE.md

Claude Code reads this file at session start. It imports the universal instructions so there is one source of truth.

@AGENTS.md

## Claude Code specifics

- The top-level session is the **orchestrator** (`@roles/orchestrator.md` describes it). The team members are subagents in `.claude/agents/`, generated from `roles/`.
- The orchestrator dispatches only `dev-manager`. The dev manager dispatches the rest.
- **The dev manager dispatches its team in the foreground** (the Agent tool with background disabled) so each result returns to the manager. In Claude Code a background subagent's completion notification goes to the top-level session, not to the subagent that spawned it; a manager that fires and forgets is stranded.
- Parallel developers on one repo: dispatch each with worktree isolation (`isolation: worktree`) or serialize them.
- Never write `tools: All tools` in an agent file. It binds zero tools. Omit the `tools` line to inherit all tools (the dev manager needs the Agent tool to dispatch).
- Subagent nesting depth is limited (configurable; see the Claude Code subagent docs). Orchestrator, then manager, then team is two levels below the top-level session, inside the default limit. Do not let team members spawn further agents.
- Headless runs (`claude -p`): never end the run while a subagent is in flight. See `principles/manager-lessons.md`.
