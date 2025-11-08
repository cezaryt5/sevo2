from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Volunteer, PartnerInquiry
from .forms import VolunteerRegistrationForm, PartnerInquiryForm


def volunteer_register(request):
    """Volunteer registration view"""
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            volunteer = form.save(commit=False)
            volunteer.status = 'pending'
            volunteer.save()
            form.save_m2m()  # Save many-to-many relationships (skills)

            # Send confirmation email
            send_mail(
                'Volunteer Application Received',
                f'Dear {volunteer.full_name},\n\n'
                f'Thank you for your interest in volunteering with SEVO! '
                f'We have received your application and will review it shortly.\n\n'
                f'We will contact you at {volunteer.email} once your application is approved.\n\n'
                f'Best regards,\nSEVO Team',
                settings.DEFAULT_FROM_EMAIL,
                [volunteer.email],
                fail_silently=True,
            )

            messages.success(
                request,
                'Thank you for registering! Your application is pending approval. '
                'We will contact you soon.'
            )
            return redirect('home')
    else:
        form = VolunteerRegistrationForm()

    return render(request, 'volunteers/register.html', {'form': form})


def partner_inquiry(request):
    """Partnership inquiry view"""
    if request.method == 'POST':
        form = PartnerInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.status = 'new'
            inquiry.save()

            # Send confirmation email
            send_mail(
                'Partnership Inquiry Received',
                f'Dear {inquiry.contact_person},\n\n'
                f'Thank you for your interest in partnering with SEVO! '
                f'We have received your inquiry and will review it shortly.\n\n'
                f'Organization: {inquiry.organization_name}\n'
                f'Partnership Type: {inquiry.get_partnership_type_display()}\n\n'
                f'We will contact you at {inquiry.email} to discuss next steps.\n\n'
                f'Best regards,\nSEVO Team',
                settings.DEFAULT_FROM_EMAIL,
                [inquiry.email],
                fail_silently=True,
            )

            messages.success(
                request,
                'Thank you for your inquiry! We will review your request and contact you soon.'
            )
            return redirect('home')
    else:
        form = PartnerInquiryForm()

    return render(request, 'volunteers/partner_inquiry.html', {'form': form})
