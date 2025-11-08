from django.shortcuts import render
from django.db.models import Sum, Count
from .models import TransparencyMetric, FinancialReport
from donations.models import Donation
from website.models import Project
from volunteers.models import Volunteer


def transparency(request):
    """Transparency dashboard page"""

    # Get key metrics
    total_donations = Donation.objects.filter(payment_status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_projects = Project.objects.filter(status__in=['ongoing', 'completed']).count()

    active_volunteers = Volunteer.objects.filter(status='active').count()

    # Get people helped metric
    try:
        people_helped_metric = TransparencyMetric.objects.filter(
            metric_type='people_helped',
            period='all_time'
        ).latest('date')
        people_helped = int(people_helped_metric.value)
    except TransparencyMetric.DoesNotExist:
        people_helped = 45000

    # Get financial breakdown (mock data for now)
    financial_breakdown = {
        'programs': 75,
        'fundraising': 15,
        'admin': 10,
    }

    # Get latest financial report
    latest_report = FinancialReport.objects.filter(is_published=True).first()
    if latest_report:
        financial_breakdown = {
            'programs': float(latest_report.program_expenses_percentage),
            'fundraising': float(latest_report.fundraising_expenses_percentage),
            'admin': float(latest_report.admin_expenses_percentage),
        }

    # Get all published reports
    reports = FinancialReport.objects.filter(is_published=True)

    # Get impact metrics
    impact_metrics = []
    try:
        wells_metric = TransparencyMetric.objects.filter(
            metric_type='wells_built',
            period='all_time'
        ).latest('date')
        impact_metrics.append({
            'label': 'Clean Water Wells Built',
            'value': int(wells_metric.value)
        })
    except TransparencyMetric.DoesNotExist:
        impact_metrics.append({
            'label': 'Clean Water Wells Built',
            'value': 27
        })

    try:
        students_metric = TransparencyMetric.objects.filter(
            metric_type='students_sponsored',
            period='all_time'
        ).latest('date')
        impact_metrics.append({
            'label': 'Women Trained',
            'value': int(students_metric.value)
        })
    except TransparencyMetric.DoesNotExist:
        impact_metrics.append({
            'label': 'Women Trained',
            'value': 1200
        })

    context = {
        'total_donations': total_donations,
        'total_projects': total_projects,
        'active_volunteers': active_volunteers,
        'people_helped': people_helped,
        'financial_breakdown': financial_breakdown,
        'reports': reports,
        'impact_metrics': impact_metrics,
    }

    return render(request, 'dashboard/transparency.html', context)
