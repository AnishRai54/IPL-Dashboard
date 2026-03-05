import pandas as pd
import plotly.express as px
import streamlit as st

from dbhelper import DB

db = DB()

st.markdown(
    """
<style>
:root {
    --bg: black;
    --bg-2: grey;
    --card: #ffffff;
    --ink: #10233c;
    --muted: #53647d;
    --accent: #fa6a21;
    --accent-2: #0b7f7a;
    --border: #d7e3f0;
}
.stApp {
    background:
        radial-gradient(circle at 8% 10%, rgba(126, 87, 194, 0.22) 0%, rgba(126, 87, 194, 0) 38%),
        radial-gradient(circle at 88% 0%, rgba(94, 53, 177, 0.2) 0%, rgba(94, 53, 177, 0) 42%),
        linear-gradient(180deg, var(--bg-2) 0%, var(--bg) 55%);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    border-right: 1px solid #243048;
}
[data-testid="stSidebar"] * {
    color: #e5f0ff !important;
}
.hero-season {
    background: linear-gradient(135deg, #133b7f 0%, #0b7f7a 100%);
    border-radius: 18px;
    padding: 1.1rem 1.3rem;
    margin: 0 0 0.9rem 0;
    color: #eef7ff;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.18);
}
.hero-season h1 {
    margin: 0;
    font-size: 1.9rem;
    color: #ffffff;
}
.hero-season p {
    margin: 0.35rem 0 0 0;
    color: #dbeafe;
}
.section-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 0.9rem 1rem;
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.07);
}
.kv {
    color: yellow ;
    font-size: 1.02rem;
    font-weight: 600;
    margin: 0.2rem 0;
}
.kv span {
    color: var(--muted);
    font-weight: 500;
}
</style>
""",
    unsafe_allow_html=True,
)

season = db.fetch_Season()
year = st.sidebar.selectbox("Season", season)
st.sidebar.caption(f"Active season: {year}")

total_matches = db.fetch_Season_Total_Matches(year)
winner, loser = db.Season_winner_loser(year)
orange_cap, runs, purple_cap, wickets = db.fetch_Cap(year)
total_six = db.fetch_totalSix(year)
total_wicket = db.total_wickets(year)

st.markdown(
    f"""
<div class="hero-season">
    <h1>Season {year} Summary</h1>
    <p>Final outcome, top performers, and team points snapshot.</p>
</div>
""",
    unsafe_allow_html=True,
)

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Matches", int(total_matches))
with m2:
    st.metric("Champion", winner)
with m3:
    st.metric("Runner-up", loser)

left, right = st.columns(2, gap="large")
with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Final Match")
    st.markdown(f'<p class="kv">{winner} <span>vs</span> {loser}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="kv"><span>Winner:</span> {winner}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="kv"><span>Runner-up:</span> {loser}</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Award Winners")
    st.markdown(
        f'<p class="kv"><span>Orange Cap:</span> {orange_cap} ({int(runs)} runs)</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p class="kv"><span>Purple Cap:</span> {purple_cap} ({int(wickets)} wickets)</p>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

s1, s2 = st.columns(2)
with s1:
    st.metric("Total Sixes", int(total_six))
with s2:
    st.metric("Total Wickets", int(total_wicket))

st.subheader("Points Table")
point_table = db.fetch_Point_table(year)
table_df = pd.DataFrame(point_table, columns=["Team", "Points"])
table_df["Points"] = pd.to_numeric(table_df["Points"])
table_df = table_df.sort_values("Points", ascending=False).reset_index(drop=True)

styled_df = table_df.copy()
styled_df.index = styled_df.index + 1
styled_df.index.name = "Rank"
st.dataframe(styled_df, use_container_width=True)

chart_df = table_df.sort_values("Points", ascending=True)
fig = px.bar(
    chart_df,
    x="Points",
    y="Team",
    orientation="h",
    color="Points",
    text="Points",
    color_continuous_scale="Tealgrn",
    title=f"Season {year} Points Distribution",
)
fig.update_traces(textposition="outside", cliponaxis=False)
fig.update_layout(
    template="plotly_white",
    showlegend=False,
    coloraxis_showscale=False,
    xaxis_title="Points",
    yaxis_title="Team",
    margin=dict(l=20, r=20, t=60, b=20),
)

st.plotly_chart(fig, use_container_width=True)









