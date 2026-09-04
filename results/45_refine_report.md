# 45 refine (labels regressed on official-mix weights; vox in logit; ⊥ male)

validity {"wer_max": "baseline", "phrases": ["sweep", "final"], "margins": {"loudness_db": 3.0, "f0_ratio": 0.15, "voiced_abs": 0.05, "dur_ratio": 0.15, "pq_abs": 1.0}, "note": "all thresholds = officials' range (sweep/calib.json) widened by these margins; pq >= officials' min - pq_abs (sensor PQ, sweep phrase)"}

## iter 4: 60 valid / 71 tries in 110s, dataset 500

| label | R² | n | Δ per unit | range | usable | moved (1-cos) |
|---|---|---|---|---|---|---|
| male | 0.258 | 500 | 0.199 | [0.0, 1.0] |  | 0.0005 |
| age | 0.481 | 500 | 4.439 | [17.0, 57.0] | yes | 0.0002 |
| f0 | 0.299 | 500 | 6.319 | [76.9, 231.3] |  | 0.0078 |
| arousal | 0.495 | 500 | 0.063 | [0.19, 0.7] | yes | 0.0007 |
| valence | 0.313 | 500 | 0.019 | [0.35, 0.61] |  | 0.0005 |
| PQ | 0.359 | 500 | 0.124 | [6.7, 8.11] |  | 0.0005 |
| deep | 0.708 | 266 | 3.151 | [-4.6, 4.6] | yes | 0.0036 |
| silky | 0.598 | 266 | 1.939 | [-4.6, 4.6] | yes | 0.0214 |
| singsong | 0.518 | 266 | 3.348 | [-4.6, 4.6] | yes | 0.0098 |
| shrill | 0.47 | 266 | 2.729 | [-4.6, 4.6] | yes | 0.0027 |
| flowing | 0.413 | 266 | 2.428 | [-4.6, 4.6] | yes | 0.0054 |
| loud | 0.361 | 266 | 1.267 | [-4.6, 4.6] |  | 0.0039 |

## iter 5: 60 valid / 63 tries in 99s, dataset 560

| label | R² | n | Δ per unit | range | usable | moved (1-cos) |
|---|---|---|---|---|---|---|
| male | 0.253 | 560 | 0.204 | [0.0, 1.0] |  | 0.0005 |
| age | 0.479 | 560 | 4.656 | [17.0, 57.0] | yes | 0.0006 |
| f0 | 0.293 | 560 | 6.633 | [76.9, 231.3] |  | 0.0007 |
| arousal | 0.504 | 560 | 0.066 | [0.19, 0.7] | yes | 0.0007 |
| valence | 0.321 | 560 | 0.021 | [0.35, 0.61] |  | 0.0029 |
| PQ | 0.351 | 560 | 0.124 | [6.7, 8.11] |  | 0.0009 |
| deep | 0.703 | 326 | 2.989 | [-4.6, 4.6] | yes | 0.0031 |
| silky | 0.594 | 326 | 1.876 | [-4.6, 4.6] | yes | 0.02 |
| singsong | 0.499 | 326 | 3.211 | [-4.6, 4.6] | yes | 0.0037 |
| shrill | 0.479 | 326 | 2.641 | [-4.6, 4.6] | yes | 0.0068 |
| flowing | 0.39 | 326 | 2.166 | [-4.6, 4.6] |  | 0.003 |
| loud | 0.376 | 326 | 1.318 | [-4.6, 4.6] |  | 0.013 |
