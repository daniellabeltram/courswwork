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

## Runaway protection

Every agent has limits so it can't run for too long or spend too much. The limits are sized from a real run: the top-10 targets search took 77 tool calls and about 10 minutes.

| Agent | Max turns (Claude Code) | Web searches | Target time | Session budget / time limit (Managed Agents) |
|---|---|---|---|---|
| `ma-deal-lead` | 50 | 25 | 20 min | $20 / 30 min, shared by every specialist it consults |
| `deal-sourcing-analyst` | 80 | 60 | 20 min | $10 / 30 min |
| `valuation-analyst`, `qoe-accountant` | 30 | 10 / 6 | 15 min | $8 / 20 min |
| `ma-tax-advisor`, `ma-attorney`, `employment-benefits-counsel` | 20 | 10 | 10 min | $5 / 15 min |
| `antitrust-counsel` | 25 | 12 | 10 min | $5 / 15 min |
| `trade-show-industry-expert`, `experiential-agency-expert`, `event-tech-expert` | 25 | 15 | 10 min | $3 / 15 min |
| `pe-operating-partner`, `investment-banker`, `integration-lead`, `labor-relations-expert` | 20 | 8 / 8 / 6 / 12 | 8 min | $3 / 12 min |

How the limits work:

- **Hard turn cap (Claude Code):** `maxTurns` in each subagent file. At the cap, Claude Code stops the agent and returns its work marked as partial. Claude can resume it if more is needed.
- **Hard dollar cap (Managed Agents):** each agent's `max_session_budget_usd`. `run_session.py` sets it as the session budget. The platform pauses the session when list-price spend reaches it (counting tokens, web searches at $10 per 1,000, and running time).
- **Time limit (Managed Agents):** each agent's `max_session_minutes`. `run_session.py` sends an interrupt at the limit, so the agent stops at the next safe point.
- **Work budget in every prompt:** each agent knows its tool-call, search and time budget, and is told to plan before searching, stop once more research wouldn't change the answer, retry a failing page only once, never loop, and deliver a partial answer on time rather than nothing.
- **Smaller pages:** in Managed Agents, each fetched web page is capped at 20,000 tokens of text so one long page can't flood an agent's context.
- **Team limits:** `ma-deal-lead` consults only the two to five specialists a decision needs. It starts at most one workflow run per request and gives every run a one-hour time limit, well under the platform's 24-hour default.
- **Least privilege:** only the agents that produce files (`ma-deal-lead`, `deal-sourcing-analyst`, `valuation-analyst`, `qoe-accountant`, `integration-lead`) can write files, and only `valuation-analyst` and `qoe-accountant` can run code. In unattended Managed Agents runs, `run_session.py` denies any tool call the server flags for approval.

The budgets are list-price ceilings set well above a typical run. Tune them from real sessions' `usage.list_cost` in the Console. To change a limit, edit `maxTurns` or the work-limits lines in the agent's `.claude/agents/` file, or `SESSION_LIMITS` in `scripts/sync_managed_agents.py`, then re-run the sync script.

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

**4. Run a session with the limits applied.** `run_session.py` reads the agent and environment IDs from `claude-lock.json`, sets the agent's dollar budget, interrupts it at its time limit, and prints the answer:

```bash
pip install anthropic pyyaml
```

```bash
cd managed-agents && python3 run_session.py ma-deal-lead "Screen Example Co as an add-on for GES."
```

Use `ma-deal-lead` for full deal questions, or any specialist's name for a focused question. Your app can use the same pattern: create the session with a `budget`, stream events, and send `user.interrupt` at the time limit.

### Settings to know about

- **Model:** each agent uses the model and effort from its `.claude/agents/` file (see *Why each agent uses its model*). When `ma-deal-lead` delegates, each specialist runs on its own model.
- **Team mode is on:** `ma-deal-lead` can delegate to the 14 specialists and only to them. It can also start **workflow runs**, which run many specialist copies in parallel (for example, screening a long list of targets). Every agent in a run uses tokens. `run_session.py` always sets a session budget. To turn workflow runs off, change `workflows` to `{"type": "disabled"}` in the sync script.
- **Tool approvals:** tools run under the `auto` permission policy. The server lets low-risk calls run, blocks high-risk ones, and pauses on unclear ones for your app to approve.
- **Networking:** the environment allows unrestricted outbound access so agents can research any target's public website. To lock it down, switch `ges-ma-cloud.yaml` to `limited` networking and list approved hosts.
- **Confidential data:** don't upload real data-room material until GES has approved the data handling. Managed Agents is not eligible for Zero Data Retention.
