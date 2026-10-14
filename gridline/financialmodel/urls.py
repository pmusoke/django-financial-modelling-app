from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login_view", views.login_view, name="login_view"),
    path("register", views.register, name="register"),
    path("logout_view", views.logout_view, name="logout_view"),
    path("createproject", views.createproject, name="createproject"),
    path("<str:user>/viewprojects", views.viewprojects, name="viewprojects"),
    path("createscenario", views.createscenario, name="createscenario"),
    path("quarterly_financial_statements/<int:id>", views.quarterly_financial_statements, name="quarterly_financial_statements"),
    path("annual_financial_statements/<int:id>", views.annual_financial_statements, name="annual_financial_statements"),
    path("quarterly_financial_statements_revenue/<int:id>", views.quarterly_financial_statements_revenue, name="quarterly_financial_statements_revenue"),
    path("quarterly_financial_statements_expense/<int:id>", views.quarterly_financial_statements_expense, name="quarterly_financial_statements_expense"),
    path("quarterly_financial_statements_escalation/<int:id>", views.quarterly_financial_statements_escalation, name="quarterly_financial_statements_escalation"),
    path("quarterly_financial_statements_depreciation/<int:id>", views.quarterly_financial_statements_depreciation, name="quarterly_financial_statements_depreciation"),
    path("quarterly_financial_statements_debt/<int:id>", views.quarterly_financial_statements_debt, name="quarterly_financial_statements_debt"),
    path("quarterly_financial_statements_rcf/<int:id>", views.quarterly_financial_statements_rcf, name="quarterly_financial_statements_rcf"),
    path("quarterly_financial_statements_tax/<int:id>", views.quarterly_financial_statements_tax, name="quarterly_financial_statements_tax"),
    path("quarterly_financial_statements_equity/<int:id>", views.quarterly_financial_statements_equity, name="quarterly_financial_statements_equity"),
    path("investment_premium/<int:id>", views.investment_premium, name="investment_premium"),
    path("irr_detail/<int:id>", views.irr_detail, name="irr_detail"),
    path("dscr/<int:id>", views.dscr, name="dscr"),
    path("updatescenario/<int:id>", views.updatescenario, name="updatescenario"),
    path("deletescenario/<int:id>", views.deletescenario, name="deletescenario"),
    path("<int:id>/project_comparison", views.project_comparison, name="project_comparison")



]