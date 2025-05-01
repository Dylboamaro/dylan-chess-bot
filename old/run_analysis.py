from engine.analyzer import load_games_from_folder
from old.analyze_quality import analyze_games

# Load and reverse for most recent games first
games = load_games_from_folder("data/raw")
games = list(reversed(games))  # prioritize recent games

# Run phase-aware analysis
results = analyze_games(games, max_games=200)  # adjust as needed

# Output results by phase
for phase in ["opening", "middlegame", "endgame"]:
    phase_data = results[phase]
    print(f"\n--- {phase.title()} Phase ---")
    for category in ["best", "inaccuracy", "mistake", "blunder"]:
        count = phase_data[category]
        total = phase_data["total"]
        pct = (count / total * 100) if total > 0 else 0
        print(f"{category.title():<12}: {count} ({pct:.1f}%)")
