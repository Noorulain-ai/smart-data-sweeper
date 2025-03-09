import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page Configuration
st.set_page_config(page_title="Data Sweeper Pro 🚀", layout="wide")

# Custom CSS for Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2C2F33;
        color: white;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
        padding: 8px 15px;
    }
    .stDownloadButton>button {
        background-color: #28a745;
        color: white;
        border-radius: 5px;
        padding: 8px 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🎯 Title & Description
st.title("📊 Data Sweeper Pro – Smart File Cleaner")
st.write("🚀 Transform, clean, and visualize your **CSV & Excel** files with ease!")

# 📂 File Uploader
uploaded_files = st.file_uploader(
    "📤 Upload your files (CSV or Excel):",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Load File
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")
        else:
            st.error(f"❌ Unsupported File Type: {file_ext}")
            continue

        # 📝 Data Preview
        st.subheader(f"📌 Preview of {file.name}")
        st.dataframe(df.head())

        # 🛠 Data Cleaning Options
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"🧹 Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button(f"🔄 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values have been filled!")

        # 📊 Data Visualization
        st.subheader(f"📊 Visualization for {file.name}")
        if st.checkbox(f"📉 Show charts for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # 🔄 File Conversion Options
        st.header(f"🔄 Convert {file.name}")
        conversion_type = st.radio(f"🔄 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"⬇️ Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine="openpyxl")
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")
