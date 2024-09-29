import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize session state for budget tracking
if 'income' not in st.session_state:
    st.session_state.income = 0
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'savings_goal' not in st.session_state:
    st.session_state.savings_goal = 0

# Function to add an expense
def add_expense(category, amount):
    st.session_state.expenses.append({'Category': category, 'Amount': amount})

# Function to calculate total expenses
def calculate_total_expenses():
    return sum(expense['Amount'] for expense in st.session_state.expenses)

# Set up the Streamlit app
st.title("Personal Finance Dashboard")

# Input for income
st.sidebar.header("Income")
st.session_state.income = st.sidebar.number_input("Enter your total income:", min_value=0, step=100)

# Input for savings goal
st.sidebar.header("Savings Goal")
st.session_state.savings_goal = st.sidebar.number_input("Enter your savings goal:", min_value=0, step=100)

# Input for expenses
st.sidebar.header("Add Expense")
expense_category = st.sidebar.selectbox("Select expense category:", ["Food", "Rent", "Utilities", "Entertainment", "Other"])
expense_amount = st.sidebar.number_input("Enter expense amount:", min_value=0, step=10)
if st.sidebar.button("Add Expense"):
    add_expense(expense_category, expense_amount)

# Display total income, expenses, and savings goal
st.subheader("Overview")
st.write(f"Total Income: ${st.session_state.income}")
st.write(f"Total Expenses: ${calculate_total_expenses()}")
st.write(f"Savings Goal: ${st.session_state.savings_goal}")

# Display expenses as a DataFrame
if st.session_state.expenses:
    expenses_df = pd.DataFrame(st.session_state.expenses)
    st.subheader("Expenses Breakdown")
    st.dataframe(expenses_df)

    # Plotting expenses
    fig = px.pie(expenses_df, names='Category', values='Amount', title='Expenses by Category')
    st.plotly_chart(fig)

# Calculate and display savings
savings = st.session_state.income - calculate_total_expenses()
st.subheader("Savings")
st.write(f"Total Savings: ${savings}")

# Provide a monthly report
if st.button("Generate Monthly Report"):
    st.subheader("Monthly Report")
    st.write("Summary of your financial data for this month:")
    st.write(f"Total Income: ${st.session_state.income}")
    st.write(f"Total Expenses: ${calculate_total_expenses()}")
    st.write(f"Savings Goal: ${st.session_state.savings_goal}")
    st.write(f"Remaining Savings: ${savings}")

