# NichePulse Research Skill

Research and score any niche for print-on-demand, digital products, or e-commerce using the NichePulse scoring framework.

## Trigger

Use this skill when the user wants to:
- Find profitable niches for POD, digital products, or e-commerce
- Validate a niche idea before investing time/money
- Compare multiple niche opportunities
- Get a 90-day launch roadmap for a specific niche
- Score a custom niche on the 5-dimension framework

## Workflow

### Step 1: Run NichePulse

```bash
# List top-ranked niches from our pre-scored database
nichepulse list --top 15

# Score a specific niche
nichepulse score mushroom-foraging

# Compare multiple niches
nichepulse compare mushroom-foraging birding trail-running

# Get a 90-day roadmap
nichepulse roadmap mushroom-foraging

# Score a custom niche interactively
nichepulse custom "Urban Beekeeping"
```

### Step 2: Supplement with Live Research

After getting the score, run these validation checks:

1. **Etsy Search**: Search the niche keyword on Etsy. Note:
   - Total results count (under 1,000 = low competition)
   - Quality of top 10 listings (are they professional or amateur?)
   - Average price point of top sellers
   - Any design gaps you notice

2. **Google Trends**: Check 12-month trend direction:
   - Go to trends.google.com
   - Search niche keywords
   - Compare 12-month windows
   - Score: Up = 4-5, Flat = 3, Down = 1-2

3. **Community Size**: Search Reddit, Facebook Groups, Discord:
   - Active communities with 10K+ members = strong signal
   - Daily posts = engaged audience
   - User-generated content = identity-level attachment

### Step 3: Present Results

Format the output as:

```
🎯 NichePulse Analysis: [Niche Name]

Score: [Total]/25 ([Grade])
Passion: [x/5] | Buy Freq: [x/5] | Gift: [x/5] | Competition: [x/5] | Trend: [x/5]

Verdict: [DOMINATE/PRIORITIZE/VIABLE/WEAK/SKIP]

Estimated Margin: [range]

Key Notes:
- [note 1]
- [note 2]

90-Day Target: $500-2,000/month
```

## Scoring Framework

Each dimension scored 1-5:

- **Passion**: 1=casual interest → 5=identity-level obsession
- **Buy Frequency**: 1=one-time → 5=weekly purchases  
- **Gift Potential**: 1=self-only → 5=gift-first market
- **Competition**: 1=10K+ competing designs → 5=<100 quality designs
- **Trend**: 1=declining → 5=exploding growth

Grade thresholds:
- S (22-25): Go all-in
- A (18-21): Start immediately
- B (14-17): Test with small batch
- C (10-13): Weak unless unique angle
- D (5-9): Skip

## Pre-Validated Niches (2026 Data)

Top performers ready to launch:

| Niche | Score | Grade | Competition | Why |
|-------|-------|-------|-------------|-----|
| Mushroom Foraging | 22 | S | Very Low | Identity-level, gift-friendly, booming |
| Birding | 20 | A | Low | High AOV, Audubon crossover |
| Native Plants | 20 | A | Low | Google Trends +34%, eco buyers |
| Women's Outdoor | 20 | A | Low | SheEXPLODING, high WTP |
| Trail Running | 18 | A | Medium | $34-65 AOV, Strava culture |
| Hammock Camping | 18 | A | Very Low | Reddit 200K, Instagram 1M+ |

## Installation

NichePulse CLI is available via pip:

```bash
pip install nichepulse
nichepulse --help
```

Or clone and run locally:

```bash
git clone https://github.com/yourhandle/nichepulse
cd nichepulse
pip install -e .
nichepulse list --top 10
```
