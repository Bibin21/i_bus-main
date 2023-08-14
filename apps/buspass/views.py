from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Bus, UserBusPass, Notification
from .forms import BookPassForm
from datetime import date
from .helper import generate_qr_code
from django.db.models import Q

from django.conf import settings

# Create your views here.

@login_required
def home(request):
    """View for home page."""

    notifications = Notification.objects.all().exclude(seen_by__in=[request.user.id])
    
    for notification in notifications:
        notification.seen_by.add(request.user)

    qr_code_data = None
    user_bus_pass = UserBusPass.objects.filter(user=request.user, active=True).first()

    if user_bus_pass:
        if user_bus_pass.expire_at > date.today():
            status = "active"

            data = "Name: {first_name} {last_name},\nBranch: {college_branch},\nStatus: Active,\nExpires on: {expire_at}\nFare: INR {fare}".format(
                first_name=user_bus_pass.user.first_name,
                last_name=user_bus_pass.user.last_name,
                college_branch=user_bus_pass.user.college_branch.branch_name,
                expire_at=str(user_bus_pass.expire_at),
                fare=user_bus_pass.fare
                )
            
            qr_code_data = generate_qr_code(data)

        elif user_bus_pass.expire_at < date.today():
            status = "renew"

            data = "Name: {first_name} {last_name},\nBranch: {college_branch},\nStatus: Expired,\nExpired on: {expire_at}".format(
                first_name=user_bus_pass.user.first_name,
                last_name=user_bus_pass.user.last_name,
                college_branch=user_bus_pass.user.college_branch.branch_name,
                expire_at=str(user_bus_pass.expire_at)
                )
            
            qr_code_data = generate_qr_code(data)
    else:
        status = "no_active_pass"

        data = "No active pass"

        qr_code_data = generate_qr_code(data)

    return render(
        request, 'home.html', {'user': request.user, 'user_bus_pass': user_bus_pass,
                               'status': status, 'qr_code_data': qr_code_data,
                               'notifications': notifications}
    )

@login_required
def select_bus(request):
    """View for selecting bus."""

    buses = Bus.objects.all()

    all_bus_info = []

    for bus in buses:
        bus_info = {
                        'pk': bus.pk,
                        'bus_number': bus.bus_number,
                        'destination': bus.destination,
                        'bus_stops': bus.bus_stops.all().
                                        order_by('distance_from_college').
                                        exclude(id=bus.destination.id)
                    }
        
        all_bus_info.append(bus_info)

    return render(
        request, 'select_bus.html', {'all_bus_info': all_bus_info}
    )

@login_required
def book(request, pk):
    """View for booking pass of selected bus."""

    bus = Bus.objects.get(pk=pk)

    bus_info = {
                "bus_number": bus.bus_number,
                "destination": bus.destination,
                "bus_stops": bus.bus_stops.all().order_by("distance_from_college").exclude(id=bus.destination.pk)
                }

    form = BookPassForm(bus=bus)

    if request.method == "POST":
        form = BookPassForm(request.POST, bus=bus)

        if form.is_valid():
            base_bus_pass_rate = settings.BASE_BUS_PASS_RATE
            distance_from_college = form.cleaned_data['boarding_point'].distance_from_college
            bus_pass_valid_days = (form.cleaned_data['expire_at'] - date.today()).days

            bus_pass_fare = round(base_bus_pass_rate*distance_from_college*bus_pass_valid_days)

            # Create new Bus Pass
            user_bus_pass = UserBusPass.objects.create(user=request.user,
                                                    bus=bus,
                                                    boarding_point=form.cleaned_data['boarding_point'],
                                                    created_at=date.today(),
                                                    expire_at=form.cleaned_data['expire_at'],
                                                    fare=bus_pass_fare,
                                                    active=False)
            
            # Make all other Bus Pass inactive
            UserBusPass.objects.filter(user=request.user).update(active=False)
        
            return redirect('payment', pk=user_bus_pass.pk)

    return render(
        request, 'book.html', {'bus':bus_info, 'form':form}
    )


@login_required
def payment(request, pk):
    """View for payment of booking pass."""

    user_bus_pass = UserBusPass.objects.get(pk=pk)

    if request.method == "POST":
        user_bus_pass.active = True
        user_bus_pass.save()

        return redirect('payment_successful', pk=user_bus_pass.pk)

    return render(
        request, 'payment.html', {'user_bus_pass':user_bus_pass}
    )


@login_required
def payment_successful(request, pk):
    """View for showing payment success message."""

    user_bus_pass = UserBusPass.objects.get(pk=pk)

    return render(
        request, 'payment_successful.html', {'user_bus_pass':user_bus_pass}
    )


@login_required
def view_pass(request, pk):
    """View for showing bus pass."""

    user_bus_pass = UserBusPass.objects.get(pk=pk)

    data = "Name: {first_name} {last_name},\nBranch: {college_branch},\nStatus: Active,\nExpires on: {expire_at}\nFare: INR {fare}".format(
                first_name=user_bus_pass.user.first_name,
                last_name=user_bus_pass.user.last_name,
                college_branch=user_bus_pass.user.college_branch.branch_name,
                expire_at=str(user_bus_pass.expire_at),
                fare=user_bus_pass.fare
                )

    qr_code_data = generate_qr_code(data)

    return render(
        request, 'view_pass.html', {'user_bus_pass': user_bus_pass, 
                                    'qr_code_data': qr_code_data}
    )


@login_required
def cancel_pass(request, pk):
    user_bus_pass = UserBusPass.objects.get(pk=pk)

    if request.method == "POST":
        user_bus_pass.active = False
        user_bus_pass.save()

        return redirect('home')

    return render(
        request, 'cancel_pass.html', {'user_bus_pass': user_bus_pass})