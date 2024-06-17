from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FAQ, Order, User, UserFeedback, Product
from .forms import FAQForm, OrderForm, UserUpdateForm
import random


def index(request):
    return render(request, 'webapp/index.html')


def gallery(request):
    # Sample photos context; replace with actual photo context
    photos = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]
    return render(request, 'webapp/gallery.html', {'photos': photos})


def faq(request):
    faqs = list(FAQ.objects.all())
    random.shuffle(faqs)
    faqs = faqs[:3]

    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faq')
    else:
        form = FAQForm()
    form.fields['question'].label = ''
    return render(request, 'webapp/faq.html', {'faqs': faqs, 'form': form})


@login_required
def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_form = form.save(commit=False)
            order_form.user = request.user
            order_form.save()
            return redirect('profile')
    else:
        form = OrderForm()
    return render(request, 'webapp/order.html', {'form': form})


@login_required
def profile(request):
    # Ensure request.user is a User instance
    user = request.user
    user_orders = Order.objects.filter(user=user)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'webapp/profile.html', {'orders': user_orders, 'form': form})
