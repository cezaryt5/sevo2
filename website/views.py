from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, NewsArticle, Partner, ContactMessage
from donations.models import Donation
from volunteers.models import Volunteer
from dashboard.models import TransparencyMetric
from .forms import UserRegistrationForm, UserLoginForm


def home(request):
    """Home page view"""
    # Get statistics from database
    stats = {
        'women_trained': '1,200+',  # Can be updated from TransparencyMetric
        'wells_built': '27',
        'active_volunteers': Volunteer.objects.filter(status='active').count() or '350',
    }

    # Try to get real stats from TransparencyMetric
    try:
        women_metric = TransparencyMetric.objects.filter(
            metric_type='students_sponsored',
            period='all_time'
        ).latest('date')
        stats['women_trained'] = f"{int(women_metric.value):,}+"
    except TransparencyMetric.DoesNotExist:
        pass

    try:
        wells_metric = TransparencyMetric.objects.filter(
            metric_type='wells_built',
            period='all_time'
        ).latest('date')
        stats['wells_built'] = int(wells_metric.value)
    except TransparencyMetric.DoesNotExist:
        pass

    context = {
        'stats': stats,
    }
    return render(request, 'website/home.html', context)


def about(request):
    """About Us page view"""
    partners = Partner.objects.filter(is_active=True)

    context = {
        'partners': partners,
    }
    return render(request, 'website/about.html', context)


def projects_list(request):
    """Projects listing page"""
    projects = Project.objects.all()

    # Filter by category
    category = request.GET.get('category')
    if category:
        projects = projects.filter(category=category)

    # Filter by status
    status = request.GET.get('status')
    if status:
        projects = projects.filter(status=status)

    # Search
    search = request.GET.get('search')
    if search:
        projects = projects.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )

    # Pagination
    paginator = Paginator(projects, 9)  # 9 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category': category,
        'status': status,
        'search': search,
    }
    return render(request, 'website/projects.html', context)


def project_detail(request, slug):
    """Project detail page"""
    project = get_object_or_404(Project, slug=slug)

    # Get related donations
    donations = project.donations.filter(payment_status='completed')[:5]

    context = {
        'project': project,
        'donations': donations,
    }
    return render(request, 'website/project_detail.html', context)


def news_list(request):
    """News listing page"""
    articles = NewsArticle.objects.filter(published_at__isnull=False)

    # Get featured article
    featured = articles.filter(is_featured=True).first()

    # Filter by category
    category = request.GET.get('category')
    if category:
        articles = articles.filter(category=category)

    # Search
    search = request.GET.get('search')
    if search:
        articles = articles.filter(
            Q(title__icontains=search) |
            Q(excerpt__icontains=search) |
            Q(content__icontains=search)
        )

    # Pagination
    paginator = Paginator(articles, 9)  # 9 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'featured': featured,
        'page_obj': page_obj,
        'category': category,
        'search': search,
    }
    return render(request, 'website/news.html', context)


def news_detail(request, slug):
    """News article detail page"""
    article = get_object_or_404(NewsArticle, slug=slug, published_at__isnull=False)

    # Increment views count
    article.views_count += 1
    article.save(update_fields=['views_count'])

    # Get related articles
    related = NewsArticle.objects.filter(
        category=article.category,
        published_at__isnull=False
    ).exclude(id=article.id)[:3]

    context = {
        'article': article,
        'related': related,
    }
    return render(request, 'website/news_detail.html', context)


def get_involved(request):
    """Get Involved page with donation, volunteer, and partner forms"""
    context = {}
    return render(request, 'website/get_involved.html', context)


def user_register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('website:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
            return redirect('website:home')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'website/register.html', context)


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('website:home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                next_url = request.GET.get('next', 'website:home')
                return redirect(next_url)
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'website/login.html', context)


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('website:home')


@login_required
def user_profile(request):
    """User profile view"""
    # Get user's donations
    donations = Donation.objects.filter(donor_email=request.user.email).order_by('-created_at')[:10]

    # Check if user has a volunteer profile
    volunteer_profile = None
    try:
        volunteer_profile = Volunteer.objects.get(email=request.user.email)
    except Volunteer.DoesNotExist:
        pass

    context = {
        'donations': donations,
        'volunteer_profile': volunteer_profile,
    }
    return render(request, 'website/profile.html', context)
