"""
=============================================================================
  Mini-Neptun - University Academic Management System
=============================================================================
  Developed by : EKKE - Software Engineering Student Project
  Framework    : Streamlit
  Data storage : Streamlit session_state (in-memory, mock data)

  Roles:
    1. Administrator (Admin)  - manage users and courses
    2. Teacher                - manage student rosters and grades
    3. Student                - course enrollment, view grades
=============================================================================
"""

import streamlit as st
import streamlit.components.v1 as components
import random
import string
import json
from pathlib import Path
import pandas as pd
from datetime import datetime

DATA_FILE = Path(__file__).parent / "data.json"

# -----------------------------------------------------------------------------
#  PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Mini-Neptun",
    page_icon="'",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
#  CUSTOM CSS - theme-responsive modern appearance
# -----------------------------------------------------------------------------
st.markdown("""
<style>
/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* -- Remove white header stripe " keep toolbar visible --------------------- */
[data-testid="stHeader"] {
    background: transparent !important;
    backdrop-filter: none !important;
}

/* Hide only the Deploy button text */
[data-testid="stToolbarActionButtonLabel"] { display: none !important; }

/* -- Main background - follows Streamlit theme ---------------------------- */
.stApp {
    background-color: var(--background-color) !important;
    min-height: 100vh;
}

/* Overlay gradient that blends with the theme background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background: linear-gradient(160deg,
        rgba(14, 30, 60, 0.45) 0%,
        rgba(10, 22, 48, 0.30) 50%,
        rgba(8, 25, 50, 0.40) 100%);
    pointer-events: none;
    z-index: 0;
}

/* -- Sidebar -------------------------------------------------------------- */
[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color) !important;
    border-right: 1px solid rgba(56, 139, 253, 0.18);
}

/* -- Heading text --------------------------------------------------------- */
h1 { color: var(--text-color) !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }
h2 { color: var(--text-color) !important; font-weight: 600 !important; opacity: 0.75; }
h3 { color: var(--text-color) !important; font-weight: 600 !important; opacity: 0.9; }

/* -- Paragraph / subtitle text -------------------------------------------- */
p:not(.stButton p):not(.stFormSubmitButton p), .stMarkdown p {
    color: var(--text-color) !important;
    opacity: 0.65;
}

/* -- Button text - always white ------------------------------------------- */
.stButton > button p,
.stButton > button,
.stFormSubmitButton > button p,
.stFormSubmitButton > button {
    color: #ffffff !important;
}

/* -- Cards / containers --------------------------------------------------- */
.mini-card {
    background: var(--secondary-background-color);
    border: 1px solid rgba(56, 139, 253, 0.2);
    border-radius: 12px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 1rem;
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
.mini-card:hover {
    border-color: rgba(56, 139, 253, 0.45);
    box-shadow: 0 4px 24px rgba(14, 165, 233, 0.08);
}

/* -- Metric cards --------------------------------------------------------- */
[data-testid="stMetric"] {
    background: rgba(14, 165, 233, 0.06);
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    border: 1px solid rgba(14, 165, 233, 0.18);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(14, 165, 233, 0.4);
    box-shadow: 0 2px 16px rgba(14, 165, 233, 0.08);
}
[data-testid="stMetricLabel"] { color: var(--text-color) !important; font-size: 0.82rem !important; font-weight: 500 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; opacity: 0.6; }
[data-testid="stMetricValue"] { color: var(--text-color) !important; font-weight: 700 !important; font-size: 1.7rem !important; }
[data-testid="stMetricDelta"] { color: #34d399 !important; font-size: 0.82rem !important; }

/* -- Buttons --------------------------------------------------------------- */
.stButton > button {
    background: #1565a8 !important;
    color: #ffffff !important;
    border: 1px solid #2d7fc1 !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
    line-height: 1.5 !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.4) !important;
}
.stButton > button:hover {
    background: #1d7fc4 !important;
    border-color: #4a9fd4 !important;
    box-shadow: 0 4px 16px rgba(14, 165, 233, 0.35) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    background: #0f5490 !important;
}

/* -- Form submit buttons --------------------------------------------------- */
.stFormSubmitButton > button {
    background: #1565a8 !important;
    color: #ffffff !important;
    border: 1px solid #2d7fc1 !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.8rem !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
    width: 100% !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.4) !important;
}
.stFormSubmitButton > button:hover {
    background: #1d7fc4 !important;
    border-color: #4a9fd4 !important;
    box-shadow: 0 4px 16px rgba(14, 165, 233, 0.35) !important;
    transform: translateY(-1px) !important;
}

/* -- Tabs ------------------------------------------------------------------ */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid rgba(56, 139, 253, 0.15) !important;
    gap: 2px;
    background: transparent !important;
}
[data-testid="stTabs"] [role="tab"] {
    color: var(--text-color) !important;
    opacity: 0.5;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 0.5rem 1.1rem !important;
    transition: color 0.18s ease, background 0.18s ease !important;
    border: none !important;
    background: transparent !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    opacity: 0.75;
    background: rgba(14, 165, 233, 0.05) !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #38bdf8 !important;
    opacity: 1;
    font-weight: 600 !important;
    border-bottom: 2px solid #0ea5e9 !important;
    background: rgba(14, 165, 233, 0.07) !important;
}

/* -- Dataframe ------------------------------------------------------------- */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid rgba(56, 139, 253, 0.15);
}

/* -- Alert messages ------------------------------------------------------- */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border-left-width: 3px !important;
}

/* -- Expander -------------------------------------------------------------- */
[data-testid="stExpander"] {
    background: var(--secondary-background-color) !important;
    border: 1px solid rgba(56, 139, 253, 0.18) !important;
    border-radius: 10px !important;
    margin-bottom: 0.5rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stExpander"]:hover {
    border-color: rgba(14, 165, 233, 0.35) !important;
}

/* -- Divider --------------------------------------------------------------- */
hr { border-color: rgba(56, 139, 253, 0.12) !important; }

/* -- Badge style ----------------------------------------------------------- */
.badge {
    display: inline-block;
    padding: 2px 9px;
    border-radius: 5px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-left: 6px;
    vertical-align: middle;
}
.badge-admin   { background: rgba(239, 68, 68, 0.12);  color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.3); }
.badge-teacher { background: rgba(251, 191, 36, 0.12); color: #fde68a; border: 1px solid rgba(251, 191, 36, 0.3); }
.badge-student { background: rgba(52, 211, 153, 0.12); color: #6ee7b7; border: 1px solid rgba(52, 211, 153, 0.3); }

/* -- Caption text ---------------------------------------------------------- */
.stCaption, [data-testid="stCaptionContainer"] {
    font-size: 0.8rem !important;
}

/* -- Scrollbar ------------------------------------------------------------- */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(56,139,253,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(56,139,253,0.5); }
</style>
""", unsafe_allow_html=True)



# -----------------------------------------------------------------------------
#  HELPER FUNCTIONS
# -----------------------------------------------------------------------------

def generate_neptun_code() -> str:
    """Generate a unique 6-character Neptun code (e.g. AB1234)."""
    letters = random.choices(string.ascii_uppercase, k=2)
    digits  = random.choices(string.digits, k=4)
    code    = "".join(letters + digits)
    # Ensure uniqueness
    existing = {u["neptun"] for u in st.session_state.users.values()}
    while code in existing:
        letters = random.choices(string.ascii_uppercase, k=2)
        digits  = random.choices(string.digits, k=4)
        code    = "".join(letters + digits)
    return code


def get_user_by_neptun(neptun: str) -> dict | None:
    """Return a user by their Neptun code."""
    return st.session_state.users.get(neptun)


def get_courses_for_teacher(teacher_neptun: str) -> list[dict]:
    """Return all courses assigned to a teacher."""
    return [
        c for c in st.session_state.courses.values()
        if c["teacher_neptun"] == teacher_neptun
    ]


def get_enrolled_courses_for_student(student_neptun: str) -> list[dict]:
    """Return all courses a student is enrolled in."""
    return [
        c for c in st.session_state.courses.values()
        if student_neptun in c["enrolled_students"]
    ]


def get_grade_label(grade: int | None) -> str:
    """Convert a numeric grade to a text label."""
    mapping = {5: "Excellent (5)", 4: "Good (4)", 3: "Average (3)",
               2: "Pass (2)", 1: "Fail (1)"}
    return mapping.get(grade, "-")


def calc_average(grades: list[int]) -> float | None:
    """Calculate the average of grades (including fails)."""
    valid = [g for g in grades if g is not None]
    if not valid:
        return None
    return round(sum(valid) / len(valid), 2)



# -----------------------------------------------------------------------------
#  PERSISTENCE
# -----------------------------------------------------------------------------

def save_data():
    """Persist users and courses to data.json next to app.py."""
    payload = {
        "users":   st.session_state.users,
        "courses": st.session_state.courses,
    }
    DATA_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


# -----------------------------------------------------------------------------
#  DATA INITIALISATION
# -----------------------------------------------------------------------------

def init_data():
    """
    Load data from data.json if it exists, otherwise seed with default data.
    Only runs once per session (guarded by 'initialized' in session_state).
    """
    if "initialized" in st.session_state:
        return

    if DATA_FILE.exists():
        try:
            payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            st.session_state.users   = payload["users"]
            st.session_state.courses = payload["courses"]
            st.session_state.initialized = True
            return
        except Exception:
            pass  # Fall through to seed data if file is corrupt

    # -- Default seed data --------------------------------------
    st.session_state.users = {
        "ADMIN1": {"name": "System Administrator", "role": "admin",    "neptun": "ADMIN1"},
        "DR1234": {"name": "Dr. Peter Kovacs",     "role": "teacher",  "neptun": "DR1234"},
        "DR5678": {"name": "Dr. Eva Nagy",          "role": "teacher",  "neptun": "DR5678"},
        "HA1111": {"name": "Anna Kiss",             "role": "student",  "neptun": "HA1111"},
        "HA2222": {"name": "Bence Toth",            "role": "student",  "neptun": "HA2222"},
        "HA3333": {"name": "Reka Varga",            "role": "student",  "neptun": "HA3333"},
    }
    st.session_state.courses = {
        "PROGFUND": {
            "name": "Fundamentals of Programming", "code": "PROGFUND",
            "max_seats": 30, "teacher_neptun": "DR1234",
            "enrolled_students": ["HA1111", "HA2222", "HA3333"],
            "grades": {"HA1111": 5, "HA2222": 4, "HA3333": None},
        },
        "DBMGMT": {
            "name": "Database Management", "code": "DBMGMT",
            "max_seats": 25, "teacher_neptun": "DR1234",
            "enrolled_students": ["HA1111", "HA3333"],
            "grades": {"HA1111": None, "HA3333": 3},
        },
        "COMPNET": {
            "name": "Computer Networks", "code": "COMPNET",
            "max_seats": 20, "teacher_neptun": "DR5678",
            "enrolled_students": ["HA2222"],
            "grades": {"HA2222": 5},
        },
        "MATHANA": {
            "name": "Mathematical Analysis", "code": "MATHANA",
            "max_seats": 40, "teacher_neptun": "DR5678",
            "enrolled_students": [], "grades": {},
        },
    }
    st.session_state.initialized = True
    save_data()


# -----------------------------------------------------------------------------
#  AUTHENTICATION
# -----------------------------------------------------------------------------

def authenticate(username: str, password: str) -> str | None:
    """
    Validate credentials and return the matching Neptun code, or None.
    - Admin : username='admin', password='a'  -> returns 'ADMIN1'
    - Teacher/Student: username=neptun, password=neptun
    """
    u = username.strip().upper()
    p = password.strip()

    # Special admin login
    if username.strip().lower() == "admin" and p == "a":
        return "ADMIN1"

    # Neptun-code login for teachers and students
    if u in st.session_state.users and p.upper() == u:
        user = st.session_state.users[u]
        if user["role"] in ("teacher", "student"):
            return u

    return None


def render_login():
    """Full-screen login page shown before the app."""
    col_l, col_c, col_r = st.columns([1, 1.1, 1])
    with col_c:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        st.markdown("""
<div style='text-align:center; margin-bottom:2rem;'>
  <div style='font-size:2.8rem; margin-bottom:0.3rem;'>'</div>
  <div style='font-size:1.8rem; font-weight:700; color:#e2e8f0; letter-spacing:-0.02em;'>Mini-Neptun</div>
  <div style='font-size:0.85rem; color:#475569; margin-top:4px;'>University Academic Management System</div>
</div>
""", unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            st.markdown("<div style='margin-bottom:0.3rem; font-size:0.8rem; color:#64748b; text-transform:uppercase; letter-spacing:0.06em;'>Username</div>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="admin  /  Neptun code",
                                     label_visibility="collapsed")
            st.markdown("<div style='margin-bottom:0.3rem; margin-top:0.8rem; font-size:0.8rem; color:#64748b; text-transform:uppercase; letter-spacing:0.06em;'>Password</div>", unsafe_allow_html=True)
            password = st.text_input("Password", type="password",
                                     placeholder="password",
                                     label_visibility="collapsed")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            login_btn = st.form_submit_button("Sign In", use_container_width=True)

        if login_btn:
            neptun = authenticate(username, password)
            if neptun:
                st.session_state.authenticated = True
                st.session_state.current_user  = neptun
                st.rerun()
            else:
                st.error("Invalid username or password.")

        st.markdown("""
<div style='margin-top:1.5rem; padding:1rem; background:rgba(14,165,233,0.06);
     border:1px solid rgba(14,165,233,0.18); border-radius:8px; font-size:0.78rem; color:#64748b;'>
  <strong style='color:#94a3b8;'>Login credentials:</strong><br/>
  Admin &nbsp;&nbsp;&nbsp;-> &nbsp;<code style='color:#38bdf8;'>admin</code> / <code style='color:#38bdf8;'>a</code><br/>
  Teacher/Student -> Neptun code as both username &amp; password
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
#  SIDEBAR - profile panel (shown after login)
# -----------------------------------------------------------------------------

def render_sidebar():
    """Sidebar: current user profile + logout button."""
    with st.sidebar:
        st.markdown("## ' Mini-Neptun")
        st.markdown("<p style='color:#64748b; font-size:0.85rem; margin-top:-8px;'>University Academic Management System</p>", unsafe_allow_html=True)
        st.divider()

        user = st.session_state.users[st.session_state.current_user]
        role = user["role"]

        role_labels   = {"admin": "Administrator", "teacher": "Teacher", "student": "Student"}
        badge_classes = {"admin": "badge-admin", "teacher": "badge-teacher", "student": "badge-student"}
        role_icons    = {"admin": "'", "teacher": "''", "student": "'"}

        st.markdown(f"""
<div class="mini-card">
  <div style="font-size:0.72rem; color:#475569; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.07em;">Logged in as</div>
  <div style="font-size:1.05rem; font-weight:700; color:#e2e8f0; margin-bottom:6px;">{user['name']}</div>
  <div style="margin-bottom:10px;">
    <span style="color:#475569; font-size:0.8rem;">Neptun:&nbsp;</span>
    <span style="background:rgba(14,165,233,0.1); color:#38bdf8; border:1px solid rgba(14,165,233,0.25); border-radius:5px; padding:2px 8px; font-size:0.82rem; font-family:monospace; font-weight:600;">{user['neptun']}</span>
  </div>
  <div>
    <span style="font-size:0.9rem;">{role_icons[role]}</span>
    <span class="badge {badge_classes[role]}">{role_labels[role]}</span>
  </div>
</div>
""", unsafe_allow_html=True)

        st.divider()
        if st.button("Sign Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_user  = None
            st.rerun()

        st.markdown(f"""
<div style="font-size:0.72rem; color:#374151; text-align:center; line-height:1.7; margin-top:1rem;">
  Mini-Neptun v1.0 &middot; EKKE<br/>
  {datetime.now().strftime('%Y-%m-%d %H:%M')}
</div>
""", unsafe_allow_html=True)

    return user




# -----------------------------------------------------------------------------
#  ADMIN VIEW
# -----------------------------------------------------------------------------

def render_admin(user: dict):
    """Admin main page: user registration and course management."""
    st.markdown("# ' Administrator Panel")
    st.markdown("<p style='color:#94a3b8;'>Manage users and courses in the system.</p>", unsafe_allow_html=True)
    st.divider()

    tab_users, tab_courses, tab_overview = st.tabs([
        "Users", "Courses", "Overview"
    ])

    # -- Tab 1: User Registration + Management --------------------------------
    with tab_users:
        col_form, col_list = st.columns([1, 1.5], gap="large")

        with col_form:
            st.markdown("### Register New User")
            with st.form("form_new_user", clear_on_submit=True):
                new_name = st.text_input("Full name", placeholder="e.g. Dr. John Smith")
                new_role = st.selectbox(
                    "Role",
                    options=["student", "teacher", "admin"],
                    format_func=lambda r: {"student": "Student",
                                           "teacher": "Teacher",
                                           "admin":   "Administrator"}[r]
                )
                submitted = st.form_submit_button("Register User", use_container_width=True)

                if submitted:
                    if not new_name.strip():
                        st.error("Name is required.")
                    else:
                        neptun = generate_neptun_code()
                        st.session_state.users[neptun] = {
                            "name": new_name.strip(),
                            "role": new_role,
                            "neptun": neptun,
                        }
                        save_data()
                        st.success(f"User registered! Neptun code: **{neptun}**")
                        st.balloons()

            # -- Edit selected user --------------------------------------------
            if st.session_state.get("edit_user_neptun"):
                en = st.session_state.edit_user_neptun
                eu = st.session_state.users.get(en)
                if eu:
                    st.divider()
                    st.markdown(f"### (Edit) Edit User `{en}`")
                    with st.form("form_edit_user", clear_on_submit=False):
                        edit_name = st.text_input("Full name", value=eu["name"])
                        role_opts = ["student", "teacher", "admin"]
                        edit_role = st.selectbox(
                            "Role",
                            options=role_opts,
                            index=role_opts.index(eu["role"]),
                            format_func=lambda r: {"student": "Student",
                                                   "teacher": "Teacher",
                                                   "admin":   "Administrator"}[r]
                        )
                        c1, c2 = st.columns(2)
                        save_edit = c1.form_submit_button("Save", use_container_width=True)
                        cancel    = c2.form_submit_button("Cancel", use_container_width=True)

                    if save_edit:
                        if not edit_name.strip():
                            st.error("Name cannot be empty.")
                        else:
                            st.session_state.users[en]["name"] = edit_name.strip()
                            st.session_state.users[en]["role"] = edit_role
                            st.session_state.edit_user_neptun = None
                            save_data()
                            st.success(f"User **{en}** updated.")
                            st.rerun()
                    if cancel:
                        st.session_state.edit_user_neptun = None
                        st.rerun()

        with col_list:
            st.markdown("### Registered Users")
            role_icons  = {"admin": "'", "teacher": "''", "student": "'"}
            role_labels = {"admin": "Admin", "teacher": "Teacher", "student": "Student"}

            current_neptun = st.session_state.current_user

            for u in list(st.session_state.users.values()):
                neptun = u["neptun"]
                is_self = (neptun == current_neptun)

                with st.container():
                    c_name, c_role, c_edit, c_del = st.columns([2.5, 1.5, 0.9, 0.9])
                    c_name.markdown(
                        f"<div style='padding:6px 0; font-weight:600; color:#e2e8f0; font-size:0.88rem;'>"
                        f"{u['name']}<br/>"
                        f"<span style='color:#38bdf8; font-family:monospace; font-size:0.75rem; font-weight:400;'>{neptun}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    c_role.markdown(
                        f"<div style='padding:8px 0; font-size:0.82rem; color:#94a3b8;'>"
                        f"{role_icons[u['role']]} {role_labels[u['role']]}</div>",
                        unsafe_allow_html=True
                    )
                    if c_edit.button("(Edit)", key=f"edit_{neptun}", use_container_width=True,
                                     help="Edit user"):
                        st.session_state.edit_user_neptun = neptun
                        st.rerun()

                    # Prevent deleting yourself or the last admin
                    admins = [x for x in st.session_state.users.values() if x["role"] == "admin"]
                    can_delete = not is_self and not (u["role"] == "admin" and len(admins) <= 1)
                    if can_delete:
                        if c_del.button("[X]", key=f"del_{neptun}", use_container_width=True,
                                        help="Delete user"):
                            del st.session_state.users[neptun]
                            # Remove from courses too
                            for course in st.session_state.courses.values():
                                if neptun in course["enrolled_students"]:
                                    course["enrolled_students"].remove(neptun)
                                course["grades"].pop(neptun, None)
                            save_data()
                            st.success(f"User **{neptun}** deleted.")
                            st.rerun()
                    else:
                        c_del.markdown(
                            "<div style='padding:6px 4px; font-size:0.72rem; color:#374151; text-align:center;'></div>",
                            unsafe_allow_html=True
                        )
                    st.markdown("<hr style='margin:2px 0; border-color:rgba(56,139,253,0.1);'/>", unsafe_allow_html=True)

            st.caption(f"Total: **{len(st.session_state.users)}** users")


    # -- Tab 2: Course Management ----------------------------------------------
    with tab_courses:
        col_form2, col_list2 = st.columns([1, 1.5], gap="large")

        with col_form2:
            st.markdown("### Add New Course")
            teachers = {
                neptun: u["name"]
                for neptun, u in st.session_state.users.items()
                if u["role"] == "teacher"
            }
            if not teachers:
                st.warning("No teachers found. Please register a teacher first.")
            else:
                with st.form("form_new_course", clear_on_submit=True):
                    course_name = st.text_input(
                        "Course name", placeholder="e.g. Algorithms and Data Structures"
                    )
                    course_code = st.text_input(
                        "Course code", placeholder="e.g. ALGADS"
                    ).upper()
                    max_seats = st.number_input(
                        "Maximum seats", min_value=1, max_value=200, value=25
                    )
                    teacher_neptun = st.selectbox(
                        "Teacher",
                        options=list(teachers.keys()),
                        format_func=lambda n: f"{teachers[n]} ({n})"
                    )
                    submitted2 = st.form_submit_button("Add Course", use_container_width=True)

                    if submitted2:
                        if not course_name.strip() or not course_code.strip():
                            st.error("Course name and code are required.")
                        elif course_code in st.session_state.courses:
                            st.error(f"A course with code '{course_code}' already exists.")
                        else:
                            st.session_state.courses[course_code] = {
                                "name": course_name.strip(),
                                "code": course_code,
                                "max_seats": int(max_seats),
                                "teacher_neptun": teacher_neptun,
                                "enrolled_students": [],
                                "grades": {},
                            }
                            save_data()
                            st.success(f"**{course_name}** added. (Code: {course_code})")

            # -- Edit selected course ------------------------------------------
            if st.session_state.get("edit_course_code"):
                ec = st.session_state.edit_course_code
                course_obj = st.session_state.courses.get(ec)
                if course_obj and teachers:
                    st.divider()
                    st.markdown(f"### (Edit) Edit Course `{ec}`")
                    with st.form("form_edit_course", clear_on_submit=False):
                        edit_cname = st.text_input("Course name", value=course_obj["name"])
                        edit_seats = st.number_input(
                            "Maximum seats", min_value=1, max_value=200,
                            value=course_obj["max_seats"]
                        )
                        teacher_keys = list(teachers.keys())
                        cur_teacher_idx = teacher_keys.index(course_obj["teacher_neptun"]) \
                            if course_obj["teacher_neptun"] in teacher_keys else 0
                        edit_teacher = st.selectbox(
                            "Teacher",
                            options=teacher_keys,
                            index=cur_teacher_idx,
                            format_func=lambda n: f"{teachers[n]} ({n})"
                        )
                        ec1, ec2 = st.columns(2)
                        save_course = ec1.form_submit_button("Save", use_container_width=True)
                        cancel_c    = ec2.form_submit_button("Cancel", use_container_width=True)

                    if save_course:
                        if not edit_cname.strip():
                            st.error("Course name cannot be empty.")
                        else:
                            st.session_state.courses[ec]["name"]           = edit_cname.strip()
                            st.session_state.courses[ec]["max_seats"]      = int(edit_seats)
                            st.session_state.courses[ec]["teacher_neptun"] = edit_teacher
                            st.session_state.edit_course_code = None
                            save_data()
                            st.success(f"Course **{ec}** updated.")
                            st.rerun()
                    if cancel_c:
                        st.session_state.edit_course_code = None
                        st.rerun()

        with col_list2:
            st.markdown("### Available Courses")

            if not st.session_state.courses:
                st.info("No courses have been added yet.")
            else:
                for c in list(st.session_state.courses.values()):
                    code     = c["code"]
                    teacher  = st.session_state.users.get(c["teacher_neptun"], {})
                    enrolled = len(c["enrolled_students"])

                    with st.container():
                        c_info, c_meta, c_edit, c_del = st.columns([2.2, 1.8, 0.7, 0.7])
                        c_info.markdown(
                            f"<div style='padding:5px 0; font-weight:600; color:#e2e8f0; font-size:0.88rem;'>"
                            f"{c['name']}<br/>"
                            f"<span style='color:#38bdf8; font-family:monospace; font-size:0.75rem; font-weight:400;'>{code}</span>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                        c_meta.markdown(
                            f"<div style='padding:5px 0; font-size:0.78rem; color:#94a3b8;'>"
                            f"' {teacher.get('name','-')}<br/>"
                            f"<span style='color:#64748b;'>{enrolled}/{c['max_seats']} seats</span>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                        if c_edit.button("(Edit)", key=f"cedit_{code}", use_container_width=True,
                                         help="Edit course"):
                            st.session_state.edit_course_code = code
                            st.rerun()
                        if c_del.button("[X]", key=f"cdel_{code}", use_container_width=True,
                                        help="Delete course"):
                            del st.session_state.courses[code]
                            save_data()
                            st.success(f"Course **{code}** deleted.")
                            st.rerun()
                        st.markdown("<hr style='margin:2px 0; border-color:rgba(56,139,253,0.1);'/>",
                                    unsafe_allow_html=True)

                st.caption(f"Total: **{len(st.session_state.courses)}** courses")


    # -- Tab 3: Overview -------------------------------------------------------
    with tab_overview:
        st.markdown("### System Statistics")
        all_users = list(st.session_state.users.values())
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", len(all_users))
        with col2:
            st.metric("Students",
                      sum(1 for u in all_users if u["role"] == "student"))
        with col3:
            st.metric("Teachers",
                      sum(1 for u in all_users if u["role"] == "teacher"))
        with col4:
            st.metric("Courses", len(st.session_state.courses))

        st.divider()
        st.markdown("### Course Capacity")
        if st.session_state.courses:
            chart_data = pd.DataFrame([
                {
                    "Course": f"{c['code']} - {c['name'][:20]}",
                    "Enrolled": len(c["enrolled_students"]),
                    "Available Seats": c["max_seats"] - len(c["enrolled_students"]),
                }
                for c in st.session_state.courses.values()
            ]).set_index("Course")
            st.bar_chart(chart_data)


# -----------------------------------------------------------------------------
#  TEACHER VIEW
# -----------------------------------------------------------------------------

def render_teacher(user: dict):
    """Teacher panel: own courses, student rosters, grade entry."""
    st.markdown(f"# '' Teacher Panel")
    st.markdown(f"<p style='color:#94a3b8;'>Welcome, <strong style='color:#e2e8f0;'>{user['name']}</strong>. Manage your courses and students.</p>", unsafe_allow_html=True)
    st.divider()

    my_courses = get_courses_for_teacher(user["neptun"])

    if not my_courses:
        st.info("No courses are currently assigned to you. Please contact an administrator.")
        return

    tab_list, tab_grades = st.tabs(["My Courses & Rosters", "Grade Entry"])

    # -- Tab 1: Course list + rosters ------------------------------------------
    with tab_list:
        st.markdown("### My Courses")

        for course in my_courses:
            enrolled_count = len(course["enrolled_students"])
            with st.expander(
                f"{course['name']}  ({course['code']})  "
                f"{enrolled_count}/{course['max_seats']} students",
                expanded=(enrolled_count > 0)
            ):
                if not course["enrolled_students"]:
                    st.info("No students are enrolled in this course yet.")
                    continue

                # Interactive per-student roster with inline grade edit
                for neptun in course["enrolled_students"]:
                    student = st.session_state.users.get(neptun, {})
                    grade   = course["grades"].get(neptun)
                    edit_key = f"grade_edit_{course['code']}_{neptun}"
                    is_editing = st.session_state.get(edit_key, False)

                    r_name, r_neptun, r_grade, r_btn = st.columns([2, 1.2, 2.2, 0.7])
                    r_name.markdown(
                        f"<div style='padding:6px 0; color:#e2e8f0; font-size:0.87rem; font-weight:500;'>"
                        f"{student.get('name','-')}</div>",
                        unsafe_allow_html=True
                    )
                    r_neptun.markdown(
                        f"<div style='padding:6px 0; color:#38bdf8; font-family:monospace; font-size:0.8rem;'>"
                        f"{neptun}</div>",
                        unsafe_allow_html=True
                    )

                    if is_editing:
                        with r_grade:
                            new_g = st.selectbox(
                                "Grade",
                                options=[5, 4, 3, 2, 1],
                                index=0 if grade is None else (5 - grade),
                                format_func=get_grade_label,
                                key=f"gsel_{course['code']}_{neptun}",
                                label_visibility="collapsed"
                            )
                        with r_btn:
                            sv = st.button("[Save]", key=f"gsave_{course['code']}_{neptun}",
                                           use_container_width=True, help="Save grade")
                            cn = st.button("[X]", key=f"gcancel_{course['code']}_{neptun}",
                                           use_container_width=True, help="Cancel")
                        if sv:
                            st.session_state.courses[course["code"]]["grades"][neptun] = new_g
                            st.session_state[edit_key] = False
                            save_data()
                            st.rerun()
                        if cn:
                            st.session_state[edit_key] = False
                            st.rerun()
                    else:
                        r_grade.markdown(
                            f"<div style='padding:6px 0; font-size:0.85rem; color:#94a3b8;'>"
                            f"{get_grade_label(grade)}</div>",
                            unsafe_allow_html=True
                        )
                        if r_btn.button("(Edit)", key=f"gedit_{course['code']}_{neptun}",
                                        use_container_width=True, help="Edit grade"):
                            st.session_state[edit_key] = True
                            st.rerun()

                    st.markdown(
                        "<hr style='margin:1px 0; border-color:rgba(56,139,253,0.08);'/>",
                        unsafe_allow_html=True
                    )


    # -- Tab 2: Grade Entry ----------------------------------------------------
    with tab_grades:
        st.markdown("### Enter / Modify Grade")

        course_options = {f"{c['name']} ({c['code']})": c["code"] for c in my_courses}
        if not course_options:
            st.warning("No courses available.")
            return

        selected_course_label = st.selectbox(
            "Select course", list(course_options.keys()), key="teacher_course_sel"
        )
        selected_course_code = course_options[selected_course_label]
        course = st.session_state.courses[selected_course_code]

        if not course["enrolled_students"]:
            st.info("No students are enrolled in this course yet.")
        else:
            student_options = {}
            for neptun in course["enrolled_students"]:
                s = st.session_state.users.get(neptun, {})
                student_options[f"{s.get('name','?')} ({neptun})"] = neptun

            selected_student_label = st.selectbox(
                "Select student", list(student_options.keys()), key="teacher_student_sel"
            )
            selected_student_neptun = student_options[selected_student_label]

            current_grade = course["grades"].get(selected_student_neptun)

            col_grade, col_btn = st.columns([2, 1])
            with col_grade:
                new_grade = st.selectbox(
                    "New grade",
                    options=[5, 4, 3, 2, 1],
                    index=0 if current_grade is None else (5 - current_grade),
                    format_func=get_grade_label,
                    key="grade_select"
                )
            with col_btn:
                st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                save_btn = st.button("Save Grade", use_container_width=True, key="save_grade_btn")

            # Current grade display
            st.markdown(
                f"<div style='margin-top:0.4rem; font-size:0.85rem; color:#64748b;'>"
                f"Current grade: <strong style='color:#e2e8f0;'>{get_grade_label(current_grade)}</strong></div>",
                unsafe_allow_html=True
            )

            if save_btn:
                st.session_state.courses[selected_course_code]["grades"][
                    selected_student_neptun
                ] = new_grade
                student_name = st.session_state.users[selected_student_neptun]["name"]
                st.success(
                    f"[OK] {student_name}'s grade set to: **{get_grade_label(new_grade)}**"
                )
                st.rerun()



# 
#  STUDENT VIEW
# 

def render_student(user: dict):
    """Student panel: course enrollment and transcript view."""
    st.markdown("# 🎓 Student Portal")
    st.markdown(f"<p style='color:#94a3b8;'>Welcome, <strong style='color:#e2e8f0;'>{user['name']}</strong>. Manage your courses and view your grades.</p>", unsafe_allow_html=True)
    st.divider()

    tab_enroll, tab_transcript = st.tabs(["Course Enrollment", "My Transcript & GPA"])

    student_neptun = user["neptun"]

    #  Tab 1: Course Enrollment 
    with tab_enroll:
        st.markdown("### Available Courses")
        
        if not st.session_state.courses:
            st.info("No courses are available at this time.")
        else:
            for course in list(st.session_state.courses.values()):
                code = course["code"]
                teacher = st.session_state.users.get(course["teacher_neptun"], {})
                enrolled_list = course["enrolled_students"]
                is_enrolled = student_neptun in enrolled_list
                enrolled_count = len(enrolled_list)
                max_seats = course["max_seats"]
                is_full = enrolled_count >= max_seats

                with st.container():
                    c_info, c_meta, c_action = st.columns([2.5, 2.0, 1.0])
                    
                    # Display badge if full (CR-01 requirement)
                    badge_html = " <span class='badge badge-admin'>[FULL]</span>" if is_full else ""
                    
                    c_info.markdown(
                        f"<div style='padding:5px 0; font-weight:600; color:#e2e8f0; font-size:0.88rem;'>"
                        f"{course['name']}{badge_html}<br/>"
                        f"<span style='color:#38bdf8; font-family:monospace; font-size:0.75rem; font-weight:400;'>{code}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    
                    c_meta.markdown(
                        f"<div style='padding:5px 0; font-size:0.78rem; color:#94a3b8;'>"
                        f" Instructor: {teacher.get('name', '-')}<br/>"
                        f"<span style='color:#64748b;'>Seats: {enrolled_count}/{max_seats}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    
                    with c_action:
                        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                        if is_enrolled:
                            if st.button("Drop Course", key=f"drop_{code}", use_container_width=True):
                                course["enrolled_students"].remove(student_neptun)
                                course["grades"].pop(student_neptun, None)
                                save_data()
                                st.success(f"Successfully dropped {code}.")
                                st.rerun()
                        else:
                            # Disable button if full (CR-01 requirement)
                            if st.button("Enroll", key=f"enroll_{code}", disabled=is_full, use_container_width=True):
                                course["enrolled_students"].append(student_neptun)
                                course["grades"][student_neptun] = None
                                save_data()
                                st.success(f"Successfully enrolled in {code}.")
                                st.rerun()
                                
                    st.markdown("<hr style='margin:2px 0; border-color:rgba(56,139,253,0.1);'/>", unsafe_allow_html=True)

    #  Tab 2: Transcript & GPA 
    with tab_transcript:
        st.markdown("### Academic Performance")
        
        enrolled_courses = get_enrolled_courses_for_student(student_neptun)
        
        if not enrolled_courses:
            st.info("You are not enrolled in any courses.")
        else:
            col_grades, col_gpa = st.columns([2, 1], gap="large")
            
            with col_grades:
                st.markdown("#### Enrolled Course Grades")
                
                grades_list = []
                for course in enrolled_courses:
                    code = course["code"]
                    grade = course["grades"].get(student_neptun)
                    
                    r_name, r_code, r_grade = st.columns([3, 1, 2])
                    r_name.markdown(f"<div style='padding:6px 0; color:#e2e8f0; font-size:0.87rem; font-weight:500;'>{course['name']}</div>", unsafe_allow_html=True)
                    r_code.markdown(f"<div style='padding:6px 0; color:#38bdf8; font-family:monospace; font-size:0.8rem;'>{code}</div>", unsafe_allow_html=True)
                    r_grade.markdown(f"<div style='padding:6px 0; font-size:0.85rem; color:#94a3b8;'>{get_grade_label(grade)}</div>", unsafe_allow_html=True)
                    
                    if grade is not None:
                        grades_list.append(grade)
                        
                    st.markdown("<hr style='margin:1px 0; border-color:rgba(56,139,253,0.08);'/>", unsafe_allow_html=True)
            
            with col_gpa:
                st.markdown("#### GPA & Summary")
                gpa = calc_average(grades_list)
                
                if gpa is not None:
                    st.metric("Grade Point Average (GPA)", f"{gpa:.2f}")
                    # Motivation message based on GPA (CR-04 requirement)
                    if gpa >= 4.5:
                        st.success(" Outstanding academic performance! Keep it up!")
                    elif gpa >= 3.5:
                        st.info(" Good progress! Aim higher next time.")
                    else:
                        st.warning(" Keep studying to improve your GPA.")
                else:
                    st.metric("Grade Point Average (GPA)", "-")
                    st.info("No grades entered yet.")


# 
#  MAIN RUNNER
# 
init_data()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    render_login()
else:
    user = render_sidebar()
    if user["role"] == "admin":
        render_admin(user)
    elif user["role"] == "teacher":
        render_teacher(user)
    elif user["role"] == "student":
        render_student(user)