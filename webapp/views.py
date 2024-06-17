from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FAQ, Order, User, UserFeedback, Product
from .forms import FAQForm, OrderForm, UserUpdateForm

def landing_page(request):
    return render(request, 'webapp/landing_page.html')

def gallery(request):
    # Sample photos context; replace with actual photo context
    photos = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]
    return render(request, 'webapp/gallery.html', {'photos': photos})

def faq(request):
    faqs = FAQ.objects.all()
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faq')
    else:
        form = FAQForm()
    return render(request, 'webapp/faq.html', {'faqs': faqs, 'form': form})

@login_required
def make_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('personal_page')
    else:
        form = OrderForm()
    return render(request, 'webapp/make_order.html', {'form': form})

@login_required
def personal_page(request):
    user = request.user  # Ensure request.user is a User instance
    user_orders = Order.objects.filter(user=user)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('personal_page')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'webapp/personal_page.html', {'orders': user_orders, 'form': form})
