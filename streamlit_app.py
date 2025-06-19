import streamlit as st
import pandas as pd
import io
import random

st.title("Random Winner Selector")

# Step 1: Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"Uploaded CSV with {len(df)} rows and {len(df.columns)} columns.")

    st.dataframe(df.head())

    # Step 2: Select number of random rows
    max_rows = len(df)
    num_rows = st.number_input(
        f"How many random winners do you want to select?",
        min_value=1,
        max_value=max_rows,
        value=min(5, max_rows),
        step=1
    )

    if st.button("Generate Winners"):
        sampled_df = df.sample(n=num_rows, random_state=42).reset_index(drop=True)
        st.dataframe(sampled_df)

        # Step 3: Download button for sampled data
        csv = sampled_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Sampled CSV",
            data=csv,
            file_name='sampled_rows.csv',
            mime='text/csv',
        )
