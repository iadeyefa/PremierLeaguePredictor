import pandas as pd
import numpy as np

# core of the functionality within this file

# -----------------------------
# 1. Define Teams and Initial Elo Ratings
# -----------------------------
teams = [
    "Arsenal", "Man City", "Man United", "Chelsea", "Liverpool",
    "Tottenham", "Newcastle", "Brighton", "Aston Villa", "Brentford",
    "Fulham", "West Ham", "Crystal Palace", "Wolves", "Bournemouth",
    "Everton", "Leicester", "Nottingham Forest", "Southampton", "Sheffield Utd"
]

# Starting Elo ratings (rough approximation based on last season)
elo = {team: 1500 for team in teams}

# -----------------------------
# 2. Define Remaining Fixtures
# -----------------------------
# For simplicity, simulate a "round-robin" season (every team plays every other once)
fixtures = [(home, away) for i, home in enumerate(teams) for j, away in enumerate(teams) if i != j]

# -----------------------------
# 3. Elo-based Win Probabilities
# -----------------------------
def win_prob(home_elo, away_elo, home_advantage=50):
    """Calculate probability of home win using Elo difference."""
    diff = home_elo + home_advantage - away_elo
    prob_home = 1 / (1 + 10**(-diff/400))
    prob_draw = 0.2  # simple fixed draw probability
    prob_home = prob_home * (1 - prob_draw)
    prob_away = 1 - prob_home - prob_draw
    return prob_home, prob_draw, prob_away

# -----------------------------
# 4. Monte Carlo Simulation
# -----------------------------
simulations = 5000
points_table = {team: [] for team in teams}

for _ in range(simulations):
    points = {team: 0 for team in teams}
    for home, away in fixtures:
        ph, pd, pa = win_prob(elo[home], elo[away])
        outcome = np.random.choice(["H", "D", "A"], p=[ph, pd, pa])
        if outcome == "H":
            points[home] += 3
        elif outcome == "A":
            points[away] += 3
        else:
            points[home] += 1
            points[away] += 1
    for team in teams:
        points_table[team].append(points[team])

# -----------------------------
# 5. Average Points Across Simulations
# -----------------------------
predicted_points = {team: np.mean(points_table[team]) for team in teams}
predicted_table = pd.DataFrame({
    "Team": list(predicted_points.keys()),
    "Predicted Points": list(predicted_points.values())
}).sort_values("Predicted Points", ascending=False).reset_index(drop=True)

print(predicted_table)

# -----------------------------
# 6. Optional: Quick Visualization
# -----------------------------
import matplotlib.pyplot as plt

plt.ion()

plt.figure(figsize=(12,6))
plt.bar(predicted_table["Team"], predicted_table["Predicted Points"], color="skyblue")
plt.xticks(rotation=90)
plt.ylabel("Predicted Points")
plt.title("Predicted Premier League 2025–26 Table (Elo + Monte Carlo)")
plt.show()
