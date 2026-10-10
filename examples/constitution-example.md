# Example constitution

An illustrative constitution for a fictional product, **ExampleApp** (a multi-tenant web and mobile app). Use it as a model for `.specify/memory/constitution.md` in your own repo; the template is `patterns/templates/spec-kit/constitution-template.md`, and the method is `patterns/spec-driven.md`. Replace every principle with your own.

---

# ExampleApp Constitution

**Status**: EXAMPLE. Adapt before use.

This constitution governs every spec, plan, task list and PR in the ExampleApp repository. Each plan must pass the Constitution Check below, or justify the violation in its Complexity Tracking table. Where a rule was set by the owner, record its date.

## Core Principles

### I. Never Lose or Corrupt User Data (NON-NEGOTIABLE)
Every change that touches stored data states how it preserves existing records in its acceptance scenarios and proves it against realistic test data. Migrations are reversible or backed up before they run. Nothing a user saved changes without their action, and every destructive operation can be undone or was confirmed.

### II. Quality Over Speed
Never trade correctness or output quality for delivery speed. Defaults are chosen on measured results, not on what is fastest to build. Specs set no deadlines that would pressure quality; the UI is honest about anything slow (real progress, real estimates, never a number we cannot back).

### III. Honest Labels and Provenance
Users always know what produced a result and how reliable it is. Automated or AI-generated content is labelled; failures are shown as failures, never dressed up as success; any measurement shown states its limits.

### IV. Evidence, Spec First, QA Before Ship
Every new priority starts with a spec in `specs/NNN-short-name/` (what and why, never how). A story is done only when its acceptance scenarios pass on the real running product, with the QA report quoting the success-criteria and requirement ids. Claims are verified from the artifact (branch tip, test run, live check), never from memory. If code and spec disagree, one is fixed on purpose by PR.

### V. Access, Data and Spend Gates
No real-user data in development or tests; use synthetic data. Any new paid resource, plan upgrade, public exposure or onboarding of outside users is an owner decision, raised with a recommendation. Secrets are referenced by name from a secrets manager; no key, token or password value is written anywhere.

### VI. Machine Etiquette and Process Safety
Shared machines and devices are single-tenant: claim them with a lock before use and release it when done. Never close a person's apps on a shared machine without an explicit instruction. Stop processes only by exact process ID or the port you started. Large artifacts go to dedicated storage, never the build machine; check free space before large writes and stop below a safe threshold.

## Additional Constraints

- **Budget guard**: the team pauses near its usage limit and resumes after the reset; commit often.
- **Writing**: pick one house style for code, copy, specs, commits and PRs, and enforce it in CI.
- **Mocks match live shapes**: frontend fixtures are captured from a real backend.
- **Tests**: fixtures are tracked; a missing fixture fails its test; parallel runs use separate temp dirs.
- **Tenant isolation**: every by-id read and operation is tenant-scoped.

## Development Workflow

1. Constitution (this file), then per priority: Specify (product manager), Clarify (at most one owner question, with a recommendation), the owner's feature-level yes, Plan with Constitution Check (dev manager), Tasks, Analyze, Implement (developers, story by story, branch and PR), Verify (QA).
2. A developer who finds the spec wrong stops and tells the dev manager, who amends the spec by PR first.
3. The dev manager reviews every PR for drift from the spec and this constitution, and merges and releases only after a QA PASS for that exact commit.
4. The board mirrors the spec: one epic card per spec, one story card per user story, tasks as a checklist in `tasks.md`.
5. `docs/DECISIONS.md` is the running decision log (date, decision, why, who); real architecture decisions get a short ADR in `docs/adr`.

## Governance

This constitution supersedes other practice in this repository. Amendments are made by PR, reviewed by the dev manager, and logged in `docs/DECISIONS.md`; amendments to Principles I, II or V also need the owner's approval. Every PR and review verifies compliance. Complexity must be justified in the plan.

**Version**: 1.0.0 (example)
