#!/usr/bin/env python3
"""Regenerate the per-harness adapters from the single source of truth in roles/.

Source of truth:
  roles/<id>.md          one file per role: small frontmatter + the role prompt
  roles/_shared-rules.md the team rules appended to every role adapter

Generated (do not edit by hand):
  .claude/agents/<id>.md          Claude Code subagents
  .github/agents/<id>.agent.md    GitHub Copilot custom agents
  .codex/agents/<id>.toml         OpenAI Codex custom agents
  The block between the GENERATED markers in AGENTS.md and
  .github/copilot-instructions.md (the shared team rules)

Usage:
  python3 scripts/build_adapters.py          write everything
  python3 scripts/build_adapters.py --check  exit 1 if anything is out of date
Standard library only.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ROLES = ROOT / "roles"
SHARED = ROLES / "_shared-rules.md"
BEGIN = "<!-- BEGIN GENERATED: shared-rules (edit roles/_shared-rules.md, then run scripts/build_adapters.py) -->"
END = "<!-- END GENERATED: shared-rules -->"
NOTICE = "GENERATED from roles/{src} by scripts/build_adapters.py. Edit the source, not this file."


def parse_role(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise SystemExit(f"{path}: missing frontmatter")
    head, body = text[4:].split("\n---\n", 1)
    meta = {}
    for line in head.splitlines():
        if line.strip():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    for key in ("id", "title", "description", "targets"):
        if key not in meta:
            raise SystemExit(f"{path}: frontmatter needs '{key}'")
    meta["targets"] = [t.strip() for t in meta["targets"].split(",") if t.strip()]
    return meta, body.strip() + "\n"


def full_prompt(body, shared):
    return f"{body}\n{shared}"


def claude_agent(meta, prompt, src):
    lines = ["---", f"name: {meta['id']}", f"description: {json.dumps(meta['description'])}"]
    if meta.get("claude_model"):
        lines.append(f"model: {meta['claude_model']}")
    tools = meta.get("claude_tools", "*")
    # IMPORTANT: never write a phrase like "All tools" here. It is parsed as
    # literal tool names and binds zero tools. Omitting the line grants all.
    if tools and tools != "*":
        lines.append(f"tools: {tools}")
    lines += ["---", "", f"<!-- {NOTICE.format(src=src)} -->", "", prompt]
    return "\n".join(lines)


def copilot_agent(meta, prompt, src):
    lines = ["---", f"name: {meta['id']}", f"description: {json.dumps(meta['description'])}"]
    tools = meta.get("copilot_tools", "*")
    if tools and tools != "*":
        items = ", ".join(json.dumps(t.strip()) for t in tools.split(","))
        lines.append(f"tools: [{items}]")
    # No model line: pick the model in the Copilot UI (or add a model line
    # with the exact name your Copilot surface lists).
    lines += ["---", "", f"<!-- {NOTICE.format(src=src)} -->", "", prompt]
    text = "\n".join(lines)
    if len(prompt) > 30000:
        raise SystemExit(f"{src}: Copilot agent prompt exceeds 30,000 characters")
    return text


def codex_agent(meta, prompt, src):
    if "'''" in prompt:
        raise SystemExit(f"{src}: prompt contains ''' which breaks the TOML literal string")
    name = meta["id"].replace("-", "_")
    return (
        f"# {NOTICE.format(src=src)}\n"
        f"name = {json.dumps(name)}\n"
        f"description = {json.dumps(meta['description'])}\n"
        f"developer_instructions = '''\n{prompt}'''\n"
    )


def splice(path, shared):
    text = path.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        raise SystemExit(f"{path}: missing GENERATED markers")
    pre, rest = text.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    return f"{pre}{BEGIN}\n{shared}{END}{post}"


def build():
    shared = SHARED.read_text(encoding="utf-8").strip() + "\n"
    out = {}
    for path in sorted(ROLES.glob("*.md")):
        if path.name.startswith("_"):
            continue
        meta, body = parse_role(path)
        prompt = full_prompt(body, shared)
        rid = meta["id"]
        if rid == "orchestrator" and [t for t in meta["targets"] if t not in ("", "none")]:
            raise SystemExit("orchestrator must not be generated as an agent (targets: none); see INSTALL.md")
        if "claude" in meta["targets"]:
            out[ROOT / ".claude/agents" / f"{rid}.md"] = claude_agent(meta, prompt, path.name)
        if "copilot" in meta["targets"]:
            out[ROOT / ".github/agents" / f"{rid}.agent.md"] = copilot_agent(meta, prompt, path.name)
        if "codex" in meta["targets"]:
            out[ROOT / ".codex/agents" / f"{rid}.toml"] = codex_agent(meta, prompt, path.name)
    for target in (ROOT / "AGENTS.md", ROOT / ".github/copilot-instructions.md"):
        out[target] = splice(target, shared)
    return out


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    for path, content in build().items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            stale.append(path.relative_to(ROOT))
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
    if check and stale:
        print("Out of date (run scripts/build_adapters.py):")
        for p in stale:
            print(f"  {p}")
        return 1
    print("Up to date." if check else f"Wrote {len(stale)} changed file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
