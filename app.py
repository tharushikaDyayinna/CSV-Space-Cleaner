import streamlit as st
import pandas as pd
import io
import zipfile

st.title("Upload CSV or XLSX, Get Cleaned CSV")

uploaded_files = st.file_uploader("Select your files", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for uploaded_file in uploaded_files:
            try:
                # Load file depending on extension
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                # Strip text columns
                text_cols = df.select_dtypes(include="object").columns
                df[text_cols] = df[text_cols].apply(lambda s: s.str.strip())

                # Save
                cleaned_csv = io.StringIO()
                df.to_csv(cleaned_csv, index=False)

                # Add to ZIP
                zip_file.writestr(f"{uploaded_file.name.split('.')[0]}_cleaned.csv", cleaned_csv.getvalue())

            except Exception as e:
                st.error(f"Error with {uploaded_file.name}: {e}")

    st.download_button("📦 Download Cleaned ZIP", data=zip_buffer.getvalue(), file_name="cleaned_files.zip", mime="application/zip")
