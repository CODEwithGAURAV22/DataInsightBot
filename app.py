import streamlit as st
import pandas as pd

from backend.gemini_service import generate_sql, explain_result
from backend.sql_validator import validate_sql
from backend.database_query import execute_query
from backend.ml_prediction import predict_future_sales


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DataInsightBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0f1117;
    }

    section[data-testid="stSidebar"] {
        background-color: #151821;
        border-right: 1px solid #292d38;
    }

    .logo {
        font-size: 27px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .tagline {
        color: #9ca3af;
        font-size: 13px;
        margin-bottom: 25px;
    }

    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .main-subtitle {
        color: #9ca3af;
        font-size: 16px;
        margin-bottom: 20px;
    }

    .status {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        background-color: #123c2b;
        color: #4ade80;
        font-size: 13px;
        margin-bottom: 20px;
    }

    .user-message {
        background-color: #252936;
        border-radius: 14px;
        padding: 15px 18px;
        margin: 15px 0 10px auto;
        max-width: 80%;
    }

    .bot-message {
        background-color: #181b24;
        border: 1px solid #292d38;
        border-radius: 14px;
        padding: 18px;
        margin: 10px 0 20px 0;
        max-width: 90%;
    }

    .message-label {
        font-size: 13px;
        color: #9ca3af;
        margin-bottom: 7px;
    }

    .message-text {
        font-size: 16px;
        line-height: 1.6;
        color: #f3f4f6;
    }

    .welcome-card {
        background-color: #181b24;
        border: 1px solid #292d38;
        border-radius: 16px;
        padding: 25px;
        margin-top: 25px;
    }

    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 12px;
        padding: 30px 0 10px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="logo">🤖 DataInsightBot</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tagline">AI Powered Business Analyst</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🧭 Navigation")

    page = st.radio(
        "Navigation",
        [
            "💬 AI Analyst",
            "📈 ML Prediction"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### 🕘 Recent Questions")

    if st.session_state.history:

        for item in reversed(st.session_state.history[-5:]):

            short_question = item

            if len(short_question) > 50:
                short_question = short_question[:50] + "..."

            st.caption("• " + short_question)

    else:

        st.caption("No questions asked yet.")

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.history = []

        st.rerun()


# ============================================================
# AI ANALYST PAGE
# ============================================================

if page == "💬 AI Analyst":

    st.markdown(
        '<div class="main-title">DataInsightBot</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Ask questions about your company data in natural language.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="status">● System Online</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # WELCOME
    # ========================================================

    if not st.session_state.messages:

        st.markdown(
            """
            <div class="welcome-card">

            <h3>👋 Welcome to DataInsightBot</h3>

            <p style="color:#9ca3af;">
            Ask questions about your company data and get
            instant business insights.
            </p>

            <p style="color:#9ca3af;">
            Try one of these:
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button(
                "💰 Highest average salary",
                use_container_width=True
            ):

                st.session_state.quick_question = (
                    "Which department has the highest average salary?"
                )

                st.rerun()

        with col2:

            if st.button(
                "🌎 Highest sales region",
                use_container_width=True
            ):

                st.session_state.quick_question = (
                    "Which region generated the highest sales?"
                )

                st.rerun()

        with col3:

            if st.button(
                "👥 Employees by department",
                use_container_width=True
            ):

                st.session_state.quick_question = (
                    "How many employees are in each department?"
                )

                st.rerun()


    # ========================================================
    # CHAT HISTORY
    # ========================================================

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(
                f"""
                <div class="user-message">

                <div class="message-label">
                👤 You
                </div>

                <div class="message-text">
                {message["content"]}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="bot-message">

                <div class="message-label">
                🤖 DataInsightBot
                </div>

                <div class="message-text">
                {message["content"]}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            # SQL
            if "sql" in message:

                with st.expander("🔍 View Generated SQL"):

                    st.code(
                        message["sql"],
                        language="sql"
                    )


            # DATABASE RESULT
            if "data" in message:

                st.markdown("##### 🗄️ Database Result")

                result_df = message["data"]

                st.dataframe(
                    result_df,
                    use_container_width=True,
                    hide_index=True
                )


            # AUTOMATIC VISUALIZATION
            if "data" in message:

                result_df = message["data"]

                if (
                    not result_df.empty
                    and len(result_df.columns) >= 2
                ):

                    numeric_columns = (
                        result_df
                        .select_dtypes(
                            include="number"
                        )
                        .columns
                        .tolist()
                    )

                    if numeric_columns:

                        st.markdown(
                            "##### 📊 Visualization"
                        )

                        x_column = result_df.columns[0]

                        y_column = numeric_columns[0]

                        chart_data = result_df[
                            [x_column, y_column]
                        ].copy()

                        chart_data = chart_data.set_index(
                            x_column
                        )

                        st.bar_chart(
                            chart_data
                        )


    # ========================================================
    # CHAT INPUT
    # ========================================================

    quick_question = st.session_state.get(
        "quick_question",
        ""
    )

    question = st.chat_input(
        "Ask a question about your company data..."
    )

    if quick_question:

        question = quick_question

        del st.session_state.quick_question


    # ========================================================
    # PROCESS QUESTION
    # ========================================================

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        st.session_state.history.append(
            question
        )

        with st.spinner(
            "🤖 Analyzing your question..."
        ):

            try:

                # Generate SQL
                sql = generate_sql(question)

                # Validate SQL
                is_valid, message = validate_sql(sql)

                if not is_valid:

                    st.error(
                        f"SQL validation failed: {message}"
                    )

                    st.stop()

                # Execute SQL
                result = execute_query(sql)

                if "error" in result:

                    st.error(
                        f"Database error: {result['error']}"
                    )

                    st.stop()

                columns = result["columns"]

                rows = result["rows"]

                # Create DataFrame
                df = pd.DataFrame(
                    rows,
                    columns=columns
                )

                # Generate explanation
                explanation = explain_result(
                    question,
                    sql,
                    columns,
                    rows
                )

                # Save response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": explanation,
                        "sql": sql,
                        "data": df
                    }
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"Something went wrong: {error}"
                )


# ============================================================
# ML PREDICTION PAGE
# ============================================================

elif page == "📈 ML Prediction":

    st.markdown(
        '<div class="main-title">📈 ML Prediction</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Predict future revenue using machine learning.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="status">● ML Model Ready</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # PREDICTION SETTINGS
    # ========================================================

    st.markdown("### 🔮 Prediction Settings")

    prediction_days = st.selectbox(
        "How many future days do you want to predict?",
        [7, 14, 30],
        index=2
    )


    # ========================================================
    # PREDICT BUTTON
    # ========================================================

    if st.button(
        "🚀 Generate Prediction",
        use_container_width=True
    ):

        with st.spinner(
            "Training model and generating predictions..."
        ):

            try:

                predictions = predict_future_sales(
                    days=prediction_days
                )

                # ==========================================
                # SUCCESS
                # ==========================================

                st.success(
                    "Prediction generated successfully!"
                )


                # ==========================================
                # TOTAL PREDICTED REVENUE
                # ==========================================

                total_prediction = (
                    predictions["predicted_revenue"]
                    .sum()
                )

                average_prediction = (
                    predictions["predicted_revenue"]
                    .mean()
                )


                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "💰 Total Predicted Revenue",
                        f"{total_prediction:,.2f}"
                    )

                with col2:

                    st.metric(
                        "📊 Average Daily Revenue",
                        f"{average_prediction:,.2f}"
                    )


                # ==========================================
                # PREDICTION CHART
                # ==========================================

                st.markdown(
                    "### 📈 Revenue Forecast"
                )

                chart_data = predictions.copy()

                chart_data["sale_date"] = pd.to_datetime(
                    chart_data["sale_date"]
                )

                chart_data = chart_data.set_index(
                    "sale_date"
                )

                st.line_chart(
                    chart_data[
                        "predicted_revenue"
                    ]
                )


                # ==========================================
                # PREDICTION TABLE
                # ==========================================

                st.markdown(
                    "### 🗓️ Prediction Details"
                )

                display_df = predictions.copy()

                display_df["sale_date"] = (
                    display_df["sale_date"]
                    .dt.strftime("%Y-%m-%d")
                )

                display_df["predicted_revenue"] = (
                    display_df["predicted_revenue"]
                    .round(2)
                )

                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )


                # ==========================================
                # BUSINESS INSIGHT
                # ==========================================

                st.markdown(
                    "### 💡 Business Insight"
                )

                highest_prediction = (
                    predictions[
                        "predicted_revenue"
                    ].max()
                )

                lowest_prediction = (
                    predictions[
                        "predicted_revenue"
                    ].min()
                )

                st.info(
                    f"Based on the ML model, predicted daily "
                    f"revenue ranges from "
                    f"{lowest_prediction:,.2f} to "
                    f"{highest_prediction:,.2f} "
                    f"over the next {prediction_days} days."
                )


            except Exception as error:

                st.error(
                    f"Prediction error: {error}"
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    'DataInsightBot • AI Powered Business Analyst'
    '</div>',
    unsafe_allow_html=True
)