import streamlit as st
from PIL import Image
import random

# Page configuration for mobile-friendly layout
st.set_page_config(
    page_title="Pitch & Putt Scramble Generator",
    page_icon="⛳",
    layout="centered"
)

# Display logo if available
try:
    logo = Image.open("pitch_putt_logo.png")
    st.image(logo, width=200)
except FileNotFoundError:
    st.markdown("### ⛳ Pitch & Putt Scramble Team Generator")

# Sidebar for team size selection
team_size = st.sidebar.selectbox("Select Scramble Format", [2, 3], index=0)

# Handicap options
handicap_options = list(range(0, 26))

# Input player names and handicaps
st.subheader("🏌️ Enter Player Names and Select Handicaps")
num_players = st.number_input("Number of players", min_value=1, max_value=100, step=1)

players = []
for i in range(int(num_players)):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(f"Player {i+1} Name", key=f"name_{i}")
    with col2:
        hcp = st.selectbox(f"HCP", handicap_options, key=f"hcp_{i}")
    if name:
        players.append((name.strip(), float(hcp)))

# Function to generate balanced teams
def generate_balanced_teams(players, team_size):
    random.shuffle(players)
    players_sorted = sorted(players, key=lambda x: -x[1])
    num_teams = len(players) // team_size

    teams = [[] for _ in range(num_teams)]
    team_totals = [0.0] * num_teams

    for player in players_sorted:
        min_index = None
        min_total = float('inf')
        for i in range(num_teams):
            if len(teams[i]) < team_size and team_totals[i] < min_total:
                min_total = team_totals[i]
                min_index = i
        if min_index is not None:
            teams[min_index].append(player)
            team_totals[min_index] += player[1]

    leftover_players = [p for p in players if p not in [player for team in teams for player in team]]
    return teams, leftover_players

# Generate teams on button click
if st.button("Generate Teams"):
    if len(players) < team_size:
        st.error(f"At least {team_size} players are required.")
    else:
        teams, leftovers = generate_balanced_teams(players, team_size)
        st.subheader("📋 Generated Teams")
        for i, team in enumerate(teams, 1):
            team_total = sum(p[1] for p in team)
            team_allowance = team_total / 3
            team_str = ", ".join([f"{p[0]} (HCP {p[1]})" for p in team])
            st.markdown(f"**Team {i}** — Total HCP: {team_total:.1f}, Allowance: **{team_allowance:.2f}**")
            st.markdown(team_str)

        if leftovers:
            st.subheader("⛳ Leftover Players")
            for p in leftovers:
                st.markdown(f"{p[0]} (HCP {p[1]})")




       

