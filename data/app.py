import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IPL Analytics Dashboard", layout="wide")

st.title("🏏 IPL Advanced Analytics Dashboard")
st.caption("Built by Pranav Iyer | Python • Power BI • Streamlit")

batters = pd.read_csv("data/final_batter_analysis.csv")
bowlers = pd.read_csv("data/bowling_analysis.csv")
venue_scores = pd.read_csv("data/venue_average_scores.csv")
venue_chasing = pd.read_csv("data/venue_chasing_analysis.csv")
strategy = pd.read_csv("data/match_strategy_analysis.csv")
phase = pd.read_csv("data/phase_analysis.csv")

st.sidebar.header("Filters")

teams = sorted(phase["batting_team"].unique())
selected_team = st.sidebar.selectbox("Select Team", ["All"] + teams)

venues = sorted(venue_scores["venue"].unique())
selected_venue = st.sidebar.selectbox("Select Venue", ["All"] + venues)

phase_view = phase if selected_team == "All" else phase[phase["batting_team"] == selected_team]

venue_scores_view = (
    venue_scores if selected_venue == "All"
    else venue_scores[venue_scores["venue"] == selected_venue]
)

venue_chasing_view = (
    venue_chasing if selected_venue == "All"
    else venue_chasing[venue_chasing["venue"] == selected_venue]
)

col1, col2, col3 = st.columns(3)
col1.metric("Total Batters", len(batters))
col2.metric("Total Bowlers", len(bowlers))
col3.metric("Teams Analyzed", phase["batting_team"].nunique())

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Batting",
    "Bowling",
    "Venue Intelligence"
])

with tab1:
    st.subheader("Winning Strategy Distribution")

    fig_strategy = px.pie(
        strategy,
        names="Strategy",
        values="Win Percentage",
        hole=0.45,
        title="Chasing vs Batting First"
    )
    st.plotly_chart(fig_strategy, use_container_width=True)

    st.subheader("Team-wise Phase Analysis")

    fig_phase = px.bar(
        phase_view,
        x="batting_team",
        y=["avg_powerplay_runs", "avg_middle_runs", "avg_death_runs"],
        title="Powerplay vs Middle Overs vs Death Overs",
        barmode="stack"
    )
    st.plotly_chart(fig_phase, use_container_width=True)

with tab2:
    st.subheader("Top Run Scorers")

    fig_runs = px.bar(
        batters.sort_values("runs_of_bat", ascending=False).head(10),
        x="runs_of_bat",
        y="striker",
        orientation="h",
        title="Top 10 Run Scorers"
    )
    fig_runs.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_runs, use_container_width=True)

    st.subheader("Most Explosive Batters")

    explosive_batters = batters[batters["balls_faced"] >= 30]

    fig_sr = px.bar(
        explosive_batters.sort_values("strike_rate", ascending=False).head(10),
        x="strike_rate",
        y="striker",
        orientation="h",
        title="Top Strike Rate Batters"
    )
    fig_sr.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_sr, use_container_width=True)

    st.subheader("Batter Performance Distribution")

    fig_scatter = px.scatter(
        explosive_batters,
        x="strike_rate",
        y="runs_of_bat",
        hover_name="striker",
        size="runs_of_bat",
        title="Strike Rate vs Runs"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.subheader("Top Wicket Takers")

    fig_wickets = px.bar(
        bowlers.sort_values("wickets", ascending=False).head(10),
        x="wickets",
        y="bowler",
        orientation="h",
        title="Top 10 Wicket Takers"
    )
    fig_wickets.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_wickets, use_container_width=True)

    st.subheader("Most Economical Bowlers")

    fig_economy = px.bar(
        bowlers.sort_values("economy_rate", ascending=True).head(10),
        x="economy_rate",
        y="bowler",
        orientation="h",
        title="Best Economy Rate Bowlers"
    )
    fig_economy.update_layout(yaxis={"categoryorder": "total descending"})
    st.plotly_chart(fig_economy, use_container_width=True)

with tab4:
    st.subheader("Venue Intelligence")

    col4, col5 = st.columns(2)

    fig_venue_runs = px.bar(
        venue_scores_view.sort_values("avg_runs", ascending=False),
        x="venue",
        y="avg_runs",
        title="Highest Scoring Venues"
    )
    col4.plotly_chart(fig_venue_runs, use_container_width=True)

    fig_chasing = px.bar(
        venue_chasing_view.sort_values("chasing_win_percentage", ascending=False),
        x="venue",
        y="chasing_win_percentage",
        title="Best Chasing Venues"
    )
    col5.plotly_chart(fig_chasing, use_container_width=True)