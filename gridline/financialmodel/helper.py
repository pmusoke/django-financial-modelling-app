import calendar
import datetime
import decimal

from .models import *

from pyxirr import xirr

import numpy_financial as npf


def calculate(input, action):

    # first_date_of_time_rulers = input.first_date_of_time_rulers

    # print(f"helper function is working, first_date_of_time_rulers: {first_date_of_time_rulers}")

    # end_of_first_operating_period = input.end_of_first_operating_period

    # acquisition_date = input.acquisition_date

    generate_timeline(action, input.first_date_of_time_rulers, input.acquisition_date, input.length_of_contract, input.repayment_term, input.useful_life, input.related_scenario)

    timelines = Timeline.objects.all().filter(related_scenario = input.related_scenario)

    # print(timelines[8])

    for i in range(len(timelines)):

        timeline = timelines[i]

        if i == 0:
            previous_timeline = 0
        else:
            previous_timeline = timelines[i - 1]

        calculate_revenue(action, i, input.q1_sa, input.q2_sa, input.q3_sa, input.q4_sa, input.annual_degredation, input.year_1_p50_production, input.availability, input.power_tarrif, input.accounts_recievable_innit, input.accounts_receivable_days ,timeline, previous_timeline)

        calculate_expense(action, i, input.annual_om_cost, input.cpi_at_close, input.cpi_growth_rate, input.cpi_sign_date, input.accounts_payable_innit, input.accounts_payable_days, timeline, previous_timeline)

        calculate_ebitda(action, timeline)

        calculate_depreciation(action, i, input.book_value, input.useful_life, timeline, previous_timeline)

        calculate_ebit(action, timeline)

        calculate_share_capital(action, i, input.book_value, input.senior_debt_gearing, timeline, previous_timeline)

        calculate_debt(action, i, input.senior_debt_gearing, input.book_value, input.repayment_term, input.senior_debt_swap_rate, input.senior_debt_int_margin, input.senior_debt_day_convention, timeline, previous_timeline)

        calculate_cash_tax(action, i, input.tax_rate, input.book_value, input.tax_depreciation_rate, input.rcf_interest_rate, input.senior_debt_day_convention, input.tax_losses_carried_forward_innit, timeline, previous_timeline)

        calculate_rcf(action, i, input.rcf_interest_rate, input.senior_debt_day_convention, input.rcf_innit, timeline, previous_timeline)

        calculate_profit_before_tax(action, timeline)

        calculate_accounting_tax(action, i, input.tax_rate, timeline)

        calculate_profit_after_tax(action, timeline)

        calculate_deferred_tax_balance(action, i, timeline, previous_timeline)



        calculate_cash_flow_available_for_senior_debt_service(action, timeline)

        calculate_cash_flow_available_for_refinancing_facility(action, timeline)

        calculate_cash_flow_available_for_rcf(action, timeline)

        calculate_cash_flow_available_for_shareholders(action, timeline)

        calculate_cash_flow_available_for_dividends(action, timeline)

        calculate_retained_earnings(action, i, input.retained_cash_innit, timeline, previous_timeline)

        calculate_net_cash_flow(action, timeline)

    cash_flows = []
    dates = []

    for i in range(len(timelines)):

        timeline = timelines[i]

        retained_earnings = Retained_earnings.objects.get(timeline_event=timeline)
        dividends_paid = retained_earnings.dividends_paid

        finance_close_flag = timeline.finance_close_flag

        if finance_close_flag == 1:
            s_capital = Share_Capital.objects.get(timeline_event=timeline)
            share_capital_issued = -1 * s_capital.share_capital
        else:
            share_capital_issued = 0

        share_capital = Share_Capital.objects.get(timeline_event=timeline)
        share_capital_redemption = share_capital.share_capital_redemption

        cash_flow = (float(dividends_paid) + float(share_capital_redemption) + float(share_capital_issued))


        date = timeline.date

        year = date.year
        month = date.month
        day = calendar.monthrange(year, month)[1] 

        cash_flows.append(cash_flow)
        dates.append(datetime.date(year, month, day))

    # irr_value = npf.irr(cash_flows)
    rate = xirr(dates, cash_flows)

    senior_debt_service_coverage_ratio_array = []

    for i in range(len(timelines)):

        timeline = timelines[i]

        debt = Debt.objects.get(timeline_event=timeline)

        principle_repayment = debt.senior_debt_repayment
        interest = debt.senior_debt_interest

        senior_debt_service = principle_repayment + interest

        cash_flow_available_for_senior_debt = Cash_flow_available_for_senior_debt.objects.get(timeline_event=timeline)

        if senior_debt_service != 0:

            ratio = float(cash_flow_available_for_senior_debt.cash_flow_available_for_senior_debt) / float(senior_debt_service)
            senior_debt_service_coverage_ratio_array.append(ratio)

    min_dscr = min(senior_debt_service_coverage_ratio_array)
    avg_dscr = sum(senior_debt_service_coverage_ratio_array) / len(senior_debt_service_coverage_ratio_array)

    premium = 0
    for i in range(len(timelines)):

        timeline = timelines[i]

        cash_flow = calculate_investment_premium(i, input.target_irr, input.share_of_project, timeline)
        premium = premium + cash_flow

    if action == "create":
        metrics = Metrics.objects.create(
            related_scenario = input.related_scenario,
            irr = rate,
            min_dscr = min_dscr,
            avg_dscr = avg_dscr,
            investment_premium = premium
        )
        metrics.save()

    elif action == "update":
        metrics = Metrics.objects.get(related_scenario=input.related_scenario)

        metrics.irr = rate
        metrics.min_dscr = min_dscr
        metrics.avg_dscr = avg_dscr
        metrics.investment_premium = premium
        metrics.save()





def generate_timeline(action, first_date_of_time_rulers, acq_date, loc, lod, loul, relevant_scenario):
    x = first_date_of_time_rulers

    month = x.month

    year = x.year

    day = x.day

    last_day = calendar.monthrange(year, month)[1]

    start_date = x

    acquisition_date = acq_date
    acquisition_date_year = acquisition_date.year
    acquisition_date_month = acquisition_date.month
    acquisition_date_last_day = calendar.monthrange(acquisition_date_year, acquisition_date_month)[1]

    end_of_operating_period_year = acquisition_date_year + loc
    end_of_operating_period_month = acquisition_date_month
    end_of_operating_period_last_day = calendar.monthrange(end_of_operating_period_year, end_of_operating_period_month)[1]
    end_of_operating_period = datetime.datetime(end_of_operating_period_year, end_of_operating_period_month, end_of_operating_period_last_day)

    end_of_senior_debt_repayment_period_date_year = acquisition_date_year + lod
    end_of_senior_debt_repayment_period_date_month = acquisition_date_month
    end_of_senior_debt_repayment_period_date_last_day = calendar.monthrange(end_of_senior_debt_repayment_period_date_year, end_of_senior_debt_repayment_period_date_month)[1]
    end_of_senior_debt_repayment_period_date = datetime.datetime(end_of_senior_debt_repayment_period_date_year, end_of_senior_debt_repayment_period_date_month, end_of_senior_debt_repayment_period_date_last_day)

    end_of_useful_life_year = acquisition_date_year + loul
    end_of_useful_life_month = acquisition_date_month
    end_of_useful_life_last_day = calendar.monthrange(end_of_useful_life_year, end_of_useful_life_month)[1]
    end_of_useful_life = datetime.datetime(end_of_useful_life_year, end_of_useful_life_month, end_of_useful_life_last_day)

    operating_period_flag = 0
    contract_year_number = 0
    period_number = 0

    escalation_flag = 0

    useful_life_flag = 0

    last_operating_period_flag = 0

    finance_close_flag = 0

    senior_debt_repayment_flag = 0


    for i in range(130):

        smonth = start_date.month

        year = start_date.year

        efirst_day = 1

        speriod = datetime.datetime(year, smonth, efirst_day)

        emonth = smonth + 3 - 1

        if emonth > 12:
            emonth = abs(12 - emonth)
            year += 1

        elast_day = calendar.monthrange(year, emonth)[1]

        eperiod = datetime.datetime(year, emonth, elast_day)

        end_of_period_last_day = calendar.monthrange(year, acquisition_date_month)[1]

        acq_day_comparison = eperiod - acquisition_date
        acq_day_comparison = int(acq_day_comparison.days)

        last_day_comparison = eperiod - end_of_operating_period
        last_day_comparison = int(last_day_comparison.days)

        if acq_day_comparison > 0 and last_day_comparison <= 0:
            operating_period_flag = 1
            
        else:
            operating_period_flag = 0
            

        
        if operating_period_flag == 1:
            if (emonth - 3) == acquisition_date_month:
                contract_year_number += 1
        else:
            contract_year_number = 0

        
        period_number = operating_period_flag * (period_number + 1)

        if period_number > 4:
            period_number = 1

        if (emonth == acquisition_date_month) and (elast_day == end_of_period_last_day):
            escalation_flag = 1
        else:
            escalation_flag = 0

        if eperiod == end_of_operating_period:
            last_operating_period_flag = 1
        else:
            last_operating_period_flag = 0
        
        if eperiod == acquisition_date:
            finance_close_flag = 1
        else:
            finance_close_flag = 0

        last_day_repayment_comparison = eperiod - end_of_senior_debt_repayment_period_date
        last_day_repayment_comparison = int(last_day_repayment_comparison.days)

        if acq_day_comparison > 0 and last_day_repayment_comparison <= 0:
            senior_debt_repayment_flag = 1
        else:
            senior_debt_repayment_flag = 0
    

        # print(f"End period is {eperiod}, {period_number}")

        days_in_period = eperiod - speriod
        days_in_period = int(days_in_period.days) + 1

        cumulative_days = eperiod - acquisition_date
        cumulative_days = int(cumulative_days.days)

        last_day_useful_life_comparison = eperiod - end_of_useful_life
        last_day_useful_life_comparison = int(last_day_useful_life_comparison.days)

        if acq_day_comparison > 0 and last_day_useful_life_comparison <= 0:
            useful_life_flag = 1
        else:
            useful_life_flag = 0


        
        if action == "create":
            timeline = Timeline.objects.create(
                related_scenario = relevant_scenario,
                index = i,
                date = eperiod,
                operating_period_flag = operating_period_flag,
                contract_year_number = contract_year_number,
                period_number = period_number,
                escalation_flag = escalation_flag,
                useful_life_flag = useful_life_flag,
                last_operating_period_flag = last_operating_period_flag,
                finance_close_flag = finance_close_flag,
                senior_debt_repayment_flag = senior_debt_repayment_flag,
                days_in_period = days_in_period,
                cumulative_days = cumulative_days
            )
            timeline.save()

        elif action == "update":
            timelines = Timeline.objects.all().filter(related_scenario=relevant_scenario)
            timeline = timelines[i]

            timeline.date = eperiod
            timeline.operating_period_flag = operating_period_flag
            timeline.contract_year_number = contract_year_number
            timeline.period_number = period_number
            timeline.escalation_flag = escalation_flag
            timeline.useful_life_flag = useful_life_flag
            timeline.last_operating_period_flag = last_operating_period_flag
            timeline.finance_close_flag = finance_close_flag
            timeline.senior_debt_repayment_flag = senior_debt_repayment_flag
            timeline.days_in_period = days_in_period
            timeline.cumulative_days = cumulative_days
            timeline.save()

        nsmonth = emonth + 1

        if nsmonth > 12:
            nsmonth = abs(12-nsmonth)
            year += 1


        start_date = datetime.datetime(year, nsmonth, 1)



def calculate_revenue(action, index, q1, q2, q3, q4, ann_deg, y1p50p, avb, pow_tarr, acc_rec_bal, acc_rec_days, timeline, previous_timeline):

    annual_degredation = ann_deg

    compound_degredation = 1

    q1_sa = q1
    q2_sa = q2
    q3_sa = q3
    q4_sa = q4

    year_1_p50_production = y1p50p
    availability = avb

    power_tarrif = pow_tarr
    units_in_thousands = 1000
    conversion = 1000000

    finance_close_flag = timeline.finance_close_flag

    operating_period_flag = timeline.operating_period_flag
    contract_year_number = timeline.contract_year_number
    period_number = timeline.period_number

    if operating_period_flag == 0:
        compound_degredation = 0
    else:
        compound_degredation = 1/((1+annual_degredation) ** (contract_year_number - 1))

    qsa = 0

    if period_number == 1:
        qsa = q1_sa
    elif period_number == 2:
        qsa = q2_sa
    elif period_number == 3:
        qsa = q3_sa
    else:
        qsa = q4_sa

    electricity_generation = compound_degredation * qsa * year_1_p50_production * availability

    revenue_amount = power_tarrif / units_in_thousands * conversion * electricity_generation * operating_period_flag

    if index == 0:
        accounts_receivable_beg = 0
    else:
        previous_revenue = Revenue.objects.get(timeline_event=previous_timeline)
        # print(previous_revenue)
        accounts_receivable_beg = previous_revenue.accounts_receivable

    accounts_receivable_days = acc_rec_days
    days_in_period = timeline.days_in_period
    forecast_accounts_receivable = revenue_amount * (accounts_receivable_days / days_in_period)

    cash_received_from_invoices = float(accounts_receivable_beg) + revenue_amount - forecast_accounts_receivable

    if finance_close_flag == 1:
        accounts_receivable = acc_rec_bal
    else:
        accounts_receivable = float(accounts_receivable_beg) + revenue_amount - cash_received_from_invoices

    if action == "create":
        revenue = Revenue.objects.create(
            timeline_event = timeline,
            revenue = revenue_amount,
            cash_received_from_invoices = cash_received_from_invoices,
            accounts_receivable = accounts_receivable
        )
        revenue.save()

    elif action == "update":
        revenue = Revenue.objects.get(timeline_event=timeline)
        revenue.revenue = revenue_amount
        revenue.cash_received_from_invoices = cash_received_from_invoices
        revenue.accounts_receivable = accounts_receivable
        revenue.save()


def calculate_expense(action, index, expe, exp_cpi, growthrate, cpi_at_signed_date, accounts_payable_bal, acc_pay_days, timeline, previous_timeline):

    annual_expense = expe

    number_of_periods = 4

    expected_cpi = exp_cpi

    growth_rate = growthrate

    operating_period_flag = timeline.operating_period_flag

    cpi_signed = cpi_at_signed_date

    if index == 0:
        current_escalation_factor = 0
        prev_escalation_factor = 0
        prev_escalation_flag = 0
        prev_cpi = 0

    else:
        previous_expense = Expense.objects.get(timeline_event=previous_timeline)
        prev_escalation_factor = previous_expense.escalation_factor
        prev_escalation_flag = previous_timeline.escalation_flag
        prev_cpi = previous_expense.cpi

    finance_close_flag = timeline.finance_close_flag

    if finance_close_flag == 1:
        current_cpi = expected_cpi
    else:
        current_cpi = operating_period_flag * float(prev_cpi) * (1+growth_rate)**(1/number_of_periods)

    if prev_escalation_flag == 1:
        current_escalation_factor = float(prev_cpi) / cpi_signed
    else:
        current_escalation_factor = prev_escalation_factor

    o_m_expense = (annual_expense / number_of_periods) * float(current_escalation_factor) * operating_period_flag


    if index == 0:
        accounts_payable_balance_beg = 0
    else:
        previous_expense = Expense.objects.get(timeline_event=previous_timeline)
        accounts_payable_balance_beg = previous_expense.accounts_payable

    accounts_payable_days = acc_pay_days
    days_in_period = timeline.days_in_period
    forecast_accounts_payable = o_m_expense * (accounts_payable_days / days_in_period)

    cash_paid_for_om_costs = float(accounts_payable_balance_beg) + o_m_expense - forecast_accounts_payable


    if finance_close_flag == 1:
        accounts_payable = accounts_payable_bal
    else:
        accounts_payable = float(accounts_payable_balance_beg) + o_m_expense - cash_paid_for_om_costs
    
    if action == "create":
        expense = Expense.objects.create(
            timeline_event = timeline,
            cpi = current_cpi,
            escalation_factor = current_escalation_factor,
            expense = o_m_expense,
            cash_paid_for_expense = cash_paid_for_om_costs,
            accounts_payable = accounts_payable
        )
        expense.save()
    
    elif action == "update":
        expense = Expense.objects.get(timeline_event=timeline)

        expense.cpi = current_cpi
        expense.escalation_factor = current_escalation_factor
        expense.expense = o_m_expense
        expense.cash_paid_for_expense = cash_paid_for_om_costs
        expense.accounts_payable = accounts_payable
        expense.save()



def calculate_depreciation(action, index, b_val, loul, timeline, previous_timeline):

    book_value = b_val
    useful_life = loul
    number_of_periods = 4

    useful_life_flag = timeline.useful_life_flag

    if index == 0:
        solar_asset_balance_beg = 0
    else:
        previous_depreciation = Depreciation.objects.get(timeline_event=previous_timeline)
        solar_asset_balance_beg = previous_depreciation.solar_asset_value

    finance_close_flag = timeline.finance_close_flag

    depreciation_amount = ((book_value / useful_life) / number_of_periods ) * useful_life_flag

    if finance_close_flag == 1:
        solar_asset_balance = book_value
    else:
        solar_asset_balance = float(solar_asset_balance_beg) - depreciation_amount

    if action == "create":
        depreciation = Depreciation.objects.create(
            timeline_event = timeline,
            depreciation = depreciation_amount,
            solar_asset_value = solar_asset_balance
        )
        depreciation.save()

    elif action == "update":
        depreciation = Depreciation.objects.get(timeline_event=timeline)

        depreciation.depreciation = depreciation_amount
        depreciation.solar_asset_value = solar_asset_balance
        depreciation.save()

def calculate_share_capital(action, index, book_value, debt_percentage, timeline, previous_timeline):

    investment_amount = book_value * (1 - debt_percentage)

    additional_capital = 0

    finance_close_flag = timeline.finance_close_flag

    last_operating_period_flag = timeline.last_operating_period_flag

    if index == 0:
        share_capital_balance_beg = 0
    else:
        previous_share_capital = Share_Capital.objects.get(timeline_event=previous_timeline)
        share_capital_balance_beg = previous_share_capital.share_capital

    if last_operating_period_flag == 1:
        redemption_capital = investment_amount
    else:
        redemption_capital = 0

    if finance_close_flag == 1:
        share_capital_balance = investment_amount
    else:
        share_capital_balance = float(share_capital_balance_beg) + additional_capital - redemption_capital

    if action == "create":
        share_capital = Share_Capital.objects.create(
            timeline_event = timeline,
            share_capital = share_capital_balance,
            share_capital_redemption = redemption_capital
        )
        share_capital.save()
    elif action == "update":
        share_capital = Share_Capital.objects.get(timeline_event=timeline)

        share_capital.share_capital = share_capital_balance
        share_capital.share_capital_redemption = redemption_capital
        share_capital.save()



def calculate_retained_earnings(action, index, retained_cash_init, timeline, previous_timeline):

    finance_close_flag = timeline.finance_close_flag

    if index == 0:
        retained_earnings_beg = 0
        retained_cash_beg = 0
    else:
        previous_retained_earnings = Retained_earnings.objects.get(timeline_event=previous_timeline)
        retained_earnings_beg = previous_retained_earnings.retained_earnings
        retained_cash_beg = previous_retained_earnings.retained_cash

    pat = Profit_after_tax.objects.get(timeline_event=timeline)
    profit_after_tax = pat.profit_after_tax

    earnings_available_for_dividend = max(0, (retained_earnings_beg + profit_after_tax))

    cfafd = Cash_flow_available_for_dividends.objects.get(timeline_event=timeline)
    cash_flow_available_for_dividends = cfafd.cash_flow_available_for_dividends

    cash_available_for_dividends = max(0, retained_cash_beg + cash_flow_available_for_dividends)

    dividends_paid = min(earnings_available_for_dividend, cash_available_for_dividends)

    retained_earnings_bal = retained_earnings_beg + profit_after_tax - dividends_paid

    if finance_close_flag == 1:
        retained_cash_bal = retained_cash_init
    else:
        retained_cash_bal = retained_cash_beg + cash_flow_available_for_dividends - dividends_paid

    if action == "create":
        retained_earnings = Retained_earnings.objects.create(
            timeline_event = timeline,
            dividends_paid = dividends_paid,
            retained_earnings = retained_earnings_bal,
            retained_cash = retained_cash_bal
        )
        retained_earnings.save()

    elif action == "update":
        retained_earnings = Retained_earnings.objects.get(timeline_event=timeline)

        retained_earnings.dividends_paid = dividends_paid
        retained_earnings.retained_earnings = retained_earnings_bal
        retained_earnings.retained_cash = retained_cash_bal
        retained_earnings.save()


def calculate_debt(action, index, sen_deb_gear, book_val, lod, sen_debt_swap_rat, sen_debt_int_marg, count_conv, timeline, previous_timeline):

    senior_debt_gearing = sen_deb_gear
    solar_asset_book_value = book_val
    senior_debt_drawdown = senior_debt_gearing * solar_asset_book_value

    senior_debt_repayment_term = lod
    number_of_periods_in_a_year = 4

    senior_debt_repayment_flag = timeline.senior_debt_repayment_flag
    finance_close_flag = timeline.finance_close_flag
    days_in_period = timeline.days_in_period

    if index == 0:
        senior_debt_balance_beg = 0
    else:
        previous_debt = Debt.objects.get(timeline_event=previous_timeline)
        senior_debt_balance_beg = previous_debt.senior_debt

    senior_debt_interest_rate = sen_debt_swap_rat + sen_debt_int_marg
    senior_debt_day_count_convention = count_conv

    senior_debt_principle_repayment = (senior_debt_drawdown / senior_debt_repayment_term / number_of_periods_in_a_year) * senior_debt_repayment_flag

    if finance_close_flag == 1:
        senior_debt_balance = senior_debt_drawdown
    else:
        senior_debt_balance = float(senior_debt_balance_beg) - senior_debt_principle_repayment

    senior_debt_period_interest_rate = senior_debt_interest_rate / senior_debt_day_count_convention * days_in_period

    senior_debt_interest = float(senior_debt_balance_beg) * senior_debt_period_interest_rate

    if action == "create":
        debt = Debt.objects.create(
            timeline_event = timeline,
            senior_debt = senior_debt_balance,
            senior_debt_repayment = senior_debt_principle_repayment,
            senior_debt_interest = senior_debt_interest
        )
        debt.save()
    
    elif action == "update":
        debt = Debt.objects.get(timeline_event=timeline)

        debt.senior_debt = senior_debt_balance
        debt.senior_debt_repayment = senior_debt_principle_repayment
        debt.senior_debt_interest = senior_debt_interest
        debt.save()


def calculate_rcf(action, index, int_rate, count_conv, rcf_bal_init, timeline, previous_timeline):

    finance_close_flag = timeline.finance_close_flag

    rcf_interest_rate = int_rate
    senior_debt_day_count_convention = count_conv

    if index == 0:
        retained_cash_balance_beg = 0
        rcf_balance_beg = 0
    
    else:
        previous_retained_earnings = Retained_earnings.objects.get(timeline_event=previous_timeline)
        retained_cash_balance_beg = previous_retained_earnings.retained_cash

        previous_rcf = Rcf.objects.get(timeline_event=previous_timeline)
        rcf_balance_beg = previous_rcf.rcf_balance

    revenue = Revenue.objects.get(timeline_event=timeline)
    cash_received_from_invoices = revenue.cash_received_from_invoices

    expense = Expense.objects.get(timeline_event=timeline)
    cash_paid_for_om_costs = expense.cash_paid_for_expense

    cash_tax = Cash_tax.objects.get(timeline_event=timeline)
    corporate_income_tax_paid = cash_tax.corporate_income_tax_paid

    debt = Debt.objects.get(timeline_event=timeline)
    senior_debt_interest = debt.senior_debt_interest
    senior_debt_repayment = debt.senior_debt_repayment

    cash_flow_available_for_rcf = cash_received_from_invoices - cash_paid_for_om_costs - corporate_income_tax_paid - senior_debt_interest - senior_debt_repayment

    cash_available_for_rcf_cash_shortfall_for_rcf = retained_cash_balance_beg + cash_flow_available_for_rcf

    cash_available_for_rcf = max(cash_available_for_rcf_cash_shortfall_for_rcf, 0)

    rcf_drawdown = -1 * min(cash_available_for_rcf_cash_shortfall_for_rcf, 0)

    days_in_period = timeline.days_in_period

    rcf_period_interest_rate = rcf_interest_rate * (days_in_period / senior_debt_day_count_convention)

    rcf_interest = float(rcf_balance_beg) * rcf_period_interest_rate

    rcf_interest_paid = min(cash_available_for_rcf, rcf_interest)

    rcf_unpaid_interest = rcf_interest - float(rcf_interest_paid)

    cash_available_for_rcf_principal_repayment = float(cash_available_for_rcf) - float(rcf_interest_paid)

    rcf_principal_repayment = min(cash_available_for_rcf_principal_repayment, rcf_balance_beg)

    if finance_close_flag == 1:
        rcf_balance = rcf_bal_init
    else:
        rcf_balance = float(rcf_balance_beg) + float(rcf_drawdown) + rcf_unpaid_interest - float(rcf_principal_repayment)

    if action == "create":
        rcf = Rcf.objects.create(
            timeline_event = timeline,
            rcf_drawdown = rcf_drawdown,
            rcf_interest = rcf_interest,
            rcf_interest_paid = rcf_interest_paid,
            rcf_principal_repayment = rcf_principal_repayment,
            rcf_balance = rcf_balance
        )
        rcf.save()

    elif action == "update":
        rcf = Rcf.objects.get(timeline_event=timeline)
        rcf.rcf_drawdown = rcf_drawdown
        rcf.rcf_interest = rcf_interest
        rcf.rcf_interest_paid = rcf_interest_paid
        rcf.rcf_principal_repayment = rcf_principal_repayment
        rcf.rcf_balance = rcf_balance
        rcf.save()


def calculate_cash_tax(action, index, tr, book_val, tdr, rcf_int_rate, count_conv, tlcf, timeline, previous_timeline):

    tax_rate = tr

    solar_asset_book_value = book_val
    tax_depreciation_rate = tdr

    allowable_capex = 0

    finance_close_date_flag = timeline.finance_close_flag
    last_operating_period_flag = timeline.last_operating_period_flag

    rcf_interest_rate = rcf_int_rate
    senior_debt_day_count_convention = count_conv
    days_in_period = timeline.days_in_period

    if index == 0:
        asset_value_for_tax_balance_beg = 0
        tax_losses_carried_forward_beg = 0
        rcf_balance_beg = 0
    else:
        previous_cash_tax = Cash_tax.objects.get(timeline_event=previous_timeline)
        asset_value_for_tax_balance_beg = previous_cash_tax.asset_value_for_tax_balance
        tax_losses_carried_forward_beg = previous_cash_tax.tax_losses_carried_forward
        
        previous_rcf = Rcf.objects.get(timeline_event=previous_timeline)
        rcf_balance_beg = previous_rcf.rcf_balance

    if last_operating_period_flag == 1:
        tax_depreciation = asset_value_for_tax_balance_beg
    else:
        tax_depreciation = float(asset_value_for_tax_balance_beg) * tax_depreciation_rate

    if finance_close_date_flag == 1:
        asset_value_for_tax_balance = solar_asset_book_value
    else:
        asset_value_for_tax_balance = float(asset_value_for_tax_balance_beg) + allowable_capex - float(tax_depreciation)

    debt = Debt.objects.get(timeline_event=timeline)
    senior_debt_interest = debt.senior_debt_interest

    rcf_period_interest_rate = rcf_interest_rate * (days_in_period / senior_debt_day_count_convention)

    rcf_interest = float(rcf_balance_beg) * rcf_period_interest_rate

    interest_deduction_for_tax = float(senior_debt_interest) + rcf_interest

    ebitda_object = Ebitda.objects.get(timeline_event=timeline)
    ebitda = ebitda_object.ebitda

    taxable_income_tax_losses_arising = float(ebitda) - float(tax_depreciation) - interest_deduction_for_tax

    taxable_income = max(taxable_income_tax_losses_arising, 0)

    tax_losses_arising = min(taxable_income_tax_losses_arising, 0) * -1

    tax_losses_utillised = min(taxable_income, tax_losses_carried_forward_beg)

    taxable_income_net_of_tax_losses_utillised = taxable_income - float(tax_losses_utillised)

    corporate_income_tax_paid = taxable_income_net_of_tax_losses_utillised * tax_rate

    if finance_close_date_flag == 1:
        tax_losses_carried_forward = tlcf
    else:
        tax_losses_carried_forward = float(tax_losses_carried_forward_beg) + tax_losses_arising - float(tax_losses_utillised)

    if action == "create":
        cash_tax = Cash_tax.objects.create(
            timeline_event = timeline,
            asset_value_for_tax_balance = asset_value_for_tax_balance,
            corporate_income_tax_paid = corporate_income_tax_paid,
            tax_losses_carried_forward = tax_losses_carried_forward
        )
        cash_tax.save()
    elif action == "update":
        cash_tax = Cash_tax.objects.get(timeline_event=timeline)

        cash_tax.asset_value_for_tax_balance = asset_value_for_tax_balance
        cash_tax.corporate_income_tax_paid = corporate_income_tax_paid
        cash_tax.tax_losses_carried_forward = tax_losses_carried_forward
        cash_tax.save()


def calculate_accounting_tax(action, index, tr, timeline):

    tax_rate = tr

    profit_before_tax_object = Profit_before_tax.objects.get(timeline_event=timeline)
    profit_before_tax = profit_before_tax_object.profit_before_tax

    tax_expense = float(profit_before_tax) * tax_rate

    if action == "create":
        accounting_tax = Accounting_tax.objects.create(
            timeline_event = timeline,
            tax_expense = tax_expense
        )
        accounting_tax.save()

    elif action == "update":
        accounting_tax = Accounting_tax.objects.get(timeline_event=timeline)

        accounting_tax.tax_expense = tax_expense
        accounting_tax.save()



def calculate_deferred_tax_balance(action, index, timeline, previous_timeline):

    if index == 0:
        deferred_tax_balance_beg = 0
    else:
        previous_deferred_tax = Deferred_tax.objects.get(timeline_event=previous_timeline)
        deferred_tax_balance_beg = previous_deferred_tax.deferred_tax

    accounting_tax = Accounting_tax.objects.get(timeline_event=timeline)
    tax_expense = accounting_tax.tax_expense

    cash_tax = Cash_tax.objects.get(timeline_event=timeline)
    corporate_income_tax_paid = cash_tax.corporate_income_tax_paid

    deferred_tax_balance = deferred_tax_balance_beg + tax_expense - corporate_income_tax_paid

    if action == "create":
        deferred_tax = Deferred_tax.objects.create(
            timeline_event=timeline,
            deferred_tax = deferred_tax_balance
        )
        deferred_tax.save()
    
    elif action == "update":
        deferred_tax = Deferred_tax.objects.get(timeline_event=timeline)
        deferred_tax.deferred_tax = deferred_tax_balance
        deferred_tax.save()


def calculate_ebitda(action, timeline):

    revenue_object = Revenue.objects.get(timeline_event=timeline)
    revenue = revenue_object.revenue

    expense_object = Expense.objects.get(timeline_event=timeline)
    expense = expense_object.expense

    ebitda = revenue - expense

    if action == "create":
        ebitda_object = Ebitda.objects.create(
            timeline_event=timeline,
            ebitda = ebitda
        )
        ebitda_object.save()

    elif action == "update":
        ebitda_object =  Ebitda.objects.get(timeline_event=timeline)
        ebitda_object.ebitda = ebitda
        ebitda_object.save()



def calculate_ebit(action, timeline):

    ebitda_object = Ebitda.objects.get(timeline_event=timeline)
    ebitda = ebitda_object.ebitda

    depreciation_object = Depreciation.objects.get(timeline_event=timeline)
    depreciation = depreciation_object.depreciation

    ebit = ebitda - depreciation

    if action == "create":
        ebit_object = Ebit.objects.create(
            timeline_event=timeline,
            ebit = ebit
        )
        ebit_object.save()
    
    elif action == "update":
        ebit_object = Ebit.objects.get(timeline_event=timeline)
        ebit_object.ebit = ebit
        ebit_object.save()


def calculate_profit_before_tax(action, timeline):

    ebit_object = Ebit.objects.get(timeline_event=timeline)
    ebit = ebit_object.ebit

    debt = Debt.objects.get(timeline_event=timeline)
    senior_debt_interest = debt.senior_debt_interest

    refi_faci_interest = 0

    rcf = Rcf.objects.get(timeline_event=timeline)
    rcf_interest_expense = rcf.rcf_interest

    profit_before_tax = ebit - senior_debt_interest - refi_faci_interest - rcf_interest_expense

    if action == "create":
        profit_before_tax_object = Profit_before_tax.objects.create(
            timeline_event = timeline,
            profit_before_tax = profit_before_tax
        )
        profit_before_tax_object.save()
    
    elif action == "update":
        profit_before_tax_object = Profit_before_tax.objects.get(timeline_event=timeline)
        profit_before_tax_object.profit_before_tax = profit_before_tax
        profit_before_tax_object.save()


def calculate_profit_after_tax(action, timeline):

    profit_before_tax_object = Profit_before_tax.objects.get(timeline_event=timeline)
    profit_before_tax = profit_before_tax_object.profit_before_tax

    accounting_tax = Accounting_tax.objects.get(timeline_event=timeline)
    tax_expense = accounting_tax.tax_expense

    profit_after_tax = profit_before_tax - tax_expense

    if action == "create":
        profit_after_tax_object = Profit_after_tax.objects.create(
            timeline_event = timeline,
            profit_after_tax = profit_after_tax
        )
        profit_after_tax_object.save()
    
    elif action == "update":
        profit_after_tax_object = Profit_after_tax.objects.get(timeline_event=timeline)
        profit_after_tax_object.profit_after_tax = profit_after_tax
        profit_after_tax_object.save()




def calculate_cash_flow_available_for_senior_debt_service(action, timeline):

    revenue = Revenue.objects.get(timeline_event=timeline)
    cash_received = revenue.cash_received_from_invoices

    expense = Expense.objects.get(timeline_event=timeline)
    cash_paid = expense.cash_paid_for_expense

    cash_tax = Cash_tax.objects.get(timeline_event=timeline)
    tax_paid = cash_tax.corporate_income_tax_paid

    if action == "create":
        cash_flow_available_for_senior_debt_service = Cash_flow_available_for_senior_debt.objects.create(
            timeline_event = timeline,
            cash_flow_available_for_senior_debt = cash_received - cash_paid - tax_paid
        )
        cash_flow_available_for_senior_debt_service.save()

    elif action == "update":
        cash_flow_available_for_senior_debt_service = Cash_flow_available_for_senior_debt.objects.get(timeline_event=timeline)
        cash_flow_available_for_senior_debt_service.cash_flow_available_for_senior_debt = cash_received - cash_paid - tax_paid

        cash_flow_available_for_senior_debt_service.save()


def calculate_cash_flow_available_for_refinancing_facility(action, timeline):

    cash_flow_available_for_senior_debt_service_object = Cash_flow_available_for_senior_debt.objects.get(timeline_event=timeline)

    cash_flow_available_for_senior_debt = cash_flow_available_for_senior_debt_service_object.cash_flow_available_for_senior_debt

    debt = Debt.objects.get(timeline_event=timeline)
    senior_debt_interest = debt.senior_debt_interest
    senior_debt_repayment = debt.senior_debt_repayment

    cash_flow_available_for_refinancing_facility = cash_flow_available_for_senior_debt - senior_debt_interest - senior_debt_repayment

    if action == "create":
        cash_flow_available_for_refinancing_facility_object = Cash_flow_available_for_refinancing_facility.objects.create(
            timeline_event = timeline,
            cash_flow_available_for_refinancing_facility = cash_flow_available_for_refinancing_facility
        )
        cash_flow_available_for_refinancing_facility_object.save()

    elif action == "update":
        cash_flow_available_for_refinancing_facility_object = Cash_flow_available_for_refinancing_facility.objects.get(timeline_event=timeline)
        cash_flow_available_for_refinancing_facility_object.cash_flow_available_for_refinancing_facility = cash_flow_available_for_refinancing_facility
        cash_flow_available_for_refinancing_facility_object.save()



def calculate_cash_flow_available_for_rcf(action, timeline):

    cash_flow_availble_for_refinancing_facility_object = Cash_flow_available_for_refinancing_facility.objects.get(timeline_event=timeline)

    cash_flow_availble_for_refinancing_facility = cash_flow_availble_for_refinancing_facility_object.cash_flow_available_for_refinancing_facility


    drawdown = 0
    repayment = 0
    interest = 0

    cash_flow_available_for_rcf = cash_flow_availble_for_refinancing_facility + drawdown - repayment - interest

    if action == "create":
        cash_flow_available_for_rcf_object = Cash_flow_available_for_rcf.objects.create(
            timeline_event = timeline,
            cash_flow_available_for_rcf = cash_flow_available_for_rcf
        )
        cash_flow_available_for_rcf_object.save()
    
    elif action == "update":
        cash_flow_available_for_rcf_object = Cash_flow_available_for_rcf.objects.get(timeline_event=timeline)
        cash_flow_available_for_rcf_object.cash_flow_available_for_rcf = cash_flow_available_for_rcf
        cash_flow_available_for_rcf_object.save()


def calculate_cash_flow_available_for_shareholders(action, timeline):

    cash_flow_available_for_rcf_object = Cash_flow_available_for_rcf.objects.get(timeline_event=timeline)
    cash_flow_available_for_rcf = cash_flow_available_for_rcf_object.cash_flow_available_for_rcf

    rcf = Rcf.objects.get(timeline_event=timeline)
    drawdown = rcf.rcf_drawdown
    repayment = rcf.rcf_principal_repayment
    interest = rcf.rcf_interest_paid

    cash_flow_available_for_shareholders = cash_flow_available_for_rcf + drawdown - repayment - interest

    if action == "create":
        cash_flow_available_for_shareholders_object = Cash_flow_available_for_shareholders.objects.create(
            timeline_event = timeline,
            cash_flow_available_for_shareholders = cash_flow_available_for_shareholders
        )
        cash_flow_available_for_shareholders_object.save()
    
    elif action == "update":
        cash_flow_available_for_shareholders_object = Cash_flow_available_for_shareholders.objects.get(timeline_event=timeline)
        cash_flow_available_for_shareholders_object.cash_flow_available_for_shareholders = cash_flow_available_for_shareholders
        cash_flow_available_for_shareholders_object.save()


def calculate_cash_flow_available_for_dividends(action, timeline):

    cash_flow_available_for_shareholders_object = Cash_flow_available_for_shareholders.objects.get(timeline_event=timeline)

    cash_flow_available_for_shareholders = cash_flow_available_for_shareholders_object.cash_flow_available_for_shareholders

    share_capital_object = Share_Capital.objects.get(timeline_event=timeline)
    redemption = share_capital_object.share_capital_redemption

    cash_flow_available_for_dividends = cash_flow_available_for_shareholders - redemption

    if action == "create":
        cash_flow_available_for_dividends_object = Cash_flow_available_for_dividends.objects.create(
            timeline_event = timeline,
            cash_flow_available_for_dividends = cash_flow_available_for_dividends
        )
        cash_flow_available_for_dividends_object.save()
    
    elif action == "update":
        cash_flow_available_for_dividends_object = Cash_flow_available_for_dividends.objects.get(timeline_event=timeline)
        cash_flow_available_for_dividends_object.cash_flow_available_for_dividends = cash_flow_available_for_dividends
        cash_flow_available_for_dividends_object.save()

def calculate_net_cash_flow(action, timeline):

    cash_flow_available_for_dividends_object = Cash_flow_available_for_dividends.objects.get(timeline_event=timeline)
    cash_flow_available_for_dividends = cash_flow_available_for_dividends_object.cash_flow_available_for_dividends

    retained_earnings_object = Retained_earnings.objects.get(timeline_event=timeline)
    dividends_paid = retained_earnings_object.dividends_paid

    net_cash_flow = cash_flow_available_for_dividends - dividends_paid

    if action == "create":
        net_cash_flow_object = Net_cash_flow.objects.create(
            timeline_event = timeline,
            net_cash_flow = net_cash_flow
        )
        net_cash_flow_object.save()

    elif action == "update":
        net_cash_flow_object = Net_cash_flow.objects.get(timeline_event=timeline)
        net_cash_flow_object.net_cash_flow = net_cash_flow
        net_cash_flow_object.save()


def calculate_investment_premium(index, targ_irr, share_of_proj, timeline):

    days_in_year = 365

    discount_factor = 0

    target_irr = targ_irr

    premium = 0

    finance_close_flag = timeline.finance_close_flag

    cumulative_days = timeline.cumulative_days

    years_since_fin_close = cumulative_days / days_in_year

    operating_period_flag = timeline.operating_period_flag

    max_flag = max(finance_close_flag, operating_period_flag)

    discount_factor = max_flag * 1 / (1 + target_irr) ** years_since_fin_close 

    retained_earnings = Retained_earnings.objects.get(timeline_event=timeline)
    dividends_paid = retained_earnings.dividends_paid

    share_of_dividends = float(dividends_paid) * share_of_proj

    share_capital = Share_Capital.objects.get(timeline_event=timeline)

    share_capital_issued = 0

    if finance_close_flag == 1:
        share_capital_issued = float(share_capital.share_capital) * share_of_proj * -1

    share_capital_redemption = float(share_capital.share_capital_redemption) * share_of_proj * 1

    cashflow_excluding_premium = share_of_dividends + share_capital_issued + share_capital_redemption

    cashflow = cashflow_excluding_premium * discount_factor

    return cashflow

