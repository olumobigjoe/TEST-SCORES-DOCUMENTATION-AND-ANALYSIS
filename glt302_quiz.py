import streamlit as st
import pandas as pd
import random
import time
import os
import json
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="GLT 302 Test", page_icon="📡", layout="centered")

SCORES_CSV    = "scores.csv"
ATTEMPTS_JSON = "attempts.json"
DURATION_SEC  = 600
PASS_MARK     = 60
NUM_Q         = 30

# ─────────────────────────────────────────────────────────────────────────────
ALL_QUESTIONS = [
    {"q": "What is the definition of measurement?",
     "options": ["A process of finding the amount or magnitude of a physical quantity",
                 "A method of designing electronic circuits",
                 "A technique for repairing faulty instruments"],
     "answer": "A process of finding the amount or magnitude of a physical quantity"},

    {"q": "Which type of measurement compares the magnitude of a quantity with a reference or known value?",
     "options": ["Direct Measurement", "Indirect Measurement", "Random Measurement"],
     "answer": "Indirect Measurement"},

    {"q": "What accuracy level does a Vernier Caliper provide?",
     "options": ["0.1 mm", "0.01 mm", "1 mm"],
     "answer": "0.1 mm"},

    {"q": "Which instrument has higher accuracy – Vernier Caliper or Micrometer Screw Gauge?",
     "options": ["Vernier Caliper", "Micrometer Screw Gauge", "Both have the same accuracy"],
     "answer": "Micrometer Screw Gauge"},

    {"q": "What type of error results from human mistakes during measurement?",
     "options": ["Systematic Error", "Random Error", "Gross Error"],
     "answer": "Gross Error"},

    {"q": "Parallax error in a voltmeter reading is an example of which type of systematic error?",
     "options": ["Instrumental Error", "Observational Error", "Environmental Error"],
     "answer": "Observational Error"},

    {"q": "What term describes the degree of exactness of a measurement compared to the expected value?",
     "options": ["Precision", "Calibration", "Accuracy"],
     "answer": "Accuracy"},

    {"q": "What is the main function of a transducer in an electronic measuring instrument?",
     "options": ["Display the measured quantity",
                 "Convert a physical quantity into its equivalent electrical form",
                 "Amplify the output signal"],
     "answer": "Convert a physical quantity into its equivalent electrical form"},

    {"q": "Digital instruments use which display type for their readouts?",
     "options": ["Pointer and dial", "LED or LCD", "Cathode ray tube only"],
     "answer": "LED or LCD"},

    {"q": "The PMMC instrument gives accurate results for which type of current?",
     "options": ["AC only", "DC only", "Both AC and DC"],
     "answer": "DC only"},

    {"q": "What materials are used for the permanent magnet in a PMMC instrument?",
     "options": ["Copper and iron", "Alcomax and Alnico", "Phosphorous bronze and aluminium"],
     "answer": "Alcomax and Alnico"},

    {"q": "In the PMMC torque equation Td = NBAI, what does 'B' represent?",
     "options": ["Number of turns of coil", "Flux density in the air gap", "Effective area of the coil"],
     "answer": "Flux density in the air gap"},

    {"q": "What is one major disadvantage of a PMMC instrument?",
     "options": ["High power consumption", "Cannot be used for AC measurements", "Non-uniform scale"],
     "answer": "Cannot be used for AC measurements"},

    {"q": "A galvanometer is converted to an ammeter by connecting a shunt resistance in:",
     "options": ["Series", "Parallel", "Series-parallel"],
     "answer": "Parallel"},

    {"q": "A galvanometer is converted to a voltmeter by connecting a high resistance in:",
     "options": ["Parallel", "Series", "Delta configuration"],
     "answer": "Series"},

    {"q": "Which type of Moving Iron instrument uses the principle of attraction?",
     "options": ["Repulsion type", "Attraction type", "PMMC type"],
     "answer": "Attraction type"},

    {"q": "Moving Iron instruments can be used on:",
     "options": ["DC only", "AC only", "Both AC and DC"],
     "answer": "Both AC and DC"},

    {"q": "What error in a Moving Iron instrument is caused by hysteresis in iron parts?",
     "options": ["Readings are higher for descending values but lower for ascending values",
                 "Readings are lower for descending values",
                 "The pointer does not deflect at all"],
     "answer": "Readings are higher for descending values but lower for ascending values"},

    {"q": "What does a multimeter measure?",
     "options": ["Voltage only", "Voltage, current and resistance", "Temperature and pressure only"],
     "answer": "Voltage, current and resistance"},

    {"q": "An oscilloscope displays which of the following?",
     "options": ["Instantaneous signal voltage as a function of time",
                 "Average power of a circuit",
                 "Resistance of a component"],
     "answer": "Instantaneous signal voltage as a function of time"},

    {"q": "How must an ammeter be connected in a circuit to measure current?",
     "options": ["In parallel", "In series", "Across the load"],
     "answer": "In series"},

    {"q": "What phenomenon discovered by Seebeck forms the basis for thermocouples?",
     "options": ["Peltier effect", "Seebeck effect", "Thomson effect"],
     "answer": "Seebeck effect"},

    {"q": "What is the temperature range that thermocouples can measure?",
     "options": ["-200 C to 1300 C", "0 C to 500 C", "-100 C to 800 C"],
     "answer": "-200 C to 1300 C"},

    {"q": "A potentiometer is best described as a:",
     "options": ["Fixed resistor with two terminals",
                 "Three-terminal variable resistor",
                 "Two-terminal capacitor"],
     "answer": "Three-terminal variable resistor"},

    {"q": "Which signal generator produces sine, square, triangular and saw-tooth waveforms?",
     "options": ["Pulse Generator", "RF Signal Generator", "Function Generator"],
     "answer": "Function Generator"},

    {"q": "What is the SI unit of pressure?",
     "options": ["Bar", "Pascal (Pa)", "mmHg"],
     "answer": "Pascal (Pa)"},

    {"q": "What is the key difference between a regulated and unregulated power supply?",
     "options": ["Regulated supply maintains stable output voltage regardless of load changes; unregulated does not",
                 "Unregulated supply uses a transformer; regulated does not",
                 "Regulated supply only works on AC; unregulated on DC"],
     "answer": "Regulated supply maintains stable output voltage regardless of load changes; unregulated does not"},

    {"q": "A rectifier is used in a power supply to:",
     "options": ["Step up the voltage",
                 "Convert alternating current into direct current",
                 "Filter ripple voltage"],
     "answer": "Convert alternating current into direct current"},

    {"q": "What does SMPS stand for?",
     "options": ["Switched Mode Power Supply", "Static Magnetic Power System", "Sequential Modulated Phase Supply"],
     "answer": "Switched Mode Power Supply"},

    {"q": "In electronic troubleshooting, the split half method involves:",
     "options": ["Dividing the faulty circuit into two successive halves until the fault is identified",
                 "Tracing the fault to the functional unit of the system",
                 "Replacing half of the components at once"],
     "answer": "Dividing the faulty circuit into two successive halves until the fault is identified"},

    {"q": "What is the primary purpose of a barometer?",
     "options": ["Measure gas pressure in pipelines",
                 "Measure local atmospheric pressure",
                 "Measure the humidity of a room"],
     "answer": "Measure local atmospheric pressure"},

    {"q": "The voltage sensitivity of a galvanometer equals:",
     "options": ["Current sensitivity x Resistance of the coil",
                 "Current sensitivity / Resistance of the coil",
                 "Current sensitivity + Resistance of the coil"],
     "answer": "Current sensitivity / Resistance of the coil"},

    {"q": "Which chart recorder archives data onto a uniformly rotating circular chart?",
     "options": ["Strip Chart Recorder", "Circular Chart Recorder", "X-Y Recorder"],
     "answer": "Circular Chart Recorder"},

    {"q": "In an oscilloscope, the frequency of a signal is calculated as:",
     "options": ["f = T (period in seconds)", "f = 1 divided by T", "f = T multiplied by number of divisions"],
     "answer": "f = 1 divided by T"},

    {"q": "Which thermocouple type uses Iron and Constantan as its composition?",
     "options": ["Type K", "Type J", "Type T"],
     "answer": "Type J"},

    {"q": "What does a UPS (Uninterruptible Power Supply) primarily provide?",
     "options": ["Higher output voltage during peak load",
                 "Backup power in case of power failure or fluctuation",
                 "Voltage step-up for industrial machines"],
     "answer": "Backup power in case of power failure or fluctuation"},

    {"q": "The loading effect error in a voltmeter is most prominent when connected to:",
     "options": ["Low resistance circuits", "High resistance circuits", "Purely capacitive circuits"],
     "answer": "High resistance circuits"},

    {"q": "Swamping resistance in a PMMC instrument is used to:",
     "options": ["Increase the deflection range",
                 "Reduce the effect of temperature on the moving coil",
                 "Improve the accuracy of AC measurements"],
     "answer": "Reduce the effect of temperature on the moving coil"},

    {"q": "Which instrument is used to measure the flatness of a disc brake in a workshop?",
     "options": ["Vernier Caliper", "Dial Indicator", "Micrometer Screw Gauge"],
     "answer": "Dial Indicator"},

    {"q": "Audio signal generators typically operate over which frequency range?",
     "options": ["100 kHz to 40 GHz", "20 Hz to 20 kHz", "0.1 Hz to 3 mHz"],
     "answer": "20 Hz to 20 kHz"},
]

# ─────────────────────────────────────────────────────────────────────────────
#  FILE HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def load_attempts():
    if os.path.exists(ATTEMPTS_JSON):
        with open(ATTEMPTS_JSON) as f:
            return json.load(f)
    return {}

def save_attempt(device_id, name):
    data = load_attempts()
    data[device_id] = name
    with open(ATTEMPTS_JSON, "w") as f:
        json.dump(data, f)

def append_score(name, score_pct, passed):
    row = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name,
        "Score (%)": round(score_pct, 1),
        "Result": "PASS" if passed else "FAIL",
    }])
    if os.path.exists(SCORES_CSV):
        row.to_csv(SCORES_CSV, mode="a", header=False, index=False)
    else:
        row.to_csv(SCORES_CSV, index=False)

def load_scores():
    if os.path.exists(SCORES_CSV):
        return pd.read_csv(SCORES_CSV)
    return pd.DataFrame(columns=["Timestamp", "Name", "Score (%)", "Result"])

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
_defaults = {
    "page":         "login",
    "name":         "",
    "device_id":    str(random.getrandbits(64)),
    "questions":    [],
    "q_index":      0,
    "score":        0,          # running correct count
    "start_time":   None,
    "time_up":      False,
    "score_saved":  False,
    "score_pct":    0.0,
    "selected_opt": None,
    "confirmed":    False,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def get_remaining():
    if st.session_state.start_time is None:
        return DURATION_SEC
    return max(0.0, DURATION_SEC - (time.time() - st.session_state.start_time))

def finish_test():
    if not st.session_state.score_saved:
        pct    = (st.session_state.score / NUM_Q) * 100
        passed = pct >= PASS_MARK
        append_score(st.session_state.name, pct, passed)
        st.session_state.score_pct  = pct
        st.session_state.score_saved = True
    st.session_state.page = "result"

# ─────────────────────────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.top-bar {
    background: linear-gradient(90deg,#1a3c6e,#2e6db4);
    color:white; padding:16px 22px; border-radius:10px; margin-bottom:18px;
}
.top-bar h2 { margin:0; font-size:1.3rem; }
.top-bar p  { margin:4px 0 0; font-size:.82rem; opacity:.85; }

.timer-ok  { background:#fff3cd; border:1.5px solid #ffc107; color:#856404;
             border-radius:8px; padding:10px 18px; font-size:1.15rem;
             font-weight:700; text-align:center; margin-bottom:14px; }
.timer-low { background:#f8d7da; border:1.5px solid #dc3545; color:#842029;
             border-radius:8px; padding:10px 18px; font-size:1.15rem;
             font-weight:700; text-align:center; margin-bottom:14px; }

.qcard { background:#f8f9fa; border:1px solid #dee2e6;
         border-radius:10px; padding:18px 20px; margin-bottom:16px;
         font-size:1.05rem; line-height:1.6; }

.fb-correct { background:#d1e7dd; border:1.5px solid #0f5132; color:#0f5132;
              border-radius:8px; padding:14px 18px; font-size:1rem;
              font-weight:600; margin:10px 0; text-align:center; }
.fb-wrong   { background:#f8d7da; border:1.5px solid #842029; color:#842029;
              border-radius:8px; padding:14px 18px; font-size:1rem;
              font-weight:600; margin:10px 0; text-align:center; }

.pass-box { background:#d1e7dd; border:2px solid #0f5132; color:#0f5132;
            padding:30px; border-radius:14px; text-align:center; margin-bottom:20px; }
.fail-box { background:#f8d7da; border:2px solid #842029; color:#842029;
            padding:30px; border-radius:14px; text-align:center; margin-bottom:20px; }
.big-score { font-size:3.5rem; font-weight:700; line-height:1.2; }
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
#  LOGIN
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "login":
    st.markdown("""
    <div class="top-bar">
        <h2>📡 GLT 302 – General Instrumentation</h2>
        <p>Online Test &nbsp;|&nbsp; 30 Questions &nbsp;|&nbsp; 10 Minutes &nbsp;|&nbsp; Pass Mark: 60%</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("### 🎓 Student Login")
    name_input = st.text_input("Enter your Full Name:", placeholder="e.g. Olumodeji Ibukun")

    if st.button("▶  Start Test", type="primary", use_container_width=True):
        name = name_input.strip()
        if len(name) < 3:
            st.error("Please enter your full name (at least 3 characters).")
        else:
            attempts = load_attempts()
            dev_id   = st.session_state.device_id
            if dev_id in attempts:
                st.session_state.page = "blocked"
                st.rerun()
            else:
                save_attempt(dev_id, name)
                pool = ALL_QUESTIONS.copy()
                random.shuffle(pool)
                selected = pool[:NUM_Q]
                for q in selected:
                    opts = q["options"].copy()
                    random.shuffle(opts)
                    q["shuffled_options"] = opts

                st.session_state.name         = name
                st.session_state.questions    = selected
                st.session_state.q_index      = 0
                st.session_state.score        = 0
                st.session_state.score_pct    = 0.0
                st.session_state.score_saved  = False
                st.session_state.start_time   = time.time()
                st.session_state.time_up      = False
                st.session_state.selected_opt = None
                st.session_state.confirmed    = False
                st.session_state.page         = "test"
                st.rerun()

    st.divider()
    st.markdown("#### 📊 Live Score Board")
    df = load_scores()
    if df.empty:
        st.info("No scores recorded yet.")
    else:
        st.dataframe(df.sort_values("Timestamp", ascending=False).reset_index(drop=True),
                     use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
#  BLOCKED
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "blocked":
    st.markdown("""
    <div class="top-bar">
        <h2>📡 GLT 302 – General Instrumentation</h2>
    </div>""", unsafe_allow_html=True)
    st.error("⛔  Only **one attempt** is allowed per device. You have already taken this test.")
    st.divider()
    df = load_scores()
    if not df.empty:
        st.markdown("#### 📊 Live Score Board")
        st.dataframe(df.sort_values("Timestamp", ascending=False).reset_index(drop=True),
                     use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
#  TEST
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "test":

    remaining = get_remaining()
    if remaining <= 0 and not st.session_state.time_up:
        st.session_state.time_up = True
        finish_test()
        st.rerun()

    questions = st.session_state.questions
    q_idx     = st.session_state.q_index

    # Header
    st.markdown(f"""
    <div class="top-bar">
        <h2>📡 GLT 302 – General Instrumentation Test</h2>
        <p>Student: <strong>{st.session_state.name}</strong></p>
    </div>""", unsafe_allow_html=True)

    # Timer
    mins = int(remaining) // 60
    secs = int(remaining) % 60
    cls  = "timer-low" if remaining < 60 else "timer-ok"
    st.markdown(f'<div class="{cls}">⏱ Time Remaining: {mins:02d}:{secs:02d}</div>',
                unsafe_allow_html=True)

    # Progress
    st.markdown(f"**Question {q_idx + 1} of {NUM_Q}**")
    st.progress(q_idx / NUM_Q)
    st.write("")

    # Question
    if q_idx < NUM_Q:
        q_data    = questions[q_idx]
        confirmed = st.session_state.confirmed

        st.markdown(f'<div class="qcard"><strong>Q{q_idx + 1}.</strong>  {q_data["q"]}</div>',
                    unsafe_allow_html=True)

        if not confirmed:
            # Option buttons
            for opt in q_data["shuffled_options"]:
                is_sel = (st.session_state.selected_opt == opt)
                label  = f"{'🔵' if is_sel else '⚪'}  {opt}"
                if st.button(label, key=f"opt_{q_idx}_{opt}", use_container_width=True):
                    st.session_state.selected_opt = opt
                    st.rerun()

            st.write("")
            if st.session_state.selected_opt:
                st.info(f"**Selected:** {st.session_state.selected_opt}")
                if st.button("✔  Confirm Answer", type="primary", use_container_width=True):
                    chosen     = st.session_state.selected_opt
                    is_correct = (chosen == q_data["answer"])
                    if is_correct:
                        st.session_state.score += 1
                    st.session_state.confirmed = True
                    # Store result in question dict (no separate dict needed)
                    st.session_state.questions[q_idx]["_correct"] = is_correct
                    st.rerun()
            else:
                st.caption("👆 Select an option above, then click Confirm Answer.")

        else:
            # Show only correct / wrong — no answer revealed
            is_correct = q_data.get("_correct", False)

            if is_correct:
                st.markdown('<div class="fb-correct">✅ Correct!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="fb-wrong">❌ Wrong!</div>', unsafe_allow_html=True)

            st.write("")
            if q_idx + 1 < NUM_Q:
                if st.button("Next Question  →", type="primary", use_container_width=True):
                    st.session_state.q_index      = q_idx + 1
                    st.session_state.selected_opt = None
                    st.session_state.confirmed    = False
                    st.rerun()
            else:
                st.success("🎉 You have answered all 30 questions!")
                if st.button("📋 Submit & View Results", type="primary", use_container_width=True):
                    finish_test()
                    st.rerun()

    # Early submit
    if q_idx > 0 and q_idx < NUM_Q - 1 and st.session_state.confirmed:
        st.divider()
        with st.expander("⚠️  End test early?"):
            st.warning(f"You have answered {q_idx + 1} of {NUM_Q} questions. "
                       "Remaining questions will count as wrong.")
            if st.button("⏹  Submit Test Now", type="secondary", use_container_width=True):
                finish_test()
                st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
#  RESULT
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "result":
    st.markdown("""
    <div class="top-bar">
        <h2>📡 GLT 302 – General Instrumentation Test</h2>
        <p>Test Completed</p>
    </div>""", unsafe_allow_html=True)

    score_pct = st.session_state.score_pct
    passed    = score_pct >= PASS_MARK
    correct   = st.session_state.score

    if st.session_state.time_up:
        st.warning("⏰ Time expired – your test was automatically submitted.")

    if passed:
        st.markdown(f"""
        <div class="pass-box">
            🎉 <strong>PASSED!</strong><br>
            <span class="big-score">{score_pct:.1f}%</span><br>
            <span style="font-size:1rem;">
                {correct} out of {NUM_Q} correct
            </span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="fail-box">
            ❌ <strong>FAILED</strong><br>
            <span class="big-score">{score_pct:.1f}%</span><br>
            <span style="font-size:1rem;">
                {correct} out of {NUM_Q} correct &nbsp;|&nbsp; Pass mark: {PASS_MARK}%
            </span>
        </div>""", unsafe_allow_html=True)

    st.write("")
    st.markdown(f"**Student:** {st.session_state.name}")
    st.divider()

    st.markdown("#### 📊 Live Score Board")
    df = load_scores()
    if not df.empty:
        st.dataframe(df.sort_values("Timestamp", ascending=False).reset_index(drop=True),
                     use_container_width=True)
