from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField()

    def __str__(self):
        return f"{self.owner}, {self.name}"
    
    def serialise(self):
        return {
            "Project_id": self.id,
            "Project_owner": self.owner.id
        }
    
class Scenario(models.Model):
    related_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    scenario_name = models.CharField()
    scenario_number = models.IntegerField()

    def __str__(self):
        return f"{self.id}, {self.related_project}, {self.scenario_number}"
    
    def serialise(self):
        return {
            "scenario_id": self.id,
            "related_project": self.related_project.id,
            "scenario_number": self.scenario_number
        }

class Input(models.Model):
    related_scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, null=True)
    first_date_of_time_rulers = models.DateField() 
    end_of_first_operating_period = models.DateField() 
    acquisition_date = models.DateField() 
    length_of_contract = models.IntegerField()
    q1_sa = models.DecimalField(max_digits=10, decimal_places=8)
    q2_sa = models.DecimalField(max_digits=10, decimal_places=8)
    q3_sa = models.DecimalField(max_digits=10, decimal_places=8)
    q4_sa = models.DecimalField(max_digits=10, decimal_places=8)
    annual_degredation = models.DecimalField(max_digits=10, decimal_places=8)
    year_1_p50_production =  models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.DecimalField(max_digits=10, decimal_places=8)
    power_tarrif = models.DecimalField(max_digits=10, decimal_places=8)
    annual_om_cost = models.DecimalField(max_digits=10, decimal_places=2)
    cpi_at_close = models.DecimalField(max_digits=10, decimal_places=2)
    cpi_sign_date = models.DecimalField(max_digits=10, decimal_places=2)
    cpi_growth_rate = models.DecimalField(max_digits=10, decimal_places=8)
    senior_debt_gearing = models.DecimalField(max_digits=10, decimal_places=8)
    senior_debt_day_convention = models.IntegerField()
    senior_debt_swap_rate = models.DecimalField(max_digits=10, decimal_places=8)
    senior_debt_int_margin = models.DecimalField(max_digits=10, decimal_places=8)
    repayment_term = models.DecimalField(max_digits=10, decimal_places=2)
    rcf_interest_rate = models.DecimalField(max_digits=10, decimal_places=8)
    rcf_innit = models.DecimalField(max_digits=10, decimal_places=2)
    share_of_project = models.DecimalField(max_digits=10, decimal_places=8)
    target_irr =  models.DecimalField(max_digits=10, decimal_places=8)
    accounts_receivable_days =  models.DecimalField(max_digits=10, decimal_places=2)
    accounts_payable_days = models.IntegerField()
    useful_life = models.IntegerField()
    book_value = models.DecimalField(max_digits=10, decimal_places=2)
    retained_cash_innit = models.DecimalField(max_digits=10, decimal_places=2)
    accounts_recievable_innit = models.DecimalField(max_digits=10, decimal_places=2)
    accounts_payable_innit = models.DecimalField(max_digits=10, decimal_places=2)
    retained_earnings_innit = models.DecimalField(max_digits=10, decimal_places=2)
    deffered_tax_innit = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=10, decimal_places=8)
    tax_depreciation_rate = models.DecimalField(max_digits=10, decimal_places=8)
    tax_losses_carried_forward_innit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.related_scenario}, {self.first_date_of_time_rulers}, {self.end_of_first_operating_period}, {self.acquisition_date}, {self.length_of_contract}, {self.q1_sa}, {self.q2_sa}, {self.q3_sa}, {self.q4_sa}, {self.annual_degredation}, {self.year_1_p50_production}, {self.availability}, {self.power_tarrif}, {self.annual_om_cost}, {self.cpi_at_close}, {self.cpi_sign_date}, {self.cpi_growth_rate}, {self.senior_debt_gearing}, {self.senior_debt_day_convention}, {self.senior_debt_swap_rate}, {self.senior_debt_int_margin}, {self.repayment_term}, {self.rcf_interest_rate}, {self.rcf_innit}, {self.share_of_project}, {self.target_irr}, {self.accounts_receivable_days}, {self.accounts_payable_days}, {self.useful_life}, {self.book_value}, {self.retained_cash_innit}, {self.accounts_recievable_innit}, {self.accounts_payable_innit}, {self.retained_earnings_innit}, {self.deffered_tax_innit}, {self.tax_rate}, {self.tax_depreciation_rate}, {self.tax_losses_carried_forward_innit} "
    
    def serialise(self):
        return {
            "id": self.id,
            "related_scenario": self.related_scenario,
            "first_date_of_time_rulers": self.first_date_of_time_rulers,
            "end_of_first_operating_period" : self.end_of_first_operating_period ,
            "acquisition_date": self.acquisition_date,
            "length_of_contract": self.length_of_contract,
            "q1_sa": self.q1_sa,
            "q2_sa": self.q2_sa,
            "q3_sa": self.q3_sa,
            "q4_sa": self.q4_sa,
            "annual_degredation": self.annual_degredation,
            "year_1_p50_production": self.year_1_p50_production,
            "availability": self.availability,
            "power_tarrif": self.power_tarrif,
            "annual_om_cost": self.annual_om_cost,
            "cpi_at_close": self.cpi_at_close,
            "cpi_sign_date": self.cpi_sign_date,
            "cpi_growth_rate": self.cpi_growth_rate,
            "senior_debt_gearing": self.senior_debt_gearing,
            "senior_debt_day_convention": self.senior_debt_day_convention,
            "senior_debt_swap_rate": self.senior_debt_swap_rate,
            "senior_debt_int_margin": self.senior_debt_int_margin,
            "repayment_term": self.repayment_term,
            "rcf_interest_rate": self.rcf_interest_rate,
            "rcf_innit": self.rcf_innit,
            "share_of_project": self.share_of_project,
            "target_irr": self.target_irr,
            "accounts_receivable_days": self.accounts_receivable_days,
            "accounts_payable_days": self.accounts_payable_days,
            "useful_life": self.useful_life,
            "book_value": self.book_value,
            "retained_cash_innit": self.retained_cash_innit,
            "accounts_recievable_innit": self.accounts_recievable_innit,
            "accounts_payable_innit": self.accounts_payable_innit,
            "retained_earnings_innit": self.retained_earnings_innit,
            "deffered_tax_innit": self.deffered_tax_innit,
            "tax_rate": self.tax_rate,
            "tax_depreciation_rate": self.tax_depreciation_rate,
            "tax_losses_carried_forward_innit": self.tax_losses_carried_forward_innit

        }
    
class Timeline(models.Model):
    related_scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, null=True)
    index = models.IntegerField()
    date = models.DateField()
    operating_period_flag = models.IntegerField()
    contract_year_number = models.IntegerField()
    period_number = models.IntegerField()
    escalation_flag = models.IntegerField()
    useful_life_flag = models.IntegerField()
    last_operating_period_flag = models.IntegerField()
    finance_close_flag = models.IntegerField()
    senior_debt_repayment_flag = models.IntegerField()
    days_in_period = models.IntegerField()
    cumulative_days = models.IntegerField()

    def serialise(self):
        return {
            "id": self.id,
            "related_scenario_id": self.related_scenario.id,
            "operating_period_flag": self.operating_period_flag,
            "contract_year_number": self.contract_year_number,
            "period number": self.period_number,
            "escalation_flag": self.escalation_flag,
            "useful_life_flag": self.useful_life_flag,
            "last operating period flag": self.last_operating_period_flag,
            "finance_close_flag": self.finance_close_flag,
            "senior_debt_repayment_flag": self.senior_debt_repayment_flag,
            "days_in_period": self.days_in_period,
            "cumulative days": self.cumulative_days
        }


class Revenue(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    revenue = models.DecimalField(max_digits=20, decimal_places=8)
    cash_received_from_invoices = models.DecimalField(max_digits=20, decimal_places=8)
    accounts_receivable = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "revenue": self.revenue,
            "cash_received_from_invoices": self.cash_received_from_invoices,
            "accounts_receivable": self.accounts_receivable
        }

class Expense(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    cpi = models.DecimalField(max_digits=15, decimal_places=8)
    escalation_factor = models.DecimalField(max_digits=10, decimal_places=8)
    expense = models.DecimalField(max_digits=20, decimal_places=8)
    cash_paid_for_expense = models.DecimalField(max_digits=20, decimal_places=8)
    accounts_payable = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "cpi": self.cpi,
            "escalation_factor": self.escalation_factor,
            "expense": self.expense,
            "cash_paid_for_expense": self.cash_paid_for_expense,
            "accounts_payable": self.accounts_payable
        }
    
class Depreciation(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    depreciation = models.DecimalField(max_digits=20, decimal_places=8)
    solar_asset_value = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "depreciation": self.depreciation,
            "solar_asset_value": self.solar_asset_value
        }
    

class Share_Capital(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    share_capital = models.DecimalField(max_digits=20, decimal_places=8)
    share_capital_redemption = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "share_capital": self.share_capital,
            "share_capital_redemption": self.share_capital_redemption
        }
    
class Retained_earnings(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    dividends_paid = models.DecimalField(max_digits=20, decimal_places=8)
    retained_earnings = models.DecimalField(max_digits=20, decimal_places=8)
    retained_cash = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "dividends_paid": self.dividends_paid,
            "retained_earnings": self.retained_earnings,
            "retained_cash": self.retained_cash
        }


class Debt(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    senior_debt = models.DecimalField(max_digits=20, decimal_places=8)
    senior_debt_repayment = models.DecimalField(max_digits=20, decimal_places=8)
    senior_debt_interest = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "senior_debt": self.senior_debt,
            "senior_debt_repayment": self.senior_debt_repayment,
            "senior_debt_interest": self.senior_debt_interest
        }
    

class Rcf(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    rcf_drawdown = models.DecimalField(max_digits=20, decimal_places=8)
    rcf_interest = models.DecimalField(max_digits=20, decimal_places=8)
    rcf_interest_paid = models.DecimalField(max_digits=20, decimal_places=8)
    rcf_principal_repayment = models.DecimalField(max_digits=20, decimal_places=8)
    rcf_balance = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "rcf_drawdown": self.rcf_drawdown,
            "rcf_interest": self.rcf_interest,
            "rcf_interest_paid": self.rcf_interest_paid,
            "rcf_principal_repayment": self.rcf_principal_repayment,
            "rcf_balance": self.rcf_balance
        }
    

class Accounting_tax(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    tax_expense = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "tax_expense": self.tax_expense
        }

class Cash_tax(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    asset_value_for_tax_balance = models.DecimalField(max_digits=20, decimal_places=8)
    corporate_income_tax_paid = models.DecimalField(max_digits=20, decimal_places=8)
    tax_losses_carried_forward = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "asset_value_for_tax_balance": self.asset_value_for_tax_balance,
            "corporate_income_tax_paid": self.corporate_income_tax_paid,
            "tax_losses_carried_forward": self.tax_losses_carried_forward
        }
    
class Deferred_tax(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    deferred_tax = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "deferred_tax": self.deferred_tax
        }
    
class Ebitda(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    ebitda = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "ebitda": self.ebitda

        }
    
class Ebit(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    ebit = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "ebit": self.ebit
        }
    
class Profit_before_tax(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    profit_before_tax = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "profit_before_tax": self.profit_before_tax
        }
    
class Profit_after_tax(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    profit_after_tax = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "profit_after_tax": self.profit_after_tax

        }
    
class Cash_flow_available_for_senior_debt(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    cash_flow_available_for_senior_debt = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "cash_flow_available_for_senior_debt": self.cash_flow_available_for_senior_debt
        }
    

class Cash_flow_available_for_refinancing_facility(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    cash_flow_available_for_refinancing_facility = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "cash_flow_available_for_refinancing_facility": self.cash_flow_available_for_refinancing_facility
        }
    

class Cash_flow_available_for_rcf(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    cash_flow_available_for_rcf = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "cash_flow_available_for_rcf": self.cash_flow_available_for_rcf
        }
class Cash_flow_available_for_shareholders(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    cash_flow_available_for_shareholders = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "cash_flow_available_for_shareholders": self.cash_flow_available_for_shareholders
        }
    
class Cash_flow_available_for_dividends(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    cash_flow_available_for_dividends = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "cash_flow_available_for_dividends": self.cash_flow_available_for_dividends
        }
    
class Net_cash_flow(models.Model):
    timeline_event = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    net_cash_flow = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "timeline_id": self.timeline_event.id,
            "date": self.timeline_event.date,
            "net_cash_flow": self.net_cash_flow

        }
    
class Metrics(models.Model):
    related_scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, null=True)
    irr = models.DecimalField(max_digits=20, decimal_places=8)
    min_dscr = models.DecimalField(max_digits=20, decimal_places=8)
    avg_dscr = models.DecimalField(max_digits=20, decimal_places=8)
    investment_premium = models.DecimalField(max_digits=20, decimal_places=8)

    def serialise(self):
        return {
            "id": self.id,
            "project_id": self.related_scenario.related_project.id,
            "scenario": self.related_scenario,
            "irr": self.irr,
            "min_dscr": self.min_dscr,
            "avg_dscr": self.avg_dscr,
            "investment_premium": self.investment_premium
        }


