#!/usr/bin/env python3
"""Run one GES M&A agent session with runaway protection.

Usage (from the managed-agents/ directory, after `ant apply`):

    python3 run_session.py ma-deal-lead "Screen Example Co as an add-on for GES."

Limits come from the agent file's metadata (set in scripts/sync_managed_agents.py):
- max_session_budget_usd: a hard dollar cap on the session. The platform pauses
  the session (stop_reason budget_reached) once list-price spend reaches it. When
  ma-deal-lead delegates, one budget covers every specialist it consults.
- max_session_minutes: a wall-clock limit. At the limit this script sends an
  interrupt, so the agent stops at the next safe point, then waits a short
  grace period before giving up on the stream.

Requires: pip install anthropic pyyaml, plus credentials (`ant auth login` or
ANTHROPIC_API_KEY).
"""
import json
import pathlib
import sys
import threading
import time

import anthropic
import yaml

HERE = pathlib.Path(__file__).resolve().parent
GRACE_SECONDS = 120  # how long to wait for the agent to stop after an interrupt


def load_limits(agent_name: str):
    text = (HERE / "agents" / f"{agent_name}.md").read_text()
    meta = yaml.safe_load(text.split("---\n")[1])["metadata"]
    return int(meta["max_session_budget_usd"]), int(meta["max_session_minutes"])


def load_ids(agent_name: str):
    lock = json.loads((HERE / "claude-lock.json").read_text())["resources"]
    agent_id = lock[f"./agents/{agent_name}.md"]["id"]
    env_id = lock["./environments/ges-ma-cloud.yaml"]["id"]
    return agent_id, env_id


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    agent_name, prompt = sys.argv[1], sys.argv[2]
    budget_usd, max_minutes = load_limits(agent_name)
    agent_id, env_id = load_ids(agent_name)

    client = anthropic.Anthropic()
    session = client.beta.sessions.create(
        agent=agent_id,
        environment_id=env_id,
        title=f"{agent_name}: {prompt[:60]}",
        budget={
            "type": "limit",
            # minor units (cents) as an integer string: "2000" = $20.00
            "max_list_cost": {"amount": str(budget_usd * 100), "currency": "USD"},
        },
    )
    print(f"Session {session.id}: budget ${budget_usd}, time limit {max_minutes} min",
          file=sys.stderr)

    interrupted = threading.Event()

    def interrupt():
        interrupted.set()
        print(f"\n[time limit of {max_minutes} min reached: interrupting]", file=sys.stderr)
        client.beta.sessions.events.send(
            session_id=session.id, events=[{"type": "user.interrupt"}]
        )

    timer = threading.Timer(max_minutes * 60, interrupt)
    timer.daemon = True
    hard_stop = time.monotonic() + max_minutes * 60 + GRACE_SECONDS

    try:
        with client.beta.sessions.events.stream(session_id=session.id) as stream:
            client.beta.sessions.events.send(
                session_id=session.id,
                events=[{"type": "user.message",
                         "content": [{"type": "text", "text": prompt}]}],
            )
            timer.start()
            for event in stream:
                if event.type == "agent.message":
                    for block in event.content:
                        if block.type == "text":
                            print(block.text, end="", flush=True)
                elif (event.type in ("agent.tool_use", "agent.mcp_tool_use")
                      and event.evaluated_permission == "ask"):
                    # Unattended run: deny anything the server couldn't clear as safe.
                    client.beta.sessions.events.send(
                        session_id=session.id,
                        events=[{"type": "user.tool_confirmation",
                                 "tool_use_id": event.id, "result": "deny"}],
                    )
                elif event.type == "session.status_idle":
                    reason = event.stop_reason.type
                    if reason == "requires_action":
                        continue  # waiting on a confirmation we just sent
                    if reason == "budget_reached":
                        print(f"\n[budget of ${budget_usd} reached: session paused]",
                              file=sys.stderr)
                    break
                elif event.type == "session.status_terminated":
                    break
                if interrupted.is_set() and time.monotonic() > hard_stop:
                    print("\n[agent did not stop after the interrupt: giving up on the "
                          f"stream; check session {session.id} in the Console]",
                          file=sys.stderr)
                    break
    finally:
        timer.cancel()
    print(f"\n[done: session {session.id}]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
