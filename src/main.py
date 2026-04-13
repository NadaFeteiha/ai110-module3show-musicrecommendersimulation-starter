"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


DIVIDER = "─" * 45

def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "favorite_genre":   "pop",
        "favorite_mood":    "happy",
        "target_energy":    0.8,
        "target_valence":   0.7,
        "target_tempo_bpm": 120.0,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nTop {len(recommendations)} recommendations for a "
          f"{user_prefs['favorite_genre']} / {user_prefs['favorite_mood']} listener:\n")

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(DIVIDER)
        print(f"#{rank}  {song['title']} — {song['artist']}")
        print(f"    Score: {score:.2f}")
        for reason in reasons:
            print(f"    • {reason}")

    print(DIVIDER)


if __name__ == "__main__":
    main()
