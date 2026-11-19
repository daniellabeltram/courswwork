# Expert Roles for a GES M&A Application

*Prepared November 19, 2026. These are the roles needed to design and run a world-class M&A decision-support application for GES (Global Experience Specialists). See `ges-company-research.md` for company background.*

> **How to use this list:** A small app doesn't need all of these people on staff. Most domain and legal experts can be part-time advisors you interview while designing the app. The 15 roles marked ⭐ are built as AI agents in this repository (see `ma-agents.md`).

---

## 1. M&A and deal experts (core advisors)

| Role | Why GES needs it | What they shape in the app |
|---|---|---|
| ⭐ **Corporate development / buy-side M&A lead** (agent: `ma-deal-lead`) | GES is a serial acquirer; this person knows how deals actually move | Pipeline stages, decision gates, investment committee memo template, what executives need to see to decide |
| ⭐ **Private equity operating partner** (agent: `pe-operating-partner`) | Truelink is running a buy-and-build and will want to sell GES around 2029–2031 | Value-creation tracking, sponsor reporting, effect of each deal on the exit |
| ⭐ **Investment banker / M&A advisor** (agent: `investment-banker`) | Knows how sale processes, auctions and founder negotiations work | Deal milestones (non-binding offer, letter of intent, exclusivity) and bid tracking |
| ⭐ **Valuation / financial modeling analyst** (agent: `valuation-analyst`) | Executives need to know what a target is worth and what to pay | Valuation engine: multiples, comparable deals, DCF, earnings impact, debt capacity, earn-outs |
| ⭐ **Quality-of-earnings accountant** (agent: `qoe-accountant`) | Event revenue is lumpy (shows that don't run every year) and COVID distorted history | Earnings normalization tools and working-capital targets |
| ⭐ **M&A tax advisor** (agent: `ma-tax-advisor`) | GES works in the US, Canada, UK, Middle East and India; deal structure has big tax effects | Structure options and after-tax returns in the model |
| ⭐ **Post-merger integration lead** (agent: `integration-lead`) | GES keeps founders and brands, so integration is delicate | 100-day plans, workstreams, synergy tracking, retention dashboards |
| **Planning and analysis (FP&A) analyst** | Someone has to measure whether promised synergies happen | Plan-versus-actual reporting for each acquired company |

## 2. Event industry experts (specific to GES)

| Role | Why | What they shape in the app |
|---|---|---|
| ⭐ **Trade show contractor operations veteran** (agent: `trade-show-industry-expert`) | Knows what makes a good official show contractor, and how organizers and venues pick them | Fit-scoring criteria, operational diligence, contract renewal tracking |
| ⭐ **Experiential agency expert** (agent: `experiential-agency-expert`) | Agencies (the Spiro side) have different economics: utilization, client concentration, creative talent | Health metrics for agency targets |
| **Show organizer / association expert** | Organizers pick contractors; they know contract terms and bid cycles | Contract and renewal tracking, cross-sell potential *(covered by the trade show agent)* |
| ⭐ **Event technology expert** (agent: `event-tech-expert`) | Truelink wants more tech-enabled services; software is valued on recurring revenue | A separate scorecard for software targets |
| ⭐ **Labor relations / union expert** (agent: `labor-relations-expert`) | Show-floor labor is heavily unionized; every contractor GES buys brings union contracts | Union diligence fields and risk flags |
| **International market advisors** (Europe/UK, Gulf states, India) | International acquisitions are a likely growth path | Region-specific diligence checklists *(partly covered by the trade show and tax agents)* |

## 3. Legal and compliance

| Role | Why |
|---|---|
| ⭐ **M&A corporate attorney** (agent: `ma-attorney`) | Drafts letters of intent and purchase agreements; owns the master diligence checklist. Also covers change-of-control clauses in organizer and venue contracts, and agency IP |
| ⭐ **Antitrust / competition counsel** (agent: `antitrust-counsel`) | Critical if GES buys competitors: GES and Freeman dominate the official-contractor market. Covers pre-merger filings, overlap analysis, gun-jumping and clean teams |
| ⭐ **Labor, employment and benefits counsel** (agent: `employment-benefits-counsel`) | Union successorship, layoff-notice rules, non-competes, and **multiemployer pension withdrawal liability**, a large hidden cost in union-heavy deals |
| **Commercial contracts counsel** | Change-of-control clauses in organizer and venue contracts *(covered by `ma-attorney`)* |
| **Data privacy counsel** | GES's Visit and onPeak hold attendee data under GDPR and CCPA; the app holds confidential deal data |
| **Intellectual property counsel** | Agency value sits in creative IP, client work rights and brands *(partly covered by `ma-attorney`)* |
| **Deal insurance broker** | Representations-and-warranties insurance is standard in private equity add-on deals |

## 4. Other diligence specialists (often outside firms)

- **IT and cybersecurity diligence**: systems, breach history, integration cost *(partly covered by `event-tech-expert`)*
- **HR, compensation and culture diligence**: key-person risk, retention bonuses, earn-out design
- **Commercial / market diligence consultant**: market size, competitor maps, customer interviews
- **Health, safety, real estate and environmental**: warehouses, equipment fleets, show-floor safety record

## 5. Data and research

- ⭐ **Deal-sourcing / market research analyst** (agent: `deal-sourcing-analyst`): builds and maintains the target list and market maps
- **Data vendor relationships** (PitchBook, Capital IQ, Crunchbase or similar)
- **Business analyst**: turns expert input into app requirements. This is likely your most important human hire.

## 6. Team to build the app

| Role | Notes |
|---|---|
| **Product manager** (ideally with fintech or deal-tool experience) | Owns the roadmap; stays close to the executives |
| **UX designer** | Executives want clear dashboards, not spreadsheets |
| **Full-stack engineers** | |
| **Data engineer** | Connects CRM, data vendors, virtual data rooms and GES's accounting system |
| **Security architect** | Deal data is highly confidential: single sign-on, role-based access, audit logs, clean-team walls when GES evaluates competitors |
| **AI/ML engineer** | Runs the agents in this repo; document summarization, contract term extraction |
| **QA engineer** | |

## 7. People at GES and Truelink to involve (not hires)

- GES CEO (Derek Linde) and CFO
- Business-unit presidents: Jeff Quade (North America), Jason Stead (EMEA), Jeff Stelmach (Spiro)
- GES corporate development or strategy staff
- **Truelink's deal team** (Luke Myers's group), who likely co-own acquisition decisions
- The leaders who integrated 2Heads and CSG Creative: the best source of lessons learned

## Smallest starting team

1. Buy-side M&A practitioner with private equity add-on experience
2. Valuation / financial modeling analyst
3. M&A attorney, with an antitrust advisor on call
4. Trade show industry veteran
5. Integration lead
6. Product manager / business analyst, with engineers and a security-minded architect

Antitrust, labor counsel and union expertise are the GES-specific risks most likely to be missed. Line them up early.
