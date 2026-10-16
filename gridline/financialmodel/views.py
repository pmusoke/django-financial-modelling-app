from decimal import Decimal

from django.http import HttpResponse
import datetime

import calendar

from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import *

from django.db import IntegrityError

from.helper import *

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "loginform"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "loginform"}))

class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "registrationform"}))
    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={"class": "registrationform"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "registrationform"}))
    confirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "registrationform"}))

class ProjectForm(forms.Form):
    name = forms.CharField(label="Project Name", widget=forms.TextInput(attrs={"class": "projectform"}))

class ScenarioForm(forms.Form):
    project_name = forms.ModelChoiceField(queryset=Project.objects.none() , label="Project", widget=forms.Select(attrs={"class": "scenarioform"}))
    scenario_name = forms.CharField(label="Scenario Name", widget=forms.TextInput(attrs={"class": "scenarioform"}))
    scenario_number = forms.IntegerField(label="Scenario Number", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    first_date_of_time_rulers = forms.DateField(label="First Date of Time Rulers", widget=forms.DateInput(attrs={"class": "scenarioform", "type": "date",}))
    end_of_first_operating_period = forms.DateField(label="End of First Operating Period", widget=forms.DateInput(attrs={"class": "scenarioform", "type": "date",}))
    acquisition_date = forms.DateField(label="Acquisition Date", widget=forms.DateInput(attrs={"class": "scenarioform", "type": "date",}))
    length_of_contract = forms.IntegerField(label="Length of Contract", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    q1_sa = forms.DecimalField(label="Q1 Seasonal Adjustment '%' of annual yield", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    q2_sa = forms.DecimalField(label="Q2 Seasonal Adjustment '%' of annual yield", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    q3_sa = forms.DecimalField(label="Q3 Seasonal Adjustment '%' of annual yield", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    q4_sa = forms.DecimalField(label="Q4 Seasonal Adjustment '%' of annual yield", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    annual_degredation = forms.DecimalField(label="Annual Degradation %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    year_1_p50_production = forms.DecimalField(label="Year 1 p50 Production", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    availability = forms.DecimalField(label="Availability %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    power_tarrif = forms.DecimalField(label="Power Tariff", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    annual_om_cost = forms.DecimalField(label="Annual Real O&M Cost", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    cpi_at_close = forms.DecimalField(label="Expected CPI at close", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    cpi_sign_date = forms.DecimalField(label="CPI at O&M contract signature date", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    cpi_growth_rate = forms.DecimalField(label="Forecast CPI Growth Rate %", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    senior_debt_gearing = forms.DecimalField(label="Senior Debt Gearing %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    senior_debt_day_convention = forms.DecimalField(label="Senior Debt Day Count Convention days", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    senior_debt_swap_rate = forms.DecimalField(label="Senior Debt Swap Rate %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    senior_debt_int_margin = forms.DecimalField(label="Senior Interest Margin %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    repayment_term = forms.DecimalField(label="Repayment Term years", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    rcf_interest_rate = forms.DecimalField(label="Interest Rate %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    rcf_innit = forms.DecimalField(label="Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    share_of_project = forms.DecimalField(label="Share of Project %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100 )
    target_irr = forms.DecimalField(label="Target IRR %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    accounts_receivable_days = forms.DecimalField(label="Accounts Receivable Days", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    accounts_payable_days = forms.DecimalField(label="Accounts Payable Days", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    useful_life = forms.DecimalField(label="Useful Life Of Solar Asset", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0 )
    book_value = forms.DecimalField(label="Solar Asset Book Value", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    retained_cash_innit = forms.DecimalField(label="Retained Cash - Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    accounts_recievable_innit = forms.DecimalField(label="Accounts Receivable - Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    accounts_payable_innit = forms.DecimalField(label="Accounts Payable - Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    retained_earnings_innit = forms.DecimalField(label="Retained earnings - Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    deffered_tax_innit = forms.DecimalField(label="Deferred Tax - Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    tax_rate = forms.DecimalField(label="Corporate Income Tax Rate", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    tax_depreciation_rate = forms.DecimalField(label="Tax Depreciation Rate %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    tax_losses_carried_forward_innit = forms.DecimalField(label="Tax Losses Carried Forward - Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))






    def __init__(self, *args, project_choices, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project_name"].queryset = project_choices


class UpdateScenarioForm(forms.Form):
    scenario_name = forms.CharField(label="Scenario Name", widget=forms.TextInput(attrs={"class": "scenarioform"}))
    scenario_number = forms.IntegerField(label="Scenario Number", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    first_date_of_time_rulers = forms.DateField(label="First Date of Time Rulers", widget=forms.DateInput(attrs={"class": "scenarioform", "type": "date",}))
    end_of_first_operating_period = forms.DateField(label="End of First Operating Period", widget=forms.DateInput(attrs={"class": "scenarioform", "type": "date",}))
    acquisition_date = forms.DateField(label="Acquisition Date", widget=forms.DateInput(attrs={"class": "scenarioform", "type": "date",}))
    length_of_contract = forms.IntegerField(label="Length of Contract", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    q1_sa = forms.DecimalField(label="Revenue: Q1 Seasonal Adjustment '%' of annual yield", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    q2_sa = forms.DecimalField(label="Revenue: Q2 Seasonal Adjustment '%' of annual yield", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    q3_sa = forms.DecimalField(label="Revenue: Q3 Seasonal Adjustment '%' of annual yield", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    q4_sa = forms.DecimalField(label="Revenue: Q4 Seasonal Adjustment '%' of annual yield", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    annual_degredation = forms.DecimalField(label="Revenue: Annual Degradation %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    year_1_p50_production = forms.DecimalField(label="Revenue: Year 1 p50 Production", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    availability = forms.DecimalField(label="Revenue: Availability %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100 )
    power_tarrif = forms.DecimalField(label="Revenue: Power Tariff", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    annual_om_cost = forms.DecimalField(label="OPEX: Annual Real O&M Cost", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    cpi_at_close = forms.DecimalField(label="OPEX: Expected CPI at close", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    cpi_sign_date = forms.DecimalField(label="OPEX: CPI at O&M contract signature date", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    cpi_growth_rate = forms.DecimalField(label="OPEX: Forecast CPI Growth Rate %", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    senior_debt_gearing = forms.DecimalField(label="Senior Debt: Senior Debt Gearing %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    senior_debt_day_convention = forms.DecimalField(label="Senior Debt: Senior Debt Day Count Convention days", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    senior_debt_swap_rate = forms.DecimalField(label="Senior Debt: Senior Debt Swap Rate %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    senior_debt_int_margin = forms.DecimalField(label="Senior Debt: Senior Interest Margin %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    repayment_term = forms.DecimalField(label="Senior Debt: Repayment Term years", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0 )
    rcf_interest_rate = forms.DecimalField(label="Revolving Credit Facility: Interest Rate %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    rcf_innit = forms.DecimalField(label="Revolving Credit Facility: Initial Balance %", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    share_of_project = forms.DecimalField(label="Equity: Initial Balance %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    target_irr = forms.DecimalField(label="Equity: Target IRR %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0 )
    accounts_receivable_days = forms.DecimalField(label="Working Capital: Accounts Receivable Days", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    accounts_payable_days = forms.DecimalField(label="Working Capital: Accounts Payable Days", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    useful_life = forms.DecimalField(label="Depreciation: Useful Life Of Solar Asset", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    book_value = forms.DecimalField(label="Depreciation: Solar Asset Book Value", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0)
    retained_cash_innit = forms.DecimalField(label="Assets: Retained Cash - Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    accounts_recievable_innit = forms.DecimalField(label="Assets: Accounts Receivable - Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    accounts_payable_innit = forms.DecimalField(label="Liabilities: Accounts Payable - Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    retained_earnings_innit = forms.DecimalField(label="Liabilities: Retained earnings - Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    deffered_tax_innit = forms.DecimalField(label="Liabilities: Deferred Tax - Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))
    tax_rate = forms.DecimalField(label="Tax: Corporate Income Tax Rate", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    tax_depreciation_rate = forms.DecimalField(label="Tax: Tax Depreciation Rate %", widget=forms.NumberInput(attrs={"class": "scenarioform"}), min_value=0, max_value=100)
    tax_losses_carried_forward_innit = forms.DecimalField(label="Tax: Tax Losses Carried Forward - Initial Balance", widget=forms.NumberInput(attrs={"class": "scenarioform"}))

    



# Create your views here.
def index(request):

    return render(request, "financialmodel/index.html")



def login_view(request):
    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            
            else:
                return render(request, "financialmodel/login.html", {
                    "message": "Username and/or Password are not valid", 
                    "form": form
                })
            

    else:
        form = LoginForm()

        return render(request, "financialmodel/login.html", {
            "form": form
        })
    

def register(request):
    if request.method == "POST":
        
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            confirm = request.POST["confirm"]

            if password != confirm:
                return render(request, "financialmodel/register.html", {
                    "message": "passwords do not match",
                    "form": form
                })
            
            
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "financialmodel/register.html", {
                    "message": "username is already in use",
                    "form": form
                })
            
            login(request, user)

            return HttpResponseRedirect(reverse("index"))
        
    else:
        form = RegistrationForm()

        return render(request, "financialmodel/register.html", {
            "form": form,
            "active_page": "registration"
        })
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
    

@login_required
def createproject(request):

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():

            user = request.user
            project_name = request.POST["name"]
            creator = User.objects.get(username=user)

            project = Project.objects.create(
                owner = creator,
                name = project_name
            )
            project.save()

            return render(request, "financialmodel/index.html")
        

    else:

        form = ProjectForm()
        return render(request, "financialmodel/createproject.html", {
            "form": form
        })
    

@login_required
def viewprojects(request, user):
    vuser = user

    currentuser = User.objects.get(username=vuser)

    metrics = Metrics.objects.all().filter(related_scenario__related_project__owner=currentuser)

    if metrics.exists() == False:
        return render(request, "financialmodel/viewprojects.html", {
            "message": "Project details will be displayed once projects and scenarios have been created"
        })

    
    return render(request, "financialmodel/viewprojects.html", {
        "metrics": metrics
    })



@login_required
def createscenario(request):

    vuser = request.user

    current_user = User.objects.get(username=vuser)


    projects = Project.objects.all().filter(owner=current_user)

    if not projects.exists():
        return render(request, "financialmodel/createproject.hmtl", {
            "message": "To Create a scenario, please create a project first",
            "form": ProjectForm()
        })
    
    
    if request.method == "POST":

        form = ScenarioForm( request.POST, project_choices=projects)

        if form.is_valid():

            project_id = request.POST["project_name"]

            project = Project.objects.get(pk=project_id)

            scenario_name = request.POST["scenario_name"]
            scenario_number = request.POST["scenario_number"]

            first_date_of_time_rulers = str(request.POST["first_date_of_time_rulers"])

            first_date_of_time_rulers = datefunction(first_date_of_time_rulers)

            end_of_first_operating_period = str(request.POST["end_of_first_operating_period"])

            end_of_first_operating_period = datefunction(end_of_first_operating_period)

            acquisition_date = str(request.POST["acquisition_date"])

            acquisition_date = datefunction(acquisition_date)

            validation_one = acquisition_date - first_date_of_time_rulers

            if int(validation_one.days) < 0:
                return render(request, "financialmodel/error.html", {
                    "error": "Acquisition Date must be after the start of the model date."
                })

            length_of_contract = int(request.POST["length_of_contract"])

            q1_sa = float(request.POST["q1_sa"]) / 100
            q2_sa = float(request.POST["q2_sa"]) / 100
            q3_sa = float(request.POST["q3_sa"]) / 100
            q4_sa = float(request.POST["q4_sa"]) / 100

            if q1_sa + q2_sa + q3_sa + q4_sa != 1:
                return render(request, "financialmodel/error.html", {
                    "error": "Seasonality must add up to 100"
                })

            

            

            annual_degredation = float(request.POST["annual_degredation"]) / 100
            year_1_p50_production = float(request.POST["year_1_p50_production"])
            availability = float(request.POST["availability"]) / 100
            power_tarrif = float(request.POST["power_tarrif"])
            annual_om_cost = float(request.POST["annual_om_cost"])
            cpi_at_close = float(request.POST["cpi_at_close"])
            cpi_sign_date = float(request.POST["cpi_sign_date"])
            cpi_growth_rate = float(request.POST["cpi_growth_rate"]) / 100
            senior_debt_gearing = float(request.POST["senior_debt_gearing"]) / 100
            senior_debt_day_convention = int(request.POST["senior_debt_day_convention"])
            senior_debt_swap_rate = float(request.POST["senior_debt_swap_rate"]) / 100
            senior_debt_int_margin = float(request.POST["senior_debt_int_margin"]) / 100
            repayment_term = int(request.POST["repayment_term"])

            if repayment_term > length_of_contract:
                return render(request, "financialmodel/error.html", {
                    "error": "length of debt should not exceed the length of the project"
                })
            

            rcf_interest_rate = float(request.POST["rcf_interest_rate"]) / 100
            rcf_innit = float(request.POST["rcf_innit"])
            share_of_project = float(request.POST["share_of_project"]) / 100
            target_irr = float(request.POST["target_irr"]) / 100
            accounts_receivable_days = int(request.POST["accounts_receivable_days"])
            accounts_payable_days = int(request.POST["accounts_payable_days"])
            useful_life = int(request.POST["useful_life"])
            book_value = float(request.POST["book_value"])
            retained_cash_innit = float(request.POST["retained_cash_innit"])
            accounts_recievable_innit = float(request.POST["accounts_recievable_innit"])
            accounts_payable_innit = float(request.POST["accounts_payable_innit"])
            retained_earnings_innit = float(request.POST["retained_earnings_innit"])
            deffered_tax_innit = float(request.POST["deffered_tax_innit"])
            tax_rate = float(request.POST["tax_rate"]) / 100
            tax_depreciation_rate = float(request.POST["tax_depreciation_rate"]) / 100
            tax_losses_carried_forward_innit = float(request.POST["tax_losses_carried_forward_innit"])

            scenario = Scenario.objects.create(
                related_project = project,
                scenario_name = scenario_name,
                scenario_number = scenario_number
            )
            scenario.save()

            input = Input.objects.create(
                related_scenario = scenario,
                first_date_of_time_rulers = first_date_of_time_rulers,
                end_of_first_operating_period = end_of_first_operating_period,
                acquisition_date = acquisition_date,
                length_of_contract = length_of_contract,
                q1_sa = q1_sa,
                q2_sa = q2_sa,
                q3_sa = q3_sa,
                q4_sa = q4_sa,
                annual_degredation = annual_degredation,
                year_1_p50_production = year_1_p50_production,
                availability = availability,
                power_tarrif = power_tarrif,
                annual_om_cost = annual_om_cost,
                cpi_at_close = cpi_at_close,
                cpi_sign_date = cpi_sign_date,
                cpi_growth_rate = cpi_growth_rate,
                senior_debt_gearing = senior_debt_gearing,
                senior_debt_day_convention = senior_debt_day_convention,
                senior_debt_swap_rate = senior_debt_swap_rate,
                senior_debt_int_margin = senior_debt_int_margin,
                repayment_term = repayment_term,
                rcf_interest_rate = rcf_interest_rate,
                rcf_innit = rcf_innit,
                share_of_project = share_of_project,
                target_irr = target_irr,
                accounts_receivable_days = accounts_receivable_days,
                accounts_payable_days = accounts_payable_days,
                useful_life = useful_life,
                book_value = book_value,
                retained_cash_innit = retained_cash_innit,
                accounts_recievable_innit = accounts_recievable_innit,
                accounts_payable_innit = accounts_payable_innit,
                retained_earnings_innit = retained_earnings_innit,
                deffered_tax_innit = deffered_tax_innit,
                tax_rate = tax_rate,
                tax_depreciation_rate = tax_depreciation_rate,
                tax_losses_carried_forward_innit = tax_losses_carried_forward_innit
            )
            input.save()

            calculate(input, "create")

            return render(request, "financialmodel/index.html")
        
    else:

        form = ScenarioForm(project_choices=projects)
        return render(request, "financialmodel/createscenario.html", {
        "form": form
    })


@login_required
def deletescenario(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    scenario.delete()

    return render(request, "financialmodel/index.html")



@login_required
def quarterly_financial_statements(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })


    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    revenues = []
    expenses = []
    depreciations = []
    ebits = []
    ebitdas = []
    debts = []
    rfis = []
    rcfs = []
    profit_before_taxes = []
    tax_expenses = []
    profit_after_taxes = []
    cash_taxes = []
    cash_flow_available_for_senior_debts = []
    cash_flow_available_for_refinancing_facilities = []
    cash_flow_available_for_rcfs = []
    cash_flow_available_for_shareholders = []
    share_capitals = []
    cash_flow_available_for_dividends = []
    net_cash_flows = []
    retained_earnings = []
    current_assets = []
    total_assets = []
    deferred_taxes = []
    total_liabilities = []
    differences = []
    statuses = []



    for i in range(len(timelines)):

        timeline = timelines[i]

        revenue = Revenue.objects.get(timeline_event=timeline)
        revenues.append(revenue)

        expense = Expense.objects.get(timeline_event=timeline)
        expenses.append(expense)

        depreciation = Depreciation.objects.get(timeline_event=timeline)
        depreciations.append(depreciation)

        ebit = Ebit.objects.get(timeline_event=timeline)
        ebits.append(ebit)

        ebitda = Ebitda.objects.get(timeline_event=timeline)
        ebitdas.append(ebitda)

        debt= Debt.objects.get(timeline_event=timeline)
        debts.append(debt)

        rfis.append(0)

        rcf = Rcf.objects.get(timeline_event=timeline)
        rcfs.append(rcf)

        profit_before_tax = Profit_before_tax.objects.get(timeline_event=timeline)
        profit_before_taxes.append(profit_before_tax.profit_before_tax)

        accounting_tax = Accounting_tax.objects.get(timeline_event=timeline)
        tax_expenses.append(accounting_tax.tax_expense)

        profit_after_tax = Profit_after_tax.objects.get(timeline_event=timeline)
        profit_after_taxes.append(profit_after_tax)
        
        cash_tax = Cash_tax.objects.get(timeline_event=timeline)
        cash_taxes.append(cash_tax)

        cash_flow_available_for_senior_debt = Cash_flow_available_for_senior_debt.objects.get(timeline_event=timeline)
        cash_flow_available_for_senior_debts.append(cash_flow_available_for_senior_debt)

        cash_flow_available_for_refinancing_facility = Cash_flow_available_for_refinancing_facility.objects.get(timeline_event=timeline)
        cash_flow_available_for_refinancing_facilities.append(cash_flow_available_for_refinancing_facility)

        cash_flow_available_for_rcf = Cash_flow_available_for_rcf.objects.get(timeline_event=timeline)
        cash_flow_available_for_rcfs.append(cash_flow_available_for_rcf)

        cash_flow_available_for_shareholder = Cash_flow_available_for_shareholders.objects.get(timeline_event=timeline)
        cash_flow_available_for_shareholders.append(cash_flow_available_for_shareholder)

        share_capital = Share_Capital.objects.get(timeline_event=timeline)
        share_capitals.append(share_capital)

        cash_flow_available_for_dividend = Cash_flow_available_for_dividends.objects.get(timeline_event=timeline)
        cash_flow_available_for_dividends.append(cash_flow_available_for_dividend)

        net_cash_flow = Net_cash_flow.objects.get(timeline_event=timeline)
        net_cash_flows.append(net_cash_flow)

        retained_earning = Retained_earnings.objects.get(timeline_event=timeline)
        retained_earnings.append(retained_earning)

        current_asset = revenue.accounts_receivable + retained_earning.retained_cash
        current_assets.append(current_asset)

        total_asset = current_asset + depreciation.solar_asset_value
        total_assets.append(total_asset)

        deferred_tax = Deferred_tax.objects.get(timeline_event=timeline)
        deferred_taxes.append(deferred_tax)

        total_liability = expense.accounts_payable + debt.senior_debt + rcf.rcf_balance + deferred_tax.deferred_tax + share_capital.share_capital + retained_earning.retained_earnings
        total_liabilities.append(total_liability)

        difference = total_asset - total_liability
        differences.append(difference)

        tolerance = Decimal("0.10")

        if abs(difference) <= tolerance:
            status = "PASS"
        else:
            status = "FAIL"

        statuses.append(status)



    




    return render(request, "financialmodel/quarterly_financial_statements.html", {
        "scenario": scenario,
        "timelines": timelines,
        "revenues": revenues,
        "expenses": expenses,
        "ebits": ebits,
        "ebitdas": ebitdas,
        "depreciations": depreciations,
        "debts": debts,
        "rfis": rfis,
        "rcfs": rcfs,
        "profit_before_taxes": profit_before_taxes,
        "tax_expenses": tax_expenses,
        "profit_after_taxes": profit_after_taxes,
        "cash_taxes": cash_taxes,
        "cash_flow_available_for_senior_debts": cash_flow_available_for_senior_debts,
        "cash_flow_available_for_refinancing_facilities": cash_flow_available_for_refinancing_facilities,
        "cash_flow_available_for_rcfs": cash_flow_available_for_rcfs,
        "cash_flow_available_for_shareholders": cash_flow_available_for_shareholders,
        "share_capitals": share_capitals,
        "cash_flow_available_for_dividends": cash_flow_available_for_dividends,
        "net_cash_flows": net_cash_flows,
        "retained_earnings": retained_earnings,
        "current_assets": current_assets,
        "total_assets": total_assets,
        "deferred_taxes": deferred_taxes,
        "total_liabilities": total_liabilities,
        "differences": differences,
        "statuses": statuses

    })

@login_required
def annual_financial_statements(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    inputs = Input.objects.get(related_scenario=scenario)
    acq_date = inputs.acquisition_date

    year_end_timelines = []
    revenues = []
    expenses = []
    ebitdas = []
    depreciations = []
    ebits = []
    senior_debt_interests = []
    rcf_interests = []
    profit_before_taxes = []
    tax_expenses = []
    profit_after_taxes = []
    cash_received_from_invoices = []
    cash_paid_for_expenses = []
    taxes_paid = []
    cash_flow_available_for_senior_debts = []
    senior_debt_principal_repayments = []
    cash_flow_available_for_refinancing_facilities = []
    rcf_drawdowns = []
    rcf_principal_repayments = []
    rcf_interest_paids = []
    cash_flow_available_for_shareholders = []
    share_capital_redemptions = []
    cash_flow_available_for_dividends = []
    net_cash_flows = []
    solar_asset_balances = []
    retained_cash_balances = []
    accounts_receivable_balances = []
    current_assets = []
    total_assets = []
    accounts_payable_balances = []
    senior_debt_balances = []
    rcf_balances = []
    deferred_tax_balances = []
    share_capital_balances = []
    retained_earnings_balances = []
    differences = []
    total_liabilities = []
    statuses = []

    revenue = 0
    expense = 0
    ebitda = 0
    depreciation = 0
    ebit = 0
    senior_debt_interest = 0
    rcf_interest = 0
    profit_before_tax = 0
    tax_expense = 0
    profit_after_tax = 0
    cash_received_from_invoice = 0
    cash_paid_for_expense = 0
    tax_paid = 0
    cash_flow_available_for_senior_debt = 0
    senior_debt_principal_repayment = 0
    cash_flow_available_for_refinancing_facility = 0
    rcf_drawdown = 0
    rcf_principal_repayment = 0
    rcf_interest_paid = 0
    cash_flow_available_for_shareholder = 0
    share_capital_redemption = 0
    cash_flow_available_for_dividend = 0
    net_cash_flow = 0


    for i in range(len(timelines)):

        timeline = timelines[i]

        if inputs.acquisition_date.month == timeline.date.month:
            revenue_object = Revenue.objects.get(timeline_event=timeline)
            revenue += revenue_object.revenue
            revenues.append(revenue)
            revenue = 0

            expense_object = Expense.objects.get(timeline_event=timeline)
            expense += expense_object.expense
            expenses.append(expense)
            expense = 0

            ebitda_object = Ebitda.objects.get(timeline_event=timeline)
            ebitda += ebitda_object.ebitda
            ebitdas.append(ebitda)
            ebitda = 0

            depreciation_object = Depreciation.objects.get(timeline_event=timeline)
            depreciation += depreciation_object.depreciation
            depreciations.append(depreciation)
            depreciation = 0

            ebit_object = Ebit.objects.get(timeline_event=timeline)
            ebit += ebit_object.ebit
            ebits.append(ebit)
            ebit = 0

            debt_object = Debt.objects.get(timeline_event=timeline)
            senior_debt_interest += debt_object.senior_debt_interest
            senior_debt_interests.append(senior_debt_interest)
            senior_debt_interest = 0

            rcf_object = Rcf.objects.get(timeline_event=timeline)
            rcf_interest += rcf_object.rcf_interest
            rcf_interests.append(rcf_interest)
            rcf_interest = 0

            profit_before_tax_object = Profit_before_tax.objects.get(timeline_event=timeline)
            profit_before_tax += profit_before_tax_object.profit_before_tax
            profit_before_taxes.append(profit_before_tax)
            profit_before_tax = 0

            accounting_tax_object = Accounting_tax.objects.get(timeline_event=timeline)
            tax_expense += accounting_tax_object.tax_expense
            tax_expenses.append(tax_expense)
            tax_expense = 0

            profit_after_tax_object = Profit_after_tax.objects.get(timeline_event=timeline)
            profit_after_tax += profit_after_tax_object.profit_after_tax
            profit_after_taxes.append(profit_after_tax)
            profit_after_tax = 0

            cash_received_from_invoice += revenue_object.cash_received_from_invoices
            cash_received_from_invoices.append(cash_received_from_invoice)
            cash_received_from_invoice = 0

            cash_paid_for_expense += expense_object.cash_paid_for_expense
            cash_paid_for_expenses.append(cash_paid_for_expense)
            cash_paid_for_expense = 0

            cash_tax_object = Cash_tax.objects.get(timeline_event=timeline)
            tax_paid += cash_tax_object.corporate_income_tax_paid
            taxes_paid.append(tax_paid)
            tax_paid = 0

            cash_flow_available_for_senior_debt_object = Cash_flow_available_for_senior_debt.objects.get(timeline_event=timeline)
            cash_flow_available_for_senior_debt += cash_flow_available_for_senior_debt_object.cash_flow_available_for_senior_debt
            cash_flow_available_for_senior_debts.append(cash_flow_available_for_senior_debt)
            cash_flow_available_for_senior_debt = 0

            senior_debt_principal_repayment += debt_object.senior_debt_repayment
            senior_debt_principal_repayments.append(senior_debt_principal_repayment)
            senior_debt_principal_repayment = 0

            cash_flow_available_for_refinancing_facility_object = Cash_flow_available_for_refinancing_facility.objects.get(timeline_event=timeline)
            cash_flow_available_for_refinancing_facility += cash_flow_available_for_refinancing_facility_object.cash_flow_available_for_refinancing_facility
            cash_flow_available_for_refinancing_facilities.append(cash_flow_available_for_refinancing_facility)
            cash_flow_available_for_refinancing_facility = 0

            rcf_object = Rcf.objects.get(timeline_event=timeline)
            rcf_drawdown += rcf_object.rcf_drawdown
            rcf_principal_repayment += rcf_object.rcf_principal_repayment
            rcf_interest_paid += rcf_object.rcf_interest_paid
            rcf_drawdowns.append(rcf_drawdown)
            rcf_principal_repayments.append(rcf_principal_repayment)
            rcf_interest_paids.append(rcf_interest_paid)
            rcf_drawdown = 0
            rcf_interest_paid = 0
            rcf_principal_repayment = 0

            cash_flow_available_for_shareholders_object = Cash_flow_available_for_shareholders.objects.get(timeline_event=timeline)
            cash_flow_available_for_shareholder += cash_flow_available_for_shareholders_object.cash_flow_available_for_shareholders
            cash_flow_available_for_shareholders.append(cash_flow_available_for_shareholder)
            cash_flow_available_for_shareholder = 0

            share_capital_object = Share_Capital.objects.get(timeline_event=timeline)
            share_capital_redemption += share_capital_object.share_capital_redemption
            share_capital_redemptions.append(share_capital_redemption)
            share_capital_redemption = 0

            cash_flow_available_for_dividends_object = Cash_flow_available_for_dividends.objects.get(timeline_event=timeline)
            cash_flow_available_for_dividend += cash_flow_available_for_dividends_object.cash_flow_available_for_dividends
            cash_flow_available_for_dividends.append(cash_flow_available_for_dividend)
            cash_flow_available_for_dividend = 0

            net_cash_flow_object = Net_cash_flow.objects.get(timeline_event=timeline)
            net_cash_flow += net_cash_flow_object.net_cash_flow
            net_cash_flows.append(net_cash_flow)
            net_cash_flow = 0

            solar_asset_balances.append(depreciation_object.solar_asset_value)

            retained_earnings_object = Retained_earnings.objects.get(timeline_event=timeline)
            retained_cash_balances.append(retained_earnings_object.retained_cash)

            accounts_receivable_balances.append(revenue_object.accounts_receivable)

            current_asset = retained_earnings_object.retained_cash + revenue_object.accounts_receivable
            current_assets.append(current_asset)

            total_asset = current_asset + depreciation_object.solar_asset_value
            total_assets.append(total_asset)

            accounts_payable_balances.append(expense_object.accounts_payable)

            senior_debt_balances.append(debt_object.senior_debt)

            rcf_balances.append(rcf_object.rcf_balance)

            deferred_tax_object = Deferred_tax.objects.get(timeline_event=timeline)
            deferred_tax_balances.append(deferred_tax_object.deferred_tax)

            share_capital_balances.append(share_capital_object.share_capital)

            retained_earnings_balances.append(retained_earnings_object.retained_earnings)

            total_liability = expense_object.accounts_payable + debt_object.senior_debt + rcf_object.rcf_balance + deferred_tax_object.deferred_tax + share_capital_object.share_capital + retained_earnings_object.retained_earnings
            total_liabilities.append(total_liability)

            difference = total_asset - total_liability
            differences.append(difference)

            tolerance = Decimal("0.10")

            if abs(difference) <= tolerance:
                status = "PASS"
            else:
                status = "FAIL"

            statuses.append(status)


            year_end_timelines.append(timeline)

            

        else:
            revenue_object = Revenue.objects.get(timeline_event=timeline)
            revenue += revenue_object.revenue

            expense_object = Expense.objects.get(timeline_event=timeline)
            expense += expense_object.expense

            ebitda_object = Ebitda.objects.get(timeline_event=timeline)
            ebitda += ebitda_object.ebitda

            depreciation_object = Depreciation.objects.get(timeline_event=timeline)
            depreciation += depreciation_object.depreciation

            ebit_object = Ebit.objects.get(timeline_event=timeline)
            ebit += ebit_object.ebit

            debt_object = Debt.objects.get(timeline_event=timeline)
            senior_debt_interest += debt_object.senior_debt_interest

            rcf_object = Rcf.objects.get(timeline_event=timeline)
            rcf_interest += rcf_object.rcf_interest

            profit_before_tax_object = Profit_before_tax.objects.get(timeline_event=timeline)
            profit_before_tax += profit_before_tax_object.profit_before_tax

            accounting_tax_object = Accounting_tax.objects.get(timeline_event=timeline)
            tax_expense += accounting_tax_object.tax_expense

            profit_after_tax_object = Profit_after_tax.objects.get(timeline_event=timeline)
            profit_after_tax += profit_after_tax_object.profit_after_tax

            cash_received_from_invoice += revenue_object.cash_received_from_invoices

            cash_paid_for_expense += expense_object.cash_paid_for_expense

            cash_tax_object = Cash_tax.objects.get(timeline_event=timeline)
            tax_paid += cash_tax_object.corporate_income_tax_paid

            cash_flow_available_for_senior_debt_object = Cash_flow_available_for_senior_debt.objects.get(timeline_event=timeline)
            cash_flow_available_for_senior_debt += cash_flow_available_for_senior_debt_object.cash_flow_available_for_senior_debt

            senior_debt_principal_repayment += debt_object.senior_debt_repayment

            cash_flow_available_for_refinancing_facility_object = Cash_flow_available_for_refinancing_facility.objects.get(timeline_event=timeline)
            cash_flow_available_for_refinancing_facility += cash_flow_available_for_refinancing_facility_object.cash_flow_available_for_refinancing_facility

            rcf_object = Rcf.objects.get(timeline_event=timeline)
            rcf_drawdown += rcf_object.rcf_drawdown
            rcf_principal_repayment += rcf_object.rcf_principal_repayment
            rcf_interest_paid += rcf_object.rcf_interest_paid

            cash_flow_available_for_shareholders_object = Cash_flow_available_for_shareholders.objects.get(timeline_event=timeline)
            cash_flow_available_for_shareholder += cash_flow_available_for_shareholders_object.cash_flow_available_for_shareholders

            share_capital_object = Share_Capital.objects.get(timeline_event=timeline)
            share_capital_redemption += share_capital_object.share_capital_redemption

            cash_flow_available_for_dividends_object = Cash_flow_available_for_dividends.objects.get(timeline_event=timeline)
            cash_flow_available_for_dividend += cash_flow_available_for_dividends_object.cash_flow_available_for_dividends

            net_cash_flow_object = Net_cash_flow.objects.get(timeline_event=timeline)
            net_cash_flow += net_cash_flow_object.net_cash_flow


    return render(request, "financialmodel/annual_financial_statements.html", {
        "scenario": scenario,
        "timelines": year_end_timelines,
        "revenues": revenues,
        "expenses": expenses,
        "ebitdas": ebitdas,
        "depreciations": depreciations,
        "ebits": ebits,
        "senior_debt_interests": senior_debt_interests,
        "rcf_interests": rcf_interests,
        "profit_before_taxes": profit_before_taxes,
        "tax_expenses": tax_expenses,
        "profit_after_taxes": profit_after_taxes,
        "cash_received_from_invoices": cash_received_from_invoices,
        "cash_paid_for_expenses": cash_paid_for_expenses,
        "taxes_paid": taxes_paid,
        "cash_flow_available_for_senior_debts": cash_flow_available_for_senior_debts,
        "senior_debt_principal_repayments": senior_debt_principal_repayments,
        "cash_flow_available_for_refinancing_facilities": cash_flow_available_for_refinancing_facilities,
        "rcf_drawdowns": rcf_drawdowns,
        "rcf_principal_repayments": rcf_principal_repayments,
        "rcf_interest_paids": rcf_interest_paids,
        "cash_flow_available_for_shareholders": cash_flow_available_for_shareholders,
        "share_capital_redemptions": share_capital_redemptions,
        "cash_flow_available_for_dividends": cash_flow_available_for_dividends,
        "net_cash_flows": net_cash_flows,
        "solar_asset_balances": solar_asset_balances,
        "retained_cash_balances": retained_cash_balances,
        "accounts_receivable_balances": accounts_receivable_balances,
        "current_assets": current_assets,
        "total_assets": total_assets,
        "accounts_payable_balances": accounts_payable_balances,
        "senior_debt_balances": senior_debt_balances,
        "rcf_balances": rcf_balances,
        "deferred_tax_balances": deferred_tax_balances,
        "share_capital_balances": share_capital_balances,
        "retained_earnings_balances": retained_earnings_balances,
        "total_liabilities": total_liabilities,
        "differences": differences,
        "statuses": statuses
    })








@login_required
def quarterly_financial_statements_revenue(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    inputs = Input.objects.get(related_scenario=scenario)

    annual_degredation = inputs.annual_degredation

    y1p50 = inputs.year_1_p50_production
    availability = inputs.availability

    power_tarrif = inputs.power_tarrif
    units_in_thousands = 1000
    conversation = 1000000

    compound_degredations = []
    seasonal_adjustments = []
    electricity_generations = []

    revenues = []
    expenses = []

    forecast_accounts_receivable_balances = []

    accounts_receivable_balance_begs = []

    for i in range(len(timelines)):

        timeline = timelines[i]

        if i == 0:
            compound_degredation = 0
            compound_degredations.append(0)

            accounts_receivable_balance_begs.append(0)
        
        else:

            contract_year_number = timeline.contract_year_number
            operating_period_flag = timeline.operating_period_flag

            compound_degredation = float(1/((1+annual_degredation) ** (contract_year_number - 1))) * operating_period_flag
            compound_degredations.append(compound_degredation)

            previous_timeline = timelines[i-1]
            previous_revenue = Revenue.objects.get(timeline_event=previous_timeline)
            accounts_receivable_balance_beg = previous_revenue.accounts_receivable
            accounts_receivable_balance_begs.append(accounts_receivable_balance_beg)

        qsa = 0

        if timeline.period_number == 1:
            qsa = inputs.q1_sa
        elif timeline.period_number == 2:
            qsa = inputs.q2_sa
        elif timeline.period_number == 3:
            qsa = inputs.q3_sa
        else:
            qsa = inputs.q4_sa

        seasonal_adjustment = qsa * timeline.operating_period_flag
        seasonal_adjustments.append(seasonal_adjustment)

        electricity_generation =  float(availability) * float(y1p50) * float(compound_degredation) * float(seasonal_adjustment)
        electricity_generations.append(electricity_generation)

        revenue = Revenue.objects.get(timeline_event=timeline)
        revenues.append(revenue)

        expense = Expense.objects.get(timeline_event=timeline)
        expenses.append(expense)

        account_receivable_days = inputs.accounts_receivable_days
        days_in_period = timeline.days_in_period
        forecast_accounts_receivable_balance = (float(account_receivable_days)/days_in_period) * float(revenue.revenue)
        forecast_accounts_receivable_balances.append(forecast_accounts_receivable_balance)




    return render(request, "financialmodel/revenue.html", {
        "inputs": inputs,
        "timelines": timelines,
        "compound_degredations": compound_degredations,
        "seasonal_adjustments": seasonal_adjustments,
        "electricity_generations": electricity_generations,
        "revenues": revenues,
        "expenses": expenses,
        "forecast_accounts_receivable_balances": forecast_accounts_receivable_balances,
        "accounts_receivable_balance_begs": accounts_receivable_balance_begs
    })

@login_required
def quarterly_financial_statements_expense(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    inputs = Input.objects.get(related_scenario=scenario)

    expenses = []

    forecast_accounts_payable_balances = []

    accounts_payable_balance_begs = []

    for i in range(len(timelines)):

        timeline = timelines[i]

        expense = Expense.objects.get(timeline_event=timeline)
        expenses.append(expense)

        accounts_payable_days = inputs.accounts_payable_days
        days_in_period = timeline.days_in_period
        forecast_accounts_payable_balance = float(expense.expense) * (accounts_payable_days/days_in_period)
        forecast_accounts_payable_balances.append(forecast_accounts_payable_balance)

        if i == 0:
            accounts_payable_balance_begs.append(0)

        else:
            previous_timeline = timelines[i-1]
            previous_expense = Expense.objects.get(timeline_event=previous_timeline)
            accounts_payable_balance_beg = previous_expense.accounts_payable
            accounts_payable_balance_begs.append(accounts_payable_balance_beg)



    return render(request, "financialmodel/expense.html", {
        "inputs": inputs,
        "timelines": timelines,
        "expenses": expenses,
        "scenario": scenario,
        "forecast_accounts_payable_balances": forecast_accounts_payable_balances,
        "accounts_payable_balance_begs": accounts_payable_balance_begs
    })

@login_required
def quarterly_financial_statements_escalation(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    inputs = Input.objects.get(related_scenario=scenario)

    forecast_cpis = []

    expenses = []

    for i in range(len(timelines)):

        timeline = timelines[i]

        expense = Expense.objects.get(timeline_event=timeline)
        expenses.append(expense)

        if i == 0:
            forecast_cpis.append(0)
            forecast_cpi = 0

        elif timeline.finance_close_flag == 1:
            forecast_cpis.append(inputs.cpi_at_close)
            forecast_cpi = float(inputs.cpi_at_close)
        
        else:
            previous_forecast_cpi = float(forecast_cpis[i-1])
            growth_rate = float(inputs.cpi_growth_rate)
            number_of_periods = 4

            forecast_cpi = previous_forecast_cpi * (1+growth_rate)**(1/number_of_periods)
            forecast_cpis.append(forecast_cpi)

    return render(request, "financialmodel/escalation.html", {
        "inputs": inputs,
        "timelines": timelines,
        "forecast_cpis": forecast_cpis,
        "expenses": expenses
    })


@login_required        
def quarterly_financial_statements_depreciation(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    inputs = Input.objects.get(related_scenario=scenario)

    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    depreciations = []

    solar_asset_book_value_begs = []

    for i in range(len(timelines)):

        timeline = timelines[i]

        depreciation = Depreciation.objects.get(timeline_event=timeline)

        depreciations.append(depreciation)

        if i == 0:
            solar_asset_book_value_begs.append(0)
        else:
            previous_timeline = timelines[i-1]
            previous_depreciation = Depreciation.objects.get(timeline_event=previous_timeline)
            solar_asset_book_value_begs.append(previous_depreciation)

    return render(request, "financialmodel/depreciation.html", {
        "inputs": inputs,
        "timelines": timelines, 
        "depreciations": depreciations,
        "solar_asset_book_value_begs": solar_asset_book_value_begs
    })


@login_required
def quarterly_financial_statements_debt(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    inputs = Input.objects.get(related_scenario=scenario)

    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    debts = []

    senior_debt_balance_begs = []

    senior_debt_drawdown = float(inputs.book_value) * float(inputs.senior_debt_gearing)

    all_in_annual_senior_debt_interest_rate = float(inputs.senior_debt_swap_rate) + float(inputs.senior_debt_int_margin)

    senior_debt_period_interest_rates = []

    for i in range(len(timelines)):

        timeline = timelines[i]

        debt = Debt.objects.get(timeline_event=timeline)

        debts.append(debt)

        if i == 0:
            senior_debt_balance_begs.append(0)
        else:
            previous_timeline = timelines[i-1]
            previous_debt = Debt.objects.get(timeline_event=previous_timeline)
            senior_debt_balance_begs.append(previous_debt.senior_debt)

        senior_debt_period_interest_rate = all_in_annual_senior_debt_interest_rate * (float(timeline.days_in_period) / inputs.senior_debt_day_convention)
        senior_debt_period_interest_rates.append(senior_debt_period_interest_rate) 

    

    
    return render(request, "financialmodel/debt.html", {
        "inputs": inputs,
        "timelines": timelines,
        "debts": debts,
        "senior_debt_drawdown": senior_debt_drawdown,
        "senior_debt_balance_begs": senior_debt_balance_begs,
        "all_in_annual_senior_debt_interest_rate": all_in_annual_senior_debt_interest_rate,
        "senior_debt_period_interest_rates": senior_debt_period_interest_rates

    })


@login_required
def quarterly_financial_statements_rcf(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    inputs = Input.objects.get(related_scenario=scenario)

    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    rcfs = []

    retained_cash_balance_begs = []
    cash_flow_available_for_rcfs = []

    cash_available_for_rcf_cash_shortfall_for_rcfs = []

    cash_available_for_rcfs = []

    rcf_period_interests = []

    rcf_balance_begs = []

    rcf_unpaid_interests = []

    cash_available_for_rcf_principal_repayments = []

    for i in range(len(timelines)):

        timeline = timelines[i]

        if i == 0:
            retained_cash_balance_beg = 0
            retained_cash_balance_begs.append(retained_cash_balance_beg)

            rcf_balance_beg = 0
            rcf_balance_begs.append(rcf_balance_beg)
        else:
            previous_timeline = timelines[i-1]
            previous_retained_earnings = Retained_earnings.objects.get(timeline_event=previous_timeline)
            previous_rcf = Rcf.objects.get(timeline_event=previous_timeline)

            retained_cash_balance_beg = previous_retained_earnings.retained_cash
            retained_cash_balance_begs.append(retained_cash_balance_beg)

            rcf_balance_beg = previous_rcf.rcf_balance
            rcf_balance_begs.append(rcf_balance_beg)

        
        cash_flow_available_for_rcf = Cash_flow_available_for_rcf.objects.get(timeline_event=timeline)
        cash_flow_available_for_rcfs.append(cash_flow_available_for_rcf)

        cash_available_for_rcf_cash_shortfall_for_rcf = float(retained_cash_balance_beg) + float(cash_flow_available_for_rcf.cash_flow_available_for_rcf)
        cash_available_for_rcf_cash_shortfall_for_rcfs.append(cash_available_for_rcf_cash_shortfall_for_rcf)

        cash_available_for_rcf = max(0, cash_available_for_rcf_cash_shortfall_for_rcf)
        cash_available_for_rcfs.append(cash_available_for_rcf)

        rcf = Rcf.objects.get(timeline_event=timeline)
        rcfs.append(rcf)

        rcf_interest_rate = float(inputs.rcf_interest_rate)
        day_count_covention = float(inputs.senior_debt_day_convention)
        days_in_period = float(timeline.days_in_period)
        rcf_period_interest = rcf_interest_rate * (days_in_period/day_count_covention)
        rcf_period_interests.append(rcf_period_interest)

        rcf_unpaid_interest = float(rcf.rcf_interest) - float(rcf.rcf_interest_paid)
        rcf_unpaid_interests.append(rcf_unpaid_interest)

        cash_available_for_rcf_principal_repayment = cash_available_for_rcf - float(rcf.rcf_interest_paid)
        cash_available_for_rcf_principal_repayments.append(cash_available_for_rcf_principal_repayment)


    return render(request, "financialmodel/rcf.html", {
        "timelines": timelines,
        "retained_cash_balance_begs": retained_cash_balance_begs,
        "cash_flow_available_for_rcfs": cash_flow_available_for_rcfs,
        "cash_available_for_rcf_cash_shortfall_for_rcfs": cash_available_for_rcf_cash_shortfall_for_rcfs,
        "cash_available_for_rcfs": cash_available_for_rcfs,
        "rcfs": rcfs,
        "inputs": inputs,
        "rcf_period_interests": rcf_period_interests,
        "rcf_unpaid_interests": rcf_unpaid_interests,
        "cash_available_for_rcf_principal_repayments": cash_available_for_rcf_principal_repayments,
        "rcf_balance_begs": rcf_balance_begs
        
    })


@login_required
def quarterly_financial_statements_tax(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    inputs = Input.objects.get(related_scenario=scenario)

    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    accounting_taxes = []

    profit_before_taxes = []

    asset_value_for_tax_balances_begs = []

    tax_depreciations = []

    cash_taxes = []

    debts = []

    rcfs = []

    interest_deduction_for_taxes = []

    ebitdas = []

    taxable_income_tax_losses_arisings = []

    taxable_incomes = []

    tax_losses_arisings = []
    tax_losses_arisings_absolutes = []

    tax_losses_carried_forwards = []

    tax_losses_utiliseds = []

    taxable_income_net_of_tax_losses_utiliseds = []

    deferred_tax_begs = []

    deferred_taxes = []

    for i in range(len(timelines)):

        timeline = timelines[i]

        accounting_tax = Accounting_tax.objects.get(timeline_event=timeline)
        accounting_taxes.append(accounting_tax)

        profit_before_tax = Profit_before_tax.objects.get(timeline_event=timeline)
        profit_before_taxes.append(profit_before_tax)

        if i == 0:
            asset_value_for_tax_balances_beg = 0
            asset_value_for_tax_balances_begs.append(asset_value_for_tax_balances_beg)

            tax_losses_carried_forward = 0
            tax_losses_carried_forwards.append(tax_losses_carried_forward)

            deferred_tax_beg = 0
            deferred_tax_begs.append(deferred_tax_beg)

        else:
            previous_timeline = timelines[i-1]
            previous_cash_tax = Cash_tax.objects.get(timeline_event=previous_timeline)
            previous_deferred_tax = Deferred_tax.objects.get(timeline_event=previous_timeline)

            asset_value_for_tax_balances_beg = float(previous_cash_tax.asset_value_for_tax_balance)
            asset_value_for_tax_balances_begs.append(asset_value_for_tax_balances_beg)

            tax_losses_carried_forward = float(previous_cash_tax.tax_losses_carried_forward)
            tax_losses_carried_forwards.append(tax_losses_carried_forward)

            deferred_tax_beg = previous_deferred_tax.deferred_tax
            deferred_tax_begs.append(deferred_tax_beg)

        tdr = float(inputs.tax_depreciation_rate)
        last_operating_period_flag = timeline.last_operating_period_flag

        if last_operating_period_flag == 1:
            tax_depreciation = asset_value_for_tax_balances_beg
        else:     
            tax_depreciation = asset_value_for_tax_balances_beg * tdr

        
        tax_depreciations.append(tax_depreciation)

        cash_tax = Cash_tax.objects.get(timeline_event=timeline)
        cash_taxes.append(cash_tax)

        debt = Debt.objects.get(timeline_event=timeline)
        debts.append(debt)

        rcf = Rcf.objects.get(timeline_event=timeline)
        rcfs.append(rcf)

        interest_deduction_for_tax = float(debt.senior_debt_interest) + float(rcf.rcf_interest)
        interest_deduction_for_taxes.append(interest_deduction_for_tax)


        ebitda = Ebitda.objects.get(timeline_event=timeline)
        ebitdas.append(ebitda)  

        taxable_income_tax_losses_arising = float(ebitda.ebitda) - tax_depreciation - interest_deduction_for_tax  
        taxable_income_tax_losses_arisings.append(taxable_income_tax_losses_arising)

        taxable_income = max(0, taxable_income_tax_losses_arising)
        taxable_incomes.append(taxable_income)

        tax_losses_arising = min(0, taxable_income_tax_losses_arising)
        tax_losses_arisings.append(tax_losses_arising)
        tax_losses_arisings_absolutes.append(tax_losses_arising * -1)

        tax_losses_utilised = min(taxable_income, tax_losses_carried_forward)
        tax_losses_utiliseds.append(tax_losses_utilised)

        taxable_income_net_of_tax_losses_utilised = taxable_income - tax_losses_utilised
        taxable_income_net_of_tax_losses_utiliseds.append(taxable_income_net_of_tax_losses_utilised)

        deferred_tax = Deferred_tax.objects.get(timeline_event=timeline)
        deferred_taxes.append(deferred_tax)



        

    return render(request, "financialmodel/tax.html", {
        "scenario": scenario,
        "timelines": timelines,
        "inputs": inputs,
        "accounting_taxes": accounting_taxes,
        "profit_before_taxes": profit_before_taxes,
        "asset_value_for_tax_balances_begs": asset_value_for_tax_balances_begs,
        "tax_depreciations": tax_depreciations,
        "cash_taxes": cash_taxes,
        "debts": debts,
        "rcfs": rcfs,
        "interest_deduction_for_taxes": interest_deduction_for_taxes,
        "ebitdas": ebitdas,
        "taxable_income_tax_losses_arisings": taxable_income_tax_losses_arisings,
        "taxable_incomes": taxable_incomes,
        "tax_losses_arisings": tax_losses_arisings,
        "tax_losses_arisings_absolutes": tax_losses_arisings_absolutes,
        "tax_losses_carried_forwards": tax_losses_carried_forwards,
        "tax_losses_utiliseds": tax_losses_utiliseds,
        "taxable_income_net_of_tax_losses_utiliseds": taxable_income_net_of_tax_losses_utiliseds,
        "deferred_tax_begs": deferred_tax_begs,
        "deferred_taxes": deferred_taxes

    })


@login_required
def quarterly_financial_statements_equity(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    inputs = Input.objects.get(related_scenario=scenario)

    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    share_capital_drawdowns = []

    share_capital_balance_begs = []

    share_capitals = []

    retained_earnings_begs = []

    profit_after_taxes = []

    retained_earningss = []

    retained_cash_balance_begs = []

    cash_flow_available_for_dividends = []

    earnings_available_for_dividends = []

    cash_available_for_dividends = []

    for i in range(len(timelines)):

        if i == 0:
            share_capital_balance_begs.append(0)
            retained_earnings_beg = 0
            retained_earnings_begs.append(retained_earnings_beg)
            retained_cash_balance_beg = 0
            retained_cash_balance_begs.append(retained_cash_balance_beg)

        else:
            previous_timeline = timelines[i-1]

            previous_share_capital = Share_Capital.objects.get(timeline_event=previous_timeline)
            share_capital_balance_beg = previous_share_capital.share_capital
            share_capital_balance_begs.append(share_capital_balance_beg)

            previous_retained_earnings = Retained_earnings.objects.get(timeline_event=previous_timeline)
            retained_earnings_beg = previous_retained_earnings.retained_earnings
            retained_earnings_begs.append(retained_earnings_beg)

            retained_cash_balance_beg = previous_retained_earnings.retained_cash
            retained_cash_balance_begs.append(retained_cash_balance_beg)

        timeline = timelines[i]
        
        share_capital = Share_Capital.objects.get(timeline_event=timeline)
        share_capitals.append(share_capital)

        profit_after_tax = Profit_after_tax.objects.get(timeline_event=timeline)
        profit_after_taxes.append(profit_after_tax)

        retained_earnings = Retained_earnings.objects.get(timeline_event=timeline)
        retained_earningss.append(retained_earnings)

        cash_flow_available_for_dividend = Cash_flow_available_for_dividends.objects.get(timeline_event=timeline)
        cash_flow_available_for_dividends.append(cash_flow_available_for_dividend)

        earnings_available_for_dividend = float(retained_earnings_beg) + float(profit_after_tax.profit_after_tax)
        earnings_available_for_dividends.append(earnings_available_for_dividend)

        cash_available_for_dividend = float(retained_cash_balance_beg) + float(cash_flow_available_for_dividend.cash_flow_available_for_dividends)
        cash_available_for_dividends.append(cash_available_for_dividend)
            

    

    return render(request, "financialmodel/equity.html", {
        "timelines": timelines,
        "inputs": inputs,
        "share_capital_balance_begs": share_capital_balance_begs,
        "share_capitals": share_capitals,
        "retained_earnings_begs": retained_earnings_begs,
        "profit_after_taxes": profit_after_taxes,
        "retained_earningss": retained_earningss,
        "retained_cash_balance_begs": retained_cash_balance_begs,
        "cash_flow_available_for_dividends": cash_flow_available_for_dividends,
        "earnings_available_for_dividends": earnings_available_for_dividends,
        "cash_available_for_dividends": cash_available_for_dividends

    })


@login_required
def irr_detail(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    inputs = Input.objects.get(related_scenario=scenario)

    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    metrics = Metrics.objects.get(related_scenario=scenario)

    retained_earningss = []
    share_capitals = [] 
    share_capital_issueds = []
    cash_flows = []

    for i in range(len(timelines)):

        timeline = timelines[i]

        retained_earnings = Retained_earnings.objects.get(timeline_event=timeline)
        retained_earningss.append(retained_earnings)

        share_capital = Share_Capital.objects.get(timeline_event=timeline)
        share_capitals.append(share_capital)

        solar_asset_book_value = inputs.book_value
        senior_debt_gearing = inputs.senior_debt_gearing
        share_capital_drawdown = float(solar_asset_book_value) * (1 - float(senior_debt_gearing))
        if timeline.finance_close_flag == 1:
            share_capital_issued = share_capital_drawdown
        else:
            share_capital_issued = 0
        share_capital_issueds.append(share_capital_issued)


        dividends_paid = float(retained_earnings.dividends_paid)
        share_capital_redemption = float(share_capital.share_capital_redemption)
        cash_flow = dividends_paid + share_capital_redemption - share_capital_issued
        cash_flows.append(cash_flow)

    return render(request, "financialmodel/irr.html", {
        "scenario": scenario,
        "inputs": inputs,
        "timelines": timelines,
        "metrics": metrics,
        "retained_earningss": retained_earningss,
        "share_capitals": share_capitals,
        "share_capital_issueds": share_capital_issueds,
        "cash_flows": cash_flows
    })


@login_required
def investment_premium(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    inputs = Input.objects.get(related_scenario=scenario)

    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    metrics = Metrics.objects.get(related_scenario=scenario)

    years_since_financial_closes = []

    discount_factors = []

    share_capitals = []

    investment_capitals = []

    retained_earningss = []

    share_of_dividends = []

    share_capital_objects = []

    share_of_redemptions = []

    cash_flows = []

    present_value_cash_flows = []

    

    for i in range(len(timelines)):

        timeline = timelines[i]

        days_in_year = 365
        cumulative_days_since_financial_close = timeline.cumulative_days
        years_since_financial_close = cumulative_days_since_financial_close / days_in_year
        years_since_financial_closes.append(years_since_financial_close)

        target_irr = float(inputs.target_irr)
        financial_close_date_flag = timeline.finance_close_flag
        operating_period_flag = timeline.operating_period_flag
        discount_factor = (1 / (1 + target_irr))**years_since_financial_close * max(financial_close_date_flag, operating_period_flag)
        discount_factors.append(discount_factor)

        
        if timeline.finance_close_flag == 1:
            share_capital = Share_Capital.objects.get(timeline_event=timeline)
            share_capitals.append(float(share_capital.share_capital))


            investment_capital = float(share_capital.share_capital) * float(inputs.share_of_project) * -1
            investment_capitals.append(investment_capital)
        else:
            share_capital = 0
            share_capitals.append(share_capital)
            investment_capital = 0
            investment_capitals.append(investment_capital)


        retained_earnings = Retained_earnings.objects.get(timeline_event=timeline)
        retained_earningss.append(retained_earnings)

        share_of_dividend = float(retained_earnings.dividends_paid) * float(inputs.share_of_project)
        share_of_dividends.append(share_of_dividend)

        share_capital_object = Share_Capital.objects.get(timeline_event=timeline)
        share_capital_objects.append(share_capital_object)

        share_of_redemption = float(share_capital_object.share_capital_redemption) * float(inputs.share_of_project)
        share_of_redemptions.append(share_of_redemption)

        cash_flow = investment_capital + share_of_dividend + share_of_redemption
        cash_flows.append(cash_flow)

        present_value_cash_flow = cash_flow * discount_factor
        present_value_cash_flows.append(present_value_cash_flow)


            



    return render(request, "financialmodel/investmentpremium.html", {
        "scenario": scenario,
        "inputs": inputs,
        "timelines": timelines,
        "metrics": metrics,
        "discount_factors": discount_factors,
        "days_in_year": days_in_year,
        "years_since_financial_closes": years_since_financial_closes,
        "share_capitals": share_capitals,
        "investment_capitals": investment_capitals,
        "retained_earningss": retained_earningss,
        "share_of_dividends": share_of_dividends,
        "share_capital_objects": share_capital_objects,
        "share_of_redemptions": share_of_redemptions,
        "cash_flows": cash_flows,
        "present_value_cash_flows": present_value_cash_flows

    })

@login_required
def dscr(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })

    inputs = Input.objects.get(related_scenario=scenario)

    timelines = Timeline.objects.all().filter(related_scenario=scenario)

    metrics = Metrics.objects.get(related_scenario=scenario)

    debts = []

    senior_debt_services = []

    cash_flow_available_for_senior_debts = []

    senior_debt_service_coverage_ratio_array = []
    
    for i in range(len(timelines)):
        timeline = timelines[i]

        debt = Debt.objects.get(timeline_event=timeline)
        debts.append(debt)

        senior_debt_service = float(debt.senior_debt_repayment) + float(debt.senior_debt_interest)
        senior_debt_services.append(senior_debt_service)

        cash_flow_available_for_senior_debt = Cash_flow_available_for_senior_debt.objects.get(timeline_event=timeline)
        cash_flow_available_for_senior_debts.append(cash_flow_available_for_senior_debt)

        if senior_debt_service != 0:
            ratio = float(cash_flow_available_for_senior_debt.cash_flow_available_for_senior_debt) / senior_debt_service
            senior_debt_service_coverage_ratio_array.append(ratio)
        else:
            senior_debt_service_coverage_ratio_array.append("N/A")







    return render(request, "financialmodel/dscr.html", {
        "scenario": scenario,
        "inputs": inputs,
        "timelines": timelines,
        "metrics": metrics,
        "debts": debts,
        "senior_debt_services": senior_debt_services,
        "cash_flow_available_for_senior_debts": cash_flow_available_for_senior_debts,
        "senior_debt_service_coverage_ratio_array": senior_debt_service_coverage_ratio_array

    })


@login_required
def updatescenario(request, id):

    try:
        scenario = Scenario.objects.get(pk=id)
    except Scenario.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Scenario does not exist"
        })
    
    inputs = Input.objects.get(related_scenario=scenario)

    if request.method == "POST":

        form = UpdateScenarioForm(request.POST)

        if form.is_valid():

            scenario_name = request.POST["scenario_name"]
            scenario_number = request.POST["scenario_number"]

            scenario.scenario_name = scenario_name
            scenario.scenario_number = scenario_number
            

            first_date_of_time_rulers = str(request.POST["first_date_of_time_rulers"])
            first_date_of_time_rulers = datefunction(first_date_of_time_rulers)

            end_of_first_operating_period = str(request.POST["end_of_first_operating_period"])
            end_of_first_operating_period = datefunction(end_of_first_operating_period)

            acquisition_date = str(request.POST["acquisition_date"])
            acquisition_date = datefunction(acquisition_date)

            validation_one = acquisition_date - end_of_first_operating_period

            if int(validation_one.days) < 0:
                return render(request, "financialmodel/error.html", {
                    "error": "Acquisition Date must be after the start of the model date."
                })

            length_of_contract = int(request.POST["length_of_contract"])

            q1_sa = float(request.POST["q1_sa"]) / 100
            q2_sa = float(request.POST["q2_sa"]) / 100
            q3_sa = float(request.POST["q3_sa"]) / 100
            q4_sa = float(request.POST["q4_sa"]) / 100

            if q1_sa + q2_sa + q3_sa + q4_sa != 1:
                return render(request, "financialmodel/error.html", {
                    "error": "Seasonality must add up to 100"
                })

            annual_degredation = float(request.POST["annual_degredation"]) / 100
            year_1_p50_production = float(request.POST["year_1_p50_production"])
            availability = float(request.POST["availability"]) / 100
            power_tarrif = float(request.POST["power_tarrif"])
            annual_om_cost = float(request.POST["annual_om_cost"])
            cpi_at_close = float(request.POST["cpi_at_close"])
            cpi_sign_date = float(request.POST["cpi_sign_date"])
            cpi_growth_rate = float(request.POST["cpi_growth_rate"]) / 100
            senior_debt_gearing = float(request.POST["senior_debt_gearing"]) / 100
            senior_debt_day_convention = int(request.POST["senior_debt_day_convention"])
            senior_debt_swap_rate = float(request.POST["senior_debt_swap_rate"]) / 100
            senior_debt_int_margin = float(request.POST["senior_debt_int_margin"]) / 100
            repayment_term = int(float(request.POST["repayment_term"]))

            if repayment_term > length_of_contract:
                return render(request, "financialmodel/error.html", {
                    "error": "length of debt should not exceed the length of the project"
                })
            

            rcf_interest_rate = float(request.POST["rcf_interest_rate"]) / 100
            rcf_innit = float(request.POST["rcf_innit"])
            share_of_project = float(request.POST["share_of_project"]) / 100
            target_irr = float(request.POST["target_irr"]) / 100
            accounts_receivable_days = int(float(request.POST["accounts_receivable_days"]))
            accounts_payable_days = int(float(request.POST["accounts_payable_days"]))
            useful_life = int(float(request.POST["useful_life"]))
            book_value = float(request.POST["book_value"])
            retained_cash_innit = float(request.POST["retained_cash_innit"])
            accounts_recievable_innit = float(request.POST["accounts_recievable_innit"])
            accounts_payable_innit = float(request.POST["accounts_payable_innit"])
            retained_earnings_innit = float(request.POST["retained_earnings_innit"])
            deffered_tax_innit = float(request.POST["deffered_tax_innit"])
            tax_rate = float(request.POST["tax_rate"]) / 100
            tax_depreciation_rate = float(request.POST["tax_depreciation_rate"]) / 100
            tax_losses_carried_forward_innit = float(request.POST["tax_losses_carried_forward_innit"])

            inputs.first_date_of_time_rulers = first_date_of_time_rulers
            inputs.end_of_first_operating_period = end_of_first_operating_period
            inputs.acquisition_date = acquisition_date
            inputs.length_of_contract = length_of_contract
            inputs.q1_sa = q1_sa
            inputs.q2_sa = q2_sa
            inputs.q3_sa = q3_sa
            inputs.q4_sa = q4_sa
            inputs.annual_degredation = annual_degredation
            inputs.year_1_p50_production = year_1_p50_production
            inputs.availability = availability
            inputs.power_tarrif = power_tarrif
            inputs.annual_om_cost = annual_om_cost
            inputs.cpi_at_close = cpi_at_close
            inputs.cpi_sign_date = cpi_sign_date
            inputs.cpi_growth_rate = cpi_growth_rate
            inputs.senior_debt_gearing = senior_debt_gearing
            inputs.senior_debt_day_convention = senior_debt_day_convention
            inputs.senior_debt_swap_rate = senior_debt_swap_rate
            inputs.senior_debt_int_margin = senior_debt_int_margin
            inputs.repayment_term = repayment_term
            inputs.rcf_interest_rate = rcf_interest_rate
            inputs.rcf_innit = rcf_innit
            inputs.share_of_project = share_of_project
            inputs.target_irr = target_irr
            inputs.accounts_receivable_days = accounts_receivable_days
            inputs.accounts_payable_days = accounts_payable_days
            inputs.useful_life = useful_life
            inputs.book_value = book_value
            inputs.retained_cash_innit = retained_cash_innit
            inputs.accounts_recievable_innit = accounts_recievable_innit
            inputs.accounts_payable_innit = accounts_payable_innit
            inputs.retained_earnings_innit = retained_earnings_innit
            inputs.deffered_tax_innit = deffered_tax_innit
            inputs.tax_rate = tax_rate
            inputs.tax_depreciation_rate = tax_depreciation_rate
            inputs.tax_losses_carried_forward_innit = tax_losses_carried_forward_innit

            scenario.save()
            inputs.save()

            calculate(inputs, "update")

            return render(request, "financialmodel/index.html")


    else:

        form = UpdateScenarioForm(initial={
            "scenario_name": scenario.scenario_name,
            "scenario_number": scenario.scenario_number,
            "first_date_of_time_rulers": inputs.first_date_of_time_rulers,
            "end_of_first_operating_period": inputs.end_of_first_operating_period,
            "acquisition_date": inputs.acquisition_date,
            "length_of_contract": inputs.length_of_contract,
            "q1_sa": (inputs.q1_sa * 100),
            "q2_sa": (inputs.q2_sa*100),
            "q3_sa": (inputs.q3_sa * 100),
            "q4_sa": (inputs.q4_sa*100),
            "annual_degredation": (inputs.annual_degredation * 100),
            "year_1_p50_production": inputs.year_1_p50_production,
            "availability": (inputs.availability*100),
            "power_tarrif": inputs.power_tarrif,
            "annual_om_cost": inputs.annual_om_cost,
            "cpi_at_close": inputs.cpi_at_close,
            "cpi_sign_date": inputs.cpi_sign_date,
            "cpi_growth_rate": (inputs.cpi_growth_rate*100),
            "senior_debt_gearing": (inputs.senior_debt_gearing*100),
            "senior_debt_day_convention": inputs.senior_debt_day_convention,
            "senior_debt_swap_rate": (inputs.senior_debt_swap_rate*100),
            "senior_debt_int_margin": (inputs.senior_debt_int_margin*100),
            "repayment_term": inputs.repayment_term,
            "rcf_interest_rate": (inputs.rcf_interest_rate * 100),
            "rcf_innit": inputs.rcf_innit,
            "share_of_project": (inputs.share_of_project*100),
            "target_irr": (inputs.target_irr*100),
            "accounts_receivable_days": inputs.accounts_receivable_days,
            "accounts_payable_days": inputs.accounts_payable_days,
            "useful_life": inputs.useful_life,
            "book_value": inputs.book_value,
            "retained_cash_innit": inputs.retained_cash_innit,
            "accounts_recievable_innit": inputs.accounts_recievable_innit,
            "accounts_payable_innit": inputs.accounts_payable_innit,
            "retained_earnings_innit": inputs.retained_earnings_innit,
            "deffered_tax_innit": inputs.deffered_tax_innit,
            "tax_rate": (inputs.tax_rate*100),
            "tax_depreciation_rate": (inputs.tax_depreciation_rate*100),
            "tax_losses_carried_forward_innit": inputs.tax_losses_carried_forward_innit

        })

        return render(request, "financialmodel/update.html", {
            "form": form,
            "scenario": scenario
        })
    

@login_required
def project_comparison(request, id):

    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        return render(request, "financialmodel/error.html", {
            "error": "Project does not exist"
        })

    scenarios = Scenario.objects.all().filter(related_project=project)

    metrics = []

    revenues = []

    expenses = []

    ebitdas = []

    depreciations = []

    ebits = []

    senior_debt_interests = []

    rcf_interests = []

    profit_before_taxes = []

    corporate_income_taxes = []

    profit_after_taxes = []

    cash_received_from_invoices = []

    cash_paid_for_expenses = []

    taxes_paid = []

    cash_flow_available_for_senior_debts = []

    senior_debt_principal_repayments = []

    cash_flow_available_for_refinancing_facilities = []

    rcf_drawdowns = []

    rcf_principal_repayments = []

    rcf_interest_paids = []

    cash_flow_available_for_shareholders = []

    share_capital_redemptions = []

    cash_flow_available_for_dividends = []

    dividends_paids = []

    net_cash_flows = []

    for i in range(len(scenarios)):

        scenario = scenarios[i]

        metric = Metrics.objects.get(related_scenario=scenario)
        metrics.append(metric)

        timelines = Timeline.objects.all().filter(related_scenario=scenario)

        revenue = 0
        expense = 0
        ebitda = 0
        depreciation = 0
        ebit = 0
        senior_debt_interest = 0
        rcf_interest = 0
        profit_before_tax = 0
        corporate_income_tax = 0
        profit_after_tax = 0
        cash_received_from_invoice = 0
        cash_paid_for_expense = 0
        tax_paid = 0
        cash_flow_available_for_senior_debt = 0
        senior_debt_principal_repayment = 0
        cash_flow_available_for_refinancing_facility = 0
        rcf_drawdown = 0
        rcf_principal_repayment = 0
        rcf_interest_paid = 0
        cash_flow_available_for_shareholder = 0
        share_capital_redemption = 0
        cash_flow_available_for_dividend = 0
        dividends_paid = 0
        net_cash_flow = 0

        for j in range(len(timelines)):

            timeline = timelines[j]

            revenue_object = Revenue.objects.get(timeline_event=timeline)
            revenue += revenue_object.revenue

            expense_object = Expense.objects.get(timeline_event=timeline)
            expense += expense_object.expense

            ebitda_object = Ebitda.objects.get(timeline_event=timeline)
            ebitda += ebitda_object.ebitda

            depreciation_object = Depreciation.objects.get(timeline_event=timeline)
            depreciation += depreciation_object.depreciation

            ebit_object = Ebit.objects.get(timeline_event=timeline)
            ebit += ebit_object.ebit

            debt_object = Debt.objects.get(timeline_event=timeline)
            senior_debt_interest += debt_object.senior_debt_interest

            rcf_object = Rcf.objects.get(timeline_event=timeline)
            rcf_interest += rcf_object.rcf_interest

            profit_before_tax_object = Profit_before_tax.objects.get(timeline_event=timeline)
            profit_before_tax += profit_before_tax_object.profit_before_tax

            accounting_tax_object = Accounting_tax.objects.get(timeline_event=timeline)
            corporate_income_tax += accounting_tax_object.tax_expense

            profit_after_tax_object = Profit_after_tax.objects.get(timeline_event=timeline)
            profit_after_tax += profit_after_tax_object.profit_after_tax

            cash_received_from_invoice += revenue_object.cash_received_from_invoices

            cash_paid_for_expense += expense_object.cash_paid_for_expense

            cash_tax_object = Cash_tax.objects.get(timeline_event=timeline)
            tax_paid += cash_tax_object.corporate_income_tax_paid

            cash_flow_available_for_senior_debt_object = Cash_flow_available_for_senior_debt.objects.get(timeline_event=timeline)
            cash_flow_available_for_senior_debt += cash_flow_available_for_senior_debt_object.cash_flow_available_for_senior_debt

            senior_debt_principal_repayment += debt_object.senior_debt_repayment

            cash_flow_available_for_refinancing_facilities_object = Cash_flow_available_for_refinancing_facility.objects.get(timeline_event=timeline)
            cash_flow_available_for_refinancing_facility += cash_flow_available_for_refinancing_facilities_object.cash_flow_available_for_refinancing_facility

            rcf_drawdown += rcf_object.rcf_drawdown

            rcf_principal_repayment += rcf_object.rcf_principal_repayment

            rcf_interest_paid += rcf_object.rcf_interest_paid

            cash_flow_available_for_shareholders_object = Cash_flow_available_for_shareholders.objects.get(timeline_event=timeline)
            cash_flow_available_for_shareholder += cash_flow_available_for_shareholders_object.cash_flow_available_for_shareholders

            share_capital_object = Share_Capital.objects.get(timeline_event=timeline)
            share_capital_redemption += share_capital_object.share_capital_redemption

            cash_flow_available_for_dividend_object = Cash_flow_available_for_dividends.objects.get(timeline_event=timeline)
            cash_flow_available_for_dividend += cash_flow_available_for_dividend_object.cash_flow_available_for_dividends

            retained_earnings_object = Retained_earnings.objects.get(timeline_event=timeline)
            dividends_paid += retained_earnings_object.dividends_paid

            net_cash_flow_object = Net_cash_flow.objects.get(timeline_event=timeline)
            net_cash_flow += net_cash_flow_object.net_cash_flow

            



        
        revenues.append(revenue)
        expenses.append(expense)
        ebitdas.append(ebitda)
        depreciations.append(depreciation)
        ebits.append(ebit)
        senior_debt_interests.append(senior_debt_interest)
        rcf_interests.append(rcf_interest)
        profit_before_taxes.append(profit_before_tax)
        corporate_income_taxes.append(corporate_income_tax)
        profit_after_taxes.append(profit_after_tax)
        cash_received_from_invoices.append(cash_received_from_invoice)
        cash_paid_for_expenses.append(cash_paid_for_expense)
        taxes_paid.append(tax_paid)
        cash_flow_available_for_senior_debts.append(cash_flow_available_for_senior_debt)
        senior_debt_principal_repayments.append(senior_debt_principal_repayment)
        cash_flow_available_for_refinancing_facilities.append(cash_flow_available_for_refinancing_facility)
        rcf_drawdowns.append(rcf_drawdown)
        rcf_principal_repayments.append(rcf_principal_repayment)
        rcf_interest_paids.append(rcf_interest_paid)
        cash_flow_available_for_shareholders.append(cash_flow_available_for_shareholder)
        share_capital_redemptions.append(share_capital_redemption)
        cash_flow_available_for_dividends.append(cash_flow_available_for_dividend)
        dividends_paids.append(dividends_paid)
        net_cash_flows.append(net_cash_flow)


    return render(request, "financialmodel/project_comparison.html", {
        "scenarios": scenarios,
        "metrics": metrics,
        "revenues": revenues,
        "expenses": expenses,
        "ebitdas": ebitdas,
        "depreciations": depreciations,
        "ebits": ebits,
        "senior_debt_interests": senior_debt_interests,
        "rcf_interests": rcf_interests,
        "profit_before_taxes": profit_before_taxes,
        "corporate_income_taxes": corporate_income_taxes,
        "profit_after_taxes": profit_after_taxes,
        "cash_received_from_invoices": cash_received_from_invoices,
        "cash_paid_for_expenses": cash_paid_for_expenses,
        "taxes_paid": taxes_paid,
        "cash_flow_available_for_senior_debt_services": cash_flow_available_for_senior_debts,
        "senior_debt_principal_repayments": senior_debt_principal_repayments,
        "cash_flow_available_for_refinancing_facilities": cash_flow_available_for_refinancing_facilities,
        "rcf_drawdowns": rcf_drawdowns,
        "rcf_principal_repayments": rcf_principal_repayments,
        "rcf_interest_paids": rcf_interest_paids,
        "cash_flow_available_for_shareholders": cash_flow_available_for_shareholders,
        "share_capital_redemptions": share_capital_redemptions,
        "cash_flow_available_for_dividends": cash_flow_available_for_dividends,
        "dividends_paids": dividends_paids,
        "net_cash_flows": net_cash_flows
    })








def datefunction(date_variable):
    datelist = date_variable.split("-")
    year = datelist[0]
    # print(int(year))
    month = datelist[1]
    # print(int(month))
    day = datelist[2]
    # print(int(day))

    return datetime.datetime(int(year), int(month), int(day))
