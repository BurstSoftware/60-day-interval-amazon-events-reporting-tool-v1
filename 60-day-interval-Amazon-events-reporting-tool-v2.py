import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="HR Corrective Actions Tracker", layout="centered")

st.title("📊 HR Corrective Actions Tracker")
st.markdown("**60-Day Interval Summary • 7 Management Personnel**")

# ====================== INPUTS ======================
st.sidebar.header("Adjust Values")

managers = st.sidebar.number_input("Management Personnel", 
                                  min_value=1, value=7, step=1)

events_per_interval = st.sidebar.number_input("Events per 60-day interval", 
                                             min_value=1, value=30, step=1)

past_events = st.sidebar.number_input("Past 60-day Events (Optional)", 
                                     min_value=0, value=22, step=1)

# ====================== CALCULATIONS ======================
events_per_manager = round(events_per_interval / managers, 1) if managers > 0 else 0
annual_projection = events_per_interval * 6
total_manager_events = events_per_interval * managers

growth = round((events_per_interval / past_events * 100 - 100), 1) if past_events > 0 else 0

# ====================== SUMMARY METRICS ======================
st.subheader("60-Day Interval Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Management Personnel", managers)
with col2:
    st.metric("Events per 60 Days", f"{events_per_interval:,}")
with col3:
    st.metric("Events per Manager", f"{events_per_manager:.1f}")
with col4:
    st.metric("Annual Projection", f"{annual_projection:,}")

st.divider()

# Growth metric (if past data provided)
if past_events > 0:
    st.metric("Change from Past Interval", f"{events_per_interval:,}", 
              delta=f"{growth:+.1f}%")

# ====================== CHARTS ======================
# Bar Chart - Projection
chart_data = pd.DataFrame({
    "Period": ["Past 60d", "Current 60d", "Annual (6×)"],
    "Events": [past_events, events_per_interval, annual_projection],
    "Type": ["Historical", "Current", "Projected"]
})

bar_chart = alt.Chart(chart_data).mark_bar(size=50).encode(
    x=alt.X("Period", sort=None, title=None),
    y=alt.Y("Events", title="Number of Events"),
    color=alt.Color("Type", scale=alt.Scale(domain=["Historical", "Current", "Projected"],
                                           range=["#4c78a8", "#2ca02c", "#ff7f0e"])),
    tooltip=["Period", "Events"]
).properties(
    title="HR Corrective Events — 60-Day vs Annual Projection",
    height=380
)

st.altair_chart(bar_chart, use_container_width=True)

# ====================== MANAGER IMPACT ======================
st.subheader("Manager Impact on HR Workload")

impact_data = pd.DataFrame({
    "Category": ["Events per Interval", "Total Manager-Events"],
    "Value": [events_per_interval, total_manager_events]
})

pie_chart = alt.Chart(impact_data).mark_arc().encode(
    theta="Value",
    color=alt.Color("Category", scale=alt.Scale(range=["#1f77b4", "#ff9896"]))
).properties(
    title="Events Created by 7 Managers",
    height=320
)

st.altair_chart(pie_chart, use_container_width=True)

# ====================== FINAL SUMMARY TABLE ======================
st.subheader("Full Summary")
summary = pd.DataFrame({
    "Metric": [
        "Management Personnel",
        "Events per 60-Day Interval",
        "Events per Manager",
        "Past 60-Day Events",
        "Growth from Past",
        "Annual Projection (6 intervals)",
        "Total Manager-Events Impact"
    ],
    "Value": [
        managers,
        events_per_interval,
        f"{events_per_manager:.1f}",
        past_events,
        f"{growth:+.1f}%" if past_events > 0 else "—",
        annual_projection,
        total_manager_events
    ]
})

st.dataframe(summary, hide_index=True, use_container_width=True)

st.caption("HR Corrective Actions Tracker • Every 60 days • Python 3.14.4 Ready")
