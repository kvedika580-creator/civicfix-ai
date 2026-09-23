import streamlit as st
import uuid
import pandas as pd

from database import (
    initialize_database,
    create_ticket,
    get_all_complaints
)

from ai_engine import analyze_complaint


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CivicFix AI",
    page_icon="🏙️",
    layout="wide"
)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #F7F9FC;
}

.civic-title {
    font-size: 46px;
    font-weight: 800;
    margin-bottom: 0;
}

.civic-subtitle {
    font-size: 18px;
    color: #667085;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 14px;
    background-color: white;
    border: 1px solid #E4E7EC;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏙️ CivicFix AI")

st.sidebar.caption(
    "AI-powered civic issue reporting system"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Report Issue",
        "Dashboard"
    ]
)


# ============================================================
# REPORT ISSUE
# ============================================================

if page == "Report Issue":

    st.markdown(
        '<div class="civic-title">CivicFix AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="civic-subtitle">'
        'Report civic problems. Let AI structure the solution.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("📍 Report a Civic Issue")

    name = st.text_input(
        "Your Name",
        placeholder="Enter your name"
    )

    location = st.text_input(
        "Location",
        placeholder="Example: Near ABC College, Pune"
    )

    issue = st.text_area(
        "Describe the problem",
        placeholder=(
            "Example: There is a large pothole near my college "
            "entrance and bikes are struggling to pass through it."
        ),
        height=160
    )

    st.caption(
        "Tip: Include what happened, where it happened and "
        "how it is affecting people."
    )

    submit = st.button(
        "🤖 Analyse with CivicFix AI",
        type="primary",
        use_container_width=True
    )

    if submit:

        if not name.strip():
            st.warning("Please enter your name.")

        elif not location.strip():
            st.warning("Please enter the location.")

        elif not issue.strip():
            st.warning("Please describe the civic problem.")

        else:

            with st.spinner(
                "CivicFix AI is analysing the complaint..."
            ):

                try:

                    result = analyze_complaint(
                        issue,
                        location
                    )

                    ticket_id = (
                        "CF-"
                        + str(uuid.uuid4())[:8].upper()
                    )

                    data = {
                        "ticket_id": ticket_id,
                        "name": name,
                        "issue": issue,
                        "category": result["category"],
                        "severity": result["severity"],
                        "summary": result["summary"],
                        "department": result["department"],
                        "complaint": result["complaint"],
                        "location": location
                    }

                    create_ticket(data)

                except Exception as error:

                    st.error(
                        f"Unable to analyse the complaint: {error}"
                    )

                else:

                    st.success(
                        f"Complaint created successfully — {ticket_id}"
                    )

                    st.divider()

                    # ------------------------------------------------
                    # AI ANALYSIS
                    # ------------------------------------------------

                    st.subheader("🔎 AI Analysis")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Issue Category",
                            result["category"]
                        )

                    with col2:
                        st.metric(
                            "Severity",
                            result["severity"]
                        )

                    with col3:
                        st.metric(
                            "Suggested Department",
                            result["department"]
                        )

                    # ------------------------------------------------
                    # SUMMARY
                    # ------------------------------------------------

                    st.subheader("📝 AI Summary")

                    st.info(
                        result["summary"]
                    )

                    # ------------------------------------------------
                    # GENERATED COMPLAINT
                    # ------------------------------------------------

                    st.subheader("📨 Generated Complaint")

                    st.text_area(
                        "Ready-to-submit complaint",
                        value=result["complaint"],
                        height=200
                    )

                    # ------------------------------------------------
                    # MISSING INFORMATION
                    # ------------------------------------------------

                    st.subheader("⚠️ Evidence & Information Check")

                    missing = result.get(
                        "missing_information",
                        []
                    )

                    if missing:

                        for item in missing:
                            st.warning(
                                f"• {item}"
                            )

                    else:

                        st.success(
                            "No major missing information detected."
                        )

                    # ------------------------------------------------
                    # TICKET
                    # ------------------------------------------------

                    st.divider()

                    st.subheader("🎫 Complaint Ticket")

                    ticket_col1, ticket_col2 = st.columns(2)

                    with ticket_col1:

                        st.write(
                            f"**Ticket ID:** `{ticket_id}`"
                        )

                        st.write(
                            "**Status:** Submitted"
                        )

                    with ticket_col2:

                        st.write(
                            f"**Location:** {location}"
                        )

                        st.write(
                            f"**Department:** "
                            f"{result['department']}"
                        )


# ============================================================
# DASHBOARD
# ============================================================

elif page == "Dashboard":

    st.title("📊 CivicFix Dashboard")

    st.caption(
        "Overview of reported civic issues"
    )

    rows, columns = get_all_complaints()

    if not rows:

        st.info(
            "No civic complaints have been submitted yet."
        )

    else:

        df = pd.DataFrame(
            rows,
            columns=columns
        )

        # ------------------------------------------------
        # DASHBOARD METRICS
        # ------------------------------------------------

        total_complaints = len(df)

        high_priority = len(
            df[
                df["severity"].isin(
                    ["High", "Critical"]
                )
            ]
        )

        submitted = len(
            df[
                df["status"] == "Submitted"
            ]
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Complaints",
                total_complaints
            )

        with col2:
            st.metric(
                "High Priority",
                high_priority
            )

        with col3:
            st.metric(
                "Submitted",
                submitted
            )

        st.divider()

        # ------------------------------------------------
        # TABLE
        # ------------------------------------------------

        st.subheader("📋 Recent Reports")

        display_df = df[
            [
                "ticket_id",
                "category",
                "severity",
                "department",
                "location",
                "status",
                "created_at"
            ]
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # ------------------------------------------------
        # CATEGORY CHART
        # ------------------------------------------------

        st.subheader("📈 Civic Issues by Category")

        category_counts = (
            df["category"]
            .value_counts()
        )

        st.bar_chart(
            category_counts
        )