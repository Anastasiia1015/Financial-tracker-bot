from django.db import models


class User(models.Model):
    chat_id = models.IntegerField(unique=True)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE, related_name='users')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    date_time = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Sums(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sums')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sum_of_expenses = models.DecimalField(max_digits=10, decimal_places=2)


class Plan(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField('Category', through='PlanCategory')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PlanCategory(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    percentage = models.FloatField(default=0)  # Range: 0 to 1

    class Meta:
        unique_together = ['plan', 'category']
