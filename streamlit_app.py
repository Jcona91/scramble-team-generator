import streamlit as st
import random

st.title("Balanced Scramble Team Generator")

team_size = st.sidebar.selectbox("Select Scramble Format", [2, 3])

# Handicap options
handicap_options = list(range(0, 26))

# Input player names
st.subheader("Enter Player Names")
num_players = st.number_input("How many players?", min_value=1, max_value=100, step=1)

players = []
for i in range(int(num_players)):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(f"Player {i+1} Name", key=f"name_{i}")
    with col2:
        hcp = st.selectbox(f"HCP", handicap_options, key=f"hcp_{i}")
    if name:
        players.append((name.strip(), float(hcp)))

def generate_balanced_teams(players, team_size):
    random.shuffle(players)
    players_sorted = sorted(players, key=lambda x: -x[1])
    num_teams = len(players) // team_size

    teams = [[] for _ in range(num_teams)]
    team_totals = [0] * num_teams

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

if st.button("Generate Teams"):
    if len(players) < team_size:
        st.error(f"At least {team_size} players are required.")
    else:
        teams, leftovers = generate_balanced_teams(players, team_size)
        st.subheader("Generated Teams")
        for i, team in enumerate(teams, 1):
            team_str = ", ".join([f"{p[0]} (HCP {p[1]})" for p in team])
            team_total = sum(p[1] for p in team)
            team_allowance = round(team_total / 3, 1)
            st.write(f"**Team {i}** — Total HCP: {team_total}, Allowance: **{team_allowance}**")
            st.write(team_str)

        if leftovers:
            st.subheader("Leftover Players")
            for p in leftovers:
                st.write(f"{p[0]} (HCP {p[1]})")


       

