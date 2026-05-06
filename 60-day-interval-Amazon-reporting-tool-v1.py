```python
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Bimonthly Performance Tracker", layout="wide")
st.title("📊 Bimonthly Events & Associates Tracker")
st.markdown("""
**Concept**: Compare Past (Feb-Mar) vs Present (Apr-May) performance.  
Project forward using **×6** (for 6 × 2-month intervals in a year).  
Track **Number of Events × 2 Associates** per interval.
""")

# Sidebar inputs
st.sidebar.header("Input Metrics")

past_x = st.sidebar.number_input("Past Period (Feb-Mar) Value (x)", 
                                min_value=0.0, value=150.0, step=1.0,
                                help="e.g., events, revenue, tasks completed in Feb-Mar")

present_y = st.sidebar.number_input("Present Period (Apr-May) Value (y)", 
                                   min_value=0.0, value=420.0, step=1.0,
                                   help="Current performance in Apr-May")

num_events = st.sidebar.number_input("Number of Events (per 2-month interval)", 
                                    min_value=0, value=12, step=1)

num_associates = st.sidebar.number_input("Number of Associates", 
                                        min_value=1, value=2, step=1)

# Calculations
growth_ratio = present_y / past_x if past_x > 0 else 0
annual_projection = present_y * 6
events_per_associate = num_events / num_associates if num_associates > 0 else 0
total_associate_events = num_events * num_associates  # as per "number of events x 2 associates"

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Past (Feb-Mar)", f"{past_x:,.1f}", delta=None)
with col2:
    st.metric("Present (Apr-May)", f"{present_y:,.1f}", 
              delta=f"{growth_ratio:.1%}" if past_x > 0 else None)
with col3:
    st.metric("Annual Projection (y × 6)", f"{annual_projection:,.1f}")
with col4:
    st.metric("Events per Associate", f"{events_per_associate:.1f}")

st.divider()

# Dataframe for visualization
periods = ["Past (Feb-Mar)", "Present (Apr-May)", "Projected Next", "Projected Full Year"]
values = [past_x, present_y, present_y, annual_projection]

df = pd.DataFrame({
    "Period": periods,
    "Value": values,
    "Type": ["Historical", "Historical", "Projected", "Projected"]
})

# Charts
tab1, tab2, tab3 = st.tabs(["📈 Performance Trend", "👥 Events & Associates", "📋 Raw Data"])

with tab1:
    fig = px.bar(df, x="Period", y="Value", color="Type", 
                 title="Performance Comparison & Annual Projection",
                 color_discrete_map={"Historical": "#1f77b4", "Projected": "#ff7f0e"},
                 text="Value")
    fig.update_traces(texttemplate='%{text:,.1f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Events × Associates Analysis")
    
    assoc_col1, assoc_col2 = st.columns(2)
    with assoc_col1:
        st.metric("Events per 2-month interval", num_events)
        st.metric("Total Associate-Event Product", total_associate_events)
    with assoc_col2:
        st.metric("Associates", num_associates)
        st.metric("Events per Associate", f"{events_per_associate:.2f}")
    
    # Simple pie for breakdown
    pie_data = pd.DataFrame({
        "Category": ["Events", "Associates Contribution"],
        "Value": [num_events, total_associate_events]
    })
    fig2 = px.pie(pie_data, names="Category", values="Value", 
                  title="Events vs Associate-Event Impact")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("All Calculations")
    calc_df = pd.DataFrame({
        "Metric": [
            "Past Value (x)", 
            "Present Value (y)", 
            "Growth Ratio", 
            "Annual Projection (y × 6)",
            "Events per Interval",
            "Associates",
            "Events × Associates",
            "Events per Associate"
        ],
        "Value": [
            f"{past_x:,.1f}",
            f"{present_y:,.1f}",
            f"{growth_ratio:.1%}",
            f"{annual_projection:,.1f}",
            num_events,
            num_associates,
            total_associate_events,
            f"{events_per_associate:.2f}"
        ]
    })
    st.table(calc_df)

st.caption("Built as a quick Streamlit prototype for your bimonthly tracking concept. "
           "Copy-paste this code into a `app.py` file and run with `streamlit run app.py`.")
