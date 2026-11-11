# Policy and Artificial Intelligence: FTC Personalized-Pricing Public Comments

**Team:** Ruth & Ketty  
**Course:** INFO 4340 Final Project

## Project question

**Can generative artificial intelligence help a public agency make sense of a large public-comment record accurately, affordably, and responsibly?**

Our specific case is the Federal Trade Commission's 2026 proposed enforcement policy statement on personalized pricing. Our classification question is:

> **What response does each commenter want from the Federal Trade Commission?**

We deliberately measure **policy intent rather than generic positive/negative sentiment**.

## Why the policy framing matters

The Federal Trade Commission's August 19, 2026 document was a **proposed enforcement policy statement**, not a blanket prohibition on personalized pricing. The Commission stated that Congress had not granted authority to prohibit personalized pricing in all circumstances, while explaining how undisclosed or misleading personalized pricing could constitute unfair or deceptive conduct. The proposal emphasized clear and conspicuous disclosure, including the fact that a price is personalized, the basis of personalization, and the types of data used.

Because a person can dislike personalized pricing while preferring very different government responses, we classify the requested policy response rather than sentiment toward the practice itself.

## Course concepts used

The project follows the course arc **Understand -> Build and Compare -> Evaluate -> Govern**.

- **Understand:** data audit, reproducibility, human coding, codebook design, and inter-rater reliability.
- **Build and compare:** a traditional text-classification baseline, prompt engineering, schema-constrained structured output, and exploratory model comparison in Arena.ai.
- **Evaluate:** accuracy, precision, recall, macro-averaged F1 score, confusion matrices, bootstrap uncertainty, stability, concern-label performance, and cost.
- **Govern:** risk scoring, measurable operating rules, human review, evidence grounding, subgroup monitoring, documentation, accountability, and escalation.

Arena.ai was used only for **exploratory side-by-side comparison during development**. It was not part of the formal benchmark and was not used as evidence for choosing the production model.

## Data

The working analytic corpus contains **1,566 individual, text-based public comments** associated with docket FTC-2026-1057.

- 1,566 unique comment identifiers
- no missing comment text
- median comment length: 28 words
- mean comment length: 56.49 words
- maximum: 820 words
- comments are self-selected and therefore are **not representative public opinion**

The analytic corpus is a verified subset of the broader docket and excludes organizational and attachment-based filings from the primary classifier.

## Coding targets

### Stance - one label per comment

- `stronger_action`
- `support_as_proposed`
- `limit_or_oppose_intervention`
- `mixed_or_conditional`
- `unclear`

### Policy concerns - multiple labels allowed

- privacy and data use
- transparency and disclosure
- fairness, discrimination, and consumer harm
- pricing, affordability, and equal treatment
- competition, business, and economics
- legal authority and policy scope
- other

The frozen coding dictionary is `FTC_Coding_Dictionary_Final.docx`.

## Human benchmark

We first used a 40-comment development pilot to tighten the coding rules. We then froze the dictionary and independently coded the same 120-comment random validation sample without seeing each other's labels.

- raw stance agreement: **85.0% (102/120)**
- Cohen's kappa: **0.706**
- course reliability threshold: **0.60**

We reconciled disagreements only after measuring independent agreement. The reconciled labels became the gold-standard validation set.

## Model comparison

### Traditional baseline

Term frequency-inverse document frequency features with class-weighted logistic regression produced:

- accuracy: **65.8%**
- macro-averaged F1 score: **0.437**

### Generative artificial intelligence

We evaluated two prompts on exactly the same 120 gold comments:

- **Prompt A:** concise taxonomy with minimal guidance
- **Prompt B:** frozen-codebook prompt with policy context, boundary rules, tie-breakers, and the substantive-reason test

Prompt A:
- accuracy: **81.7%**
- macro-averaged F1 score: **0.726**

Prompt B:
- accuracy: **80.8%**
- macro-averaged F1 score: **0.820**
- stronger-action recall: **0.921**
- accuracy among comments not flagged for review: **93.5%**
- share of stance errors captured by its review flag: **78.3%**

We selected Prompt B for the final stance workflow because its class-balanced performance and review behavior were more useful operationally. We do not claim statistical dominance: the paired bootstrap interval for the Prompt-B-minus-Prompt-A macro-averaged F1 difference crosses zero.

## Full-corpus results

Prompt B classified all 1,566 comments:

| Stance | Comments | Share |
|---|---:|---:|
| Stronger action | 963 | 61.5% |
| Unclear | 511 | 32.6% |
| Limit or oppose intervention | 53 | 3.4% |
| Support as proposed | 27 | 1.7% |
| Mixed or conditional | 12 | 0.8% |

Most common model-coded concern labels were:

| Concern | Share of comments |
|---|---:|
| Pricing, affordability, and equal treatment | 64.0% |
| Privacy and data use | 50.8% |
| Fairness, discrimination, and consumer harm | 39.1% |
| Transparency and disclosure | 13.0% |

Concern labels are multi-select, so shares overlap.

## Cost

Observed Claude Haiku 5.5 inference spending across the recorded project runs was approximately **$0.69**:

- Prompt A validation: ~$0.035
- Prompt B validation: ~$0.048
- 1,446 new full-corpus calls: ~$0.581
- two fresh 30-comment stability runs: ~$0.026

This is **model-inference cost only**. It does not include our time, data engineering, quality assurance, security, documentation, governance, or human review.

## Governance decision

The final system is suitable for **assisted aggregate analysis with human review and monitoring, not autonomous reporting**.

Key rules:

1. Revise the codebook and recode if human-human Cohen's kappa falls below **0.60**.
2. Automated aggregate reporting is not permitted if macro-averaged F1 score is below **0.80** or a substantively important stance has recall below **0.70**.
3. Investigate if any observed text-length group's error rate exceeds **1.25 times** the best-performing group.
4. Reject, retry, or route to human review any record with invalid structured output, an unapproved label, or an evidence quote that cannot be found in the source text.
5. Investigate stability if exact three-run stance agreement falls below **90%**.

Observed status:

- macro-averaged F1 score: **0.820 - pass**
- three-run exact stance stability: **86.7% - investigation trigger**
- text-length error-rate ratio: **investigation trigger**
- combined model/evidence governance queue: **510 comments (32.6%)**

The 510-record governance queue is not the same set as the 511 comments classified `unclear`. For aggregate research, `unclear` is retained as a valid substantive category rather than forced into another stance. Case-level interpretation of an `unclear` comment still requires human judgment.


## Final deliverables

The repository includes the completed project artifacts under `deliverables/`:

- `FTC_Personalized_Pricing_Written_Summary_FINAL.pdf` - 4-page written project summary
- `FTC_Personalized_Pricing_Governance_Memo_FINAL.pdf` - governance memo using the class risk-matrix and threshold-rule framework
- `FTC_Policy_and_Artificial_Intelligence_FINAL.pdf` - 13-slide presentation for the final pair presentation
- editable Word and PowerPoint versions of those documents
- `AI_Use_Log_Ruth_FINAL.pdf` - Ruth's individual artificial-intelligence use log

The pair-authored materials use first-person plural voice throughout. Ketty should submit her own individual artificial-intelligence use log based on her personal use of tools during the project.

## Reproducibility

`FTC_Final_Project.ipynb` contains the executed end-to-end analysis. Paid model outputs are saved under `outputs/`, so reproduction does not require another paid model run. No secret key is stored in this repository.

## Repository structure

```text
.
├── Data/
├── docs/
├── outputs/
├── prompts/
├── FTC_Coding_Dictionary_Final.docx
├── FTC_Final_Project.ipynb
├── FTC_Final_Project_EXECUTED_FINAL.ipynb
├── FTC_Final_Project_FINAL.html
├── README.md
└── requirements.txt
```

## Interpretation limits

- Public comments are self-selected and do not represent a probability sample of public opinion.
- The 1,566-row analytic corpus is a verified subset rather than the full docket.
- The random validation sample happened not to contain two rare stance categories; the challenge set was retained for boundary testing.
- Concern extraction was weaker than stance classification and is interpreted more cautiously.
- Cost estimates describe model inference, not the total cost of responsible public-sector analysis.

## Official policy sources

- Federal Trade Commission, *Federal Trade Commission's Proposed Enforcement Policy Statement Regarding Personalized Pricing*, August 19, 2026.
- Federal Trade Commission, *FTC Seeks Comment on Enforcement Policy Statement Regarding Personalized Pricing*, August 19, 2026.
- Federal Trade Commission, *FTC Extends Public Comment on Proposed Policy Statement Regarding Personalized Pricing*, September 3, 2026.
- Anthropic, Claude Haiku 5.5 pricing documentation, checked November 11, 2026.
