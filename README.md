# Lead Qualification Agent

A small, working agent that turns a raw lead list into a prioritised
action list. It does not just chat. It scores, prioritises and drafts.

## The problem it solves

A business gets a long list of leads and does not know who to contact
first. Calling everyone wastes time. Calling in the wrong order loses
good customers.

## What this agent does

1. **Intake:** Reads leads from a CSV file.
2. **Score:** Gives each lead 0-100 based on fit and completeness:
   - Business email: 30
   - Phone: 20
   - Website: 20
   - Target industry fit: 20
   - Complete location (city + state): 10
3. **Grade:** A (80+) contact first, B (60-79) contact next,
   C (below 60) needs more data.
4. **Draft:** Writes a short, personalised first outreach email for
   A and B leads. No price in the first email. No contact is guessed,
   a missing field simply lowers the score.
5. **Output:** Saves `scored_leads.csv`, highest score first.

## How to run it

```bash
python3 agent.py --input leads_sample.csv --output scored_leads.csv
```

Sample result from the included sample file:

| Lead | Score | Grade |
|---|---|---|
| Bright Homes Realty | 100 | A - Contact first |
| Summit Mortgage Group | 100 | A - Contact first |
| Northside Marketing Co | 80 | A - Contact first |
| Sample SaaS Studio | 80 | A - Contact first |
| Harbor Property Management | 50 | C - Needs more data |

## Optional API demo

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Then `POST /score` with a lead JSON object to get its score, grade,
reasons and outreach draft.

## How it can grow

- Plug an LLM into `draft_outreach()` to rewrite drafts in a
  different tone, without changing scoring or output format.
- Add new scoring rules, for example company size or lead source.
- Connect the output to Google Sheets instead of CSV.

## Sample data note

`leads_sample.csv` uses fictional example businesses with
`.example` domains, so no real business is misrepresented. Replace
it with a client's real, verified lead list to run it for real work.

Built by Faryal Syeda — Agentic AI portfolio project 1.
