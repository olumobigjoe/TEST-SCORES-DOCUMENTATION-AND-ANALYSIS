import streamlit as st
import pandas as pd
import random
import time
import os
import json
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GLT 302 – General Instrumentation Test",
    page_icon="📡",
    layout="centered",
)

# ── Paths ─────────────────────────────────────────────────────────────────────
SCORES_CSV   = "scores.csv"
ATTEMPTS_JSON = "attempts.json"

# ── Question bank (30 base questions; app picks 30 randomly per session) ──────
ALL_QUESTIONS = [
    {
        "q": "What is the definition of measurement?",
        "options": [
            "A process of finding the amount or magnitude of a physical quantity",
            "A method of designing electronic circuits",
            "A technique for repairing faulty instruments",
        ],
        "answer": "A process of finding the amount or magnitude of a physical quantity",
    },
    {
        "q": "Which type of measurement compares the magnitude of a quantity with a reference or known value?",
        "options": [
            "Direct Measurement",
            "Indirect Measurement",
            "Random Measurement",
        ],
        "answer": "Indirect Measurement",
    },
    {
        "q": "What accuracy level does a Vernier Caliper provide?",
        "options": ["0.1 mm", "0.01 mm", "1 mm"],
        "answer": "0.1 mm",
    },
    {
        "q": "Which instrument has a higher accuracy – Vernier Caliper or Micrometer Screw Gauge?",
        "options": [
            "Vernier Caliper",
            "Micrometer Screw Gauge",
            "Both have the same accuracy",
        ],
        "answer": "Micrometer Screw Gauge",
    },
    {
        "q": "What type of error results from human mistakes during measurement?",
        "options": ["Systematic Error", "Random Error", "Gross Error"],
        "answer": "Gross Error",
    },
    {
        "q": "Parallax error in a voltmeter reading is an example of which type of systematic error?",
        "options": [
            "Instrumental Error",
            "Observational Error",
            "Environmental Error",
        ],
        "answer": "Observational Error",
    },
    {
        "q": "What term describes the degree of exactness of a measurement compared to the expected value?",
        "options": ["Precision", "Calibration", "Accuracy"],
        "answer": "Accuracy",
    },
    {
        "q": "What is the main function of a transducer in an electronic measuring instrument?",
        "options": [
            "Display the measured quantity",
            "Convert a physical quantity into its equivalent electrical form",
            "Amplify the output signal",
        ],
        "answer": "Convert a physical quantity into its equivalent electrical form",
    },
    {
        "q": "Digital instruments use which display type for their readouts?",
        "options": [
            "Pointer and dial",
            "LED or LCD",
            "Cathode ray tube only",
        ],
        "answer": "LED or LCD",
    },
    {
        "q": "The PMMC instrument gives accurate results for which type of current?",
        "options": ["AC only", "DC only", "Both AC and DC"],
        "answer": "DC only",
    },
    {
        "q": "What materials are used for the permanent magnet in a PMMC instrument?",
        "options": [
            "Copper and iron",
            "Alcomax and Alnico",
            "Phosphorous bronze and aluminium",
        ],
        "answer": "Alcomax and Alnico",
    },
    {
        "q": "In a PMMC instrument, the deflecting torque equation is Td = NBAI. What does 'B' represent?",
        "options": [
            "Number of turns of coil",
            "Flux density in the air gap",
            "Effective area of the coil",
        ],
        "answer": "Flux density in the air gap",
    },
    {
        "q": "What is one major disadvantage of a PMMC instrument?",
        "options": [
            "High power consumption",
            "Cannot be used for AC measurements",
            "Non-uniform scale",
        ],
        "answer": "Cannot be used for AC measurements",
    },
    {
        "q": "A galvanometer is converted to an ammeter by connecting a shunt resistance in:",
        "options": ["Series", "Parallel", "Series-parallel"],
        "answer": "Parallel",
    },
    {
        "q": "A galvanometer is converted to a voltmeter by connecting a high resistance in:",
        "options": ["Parallel", "Series", "Delta configuration"],
        "answer": "Series",
    },
    {
        "q": "Which type of Moving Iron instrument uses the principle of attraction?",
        "options": [
            "Repulsion type",
            "Attraction type",
            "PMMC type",
        ],
        "answer": "Attraction type",
    },
    {
        "q": "Moving Iron instruments can be used on:",
        "options": [
            "DC only",
            "AC only",
            "Both AC and DC",
        ],
        "answer": "Both AC and DC",
    },
    {
        "q": "What error in a Moving Iron instrument is caused by hysteresis in iron parts?",
        "options": [
            "Readings are higher for descending values but lower for ascending values",
            "Readings are lower for descending values",
            "The pointer does not deflect at all",
        ],
        "answer": "Readings are higher for descending values but lower for ascending values",
    },
    {
        "q": "What does a multimeter measure?",
        "options": [
            "Voltage only",
            "Voltage, current and resistance",
            "Temperature and pressure only",
        ],
        "answer": "Voltage, current and resistance",
    },
    {
        "q": "An oscilloscope displays which of the following?",
        "options": [
            "Instantaneous signal voltage as a function of time",
            "Average power of a circuit",
            "Resistance of a component",
        ],
        "answer": "Instantaneous signal voltage as a function of time",
    },
    {
        "q": "How must an ammeter be connected in a circuit to measure current?",
        "options": ["In parallel", "In series", "Across the load"],
        "answer": "In series",
    },
    {
        "q": "What phenomenon discovered by Seebeck forms the basis for thermocouples?",
        "options": [
            "Peltier effect",
            "Seebeck effect",
            "Thomson effect",
        ],
        "answer": "Seebeck effect",
    },
    {
        "q": "What is the temperature range that thermocouples can measure?",
        "options": [
            "-200°C to 1300°C",
            "0°C to 500°C",
            "-100°C to 800°C",
        ],
        "answer": "-200°C to 1300°C",
    },
    {
        "q": "A potentiometer is described as a:",
        "options": [
            "Fixed resistor with two terminals",
            "Three-terminal variable resistor",
            "Two-terminal capacitor",
        ],
        "answer": "Three-terminal variable resistor",
    },
    {
        "q": "Which type of signal generator produces sine, square, triangular and saw-tooth waveforms?",
        "options": [
            "Pulse Generator",
            "RF Signal Generator",
            "Function Generator",
        ],
        "answer": "Function Generator",
    },
    {
        "q": "What is the SI unit of pressure?",
        "options": ["Bar", "Pascal (Pa)", "mmHg"],
        "answer": "Pascal (Pa)",
    },
    {
        "q": "What is the main difference between a regulated and unregulated power supply?",
        "options": [
            "Regulated supply has stable output voltage regardless of load changes; unregulated does not",
            "Unregulated supply uses a transformer; regulated does not",
            "Regulated supply only works on AC; unregulated on DC",
        ],
        "answer": "Regulated supply has stable output voltage regardless of load changes; unregulated does not",
    },
    {
        "q": "A rectifier is used in a power supply to:",
        "options": [
            "Step up the voltage",
            "Convert alternating current into direct current",
            "Filter ripple voltage",
        ],
        "answer": "Convert alternating current into direct current",
    },
    {
        "q": "What does SMPS stand for?",
        "options": [
            "Switched Mode Power Supply",
            "Static Magnetic Power System",
            "Sequential Modulated Phase Supply",
        ],
        "answer": "Switched Mode Power Supply",
    },
    {
        "q": "In electronic troubleshooting, the 'split half method' refers to:",
        "options": [
            "Dividing the faulty circuit into two successive halves until the fault is identified",
            "Tracing the fault to the functional unit of the system",
            "Replacing half of the components at once",
        ],
        "answer": "Dividing the faulty circuit into two successive halves until the fault is identified",
    },
    {
        "q": "What is the purpose of a barometer?",
        "options": [
            "Measure gas pressure in pipelines",
            "Measure local atmospheric pressure",
            "Measure the humidity of a room",
        ],
        "answer": "Measure local atmospheric pressure",
    },
    {
        "q": "The voltage sensitivity of a galvanometer equals:",
        "options": [
            "Current sensitivity × Resistance of the coil",
            "Current sensitivity / Resistance of the coil",
            "Current sensitivity + Resistance of the coil",
        ],
        "answer": "Current sensitivity / Resistance of the coil",
    },
    {
        "q": "Which chart recorder archives data onto a uniformly rotating circular chart?",
        "options": [
            "Strip Chart Recorder",
            "Circular Chart Recorder",
            "X-Y Recorder",
        ],
        "answer": "Circular Chart Recorder",
    },
    {
        "q": "In an oscilloscope, frequency of a signal is calculated as:",
        "options": [
            "f = T (period in seconds)",
            "f = 1 / T",
            "f = T × number of divisions",
        ],
        "answer": "f = 1 / T",
    },
    {
        "q": "Which thermocouple type uses Iron and Constantan as its composition?",
        "options": ["Type K", "Type J", "Type T"],
        "answer": "Type J",
    },
    {
        "q": "What does a UPS (Uninterruptible Power Supply) primarily provide?",
        "options": [
            "Higher output voltage during peak load",
            "Backup power in case of power failure or fluctuation",
            "Voltage step-up for industrial machines",
        ],
        "answer": "Backup power in case of power failure or fluctuation",
    },
    {
        "q": "The loading effect error in a voltmeter is most prominent when connected to:",
        "options": [
            "Low resistance circuits",
            "High resistance circuits",
            "Purely capacitive circuits",
        ],
        "answer": "High resistance circuits",
    },
    {
        "q": "Swamping resistance in a PMMC instrument is used to:",
        "options": [
            "Increase the deflection range",
            "Reduce the effect of temperature on the moving coil",
            "Improve the accuracy of AC measurements",
        ],
        "answer": "Reduce the effect of temperature on the moving coil",
    },
    {
        "q": "Which instrument is used to measure the flatness of a disc brake in a car workshop?",
        "options": ["Vernier Caliper", "Dial Indicator", "Micrometer Screw Gauge"],
        "answer": "Dial Indicator",
    },
    {
        "q": "Audio signal generators typically operate over which frequency range?",
        "options": [
            "100 kHz to 40 GHz",
            "20 Hz to 20 kHz",
            "0.1 Hz to 3 mHz",
        ],
        "answer": "20 Hz to 20 kHz",
    },
]

DURATION_SECONDS = 10 * 60  # 10 minutes
PASS_SCORE = 64              # pass mark (%)
NUM_QUESTIONS = 30

# ── Helper: load / save attempts ──────────────────────────────────────────────
def load_attempts():
    if os.path.exists(ATTEMPTS_JSON):
        with open(ATTEMPTS_JSON, "r") as f:
            return json.load(f)
    return {}

def save_attempts(data):
    with open(ATTEMPTS_JSON, "w") as f:
        json.dump(data, f)

def get_device_id():
    """Use session-stable fingerprint stored in st.session_state."""
    if "device_id" not in st.session_state:
        st.session_state["device_id"] = str(random.getrandbits(64))
    return st.session_state["device_id"]

# ── Helper: scores CSV ────────────────────────────────────────────────────────
def append_score(name, score_pct, passed):
    row = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name,
        "Score (%)": round(score_pct, 1),
        "Result": "PASS" if passed else "FAIL",
    }
    df_new = pd.DataFrame([row])
    if os.path.exists(SCORES_CSV):
        df_new.to_csv(SCORES_CSV, mode="a", header=False, index=False)
    else:
        df_new.to_csv(SCORES_CSV, mode="w", header=True, index=False)

def load_scores():
    if os.path.exists(SCORES_CSV):
        return pd.read_csv(SCORES_CSV)
    return pd.DataFrame(columns=["Timestamp", "Name", "Score (%)", "Result"])

# ── Session state init ────────────────────────────────────────────────────────
defaults = {
    "page": "login",          # login | test | result | blocked
    "student_name": "",
    "questions": [],
    "current_q": 0,
    "answers": {},            # idx -> chosen option
    "feedback": {},           # idx -> bool (correct?)
    "score": 0,
    "start_time": None,
    "time_up": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
body { font-family: 'Segoe UI', sans-serif; }
.header-bar {
    background: linear-gradient(90deg,#1a3c6e,#2e6db4);
    color:white; padding:18px 24px; border-radius:10px; margin-bottom:20px;
}
.header-bar h2 { margin:0; font-size:1.35rem; }
.header-bar p  { margin:4px 0 0; font-size:.85rem; opacity:.85; }
.timer-box {
    background:#fff3cd; border:1px solid #ffc107;
    border-radius:8px; padding:10px 16px;
    font-size:1.1rem; font-weight:600; color:#856404; text-align:center;
}
.qcard {
    background:#f8f9fa; border:1px solid #dee2e6;
    border-radius:10px; padding:20px; margin-bottom:12px;
}
.correct-msg  { background:#d1e7dd; border:1px solid #0f5132; color:#0f5132; padding:10px; border-radius:6px; }
.wrong-msg    { background:#f8d7da; border:1px solid #842029; color:#842029; padding:10px; border-radius:6px; }
.pass-banner  { background:#d1e7dd; border:2px solid #0f5132; color:#0f5132;
                padding:24px; border-radius:12px; text-align:center; font-size:1.4rem; }
.fail-banner  { background:#f8d7da; border:2px solid #842029; color:#842029;
                padding:24px; border-radius:12px; text-align:center; font-size:1.4rem; }
.score-num { font-size:3rem; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: LOGIN
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "login":
    st.markdown("""
    <div class="header-bar">
        <h2>📡 GLT 302 – General Instrumentation</h2>
        <p>Online Test &nbsp;|&nbsp; Duration: 10 minutes &nbsp;|&nbsp; 30 Questions &nbsp;|&nbsp; Pass: 65%</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Student Login")
    name_input = st.text_input("Enter your Full Name to begin:", placeholder="e.g. Adaeze Okonkwo")

    if st.button("Start Test", type="primary"):
        name = name_input.strip()
        if not name or len(name) < 3:
            st.error("Please enter your full name (at least 3 characters).")
        else:
            device_id = get_device_id()
            attempts = load_attempts()
            if device_id in attempts:
                st.session_state.page = "blocked"
                st.rerun()
            else:
                # Mark attempt
                attempts[device_id] = name
                save_attempts(attempts)

                # Pick 30 random questions
                pool = ALL_QUESTIONS.copy()
                random.shuffle(pool)
                selected = pool[:NUM_QUESTIONS]
                # Shuffle options for each question
                for q in selected:
                    ops = q["options"].copy()
                    random.shuffle(ops)
                    q["shuffled_options"] = ops

                st.session_state.student_name = name
                st.session_state.questions    = selected
                st.session_state.current_q    = 0
                st.session_state.answers      = {}
                st.session_state.feedback     = {}
                st.session_state.score        = 0
                st.session_state.start_time   = time.time()
                st.session_state.time_up      = False
                st.session_state.page         = "test"
                st.rerun()

    st.divider()
    st.markdown("#### 📊 Live Score Board")
    df_scores = load_scores()
    if df_scores.empty:
        st.info("No scores recorded yet.")
    else:
        st.dataframe(
            df_scores.sort_values("Timestamp", ascending=False).reset_index(drop=True),
            use_container_width=True,
        )

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: BLOCKED
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "blocked":
    st.markdown("""
    <div class="header-bar">
        <h2>📡 GLT 302 – General Instrumentation</h2>
    </div>
    """, unsafe_allow_html=True)
    st.error("⛔ Only one attempt is allowed per device. You have already taken this test.")
    st.markdown("#### 📊 Live Score Board")
    df_scores = load_scores()
    if not df_scores.empty:
        st.dataframe(df_scores.sort_values("Timestamp", ascending=False).reset_index(drop=True), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: TEST
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "test":
    questions   = st.session_state.questions
    current_idx = st.session_state.current_q
    elapsed     = time.time() - st.session_state.start_time
    remaining   = max(0, DURATION_SECONDS - elapsed)

    # ── Timer check ──────────────────────────────────────────────────────────
    if remaining <= 0 and not st.session_state.time_up:
        st.session_state.time_up = True
        # Compute score from answered questions
        correct = sum(1 for v in st.session_state.feedback.values() if v)
        pct = (correct / NUM_QUESTIONS) * 100
        passed = pct >= PASS_SCORE
        append_score(st.session_state.student_name, pct, passed)
        st.session_state.score = pct
        st.session_state.page  = "result"
        st.rerun()

    # ── Header ───────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="header-bar">
        <h2>📡 GLT 302 – General Instrumentation Test</h2>
        <p>Student: <strong>{st.session_state.student_name}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # ── Timer display ─────────────────────────────────────────────────────────
    mins = int(remaining) // 60
    secs = int(remaining) % 60
    timer_color = "#856404"
    if remaining < 60:
        timer_color = "#842029"
    st.markdown(f'<div class="timer-box" style="color:{timer_color}">⏱ Time Remaining: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    # Auto-refresh every second
    st.markdown('<meta http-equiv="refresh" content="1">', unsafe_allow_html=True)

    st.markdown(f"**Progress: {min(current_idx + 1, NUM_QUESTIONS)} / {NUM_QUESTIONS}**")
    st.progress((current_idx) / NUM_QUESTIONS)

    # ── Show all answered questions (feedback) ────────────────────────────────
    if current_idx > 0:
        with st.expander(f"✅ Reviewed Questions (1 – {current_idx})", expanded=False):
            for i in range(current_idx):
                q_data  = questions[i]
                chosen  = st.session_state.answers.get(i, "")
                correct = st.session_state.feedback.get(i, False)
                icon    = "✔️" if correct else "❌"
                st.markdown(f"**Q{i+1}. {q_data['q']}**")
                st.markdown(f"{icon} Your answer: _{chosen}_")
                if not correct:
                    st.markdown(f"✅ Correct answer: _{q_data['answer']}_")
                st.divider()

    # ── Current question ──────────────────────────────────────────────────────
    if current_idx < NUM_QUESTIONS:
        q_data = questions[current_idx]
        already_answered = current_idx in st.session_state.answers

        st.markdown(f'<div class="qcard"><strong>Q{current_idx + 1}. {q_data["q"]}</strong></div>', unsafe_allow_html=True)

        if not already_answered:
            chosen = st.radio(
                "Select your answer:",
                q_data["shuffled_options"],
                key=f"q_{current_idx}",
                index=None,
            )

            if chosen is not None:
                is_correct = chosen == q_data["answer"]
                st.session_state.answers[current_idx]  = chosen
                st.session_state.feedback[current_idx] = is_correct

                if is_correct:
                    st.markdown('<div class="correct-msg">✔️ Correct!</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="wrong-msg">❌ Wrong. The correct answer is: <strong>{q_data["answer"]}</strong></div>', unsafe_allow_html=True)

                # Move to next
                time.sleep(0.8)
                if current_idx + 1 < NUM_QUESTIONS:
                    st.session_state.current_q = current_idx + 1
                else:
                    # All answered
                    correct_count = sum(1 for v in st.session_state.feedback.values() if v)
                    pct   = (correct_count / NUM_QUESTIONS) * 100
                    passed = pct >= PASS_SCORE
                    append_score(st.session_state.student_name, pct, passed)
                    st.session_state.score = pct
                    st.session_state.page  = "result"
                st.rerun()
        else:
            chosen    = st.session_state.answers[current_idx]
            is_correct = st.session_state.feedback[current_idx]
            st.info(f"Your answer: **{chosen}**")
            if is_correct:
                st.markdown('<div class="correct-msg">✔️ Correct!</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="wrong-msg">❌ Wrong. Correct: <strong>{q_data["answer"]}</strong></div>', unsafe_allow_html=True)

            if st.button("Next Question →", key="next_btn"):
                if current_idx + 1 < NUM_QUESTIONS:
                    st.session_state.current_q = current_idx + 1
                else:
                    correct_count = sum(1 for v in st.session_state.feedback.values() if v)
                    pct   = (correct_count / NUM_QUESTIONS) * 100
                    passed = pct >= PASS_SCORE
                    append_score(st.session_state.student_name, pct, passed)
                    st.session_state.score = pct
                    st.session_state.page  = "result"
                st.rerun()

    # ── Submit button ─────────────────────────────────────────────────────────
    st.divider()
    if len(st.session_state.answers) > 0:
        if st.button("⏹ Submit Test Now", type="secondary"):
            correct_count = sum(1 for v in st.session_state.feedback.values() if v)
            pct   = (correct_count / NUM_QUESTIONS) * 100
            passed = pct >= PASS_SCORE
            append_score(st.session_state.student_name, pct, passed)
            st.session_state.score = pct
            st.session_state.page  = "result"
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: RESULT
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "result":
    st.markdown("""
    <div class="header-bar">
        <h2>📡 GLT 302 – General Instrumentation Test</h2>
        <p>Test Completed</p>
    </div>
    """, unsafe_allow_html=True)

    score_pct = st.session_state.score
    passed    = score_pct >= PASS_SCORE
    correct   = sum(1 for v in st.session_state.feedback.values() if v)

    if st.session_state.time_up:
        st.warning("⏰ Time is up! Your test has been automatically submitted.")

    if passed:
        st.markdown(f"""
        <div class="pass-banner">
            🎉 PASSED!<br>
            <span class="score-num">{score_pct:.1f}%</span><br>
            <span style="font-size:1rem;">You answered {correct} out of {NUM_QUESTIONS} questions correctly.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="fail-banner">
            ❌ FAILED<br>
            <span class="score-num">{score_pct:.1f}%</span><br>
            <span style="font-size:1rem;">You answered {correct} out of {NUM_QUESTIONS} questions correctly.</span><br>
            <span style="font-size:.9rem;">Pass mark: {PASS_SCORE}%</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Question Review")
    questions = st.session_state.questions
    for i, q_data in enumerate(questions):
        chosen     = st.session_state.answers.get(i, "Not answered")
        is_correct = st.session_state.feedback.get(i, False)
        icon       = "✔️" if is_correct else "❌"
        bg         = "#d1e7dd" if is_correct else "#f8d7da"
        st.markdown(f"""
        <div style="background:{bg}; border-radius:8px; padding:12px; margin-bottom:8px;">
            <strong>{icon} Q{i+1}. {q_data['q']}</strong><br>
            Your answer: <em>{chosen}</em><br>
            {'✅ Correct!' if is_correct else f'Correct answer: <strong>{q_data["answer"]}</strong>'}
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 📊 Live Score Board")
    df_scores = load_scores()
    if not df_scores.empty:
        st.dataframe(
            df_scores.sort_values("Timestamp", ascending=False).reset_index(drop=True),
            use_container_width=True,
        )