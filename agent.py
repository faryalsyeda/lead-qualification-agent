"""
Lead Qualification Agent - Portfolio Project 1
------------------------------------------------
What it does, in plain words:
  1. Takes a raw list of leads (CSV).
  2. Scores each lead for fit and completeness.
  3. Drafts a short, personalised first outreach email for the top leads.
  4. Saves a prioritised, scored list (CSV) that a client can act on.

This demo version uses clear, transparent scoring rules so the result
can be explained to a client without hiding behind a black box.
An LLM can later be plugged into draft_outreach() to rewrite the draft
in a different tone - the scoring and output format stay the same.

No prices are put in the first email. No contact details are guessed:
a missing email, phone or website simply lowers the score.
"""

import argparse
import csv
import json
import sys
from pathlib import Path

TARGET_INDUSTRIES = {
    "real estate",
    "mortgage",
    "property management",
    "marketing agency",
    "saas",
    "software",
}


def score_lead(lead):
    """Return (score 0-100, grade, reasons) for one lead dict."""
    score = 0
    reasons = []

    if lead.get("email"):
        score += 30
        reasons.append("Business email available")
    else:
        reasons.append("No business email - score reduced")

    if lead.get("phone"):
        score += 20
        reasons.append("Phone available")
    else:
        reasons.append("No phone listed")

    if lead.get("website"):
        score += 20
        reasons.append("Website available")
    else:
        reasons.append("No website listed")

    industry = (lead.get("industry") or "").strip().lower()
    if industry in TARGET_INDUSTRIES:
        score += 20
        reasons.append(f"Industry fit: {lead.get('industry')}")
    elif industry:
        reasons.append(f"Industry not in target list: {lead.get('industry')}")

    if lead.get("city") and lead.get("state"):
        score += 10
        reasons.append("Location complete (city + state)")
    else:
        reasons.append("Location incomplete")

    if score >= 80:
        grade = "A - Contact first"
    elif score >= 60:
        grade = "B - Contact next"
    else:
        grade = "C - Needs more data"

    return score, grade, reasons


def draft_outreach(lead):
    """Draft a short first email. No price, no full list attached."""
    company = lead.get("company") or "your team"
    city = lead.get("city") or ""
    state = lead.get("state") or ""
    place = f" in {city}, {state}" if city and state else ""
    industry = lead.get("industry") or "your business"

    return (
        f"Subject: Quick question about leads for {company}\n\n"
        f"Hi {company} team,\n\n"
        f"I work with {industry} businesses{place} and help them get "
        "new customers through verified leads.\n\n"
        "Can I ask a quick question? What kind of leads would help you most "
        "right now, which city/state, and roughly how many per month? "
        "I can share a small free sample matched to your criteria, "
        "with no obligation.\n\n"
        "Thanks,\nFaryal Syeda"
    )


def process_file(input_path, output_path):
    with open(input_path, newline="", encoding="utf-8") as f:
        leads = list(csv.DictReader(f))

    rows = []
    for lead in leads:
        score, grade, reasons = score_lead(lead)
        rows.append(
            {
                **lead,
                "score": score,
                "grade": grade,
                "reasons": "; ".join(reasons),
                "outreach_draft": draft_outreach(lead) if score >= 60 else "",
            }
        )

    # Highest score first, so the client knows who to contact first.
    rows.sort(key=lambda r: r["score"], reverse=True)

    if rows:
        fieldnames = list(rows[0].keys())
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    return rows


def main():
    parser = argparse.ArgumentParser(description="Score leads and draft outreach.")
    parser.add_argument("--input", default="leads_sample.csv")
    parser.add_argument("--output", default="scored_leads.csv")
    args = parser.parse_args()

    rows = process_file(args.input, args.output)
    print(f"Processed {len(rows)} leads -> {args.output}")
    for row in rows:
        print(f"{row['score']:3} | {row['grade']:22} | {row.get('company')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
