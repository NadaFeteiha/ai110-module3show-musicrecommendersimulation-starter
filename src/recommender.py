from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.5
    target_tempo_bpm: float = 120.0

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Returns a (score, reasons) tuple rating how well a song matches a user profile.

    Returns (score, reasons) where:
      - score  is a float in [0.0, 1.0] — weighted sum of five components
      - reasons is a list of human-readable strings, one per feature

    user_prefs keys: favorite_genre, favorite_mood, target_energy,
                     target_valence, target_tempo_bpm
    song keys:       genre, mood, energy, valence, tempo_bpm
    """
    reasons = []

    # --- genre: binary match, weight 0.35 ---
    if song["genre"] == user_prefs["favorite_genre"]:
        s_genre = 1.0
        reasons.append(f"genre match: {song['genre']} (+{0.35 * s_genre:.2f})")
    else:
        s_genre = 0.0
        reasons.append(
            f"genre mismatch: {song['genre']} vs {user_prefs['favorite_genre']} (+0.00)"
        )

    # --- mood: binary match, weight 0.25 ---
    if song["mood"] == user_prefs["favorite_mood"]:
        s_mood = 1.0
        reasons.append(f"mood match: {song['mood']} (+{0.25 * s_mood:.2f})")
    else:
        s_mood = 0.0
        reasons.append(
            f"mood mismatch: {song['mood']} vs {user_prefs['favorite_mood']} (+0.00)"
        )

    # --- energy: proximity, weight 0.20 ---
    s_energy = 1.0 - abs(song["energy"] - user_prefs["target_energy"]) / 1.0
    reasons.append(
        f"energy proximity: {song['energy']:.2f} vs {user_prefs['target_energy']:.2f}"
        f" (+{0.20 * s_energy:.2f})"
    )

    # --- valence: proximity, weight 0.12 ---
    s_valence = 1.0 - abs(song["valence"] - user_prefs["target_valence"]) / 1.0
    reasons.append(
        f"valence proximity: {song['valence']:.2f} vs {user_prefs['target_valence']:.2f}"
        f" (+{0.12 * s_valence:.2f})"
    )

    # --- tempo: proximity, weight 0.08 ---
    s_tempo = 1.0 - abs(song["tempo_bpm"] - user_prefs["target_tempo_bpm"]) / 120.0
    reasons.append(
        f"tempo proximity: {song['tempo_bpm']:.1f} vs {user_prefs['target_tempo_bpm']:.1f} BPM"
        f" (+{0.08 * s_tempo:.2f})"
    )

    # --- weighted sum ---
    score = (
        0.35 * s_genre +
        0.25 * s_mood  +
        0.20 * s_energy +
        0.12 * s_valence +
        0.08 * s_tempo
    )
    return score, reasons


def _score_song_objects(song: Song, user_profile: UserProfile) -> float:
    """
    Score a Song dataclass against a UserProfile dataclass.
    Used internally by Recommender.recommend() and recommend_songs().
    """
    s_energy  = 1.0 - abs(song.energy    - user_profile.target_energy)    / 1.0
    s_valence = 1.0 - abs(song.valence   - user_profile.target_valence)   / 1.0
    s_tempo   = 1.0 - abs(song.tempo_bpm - user_profile.target_tempo_bpm) / 120.0
    s_genre   = 1.0 if song.genre == user_profile.favorite_genre else 0.0
    s_mood    = 1.0 if song.mood  == user_profile.favorite_mood  else 0.0
    return (
        0.35 * s_genre   +
        0.25 * s_mood    +
        0.20 * s_energy  +
        0.12 * s_valence +
        0.08 * s_tempo
    )


def recommend_songs(
    song_list: List[Song],
    user_profile: UserProfile,
    top_n: int = 5,
) -> List[Tuple[str, float]]:
    """
    Ranking Rule: score every song, sort highest-to-lowest, return the top N.

    Scoring tells you how good each song is in isolation.
    Ranking answers the different question: given ALL scored songs, which N
    should actually surface to the user?  That requires:
      1. A global comparison across all scores (sorting)
      2. A cutoff decision (top_n)
    Neither is possible from a single score_song call.

    Returns a list of (song_title, score) tuples, best match first.
    """
    scored = [(song.title, _score_song_objects(song, user_profile)) for song in song_list]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_n]


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(self.songs, key=lambda s: _score_song_objects(s, user), reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre matches ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood matches ({song.mood})")
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff <= 0.1:
            reasons.append(f"energy is close to your preference ({song.energy:.2f})")
        if not reasons:
            reasons.append("overall profile is similar to your preferences")
        return "Recommended because: " + ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Reads a CSV catalog and returns a list of song dicts with numeric fields cast to float.

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    return []

    Required by src/main.py
    """
    import csv

    float_fields = {"energy", "valence", "tempo_bpm", "danceability", "acousticness"}

    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            songs = []
            for row in reader:
                for field in float_fields:
                    row[field] = float(row[field])
                songs.append(dict(row))
        return songs
    except FileNotFoundError:
        print(f"Error: song catalog not found at '{csv_path}'. Check the file path and try again.")
        return []

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
) -> List[Tuple[Dict, float, List[str]]]:
    """Scores all songs against a user profile and returns the top k matches as (song, score, reasons) tuples."""
    # Score every song in one pass using a list comprehension.
    # score_song returns (score, reasons), so we unpack inline and keep the
    # full song dict alongside them so callers can access any field (title,
    # artist, genre, etc.) without needing a second lookup.
    scored = [
        (song, score, reasons)
        for song in songs
        for score, reasons in (score_song(user_prefs, song),)
    ]

    # sorted() is used here instead of list.sort() for one key reason:
    #
    #   .sort()   mutates the list in-place and returns None.
    #   sorted()  leaves the original list untouched and returns a new list.
    #
    # Because `scored` is a local variable we built just above, mutation would
    # be harmless in this specific case — but sorted() makes the intent clearer:
    # we are *producing* a ranked result, not *reordering* an existing structure.
    # It also keeps the function free of side-effects, which matters if the
    # caller reuses `songs` elsewhere and expects it to stay in its original order.
    return sorted(scored, key=lambda t: t[1], reverse=True)[:k]


# ---------------------------------------------------------------------------
# Sample profiles
# ---------------------------------------------------------------------------

# Mainstream pop listener.
# Well-aligned values: high energy, positive valence, and 120 BPM are all
# typical pop characteristics, so genre/mood matches will dominate and
# numerical features will fine-tune within that group.
#
# Known limitations:
#   - "indie pop" != "pop" (exact string match) costs 0.35 points even for
#     songs that sound identical, e.g. Rooftop Lights scores 0.626 vs 0.978.
#   - likes_acoustic=False is stored but never read by score_song; it has
#     no effect on results until wired into the scoring logic.
PROFILE_MAINSTREAM_POP = UserProfile(
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.8,
    target_valence=0.7,
    target_tempo_bpm=120.0,
    likes_acoustic=False,
)

# Stress-test profile: contradictory preferences.
# favorite_genre="classical" but the numerical targets (energy 0.88,
# tempo 162 BPM) match metal/rock far better than any classical song in
# the catalog (classical songs sit at energy ~0.24, tempo ~70 BPM).
#
# What this reveals:
#   1. Genre scarcity — only 2 classical songs exist, so the 0.35 genre
#      weight fires rarely and the recommender degrades to near-purely
#      numerical scoring for this user.
#   2. Silent preference conflict — metal songs will outscore classical ones
#      on every numerical dimension, so the user will receive metal
#      recommendations despite saying they prefer classical.
#   3. likes_acoustic=True is again silently ignored, which would have been
#      the one feature reliably separating classical from metal.
PROFILE_STRESS_TEST = UserProfile(
    favorite_genre="classical",
    favorite_mood="melancholic",
    target_energy=0.88,
    target_valence=0.15,
    target_tempo_bpm=162.0,
    likes_acoustic=True,
)
