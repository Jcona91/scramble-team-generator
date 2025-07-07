import streamlit as st

st.set_page_config(page_title="Scramble Team Generator", layout="centered")

st.markdown("<h1 style='text-align: center;'>🏌️ Scramble Team Generator</h1>", unsafe_allow_html=True)

team_size = st.selectbox("Select Scramble Format", [2, 3], index=0)

st.markdown("### Enter Player Names and Handicaps")
st.markdown("Use the format: `Name, Handicap` (one per line)")

player_input = st.text_area("Player List", height=200, placeholder="e.g.
Alice, 5
Bob, 12
Charlie, 20")

players = []
if player_input:
    for line in player_input.strip().split("\n"):
        if "," in line:
            name, hcp = line.split(",", 1)
            try:
                players.append((name.strip(), float(hcp.strip())))
            except ValueError:
                st.warning(f"Invalid handicap for player: {line}")

def generate_balanced_teams(players, team_size):
    players_sorted = sorted(players, key=lambda x: -x[1])
    num_teams = len(players) // team_size
    if num_teams == 0:
        return []

    teams = [[] for _ in range(num_teams)]
    team_totals = [0] * num_teams
