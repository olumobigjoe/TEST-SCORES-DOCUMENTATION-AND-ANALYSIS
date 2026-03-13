# 📡 Continous Assessment System & Performance Analysis

A fully featured browser-based test platform built with **Python + Streamlit** for the course *GLT 302 — General Instrumentation*, complete with a comprehensive data analysis of combined test results from two student batches.

---

## Table of Contents

- [System Overview](#system-overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [Adding Questions](#adding-questions)
- [Deployment](#deployment)
- [Reset Attempts](#reset-attempts)
- [Test Performance Analysis](#test-performance-analysis)
  - [Dataset](#dataset)
  - [Overall Results](#overall-results)
  - [Batch Comparison](#batch-comparison)
  - [Score Distribution](#score-distribution)
  - [Grade Bands](#grade-bands)
  - [Submission Timeline](#submission-timeline)
  - [Top Performers](#top-performers)
  - [Flags & Data Quality](#flags--data-quality)
  - [Key Findings](#key-findings)
  - [Recommendations](#recommendations)
- [Tech Stack](#tech-stack)
- [License](#license)

---

## System Overview

The GLT 302 Test System is a single-file Streamlit application that:
- Authenticates students by full name
- Serves 30 randomly selected and shuffled questions from a bank of 39
- Enforces a 10-minute countdown with auto-submission
- Blocks repeat attempts using device fingerprinting
- Saves every result to a CSV file for post-test analysis

---

## Features

| Feature | Details |
|---|---|
| 🔐 Name-based login | Students enter their full name to begin |
| 🎲 Randomised questions | 30 drawn randomly from a bank of 39; option order shuffled per session |
| ⏱️ 10-minute countdown | Auto-submits when time runs out |
| ✅ Instant feedback | "Correct" or "Wrong" shown after each answer — correct answer not revealed |
| 🛡️ Anti-cheat | One attempt per device — enforced via device fingerprinting |
| 📊 Live score board | Visible on the login page; updates in real time as results come in |
| 🏆 Pass / Fail result | Clear banner with percentage score; pass mark is **65%** |
| 💾 CSV export | Every result appended to `scores.csv` automatically |

---

## File Structure

```
glt302-quiz-system/
├── glt302_quiz.py                  ← main application (single file)
├── README.md                       ← this file
├── requirements.txt                ← Python dependencies
├── analysis/
│   ├── BATCH_2_GLT_TEST.csv        ← raw Batch 2 results
│   ├── FirstBatchTESTscore.csv     ← raw Batch 1 results
│   └── GLT302_combined_scores.csv  ← appended and cleaned dataset
└── data/                           (auto-created at runtime)
    ├── attempts.json               ← device fingerprints of completed attempts
    └── scores.csv                  ← all student results
```

### `scores.csv` / `GLT302_combined_scores.csv` columns

| Column | Description |
|---|---|
| `Timestamp` | Date and time of submission |
| `Name` | Student's full name (title-cased) |
| `Score` | Percentage score (0–100) |
| `Result` | `PASS` or `FAIL` |
| `Batch` | `Batch 1` or `Batch 2` (added during merge) |

---

## Configuration

All settings live at the top of `glt302_quiz.py`:

```python
DURATION_SEC = 600   # test duration in seconds (600 = 10 min)
PASS_MARK    = 65    # pass threshold in percent
NUM_Q        = 30    # number of questions served per session
```

---

## Adding Questions

Append to the `ALL_QUESTIONS` list in `glt302_quiz.py`:

```python
{
    "q": "Your question text here?",
    "options": [
        "Option A",
        "Option B",
        "Option C",
    ],
    "answer": "Option A",   # must match one of the options exactly
},
```

The app automatically includes new questions in the random pool on next launch.

---

## Test Performance Analysis

### Dataset

| Property | Value |
|---|---|
| Test date | 13 March 2026 |
| Total submissions | 65 |
| Batch 1 submissions | 44 |
| Batch 2 submissions | 21 |
| Source files | `BATCH_2_GLT_TEST.csv`, `FirstBatchTESTscore.csv` |
| Combined file | `GLT302_combined_scores.csv` |
| Pass mark | 65% |
| Questions per session | 30 (randomly selected from 39) |

Both source files were cleaned (index columns dropped, timestamps normalised, names title-cased), a `Batch` column was added, and the files were concatenated in chronological order.

---

### Overall Results

| Metric | Value |
|---|---|
| Total students | 65 |
| Passed | 15 (23.1%) |
| Failed | 50 (76.9%) |
| Class mean | 49.1% |
| Class median | 43.3% |
| Standard deviation | 19.1% |
| Highest score | 96.7% |
| Lowest score | 16.7% |
| 10th percentile | 30.0% |
| 25th percentile | 36.7% |
| 75th percentile | 56.7% |
| 90th percentile | 82.0% |

The median of 43.3% — more than 20 points below the 65% pass mark — indicates that the majority of students had significant gaps in preparation or understanding of the material.

---

### Batch Comparison

| Metric | Batch 1 | Batch 2 |
|---|---|---|
| Students | 44 | 21 |
| Passed | 13 (29.5%) | 2 (9.5%) |
| Failed | 31 (70.5%) | 19 (90.5%) |
| Mean score | 52.4% | 42.2% |
| Median score | 46.7% | 40.0% |
| Std deviation | 18.7% | 13.1% |
| Highest score | 96.7% | 63.3% |
| Lowest score | 23.3% | 16.7% |

Batch 2's pass rate was less than a third of Batch 1's (9.5% vs 29.5%). No student in Batch 2 scored above 63.3%, meaning nobody comfortably cleared the 65% pass mark. Batch 2's lower standard deviation also suggests less score spread — most students clustered in the 30–50% range without the high-performing outliers seen in Batch 1.

---

### Score Distribution

| Band | Count | % of class |
|---|---|---|
| 0–9% | 0 | 0.0% |
| 10–19% | 1 | 1.5% |
| 20–29% | 4 | 6.2% |
| 30–39% | 16 | 24.6% |
| 40–49% | 19 | 29.2% |
| 50–59% | 10 | 15.4% |
| 60–69% | 6 | 9.2% |
| 70–79% | 1 | 1.5% |
| 80–89% | 4 | 6.2% |
| 90–100% | 4 | 6.2% |

The 30–49% band accounts for 54% of all students (35 of 65), indicating that the majority of the class has partial knowledge but falls well short of competency.

---

### Grade Bands

| Grade Band | Count | % of class | Status |
|---|---|---|---|
| Below 40% | 21 | 32.3% | FAIL |
| 40–49% | 19 | 29.2% | FAIL |
| 50–64% | 14 | 21.5% | FAIL |
| 65–74% | 2 | 3.1% | PASS |
| 75–84% | 3 | 4.6% | PASS |
| 85–100% | 6 | 9.2% | PASS |

---

### Submission Timeline

Batch 1 tested primarily between **12:00 and 14:00** (32 of 44 students), with a secondary wave at **17:00** (8 students).

Batch 2 tested entirely in the **evening — 19:00 to 21:00** (all 21 students). This late-session window likely contributed to lower performance due to fatigue, less faculty supervision, and reduced preparation time.

| Hour | Batch 1 | Batch 2 | Total |
|---|---|---|---|
| 09:00 | 1 | 0 | 1 |
| 12:00 | 20 | 0 | 20 |
| 13:00 | 7 | 0 | 7 |
| 14:00 | 5 | 0 | 5 |
| 15:00 | 2 | 0 | 2 |
| 16:00 | 1 | 0 | 1 |
| 17:00 | 8 | 0 | 8 |
| 19:00 | 0 | 13 | 13 |
| 20:00 | 0 | 5 | 5 |
| 21:00 | 0 | 3 | 3 |

---

### Top Performers

| Rank | Name | Score | Batch |
|---|---|---|---|
| 1 | Matthew Felix | 96.7% | Batch 1 |
| 1 | Ayomide Benjamin | 96.7% | Batch 1 |
| 3 | Oni Bosede Ifeoluwa | 93.3% | Batch 1 |
| 4 | Agbele Oluwasola Esther | 90.0% | Batch 1 |
| 5 | Akpan Rita Oluwabunmi | 86.7% | Batch 1 |
| 5 | Deborah Funmilola Ajibabi | 86.7% | Batch 1 |
| 7 | Stuart | 83.3% | Batch 1 |
| 8 | Oladeji Henry | 80.0% | Batch 1 |
| 9 | Alabi Ayomide | 76.7% | Batch 1 |
| 10 | Boluwatife | 66.7% | Batch 1 |

All top 10 performers came from Batch 1.

---

### Near-Miss Students (55–64%)

Four students scored within 9 points of the pass mark and are strong candidates for supplementary assessment or targeted revision:

| Name | Score | Batch |
|---|---|---|
| Precious Favour | 56.7% | Batch 1 |
| Abubakar Oluwaferanmi Abdulsheriffdeen | 56.7% | Batch 1 |
| Adejumo Boluwatife Esther | 56.7% | Batch 1 |
| Olorunfemi Oluwaseun Beatrice | 56.7% | Batch 2 |

---

### Flags & Data Quality

The following students have multiple submission records and require manual review:

| Name | Attempts | Scores | Batch | Action needed |
|---|---|---|---|---|
| Aregbesola Deborah Bukunmi | 4 | 43.3%, 43.3%, 43.3%, 23.3% | Batch 2 | Retain only the first valid attempt |
| Tope Ogala | 2 | 43.3%, 43.3% (same timestamp) | Batch 1 | Likely system duplicate — retain one |
| Adegbegi Adenike Hellen | 2 | 43.3%, 26.7% | Batch 1 | Confirm which attempt is official |
| Adejumo Boluwatife Esther | 2 | 56.7%, 33.3% | Batch 1 | Confirm which attempt is official |
| Adeniyi Faith Temitope | 2 | 60.0% (PASS), 53.3% (FAIL) | Batch 2 | **Critical** — one attempt passes, one fails |

> ⚠️ If duplicates are removed and only first attempts are counted, the effective student count drops to approximately **58 unique students**, which may alter the pass rate slightly.

---

### Key Findings

1. **Overall pass rate of 23.1% is critically low.** Only 1 in 4 students passed. This suggests either insufficient preparation, difficulty of the question bank relative to what was taught, or a mismatch between lecture content and test topics.

2. **Batch 2 significantly underperformed Batch 1.** With a pass rate of 9.5% vs 29.5% and a mean 10 points lower, the late-evening test slot is a likely contributing factor alongside possible under-preparation.

3. **The distribution is bimodal.** A cluster of high achievers (6 students above 85%) sits well apart from the majority who scored below 50%. This suggests a subset of the class engaged deeply with the material while the majority did not.

4. **More than half the class scored below 50%.** 35 of 65 students (54%) fall in the 30–49% range, indicating a partial but insufficient grasp of the subject.

5. **32% scored below 40%.** This points to foundational knowledge gaps — not near-misses, but students who were largely unprepared.

6. **No student in Batch 2 scored above 63.3%.** The ceiling effect in Batch 2 is striking and warrants investigation.

---

### Recommendations

- **Remedial session** — schedule a focused revision class covering the most-failed topics before any re-sit, targeting the 35 students in the 30–49% band.
- **Near-miss review** — the 4 students who scored 56.7% should be offered a supplementary test or oral examination.
- **Batch scheduling** — avoid scheduling test sessions after 18:00 where possible; the data strongly suggests the evening slot disadvantages students.
- **Duplicate resolution** — the 5 flagged students with multiple records must be reviewed manually before finalising the grade sheet.
- **Item analysis** — run a question-level analysis on the 39-question bank to identify which questions had the lowest correct-answer rates, which may reveal topics that need stronger coverage in lectures.
- **Increase question bank** — expanding from 39 to 60+ questions would further reduce the chance of similar question sets appearing in supplementary tests.

---

## Tech Stack

| Technology | Role |
|---|---|
| Python 3 | Core language |
| Streamlit | Web UI framework |
| Pandas | CSV handling and data analysis |
| Chart.js | Interactive visualisations in analysis dashboard |
| json / random / time | Standard library — session control, shuffling, timing |

---

## License

MIT — free to use, modify, and distribute.

---

*GLT 302 — General Instrumentation · Test System & Performance Analysis · 13 March 2026*
