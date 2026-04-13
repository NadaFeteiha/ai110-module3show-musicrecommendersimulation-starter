# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name
**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder is a small classroom project I built to better understand how music
recommendation systems work. It is not meant to be a real product. There are no
real users, no listening history, and no streaming platform behind it. The goal
was to simulate the basic idea of a recommender and see how simple rules can turn
song data into ranked suggestions.

This model works best as a learning tool. It assumes the user can describe their
preferences clearly, like favorite genre, mood, target energy, and tempo. That is
not very realistic for most people, but it made the system easier to test and
helped me see exactly how each feature affected the final recommendation.

---

## 3. How the Model Works

Each song gets a score between 0 and 1. That score comes from five main features:
genre, mood, energy, valence, and tempo.

Genre has the biggest weight at 35%. If the song's genre matches the user's
favorite genre exactly, it gets full credit. Mood works in a similar way and is
worth 25%. These two are strict matches, so if the labels are different, the song
does not get any points for that part.

Energy, valence, and tempo are handled differently. Instead of exact matching, the
system checks how close the song is to the user's target values. Songs that are
closer get a higher score, and songs that are farther away get a lower score.

After every song is scored, the recommender sorts them from highest to lowest and
returns the top results. One part I added to the starter code was a "reasons" list
so the output is easier to understand. That way I could see not just which songs
ranked highest, but also why they ranked that way.

---

## 4. Data

The dataset has 18 songs across 15 genres. I started with the original songs in
`songs.csv` and added more tracks to make the catalog feel a little more varied.
I included genres like jazz, metal, reggae, classical, and r&b so the system was
not focused only on pop-style music.

Each song includes a title, artist, genre, mood, energy, valence, tempo, 
danceability, and acousticness. Even though danceability and acousticness are
stored, I did not use them in the final scoring formula.

One big weakness of the dataset is that it is still very small. Even though there
are 15 genres, most of them only appear once. That means the system cannot really
compare songs fairly for users with niche tastes. The catalog is also limited in
language, style, and time period, so it does not represent music very broadly.

---

## 5. Strengths

One strength of the system is that it is easy to understand. The scoring is simple,
and the reasons list makes the recommendations more transparent. When I tested the
system, I could usually tell why a song ranked high or low just by reading the
feature breakdown.

It also works reasonably well when the user's favorite genre has more than one song
in the catalog. In those cases, the model can make more meaningful comparisons
instead of just choosing the only available match.

Another strength is that the numerical scoring for energy, valence, and tempo
mostly behaves the way I expected. Songs closer to the user's target values tend
to rank higher, which made the output feel logical in many test cases.

---

## 6. Limitations and Bias

**Features it does not consider**

The system does not consider artist, release year, lyrics, language, or listening
history. It also stores `likes_acoustic` in the user profile but does not actually
use it in scoring, so that preference currently has no effect. Another issue is
that there is no diversity rule, which means the recommender can return several
very similar songs in a row.

**Genres or moods that are underrepresented**

Most genres in the dataset only appear once, so users with less common preferences
do not get the same quality of recommendations. For example, a lofi listener has
multiple possible matches, but a metal listener may only have one. The same issue
shows up with moods, since some mood labels are very rare.

**Cases where the system overfits to one preference**

In testing, the model often over-relied on genre and mood. If a song matched both,
it could jump far ahead of the others even if the numerical features were only an
average fit. This made the system feel more like a strict filter than a balanced
recommender.

**Ways the scoring might unintentionally favor some users**

Users whose favorite genres appear more often in the catalog are likely to get
better recommendations than users with niche genres. The dataset also leans a bit
toward higher-energy songs, so those users may be helped more often than low-energy
listeners. In addition, the tempo formula can go below zero for extreme cases,
which can unfairly lower a song's total score.

---

## 7. Evaluation

I tested the recommender with several different user profiles, including pop,
lofi, metal, and ambient listeners. I also tried some edge cases on purpose, like
contradictory preferences, missing genres, and extreme tempo targets, to see where
the model would struggle.

The biggest pattern I noticed was that genre and mood had a very strong effect on
the rankings. For example, "Sunrise City" kept ranking first for the pop/happy
profile mainly because it matched both labels exactly. When I changed the weights,
the rankings changed a lot, which showed me that the system is very sensitive to
small design decisions.

One example that stood out was "Rooftop Lights." It seems like a good fit for a
pop/happy listener, but because its genre is labeled `"indie pop"` instead of
`"pop"`, it loses a large part of its score. That result helped me see how rigid
exact string matching can be and why human judgment still matters when evaluating
recommendations.

---

## 8. Future Work

If I kept working on this project, the first thing I would improve is the dataset.
The current catalog is too small to support fair or realistic recommendations, so
I would want a much larger and more balanced set of songs.

I would also replace exact genre and mood matching with something softer, so
similar labels like `"indie pop"` and `"pop"` are not treated as completely
different. That would make the system feel more realistic and less rigid.

Another improvement would be adding diversity to the recommendations. Right now,
the top results can all come from the same genre if they score well. In the future,
I would also like to explore using real feedback, such as skips or replays, so the
system could learn from behavior instead of only depending on manually entered
preferences.

---

## 9. Personal Reflection

This project made recommendation systems feel much more understandable to me. Before
building this, I mostly thought of recommenders as smart tools that somehow know
what people want. After building my own version, I realized they depend a lot on
human choices like which features to include, how to weight them, and how the data
is labeled.

The part that surprised me most was how much a small label difference could affect
the result. In my model, `"indie pop"` and `"pop"` are treated as fully different,
even if they sound very close to a real listener. That showed me that the quality
of the data can matter just as much as the algorithm itself.

Overall, this project helped me see that recommendation systems are not magic. At
their core, they are still based on rules, tradeoffs, and imperfect data. That
made me think more critically about the playlists and recommendations I use in real
apps, and it also helped me appreciate how much design and human judgment goes into
making those systems work well.
