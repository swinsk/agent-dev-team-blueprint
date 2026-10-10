# Example constitution

A real constitution from an internal AI music studio built with this team structure (DAWArtist Studio), lightly edited to remove infrastructure details. Use it as a model for `.specify/memory/constitution.md` in your own repo; the template is `patterns/templates/spec-kit/constitution-template.md`, and the method is `patterns/spec-driven.md`.

---

# DAWArtist Studio Constitution

**Status**: DRAFT (2026-10-09). Shared copy, lightly edited to remove internal infrastructure details.

This constitution governs every spec, plan, task list and PR in the DAWArtist Studio repository. Each plan must pass the Constitution Check below, or justify the violation in its Complexity Tracking table. Where a rule was set by the owner, its date is given.

## Core Principles

### I. The Preservation Contract (NON-NEGOTIABLE)
Everything outside the artist's approved edit region stays sample-identical, and this is checked before every save, outside any model. Every feature that touches audio states its preservation check in its acceptance scenarios and proves it on a real song. A gate, label or picker may change which options are shown, never the audio of anything the artist did not approve. Nothing the artist approved changes behind their back. Every approved change is a version on a branch, so the artist can compare against the original and undo.

### II. Quality Over Speed (2026-10-07)
Never trade output quality for render time. Every engine default is chosen on measured quality plus a music-vision read, even when renders get slower. Render time is a hardware problem we will solve later. Specs set no speed targets that could pressure quality; the waiting UI must stay honest (real stage, real progress, estimates from measured records, never a number we cannot back).

### III. Honest Labels and Provenance
The artist always knows what produced what. The engine is named on the card and in the version line; no engine is substituted silently; an option that failed a check is never shown as a normal option; held-back options are reported with the reason. Every generated option records its provenance (engine, prompt, seed or generation id, measured values). A measurement is a measurement, not a guarantee: stated error rates and calibration limits are shown where they matter.

### IV. Evidence, Spec First, QA Before Ship
Every new priority starts with a spec in `specs/NNN-short-name/` (what and why, never how). A story is done only when its acceptance scenarios pass on the real running product, on real songs from our own catalogue, with the QA report quoting the SC and FR ids. Claims are verified from the artifact (branch tip, test run, render, null test), never from memory. If code and spec disagree, one is fixed on purpose by PR.

### V. Internal, Owner-Only, Zero New Spend
Studio is an internal, owner-only tool today: no anonymous access, no demo logins, no outside users or their data, and the access model is re-architected before any outside user is allowed in. The in-app language and producer-agent features run on an existing AI subscription, never per-call API billing. Metered use of already-funded APIs is allowed, with a visible per-request cap. Any card charge, plan upgrade, new paid cloud resource, public exposure or outside user is an owner decision.

### VI. Data, Models and Licences
The product never trains on scraped artist audio. Internal adapters trained on our own music may serve our own work through the internal engine only, and are never baked into a product model or used for a route meant to be product-safe. Reference clips are used only with an ownership attestation or from the artist's own project. Licences for any model or dataset are an owner decision before outside use. Secrets are referenced by name only from a secrets manager; no key, token or password value is written anywhere.

### VII. Machine Etiquette and Process Safety
Shared GPU and DAW machines are single-tenant: claim them with a lock before use and release it when done. Never close a person's apps on a shared machine without an explicit instruction. Stop or kill processes only by exact process ID or the port you started, never by name or pattern. Bulk renders and large intermediates go to dedicated storage, never the build machine; check free space before every pull and stop below a safe threshold.

### VIII. The Product Does Not Override the Artist's Ear (the owner's locked music rules, as they apply to what Studio generates)
Studio never puts describing words in a vocal: a vocal request produces wordless sound unless the artist supplies words. No ducking is applied unless the artist asks. Endings end on natural decay; no hard cut or fade is imposed unless requested. A part is one cohesive generation, not a collage. No raspy, detuned or buzzy lead is introduced by default. The artist's stated tempo wins over detection. Studio never calls a lane a voice when it is not. Musical judgement is the artist's ear; Studio reports measurements and leaves taste to the artist.

## Additional Constraints

- **Brain and budget (2026-10-02)**: the team runs on one AI provider; a budget guard pauses work near the usage limit; commit often. Never switch provider just to keep working.
- **Writing**: no em dashes or en dashes anywhere (code, copy, specs, commits, PRs, ADRs). Plain hyphens, colons or commas only.
- **Mocks match live shapes**: frontend fixtures are captured from a real backend (2026-10-07).
- **Tests**: fixtures are always tracked; a missing fixture fails its test; parallel test runs use separate basetemp dirs.
- **Tenant isolation**: every by-id read and operation is tenant-scoped (ADR, 2026-10-03).

## Development Workflow

1. Constitution (this file), then per priority: Specify (PM agent), Clarify (the PM resolves from the knowledge base, briefs and decision log; at most ONE owner question, with a recommendation), the owner's feature-level yes, Plan with Constitution Check (manager agent), Tasks, Analyze, Implement (developer agents, story by story, branch and PR), Verify (QA agent).
2. A developer who finds the spec wrong stops and tells the manager, who amends the spec by PR first.
3. The manager agent reviews every PR for drift from the spec and the preservation contract, merges, deploys the internal tool after QA, and checks it live.
4. The board mirrors the spec: one epic card per spec, one story card per user story, tasks as a checklist in `tasks.md`.
5. docs/DECISIONS.md is the running decision log (date, decision, why, who); real architecture decisions get a short ADR in `docs/adr`.

## Governance

This constitution supersedes other practice in this repository. Amendments are made by PR, reviewed by the manager agent, and logged in docs/DECISIONS.md; amendments that touch Principles I, II, V or VI also need the owner's approval. Every PR and review verifies compliance. Complexity must be justified in the plan.

**Version**: 0.1.0-draft | **Ratified**: pending | **Last Amended**: 2026-10-09
