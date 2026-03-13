# 📡 GLT 302 – General Instrumentation Online Quiz System

A fully featured browser-based examination platform built with **Python + Streamlit** for the course *GLT 302 — General Instrumentation*.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔐 Name-based login | Students enter their full name to begin |
| 🎲 Randomised questions | 30 drawn randomly from a bank of 39; option order shuffled too |
| ⏱️ 10-minute countdown | Auto-submits when time runs out |
| ✅ Instant feedback | "Correct" or "Wrong" shown after each answer (no answer revealed) |
| 🛡️ Anti-cheat | One attempt per device — enforced via device fingerprinting |
| 📊 Live score board | Visible on the login page; updates as results come in |
| 🏆 Pass / Fail result | Clear banner with percentage; pass mark is **65%** |
| 💾 CSV export | Every result saved to `scores.csv` automatically |

---

## 🚀 Quick Start

### 1. Clone

```bash
git clone https://github.com/olumobigjoe/glt302-quiz-system.git
cd glt302-quiz-system
```

### 2. Install dependencies

```bash
pip install streamlit pandas
```

### 3. Run

```bash
streamlit run glt302_quiz.py
```

The app opens at `http://localhost:8501`.  
Share the **Network URL** shown in the terminal with students on the same Wi-Fi.

---

## 📁 File Structure

```
glt302-quiz-system/
├── glt302_quiz.py      ← main application (single file)
├── README.md
├── requirements.txt
└── data/               (auto-created at runtime)
    ├── attempts.json   ← device fingerprints of completed attempts
    └── scores.csv      ← all student results
```

### scores.csv columns

| Column | Description |
|---|---|
| `Timestamp` | Date and time of submission |
| `Name` | Student's full name |
| `Score (%)` | Percentage score (0–100) |
| `Result` | `PASS` or `FAIL` |

---

## ⚙️ Configuration

All settings live at the top of `glt302_quiz.py`:

```python
DURATION_SEC = 600   # test duration in seconds (600 = 10 min)
PASS_MARK    = 65    # pass threshold in percent
NUM_Q        = 30    # number of questions served per session
```

---

## 📚 Adding Questions

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

The app will automatically include new questions in the random pool.

---

## 🌐 Deploying to Streamlit Cloud (Free)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → select this repo → set main file to `glt302_quiz.py`.
4. Click **Deploy**. You'll get a public URL to share with students anywhere.

---

## 🔄 Reset Attempts

To allow students to retake the test (e.g. for a new session), delete the auto-generated files:

```bash
rm attempts.json scores.csv
```

---

## 🛠️ Tech Stack

- **Python 3** — core language
- **Streamlit** — UI framework
- **Pandas** — CSV read/write
- **json / random / time** — standard library modules

---

## 📄 License

MIT — free to use, modify, and distribute.

---

*Built for GLT 302 — General Instrumentation*
