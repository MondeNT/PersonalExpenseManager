from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense, Income, Category, Budget
from .forms import ExpenseForm, IncomeForm, CategoryForm, BudgetForm
from django.db.models import Sum
from django.contrib import messages
from decimal import Decimal
from django.utils.timezone import now
from .models import User
import json
from django.utils.safestring import mark_safe


# Create your views here.

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'Account created successfully for {user.username}!')
        return redirect('home')

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Successfully logged in!')
        return super().form_valid(form)

@login_required
def home_view(request):
    # Retrieve all expenses and calculate the total
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_expenses = Decimal(total_expenses)  # Ensure total_expenses is a Decimal

    # Retrieve all incomes and calculate the total
    total_income = Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_income = Decimal(total_income)  # Ensure total_income is a Decimal

    # Determine if expenses are over or under income
    if total_expenses <= total_income:
        budget_message = "Your expenses are within your income!"
        budget_class = "text-success"  # Green text for success
    else:
        budget_message = "Your expenses exceed your income!"
        budget_class = "text-danger"  # Red text for danger

    context = {

        'total_expenses': total_expenses,
        'total_income': total_income,
        'budget_status': budget_message,
        'budget_class': budget_class,
        'expenses': Expense.objects.filter(user=request.user),
        'incomes': Income.objects.filter(user=request.user),
    }

    return render(request, 'home.html', context)


# Category Management
@login_required
def category_list_view(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'category_list.html', {'categories': categories})

@login_required
def category_create_view(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        category.save()
        messages.success(request, 'Category created successfully!')
        return redirect('category_list')
    return render(request, 'category_form.html', {'form': form})

@login_required
def category_edit_view(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, 'Category updated successfully!')
        return redirect('category_list')
    return render(request, 'category_form.html', {'form': form})

@login_required
def category_delete_view(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})

# Expense Management
@login_required
def expense_list_view(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expense_list.html', {'expenses': expenses})

@login_required
def expense_create_view(request):
    form = ExpenseForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        messages.success(request, 'Expense added successfully!')
        return redirect('expense_list')
    return render(request, 'expense_form.html', {'form': form})

@login_required
def expense_edit_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, request.FILES or None, instance=expense)
    if form.is_valid():
        form.save()
        messages.success(request, 'Expense updated successfully!')
        return redirect('expense_list')
    return render(request, 'expense_form.html', {'form': form})

@login_required
def expense_delete_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expense_list')
    return render(request, 'expense_confirm_delete.html', {'expense': expense})

# Income Management
@login_required
def income_list_view(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'income_list.html', {'incomes': incomes})

@login_required
def income_create_view(request):
    form = IncomeForm(request.POST or None)
    if form.is_valid():
        income = form.save(commit=False)
        income.user = request.user
        income.save()
        messages.success(request, 'Income added successfully!')
        return redirect('income_list')
    return render(request, 'income_form.html', {'form': form})

@login_required
def income_edit_view(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    form = IncomeForm(request.POST or None, instance=income)
    if form.is_valid():
        form.save()
        messages.success(request, 'Income updated successfully!')
        return redirect('income_list')
    return render(request, 'income_form.html', {'form': form})

@login_required
def income_delete_view(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income deleted successfully!')
        return redirect('income_list')
    return render(request, 'income_confirm_delete.html', {'income': income})

# Budget Management
@login_required
def budget_list_view(request, month=None, year=None):
    if not month or not year:
        from django.utils.timezone import now  # Make sure to import now
        month = now().month
        year = now().year
    
    # Retrieve all budgets for the user for the specified month and year
    budgets = Budget.objects.filter(user=request.user, month=month, year=year)

    # Calculate the total budget limit
    total_budget = budgets.aggregate(total=Sum('limit'))['total'] or Decimal('0.00')
    
    # Retrieve all expenses for the user for the specified month and year
    total_expenses = Expense.objects.filter(user=request.user, date__month=month, date__year=year).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # Calculate remaining budget
    remaining_budget = total_budget - total_expenses

    # Determine budget status
    if remaining_budget >= Decimal('0.00'):
        budget_message = "You are within your budget!"
        budget_class = "text-success"  # Green text for success
    else:
        budget_message = "You are over your budget!"
        budget_class = "text-danger"  # Red text for danger

    context = {
        'budgets': budgets,
        'month': month,
        'year': year,
        'budget_status': budget_message,
        'budget_class': budget_class,
    }

    return render(request, 'budget_list.html', context)

@login_required
def budget_create_view(request):
    form = BudgetForm(request.POST or None)
    if form.is_valid():
        budget = form.save(commit=False)
        budget.user = request.user
        budget.save()
        messages.success(request, 'Budget created successfully!')
        return redirect('budget_list')
    return render(request, 'budget_form.html', {'form': form})

@login_required
def budget_edit_view(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    form = BudgetForm(request.POST or None, instance=budget)
    if form.is_valid():
        form.save()
        messages.success(request, 'Budget updated successfully!')
        return redirect('budget_list')
    return render(request, 'budget_form.html', {'form': form})

@login_required
def budget_delete_view(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully!')
        return redirect('budget_list')
    return render(request, 'budget_confirm_delete.html', {'budget': budget})

# Reports
import json
import plotly.express as px
from django.shortcuts import render
from django.utils.timezone import now
from .models import Expense, Income

def report_view(request):
    # Retrieve all expenses and calculate the total
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_expenses = Decimal(total_expenses)

    # Retrieve all incomes and calculate the total
    total_income = Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_income = Decimal(total_income)

    # Determine if expenses are over or under income
    if total_expenses <= total_income:
        budget_message = "Your expenses are within your income!"
        budget_class = "text-success"
    else:
        budget_message = "Your expenses exceed your income!"
        budget_class = "text-danger"

    # Calculate savings rate and expense to income ratio
    if total_income > 0:
        savings_rate = ((total_income - total_expenses) / total_income) * 100
        expense_to_income_ratio = (total_expenses / total_income) * 100
        net_income = total_income - total_expenses
    else:
        savings_rate = None
        expense_to_income_ratio = None
        net_income = None

    # Prepare data for the expense distribution pie chart
    expenses_by_category = Expense.objects.filter(user=request.user).values('category__name').annotate(total_amount=Sum('amount'))
    categories = [item['category__name'] for item in expenses_by_category]
    amounts = [float(item['total_amount']) for item in expenses_by_category]

    # Create Plotly figure
    fig = px.pie(values=amounts, names=categories, title='Expense Distribution')

    # Convert plotly figure to JSON
    plot_div = fig.to_json()

    context = {
        'total_expenses': total_expenses,
        'total_income': total_income,
        'budget_status': budget_message,
        'budget_class': budget_class,
        'savings_rate': savings_rate,
        'expense_to_income_ratio': expense_to_income_ratio,
        'net_income': net_income,
        'plot_div': plot_div,
    }

    return render(request, 'report.html', context)






