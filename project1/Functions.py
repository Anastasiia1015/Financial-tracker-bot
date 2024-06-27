import os
import django
import pandas as pd
from datetime import datetime
from calendar import monthrange
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project1.settings')
django.setup()
from django.utils import timezone
from Database.models import Income, User, Category, Expense, Sums, PlanCategory, Plan


def add_income(user_chat_id, money):
    try:
        user = User.objects.get(chat_id=user_chat_id)
    except User.DoesNotExist:
        print(f"User with chat ID {user_chat_id} does not exist.")
        return
    else:
        income_amount = money
        income_date = timezone.now().date()
        income = Income.objects.create(user=user, amount=income_amount, date_time=income_date)
        update_balance(user_chat_id, money)
        print(f"Income of {income_amount} added for user {user_chat_id}.")


def add_user(user_chat_id, user_balance, user_plan):
    try:
        user = User.objects.get(chat_id=user_chat_id)
        print(f"User with chat ID {user_chat_id} already exists.")
        return user, False
    except User.DoesNotExist:
        user = User.objects.create(chat_id=user_chat_id, balance=user_balance, plan_id=user_plan)
        print(f"User with chat ID {user_chat_id} created successfully.")
        create_all_sums(user_chat_id)
        return user, True
    except Exception as e:
        print(f"Error occurred while adding user: {e}")
        return None


def get_category_name(category_id):
    try:
        category = Category.objects.get(pk=category_id)
        return category.name
    except Category.DoesNotExist:
        print(f"Category with ID {category_id} does not exist.")
        return None
    except Exception as e:
        print(f"Error occurred while retrieving category: {e}")
        return None


def add_expense(user_chat_id, money, user_category_id):
    try:
        user = User.objects.get(chat_id=user_chat_id)
    except User.DoesNotExist:
        print(f"User with chat ID {user_chat_id} does not exist.")
        return
    else:
        expense_amount = money
        expense_date = timezone.now().date()
        expense = Expense.objects.create(user=user, amount=expense_amount, date=expense_date,
                                       category_id=user_category_id)
        category = get_category_name(user_category_id)
        update_balance(user_chat_id, -money)
        update_sums(user_chat_id, money, user_category_id)
        print(f"Expense of {expense_amount} on {category} added for user {user_chat_id}.")


def update_balance(user_chat_id, amount):
    try:
        user = User.objects.get(chat_id=user_chat_id)
        user.balance += amount
        user.save()
        print(f"Balance updated successfully for user with chat ID {user_chat_id}.")
        return user.balance
    except User.DoesNotExist:
        print(f"User with chat ID {user_chat_id} does not exist.")
        return None


def update_sums(user_chat_id, amount, user_category_id):
    try:
        user = User.objects.get(chat_id=user_chat_id)
        user_id = user.id
        sums = Sums.objects.get(user_id=user_id, category_id=user_category_id)
        sums.sum_of_expenses += amount
        sums.save()
        print(f"Balance updated successfully for user with chat ID {user_chat_id}.")
        return sums.sum_of_expenses
    except Sums.DoesNotExist:
        print(f"Sum of user with chat ID {user_chat_id} does not exist.")
        return None


def create_all_sums(user_chat_id):
    try:
        user = User.objects.get(chat_id=user_chat_id)
        user_id = user.id
        try:
            sums = Sums.objects.get(user_id=user_id, category_id=1)
        except Sums.DoesNotExist:
            user_plan = user.plan_id
            chat_ids = Category.objects.values_list('id', flat=True)
            if user_plan == 1:
                for category_id in chat_ids:
                    if category_id == 5:
                        pass
                    else:
                        Sums.objects.create(sum_of_expenses=0, category_id=category_id, user_id=user_id)
                        print("Sums created successfully.")
            elif user_plan == 2:
                for category_id in chat_ids:
                    if category_id == 3:
                        pass
                    else:
                        Sums.objects.create(sum_of_expenses=0, category_id=category_id, user_id=user_id)
                        print("Sums created successfully.")
            elif user_plan == 3:
                for category_id in chat_ids:
                    Sums.objects.create(sum_of_expenses=0, category_id=category_id, user_id=user_id)
                    print("Sums created successfully.")
            elif user_plan == 4:
                for category_id in chat_ids:
                    if category_id == 6:
                        pass
                    else:
                        Sums.objects.create(sum_of_expenses=0, category_id=category_id, user_id=user_id)
                        print("Sums created successfully.")
    except User.DoesNotExist:
        print(f"User with chat ID {user_chat_id} does not exist.")
    except Exception as e:
        print(f"Error occurred while creating sums: {e}")


def get_balance(user_chat_id):
    try:
        bal=User.objects.get(chat_id=user_chat_id)
        bal=bal.balance
        return bal
    except User.DoesNotExist:
        return None


def get_user_plan_id(user_chat_id):
    try:
        user = User.objects.get(chat_id=user_chat_id)
        plan_id = user.plan_id
        return plan_id
    except User.DoesNotExist:
        print(f"User with chat ID {user_chat_id} does not exist.")
        return None


def get_plan_name(plan_id):
    try:
        plan=Plan.objects.get(id=plan_id)
        name=plan.name
        return name
    except Plan.DoesNotExist:
        print(f"Plan with ID {plan_id} does not exist.")
        return None


def get_plan_category(plan_id):
    try:
        plan_categories = PlanCategory.objects.filter(plan_id=plan_id).order_by('category_id').select_related(
            'category')
        # Create a DataFrame from the queryset
        df = pd.DataFrame(list(plan_categories.values('category__name', 'percentage')))
        df['percentage'] = df['percentage'].astype(float)
        data_1 = df['category__name'].tolist()
        data_2 = df['percentage'].tolist()
        return data_1, data_2
    except PlanCategory.DoesNotExist:
        print(f"Plan with ID {plan_id} does not exist.")
        return None, None


def get_category_ids(plan_id):
    try:
        plan_categories = PlanCategory.objects.filter(plan_id=plan_id)
        df = pd.DataFrame(list(plan_categories.values('category__name', 'category_id')))
        category_ids = df.set_index('category__name').to_dict()['category_id']
        return category_ids
    except Plan.DoesNotExist:
        print(f"Plan with ID {plan_id} does not exist.")
        return None


def average_percentage(user_chat_id):
    try:
        user = User.objects.get(chat_id=user_chat_id)
        user_sums = Sums.objects.filter(user=user)
        total_expenses = float(sum(sum_obj.sum_of_expenses for sum_obj in user_sums))
        plan_id = user.plan_id
        categories, percentages = get_plan_category(plan_id)
        result = []
        for percentage in percentages:
            result.append(round(total_expenses*percentage))
        return result
    except PlanCategory.DoesNotExist:
        print(f"Plan with ID {plan_id} does not exist.")
        return None


def get_daily_spending(user_chat_id):
    try:
        user = User.objects.get(chat_id=user_chat_id)
        current_date = datetime.now().date()
        num_days_in_month = monthrange(current_date.year, current_date.month)[1]
        days_of_month = list(range(1, num_days_in_month + 1))
        total_spending_per_day = []
        for day in days_of_month:
            expenses_on_day = Expense.objects.filter(user=user,
                                                     date__year=current_date.year,
                                                     date__month=current_date.month,
                                                     date__day=day)
            total_spending = int(sum(expense.amount for expense in expenses_on_day))
            total_spending_per_day.append(total_spending)
        return days_of_month, total_spending_per_day
    except User.DoesNotExist:
        print(f"User with chat ID {user_chat_id} does not exist.")
        return None, None


def get_daily_income(user_chat_id):
    try:
        user = User.objects.get(chat_id=user_chat_id)
        current_date = datetime.now().date()
        num_days_in_month = monthrange(current_date.year, current_date.month)[1]
        days_of_month = list(range(1, num_days_in_month + 1))
        total_income_per_day = []
        for day in days_of_month:
            incomes_on_day = Income.objects.filter(user=user,
                                                    date_time__year=current_date.year,
                                                    date_time__month=current_date.month,
                                                    date_time__day=day)
            total_income = int(sum(income.amount for income in incomes_on_day))
            total_income_per_day.append(total_income)
        return days_of_month, total_income_per_day
    except User.DoesNotExist:
        print(f"User with chat ID {user_chat_id} does not exist.")
        return None, None


def get_spendings(user_chat_id):
    try:
        user = User.objects.get(chat_id=user_chat_id)
        user_sums = Sums.objects.filter(user=user)
        category_names = []
        sum_of_expenses = []
        for sum_obj in user_sums:
            category_name = Category.objects.get(id=sum_obj.category_id).name
            category_names.append(category_name)
            sum_of_expenses.append(sum_obj.sum_of_expenses)
        return category_names, sum_of_expenses
    except User.DoesNotExist:
        print(f"User with chat ID {user_chat_id} does not exist.")
        return None, None


def reset_user_data(user_chat_id):
    try:
        user = User.objects.get(chat_id=user_chat_id)
        Income.objects.filter(user=user).delete()
        Expense.objects.filter(user=user).delete()
        Sums.objects.filter(user=user).delete()
        user.delete()
        print(f"All data for user with chat ID {user_chat_id} has been reset.")
    except User.DoesNotExist:
        print(f"User with chat ID {user_chat_id} does not exist.")
