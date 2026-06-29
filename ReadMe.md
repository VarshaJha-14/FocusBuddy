# ⚡ FocusBuddy
### AI Co-Pilot for Task Paralysis & Executive Dysfunction

> *"I know exactly what I need to do. I just can't seem to start."*
> — Rohan, Final-Year CS Student (Primary Persona)

> **Live site:** [FocusBuddy](https://focusbuddy-wbo3.onrender.com)

**FocusBuddy** is a full end-to-end PM case study — from zero-to-one product discovery through PRD, responsible AI design, metrics framework, and go-to-market strategy. It explores how conversational AI can break the neurological freeze response that prevents neurodivergent users from initiating tasks.

![Status](https://img.shields.io/badge/Status-Case%20Study%20%7C%20MVP%20Concept-blueviolet)
![Type](https://img.shields.io/badge/Type-Product%20Management%20Portfolio-informational)
![Domain](https://img.shields.io/badge/Domain-AI%20%7C%20Mental%20Health%20%7C%20Productivity-success)

---

## 📌 Table of Contents

- [The Problem](#-the-problem)
- [My Role](#-my-role)
- [Product Overview](#-product-overview)
- [Key Product Decisions & Tradeoffs](#-key-product-decisions--tradeoffs)
- [Feature Prioritization (RICE)](#-feature-prioritization-rice)
- [AI Design & Responsible AI Guardrails](#-ai-design--responsible-ai-guardrails)
- [North Star Metric & KPIs](#-north-star-metric--kpis)
- [A/B Test Design](#-ab-test-design)
- [Go-To-Market Strategy](#-go-to-market-strategy)
- [Wireframes & Prototype](#-wireframes--prototype)
- [What I'd Validate Next](#-what-id-validate-next)
- [Document Index](#-document-index)

---

## 🧠 The Problem

For neurodivergent individuals — and those experiencing situational burnout — the standard productivity stack is broken. Not because users don't know what to do, but because they cannot cross the neurological chasm from **intention to initiation**.

This is **task paralysis**: a biological freeze response triggered by overwhelm, perfectionism, or ambiguity. Existing tools make it worse.

| Tool Type | Example | Why It Fails |
|---|---|---|
| Task managers | Todoist, Linear | Assume the user can already initiate. Add cognitive load. |
| Body doubling | Focusmate, Twitch | Requires scheduling. Unavailable during acute paralysis. |
| ADHD coaching | Coach.me | $150–300/month. Not on-demand. Not scalable. |
| Wellness apps | Calm, Headspace | Address anxiety, not task initiation. |
| General AI | ChatGPT, Claude | Passive. No proactive nudging. Requires a composed prompt. |

**The gap:** No tool intervenes at the exact moment of freeze, inside the channels users already live in, with zero setup friction.

**Market context:** ADHD prevalence among urban Indian college students and young professionals runs 11.4–15.9% — nearly double the global baseline of 5.9% — and over 62% present as the inattentive subtype: no visible hyperactivity, just quietly paralyzed.

---

## 👤 My Role

End-to-end product case study across the full PM lifecycle:

- ✅ Problem discovery & user research synthesis
- ✅ User personas, JTBD, and psychographic profiling
- ✅ PRD, user stories, and acceptance criteria
- ✅ Feature prioritization using RICE framework
- ✅ AI feature design and responsible AI risk mapping
- ✅ North Star Metric definition and KPI framework
- ✅ A/B test design and experimentation plan
- ✅ Freemium pricing strategy and GTM planning
- ✅ Wireframes and Figma prototype

---

## 🚀 Product Overview

**FocusBuddy** is a conversational AI companion that lives inside the tools users already use — Slack, WhatsApp, Discord — and acts as an on-demand executive function co-pilot.

**One-liner:**
> FocusBuddy is the AI co-pilot for people with ADHD and executive dysfunction, breaking the cycle of task paralysis through gentle, conversational nudges that meet users where they already are.

**Jobs-to-Be-Done:**
> When I am frozen in an overwhelming state of task paralysis and drowning in guilt over a looming deadline, I want to immediately offload my unstructured anxiety to a gentle, objective system that isolates a singular, low-stakes micro-action, so that I can break the neurological freeze response and build friction-free momentum without feeling judged.

### How It Works

```
User types/speaks chaotic anxiety dump
         ↓
AI strips emotional noise → identifies core task
         ↓
Single micro-step displayed (ONE step, nothing else)
         ↓
User clicks [Done → Next Step] or [Too Hard / Stuck]
         ↓
If "Too Hard": AI generates an even smaller sub-action
If "Done": momentum builds → next step revealed
         ↓
Completion reward screen: "You started. That's the hardest part."
```

### MVP Feature Set

| Feature | Why It's In Scope |
|---|---|
| Vent-Capture Engine | Lowest-friction entry point — accepts raw, unstructured anxiety dumps |
| Natural Language Sifter | Extracts the real task from emotional noise |
| Single-Step Progressive Interface | Hides all future steps to eliminate anticipatory overwhelm |
| Adaptive Micro-Step Engine | Shrinks tasks past the "Absurdity Threshold" (e.g., "Just open the document") |
| Dynamic Strategy Toggles | Adapts AI tone to cognitive state: Terrified / Bored / Low Energy |
| Dynamic Step Size Calibration | "Too Hard" button triggers automatic downscaling |
| Lightweight Session Feedback | One-tap post-session check-in to measure freeze-break success |

**Intentionally excluded from MVP:** Calendar integrations, productivity dashboards, gamification/streaks, social accountability rooms, historical analytics. Each was excluded deliberately — not by default.

---

## 🧩 Key Product Decisions & Tradeoffs

These are the hardest calls made during the design process, and why.

**1. No streaks. No dashboards. No gamification.**

Every competing ADHD app builds streaks into their retention model. We explicitly rejected this. Streaks create guilt when broken — and guilt is the primary amplifier of executive dysfunction. The psychological cost of a missed day is higher than any retention benefit. FocusBuddy measures success by whether the freeze was broken in the session, not whether the user came back tomorrow.

**2. One step at a time, always — even if we generate ten.**

User research surfaced a consistent pattern: showing even a 3-item checklist during a paralysis episode caused immediate app abandonment. The progressive disclosure isn't a UX flourish — it's the core product mechanism. The AI can plan ten steps internally; the user sees exactly one.

**3. The "Absurdity Threshold" as a design constraint.**

Standard micro-tasks ("Write the introduction") still felt too large to paralyzed users. True initiation only occurred when steps crossed into near-comical smallness: "Just open the document," "Sit down at your desk." This became a hard constraint on the AI's prompt engineering — not a nice-to-have.

**4. Free tier with full core functionality.**

Neurodivergent users experience the "ADHD Tax" — a pattern of buying productivity tools during hyper-focus windows and abandoning them within a week, compounding financial guilt. Charging upfront would kill adoption before trust is established. The free tier must be genuinely useful, not artificially crippled.

**5. Excluded calendar/Jira integrations from MVP.**

High engineering cost, but more importantly: task paralysis doesn't wait for integrations to sync. The fastest path to validating the core initiation hypothesis is a zero-setup, zero-sync text box. Integrations can be added after proving the core mechanism works.

---

## 📊 Feature Prioritization (RICE)

RICE Score = (Reach × Impact × Confidence) / Effort

| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---|---|---|---|---|---|---|
| Single-Step Progressive Interface | 1,000 | 3.0 | 95% | 0.5 | **5,700** | Must-Have |
| Adaptive Micro-Step Engine | 1,000 | 3.0 | 90% | 1.0 | **2,700** | Must-Have |
| Vent-Capture Engine | 900 | 2.0 | 85% | 1.0 | **1,530** | Must-Have |
| Natural Language Sifter | 950 | 2.5 | 85% | 1.5 | **1,346** | Must-Have |
| Lightweight Session Feedback | 700 | 1.0 | 90% | 0.5 | **1,260** | Should-Have |
| Dynamic Strategy Toggles | 550 | 2.0 | 80% | 1.5 | **587** | Should-Have |
| Dynamic Step Size Calibration | 400 | 1.5 | 75% | 1.0 | **450** | Should-Have |
| Full Productivity Dashboard | 300 | 0.5 | 60% | 4.0 | **22.5** | Won't-Have |
| Historical Analytics | 150 | 0.5 | 50% | 3.0 | **12.5** | Won't-Have |
| Public Accountability Rooms | 120 | 1.0 | 40% | 4.0 | **12.0** | Won't-Have |

---

## 🤖 AI Design & Responsible AI Guardrails

### AI Capability Stack

FocusBuddy combines five AI capabilities in sequence:
1. **Conversational AI** — interprets vague, emotional, ungrammatical input
2. **Summarization** — extracts the real task from the anxiety dump
3. **Classification** — identifies cognitive state (overwhelmed / avoiding / low energy)
4. **Personalization Engine** — adapts step size and tone to user's current capacity
5. **AI Agent Workflow** — loops through task initiation and step progression

### AI Workflow

```
[1] User Vent Input → [2] State Appended (cognitive toggle) → [3] LLM (few-shot)
                                                                      ↓
[6] UI Displays Step 1  ← [5] Regex/JSON Guard ← [4] Content Safety Filter
         ↓
[Feedback Loop] → Done / Too Hard / Toggle Change → updates context for next call
```

### Responsible AI Guardrails

| Risk | Potential Impact | Mitigation |
|---|---|---|
| Mental health crisis in vent input | User shares self-harm ideation | Safety keyword intercept → exits AI loop, surfaces iCall / Vandrevala crisis modal. No AI response generated. |
| PII leakage in vent field | Passwords, IDs, credentials exposed | Client-side regex scrubs emails, phone numbers, numeric codes before string reaches API |
| Step size miscalibration | Overly broad first step re-triggers paralysis | Few-shot JSON schema: every step must begin with a physical action verb. "Too Hard" triggers immediate re-generation. |
| Overdependence | User loses autonomous initiation ability | Progressive autonomy: as momentum builds, AI shifts from directive ("Open the document") to open-ended ("What feels right next?") |
| Cultural bias | Western productivity steps misaligned with Indian academic/professional norms | Few-shot templates calibrated for Indian context; hierarchical communication norms accounted for |
| Confidently wrong output | User does unnecessary or incorrect work | All steps framed as suggestions: "Based on what you shared, try this…" Binary feedback on every card |

### AI Transparency Commitments
- Persistent UI label: *"FocusBuddy is an automated AI co-pilot, not a human or clinical tool."*
- Mandatory first-session disclaimer modal before any interaction
- Every step card includes binary feedback: `[✓ Match]` / `[↓ Too Complex]`
- Low-confidence outputs display: *"I had limited context — does this feel right?"*

---

## 📈 North Star Metric & KPIs

### North Star: Task Activation Velocity (TAV)

**Definition:** Average time from "Vent Capture" submission → first `[Done — Next Step]` tap.

**Why this, not "time in app":** For an executive dysfunction tool, success means getting the user *out* of the app and *into* their work as fast as possible. A falling TAV directly proves the freeze response was broken.

### Supporting KPIs

| Metric | What It Measures | Why It Matters |
|---|---|---|
| Micro-Step Completion Rate | % of steps marked Done | Measures AI decomposition accuracy |
| Calibration Trigger Rate | % of sessions where "Too Hard" is clicked on Step 1 | Tracks whether baseline prompts are over-scoping |
| Rescue Success Rate | % of sessions where user completes the full micro-sequence | End-to-end session efficacy |
| 7-Day / 30-Day Cohort Retention | % of users returning weekly | Proves habit formation, not novelty |

### AARRR Funnel

| Stage | User Action | Key Metric |
|---|---|---|
| Acquisition | Visits via community post / referral / short-form video | Sign-Up Conversion Rate |
| **Activation** | Completes first Task Rescue session; marks ≥1 step Done | **First-Time Activation Rate** ← primary MVP focus |
| Retention | Returns for additional sessions after first experience | D7 / D30 Retention Rate |
| Revenue | Upgrades to Premium | Free-to-Paid Conversion, MRR |
| Referral | Shares with community | K-Factor, Invites Sent Per User |

*Revenue is not a primary MVP focus. The objective is to validate whether AI-guided micro-steps successfully improve task initiation before monetizing.*

---

## 🧪 A/B Test Design

### Hypothesis
If we present users with a single blank input field rather than mandatory cognitive state toggles, First-Time Activation Rates will increase by ≥20% — because an overwhelmed brain cannot process multi-choice self-categorization when frozen.

| | **Control (A)** | **Variant (B)** |
|---|---|---|
| UI | Text field + 3 mandatory buttons: [I'm Overwhelmed] / [I'm Avoiding] / [I have Low Energy] | Single text field: *"Type or paste what's hanging over your head right now."* |
| Strategy detection | Explicit user selection | Implicit AI sentiment analysis |
| Hypothesis | Explicit state = better AI output | Less friction = higher activation |

**Test parameters:**
- 50/50 randomized split across all new signups
- 14-day testing window
- Success: ≥20% lift in First-Time Activation Rate, p < 0.05, n ≥ 500 per variant
- If inconclusive at 14 days: extend 7 days, then default to Variant B (lower cognitive load)

---

## 🗺 Go-To-Market Strategy

**Positioning:**
> For overwhelmed minds trapped in task paralysis, FocusBuddy is the zero-friction AI co-pilot that converts mental freeze into physical momentum. Unlike traditional planner apps that make you organize your day, FocusBuddy meets you in your moment of crisis and gives you just your next achievable step.

**Launch channels:**
1. **Organic community seeding** — r/ADHD, r/productivity, neurodivergent Discord servers. Non-promotional. Value-first.
2. **Short-form video** — Raw screen recordings: panic text in → absurdly small step out. TikTok / Reels / YouTube Shorts.
3. **Micro-influencer partnerships** — ADHD coaches and accessibility advocates doing live testing.

**Key message:** *"Stop planning. Stop organizing. Just tell us what you're stuck on, and let's take the first step together."*

### Pricing

| Tier | Price | What's Included |
|---|---|---|
| **Free** | ₹0/month | Unlimited Task Rescue sessions, full micro-step UI, all cognitive toggles, crisis modal |
| **Premium** | ₹399/month | Everything in Free + session history, voice input, Slack/WhatsApp integration, weekly AI pattern summary |
| **Institutional** | ₹120–180/seat/year | Full Premium + admin dashboard, cohort analytics, crisis event reporting, dedicated CSM |

**Pricing rationale:** The "ADHD Tax" — neurodivergent users compulsively buy productivity apps during hyper-focus windows and abandon them within a week, leaving financial guilt. A strong free tier builds trust before asking for commitment. The institutional per-seat price is deliberately set below the cost of a single university counsellor session (₹800–2,000 in urban India), making the ROI case for institutions straightforward.

---

## 🎨 Wireframes & Prototype

The UX is intentionally linear — no sidebars, no dashboards, no notification badges. During an active freeze episode, every extra link is an avoidance pathway.

**Screen flow:**

| Screen | Purpose |
|---|---|
| **1. Vent / Ingest Screen** | "What's hanging over your head right now?" — zero structure required |
| **2. Calming Loading State** | Buffers AI latency; keeps user grounded during processing |
| **3. Step Execution Workspace** | One step. One action. Nothing else visible. |
| **3b. Dynamic Downscale** | "Too Hard" triggers a sub-step below the Absurdity Threshold |
| **4. Completion Reward Screen** | "You started. That's the hardest part." — positive reinforcement loop |

**→ [View Interactive Figma Prototype](https://www.figma.com/make/1SOA9Sv3Z7rGYOuLp15SUB/User-flow-creation?codenode-id=0-9&p=f&t=zSV0PM7Q3cuTu5FH-0&fullscreen=1)**

> 💡 *Add screenshots from your Figma prototype into `/assets/` and embed them here for maximum recruiter impact.*

---

## 🔭 What I'd Validate Next

If this moved into live beta, here's the prioritized validation roadmap:

1. **Does the Absurdity Threshold actually break freezes?** — Track TAV in cohort Week 1. If median TAV > 90 seconds, the steps aren't small enough. Refine few-shot prompt templates.

2. **Does implicit sentiment detection (Variant B) outperform explicit toggles?** — Run the A/B test described above. This directly determines the onboarding UX direction.

3. **Where does the step decomposition fail by task domain?** — Analyze "Too Hard" trigger rates segmented by task category (e.g., studying for exams vs. writing a report). High rates in specific domains flag prompt engineering gaps.

4. **What's the D7 retention shape?** — If users activate but don't return, the product is solving the acute freeze but not forming a habit. Would explore lightweight re-engagement that doesn't rely on streaks or guilt.

5. **Is there institutional pull before we build for it?** — Run 3 conversations with university welfare officers before building the B2B admin dashboard. Validate whether outcome reporting is a real procurement requirement.

---

## 📁 Document Index

| Document | Contents |
|---|---|
| [01 — Product Discovery & Strategy](https://github.com/VarshaJha-14/FocusBuddy/blob/main/Product%20Documents/01_Product_Discovery_and_Strategy.pdf) | Problem framing, user research insights, personas, JTBD, value proposition, MVP scope, RICE prioritization |
| [02 — PRD & Agile Backlog](https://github.com/VarshaJha-14/FocusBuddy/blob/main/Product%20Documents/02_PRD_and_Agile_Backlog.pdf) | Product objectives, user stories, acceptance criteria, functional & non-functional requirements, risk register, sprint backlog |
| [03 — AI Feature & Responsible AI](https://github.com/VarshaJha-14/FocusBuddy/blob/main/Product%20Documents/03_AI_Feature_and_Responsible_AI.pdf) | AI capability stack, input/output matrix, workflow diagram, data architecture, failure cases, guardrails matrix, transparency strategy |
| [04 — Metrics, Experimentation & GTM](https://github.com/VarshaJha-14/FocusBuddy/blob/main/Product%20Documents/04_Metrics_Experimentation_and_GTM.pdf) | North Star Metric, KPI framework, AARRR funnel, A/B test design, dashboard plan, GTM strategy, pricing model |
| [05 — Wireframes & User Flow](https://github.com/VarshaJha-14/FocusBuddy/blob/main/Product%20Documents/05_Wireframes_and_User_Flow.pdf) | Core user flow diagram, low-fidelity wireframes, UX design rationale, high-fidelity Figma prototype screens |
| [06 — AI Tool Usage Appendix](https://github.com/VarshaJha-14/FocusBuddy/blob/main/Product%20Documents/06_AI_Tool_Usage_Appendix.pdf) | Transparent log of AI tools used (ChatGPT, Claude, Gemini), prompts used, how outputs were reviewed and modified |

---

## 🛠 Built With

- **Research:** Primary user interviews + NIMHANS / AIIMS Delhi prevalence data
- **Framework:** RICE prioritization, AARRR funnel, Jobs-to-Be-Done
- **AI Tools:** ChatGPT (discovery, AI feature design), Claude (PRD, metrics, critique), Gemini (market research)
- **Design:** Figma (wireframes + prototype), Whimsical (user flow diagram)
- **All final decisions reviewed, validated, and modified by the author. AI outputs were treated as recommendations, not conclusions.**

---

*This is a product management portfolio case study. FocusBuddy is a concept product, not a live application.*
