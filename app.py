# ASSIGNMENT
# SURVIVAL ANALYTICS - STREAMLIT CODE
# RESHMA SEN N

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

# Streamlit UI
st.title("Kaplan-Meier Survival Analysis")

# File Uploader
uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Handling column defaults safely
    default_time = "survival_time_hr" if "survival_time_hr" in df.columns else df.columns[0]
    default_event = "alive" if "alive" in df.columns else df.columns[1]

    # Ensure columns exist before selecting them
    time_col = st.sidebar.selectbox("Select Time Column", df.columns, 
                                    index=df.columns.get_loc(default_time) if default_time in df.columns else 0)
    event_col = st.sidebar.selectbox("Select Event Column", df.columns, 
                                     index=df.columns.get_loc(default_event) if default_event in df.columns else 1)

    if st.sidebar.button("Plot Survival Curve"):
        df_filtered = df[[time_col, event_col]].dropna()

        # Convert event column to binary (0 or 1)
        df_filtered = df_filtered.copy()
        df_filtered["event_numeric"] = pd.to_numeric(df_filtered[event_col], errors="coerce").fillna(0).astype(int)

        if not df_filtered["event_numeric"].isin([0, 1]).all():
            st.sidebar.warning("⚠️ Warning: The event column should contain only 0s and 1s.")

        try:
            # Fit the Kaplan-Meier model
            kmf = KaplanMeierFitter()
            kmf.fit(df_filtered[time_col], event_observed=df_filtered["event_numeric"]) 

            # Plot the survival function
            fig, ax = plt.subplots()
            kmf.plot(ax=ax, ci_show=True, color="blue")
            plt.grid(True, linestyle="--", alpha=0.6)
            plt.title("Kaplan-Meier Survival Curve", fontsize=14)
            plt.xlabel("Time (Hours)", fontsize=12)
            plt.ylabel("Survival Probability", fontsize=12)
            st.pyplot(fig)

        except Exception as e:
            st.sidebar.error(f"❌ Error: {str(e)}")

else:
    st.warning("📂 Please upload an Excel file to proceed.")

st.sidebar.write("Developed with ❤️ using Streamlit")
