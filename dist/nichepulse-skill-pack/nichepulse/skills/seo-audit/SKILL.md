# SEO Audit Skill

Perform comprehensiveSEO analysis on any URL using the `web_search` and `web_extract` tools.

## Trigger

Use when user asks about:
- SEO analysis or audit of a website/page
- Keyword research or search volume estimation
- Competitor SEO analysis
- Ranking improvement recommendations
- Technical SEO issues
- Content optimization suggestions

## Workflow

### Step 1: Gather Page Data

Use `web_extract` to pull the full content of the target URL.

### Step 2: Run SEO Audit

Analyze these dimensions:

**On-Page SEO:**
- Title tag: length, keyword placement, uniqueness
- Meta description: length, call-to-action, keyword inclusion
- H1/H2/H3 hierarchy: structure, keyword usage, readability
- Content length: word count vs. competitors
- Keyword density: primary and secondary keywords
- Image alt tags: coverage and relevance
- Internal linking: depth and anchor text
- URL structure: clean, keyword-rich, canonical

**Technical SEO:**
- Page speed signals (LCP, FID, CLS)
- Mobile responsiveness indicators
- Schema markup presence
- HTTPS, canonical tags, robots meta

**Content Quality:**
- E-E-A-T signals (expertise, experience, authority, trust)
- Content freshness and depth
- Readability score estimate
- Content gap vs. competitors

### Step 3: Competitor Comparison

For the top search query for the page's topic:
- Use `web_search` to find the top 5-10 results for the primary keyword
- Note common themes, content types, and gaps
- Identify what the target page is missing

### Step 4: Keyword Opportunity Analysis

Use `web_search` patterns to identify:
- Primary keyword (highest volume, most relevant)
- Secondary keywords (related terms in results)
- Long-tail keywords (niche-specific, lower competition)
- Question-based keywords (content opportunity)

### Step 5: Output Audit Report

Format output as:

```
📊 SEO Audit: [URL]

Score: [X]/100

Title: [text] — [OK/TOO SHORT/TOO LONG/NO KEYWORD]
Meta: [text] — [OK/MISSING/TOO LONG]
Word Count: [X] — [OK/TOO SHORT]
H1: [text] — [OK/MISSING/MULTIPLE]

Top 3 Quick Wins:
1. [actionable recommendation with expected impact]
2. [actionable recommendation with expected impact]
3. [actionable recommendation with expected impact]

Keyword Opportunities:
- Primary: [keyword] (estimated volume, difficulty)
- Secondary: [keyword1, keyword2, keyword3]
- Long-tail: [keyword1, keyword2]

Competitor Gaps:
- [What competitors have that target page lacks]
- [Content type or topic gap to fill]
```

## SEO Scoring Rubric

| Dimension | Weight | Max Points |
|-----------|--------|------------|
| Title optimization | 15% | 15 |
| Meta description | 10% | 10 |
| Content depth & quality | 25% | 25 |
| Keyword usage | 15% | 15 |
| Technical signals | 15% | 15 |
| E-E-A-T signals | 10% | 10 |
| Internal structure | 10% | 10 |

## Tips for High-Quality Audits

- Always check multiple competitor pages, not just the target
- Prioritize recommendations by impact (traffic potential) not effort
- Flag critical issues (missing title, no content) separately from optimizations
- Include specific suggested rewrite text for underperforming elements
- Estimate traffic impact of each recommendation where possible
