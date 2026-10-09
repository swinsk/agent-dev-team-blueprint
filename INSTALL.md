# INSTALL.md: read this before installing anything

This file is for the AI agent doing the install (Copilot, Claude Code, Codex or any other harness). Follow it exactly. These rules exist because an install once created a second orchestrator next to the user's existing one.

## Rule 1: the orchestrator already exists. Never create another.

The orchestrator is the user's own primary assistant: the agent the user talks to every day, often with a name and personality of its own (for example "Jarvis"). **If you are the agent running this install, you are almost certainly that assistant.**

- Do NOT create, copy or register an `orchestrator` agent, and do NOT create any new top-level or primary assistant, under any name.
- Do NOT create an agent that duplicates or renames the existing primary assistant (another "Jarvis", another "Optimus", another "assistant", "main", "chief", "copilot" and so on).
- Instead, the EXISTING primary assistant takes on the orchestrator duties. Merge the content of `roles/orchestrator.md` into that assistant's existing instructions as a clearly marked block (see Rule 4), without changing its name, persona or other instructions.
- If you cannot tell which agent is the primary assistant, STOP and ask the user one question: "Which agent is your main assistant? It will become the team's orchestrator." Do not guess and do not create one.

## Rule 2: detect before you write

Before copying any file, list what the target system already has:

1. Every existing agent definition the harness uses (for example `.github/agents/*.agent.md`, `.claude/agents/*.md`, `.codex/agents/*.toml`, plus any user-level or organization-level agent folders the harness reads).
2. Each agent's `name`, file name and description.
3. Any repository or user instruction files (`AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`).

Treat an existing agent as the **primary assistant** if any of these is true: you are it; its name or description says main, primary, chief, orchestrator, assistant or similar; it is the user's named persona; or the user calls it their assistant.

## Rule 3: install only the six team roles, and never overwrite

Install only: `dev-manager`, `product-manager`, `backend-dev`, `frontend-dev`, `qa`, `release-manager`.

- If an agent with the same file name or `name` already exists, do NOT overwrite it. Show the user the conflict and ask whether to skip it, rename the new one (for example `team-qa`), or replace it.
- Never delete, rename or edit an existing agent other than the marked orchestrator block from Rule 1.
- The install is idempotent: if the marked block or the six roles are already present, update them in place; never add a second copy.

## Rule 4: the orchestrator merge block

Add this block to the existing primary assistant's instructions (its agent file, or the user or repository instruction file it reads), replacing any older copy of the same block:

```
<!-- BEGIN agent-dev-team-blueprint: orchestrator duties -->
(paste the body of roles/orchestrator.md here, from "# Orchestrator" to the end)
<!-- END agent-dev-team-blueprint: orchestrator duties -->
```

## Rule 5: verify and report

After installing, list for the user: the agent that now holds the orchestrator duties (by its existing name), the six team agents installed or skipped, any conflicts and how they were resolved, and confirm that **no new orchestrator or primary assistant was created**. If one was created by mistake, remove it and say so.

## If the user has no primary assistant at all

Only then, and only after the user confirms they want one, may you set one up from `roles/orchestrator.md`, under a name the user chooses.
