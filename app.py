import streamlit as st
import gspread
import pandas as pd
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
import io
import re
import json

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

HEADERS = ["Date", "Day", "Work Done Today", "Submission Time"]
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# --------------------------------------------------
# GOOGLE SHEETS CONNECTION
# --------------------------------------------------

def connect_to_google_sheets():
    """
    Connects to Google Sheets using credentials.
    On Streamlit Cloud: uses st.secrets
    On local machine: reads from service_account.json
    """
    try:
        if "gcp_service_account" in st.secrets:
            creds = Credentials.from_service_account_info(
                st.secrets["gcp_service_account"],
                scopes=SCOPES
            )
        else:
            key_path = r"C:\Users\91942\Downloads\Logify\service_account.json"
            with open(key_path, "r", encoding="utf-8") as f:
                service_account_info = json.load(f)
            creds = Credentials.from_service_account_info(
                service_account_info,
                scopes=SCOPES
            )

        client = gspread.authorize(creds)
        return client

    except FileNotFoundError:
        st.error("service_account.json not found.")
        st.stop()
    except Exception as e:
        st.error(f"Could not connect to Google Sheets: {e}")
        st.stop()


def get_user_sheet(client, user_name):
    """
    Each user gets their own Google Sheet named: Logify - TheirName
    If the sheet does not exist, it is created automatically.
    If headers are missing, they are added.

    This means:
    - Preksha gets: "Logify - Preksha"
    - John gets: "Logify - John"
    - Each person's data is completely private and separate.
    """
    # Clean up the name - remove extra spaces, capitalize nicely
    clean_name = user_name.strip().title()

    # Each user gets their own sheet named after them
    sheet_name = f"Logify - {clean_name}"

    try:
        spreadsheet = client.open(sheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        # Sheet doesn't exist yet - create it for this user
        spreadsheet = client.create(sheet_name)
        # Share it so the user can also view it if they want
        spreadsheet.share(None, perm_type="anyone", role="writer")

    sheet = spreadsheet.sheet1

    # Add headers if the sheet is empty
    existing_data = sheet.get_all_values()
    if not existing_data or existing_data[0] != HEADERS:
        sheet.insert_row(HEADERS, index=1)

    return sheet, clean_name


# --------------------------------------------------
# DATE AND TIME HELPERS
# --------------------------------------------------

def get_today_date():
    return datetime.now().strftime("%d %B %Y")

def get_today_day():
    return datetime.now().strftime("%A")

def get_submission_time():
    return datetime.now().strftime("%I:%M %p")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_all_logs(sheet):
    records = sheet.get_all_records()
    if not records:
        return pd.DataFrame(columns=HEADERS)
    return pd.DataFrame(records)


# --------------------------------------------------
# DUPLICATE CHECK
# --------------------------------------------------

def already_submitted_today(df):
    """Check if today's date already has an entry for this user."""
    today = get_today_date()
    if df.empty or "Date" not in df.columns:
        return False
    return today in df["Date"].values


# --------------------------------------------------
# STREAK TRACKER
# --------------------------------------------------

def calculate_streak(df):
    if df.empty or "Date" not in df.columns:
        return 0

    logged_dates = set()
    for date_str in df["Date"]:
        try:
            date_obj = datetime.strptime(date_str, "%d %B %Y").date()
            logged_dates.add(date_obj)
        except Exception:
            pass

    if not logged_dates:
        return 0

    streak = 0
    check_date = datetime.now().date()
    while check_date in logged_dates:
        streak += 1
        check_date -= timedelta(days=1)
    return streak


# --------------------------------------------------
# MONTHLY STATS
# --------------------------------------------------

def get_monthly_stats(df):
    if df.empty or "Date" not in df.columns:
        return 0

    current_month = datetime.now().strftime("%B %Y")
    count = 0
    for date_str in df["Date"]:
        try:
            date_obj = datetime.strptime(date_str, "%d %B %Y")
            if date_obj.strftime("%B %Y") == current_month:
                count += 1
        except Exception:
            pass
    return count


# --------------------------------------------------
# POLISH MY EOD
# --------------------------------------------------

def polish_text(raw_text):
    if not raw_text.strip():
        return raw_text

    replacements = {
        r"\bworked on\b": "Made progress on",
        r"\bfixed a bug\b": "Resolved a bug",
        r"\bfixed bugs\b": "Resolved multiple bugs",
        r"\blooked into\b": "Investigated",
        r"\bchecked\b": "Reviewed",
        r"\btried to\b": "Attempted to",
        r"\bdid some\b": "Performed",
        r"\bwrote\b": "Authored",
        r"\bchanged\b": "Modified",
        r"\badded\b": "Implemented",
        r"\bfinished\b": "Completed",
        r"\bstarted\b": "Initiated",
        r"\blooked at\b": "Analyzed",
        r"\bwent through\b": "Reviewed",
        r"\bset up\b": "Configured",
        r"\bworked with\b": "Collaborated with",
        r"\btested\b": "Conducted testing on",
        r"\bhad a meeting\b": "Attended a meeting",
        r"\btalked about\b": "Discussed",
    }

    polished = raw_text.strip()
    for pattern, replacement in replacements.items():
        polished = re.sub(pattern, replacement, polished, flags=re.IGNORECASE)

    sentences = polished.split(". ")
    sentences = [s.strip().capitalize() for s in sentences if s.strip()]
    polished = ". ".join(sentences)

    if polished and not polished.endswith("."):
        polished += "."
    return polished


# --------------------------------------------------
# EXCEL EXPORT
# --------------------------------------------------

def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Work Logs")
    output.seek(0)
    return output.read()


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Logify - Daily Work Logger",
    page_icon="📋",
    layout="centered"
)

st.markdown("""
    <style>
        .block-container { max-width: 720px; padding-top: 2rem; }
        .streak-box {
            border-left: 4px solid #1a73e8;
            padding: 0.75rem 1rem;
            border-radius: 4px;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        .stat-box {
            border: 1px solid #1a73e8;
            padding: 0.75rem 1rem;
            border-radius: 6px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# MAIN APP
# --------------------------------------------------

def main():

    st.title("Logify")
    st.caption("Your smart daily work logging system.")
    st.markdown("---")

    # --------------------------------------------------
    # STEP 1 - Ask for user name
    # We store the name in session_state so the user
    # doesn't have to retype it every time they click a button.
    # --------------------------------------------------

    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    if not st.session_state.user_name:
        st.subheader("👋 Welcome to Logify!")
        st.write("Please enter your name to get started. Your logs will be saved privately just for you.")

        name_input = st.text_input("Your Name", placeholder="e.g. Preksha")

        if st.button("Continue", type="primary"):
            if not name_input.strip():
                st.warning("Please enter your name to continue.")
            else:
                st.session_state.user_name = name_input.strip().title()
                st.rerun()
        return  # Stop here until name is entered

    # --------------------------------------------------
    # STEP 2 - Connect to this user's personal Google Sheet
    # --------------------------------------------------

    user_name = st.session_state.user_name

    client = connect_to_google_sheets()
    sheet, user_name = get_user_sheet(client, user_name)
    df = load_all_logs(sheet)

    # Show greeting with user's name
    st.markdown(f"### Hello, {user_name}! 👋")

    # Small button to switch user
    if st.button("Not you? Switch user"):
        st.session_state.user_name = ""
        st.rerun()

    st.markdown("---")

    # --------------------------------------------------
    # STATS - Streak and monthly count
    # --------------------------------------------------

    streak = calculate_streak(df)
    monthly_count = get_monthly_stats(df)
    current_month = datetime.now().strftime("%B %Y")

    if streak > 0:
        st.markdown(
            f'<div class="streak-box">🔥 You are on a <strong>{streak}-day streak</strong>! Keep it up 🚀</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="streak-box">💡 No active streak. Submit today\'s log to start one!</div>',
            unsafe_allow_html=True
        )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="stat-box"><strong>{monthly_count}</strong><br/>Days logged in {current_month}</div>',
            unsafe_allow_html=True
        )
    with col2:
        total_logs = len(df)
        st.markdown(
            f'<div class="stat-box"><strong>{total_logs}</strong><br/>Total entries all time</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # --------------------------------------------------
    # LOG ENTRY FORM
    # --------------------------------------------------

    st.subheader("📝 Today's Log")

    today_date = get_today_date()
    today_day = get_today_day()

    col_date, col_day = st.columns(2)
    with col_date:
        st.text_input("📅 Date", value=today_date, disabled=True)
    with col_day:
        st.text_input("📆 Day", value=today_day, disabled=True)

    work_done = st.text_area(
        "📝 Work Done Today",
        placeholder=(
            "e.g. Completed the login module, fixed authentication bug, "
            "reviewed PR #42, attended team standup, updated documentation..."
        ),
        height=160,
        key="work_input"
    )

    # Polish button
    if st.button("✨ Polish My EOD"):
        if work_done.strip():
            polished = polish_text(work_done)
            st.info("✨ Polished version:\n\n" + polished)
            st.caption("Tip: Copy the polished text and paste it above before saving.")
        else:
            st.warning("Please write something first, then polish it.")

    st.markdown(" ")

    # Save button
    if st.button("💾 Save EOD Log", type="primary", use_container_width=True):
        if not work_done.strip():
            st.warning("Please describe what you did today before saving.")
        elif already_submitted_today(df):
            st.warning("EOD already submitted for today. See you tomorrow!")
        else:
            submission_time = get_submission_time()
            new_row = [today_date, today_day, work_done.strip(), submission_time]
            try:
                sheet.append_row(new_row)
                st.success(f"EOD saved successfully at {submission_time}!")
                st.balloons()
                df = load_all_logs(sheet)
            except Exception as e:
                st.error(f"Failed to save your log: {e}")

    st.markdown("---")

    # Recent logs
    st.subheader("🗂️ Recent Logs")

    if df.empty:
        st.info("No logs yet. Submit your first EOD above to get started!")
    else:
        recent = df.tail(5).iloc[::-1].reset_index(drop=True)
        st.dataframe(recent, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Export
    st.subheader("📥 Export Logs")

    if not df.empty:
        excel_data = convert_df_to_excel(df)
        filename = f"logify_{user_name}_{datetime.now().strftime('%Y_%m_%d')}.xlsx"
        st.download_button(
            label="Download All Logs as Excel",
            data=excel_data,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        st.caption(f"{len(df)} total entries will be included in the export.")
    else:
        st.info("Nothing to export yet. Add some logs first!")

    st.markdown("---")


if __name__ == "__main__":
    main()