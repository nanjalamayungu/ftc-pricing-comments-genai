# FTC PERSONALIZED-PRICING COMMENTS: GENAI WORKFLOW APP
# An interactive companion to Notebooks/ftc_genai_workflow.ipynb, organised by
# the four course competencies: Understand, Use, Evaluate, Govern.
# Every number comes from files the notebook saves (outputs/app/app_results.json,
# outputs/llm/labels_all_comments.csv, coding/human_review_queue.csv), so the
# app never recalculates or retypes a result.
#
# Run from the top folder of the repo:   streamlit run app.py

import html
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 1. Paths and page setup
ROOT = Path(__file__).resolve().parent                       # the repo's top folder (where app.py lives)
RESULTS_FILE = ROOT / "outputs" / "app" / "app_results.json"   # written by Section 15 of the notebook
LABELS_FILE = ROOT / "outputs" / "llm" / "labels_all_comments.csv"
REVIEW_FILE = ROOT / "coding" / "human_review_queue.csv"
DECISIONS_FILE = ROOT / "coding" / "review_decisions.csv"     # created by the Govern tab
WORDCLOUD_FILE = ROOT / "outputs" / "figures" / "word_cloud.png"

st.set_page_config(page_title="FTC Comments · GenAI Workflow", page_icon=":material/sell:", layout="wide")

# 2. Design tokens: one palette for the whole app (matches the slides)
NAVY, SLATE, RED, GREY, MID, LIGHT = "#1B2A41", "#324A5F", "#C8102E", "#5B7083", "#A7B4C2", "#EEF1F5"
GREEN, AMBER = "#2E8B57", "#E0A030"
COMP = {"Understand": "#6B5CA5", "Use": "#2F6DB5", "Evaluate": "#D9822B", "Govern": RED}   # competency colours

# 3. Page styling: fonts, cards, pills, hero banner
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap');
html, body, [class*="css"], .stMarkdown, .stText, p, li, label {{ font-family: 'Inter', sans-serif; }}
h1, h2, h3, .serif {{ font-family: 'Source Serif 4', Georgia, serif !important; color: {NAVY}; letter-spacing: -0.01em; }}
.block-container {{ padding-top: 1.2rem; max-width: 1320px; }}
.hero {{ background: linear-gradient(120deg, {NAVY} 0%, #24395A 60%, #2E4A70 100%); border-radius: 18px; padding: 30px 36px;
         color: white; margin-bottom: 14px; position: relative; overflow: hidden; }}
.hero:after {{ content: ""; position: absolute; right: -60px; top: -60px; width: 260px; height: 260px; border-radius: 50%;
               background: radial-gradient(circle, rgba(200,16,46,0.45) 0%, rgba(200,16,46,0) 70%); }}
.hero h1 {{ color: white !important; font-size: 2.3rem; margin: 0 0 6px 0; }}
.hero p {{ color: #D6DEEA; font-size: 1.05rem; margin: 0 0 14px 0; max-width: 820px; }}
.pill {{ display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 0.8rem; font-weight: 600; margin: 0 6px 6px 0; }}
.pill-ok {{ background: rgba(46,139,87,0.18); color: #9BE3B8; border: 1px solid rgba(46,139,87,0.6); }}
.pill-warn {{ background: rgba(200,16,46,0.22); color: #FFB3BF; border: 1px solid rgba(200,16,46,0.7); }}
.pill-info {{ background: rgba(255,255,255,0.10); color: #E6ECF5; border: 1px solid rgba(255,255,255,0.25); }}
.card {{ background: white; border: 1px solid #E3E8EF; border-radius: 14px; padding: 18px 20px; height: 100%;
         box-shadow: 0 1px 2px rgba(27,42,65,0.04), 0 6px 18px rgba(27,42,65,0.05); }}
.card h4 {{ font-family: 'Source Serif 4', serif; color: {NAVY}; margin: 0 0 6px 0; font-size: 1.12rem; }}
.card p, .card li {{ color: #44546A; font-size: 0.95rem; margin: 0; }}
.kpi {{ background: white; border: 1px solid #E3E8EF; border-radius: 14px; padding: 16px 18px; height: 100%;
        box-shadow: 0 6px 18px rgba(27,42,65,0.05); }}
.kpi .v {{ font-family: 'Source Serif 4', serif; font-size: 2.1rem; font-weight: 700; line-height: 1.1; }}
.kpi .l {{ font-size: 0.86rem; color: {GREY}; margin-top: 4px; }}
.eyebrow {{ text-transform: uppercase; letter-spacing: 0.14em; font-size: 0.74rem; font-weight: 700; margin-bottom: 2px; }}
.question {{ font-family: 'Source Serif 4', serif; font-size: 1.5rem; color: {NAVY}; margin: 0 0 4px 0; }}
.lead {{ color: #44546A; font-size: 1.0rem; margin-bottom: 10px; }}
.flow {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: stretch; }}
.step {{ flex: 1 1 140px; border-radius: 12px; padding: 12px 12px; color: white; min-height: 92px; position: relative; }}
.step b {{ display: block; font-size: 0.95rem; margin-bottom: 3px; }}
.step span {{ font-size: 0.8rem; opacity: 0.92; }}
.step i {{ position: absolute; right: 10px; top: 8px; font-style: normal; font-size: 0.72rem; opacity: 0.85; }}
.quote {{ border-left: 0; background: {LIGHT}; border-radius: 12px; padding: 16px 18px; font-size: 1.02rem; color: {NAVY}; line-height: 1.55; }}
.quote mark {{ background: rgba(200,16,46,0.16); color: {NAVY}; padding: 1px 2px; border-radius: 3px; }}
.banner {{ border-radius: 12px; padding: 14px 18px; font-weight: 600; margin: 8px 0; }}
.banner-ok {{ background: rgba(46,139,87,0.10); color: #1F6B41; border: 1px solid rgba(46,139,87,0.35); }}
.banner-bad {{ background: rgba(200,16,46,0.08); color: #9B0C24; border: 1px solid rgba(200,16,46,0.35); }}
.check {{ display: grid; grid-template-columns: 26px 1.6fr 0.8fr 1.4fr; gap: 10px; align-items: center;
          padding: 9px 4px; border-bottom: 1px solid #EEF1F5; font-size: 0.95rem; }}
.check .bar {{ height: 8px; border-radius: 6px; background: #EEF1F5; position: relative; }}
.check .fill {{ height: 8px; border-radius: 6px; position: absolute; left: 0; top: 0; }}
.check .tick {{ position: absolute; top: -4px; width: 2px; height: 16px; background: {NAVY}; }}
.tag {{ display: inline-block; padding: 2px 9px; border-radius: 999px; font-size: 0.78rem; font-weight: 600; background: {LIGHT}; color: {SLATE}; margin: 0 4px 4px 0; }}
div[data-baseweb="tab-list"] {{ gap: 6px; }}
button[data-baseweb="tab"], button[role="tab"] {{ font-size: 1.02rem; font-weight: 600; padding: 10px 18px; border-radius: 10px 10px 0 0; }}
</style>
""", unsafe_allow_html=True)


# 4. Small building blocks for the page
def card(title, body, color=None):
    """A white card with a serif title; an optional colour dot marks its competency."""
    dot = f'<span style="color:{color};font-size:1.1rem">●</span> ' if color else ""
    st.markdown(f'<div class="card"><h4>{dot}{title}</h4><p>{body}</p></div>', unsafe_allow_html=True)


def kpi(value, label, color=NAVY):
    """A big-number tile: the number in the competency colour, the label underneath."""
    st.markdown(f'<div class="kpi"><div class="v" style="color:{color}">{value}</div><div class="l">{label}</div></div>',
                unsafe_allow_html=True)


def section(eyebrow, question, lead, color):
    """Section header: competency name, the question it answers, and a one-line lead."""
    st.markdown(f'<div class="eyebrow" style="color:{color}">{eyebrow}</div><div class="question">{question}</div>'
                f'<div class="lead">{lead}</div>', unsafe_allow_html=True)


def style(fig, height=360, legend=False):
    """One chart style for every figure: Inter font, quiet grid, no clutter."""
    fig.update_layout(height=height, margin=dict(l=10, r=20, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", size=13, color=NAVY),
                      showlegend=legend, title_font=dict(family="Source Serif 4, serif", size=17, color=NAVY),
                      legend=dict(orientation="h", y=-0.18, x=0, font=dict(size=12)))
    fig.update_xaxes(gridcolor="#EEF1F5", zerolinecolor="#D5DCE6")
    fig.update_yaxes(gridcolor="#EEF1F5", zerolinecolor="#D5DCE6")
    return fig


def show(fig):
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def pretty(label):
    """'stronger_action' -> 'Stronger action' for display."""
    return str(label).replace("_", " ").capitalize()


# 5. Privacy and answer checks: the same rules as the notebook
def mask_names(t):
    """Masks names commenters typed into their text (same pattern as notebook Section 7.1)."""
    return re.sub(r"(?i)(submitter|submitted by|name|sincerely|regards|respectfully)\s*[:,]?\s*[A-Z][\w.\-]*(\s+[A-Z][\w.\-]*){0,3}",
                  r"\1: [NAME]", t)


def normalize(t):
    return re.sub(r"\s+", " ", str(t)).strip().lower()


def parse_answer(raw, comment_text, stances, reasons):
    """Checks Claude's answer exactly as the notebook does: valid JSON, valid labels, quote really in the comment."""
    out = {"stance": "INVALID", "reasons": [], "evidence_quote": "", "confidence": "low",
           "parse_error": False, "invalid_reason_label": False, "quote_found": False}
    try:
        ans = json.loads(re.search(r"\{.*\}", raw, re.S).group(0))
    except Exception:
        out["parse_error"] = True
        return out
    out["stance"] = ans.get("stance") if ans.get("stance") in stances else "INVALID"
    rs = ans.get("reasons") or []
    rs = rs if isinstance(rs, list) else [rs]
    out["invalid_reason_label"] = any(r not in reasons for r in rs)
    out["reasons"] = sorted({r for r in rs if r in reasons})
    out["evidence_quote"] = str(ans.get("evidence_quote", ""))
    out["confidence"] = ans.get("confidence") if ans.get("confidence") in ("low", "medium", "high") else "low"
    q = normalize(out["evidence_quote"]).strip(" .\"'")
    out["quote_found"] = bool(q) and q in normalize(comment_text)
    return out


def highlight(text, quote):
    """Escapes the comment for HTML and highlights Claude's evidence quote inside it."""
    safe = html.escape(text)
    q = html.escape(str(quote or "")).strip()
    if q and q.lower() in safe.lower():
        i = safe.lower().index(q.lower())
        safe = safe[:i] + "<mark>" + safe[i:i + len(q)] + "</mark>" + safe[i + len(q):]
    return safe.replace("\n", "<br>")


# 6. Load the saved results (cached, so the app stays fast)
@st.cache_data
def load_results():
    return json.loads(RESULTS_FILE.read_text(encoding="utf-8"))


@st.cache_data
def load_comments():
    """The labelled comments joined with their (cleaned, name-masked) text."""
    labels = pd.read_csv(LABELS_FILE)
    data_file = ROOT / "Data" / "Used_individuals_sentiment_data.csv"   # the same file the notebook analyses
    raw = pd.read_csv(data_file)
    raw["text"] = (raw["comment_text"].astype(str).map(html.unescape).str.replace("\r\n", "\n")
                   .str.replace(r"[ \t]+", " ", regex=True).str.strip().map(mask_names))
    out = labels.merge(raw[["comment_id", "text"]], on="comment_id", how="left")
    out["reasons"] = out["reasons"].fillna("none")
    out["reason_list"] = out["reasons"].map(lambda s: [] if s == "none" else [x.strip() for x in s.split(";")])
    return out


for f, what in [(RESULTS_FILE, "run Section 15 of the notebook"), (LABELS_FILE, "run the notebook's production run (Section 9)")]:
    if not f.exists():
        st.error(f"Missing `{f.relative_to(ROOT)}`: {what}, then reload this page.")
        st.stop()

R = load_results()
C = load_comments()
S = R["settings"]
T = R["thresholds"]
gov = pd.DataFrame(R["governance"])
stance_scores = pd.DataFrame(R["stance_scores"])
best = stance_scores.set_index("model").loc[S["best"]]
n_pass, n_checks = int(gov["passed"].sum()), len(gov)
STANCES, REASONS = list(R["dictionary"]["stance"]), list(R["dictionary"]["reasons"])


# 7. Hero banner: what this is, and how far to trust it
status_pills = "".join(
    f'<span class="pill {"pill-ok" if v == "validated" else "pill-warn"}">{k.capitalize()}: {v}</span>' for k, v in R["status"].items())
st.markdown(f"""
<div class="hero">
  <div class="eyebrow" style="color:#FF8FA1">FTC docket FTC-2026-1057 · personalized pricing</div>
  <h1>Can GenAI read the public record?</h1>
  <p>{R['data']['comments']:,} public comments, labelled by Claude and checked against two human coders.
     Explore the workflow the way the course frames it: Understand, Use, Evaluate, Govern.</p>
  {status_pills}
  <span class="pill {'pill-ok' if n_pass == n_checks else 'pill-warn'}">{n_pass} of {n_checks} governance checks passed</span>
  <span class="pill pill-info">{'Automatic reporting allowed' if n_pass == n_checks else 'Human review required before reporting'}</span>
  <span class="pill pill-info">{S['model']} · prompt {S['prompt_version']}</span>
</div>
""", unsafe_allow_html=True)

tab_u, tab_use, tab_e, tab_g = st.tabs([":material/lightbulb: Understand", ":material/build: Use",
                                        ":material/query_stats: Evaluate", ":material/verified_user: Govern"])


# 8. UNDERSTAND: the use case, and what AI does vs what people do
with tab_u:
    section("Understand", "What can and can't AI do for this task?",
            "The business problem, who needs the answer, and where the AI fits in the workflow.", COMP["Understand"])

    c1, c2 = st.columns([1.35, 1])
    with c1:
        card("The business problem",
             "Regulators, law firms and public-affairs teams must read and summarize thousands of public comments by hand. "
             "GenAI could do it faster and more cheaply, but a misread comment misrepresents the public record, so its accuracy "
             "has to be measured against careful human judgment before anyone relies on it.", COMP["Understand"])
    with c2:
        card("The case",
             f"In August 2026 the FTC proposed that hidden personalized pricing (prices set from a person's own data) may be unlawful. "
             f"It requires <b>disclosure</b>; it does <b>not</b> ban the practice. {R['data']['docket_total']:,} comments came in; "
             f"we study the {R['data']['comments']:,} from individuals.", RED)

    st.write("")
    a1, a2 = st.columns(2)
    with a1:
        card("Organizations deciding whether to use GenAI",
             "1. How accurately does it classify comments?<br>2. What does it cost?<br>3. Where does it fail?<br>"
             "4. What controls make it safe?", COMP["Evaluate"])
    with a2:
        card("Companies that use personalized pricing",
             "5. What do commenters object to: the price difference, their data, or the lack of disclosure?<br>"
             "6. What do they want the FTC to do?", COMP["Use"])

    st.write("")
    st.markdown('<div class="eyebrow" style="color:#6B5CA5">The workflow</div>', unsafe_allow_html=True)
    steps = [("Business question", "6 questions, 2 audiences", "Understand", "1"), ("Collect", "Regulations.gov API", "Use", "2"),
             ("Clean and check", "assertions, name masking", "Use", "3"), ("Explore", "stats, word cloud, topics", "Use", "4-6"),
             ("Coding dictionary", "5 stances, 7 reasons", "Understand", "7.4"), ("Hand-code", "2 coders, 100 comments", "Evaluate", "8.1"),
             ("Models", "baselines + Claude", "Use", "7"), ("Evaluate", "F1, kappa, CI, MDD", "Evaluate", "8"),
             ("Label all", "best Claude version", "Use", "9"), ("Govern", "back-tests, risk matrix", "Govern", "10-12"),
             ("Recommend", "answers to 6 questions", "Govern", "13")]
    st.markdown('<div class="flow">' + "".join(
        f'<div class="step" style="background:{COMP[c]}"><i>§{s}</i><b>{t}</b><span>{d}</span></div>' for t, d, c, s in steps)
        + "</div>", unsafe_allow_html=True)
    st.caption("Colours show the competency each step demonstrates; § is the notebook section.")

    st.write("")
    w1, w2, w3 = st.columns([1, 1, 1.2])
    with w1:
        card("Claude does", f"Labels all {R['data']['comments']:,} comments with a stance, reasons, an exact supporting quote and "
                            "a confidence rating, using the same coding dictionary as the human coders.", COMP["Use"])
    with w2:
        card("People do", "Write the rules, hand-code 100 comments to build the gold standard, set thresholds before seeing results, "
                          f"and review the {R['review_total'] / R['data']['comments']:.0%} of comments the system flags.", COMP["Govern"])
    with w3:
        # Why not a simpler tool? Tone is not a position.
        vader = R["data"]["vader"]
        vs = stance_scores.set_index("model")
        fig = go.Figure(go.Bar(x=[vs.loc["VADER baseline", "macro_f1"], best["macro_f1"]], y=["Tone (VADER)", S["best"]],
                               orientation="h", marker_color=[MID, RED],
                               text=[f"{vs.loc['VADER baseline', 'macro_f1']:.2f}", f"{best['macro_f1']:.2f}"], textposition="outside"))
        fig.update_layout(title=f"Why AI? {vader.get('negative', 0):.0%} of comments sound negative,<br>but tone can't tell what people want")
        fig.update_xaxes(range=[0, 1.1], title="Stance score (macro-F1)")
        show(style(fig, 230))

    with st.expander("The coding dictionary: what every label means"):
        d1, d2 = st.columns(2)
        with d1:
            st.markdown("**Stance** (exactly one): *what does this commenter want the FTC to do?*")
            for k, v in R["dictionary"]["stance"].items():
                st.markdown(f"- **{pretty(k)}**: {v}")
        with d2:
            st.markdown("**Reasons** (zero or more): *what arguments do they use?*")
            for k, v in R["dictionary"]["reasons"].items():
                st.markdown(f"- **{pretty(k)}**: {v}")


# 9. USE: the data, the AI step, the findings, and a live classifier
with tab_use:
    section("Use", "Did we build it well, and what did it find?",
            "Clean data, a documented AI step, the findings, and the classifier running live.", COMP["Use"])

    D = R["data"]
    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi(f"{D['comments']:,}", f"individual comments ({D['comments'] / D['docket_total']:.0%} of the docket)", COMP["Use"])
    with k2: kpi(f"{D['median_words']:.0f}", "median words per comment", COMP["Use"])
    with k3: kpi(f"{D['near_duplicates'] / D['comments']:.1%}", f"form letters ({D['duplicate_groups']} groups), flagged and checked", COMP["Use"])
    with k4: kpi(f"{sum(v for k, v in D['topics'].items() if k in D['ban_topics']):.0%}", "of comments mainly about wanting a ban (topics)", RED)

    st.write("")
    e1, e2 = st.columns([1.15, 1])
    with e1:
        if WORDCLOUD_FILE.exists():
            st.image(str(WORDCLOUD_FILE), caption="Most frequent words, common ones removed", width="stretch")
    with e2:
        tp = pd.Series(D["topics"]).sort_values()
        fig = go.Figure(go.Bar(x=tp.values * 100, y=tp.index, orientation="h",
                               marker_color=[RED if t in D["ban_topics"] else COMP["Use"] for t in tp.index],
                               text=[f"{v:.0%}" for v in tp.values], textposition="outside"))
        fig.update_layout(title="Themes found by the topic model (red = about a ban)")
        fig.update_xaxes(title="Share of comments (%)", range=[0, tp.max() * 120])
        show(style(fig, 330))

    st.write("")
    st.markdown('<div class="eyebrow" style="color:#2F6DB5">The AI step</div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    with s1: card("Model", f"{S['model']}<br>effort: {S['effort'] or 'default'} · max {S['max_output_tokens']:,} tokens", COMP["Use"])
    with s2: card("Prompt", f"Built from the coding dictionary (version {S['prompt_version']}); {S['best']} chosen in evaluation", COMP["Use"])
    with s3: card("Output", "JSON: stance, reasons, an exact quote from the comment, and low / medium / high confidence", COMP["Use"])
    with s4: card("Checks", "Valid labels, quote really in the comment, names masked, every answer saved so reruns are free", COMP["Use"])
    with st.expander("See the exact prompt sent to Claude"):
        st.code(S["system_prompt"], language="text")

    # Findings
    st.write("")
    st.markdown('<div class="eyebrow" style="color:#C8102E">What the workflow found</div>', unsafe_allow_html=True)
    f1c, f2c = st.columns(2)
    with f1c:
        stt = pd.DataFrame(R["stance_tab"]).set_index("stance").reindex(STANCES).iloc[::-1]
        fig = go.Figure(go.Bar(x=stt["share"] * 100, y=[f"{pretty(s)}  <b>{v:.1%}</b>" for s, v in zip(stt.index, stt["share"])], orientation="h",
                               marker_color=[RED if s == "stronger_action" else GREY for s in stt.index],
                               error_x=dict(type="data", symmetric=False, array=(stt["ci_high"] - stt["share"]).clip(lower=0) * 100,
                                            arrayminus=(stt["share"] - stt["ci_low"]).clip(lower=0) * 100, color=NAVY, thickness=1.2),
                               ))
        fig.update_layout(title="Part A · What they want the FTC to do (Q6)")
        fig.update_xaxes(title="Share of comments (%), 95% CI", range=[0, stt["ci_high"].max() * 118])
        show(style(fig, 340))
    with f2c:
        pt = pd.DataFrame(R["practice_tab"]).set_index("group")
        ev = R["unsaid_evidence"]
        against = pt.iloc[0]
        fig = go.Figure(go.Pie(labels=[f"{n}  {v:.1%}" for n, v in zip(["Against the practice", "Partly against", "Against the FTC's rules", "Did not say"], pt["share"])],
                               values=pt["share"].values, hole=0.62, sort=False,
                               marker=dict(colors=[RED, AMBER, SLATE, MID]), textinfo="none"))
        fig.update_layout(title="Part B · View of personalized pricing itself",
                          annotations=[dict(text=f"<b>{against['share']:.0%}+</b><br>against", x=0.5, y=0.5, showarrow=False,
                                            font=dict(size=22, family="Source Serif 4", color=RED))])
        show(style(fig, 340, legend=True))
        st.caption(f"A validated minimum (95% CI {against['ci_low']:.0%}–{against['ci_high']:.0%}). Of those who did not say what should "
                   f"happen, {list(ev.values())[0]:.0%} still give an objection; no stance defends the practice.")

    r1c, r2c = st.columns(2)
    with r1c:
        rt = pd.DataFrame(R["reason_tab"]).set_index("reason").sort_values("share")
        fig = go.Figure(go.Bar(x=rt["share"] * 100, y=[f"{pretty(r)}  <b>{v:.0%}</b>" for r, v in zip(rt.index, rt["share"])], orientation="h",
                               marker_color=[RED if r == "transparency_disclosure" else NAVY for r in rt.index],
                               error_x=dict(type="data", symmetric=False, array=(rt["ci_high"] - rt["share"]).clip(lower=0) * 100,
                                            arrayminus=(rt["share"] - rt["ci_low"]).clip(lower=0) * 100, color=GREY, thickness=1.2),
                               ))
        fig.update_layout(title="Why they object (Q5) · disclosure in red")
        fig.update_xaxes(title="Share of comments (%), 95% CI", range=[0, rt["ci_high"].max() * 112])
        show(style(fig, 360))
    with r2c:
        rb = pd.DataFrame(R["reasons_by_stance"]).sort_values("share_if_stronger_action")
        fig = go.Figure()
        for _, r in rb.iterrows():   # a line joining the two groups' shares for each reason
            fig.add_shape(type="line", x0=r["share_if_other_stance"] * 100, x1=r["share_if_stronger_action"] * 100,
                          y0=pretty(r["reason"]), y1=pretty(r["reason"]), line=dict(color=MID, width=3))
        fig.add_trace(go.Scatter(x=rb["share_if_other_stance"] * 100, y=[pretty(r) for r in rb["reason"]], mode="markers",
                                 name="All other stances", marker=dict(size=13, color=GREY)))
        fig.add_trace(go.Scatter(x=rb["share_if_stronger_action"] * 100, y=[pretty(r) for r in rb["reason"]], mode="markers+text",
                                 name="Want stronger action", marker=dict(size=13, color=RED),
                                 text=[f"  V={v:.2f}" for v in rb["cramers_v"]], textposition="middle right",
                                 textfont=dict(size=11, color=GREY)))
        fig.update_layout(title="Ban supporters raise privacy far more often")
        fig.update_xaxes(title="Share of each group giving the reason (%)", range=[0, rb["share_if_stronger_action"].max() * 125])
        show(style(fig, 360, legend=True))

    # Explore comments
    st.write("")
    st.markdown('<div class="eyebrow" style="color:#2F6DB5">Explore the comments</div>', unsafe_allow_html=True)
    x1, x2, x3, x4 = st.columns([1.2, 1.2, 1, 1.4])
    with x1: f_stance = st.multiselect("Stance", STANCES, format_func=pretty)
    with x2: f_reason = st.multiselect("Reason", REASONS, format_func=pretty)
    with x3: f_conf = st.multiselect("Confidence", ["high", "medium", "low"])
    with x4: f_text = st.text_input("Search the text", placeholder="e.g. groceries, insurance, airline")
    view = C.copy()
    if f_stance: view = view[view["stance"].isin(f_stance)]
    if f_reason: view = view[view["reason_list"].map(lambda rs: any(r in rs for r in f_reason))]
    if f_conf: view = view[view["confidence"].isin(f_conf)]
    if f_text: view = view[view["text"].str.contains(f_text, case=False, na=False)]
    st.caption(f"{len(view):,} of {len(C):,} comments match")
    table = view[["comment_id", "text", "stance", "reasons", "confidence", "quote_found"]].rename(columns={
        "comment_id": "Comment", "text": "Text", "stance": "Stance", "reasons": "Reasons", "confidence": "Confidence",
        "quote_found": "Quote found"})
    picked = st.dataframe(table, width="stretch", height=300, hide_index=True, on_select="rerun",
                          selection_mode="single-row",
                          column_config={"Text": st.column_config.TextColumn(width="large"),
                                         "Quote found": st.column_config.CheckboxColumn()})
    sel = picked.selection.rows if picked and hasattr(picked, "selection") else []
    if sel:
        row = view.iloc[sel[0]]
        st.markdown(f'<div class="quote">{highlight(row["text"], row["evidence_quote"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="tag">Stance: {pretty(row["stance"])}</span><span class="tag">Confidence: {row["confidence"]}</span>'
                    + "".join(f'<span class="tag">{pretty(r)}</span>' for r in row["reason_list"]), unsafe_allow_html=True)
    else:
        st.caption("Select a row to read the full comment with Claude's evidence quote highlighted.")

    # Live classifier
    st.write("")
    st.markdown('<div class="eyebrow" style="color:#C8102E">Try it live</div>', unsafe_allow_html=True)
    st.markdown('<div class="lead">Paste any comment. Claude labels it with the exact prompt and checks from the notebook, '
                'and the governance rules decide whether it can be used or must go to a person.</div>', unsafe_allow_html=True)
    examples = {"Write your own": ""} | {f"Gold-set error · {e['comment_id']}": e["text"] for e in R["errors"]}
    ex = st.selectbox("Start from an example (real comments Claude got wrong in evaluation)", list(examples))
    live_text = st.text_area("Comment", value=examples[ex], height=130, placeholder="Paste a public comment here")
    if S["best_variant"] != "zeroshot":
        st.caption("Note: the live classifier uses the dictionary prompt without the few-shot examples.")
    if st.button("Classify with Claude", type="primary", disabled=not live_text.strip()):
        try:
            import anthropic
            from dotenv import load_dotenv
            load_dotenv(ROOT / ".env")
            if not os.environ.get("ANTHROPIC_API_KEY"):
                st.error("No ANTHROPIC_API_KEY found in .env")
                st.stop()
            text = mask_names(live_text.strip())
            kwargs = dict(model=S["model"], max_tokens=S["max_output_tokens"], system=S["system_prompt"],
                          messages=[{"role": "user", "content": f"COMMENT:\n{text}"}])
            if S["effort"]:
                kwargs["output_config"] = {"effort": S["effort"]}
            with st.spinner("Claude is reading the comment..."):
                t0 = time.time()
                resp = anthropic.Anthropic().messages.create(**kwargs)
                secs = time.time() - t0
            raw = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
            a = parse_answer(raw, text, STANCES, REASONS)
            cost = (resp.usage.input_tokens * S["price_in_per_mtok"] + resp.usage.output_tokens * S["price_out_per_mtok"]) / 1e6
            n_words = len(text.split())

            # The governance rules applied to this one answer
            flags = []
            if a["parse_error"] or a["stance"] == "INVALID" or a["invalid_reason_label"]: flags.append("invalid answer")
            if a["confidence"] == "low": flags.append("low confidence")
            if not a["quote_found"]: flags.append("quote not found in the comment")
            if n_words > 50: flags.append("long comment (the length check failed in evaluation)")

            o1, o2, o3 = st.columns(3)
            with o1: kpi(pretty(a["stance"]), "stance", RED if a["stance"] == "stronger_action" else NAVY)
            with o2: kpi(a["confidence"].capitalize(), "Claude's confidence", {"high": GREEN, "medium": AMBER}.get(a["confidence"], RED))
            with o3: kpi(f"${cost:.4f}", f"cost of this call · {secs:.1f} s", GREY)
            st.markdown(f'<div class="quote" style="margin-top:12px">{highlight(text, a["evidence_quote"])}</div>', unsafe_allow_html=True)
            st.markdown("".join(f'<span class="tag">{pretty(r)}</span>' for r in a["reasons"]) or '<span class="tag">No reason given</span>',
                        unsafe_allow_html=True)
            if flags:
                st.markdown(f'<div class="banner banner-bad">Send to human review: {"; ".join(flags)}.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="banner banner-ok">Passes the automatic checks (the 5% random audit still applies).</div>',
                            unsafe_allow_html=True)
        except Exception as err:
            st.error(f"The live call failed: {err}")


# 10. EVALUATE: how do we know it works?
with tab_e:
    section("Evaluate", "How do we know it works?",
            "Claude scored against an 80-comment gold standard coded independently by two people, with confidence intervals, "
            "the minimum detectable difference, failure analysis and cost.", COMP["Evaluate"])

    hs = R["human"]["stance"][0]
    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi(f"{hs['kappa']:.2f}", f"coders agree with each other (kappa, CI {hs['kappa_ci_low']:.2f}–{hs['kappa_ci_high']:.2f})", COMP["Evaluate"])
    with k2: kpi(f"{best['macro_f1']:.2f}", f"{S['best']} stance F1 (95% CI {best['f1_ci_low']:.2f}–{best['f1_ci_high']:.2f})", RED)
    with k3: kpi(f"{best['kappa_vs_gold']:.2f}", "Claude agrees with the gold standard (kappa)", COMP["Evaluate"])
    with k4: kpi(f"±{R['mdd_single']:.2f}", "minimum detectable difference for one score (80 comments)", GREY)

    st.write("")
    m1, m2 = st.columns(2)
    with m1:
        ss = stance_scores.sort_values("macro_f1")
        fig = go.Figure(go.Bar(x=ss["macro_f1"], y=[f"{m}  <b>{v:.2f}</b>" for m, v in zip(ss["model"], ss["macro_f1"])], orientation="h",
                               marker_color=[RED if m.startswith("Claude") else MID for m in ss["model"]],
                               error_x=dict(type="data", symmetric=False, array=(ss["f1_ci_high"] - ss["macro_f1"]).clip(lower=0),
                                            arrayminus=(ss["macro_f1"] - ss["f1_ci_low"]).clip(lower=0), color=NAVY, thickness=1.2),
                               ))
        fig.add_vline(x=T["min_stance_macro_f1"], line_dash="dash", line_color=RED, annotation_position="bottom right",
                      annotation_text=f"threshold {T['min_stance_macro_f1']}", annotation_font_color=RED)
        fig.update_layout(title="Accuracy vs the gold standard (Q1)")
        fig.update_xaxes(title="Stance macro-F1 with 95% bootstrap CI", range=[0, 1.05])
        show(style(fig, 360))
    with m2:
        md = pd.DataFrame(R["mdd"]).sort_values("observed_gap")
        band = md["mdd"].median()
        fig = go.Figure()
        fig.add_vrect(x0=-band, x1=band, fillcolor=LIGHT, line_width=0,
                      annotation_text="within noise", annotation_position="top left", annotation_font_color=GREY)
        fig.add_vline(x=0, line_color=NAVY, line_width=1)
        fig.add_trace(go.Scatter(x=md["observed_gap"], y=[f"vs {c.split(' vs ')[1]}  <b>{g:+.2f} {'real' if r else 'tie'}</b>"
                                                          for c, g, r in zip(md["comparison"], md["observed_gap"], md["real_difference"])], mode="markers",
                                 marker=dict(size=14, color=[RED if r else GREY for r in md["real_difference"]]),
                                 error_x=dict(type="data", symmetric=False, array=(md["gap_ci_high"] - md["observed_gap"]).clip(lower=0),
                                              arrayminus=(md["observed_gap"] - md["gap_ci_low"]).clip(lower=0), color=NAVY),
                                 ))
        fig.update_layout(title=f"Which gaps are real? {S['best']} minus each model")
        fig.update_xaxes(title=f"Gap in F1 (95% CI); grey = noise (MDD {band:.2f})",
                         range=[min(-band, md["gap_ci_low"].min()) - 0.05, md["gap_ci_high"].max() + 0.08])
        show(style(fig, 360))
    st.caption(f"Zero-shot vs few-shot: McNemar p = {R['mcnemar_p']:.2f}. The minimum detectable difference is 2.8 × the standard error "
               "of the gap (5% significance, 80% power), from a paired bootstrap.")

    c1, c2 = st.columns([1, 1.1])
    with c1:
        cm = np.array(R["confusion"]["matrix"])
        labs = [pretty(l) for l in R["confusion"]["labels"]]
        fig = go.Figure(go.Heatmap(z=cm, x=labs, y=labs, colorscale=[[0, "#FFFFFF"], [0.15, "#F3C9D0"], [1, RED]], showscale=False,
                                   text=cm, texttemplate="%{text}", textfont=dict(size=14)))
        fig.update_layout(title=f"Confusion matrix ({S['best']})")
        fig.update_xaxes(title="Claude", tickangle=-30)
        fig.update_yaxes(title="Gold standard", autorange="reversed")
        show(style(fig, 400))
    with c2:
        pc = pd.DataFrame(R["stance_per_class"])
        pc = pc[pc["model"] == S["best"]]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Precision", y=[f"{pretty(s)} (n={g})" for s, g in zip(pc["stance"], pc["gold_examples"])],
                             x=pc["precision"], orientation="h", marker_color=NAVY))
        fig.add_trace(go.Bar(name="Recall", y=[f"{pretty(s)} (n={g})" for s, g in zip(pc["stance"], pc["gold_examples"])],
                             x=pc["recall"], orientation="h", marker_color=COMP["Evaluate"]))
        fig.update_layout(title="Per-stance precision and recall", barmode="group")
        fig.update_xaxes(range=[0, 1.05])
        show(style(fig, 400, legend=True))

    st.write("")
    st.markdown('<div class="eyebrow" style="color:#D9822B">Where it fails (Q3)</div>', unsafe_allow_html=True)
    l1, l2, l3 = st.columns([1.1, 1.1, 0.9])
    with l1:
        ls = pd.DataFrame(R["length_slices"])
        fig = go.Figure(go.Bar(x=ls["length"], y=ls["error_rate"] * 100, marker_color=[RED if f else MID for f in ls["flag"]],
                               text=[f"{v:.0%}" for v in ls["error_rate"]], textposition="outside", cliponaxis=False))
        fig.update_layout(title="Errors rise with comment length")
        fig.update_yaxes(title="Stance error rate (%)", range=[0, ls["error_rate"].max() * 135])
        show(style(fig, 320))
    with l2:
        ce = pd.DataFrame(R["confidence_errors"]).set_index("confidence").reindex(["high", "medium", "low"]).reset_index()
        fig = go.Figure(go.Bar(x=ce["confidence"], y=ce["stance_error_rate"] * 100, marker_color=[GREEN, AMBER, RED],
                               text=[f"{v:.0%}" for v in ce["stance_error_rate"]], textposition="outside", cliponaxis=False))
        fig.update_layout(title="Its own confidence predicts its errors")
        fig.update_xaxes(title="Claude's confidence")
        fig.update_yaxes(title="Stance error rate (%)", range=[0, ce["stance_error_rate"].max() * 135])
        show(style(fig, 320))
    with l3:
        fig = go.Figure(go.Indicator(mode="gauge+number", value=R["stability"] * 100, number=dict(suffix="%", font=dict(size=40)),
                                     gauge=dict(axis=dict(range=[50, 100]), bar=dict(color=COMP["Evaluate"]),
                                                threshold=dict(line=dict(color=RED, width=3), value=T["min_stability"] * 100))))
        fig.update_layout(title="Same stance in all 3 runs")
        style(fig, 320)
        fig.update_layout(margin=dict(l=40, r=50, t=60, b=10))
        show(fig)

    rp = pd.DataFrame(R["reason_per_class"])
    rp = rp[rp["model"].str.startswith("Claude")]
    fig = go.Figure()
    for mname, col in [("Claude zero-shot", RED), ("Claude few-shot", NAVY)]:
        sub = rp[rp["model"] == mname]
        fig.add_trace(go.Bar(name=mname, y=[f"{pretty(r)} (n={g})" for r, g in zip(sub["reason"], sub["gold_examples"])],
                             x=sub["f1"], marker_color=col, orientation="h"))
    fig.update_layout(title="Reason F1 by category", barmode="group")
    fig.update_xaxes(title="F1 against the gold standard", range=[0, 1.05])
    fig.update_yaxes(autorange="reversed")
    show(style(fig, 420, legend=True))

    with st.expander(f"The {len(R['errors'])} stance errors on the gold set"):
        cols = st.columns(2)
        for i, e in enumerate(R["errors"]):
            with cols[i % 2]:
                st.markdown(f'<div class="card" style="margin-bottom:10px"><h4>{e["comment_id"]}</h4>'
                            f'<p style="margin-bottom:8px">{html.escape(e["text"][:420])}{"…" if len(e["text"]) > 420 else ""}</p>'
                            f'<span class="tag">Gold: {pretty(e["gold"])}</span><span class="tag" style="background:#FBE3E7;color:{RED}">'
                            f'Claude: {pretty(e["claude"])}</span><span class="tag">Confidence: {e["confidence"]}</span></div>',
                            unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="eyebrow" style="color:#D9822B">Cost (Q2)</div>', unsafe_allow_html=True)
    pj = pd.DataFrame(R["projection"])
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi(f"${C.shape[0] * R['llm_cost_per_comment']:.2f}", f"to label all {C.shape[0]:,} comments", RED)
    with c2: kpi(f"${R['llm_cost_per_comment'] * 1000:.2f}", "per 1,000 comments with Claude", COMP["Evaluate"])
    with c3: kpi(f"{R['llm_seconds_per_comment']:.1f} s", "per comment with Claude, one at a time", COMP["Evaluate"])
    with c4: kpi(f"{R['human_minutes_for_gold']:.0f} min", "estimated per coder for 80 gold comments", GREY)
    fig = go.Figure()
    for colname, label, col in [("llm_cost_usd", "Claude only", RED), ("llm_plus_review_usd", "Claude + 5% human audit", COMP["Evaluate"]),
                                ("human_cost_usd", "Human coding only", MID)]:
        fig.add_trace(go.Bar(name=label, x=[f"{n:,}" for n in pj["comments"]], y=pj[colname], marker_color=col,
                             text=[f"${v:,.0f}" if v >= 1 else f"${v:.2f}" for v in pj[colname]], textposition="outside", cliponaxis=False))
    fig.update_layout(title="Projected cost of labeling comments", barmode="group")
    fig.update_yaxes(type="log", title="US dollars (log scale)")
    fig.update_xaxes(title="Number of comments", type="category")
    show(style(fig, 380, legend=True))
    st.caption(f"Claude cost measured from logged tokens (total spent on the API in this project: ${R['total_api_cost']:.2f}). "
               "Human time estimated from comment length; reconciliation not included.")


# 11. GOVERN: the rules for using it
with tab_g:
    section("Govern", "What are the rules for using it?",
            "Thresholds fixed before any results were seen, what happens when one is crossed, and the human review in practice.",
            COMP["Govern"])

    g1, g2 = st.columns([1.45, 1])
    with g1:
        rows_html = ""
        for _, r in gov.iterrows():
            ok = bool(r["passed"])
            # Bar: value on a 0-1 scale (ratios over 1 are scaled to their own maximum), tick = threshold
            scale = max(r["value"], r["threshold"]) * 1.15 if max(r["value"], r["threshold"]) > 1 else 1.0
            fill = min(r["value"] / scale, 1) * 100
            tick = min(r["threshold"] / scale, 1) * 100
            rows_html += (f'<div class="check"><span style="color:{GREEN if ok else RED};font-size:1.2rem">{"✔" if ok else "✖"}</span>'
                          f'<span style="font-weight:{500 if ok else 700};color:{NAVY if ok else RED}">{r["check"]}</span>'
                          f'<span style="font-weight:600;color:{SLATE if ok else RED}">{r["value"]:g} {r["rule"]} {r["threshold"]:g}</span>'
                          f'<div class="bar"><div class="fill" style="width:{fill:.0f}%;background:{GREEN if ok else RED}"></div>'
                          f'<div class="tick" style="left:{tick:.0f}%"></div></div></div>')
        st.markdown(f'<div class="card"><h4>{n_pass} of {n_checks} checks passed</h4>{rows_html}'
                    f'<p style="margin-top:8px;font-size:0.82rem">Bar = measured value; black tick = threshold.</p></div>',
                    unsafe_allow_html=True)
    with g2:
        rules = [("If any check fails", "Results are reported only together with human review of the flagged comments.", RED),
                 ("If invalid answers exceed 2%", "Stop the run and fix the prompt before continuing.", NAVY),
                 ("Every comment that is", "low confidence, has a quote not found in the text, or is invalid goes to the review queue.", NAVY),
                 ("Every run", f"A {T['audit_share']:.0%} random audit is re-checked by a person, even when every check passes.", NAVY),
                 ("When the model or prompt changes", "Re-run the gold-standard evaluation before using the new version.", NAVY)]
        for title, body, col in rules:
            st.markdown(f'<div class="card" style="margin-bottom:8px;padding:12px 16px"><h4 style="color:{col}">{title}</h4><p>{body}</p></div>',
                        unsafe_allow_html=True)

    st.write("")
    k1, k2, k3, k4 = st.columns(4)
    rc = R["review_counts"]
    with k1: kpi(f"{R['review_total']:,}", f"comments in the review queue ({R['review_total'] / len(C):.0%})", RED)
    with k2: kpi(f"{rc.get('low confidence', 0):,}", "low confidence", COMP["Govern"])
    with k3: kpi(f"{rc.get('quote not found', 0):,}", "quote not found in the comment", COMP["Govern"])
    with k4: kpi(f"{R['audit_total']:,}", f"random audit ({T['audit_share']:.0%} of every run)", NAVY)

    # The review workbench
    st.write("")
    st.markdown('<div class="eyebrow" style="color:#C8102E">Human review queue</div>', unsafe_allow_html=True)
    if not REVIEW_FILE.exists():
        st.info("No review queue yet: run Section 10 of the notebook.")
    else:
        queue = pd.read_csv(REVIEW_FILE).merge(C[["comment_id", "text", "reason_list"]], on="comment_id", how="left")
        done = pd.read_csv(DECISIONS_FILE) if DECISIONS_FILE.exists() else pd.DataFrame(
            columns=["comment_id", "decision", "claude_stance", "final_stance", "note", "reviewed_at"])
        todo = queue[~queue["comment_id"].isin(done["comment_id"])]
        p1, p2 = st.columns([3, 1])
        with p1:
            st.progress(len(done) / max(len(queue), 1), text=f"{len(done)} of {len(queue)} reviewed")
        with p2:
            if len(done):
                agree = (done["decision"] == "agree").mean()
                st.markdown(f'<span class="tag">Reviewers agreed with Claude: {agree:.0%}</span>', unsafe_allow_html=True)
        if todo.empty:
            st.success("Every flagged comment has been reviewed.")
        else:
            q = todo.iloc[0]
            st.markdown(f'<span class="tag" style="background:#FBE3E7;color:{RED}">Flagged: {q["reason_for_review"]}</span>'
                        f'<span class="tag">{q["comment_id"]}</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="quote">{highlight(str(q["text"]), q["evidence_quote"])}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="tag">Claude: {pretty(q["stance"])}</span><span class="tag">Confidence: {q["confidence"]}</span>'
                        + "".join(f'<span class="tag">{pretty(r)}</span>' for r in (q["reason_list"] if isinstance(q["reason_list"], list) else [])),
                        unsafe_allow_html=True)
            with st.form("review", clear_on_submit=True):
                d1, d2 = st.columns([1, 1.4])
                with d1:
                    decision = st.radio("Is Claude's stance right?", ["agree", "correct it"], horizontal=True)
                with d2:
                    final = st.selectbox("Correct stance (used if you choose 'correct it')", STANCES,
                                         index=STANCES.index(q["stance"]) if q["stance"] in STANCES else 0, format_func=pretty)
                note = st.text_input("Note (optional)")
                if st.form_submit_button("Save decision and show the next comment", type="primary"):
                    new = pd.DataFrame([{"comment_id": q["comment_id"], "decision": "agree" if decision == "agree" else "corrected",
                                         "claude_stance": q["stance"], "final_stance": q["stance"] if decision == "agree" else final,
                                         "note": note, "reviewed_at": datetime.now().isoformat(timespec="seconds")}])
                    pd.concat([done, new], ignore_index=True).to_csv(DECISIONS_FILE, index=False)
                    st.rerun()
            st.caption("Decisions are saved to coding/review_decisions.csv. The agreement rate is a live check on the model.")

st.markdown(f'<p style="text-align:center;color:{GREY};font-size:0.8rem;margin-top:30px">'
            f'Every number on this page comes from the notebook (outputs/app/app_results.json) · seed {S["seed"]} · '
            f'{S["model"]} · prompt {S["prompt_version"]}</p>', unsafe_allow_html=True)
