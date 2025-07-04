import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# File to store data
DATA_FILE = "data.csv"

# Initialize the data file
def init_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Description"])
        df.to_csv(DATA_FILE, index=False)

# Load data
def load_data():
    return pd.read_csv(DATA_FILE)

# Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Add new transaction
def add_transaction(date, t_type, category, amount, description):
    new_entry = pd.DataFrame([[date, t_type, category, amount, description]],
                             columns=["Date", "Type", "Category", "Amount", "Description"])
    df = load_data()
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)

# Summary statistics
def calculate_summary(df):
    income = df[df['Type'] == 'Income']['Amount'].sum()
    expense = df[df['Type'] == 'Expense']['Amount'].sum()
    balance = income - expense
    return income, expense, balance

# Visualization
def plot_summary(df):
    summary = df.groupby('Type')['Amount'].sum()
    fig, ax = plt.subplots()
    ax.pie(summary, labels=summary.index, autopct='%1.1f%%', startangle=90, colors=['red', 'green'])
    ax.axis('equal')
    return fig

# Main App
def main():
    st.set_page_config(page_title="💰 Personal Finance Tracker", layout="centered")
    st.title("💰 Personal Finance Tracker")

    init_data_file()
    df = load_data()

    # --- Form to Add Transaction ---
    with st.form("Add Transaction"):
        st.subheader("Add New Transaction")
        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("Date")
            t_type = st.selectbox("Type", ["Income", "Expense"])
        with col2:
            category = st.text_input("Category")
            amount = st.number_input("Amount", min_value=0.01, step=0.01)

        # ✅ Fixed: Set height to minimum allowed (68)
        description = st.text_area("Description", height=100)

        submitted = st.form_submit_button("Add")
        if submitted:
            add_transaction(str(date), t_type, category, amount, description)
            st.success("Transaction added successfully!")

    st.divider()

    # --- Summary ---
    st.subheader("💡 Summary")
    df = load_data()  # Reload in case new data was added
    income, expense, balance = calculate_summary(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹ {income:.2f}")
    col2.metric("Total Expense", f"₹ {expense:.2f}")
    col3.metric("Balance", f"₹ {balance:.2f}")

    # --- Visualization ---
    if not df.empty:
        st.subheader("📊 Income vs Expense")
        fig = plot_summary(df)
        st.pyplot(fig)

    # --- Transaction History ---
    st.subheader("📋 Transaction History")
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
