# Dev manager lessons: what broke, and the rule it produced

The dev manager is the role that makes an autonomous team work, and it is the role that failed in the most expensive ways. Each lesson below is a real failure from running this pattern in production, generalized. The rule after each one is already written into `roles/dev-manager.md`; this file is the why.

## 1. The orchestrator kept doing the manager's job

**What happened.** The top-level assistant kept "helping": it collected the subagents' completions, ran the QA gate itself, and drove the deploys. Work got done, but the orchestrator became the bottleneck and the manager never learned to own delivery.

**Rule.** The orchestrator talks only to the manager and stays out of the team's way. It never collects subagent handbacks, never runs QA or deploys for the team. If it finds itself doing so, the manager's loop is broken and that is what gets fixed.

## 2. Background children reported to the wrong parent

**What happened.** The manager dispatched its team in the background (the harness default), then said "standing by for handbacks" and ended its turn. On that harness, a background child's completion notification goes to the **top-level** session, not to the subagent that spawned it. The manager was stranded forever; the handbacks landed on the orchestrator.

**Rule.** The manager dispatches its team in the foreground (blocking), so each result returns to the manager in-turn. It runs one long resident loop: dispatch, block, verify, dispatch next. Parallel streams are separate blocking chains in separate worktrees. Check your harness's notification routing before relying on background dispatch.

## 3. The manager went idle between steps

**What happened.** The manager dispatched a build, got a handback, and stopped instead of driving the next step. Two consecutive builds sat orphaned because nobody picked the handback up.

**Rule.** Active oversight: never go idle while any dispatched work is open. Every re-invocation is a cue to drive the next step, not to report status and stop. Stop only at shipped-and-verified or at a genuine human-decision blocker.

## 4. Returning the final answer killed in-flight work

**What happened.** In a headless run, the manager returned its final answer while a release and a developer were still working. The session ended, and the runner's ceiling on leftover background work (about ten minutes) expired and killed both. A build that had actually uploaded was then partially redone by the next run.

**Rule.** Never return a final answer while a subagent is in flight. Block on foreground calls, or poll the real state in a loop, until every step reaches a terminal state.

## 5. A literal "All tools" bound zero tools

**What happened.** The manager's agent definition said `tools: All tools`. The harness parsed it as a list of two tool names, "All" and "tools", neither of which exists, so the manager launched with no usable tools. It finished instantly with zero tool calls and printed its intended first command as plain text. It stalled twice before anyone checked the config.

**Rule.** To grant all tools, **omit** the tools line (or use the harness's documented wildcard, such as `["*"]` on GitHub Copilot). When any manager stalls, check its frontmatter first. A turn with zero tool calls is a configuration smell.

## 6. A compile-only signal almost shipped a crash

**What happened.** A developer reported a crash "fixed" with a green build. The crash still reproduced at runtime. It nearly went to release on the strength of "build succeeded".

**Rule.** Verify every handback independently. For runtime bugs, the runtime repro must be run and found clean. Compile success is not evidence of a runtime fix.

## 7. QA tested the wrong binary, twice

**What happened.** QA reused an already-installed app because its build number matched. Every build of the branch carried the same number. Two full QA passes ran against a binary that contained none of the changes, and produced a "bug" that did not exist in the real build.

**Rule.** Build identity is the commit SHA plus proof that the installed artifact contains something only that commit has (a string, asset, or stamp), plus a checksum in the progress file. Results from an unverified install are void.

## 8. Two developers in one checkout

**What happened.** A backend developer and a mobile developer worked the same checkout in parallel. The backend commit swept in the mobile developer's uncommitted files, producing two overlapping PRs. It only came out clean by luck.

**Rule.** At most two dev streams. Never two developers in one checkout: separate git worktrees, or serialize. Serialize the shared build phase (project generation, signing, simulators, the main checkout, deploys) to one writer at a time.

## 9. The runner killed every run at a fixed wall-clock cap

**What happened.** The queue runner that launched headless manager runs had a fixed timeout (45 minutes). Every run died at the cap and took its subagents with it. The manager kept planning as if it had unlimited time.

**Rule.** Know the wall-clock ceiling and plan each run as a shorter window. Checkpoint to the state file at every handback. Never start a long or irreversible step (an upload, a deploy, a migration) late in a window. Raise the cap for overseer roles if you own the runner.

## 10. Context was lost across pauses and crashes

**What happened.** Runs ended (budget pauses, runner caps, crashes) and the next run had to rediscover where things stood.

**Rule.** A durable `STATE.md`, re-read at the start of every run and updated after every meaningful step, with a "next run does exactly this" contingency block. Reality wins over the file: verify its claims against the remote and the live system before acting. See `patterns/state-file.md`.

## 11. A dead run had done more than it recorded

**What happened.** A run was killed before writing its last state entry. The next run saw no record of an upload and re-uploaded; the store silently renumbered the duplicate. The original had in fact succeeded.

**Rule.** On resume, reconcile before redoing. Check the remote, the store or release console, and the deploy history for evidence the step already happened. Redo only what is provably missing.

## 12. Budget ran out mid-pipeline

**What happened.** Long epic runs approached the plan's usage window limit. Running out mid-deploy would leave things half-done.

**Rule.** A usage guard runs before every dispatch and every new story. At the threshold it pauses cleanly (committed branches, nothing half-deployed), writes a `PAUSED` marker with the reset time, updates the state file, and ends the run. An external watcher relaunches the manager after the reset. Do not switch to another model provider to keep going unless the human allowed it. See `patterns/usage-guard.md` and `patterns/resume-watcher.md`.

## 13. The usage guard itself crashed

**What happened.** Right after a usage window reset, the usage source omitted a field the guard expected. The guard threw, and the run stopped for the wrong reason.

**Rule.** The guard fails safe and loud: a missing reading is logged as a warning and handled explicitly (treated as zero only if the source is known to omit it after a reset; otherwise treated as "stop"). Test the guard against empty and malformed input.

## 14. Mid-task scope additions were refused

**What happened.** The manager sent the release manager an extra "also merge these" message mid-task. The release manager correctly refused: its charter says scope comes from the dispatch.

**Rule.** Put the complete scope in the dispatch. If scope changes, send a fresh dispatch.

## 15. A severe QA finding was a test-input artifact

**What happened.** QA filed a p1 "cannot sign in" bug. The real cause was the soft keyboard covering the button, so a tap landed on a key and appended a character to the password. Another time, a fault-injection variable passed the wrong way never reached the app, producing a false negative.

**Rule.** When a severe finding contradicts other evidence, run an A/B before mobilizing the team: known-good build versus new build in the same environment. Record each discovered QA gotcha in one sentence in the QA role file.

## 16. Credentials leaked into transcripts

**What happened.** QA typed a test password into a field that was screenshotted; a UI dump printed another; a release step printed a script containing a keychain password.

**Rule.** Credentials are read at run time from the secret store, never embedded in scripts, never displayed. Any exposure is an incident: report it, rotate the credential (immediately for throwaway test accounts).

## 17. Gated stories idled the team

**What happened (avoided).** Two stories needed vendor developer accounts only the human could create.

**Rule.** Build to the boundary, ship dark behind a flag, escalate the human step with exact instructions, and keep the other stream working. A credential gate never idles the team.

## 18. Escalations without recommendations

**Rule.** Every escalation carries options and a recommendation, framed so the human can answer in one word. A bare question pushes the manager's job back onto the human.

## 19. Infrastructure deploys need a preview

**Rule.** Before any infrastructure deploy, create and read a change preview. Expect only the named changes. Any replacement or deletion of a data resource stops the deploy. Learn which preview patterns are benign for your stack (for example, version cascades on shared layers) and write them into the release role so they stop causing false alarms.

## 20. Architecture decisions were made but not written

**Rule.** Every significant choice gets a short ADR in the repo, amended with a ship record. PR review checks diffs against the ADRs for drift. Without the record, the next developer reverses the decision without knowing it was one.
