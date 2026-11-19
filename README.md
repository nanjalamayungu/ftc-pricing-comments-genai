# Can GenAI Read the Public Record? Validated Classification of Public Comments on the FTC's Personalized-Pricing Policy

Ruth and Ketty
INFO 4340, Fall 2026, University of Denver

## Overview

Regulators, law firms and public-affairs teams must read and summarize thousands of public comments by hand; a misread comment misrepresents the public record. This project asks whether a generative AI model can do that work accurately, cheaply and safely, using 1,566 individual comments on the Federal Trade Commission's 2026 proposed policy on personalized pricing (docket FTC-2026-1057). Claude labels each comment with **what the commenter wants the FTC to do** (one stance) and **the reasons they give** (zero or more), together with an exact supporting quote and a confidence rating; two human coders built the gold standard it is checked against, and fixed governance thresholds decide when its results can be used. The answers serve two audiences: organizations deciding whether to use GenAI for comment analysis, and companies that use personalized pricing.

## Key findings

- **Claude matches human coders closely on stance.** Claude Haiku 5.5 (zero-shot) scored macro-F1 = 0.93 (95% CI: 0.86-0.97), 90% accuracy and kappa = 0.82 against an 80-comment gold standard on which the two human coders agreed at kappa = 0.95. Every non-AI baseline scored far lower: TF-IDF + logistic regression 0.66, topic model 0.56, VADER sentiment 0.43. The gap to each baseline exceeds the minimum detectable difference; zero-shot and few-shot Claude are a statistical tie (McNemar p = 1.00).
- **It is cheap to run, and its errors are predictable.** Labelling all 1,566 comments cost $0.44 ($0.28 per 1,000), about $28 per 100,000 comments against roughly 1,300 analyst hours by hand. Its errors cluster in long comments (21% wrong vs 4% for short ones), comments that discuss the FTC's rule itself (27% vs 7%), and the rare stance "limit or oppose", where only 1 of its 5 labels was right. Its own confidence predicts errors (25% wrong when "low" vs 3% when "high").
- **Two thirds of commenters want more than disclosure.** 65% (95% CI: 62.5-67.3%) want stronger action than the FTC proposed, mostly a ban; at least 67% are against personalized pricing itself, and almost no one defends it. The objections are use of personal data (50%), unequal prices (49%) and fairness (48%); lack of disclosure, the FTC's main remedy, appears in only 10%.
- **Governance: assisted analysis, not autonomous reporting.** 8 of 9 pre-registered checks passed; the comment-length check failed (5.8x the best group's error rate vs a 1.25x limit). Back-testing shows low confidence alone catches only 4 of 10 errors; the recommended review queue (low confidence, quote not found, or over 200 words) catches 5 of 10 while flagging 21% of comments, plus a 5% random audit.

## Data

- **Source:** Public comments on docket FTC-2026-1057 ([regulations.gov/docket/FTC-2026-1057](https://www.regulations.gov/docket/FTC-2026-1057)), retrieved from the official Regulations.gov v4 API with a fixed random seed (20261027).
- **Size:** 1,566 individual, text-based comments (42% of the 3,706 comments on the docket); median 28 words, maximum 820. Comments from organizations (mostly long attachments) are out of scope.
- **Unit of observation:** One public comment submitted by an individual.
- **Access:** Included in `Data/Used_individuals_sentiment_data.csv`. Commenters' typed-in names are masked before any text is shown, saved for coding or sent to the API.

## Workflow

1. **Cleaning:** Decode HTML characters, normalize whitespace, check IDs are unique and no text is empty (every step guarded by `assert`), flag very short comments, and detect near-duplicate form letters (59 comments in 22 groups, TF-IDF cosine >= 0.80). Form letters are kept but every finding is re-checked counting each group once.
2. **AI step:** Claude Haiku 5.5 (`claude-haiku-5-5`), low thinking effort, prompt version v2. The current API (2026-10-21) no longer accepts a temperature setting, so the model runs with default sampling and consistency is measured instead (same stance in 3 runs for 90% of comments). The prompt is generated from our coding dictionary (5 stances, 7 reasons, boundary rules) and asks for JSON: one stance, any reasons, an exact evidence quote and a low/medium/high confidence. Every answer is validated (valid labels, quote really in the comment) and saved, so reruns cost nothing.
3. **Analysis:** Stance and reason shares for all 1,566 comments with Wilson 95% confidence intervals, a form-letter sensitivity check, chi-square tests and Cramer's V for reasons by stance, and a "Part B" view of attitudes to the practice itself.
4. **Evaluation:** A 100-comment random sample coded independently by both of us (20 pilot + 80 gold; stance kappa 0.95). Claude zero-shot and few-shot compared with three baselines (VADER sentiment, topic model, TF-IDF + logistic regression) on accuracy, precision, recall, macro- and micro-F1 and kappa, with bootstrap CIs, the minimum detectable difference, McNemar's test, every category including rare ones, run-to-run stability, error rates by comment length, error analysis, and measured cost.
5. **Recommendation:** Use GenAI as a validated first reader, not a replacement: report results only with human review of the flagged comments, never report the "limit or oppose" share without reviewing every comment in it, keep a 5% random audit, and re-validate on any model or prompt change or quarterly. For companies: disclosure alone is unlikely to defuse opposition, which centres on data use and unequal prices.

## Notebook structure

`ftc_genai_workflow.ipynb` runs top to bottom in 15 sections. Every chart is followed by a note on how to read it and what it shows.

| Section | What it does | Competency |
|---|---|---|
| 1. Business understanding | Use case, business problem, the six questions, scope | Understand |
| Setup + workflow diagram | Libraries, settings, seed, file paths; the whole pipeline on one page | Use |
| 2. Data understanding | Load the 1,566 comments and check columns and missing values | Use |
| 3. Data cleaning | Clean text and check every step with `assert` | Use |
| 4. Summary statistics + word cloud | Comment length, posting dates, states, most frequent words | Use |
| 5. Form letters | Near-duplicate detection (59 comments in 22 groups) | Use |
| 6. Topic modelling | NMF topics, named and linked to the coding dictionary | Use |
| 7. Modelling | VADER and topic baselines, TF-IDF + logistic regression, the coding dictionary, the Claude classifier (prompt, answer checks, cache) | Use |
| 8. Evaluation | Thresholds fixed before results; hand-coding and coder agreement (kappa 0.95); every model vs the gold standard with 95% CIs and the minimum detectable difference; every stance and reason including rare ones; stability; errors by comment length; where and why Claude fails | Evaluate |
| 9. Findings | Labels for all 1,566 comments; Part A (what commenters want the FTC to do), Part B (views of the practice), reasons, reasons by stance | Use |
| 10. Governance checks | All 9 thresholds applied; human-review queue and 5% random audit | Govern |
| 11. Cost analysis | Measured API cost and time, projection vs human coding | Evaluate |
| 12. Governance in depth | Back-tested review rules, subgroup disparity, harm at 5,000 comments a month, safeguard map, risk matrix, audit trail, recommendations and limitations | Govern |
| 13. Answers to the business questions | Each question answered from the evidence, with its validation status | Recommend |
| 14. Reproducibility record | Package versions, seed, model and prompt settings, data fingerprint | Use |
| 15. Save results for the app | Writes `outputs/app/app_results.json` for the Streamlit app | Use |

## Repo contents

- `ftc_genai_workflow.ipynb` - Main analysis, runs top to bottom (Sections 1-15: business understanding, data, cleaning, EDA, modelling, evaluation, findings, governance, cost, answers, reproducibility)
- `ftc_genai_workflow.html` - Rendered copy of the executed notebook
- `Data/Used_individuals_sentiment_data.csv` - The 1,566 comments
- `coding/` - Coding dictionary (`CODEBOOK.md`), both coders' sheets, reconciliation sheets (agreed gold labels), Claude's stance errors, the human-review queue and the random-audit sample
- `outputs/llm/` - Saved model outputs: every Claude answer with tokens, latency, model and prompt version (`labels_*.jsonl`), and the final labels for all comments (`labels_all_comments.csv`)
- `outputs/figures/` - All charts
- `outputs/app/app_results.json` - Results used by the Streamlit app
- `app.py` and `.streamlit/config.toml` - Interactive Streamlit app organized by Understand, Use, Evaluate, Govern, including a live classifier and a human-review desk
- `deliverables/` - Written summary, governance memo and presentation slides (PDF)
- `requirements.txt` - Pinned package versions

## How to run it

1. Clone this repo and install packages:
   `pip install -r requirements.txt`
2. (Only needed to re-run the AI step or use the app's live classifier) Create a file named `.env` in the repo folder containing `ANTHROPIC_API_KEY=your-key`. It is listed in `.gitignore` and never committed.
3. Open `ftc_genai_workflow.ipynb` and run all cells. By default, the notebook reads the saved AI outputs in `outputs/llm/` and does not call the API, so every number reproduces exactly at no cost.
4. (Optional) Start the app from the repo folder: `streamlit run app.py`

## Limitations

- **Commenters are self-selected,** so shares describe people who chose to comment, not U.S. public opinion; organizations' comments are not included.
- **Rare stances are not really tested.** Only 4 of the 80 gold comments were "support as proposed", "mixed" or "limit or oppose"; Claude's accuracy on them is not established, and the "limit or oppose" share (2.5%) is probably overstated.
- **Reasons are harder than stance:** reason micro-F1 is 0.78, and transparency arguments are under-detected (recall 0.50-0.62), so the 10% transparency share is a minimum.
- **Human review catches only part of the errors:** even the recommended review queue catches about half of Claude's mistakes on our data, and the back-tests rest on only 10 known errors.
- **The gold standard was coded by the two of us,** who also wrote the coding dictionary; human coding time in the cost comparison is estimated from comment length, not measured.
- **One model, one prompt, one date:** results apply to Claude Haiku 5.5 with prompt v2 and expire when either changes.

## AI use

We used Claude as a coding and writing assistant to draft and debug the notebook, the Streamlit app and documentation, and Claude Haiku 5.5 as the classifier inside the workflow. Every AI-generated number was checked against the executed notebook, the classifier was validated against our own hand-coded labels, and our individual AI use logs record each judgment call.
