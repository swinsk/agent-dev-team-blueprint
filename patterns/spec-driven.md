# Spec-driven development

Every new priority starts with a written spec. A spec says what we are building and why, and how we will know it works. It never says how to code it. The team builds from the spec, and QA tests against it. This pattern adapts GitHub Spec Kit (https://github.com/github/spec-kit, MIT) to a multi-role agent team. The templates are in `templates/spec-kit/`, and their source and licence are in `templates/spec-kit/NOTICE.md`.

## Why a team of agents needs this

- **Agents start cold.** Every dispatch re-reads context. A written spec is the one thing that does not drift between sessions, so a developer cannot quietly build something other than what the human meant.
- **"Done" becomes testable.** Acceptance scenarios and numbered success criteria give QA something exact to pass or fail. Without them, a QA verdict slides toward "looks good".
- **Questions surface before code.** The clarify step, the review debate and the analyze step catch gaps, untestable criteria and contradictions while they are still cheap to fix.
- **The human approves once, at the right level.** One feature-level yes on a readable spec, instead of being asked things mid-build.

## Where things live

| What | Where | Notes |
|---|---|---|
| Constitution | `.specify/memory/constitution.md` in the product repo | The project's non-negotiables. Written once from the role rules and the human's locked decisions. Amended by PR. |
| Spec | `specs/NNN-short-name/spec.md` | NNN is a zero-padded running number per repo. Versioned with the code and changed by PR. |
| Plan | `specs/NNN-short-name/plan.md` | Technical context, a constitution check, structure, and links to ADRs. |
| Tasks | `specs/NNN-short-name/tasks.md` | Grouped by user story, with `[P]` on tasks that can run in parallel and exact file paths. |
| Board | Your tracker | One epic per spec, plus one story per user story in the spec, keeping its priority (P1, P2, P3) and acceptance scenarios. Tasks stay a checklist in `tasks.md`; do not turn every task into its own issue. |

The full spec lives in the repo and the board is its live view. Keep the spec in the repo so it is versioned, reviewed and readable by every agent, and use the board for status.

## The flow and who owns each step

1. **Constitution (dev manager, once per repo).** Draft it from `templates/spec-kit/constitution-template.md`, using `roles/_shared-rules.md`, `principles/` and the human's locked decisions. The product manager files it by PR.
2. **Specify (product manager).** Fill `spec-template.md` from the human's priority:
   - User stories ranked P1, P2, P3. Each one is independently testable and has Given/When/Then acceptance scenarios.
   - Edge cases.
   - Functional requirements, FR-001 and up.
   - Measurable success criteria, SC-001 and up, with real numbers tied to how QA will test them.
   - Assumptions.
   - At most three `[NEEDS CLARIFICATION: question]` markers.
3. **Clarify (product manager).** Resolve every marker from the brief, the decision log and the existing docs, and record the answers in a Clarifications section. A question that truly needs the human goes to the dev manager as ONE question with a recommended answer. Never send the human a questionnaire about things the team can decide.
3b. **Spec review: the debate (dev manager runs it, before anything reaches the human).** A spec written by one agent and checked by nobody carries that agent's blind spots straight into the build. So before approval, the dev manager dispatches three reviewers in parallel. Each reads only `spec.md` and the brief, argues the opposite side, and returns numbered findings using `templates/SPEC-REVIEW.md`, each with a severity (blocker, major, minor) and a concrete fix:
   - **Builder** (one developer): can this be built with our stack and rules? What is missing or underspecified, and what hidden cost sits behind each requirement?
   - **Tester** (QA): can every acceptance scenario and success criterion be measured and tested on real data? Name every SC that is vague, unmeasurable or untestable.
   - **Domain critic** (whoever best speaks for the user: a subject-matter agent, a compliance-minded reviewer for regulated products, or the product manager role played adversarially by a fresh session): does this solve the user's real problem, and what would a demanding user hate?
   The product manager answers every finding in a `Review` section at the end of `spec.md`, marking each one accepted (with the change made) or rejected (with the reason). All blockers must be resolved. One rebuttal round at most: if a reviewer still disputes a rejected blocker, the dev manager decides, and only a true product call goes to the human, as ONE question with a recommendation. The dev manager attaches the review summary (the finding counts and the top changes) to the approval request.
4. **Approval (human, via the orchestrator).** The dev manager sends the orchestrator the spec summary: the stories in one line each and the top success criteria. The human's yes at feature level authorizes build, merge and ship, as in `principles/autonomy-and-gates.md`. Small specs inside an already-approved priority need no extra approval.
5. **Plan (dev manager).** Fill `plan-template.md`. The constitution check must pass, or the violation must be justified in Complexity Tracking.
6. **Tasks (dev manager, or the product manager with the dev manager's review).** Fill `tasks-template.md`, grouped by story.
7. **Analyze (dev manager).** Before any code, cross-check spec, plan and tasks for gaps, contradictions and constitution violations (`command-analyze.md`). Fix what it finds, then move the stories to Ready.
8. **Implement (developers).** Build story by story from `tasks.md`, citing task ids (T001 and up) and the story in commits and PRs, and ticking tasks in the PR. A developer who finds the spec wrong stops and tells the dev manager. The spec is amended by PR before work continues.
9. **Verify (QA).** Test against the acceptance scenarios and success criteria on the exact commit (`patterns/qa-gate.md`), quoting the FR and SC ids in the report. A story passes only when all of its scenarios pass.
10. **Release (release manager).** Ship only stories whose QA pass cites their scenarios, and list the spec ids in the changelog.

## Rules

- The spec is the source of truth. When code and spec disagree, fix one of them on purpose by PR; never leave them drifting.
- No speed target that could pressure quality unless the human asked for one.
- Specs carry no secrets: reference credentials by the name of their store entry only.
- Work already in flight finishes as it is. New priorities start with a spec.

## Example

`examples/constitution-example.md` is an illustrative constitution for the fictional ExampleApp; replace every principle with your own.
