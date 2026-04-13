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

    # Profile 1: High-Energy Pop Fan
    pop_fan = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "target_valence": 0.85,
        "target_tempo_bpm": 128.0
    }

    # Profile 2: Chill Lofi Listener
    lofi_listener = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.25,
        "target_valence": 0.4,
        "target_tempo_bpm": 75.0
    }

    # Profile 3: Deep Intense Rock Fan
    rock_fan = {
        "favorite_genre": "metal",
        "favorite_mood": "aggressive",
        "target_energy": 0.95,
        "target_valence": 0.2,
        "target_tempo_bpm": 160.0
    }

    for profile in [user_prefs, pop_fan, lofi_listener, rock_fan]:
        recommendations = recommend_songs(profile, songs, k=5)

        print(f"\nTop {len(recommendations)} recommendations for a "
              f"{profile['favorite_genre']} / {profile['favorite_mood']} listener:\n")

        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            print(DIVIDER)
            print(f"#{rank}  {song['title']} — {song['artist']}")
            print(f"    Score: {score:.2f}")
            for reason in reasons:
                print(f"    • {reason}")

        print(DIVIDER)


if __name__ == "__main__":
    main()
