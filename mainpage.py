import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from st_justgage import st_justgage  

# Set Streamlit app to use full width
st.set_page_config(layout="wide")

# Initialize session state for budget tracking
if 'income' not in st.session_state:
    st.session_state.income = 0
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'savings_goal' not in st.session_state:
    st.session_state.savings_goal = 0

# Function to add an expense
def add_expense(category, amount, date):
    st.session_state.expenses.append({'Category': category, 'Amount': amount, 'Date': date})

# Function to calculate total expenses
def calculate_total_expenses():
    return sum(expense['Amount'] for expense in st.session_state.expenses)

# Set up the Streamlit app
st.title("Enhanced Personal Finance Dashboard")

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
expense_date = st.sidebar.date_input("Date of expense")
if st.sidebar.button("Add Expense"):
    add_expense(expense_category, expense_amount, expense_date)

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

    # Create columns for the first set of charts with some spacing
    col1, col2 = st.columns([1, 1])  # Use equal column widths

    # Expenses by category pie chart (Left column)
    with col1:
        fig_pie = px.pie(expenses_df, names='Category', values='Amount', title='Expenses by Category')
        st.plotly_chart(fig_pie, use_container_width=True)  # Ensure full width in the column

    # Add spacing between charts
    st.write("")  # This will add some vertical space

    # Bar chart for expenses over time by category (Right column)
    with col2:
        fig_bar = px.bar(expenses_df, x='Date', y='Amount', color='Category', title='Expenses Over Time by Category')
        st.plotly_chart(fig_bar, use_container_width=True)  # Ensure full width in the column

    # Create a new row for more charts with spacing
    col3, col4 = st.columns([1, 1])  # Equal columns

    # Monthly summary analysis (Left column)
    with col3:
        expenses_by_category = expenses_df.groupby('Category').sum()['Amount'].reset_index()
        fig_category_bar = px.bar(expenses_by_category, x='Category', y='Amount', title='Total Expenses by Category')
        st.plotly_chart(fig_category_bar, use_container_width=True)

    # Add space between rows
    st.write("")  # Adds vertical space between charts

    # Line chart for cumulative savings over time (Right column)
    with col4:
        expenses_df['Cumulative Expenses'] = expenses_df['Amount'].cumsum()
        savings = st.session_state.income - expenses_df['Cumulative Expenses']
        fig_line = px.line(expenses_df, x='Date', y='Cumulative Expenses', title='Cumulative Expenses Over Time')
        st.plotly_chart(fig_line, use_container_width=True)

# Savings progress
st.subheader("Savings Progress")
if st.session_state.income > 0 and st.session_state.savings_goal > 0:
    savings_progress = (st.session_state.income - calculate_total_expenses()) / st.session_state.savings_goal * 100
    savings_progress = min(max(savings_progress, 0), 100)  # Ensure it's between 0 and 100
    
    # Create a new row with columns for savings gauge and budget vs actual
    col5, col6 = st.columns([1, 1])  # Equal columns

    # Use st_justgage to create a gauge chart (Left column)
    with col5:
        st_justgage(
            value=savings_progress, 
            min_value=0, 
            max_value=100, 
            title="Savings Progress", 
            symbol="%", 
            title_color="blue",
            gaugeWidthScale=0.5,
            levelColors=["#FF0000", "#FFFF00", "#00FF00"],  # Red to Green color gradient
        )

# Budget vs Actual
st.subheader("Budget vs Actual")
if st.session_state.expenses:
    budget = st.sidebar.number_input("Set your total budget:", min_value=0, step=100)
    actual_expenses = calculate_total_expenses()
    
    with col6:  # Use the right column for the bar chart
        fig_budget_vs_actual = go.Figure()

        fig_budget_vs_actual.add_trace(go.Bar(
            x=['Budget'],
            y=[budget],
            name='Budget',
            marker_color='blue'
        ))

        fig_budget_vs_actual.add_trace(go.Bar(
            x=['Actual'],
            y=[actual_expenses],
            name='Actual',
            marker_color='orange'
        ))

        fig_budget_vs_actual.update_layout(title='Budget vs Actual', barmode='group')
        st.plotly_chart(fig_budget_vs_actual, use_container_width=True)

# Generate a monthly financial report
if st.button("Generate Monthly Report"):
    st.subheader("Monthly Financial Report")
    st.write("### Income and Savings")
    st.write(f"Total Income: ${st.session_state.income}")
    st.write(f"Total Expenses: ${calculate_total_expenses()}")
    st.write(f"Savings Goal: ${st.session_state.savings_goal}")
    st.write(f"Remaining Savings: ${st.session_state.income - calculate_total_expenses()}")
    
    # Budget analysis
    if 'budget' in st.session_state:
        st.write(f"Budget: ${st.session_state.budget}")
        st.write(f"Over Budget by: ${actual_expenses - st.session_state.budget if actual_expenses > st.session_state.budget else 0}")
