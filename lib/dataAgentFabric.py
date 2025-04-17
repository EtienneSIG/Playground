import os
import json
import re
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import InteractiveBrowserCredential
from azure.ai.projects.models import MessageRole

# Load environment variables
# load_dotenv()

# AIPROJECT_CONNECTION_STRING = os.getenv("AIPROJECT_CONNECTION_STRING")
# AGENT_ID = os.getenv("AGENT_ID")

# --- Chargement des paramètres depuis config.json ---
with open("lib/config.json") as config_file:
    config_details = json.load(config_file)

AIPROJECT_CONNECTION_STRING = config_details['AIPROJECT_CONNECTION_STRING']
AGENT_ID = config_details['AGENT_ID']

# Chart rendering function
def render_chart(chart_data):
    chart_type = chart_data.get("type", "line")
    fig = go.Figure()

    if chart_type == "bar":
        fig.add_trace(go.Bar(x=chart_data["x"], y=chart_data["y"]))
    elif chart_type == "pie":
        fig = go.Figure(go.Pie(labels=chart_data["x"], values=chart_data["y"]))
    else:  # default to line chart
        fig.add_trace(go.Scatter(x=chart_data["x"], y=chart_data["y"], mode='lines+markers'))

    fig.update_layout(
        title=chart_data.get("title", "Chart"),
        xaxis_title=chart_data.get("xlabel", "X"),
        yaxis_title=chart_data.get("ylabel", "Y")
    )
    st.plotly_chart(fig, use_container_width=True)

# Chat history display
for entry in st.session_state.chat_history:
    if entry["role"] == "user":
        st.markdown(f"**😏:** {entry['content']}")
    else:
        st.markdown(f"**🤖:** {entry['content']}")
        if entry.get("chart_data"):
            render_chart(entry["chart_data"])

