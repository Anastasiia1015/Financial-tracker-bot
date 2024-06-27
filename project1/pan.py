import pandas as pd
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project1.settings')
django.setup()

from Database.models import Income, Expense
from django.db.models import Sum
from django.db.models.functions import TruncMonth


def calculate_total_monthly_income(user_chat_id):
    try:
        incomes = Income.objects.filter(user__chat_id=user_chat_id).annotate(month=TruncMonth('date_time')).values('month').annotate(total_income=Sum('amount'))
        income_df = pd.DataFrame(incomes)
        return income_df
    except Exception as e:
        print(f"Error occurred while calculating total monthly income: {e}")
        return None


def calculate_total_monthly_expenses(user_chat_id):
    try:
        expenses = Expense.objects.filter(user__chat_id=user_chat_id).annotate(month=TruncMonth('date')).values('month').annotate(total_expenses=Sum('amount'))
        expense_df = pd.DataFrame(expenses)
        return expense_df
    except Exception as e:
        print(f"Error occurred while calculating total monthly expenses: {e}")
        return None


def calculate_savings(user_chat_id):
    try:
        total_income_df = calculate_total_monthly_income(user_chat_id)
        total_expenses_df = calculate_total_monthly_expenses(user_chat_id)
        if total_income_df is not None and total_expenses_df is not None:
            merged_df = pd.merge(total_income_df, total_expenses_df, on='month', how='outer').fillna(0)
            merged_df['savings'] = merged_df['total_income'] - merged_df['total_expenses']
            return merged_df
        else:
            return None
    except Exception as e:
        print(f"Error occurred while calculating savings: {e}")
        return None


def get_monthly_savings_summary(user_chat_id):
    try:
        savings_df = calculate_savings(user_chat_id)
        if savings_df is not None:
            summary = ""
            for index, row in savings_df.iterrows():
                month = row['month'].strftime('%B %Y')
                total_income = row['total_income']
                total_expenses = row['total_expenses']
                savings = row['savings']

                summary += f"Month: {month}\n"
                summary += f"Total Income: {total_income}\n"
                summary += f"Total Expenses: {total_expenses}\n"
                summary += f"Savings: {savings}\n\n"
            return summary
        else:
            return "Error: Unable to retrieve savings data."
    except Exception as e:
        print(f"Error occurred while generating savings summary: {e}")
        return None
