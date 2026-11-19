#!/usr/bin/env python3
"""Generate Claude Managed Agents files from the Claude Code subagents.

Source of truth: .claude/agents/*.md (Claude Code subagent files).
Output:         managed-agents/agents/*.md (files for `ant apply`).

Edit a subagent in .claude/agents/, then re-run:

    python3 scripts/sync_managed_agents.py

Each subagent's `model` and `effort` frontmatter carry over to its
Managed Agent. Requires PyYAML (pip install pyyaml).
"""
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / ".claude" / "agents"
DST = ROOT / "managed-agents" / "agents"

COORDINATOR = "ma-deal-lead"

# Runaway limits that only apply to Managed Agents (Claude Code enforces
# `maxTurns` from the subagent file instead). The app reads these from each
# agent's metadata: run_session.py sets the session's dollar budget and
# interrupts it at the time limit. Budgets are list-price USD ceilings, set
# well above a typical run; tune them from real sessions' usage.list_cost.
SESSION_LIMITS = {
    # name: (max session budget USD, max session minutes)
    "ma-deal-lead": (20, 30),
    "deal-sourcing-analyst": (10, 30),
    "valuation-analyst": (8, 20),
    "qoe-accountant": (8, 20),
    "ma-tax-advisor": (5, 15),
    "ma-attorney": (5, 15),
    "antitrust-counsel": (5, 15),
    "employment-benefits-counsel": (5, 15),
    "pe-operating-partner": (3, 12),
    "investment-banker": (3, 12),
    "integration-lead": (3, 12),
    "trade-show-industry-expert": (3, 15),
    "experiential-agency-expert": (3, 15),
    "event-tech-expert": (3, 15),
    "labor-relations-expert": (3, 12),
}

# Cap on text from any one fetched web page entering an agent's context.
WEB_FETCH_MAX_TOKENS = 20000


def toolset_for(claude_code_tools: str):
    """Mirror the subagent's Claude Code tool list onto the Managed Agents toolset."""
    allowed = {x.strip() for x in claude_code_tools.split(",")}
    configs = [
        {"name": "web_search", "enabled": "WebSearch" in allowed},
        {"name": "web_fetch", "enabled": "WebFetch" in allowed,
         "max_content_tokens": WEB_FETCH_MAX_TOKENS},
        {"name": "bash", "enabled": "Bash" in allowed},
        {"name": "write", "enabled": "Write" in allowed},
        {"name": "edit", "enabled": "Write" in allowed},
    ]
    return [{
        "type": "agent_toolset_20260401",
        "default_config": {"permission_policy": {"type": "auto"}},
        "configs": configs,
    }]


COORDINATOR_NOTE = """
## Working with the specialist team

You can delegate to each specialist listed above by name. Send each one a
self-contained task with the facts it needs, then combine their reports into
your recommendation. When a task covers many targets at once (for example,
screening a long list of companies, or profiling every contractor in a
region), start a workflow run that assesses them in parallel and combines the
results. For a single deal question, consult the specialists directly
instead of starting a run.

Limits on workflow runs: start at most one run per request, and give every
run a one-hour time limit. If a run fails or is cut short, report what it
finished and list what it did not cover rather than starting it again.
"""


def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    _, fm, body = text.split("---\n", 2)
    return yaml.safe_load(fm), body.lstrip("\n")


def main() -> int:
    sources = sorted(SRC.glob("*.md"))
    if not sources:
        print(f"No subagents found in {SRC}", file=sys.stderr)
        return 1

    DST.mkdir(parents=True, exist_ok=True)
    names = []
    parsed = {}
    for path in sources:
        meta, body = split_frontmatter(path.read_text())
        names.append(meta["name"])
        parsed[meta["name"]] = (meta, body)

    specialists = [n for n in names if n != COORDINATOR]

    for name, (meta, body) in parsed.items():
        title = body.splitlines()[0].lstrip("# ").strip()
        agent = {
            "name": f"GES {title}",
            "description": meta["description"],
            "model": {"id": meta["model"], "effort": meta["effort"]},
            "tools": toolset_for(meta["tools"]),
            "metadata": {
                "claude_code_subagent": name,
                "customer": "GES",
                "max_session_budget_usd": str(SESSION_LIMITS[name][0]),
                "max_session_minutes": str(SESSION_LIMITS[name][1]),
            },
        }
        if name == COORDINATOR:
            roster = [f"./{s}.md" for s in specialists]
            agent["multiagent"] = {
                "type": "multiagent_20261001",
                "subagents": {
                    "type": "enabled",
                    "predefined_agents": list(roster),
                    "inline_agents": {"type": "disabled"},
                },
                "workflows": {
                    "type": "enabled",
                    "predefined_agents": list(roster),
                    "inline_agents": {"type": "disabled"},
                },
            }
            body = body.rstrip() + "\n" + COORDINATOR_NOTE

        out = (
            "---\n"
            "# Generated by scripts/sync_managed_agents.py from "
            f".claude/agents/{name}.md. Edit the source, not this file.\n"
            + yaml.safe_dump(agent, sort_keys=False, width=1000)
            + "---\n\n"
            + body
        )
        (DST / f"{name}.md").write_text(out)
        print(f"wrote managed-agents/agents/{name}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
