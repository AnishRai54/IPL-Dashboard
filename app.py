import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

from dbhelper import DB

db = DB()

st.set_page_config(page_title="IPL Dashboard", layout="wide")

st.markdown(
    """
<style>
:root {
    --bg: black;
    --bg-2: grey;
    --card: #ffffff;
    --ink: #10233c;
    --muted: #4d607a;
    --brand: #ef6c00;
    --brand-2: #00897b;
    --brand-3: #1565c0;
}
.stApp {
    background:
        radial-gradient(circle at 10% 8%, rgba(0, 137, 123, 0.12) 0%, rgba(0, 137, 123, 0) 36%),
        radial-gradient(circle at 88% 0%, rgba(21, 101, 192, 0.2) 0%, rgba(21, 101, 192, 0) 40%),
        linear-gradient(180deg, var(--bg-2) 0%, var(--bg) 60%);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    border-right: 1px solid #243048;
}
[data-testid="stSidebar"] * {
    color: #e5f0ff !important;
}
.hero {
    background: linear-gradient(130deg, var(--brand-2) 0%, var(--brand-3) 58%, var(--brand) 100%);
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
    color: white;
    margin-bottom: 0.8rem;
    box-shadow: 0 10px 24px rgba(20, 79, 159, 0.2);
}
.hero h1 {
    font-size: 2rem;
    margin: 0;
}
.hero p {
    margin: 0.35rem 0 0 0;
    color: #dbeafe;
}
.chip-row {
    margin-top: 0.65rem;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.chip {
    display: inline-block;
    padding: 0.3rem 0.7rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.18);
    border: 1px solid rgba(255, 255, 255, 0.35);
    color: #f8fbff;
    font-size: 0.82rem;
}
.section-card {
    background: var(--card);
    border: 1px solid #d7e3f0;
    border-radius: 16px;
    padding: 0.9rem 1rem;
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
}
.kpi-card {
    background: var(--card);
    border: 1px solid #d7e3f0;
    border-radius: 14px;
    padding: 0.85rem 0.95rem;
    box-shadow: 0 8px 16px rgba(15, 23, 42, 0.08);
}
.kpi-label {
    font-size: 0.78rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.kpi-value {
    margin-top: 0.3rem;
    font-size: 1.45rem;
    color: var(--ink);
    font-weight: 700;
    line-height: 1.05;
}
.kpi-note {
    margin-top: 0.2rem;
    color: var(--muted);
    font-size: 0.8rem;
}
.img-card {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #d7e3f0;
    box-shadow: 0 12px 24px rgba(15, 23, 42, 0.13);
}
.caption-text {
    color: var(--muted);
    margin-top: 0.25rem;
}
</style>
""",
    unsafe_allow_html=True,
)

st.sidebar.title("IPL Dashboard")
sidebar_logo = "https://www.shutterstock.com/image-photo/semi-top-view-rounded-full-600nw-2594552419.jpg"
st.sidebar.image(sidebar_logo, use_container_width=True)
season = db.fetch_Season()
selected_season = st.sidebar.selectbox("Season", season, index=0)
team = db.fetch_team()
selected_team = st.sidebar.selectbox("Team", team, index=0)
st.sidebar.caption(f"Active season: {selected_season}")
st.sidebar.caption(f"Selected team: {selected_team}")

team_names, trophies = db.fetch_NoOfTrophy()
df = pd.DataFrame({"team": team_names, "no_of_trophy": trophies}).sort_values(
    "no_of_trophy", ascending=False
)
df["rank"] = df["no_of_trophy"].rank(method="dense", ascending=False).astype(int)

total_teams = int(df["team"].nunique())
total_titles = int(df["no_of_trophy"].sum())
top_team = df.iloc[0]
avg_titles = round(float(df["no_of_trophy"].mean()), 2)

st.markdown(
    f"""
<div class="hero">
    <h1>IPL Analytics Dashboard</h1>
    <p>Professional snapshot of championship outcomes, team dominance, and title distribution trends.</p>
    <div class="chip-row">
        <span class="chip">Season Focus: {selected_season}</span>
        <span class="chip">Team Lens: {selected_team}</span>
        <span class="chip">Top Franchise: {top_team["team"]}</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

local_images = sorted(Path("assets").glob("*"))
hero_images = [str(path) for path in local_images if path.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"]][:3]
if not hero_images:
    hero_images = [
  "https://commons.wikimedia.org/wiki/Special:FilePath/Eden%20Gardens%20during%20IPL%20match%2006.jpg",
  "https://commons.wikimedia.org/wiki/Special:FilePath/Wankhede%20stadium.jpg",
  "https://commons.wikimedia.org/wiki/Special:FilePath/IPL%20Match%20--%20Dr.%20D%20Y%20Patil%20Stadium.jpg"
]

img_col1, img_col2, img_col3 = st.columns(3)
for col, image in zip([img_col1, img_col2, img_col3], hero_images):
    with col:
        st.markdown('<div class="img-card">', unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
st.markdown('<p class="caption-text">Add your own images in `assets/` to replace demo visuals automatically.</p>', unsafe_allow_html=True)

kpi_cols = st.columns(4, gap="medium")
kpi_data = [
    ("Total Teams", total_teams, "Franchises in trophy table"),
    ("Total Titles", total_titles, "Finals won across IPL seasons"),
    ("Most Successful", int(top_team["no_of_trophy"]), str(top_team["team"])),
    ("Avg Titles/Team", avg_titles, "Across all listed teams"),
]
for col, (label, value, note) in zip(kpi_cols, kpi_data):
    with col:
        st.markdown(
            f"""
<div class="kpi-card">
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">{value}</div>
    <div class="kpi-note">{note}</div>
</div>
""",
            unsafe_allow_html=True,
        )

overview_col, spotlight_col = st.columns([1.6, 1], gap="large")

with overview_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Executive Overview")
    st.markdown(
        """
This page highlights title-winning patterns from IPL finals and identifies dominant franchises over time.

- Title count benchmarking across teams  
- Fast identification of the top-performing franchise  
- Compact leaderboard for decision-ready insights
"""
    )
    st.markdown("</div>", unsafe_allow_html=True)

with spotlight_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Top 3 Franchises")
    for _, row in df.head(3).iterrows():
        st.markdown(f'- **#{int(row["rank"])} {row["team"]}**: {int(row["no_of_trophy"])} titles')
    st.markdown("</div>", unsafe_allow_html=True)

chart_col, leader_col = st.columns([2, 1], gap="large")

with chart_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    chart_source = df.sort_values("no_of_trophy").copy()
    fig = px.bar(
        chart_source,
        x="no_of_trophy",
        y="team",
        orientation="h",
        color="no_of_trophy",
        color_continuous_scale=[
            [0.0, "#b2ebf2"],
            [0.35, "#26a69a"],
            [0.7, "#1565c0"],
            [1.0, "#ef6c00"],
        ],
        text="no_of_trophy",
        custom_data=["rank"],
    )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_color="rgba(255,255,255,0.9)",
        marker_line_width=1.2,
        hovertemplate="<b>%{y}</b><br>Titles: %{x}<br>Rank: %{customdata[0]}<extra></extra>",
    )
    fig.update_layout(
        title="IPL Titles by Franchise",
        xaxis_title="No. of Titles",
        yaxis_title="Team",
        template="plotly_white",
        showlegend=False,
        coloraxis_showscale=False,
        plot_bgcolor="#f9fcff",
        paper_bgcolor="rgba(0,0,0,0)",
        title_font=dict(size=20, color="#10233c"),
        margin=dict(l=10, r=20, t=62, b=20),
        height=460,
        xaxis=dict(showgrid=True, gridcolor="#d9e6f5", zeroline=False),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with leader_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Leaderboard")
    st.dataframe(
        df[["rank", "team", "no_of_trophy"]].rename(
            columns={"rank": "Rank", "team": "Team", "no_of_trophy": "Titles"}
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.subheader("All IPL Teams")
team_df = pd.DataFrame({"Team": sorted(db.fetch_team())})
st.dataframe(team_df, use_container_width=True, hide_index=True)





