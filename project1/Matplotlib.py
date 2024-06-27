import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import Functions
from io import BytesIO

def basic_plans(category):
    labels, sizes = Functions.get_plan_category(category)

    if category == 1:
        mycolors = ["#f9af8c", "#b19cbd", "#a0aed9", "#c98689", "#a19f93", "#efccc9", "#999098", "#4a1a42"]
    elif category == 2:
        mycolors = ["#ffd380", "#ffa600", "#ff8531", "#ff6361", "#bc5090", "#8a508f", "#893f71", "#660e60"]
    elif category == 3:
        mycolors = ["#ffadad", "#ffd6a5", "#fdffb6", "#caffbf", "#9bf6ff", "#a0c4ff", "#bdb2ff", "#ffc6ff"]
    elif category == 4:
        mycolors = ["#ef959c", "#dbc7be", "#cbb3bf", "#95adb6", "#8da1b9", "#a0aed9", "#efccc9", "#f9af8c"]
    else:
        raise ValueError("Invalid category value")

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=['']*len(sizes), colors=mycolors, autopct='%1.0f%%', pctdistance=1.1, labeldistance=.6)
    plt.legend(labels, title="Sections:", bbox_to_anchor=(0.03, 1.1))
    plt.title("Plan {}".format(category))
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf


def month_expenses(user_chat_id):
    labels, sizes = Functions.get_spendings(user_chat_id)
    mycolors = ["#ffadad", "#ffd6a5", "#fdffb6", "#caffbf", "#9bf6ff", "#a0c4ff", "#bdb2ff", "#ffc6ff"]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=['']*len(sizes), colors=mycolors, autopct='%1.0f%%', pctdistance=1.1, labeldistance=.6)
    plt.legend(labels, title="Sections:", bbox_to_anchor=(0.03, 1.1))
    plt.title("Spendings")
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf

def get_daily_spend(user_chat_id):
    days, spending = Functions.get_daily_spending(user_chat_id)
    plt.figure(figsize=(10, 5))
    ax = plt.axes(facecolor='#feeafa')

    plt.plot(days, spending, marker='o', linestyle='-', color='#70075d')
    plt.title('Daily Spending Throughout the Month in PLN')
    plt.xlabel('Day of the Month')
    plt.ylabel('Spending (PLN)')
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf

def income_day(user_chat_id):
    days, earnings=Functions.get_daily_income(user_chat_id)
    plt.figure(figsize=(10, 5), facecolor='#edf2fb')
    ax = plt.axes(facecolor='#d7e3fc')

    plt.plot(days, earnings, marker='o', linestyle='-', color='#363946')
    plt.title('Daily Earnings Throughout the Month')
    plt.xlabel('Day of the Month')
    plt.ylabel('Earnings (PLN)')
    plt.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf


def planned_actual(user_chat_id):
    categories, actual_expenses = Functions.get_spendings(user_chat_id)
    planned_expenses = Functions.average_percentage(user_chat_id)

    planned_color = '#cfbaf0'
    actual_color = '#fafabd'

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(facecolor='#fefef2')

    rects1 = ax.bar(x - width/2, planned_expenses, width, label='Planned', color=planned_color)
    rects2 = ax.bar(x + width/2, actual_expenses, width, label='Actual', color=actual_color)

    ax.set_ylabel('Amount (PLN)')
    ax.set_title('Expenses by Category')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10, rotation=40, ha='right')
    ax.legend()

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8)

    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf




basic_plans(3)
month_expenses(2)
get_daily_spend(2)
income_day(2)
planned_actual(2)