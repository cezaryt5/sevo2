from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Donation, BankTransfer
from .forms import DonationForm, BankTransferForm


def donate(request):
    """Main donation page with payment method selection"""
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.payment_status = 'pending'
            donation.save()

            # Redirect based on payment method
            if donation.payment_method == 'bank_transfer':
                return redirect('donations:bank_transfer', donation_id=donation.id)
            elif donation.payment_method in ['paypal', 'stripe']:
                return redirect('donations:mock_payment', donation_id=donation.id)
            elif donation.payment_method == 'crypto':
                messages.info(request, 'Cryptocurrency payments coming soon!')
                return redirect('donations:donate')
    else:
        form = DonationForm()

    return render(request, 'donations/donate.html', {'form': form})


def bank_transfer(request, donation_id):
    """Bank transfer details and proof upload"""
    donation = get_object_or_404(Donation, id=donation_id, payment_method='bank_transfer')

    if request.method == 'POST':
        form = BankTransferForm(request.POST, request.FILES)
        if form.is_valid():
            bank_transfer = form.save(commit=False)
            bank_transfer.donation = donation
            bank_transfer.save()

            # Send confirmation email
            send_mail(
                'Donation Received - Pending Verification',
                f'Thank you for your donation of {donation.amount} {donation.currency}. '
                f'We have received your bank transfer details and will verify them shortly. '
                f'Transaction ID: {donation.transaction_id}',
                settings.DEFAULT_FROM_EMAIL,
                [donation.donor_email],
                fail_silently=True,
            )

            messages.success(request, 'Thank you! Your donation is pending verification.')
            return redirect('donations:thank_you', donation_id=donation.id)
    else:
        form = BankTransferForm()

    return render(request, 'donations/bank_transfer.html', {
        'form': form,
        'donation': donation
    })


def mock_payment(request, donation_id):
    """Mock payment processing for PayPal/Stripe"""
    donation = get_object_or_404(Donation, id=donation_id)

    if request.method == 'POST':
        # Simulate payment processing
        action = request.POST.get('action')

        if action == 'success':
            donation.payment_status = 'completed'
            donation.save()

            # Send confirmation email
            send_mail(
                'Donation Successful',
                f'Thank you for your donation of {donation.amount} {donation.currency}! '
                f'Receipt Number: {donation.receipt_number}',
                settings.DEFAULT_FROM_EMAIL,
                [donation.donor_email],
                fail_silently=True,
            )

            messages.success(request, 'Payment successful! Thank you for your donation.')
            return redirect('donations:thank_you', donation_id=donation.id)
        else:
            donation.payment_status = 'failed'
            donation.save()
            messages.error(request, 'Payment failed. Please try again.')
            return redirect('donations:donate')

    return render(request, 'donations/mock_payment.html', {'donation': donation})


def thank_you(request, donation_id):
    """Thank you page after donation"""
    donation = get_object_or_404(Donation, id=donation_id)
    return render(request, 'donations/thank_you.html', {'donation': donation})
