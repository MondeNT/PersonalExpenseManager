from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Expense, Income, Category, Budget

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control short-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control short-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control short-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control short-input'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description', 'receipt']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control short-input'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control short-input'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control short-input'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control short-input'}),
            'receipt': forms.FileInput(attrs={'class': 'form-control short-input'}),
        }

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date']
        widgets = {
            'source': forms.TextInput(attrs={'class': 'form-control short-input'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control short-input'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control short-input'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control short-input'}),
        }


class BudgetForm(forms.ModelForm):
    recurring = forms.BooleanField(required=False, initial=False, help_text="Should this budget recur automatically?")
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'short-input'}), required=False)

    class Meta:
        model = Budget
        fields = ['category', 'limit', 'recurring', 'notes']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control short-input'}),
            'limit': forms.NumberInput(attrs={'placeholder': 'Enter limit amount in Rands', 'class': 'form-control short-input'}),
        }
