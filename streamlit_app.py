import streamlit as st
import random

st.title("Balanced Scramble Team Generator")

team_size = st.sidebar.selectbox("Select Scramble Format", [2, 3])

st.subheader("Enter Player Names and Handicaps")
player_data = st.text_area("Format: Name, Handicap (one per line)", height=200)

players = []
if player_data:
    for line in player_data.strip().split("\n"):
        if "," in line:
            name, hcp = line.split(",", 1)
            try:
                players.append((name.strip(), float(hcp.strip())))
            except ValueError:
                st.warning(f"Invalid handicap for player: {line}")

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

    # Handle leftover players
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
            st.write(f"**Team {i} (Total HCP: {team_total}):** {team_str}")

       

