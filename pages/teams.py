import streamlit as st

from dbhelper import DB


db = DB()

TEAM_LOGOS = {
    "Chennai Super Kings": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2b/Chennai_Super_Kings_Logo.svg/500px-Chennai_Super_Kings_Logo.svg.png",
    "Delhi Capitals": "https://upload.wikimedia.org/wikipedia/en/2/2f/Delhi_Capitals.svg",
    "Gujarat Titans": "https://upload.wikimedia.org/wikipedia/en/thumb/0/09/Gujarat_Titans_Logo.svg/500px-Gujarat_Titans_Logo.svg.png",
    "Kolkata Knight Riders": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Kolkata_Knight_Riders_Logo.svg/330px-Kolkata_Knight_Riders_Logo.svg.png",
    "Lucknow Super Giants": "https://shorturl.at/Dbm7j",
    "Mumbai Indians": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Mumbai_Indians_Logo.svg/500px-Mumbai_Indians_Logo.svg.png",
    "Punjab Kings": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Punjab_Kings_Logo.svg/330px-Punjab_Kings_Logo.svg.png",
    "Rajasthan Royals": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Punjab_Kings_Logo.svg/330px-Punjab_Kings_Logo.svg.png",
    "Royal Challengers Bangalore": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Royal_Challengers_Bengaluru_Logo.svg/500px-Royal_Challengers_Bengaluru_Logo.svg.png?_=20250525064902",
    "Sunrisers Hyderabad": "https://upload.wikimedia.org/wikipedia/en/thumb/5/51/Sunrisers_Hyderabad_Logo.svg/500px-Sunrisers_Hyderabad_Logo.svg.png"
}


st.markdown(
    """
<style>
:root {
    --bg-start: #3a3a3a;
    --bg-end: #0f0f0f;
    --card: #171717;
    --card-2: #1f1f1f;
    --ink: #f3f4f6;
    --muted: #c3cad5;
    --brand: #1d4ed8;
    --brand-2: #0ea5a4;
    --line: #2f3a4a;
}
.stApp {
    background:
      radial-gradient(circle at 12% 8%, rgba(29, 78, 216, 0.18) 0%, rgba(29, 78, 216, 0) 35%),
      radial-gradient(circle at 88% 0%, rgba(14, 165, 164, 0.14) 0%, rgba(14, 165, 164, 0) 35%),
      linear-gradient(180deg, var(--bg-start) 0%, var(--bg-end) 72%);
    color: var(--ink);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    border-right: 1px solid #243048;
}
[data-testid="stSidebar"] * {
    color: #e8f1ff !important;
}
.hero {
    background: linear-gradient(120deg, #1d4ed8 0%, #2563eb 45%, #0ea5a4 100%);
    border-radius: 18px;
    color: #f8fbff;
    padding: 1.05rem 1.2rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.35);
}
.hero h1 {
    margin: 0;
    font-size: 1.85rem;
    color: #ffffff;
}
.hero p {
    margin: 0.45rem 0 0;
    color: #e3efff;
}
.section-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 0.9rem 1rem;
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.25);
}
.logo-card {
    background: var(--card-2);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 0.7rem;
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.3);
}
.label {
    color: var(--muted);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.value {
    color: var(--ink);
    font-size: 1.4rem;
    font-weight: 700;
    margin-top: 0.2rem;
}
[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 0.8rem;
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
}
[data-testid="stMetricValue"] {
    color: #f9fafb !important;
}
.season-mini-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 0.55rem 0.7rem;
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.25);
}
.season-mini-label {
    color: var(--muted);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.season-mini-value {
    color: var(--ink);
    font-size: 1.1rem;
    font-weight: 700;
    margin-top: 0.15rem;
}
h1, h2, h3, p, div, span, label {
    color: var(--ink);
}
[data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

teams = sorted(db.fetch_team())
seasons = sorted(db.fetch_Season(), reverse=True)

st.sidebar.title("Team Analytics")
curr_team = st.sidebar.selectbox("Select Team", teams, index=0)
season = st.sidebar.selectbox("Select Season", seasons, index=0)

logo_url = TEAM_LOGOS[curr_team]

st.markdown(
    f"""
<div class="hero">
    <h1>{curr_team}</h1>
    <p>Professional team summary with all-time and season-level performance indicators.</p>
</div>
""",
    unsafe_allow_html=True,
)

header_col, logo_col = st.columns([2.2, 1], gap="large")
with header_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="label">Current Selection</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="value">{curr_team}</div>', unsafe_allow_html=True)
    st.caption(f"Season focus: {season}")
    st.markdown("</div>", unsafe_allow_html=True)

with logo_col:
    st.markdown('<div class="logo-card">', unsafe_allow_html=True)
    st.image(logo_url, use_container_width=True)
    st.caption("Team logo")
    st.markdown("</div>", unsafe_allow_html=True)

all_time_runs = db.fetch_team_run(curr_team)
all_time_matches = db.fetch_total_matches(curr_team)
all_time_wickets = db.fetch_total_wicket(curr_team)

kpi_1, kpi_2, kpi_3 = st.columns(3, gap="medium")
kpi_1.metric("All-Time Runs", f"{all_time_runs:,}")
kpi_2.metric("Total Matches", f"{all_time_matches:,}")
kpi_3.metric("Total Wickets", f"{all_time_wickets:,}")

season_runs = db.fetch_Season_runs(curr_team, season)
season_wickets = db.fetch_season_wickets(curr_team, season)

spacer_left, season_col1, season_col2, spacer_right = st.columns([0.45, 1, 1, 0.45], gap="medium")
with season_col1:
    st.markdown('<div class="season-mini-card">', unsafe_allow_html=True)
    st.markdown('<div class="season-mini-label">Season Runs</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="season-mini-value">{season_runs:,}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with season_col2:
    st.markdown('<div class="season-mini-card">', unsafe_allow_html=True)
    st.markdown('<div class="season-mini-label">Season Wickets</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="season-mini-value">{season_wickets:,}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Quick Insight")
st.write(
    f"In {season}, {curr_team} recorded {season_runs:,} runs and {season_wickets:,} wickets. "
    "Use the sidebar to compare season changes for the same franchise."
)
st.markdown("</div>", unsafe_allow_html=True)
