# Codebook: FTC Personalized-Pricing Comments (Docket FTC-2026-1057)

Version 1.1 · individuals only; six concern categories. Use for the pilot round, then revise and bump the version.

**Context to keep in mind.** The FTC proposal does **not** ban personalized pricing. It says companies may break the law if they don't clearly disclose when a price is personalized, why, and what data was used. Many commenters misunderstand this. Code what the commenter **wants**, not what they think the rule says.

**How to code.**
- Read the whole comment once. Fill every column using the dropdowns, and add a note when you're unsure.
- Code independently. Don't discuss gold-set comments with your partner until both sheets are done.
- Code only what the text says. Don't guess intent from tone. If you can't tell, use `unclear` or `not_stated`.

---

## 1. `view`: the commenter's view of personalized pricing as a practice

| Value | Definition | Real example |
|---|---|---|
| `against` | Opposes personalized or surveillance pricing. | "Personalized pricing is a shady practice that should not be legal." |
| `in_favor` | Defends it or its benefits (discounts, efficiency, consumer choice). | Mostly business and think-tank comments; rare among individuals. |
| `mixed` | Accepts it only under conditions, or weighs benefits against harms. | "Prices must be the same for all individuals. The exception would be if an individual enrolled in a special discount plan." |
| `unclear` | The position can't be determined, or the comment is off-topic. | "just got a notice from my county auditor for a tax increase." |

**Rules.** Anger at corporations in general, without mentioning pricing, is `unclear`. "Do not pass this rule" is usually `against` the practice: check the rest of the text.

## 2. `requested_action`: what the commenter asks the FTC to do

| Value | Definition | Real example |
|---|---|---|
| `ban` | Prohibit it; disclosure isn't enough. Includes "make it illegal" and "use your authority to ban". | "Disclosure is not enough. Personalized pricing needs to be banned." |
| `support_or_strengthen` | Supports the FTC proposal, or asks for more disclosure, opt-outs or enforcement, without asking for a ban. | "I support the FTC proposed Enforcement Policy Regarding Personalized Pricing." |
| `narrow_or_exempt` | Asks the FTC to narrow the policy or exempt discounts, loyalty programs, etc. | The RV Dealers Association asks the FTC to distinguish price increases from "bona fide discounts". |
| `withdraw` | Wants the FTC to drop the proposal or not regulate, **because regulation is unwanted**. | Rare among individuals. |
| `not_stated` | No clear request. Includes "stop this" aimed at companies, and "don't pass this" when it's unclear whether they want more or less regulation. | "Please do not implement this regulation. It will definitely hurt me as I am on a fixed income." |

**Rules.**
- "Stop personalized pricing" / "this should be illegal" → `ban`.
- "Stop this" with no clear target → `not_stated`.
- If a comment asks for both a ban and, failing that, stronger disclosure, code the strongest request: `ban`.

## 3. `primary_concern`: the main reason given (and `secondary_concern` for a second one)

| Value | Definition | Real example |
|---|---|---|
| `privacy_data_use` | Collection or use of personal data, surveillance, consent. | "No one should have access to our personal data especially companies selling products and services." |
| `fairness_discrimination` | Unequal prices for the same product, discrimination, harm to vulnerable people. | "Two consumers purchasing the same product… should pay the same price." |
| `transparency_disclosure` | Not knowing prices are personalized; hidden pricing; disclosure being weak or misleading. | "People deserve to know if and when and how they [are charged]." |
| `corporate_greed_gouging` | Price gouging, profiteering, corporations exploiting consumers or the cost of living. | "PRICE GOUGING HAS NO PLACE ANYWHERE!! I'M SICK OF CORPORATIONS RIPPING THE AMERICAN PEOPLE OFF!!" |
| `competition_markets` | Harm to comparison shopping, free markets, competition or small businesses. | "Capitalism works best when consumers know what price they are paying AHEAD of TIME." |
| `other` | Any other reason (including legal or constitutional arguments), or no reason given. | "Stop personalized pricing now." |

**Rules.**
- **Primary = the reason given the most space**, or the first one if they're equal. Secondary = a second, clearly separate reason; otherwise `other`.
- "Use your authority to ban it" is a request (`ban`), **not** a concern. Code the concern from the reason they give.
- "Unfair" with no explanation → `fairness_discrimination`.
- "Unfair because they use my data" → primary `privacy_data_use`, secondary `fairness_discrimination`.
- Calling the practice "discrimination" → `fairness_discrimination`.
- Market language as the main argument ("free market", "comparison shopping", "monopoly") → `competition_markets`; a passing word like "corrupt capitalism" alongside another reason → code the other reason.
- Blaming companies for high prices or the cost of living → `corporate_greed_gouging`.

## 4. `personal_experience`

`yes` if the commenter describes something that happened to them or that they saw (a price change, a store, an app). Otherwise `no`.

Example: "Usually the price goes up the same day when I circle back to item." → `yes`.

## 5. Notes

Use `notes` for anything you were unsure about. These notes feed the codebook revision after the pilot round and the error analysis.

---

## Process

1. **Pilot (20 comments).** Both partners code the pilot rows. Compare, discuss every disagreement, and update the rules here (version 1.1). Save the agreed labels as `coding/pilot_reconciled.csv`; these become the few-shot examples.
2. **Gold set (130 comments).** Code independently. Save as `coding/coding_sheet_coder1.xlsx` and `coding_sheet_coder2.xlsx`, then run the notebook. It computes Cohen's κ and lists disagreements.
3. **Reconcile.** Discuss each disagreement and save the agreed labels as `coding/gold_reconciled.csv` (columns: `comment_id, text, view, requested_action, primary_concern`).
