# Coding Dictionary: FTC Personalized-Pricing Comments (Docket FTC-2026-1057)

Version 2 · developed by the team through a 40-comment development pilot that tested and tightened the category boundaries.

**Context.** The FTC proposal does **not** ban personalized pricing. It says undisclosed or misleading personalization may be unlawful, and it emphasizes clear disclosure that a price is personalized, why, and what data were used. A negative comment about personalized pricing does not tell us what the commenter wants the government to do. We therefore code **policy intent**, not sentiment.

## How to code

1. Read the whole comment once before assigning any label.
2. **Stance:** ask *"What does this commenter want the FTC/government to do?"* Pick **exactly one** from the dropdown.
3. **Reasons:** ask *"What substantive arguments does the commenter use to justify that position?"* Put **yes** under every reason that applies; leave the others blank. Zero reasons is allowed.
4. **Substantive-reason test:** if this issue were removed from the comment, would one of the author's actual reasons disappear? If yes, code it. If no, don't.
5. If you've marked four or more reasons, reread the comment and check each one passes the test.
6. Code only what the comment says. Don't infer a reason that is merely plausible.
7. Code independently. Don't discuss gold-set comments until both sheets are finished, and don't look at any Claude labels.
8. If a case feels ambiguous, record your best label and explain in `notes`. Don't change the rules mid-round.

## Stance (exactly one)

| Label | Definition | Typical evidence |
|---|---|---|
| `stronger_action` | Supports intervention but explicitly wants a materially stronger response than the proposed disclosure/enforcement approach. | Ban or prohibit personalized/surveillance pricing; "disclosure is not enough"; prohibit individualized markups; mandatory opt-in. |
| `support_as_proposed` | Broadly supports the FTC's disclosure/enforcement approach; doesn't ask for a materially stronger or narrower response. | Require clear notice that a price is personalized; explain the basis and data used; support with implementation suggestions. |
| `limit_or_oppose_intervention` | Argues the FTC goes too far, should narrow the policy or not adopt it, imposes unjustified burdens, or exceeds its authority. | Government overreach; FTC lacks authority; regulation would eliminate beneficial pricing; large exemptions. |
| `mixed_or_conditional` | Supports some intervention but draws a substantive boundary that prevents a clean placement above. | Personalized discounts are fine but personalized markups should be prohibited; intervention only for sensitive data or essential goods. |
| `unclear` | The desired government response can't be determined reliably. | Only says personalized pricing is bad or unfair; too little information; misunderstands the proposal with no recoverable desired action. |

### Tie-breaking rules
- A direct request for a ban or materially stronger restriction overrides generic praise for the FTC → `stronger_action`.
- Support for disclosure/enforcement plus minor implementation suggestions remains `support_as_proposed`.
- A genuine carve-out or two-sided position (discounts yes, individualized markups no) → `mixed_or_conditional`.
- Use `limit_or_oppose_intervention` only when the commenter genuinely wants less or narrower FTC intervention. **Disliking personalized pricing is not opposition to the FTC.**
- If the commenter misunderstands the proposal and the desired response isn't otherwise clear → `unclear`.
- **Tone doesn't determine stance.** Anger, "unfair" or political language are not stance labels by themselves.
- Saying personalized pricing is unfair or wrong is **not automatically** a request for action. Direct requests to ban, stop, protect consumers, guarantee an opt-out or otherwise strengthen the remedy count as `stronger_action`.

## Reasons (zero or more)

| Label | Code when… | Don't code when… |
|---|---|---|
| `privacy_data_use` | Personal data collection or use is part of the argument: surveillance, tracking, profiling, consent, browsing/location/purchase data, data brokers. | The comment merely mentions that an algorithm uses "data". |
| `transparency_disclosure` | Hidden or opaque personalized pricing, notice, disclosure, explaining what affected the price. | The comment only repeats the proposal's disclosure requirement without endorsing or criticizing it. |
| `fairness_discrimination_consumer_harm` | Exploitation, unfairness, discrimination, vulnerable consumers, emergencies, necessities, inability to shop around, manipulation, concrete harm. | Used as a catch-all for any negative comment; the harm logic must be stated. |
| `pricing_affordability_equal_treatment` | The price outcome itself: different people paying different prices, individualized markups, affordability, gouging, equal or uniform pricing. | Prices are mentioned without being part of the argument. |
| `competition_business_economics` | A genuine market or economic argument: competition, market power, innovation, efficiency, business burden, benefits of discounts. | Firms, profits or corporations are merely mentioned. |
| `legal_authority_policy_scope` | FTC authority, Section 5, jurisdiction, constitutionality, statutory limits, which sectors or practices should be covered or exempt. | The comment only says "the FTC should act" or "use its authority". |
| `other` | A substantive policy reason that fits none of the above. | The comment is vague. If no reason is given, mark no reasons. |

### Boundary decisions
- **Privacy vs transparency:** privacy asks whether/how personal data are collected or used; transparency asks whether consumers are told. Code both only when both arguments are substantive.
- **Fairness vs pricing:** fairness is about exploitation, vulnerability, discrimination or harm; pricing is about the fact or size of different prices, affordability, markups or equal treatment. A comment can have both.
- **Fairness vs competition/economics:** "firms profit from consumers" is not automatically an economics argument. Use `competition_business_economics` only for a real market, efficiency, competition, innovation or business-burden argument.
- **FTC action vs legal authority:** asking the FTC to act is part of stance, not a legal reason. Code `legal_authority_policy_scope` only when authority, jurisdiction or scope is itself argued.
- **Description vs reason:** don't code a category because the commenter repeats wording from the proposal. It must play a role in their own argument.

## Worked examples (illustrative, not from the sample)

| Comment | Stance | Reasons |
|---|---|---|
| "FTC should ban personalized pricing." | `stronger_action` | none (no justification given) |
| "The FTC should require companies to tell consumers when a price is personalized and what data were used." | `support_as_proposed` | transparency_disclosure; privacy_data_use |
| "Personalized discounts can help consumers, but companies should not be allowed to raise a person's price based on personal data." | `mixed_or_conditional` | competition_business_economics; privacy_data_use; pricing_affordability_equal_treatment |
| "The FTC lacks statutory authority to regulate pricing in this way, and the proposal would burden legitimate discount programs." | `limit_or_oppose_intervention` | legal_authority_policy_scope; competition_business_economics |
| "This practice is creepy and unfair." | `unclear` | fairness_discrimination_consumer_harm |
| "Disclosure is not enough. Companies should be banned from using sensitive personal data to charge vulnerable people more." | `stronger_action` | privacy_data_use; fairness_discrimination_consumer_harm; pricing_affordability_equal_treatment |

## Process (final notebook)

1. **Pilot (20 comments).** Both coders code the `pilot` rows in their own sheet (`coding/coding_sheet_coder1.xlsx`, `coding/coding_sheet_coder2.xlsx`). Run the notebook; it creates `coding/reconcile_pilot.xlsx`. Discuss each blank `agreed_` cell and fill it. These agreed labels become Claude's few-shot examples.
2. **Gold set (80 comments).** Code independently. Time yourselves; the minutes go into Section 11.
3. **Reconcile.** Run the notebook; it computes Cohen's kappa **before** reconciliation and creates `coding/reconcile_gold.xlsx`. Fill every blank `agreed_` cell together (`agreed_reasons`: labels separated by `; `, or `none`). Run the notebook again for the full evaluation.
