import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime

st.title("Random Winner Selector with Exclusion & Logging")

# Step 1: Upload main CSV
uploaded_file = st.file_uploader("Upload your main CSV file", type=["csv"])

# Step 1.1: Optional exclusion list
exclusion_file = st.file_uploader("Upload exclusion list (Optional)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"Main file uploaded: {len(df)} rows, {len(df.columns)} columns.")
    st.dataframe(df.head())

    exclude_column = None
    excluded_values = set()

    # Handle exclusion file if provided
    if exclusion_file is not None:
        exclusion_df = pd.read_csv(exclusion_file)
        st.success(f"Exclusion file uploaded: {len(exclusion_df)} rows.")

        # Let user select column to match on
        common_cols = list(set(df.columns).intersection(set(exclusion_df.columns)))
        if common_cols:
            exclude_column = st.selectbox("Select column to match for exclusion", common_cols)
            excluded_values = set(exclusion_df[exclude_column].astype(str).unique())
            df = df[~df[exclude_column].astype(str).isin(excluded_values)]
            st.info(f"{len(excluded_values)} values will be excluded from column '{exclude_column}'.")
        else:
            st.warning("No matching columns found between main and exclusion file. No exclusion applied.")

    # Step 2: Choose number of winners
    max_rows = len(df)
    if max_rows == 0:
        st.error("No data left after exclusions!")
    else:
        num_rows = st.number_input(
            "How many random winners do you want to select?",
            min_value=1,
            max_value=max_rows,
            value=min(5, max_rows),
            step=1
        )

        if st.button("Generate Winners"):
            sampled_df = df.sample(n=num_rows, random_state=42).reset_index(drop=True)
            st.dataframe(sampled_df)

            # Step 3: Allow download
            csv = sampled_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Sampled Winners",
                data=csv,
                file_name='sampled_winners.csv',
                mime='text/csv',
            )

            # Step 4: Log to winner_logs.csv
            log_file = "winner_logs.csv"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sampled_df["timestamp"] = timestamp

            if os.path.exists(log_file):
                sampled_df.to_csv(log_file, mode='a', header=False, index=False)
            else:
                sampled_df.to_csv(log_file, index=False)

            st.success(f"Logged {num_rows} winners to {log_file}")
