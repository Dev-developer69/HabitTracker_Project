"""
Habit Tracker - Streamlit App (Local, JSON storage)
Author: Built for Devansh
Run: streamlit run app.py
"""

import streamlit as st
import json
import os
import datetime
import calendar
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# ---------------------------------------------------------------------------
# CONFIG / PATHS
# ---------------------------------------------------------------------------
# Use a path next to the exe/script so data persists locally
if getattr(__import__("sys"), "frozen", False):
    BASE_DIR = os.path.dirname(__import__("sys").executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "habit_data.json")

st.set_page_config(page_title="Habit Tracker", page_icon="🌿", layout="wide")

# ---------------------------------------------------------------------------
# CALM, SOOTHING THEME (sage green + lavender pastel palette)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Quicksand:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Soft gradient app background */
.stApp {
    background: linear-gradient(160deg, #f4f7f3 0%, #eef2f6 45%, #f3f0f7 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e8f0e6 0%, #e9e6f0 100%);
    border-right: 1px solid #d8e0d4;
}
section[data-testid="stSidebar"] * {
    color: #4a5a4a;
}

/* Main title */
h1 {
    font-family: 'Quicksand', sans-serif;
    color: #5b7065 !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
}
h2, h3, h4 {
    font-family: 'Quicksand', sans-serif;
    color: #6b6080 !important;
    font-weight: 600 !important;
}

/* Caption under title */
.stCaption, [data-testid="stCaptionContainer"] {
    color: #8a9a8a !important;
    font-style: italic;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,0.5);
    padding: 6px;
    border-radius: 16px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    padding: 10px 18px;
    background-color: transparent;
    color: #6b6080;
    font-weight: 500;
    transition: all 0.25s ease;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #c9dcc4 0%, #d6cce6 100%) !important;
    color: #4a5a4a !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* Buttons */
.stButton button, .stDownloadButton button {
    background: linear-gradient(135deg, #a8c8a0 0%, #c4b8dc 100%);
    color: #3c4a3c;
    border: none;
    border-radius: 12px;
    padding: 0.5rem 1.2rem;
    font-weight: 500;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.stButton button:hover, .stDownloadButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.12);
    color: #2c3a2c;
}

/* Checkboxes */
.stCheckbox label p {
    font-size: 1rem;
    color: #4a5a4a;
}

/* Progress bars - calm sage/lavender gradient */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #a8c8a0 0%, #c4b8dc 100%) !important;
    border-radius: 8px;
}
.stProgress > div > div {
    background-color: #e6e6ee !important;
    border-radius: 8px;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.65);
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    border: 1px solid rgba(200,200,210,0.3);
}
[data-testid="stMetricLabel"] {
    color: #8a9a8a !important;
}
[data-testid="stMetricValue"] {
    color: #5b7065 !important;
    font-family: 'Quicksand', sans-serif;
}

/* Data editor / dataframe containers */
[data-testid="stDataFrame"], div[data-testid="stDataEditor"] {
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

/* Expanders in sidebar */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.5);
    border-radius: 10px;
    font-weight: 500;
    color: #5b7065 !important;
}

/* Input fields */
.stTextInput input, .stNumberInput input, .stDateInput input {
    border-radius: 10px !important;
    border: 1px solid #d8d0e6 !important;
}

/* Subtle fade-in animation for content */
.main .block-container {
    animation: fadeIn 0.6s ease-in;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Hide default streamlit branding clutter for a calmer look */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Hide the top header bar entirely (sidebar arrow + Deploy button + colored decoration line) */
header[data-testid="stHeader"] {display: none !important;}
div[data-testid="stToolbar"] {display: none !important;}
div[data-testid="stDecoration"] {display: none !important;}
div[data-testid="stStatusWidget"] {display: none !important;}

/* Push content up since header is gone */
.block-container {
    padding-top: 2rem !important;
}

/* Nav buttons (replacing tabs) */
div[data-testid="stHorizontalBlock"] .stButton button {
    width: 100%;
    border-radius: 14px;
    font-weight: 500;
}
.nav-active button {
    background: linear-gradient(135deg, #a8c8a0 0%, #c4b8dc 100%) !important;
    color: #2c3a2c !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.12) !important;
}
.nav-inactive button {
    background: rgba(255,255,255,0.6) !important;
    color: #6b6080 !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# DATA LAYER (simple JSON file)
# ---------------------------------------------------------------------------
DEFAULT_DATA = {
    "habits": [
        {"name": "Wake up early", "goal": 25},
        {"name": "4 hours deep work", "goal": 30},
    ],
    "logs": {}  # logs["YYYY-MM-DD"] = {"Habit Name": true/false, ...}
}


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return json.loads(json.dumps(DEFAULT_DATA))
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        save_data(DEFAULT_DATA)
        return json.loads(json.dumps(DEFAULT_DATA))


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def habit_names():
    return [h["name"] for h in data["habits"]]


def habit_goal(name):
    for h in data["habits"]:
        if h["name"] == name:
            return h["goal"]
    return 0


def get_month_dates(year, month):
    num_days = calendar.monthrange(year, month)[1]
    return [datetime.date(year, month, d) for d in range(1, num_days + 1)]


def is_checked(date_str, habit):
    return data["logs"].get(date_str, {}).get(habit, False)


def set_checked(date_str, habit, value):
    data["logs"].setdefault(date_str, {})[habit] = value


def completed_count(habit, year, month):
    count = 0
    for date_str, entries in data["logs"].items():
        try:
            d = datetime.date.fromisoformat(date_str)
        except ValueError:
            continue
        if d.year == year and d.month == month and entries.get(habit):
            count += 1
    return count


def weekly_completion(year, month):
    """Returns dict week_number -> total completions across all habits."""
    dates = get_month_dates(year, month)
    weeks = {}
    for d in dates:
        week_no = (d.day - 1) // 7 + 1
        date_str = d.isoformat()
        entries = data["logs"].get(date_str, {})
        weeks.setdefault(week_no, 0)
        weeks[week_no] += sum(1 for v in entries.values() if v)
    return weeks


# ---------------------------------------------------------------------------
# SETUP — now a popover button on the main page (sidebar/header removed)
# ---------------------------------------------------------------------------
def render_setup_popover():
    with st.popover("⚙️ Setup", use_container_width=False):
        st.markdown("##### ➕ Add New Habit")
        new_habit = st.text_input("Habit name", key="new_habit_name")
        new_goal = st.number_input("Monthly goal (target days)", min_value=1, max_value=31, value=25, key="new_habit_goal")
        if st.button("Add Habit", key="add_habit_btn"):
            if new_habit.strip():
                if new_habit.strip() not in habit_names():
                    data["habits"].append({"name": new_habit.strip(), "goal": int(new_goal)})
                    save_data(data)
                    st.success(f"Added habit: {new_habit.strip()}")
                    st.rerun()
                else:
                    st.warning("Habit already exists!")
            else:
                st.warning("Enter a habit name.")

        st.markdown("---")
        st.markdown("##### 🗑️ Remove Habit")
        if habit_names():
            remove_habit = st.selectbox("Select habit to remove", habit_names(), key="remove_select")
            if st.button("Remove", key="remove_habit_btn"):
                data["habits"] = [h for h in data["habits"] if h["name"] != remove_habit]
                for date_str in data["logs"]:
                    data["logs"][date_str].pop(remove_habit, None)
                save_data(data)
                st.success(f"Removed: {remove_habit}")
                st.rerun()
        else:
            st.caption("No habits yet.")

        st.markdown("---")
        st.markdown("##### ✏️ Edit Goals")
        for h in data["habits"]:
            new_g = st.number_input(h["name"], min_value=1, max_value=31, value=h["goal"], key=f"goal_{h['name']}")
            if new_g != h["goal"]:
                h["goal"] = int(new_g)
                save_data(data)

        st.markdown("---")
        st.caption(f"📁 Data file: `{DATA_FILE}`")

# ---------------------------------------------------------------------------
# MAIN TITLE + TOP NAV (button-style instead of tabs)
# ---------------------------------------------------------------------------
st.markdown("""
<div style="text-align:center; padding: 4px 0 8px 0;">
    <h1 style="margin-bottom:0;">🌿 Habit Tracker</h1>
    <p style="color:#8a9a8a; font-style:italic; font-size:1.05rem; margin-top:4px;">
        Until you realize what it builds ✨
    </p>
</div>
""", unsafe_allow_html=True)

if "active_view" not in st.session_state:
    st.session_state.active_view = "checkin"

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 1, 0.55, 0.55])
nav_items = [
    (nav_col1, "checkin", "📌 Daily Check-in"),
    (nav_col2, "grid", "📊 Grid View"),
    (nav_col3, "progress", "📈 Progress & Charts"),
]
for col, key, label in nav_items:
    with col:
        css_class = "nav-active" if st.session_state.active_view == key else "nav-inactive"
        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.active_view = key
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with nav_col4:
    render_setup_popover()

with nav_col5:
    if st.button("🔴 Close App", key="close_app_btn", use_container_width=True,
                  help="Saves your data and fully shuts down the app (closes the background process too)"):
        save_data(data)
        st.session_state["_closing"] = True
        st.rerun()

if st.session_state.get("_closing"):
    st.markdown("""
    <div style="text-align:center; padding: 60px 0;">
        <h2>👋 Habit Tracker has been closed</h2>
        <p style="color:#8a9a8a;">Your data has been saved. You can safely close this browser tab now.</p>
    </div>
    """, unsafe_allow_html=True)

    def _delayed_exit():
        import time as _time
        import os as _os
        _time.sleep(1.5)
        _os._exit(0)

    import threading as _threading
    _threading.Thread(target=_delayed_exit, daemon=True).start()
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TAB 1 — DAILY CHECK-IN
# ---------------------------------------------------------------------------
if st.session_state.active_view == "checkin":
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_date = st.date_input("Select date", value=datetime.date.today())
    date_str = selected_date.isoformat()

    st.subheader(f"Habits for {selected_date.strftime('%d %B %Y')}")

    if not habit_names():
        st.info("No habits added yet. Use the ⚙️ Setup button above to add your first habit.")
    else:
        changed = False
        for h in data["habits"]:
            current = is_checked(date_str, h["name"])
            checked = st.checkbox(h["name"], value=current, key=f"chk_{date_str}_{h['name']}")
            if checked != current:
                set_checked(date_str, h["name"], checked)
                changed = True
        if changed:
            save_data(data)
            st.rerun()

        done_today = sum(1 for h in data["habits"] if is_checked(date_str, h["name"]))
        total_today = len(data["habits"])
        st.progress(done_today / total_today if total_today else 0)
        st.caption(f"{done_today}/{total_today} habits completed today")

# ---------------------------------------------------------------------------
# TAB 2 — GRID VIEW (spreadsheet style)
# ---------------------------------------------------------------------------
elif st.session_state.active_view == "grid":
    colA, colB = st.columns(2)
    with colA:
        sel_year = st.number_input("Year", min_value=2000, max_value=2100,
                                    value=datetime.date.today().year, key="grid_year")
    with colB:
        sel_month = st.selectbox("Month", list(range(1, 13)),
                                  index=datetime.date.today().month - 1,
                                  format_func=lambda m: calendar.month_name[m], key="grid_month")

    if not habit_names():
        st.info("No habits added yet. Use the ⚙️ Setup button above to add your first habit.")
    else:
        dates = get_month_dates(sel_year, sel_month)
        st.write("Tick the boxes below to mark a habit done on that day. Click outside the grid to save.")

        # Build a DataFrame: rows = habits, columns = day numbers (+ Goal, Completed, %)
        day_cols = [str(d.day) for d in dates]
        rows = []
        for h in data["habits"]:
            row = {"Habit": h["name"]}
            for d in dates:
                row[str(d.day)] = is_checked(d.isoformat(), h["name"])
            comp = completed_count(h["name"], sel_year, sel_month)
            row["Goal"] = h["goal"]
            row["Completed"] = comp
            row["%"] = round((comp / h["goal"]) * 100, 1) if h["goal"] else 0
            rows.append(row)

        df = pd.DataFrame(rows)

        column_config = {"Habit": st.column_config.TextColumn("Habit", disabled=True)}
        for c in day_cols:
            column_config[c] = st.column_config.CheckboxColumn(c, width="small")
        column_config["Goal"] = st.column_config.NumberColumn("Goal", disabled=True)
        column_config["Completed"] = st.column_config.NumberColumn("Completed", disabled=True)
        column_config["%"] = st.column_config.NumberColumn("%", disabled=True, format="%.1f%%")

        edited_df = st.data_editor(
            df,
            column_config=column_config,
            hide_index=True,
            use_container_width=True,
            key=f"grid_{sel_year}_{sel_month}",
        )

        # Detect changes and save
        if not edited_df[day_cols].equals(df[day_cols]):
            for _, row in edited_df.iterrows():
                habit_name = row["Habit"]
                for d in dates:
                    col = str(d.day)
                    set_checked(d.isoformat(), habit_name, bool(row[col]))
            save_data(data)
            st.rerun()

        # Overall month progress bar chart (like the screenshot's orange bars)
        st.markdown("#### Overall Progress")
        overall_df = pd.DataFrame({
            "Habit": [h["name"] for h in data["habits"]],
            "Completed": [completed_count(h["name"], sel_year, sel_month) for h in data["habits"]],
            "Goal": [h["goal"] for h in data["habits"]],
        })
        overall_df["% Complete"] = (overall_df["Completed"] / overall_df["Goal"] * 100).round(1)
        st.dataframe(
            overall_df,
            column_config={
                "% Complete": st.column_config.ProgressColumn(
                    "% Complete", min_value=0, max_value=100, format="%.1f%%"
                )
            },
            hide_index=True,
            use_container_width=True,
        )

# ---------------------------------------------------------------------------
# TAB 3 — PROGRESS & CHARTS
# ---------------------------------------------------------------------------
elif st.session_state.active_view == "progress":
    colA, colB = st.columns(2)
    with colA:
        py = st.number_input("Year", min_value=2000, max_value=2100,
                              value=datetime.date.today().year, key="prog_year")
    with colB:
        pm = st.selectbox("Month", list(range(1, 13)),
                           index=datetime.date.today().month - 1,
                           format_func=lambda m: calendar.month_name[m], key="prog_month")

    if not habit_names():
        st.info("No habits added yet. Use the ⚙️ Setup button above to add your first habit.")
    else:
        # Weekly completion bar chart
        st.markdown("#### Weekly Completion (all habits combined)")
        weeks = weekly_completion(py, pm)
        if weeks:
            week_labels = [f"Week {w}" for w in sorted(weeks.keys())]
            week_vals = [weeks[w] for w in sorted(weeks.keys())]
            max_val = max(week_vals) if week_vals else 0

            if max_val == 0:
                st.info("No check-ins logged yet for this month — tick some habits in Daily Check-in or Grid View first, and this chart will fill up. 🌱")
            else:
                fig, ax = plt.subplots(figsize=(8, 3.5))
                fig.patch.set_alpha(0.0)
                ax.set_facecolor("none")
                palette = ["#a8c8a0", "#bcd0c8", "#c4b8dc", "#d6cce6", "#a8c8a0", "#c4b8dc"]
                colors = [palette[i % len(palette)] for i in range(len(week_vals))]
                bars = ax.bar(week_labels, week_vals, color=colors, edgecolor="white", linewidth=1.2, width=0.55)
                ax.set_ylabel("Total check-ins", color="#6b6080", fontsize=10)
                ax.set_ylim(0, max_val * 1.25)
                ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))
                ax.tick_params(colors="#6b6080")
                for bar in bars:
                    height = bar.get_height()
                    ax.annotate(f"{int(height)}", xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 4), textcoords="offset points", ha="center",
                                fontsize=9, color="#4a5a4a", fontweight="medium")
                ax.spines[["top", "right", "left"]].set_visible(False)
                ax.spines["bottom"].set_color("#d8d8e0")
                ax.grid(axis="y", linestyle="--", alpha=0.25, color="#b0b8c0")
                st.pyplot(fig, transparent=True)

        st.markdown("#### Per-Habit Progress")
        for h in data["habits"]:
            comp = completed_count(h["name"], py, pm)
            goal = h["goal"]
            pct = min(comp / goal, 1.0) if goal else 0
            left = goal - comp
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"**{h['name']}**")
                st.progress(pct)
            with c2:
                st.metric("Completed / Goal", f"{comp}/{goal}", f"{left:+d} left")

        # Overall stats
        total_completed = sum(completed_count(h["name"], py, pm) for h in data["habits"])
        total_goal = sum(h["goal"] for h in data["habits"])
        overall_pct = round((total_completed / total_goal) * 100, 1) if total_goal else 0
        st.markdown("---")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Completed", total_completed)
        m2.metric("Total Goal", total_goal)
        m3.metric("Overall %", f"{overall_pct}%")