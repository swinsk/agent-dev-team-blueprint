# Running the team on OpenAI Codex

Formats and sources: `docs/harnesses.md`.

## What Codex reads

- `AGENTS.md` at the repo root (and any closer to your working directory) at the start of each run.
- Custom agents from `.codex/agents/*.toml`, generated from `roles/`.

## Recommended topology

Codex is the dev manager. You are the orchestrator.

1. Start Codex in the repo and tell it which role it is:

   ```
   You are the dev-manager for this repository. Read AGENTS.md, roles/dev-manager.md and
   principles/manager-lessons.md. Approved work: Epic #12 and its stories. Window: until 17:00.
   Decisions: <list>. State file: <assignment dir>/STATE.md.
   ```

2. The manager spawns team members by name when it delegates, for example "spawn backend_dev for issue 42 in worktree ../wt/backend-42". Codex agent names use underscores (`backend_dev`, `release_manager`) because the generator converts hyphens.

3. For unattended runs, launch Codex non-interactively from your run queue (see `patterns/run-queue.md`) with a "resume the assignment" prompt; the resume watcher pattern applies unchanged.

## Codex-specific cautions

- The instruction chain is built once per run. If you edit `AGENTS.md` mid-run, start a new run.
- Keep the combined instruction size under the configured cap; put long material in `roles/`, `principles/`, and `patterns/` and let the agent read it on demand.
- Use the sandbox and approval settings your organization requires. A sandbox that blocks network or writes outside the workspace will block `git push`, PR creation, and writing the assignment state outside the repo; grant exactly those, nothing broader.
- Never wait for a background notification at the end of a non-interactive run: nothing re-invokes a finished run. Block, or poll in-turn, until each spawned agent finishes.
