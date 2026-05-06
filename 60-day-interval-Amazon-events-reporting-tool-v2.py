import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Bimonthly Tracker", layout="centered")

st.title("📊 Bimonthly Performance Tracker")
st.markdown("**Past (Feb-Mar) → Present (Apr-May) × 6**")

# ====================== SIDEBAR ======================
st.sidebar.header("Input Values")

past_x = st.sidebar.number_input("Past (Feb-Mar)", 
                                min_value=0.0, value=150.0, step=10.0)

present_y = st.sidebar.number_input("Present (Apr-May)", 
                                   min_value=0.0, value=420.0, step=10.0)

events = st.sidebar.number_input("Events per 2-month interval", 
                                min_value=1, value=12, step=1)

associates = st.sidebar.number_input("Number of Associates", 
                                    min_value=1, value=2, step=1)

# ====================== CALCULATIONS ======================
growth = round((present_y / past_x * 100 - 100), 1) if past_x > 0 else 0.0
annual_projection = present_y * 6
events_per_assoc = round(events / associates, 1) if associates > 0 else 0.0
total_event_associates = events * associates

# ====================== METRICS ======================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Past (Feb-Mar)", f"{past_x:,.0f}")
with col2:
    st.metric("Present (Apr-May)", f"{present_y:,.0f}", 
              delta=f"{growth:+.1f}%")
with col3:
    st.metric("Annual Projection", f"{annual_projection:,.0f}")

st.divider()

# ====================== PERFORMANCE CHART ======================
chart_data = pd.DataFrame({
    "Period": ["Past\n(Feb-Mar)", "Present\n(Apr-May)", "Projected\nFull Year"],
    "Value": [past_x, present_y, annual_projection],
    "Type": ["Historical", "Historical", "Projected"]
})

bar_chart = alt.Chart(chart_data).mark_bar(size=60).encode(
    x=alt.X("Period", sort=None, title=None),
    y=alt.Y("Value", title="Value"),
    color=alt.Color("Type", scale=alt.Scale(domain=["Historical", "Projected"],
                                           range=["#4c78a8", "#f58518"])),
    tooltip=["Period", "Value"]
).properties(
    title="Performance Comparison & Annual Projection",
    height=380
)

st.altair_chart(bar_chart, use_container_width=True)

# ====================== EVENTS & ASSOCIATES ======================
st.subheader("Events × Associates")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Events / 2 months", f"{events:,}")
with c2:
    st.metric("Associates", associates)
with c3:
    st.metric("Events per Associate", f"{events_per_assoc:.1f}")

st.metric("Total (Events × Associates)", f"{total_event_associates:,}")

# Pie Chart
pie_data = pd.DataFrame({
    "Category": ["Events", "Associate Impact"],
    "Value": [events, total_event_associates]
})

pie_chart = alt.Chart(pie_data).mark_arc().encode(
    theta="Value",
    color=alt.Color("Category", scale=alt.Scale(range=["#4c78a8", "#f58518"]))
).properties(
    title="Events vs Associate Contribution",
    height=300
)

st.altair_chart(pie_chart, use_container_width=True)

# ====================== SUMMARY ======================
st.subheader("Summary")
summary = pd.DataFrame({
    "Metric": [
        "Past Period (x)",
        "Present Period (y)",
        "Growth",
        "Annual Projection (y × 6)",
        "Events per Interval",
        "Associates",
        "Events × Associates",
        "Events per Associate"
    ],
    "Value": [
        f"{past_x:,.0f}",
        f"{present_y:,.0f}",
        f"{growth:+.1f}%",
        f"{annual_projection:,.0f}",
        events,
        associates,
        total_event_associates,
        f"{events_per_assoc:.1f}"
    ]
})

st.dataframe(summary, hide_index=True, use_container_width=True)

st.caption("Simplified Bimonthly Tracker • Streamlit 1.39.0 + Python 3.14.4")
