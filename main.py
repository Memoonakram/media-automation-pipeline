import streamlit as st
import pandas as pd

# Set the page layout to centered structure
st.set_page_config(page_title="AI Data Rendering Pipeline", layout="centered")
st.title("🤖 Production-Grade Content Pipeline")
st.caption("Automated Visual Layout Engine — Data Science Skills Training")

# Google Sheet URL (Apna converted URL yahan paste karein)
CSV_URL = CSV_URL = "https://docs.google.com/spreadsheets/d/1VOeZj-w_nIXVEWMIImuyHWQCHvvTXmiIhkJAizraWVY/export?format=csv"


@st.cache_data(ttl=60)
def fetch_and_clean_matrix(url):
    matrix_df = pd.read_csv(url)
    matrix_df.columns = matrix_df.columns.str.strip()
    return matrix_df


try:
    df = fetch_and_clean_matrix(CSV_URL)

    st.subheader("📁 Structured Prompting Context (JSON Matrix Output)")
    json_preview = df.to_json(orient="records", indent=4)
    st.code(json_preview, language="json")

    st.markdown("---")

    st.subheader("🎯 Automated Visual Layouts")

    for index, row in df.iterrows():
        with st.container():
            st.markdown(
                f"""
                            <div style="
                                background-color: #1E293B; 
                                padding: 24px; 
                                border-radius: 12px; 
                                margin-bottom: 20px; 
                                border-left: 6px solid #0EA5E9;
                            ">
                                <h4 style="color: #38BDF8; font-family: 'Inter', sans-serif; margin-top: 0; font-size: 18px; font-weight: 700;">
                                    🪝 Hook Structure {index + 1}: {row['#Psychological_Hook']}
                                </h4>
                                <p style="color: #E2E8F0; font-family: 'Inter', sans-serif; font-size: 15px; line-height: 1.6; margin-bottom: 0;">
                                    📖 Story Block: {row['#Body_Story']}
                                </p>
                            </div>
                            """,
                unsafe_allow_html=True  # <-- Sirf is line ko sahi karna hai
            )
except Exception as pipeline_error:
    st.error(f"Critical Ingestion Pipeline Error: {pipeline_error}")


