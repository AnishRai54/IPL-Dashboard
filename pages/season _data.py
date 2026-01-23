import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


from dbhelper import DB
db = DB()

season = db.fetch_Season()
year = st.sidebar.selectbox("Season", season)

total_matches = db.fetch_Season_Total_Matches(year)

st.title("Season Summary")
st.metric("Total Matches", total_matches)


st.title("FINAl MATCH")
winner,losser=db.Season_winner_loser(year)

st.markdown(
    f"""<h2 style='text-align:center;'>{winner} vs {losser}</h2>""",
    unsafe_allow_html=True
)



st.markdown(
    f" <h3 style='text-align:center;'> Winner = {winner}</h3>",
    unsafe_allow_html=True
)

st.markdown(
    f" <h3 style='text-align:center;'> Losser = {losser}</h3>",
    unsafe_allow_html=True

)


orange_cap,run,purple_cap,wicket=db.fetch_Cap(year)
st.title(" Cap Detail ")
col1,col2=st.columns(2)



with col1:
    st.markdown(
        f" <h4  style='text-align:center;'> Orange cap --> {orange_cap} |  runs-->{run}",

        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f" <h4  style='text-align:center;'> Purple cap --> {purple_cap}  |  wicket-->{wicket}",

        unsafe_allow_html=True
    )


st.title(" ")

total_six=db.fetch_totalSix(year)
total_wicket=db.total_wickets(year)

col3,col4=st.columns(2)

with col3:
    st.markdown(
        f" <h4  style='text-align:center;'> Total Six --> {total_six} ",

        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f" <h4  style='text-align:center;'> Total Wicket --> {total_wicket} ",

        unsafe_allow_html=True
    )


st.title("Points Table")

point_table=db.fetch_Point_table(year)

st.dataframe(point_table)

table_graph=pd.DataFrame(point_table,columns=['Teams','Points'])

df = table_graph.copy()
df["Points"] = pd.to_numeric(df["Points"])
df = df.sort_values("Points", ascending=True)  # highest will appear on top in horizontal

fig = px.bar(
    df,
    x="Points",
    y="Teams",
    orientation="h",
    color="Points",
    text="Points",
    title="Points Table"
)



st.plotly_chart(fig, use_container_width=True)





