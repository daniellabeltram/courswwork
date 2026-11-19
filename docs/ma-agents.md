# GES M&A Expert Agents

Fifteen AI agents, one for each of the most important expert roles in `ma-expert-roles.md`. Each agent knows GES's situation (Truelink ownership, the 2Heads and CSG Creative deals, Freeman as main rival) and answers in the same executive memo format:

1. **Bottom line**
2. **Analysis**, with numbers shown
3. **Risks and red flags**, each rated High, Medium or Low
4. **What we still need**
5. **Confidence and assumptions**

Every agent shares the same format and ground rules, so the M&A app can display and combine their answers consistently.

> ⚠️ These agents support executive decisions; they don't replace licensed advisors. The legal, tax and accounting agents say so in their answers when a conclusion needs sign-off from a licensed attorney or CPA.

## The 15 agents

| Agent | Role | Model | Ask it about |
|---|---|---|---|
| `ma-deal-lead` | M&A Deal Lead (Corporate Development) | Opus 5.5 | **Start here.** Should we do this deal? Combines the specialists into one recommendation and investment committee memo |
| `pe-operating-partner` | Private Equity Operating Partner | Sonnet 5.5 | Truelink's view, value creation, exit, debt capacity, MOIC/IRR |
| `investment-banker` | Investment Banker / M&A Advisor | Sonnet 5.5 | Approaching founders, auction tactics, offer and LOI terms, timelines |
| `valuation-analyst` | Valuation & Financial Modeling Analyst | Opus 5.5 | What it's worth, what to pay, earn-outs, sensitivities (can run Python) |
| `qoe-accountant` | Quality of Earnings Accountant | Opus 5.5 | Are the earnings real? Add-backs, working capital, show-rotation normalization (can run Python) |
| `ma-tax-advisor` | M&A Tax Advisor | Opus 5.5 | Asset vs. stock, rollover, earn-out tax, cross-border tax |
| `integration-lead` | Post-Merger Integration Lead | Sonnet 5.5 | Stand-alone vs. fold-in, 100-day plan, synergies, retention |
| `trade-show-industry-expert` | Trade Show & Exhibition Industry Expert | Sonnet 5.5 | Contractor targets, organizer and venue contracts, competitors, international markets |
| `experiential-agency-expert` | Experiential Agency & Exhibit House Expert | Sonnet 5.5 | Agency economics, client concentration, creative talent |
| `event-tech-expert` | Event Technology Expert | Sonnet 5.5 | Software targets, SaaS metrics, tech diligence, data privacy |
| `labor-relations-expert` | Labor Relations & Union Expert | Sonnet 5.5 | Union agreements, jurisdictions, labor cost, strike risk |
| `ma-attorney` | M&A Corporate Attorney | Opus 5.5 | LOI and purchase agreement terms, indemnities, change-of-control clauses, IP |
| `antitrust-counsel` | Antitrust & Competition Counsel | Opus 5.5 | Buying competitors, filings, overlaps, clean teams |
| `employment-benefits-counsel` | Labor, Employment & Benefits Counsel | Opus 5.5 | Pension withdrawal liability, non-competes, WARN, TUPE, retention |
| `deal-sourcing-analyst` | Deal Sourcing & Market Research Analyst | Sonnet 5.5 (medium effort) | Finding and profiling targets, market maps, fit scores |

## Why each agent uses its model

Each agent runs on the least expensive model that does its job well. Opus 5.5 costs about twice as much as Sonnet 5.5 ($4 vs. $2 per million input tokens, $20 vs. $10 output).

| Model | Agents | Why |
|---|---|---|
| **Claude Opus 5.5**, high effort | `ma-deal-lead`, `valuation-analyst`, `qoe-accountant`, `ma-tax-advisor`, `ma-attorney`, `antitrust-counsel`, `employment-benefits-counsel` | Mistakes here are expensive and the reasoning is hard: setting the price, spotting earnings that won't repeat, multi-country tax structures, contract and antitrust exposure, hidden pension liabilities, and weighing all the specialists' input into one go/no-go call. |
| **Claude Sonnet 5.5**, high effort | `pe-operating-partner`, `investment-banker`, `integration-lead`, `trade-show-industry-expert`, `experiential-agency-expert`, `event-tech-expert`, `labor-relations-expert` | These apply industry knowledge and proven frameworks (deal process, integration plans, agency economics, union inventories). Sonnet handles this well at half the cost. Their numbers and legal points go to the Opus agents for the final call. |
| **Claude Sonnet 5.5**, medium effort | `deal-sourcing-analyst` | Many web lookups and structured profiles. Medium effort keeps long research runs fast and cheap while still checking facts like ownership. |
| Claude Haiku 5.5 | none | Considered and not used. Every agent here advises executives or has to check facts, which needs more judgment than Haiku gives. Haiku would suit future bulk jobs, such as pulling fields out of hundreds of documents. |
| Claude Fable 5.2 | none | Anthropic's most capable model, but twice the cost of Opus and slower per answer. Worth testing on `ma-deal-lead` for final investment committee memos only if Opus's answers fall short. |

To change an agent's model, edit the `model` and `effort` lines in its `.claude/agents/` file, then run `python3 scripts/sync_managed_agents.py`.

## Two versions of the same agents

The agents come in two formats, built from the same prompts:

| | **Claude Code subagents** | **Claude Managed Agents** |
|---|---|---|---|
| Location | `.claude/agents/*.md` | `managed-agents/agents/*.md` + `managed-agents/environments/ges-ma-cloud.yaml` |
| Best for | You, researching and prototyping in Claude Code today | The M&A app itself: your code calls them through the Claude API |
| Who runs them | Claude Code on your machine or in a cloud session | Anthropic's managed infrastructure (beta) |
| Coordination | Your main Claude Code conversation picks which specialists to call | `ma-deal-lead` is a coordinator that delegates to the other 14 itself |

**The source of truth is `.claude/agents/`.** The Managed Agents files are generated from it. To change an agent, edit its file in `.claude/agents/`, then run:

```bash
python3 scripts/sync_managed_agents.py
```

(The script needs PyYAML: `pip install pyyaml`.)

## Using the Claude Code subagents

Open this repository in Claude Code. The agents load automatically from `.claude/agents/`. Claude picks the right specialist from your question, or you can name one:

```text
Use the valuation-analyst to value a 60-person experiential agency with $4M EBITDA and an earn-out.
```

```text
Ask the antitrust-counsel and trade-show-industry-expert whether buying a regional contractor in Chicago creates overlap problems.
```

```text
Have the ma-deal-lead write an investment committee memo for acquiring Example Co, consulting whichever specialists it needs.
```

Each agent runs on the model listed above. They can read the repo (including `docs/ges-company-research.md`), search the web, and write files such as memos. The valuation and QoE agents can also run Python for calculations.

## Using the Managed Agents (for the app)

Managed Agents are in beta. Anthropic hosts the agent loop and a sandbox per session. Sessions are billed for runtime as well as tokens, and session history is kept until you delete it.

**1. Install the `ant` CLI** (1.40.0 or later, needed because `ma-deal-lead` references its specialists by file path) and log in:

```bash
ant auth login
```

**2. Preview what will be created** (changes nothing):

```bash
cd managed-agents && ant apply --dry-run agents environments
```

**3. Create the agents and environment** once you've reviewed the plan:

```bash
cd managed-agents && ant apply agents environments
```

This creates 15 agents and one cloud environment. It writes their IDs to `managed-agents/claude-lock.json`, which you should commit. Re-running `ant apply` after an edit updates the agents in place and creates a new version, rather than creating duplicates.

**4. Start a session from your app** with the IDs in `claude-lock.json`. For example, from the shell:

```bash
cd managed-agents
AGENT_ID=$(jq -r '.resources["./agents/ma-deal-lead.md"].id' claude-lock.json)
ENV_ID=$(jq -r '.resources["./environments/ges-ma-cloud.yaml"].id' claude-lock.json)
SID=$(ant beta:sessions create --agent "$AGENT_ID" --environment-id "$ENV_ID" --title "Deal screen" --transform id -r)
ant beta:sessions:events send --session-id "$SID" \
  --event '{type: user.message, content: [{type: text, text: "Screen Example Co as an add-on for GES."}]}'
ant beta:sessions:events stream --session-id "$SID"
```

Start sessions with `ma-deal-lead` for full deal questions, or with any single specialist's agent ID for a focused question.

### Settings to know about

- **Model:** each agent uses the model and effort from its `.claude/agents/` file (see *Why each agent uses its model*). When `ma-deal-lead` delegates, each specialist runs on its own model.
- **Team mode is on:** `ma-deal-lead` can delegate to the 14 specialists and only to them. It can also start **workflow runs**, which run many specialist copies in parallel (for example, screening a long list of targets). Every agent in a run uses tokens, so **set a session budget** when you create sessions with `ma-deal-lead`. To turn workflow runs off, change `workflows` to `{"type": "disabled"}` in the sync script.
- **Tool approvals:** tools run under the `auto` permission policy. The server lets low-risk calls run, blocks high-risk ones, and pauses on unclear ones for your app to approve.
- **Networking:** the environment allows unrestricted outbound access so agents can research any target's public website. To lock it down, switch `ges-ma-cloud.yaml` to `limited` networking and list approved hosts.
- **Confidential data:** don't upload real data-room material until GES has approved the data handling. Managed Agents is not eligible for Zero Data Retention.
