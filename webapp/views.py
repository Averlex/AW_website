from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FAQ, Order, User, UserFeedback, Product
from .forms import FAQForm, OrderForm, UserUpdateForm, SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
import random
from django.contrib import messages
from django.core.exceptions import ValidationError


def index(request):
    return render(request, 'webapp/index.html')


def gallery(request):
    # Sample photos context; replace with actual photo context
    photos = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]
    return render(request, 'webapp/gallery.html', {'photos': photos})


def faq(request):
    # Getting random top-3 FAQs to display on the page
    faqs = list(FAQ.objects.all())
    random.shuffle(faqs)
    faqs = faqs[:3]

    # Actions on submit button
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = FAQForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['text']
                rate = form.cleaned_data['rate']

                # TODO: user is unlinked to a feedback
                feedback = UserFeedback(text=text, rate=rate, feedback_type=1, user=request.user)
                feedback.save()
                form.save()

                # TODO: change form for a success message
                return redirect('faq')
        else:
            form = FAQForm()
            # TODO: login button here
            pass
    else:
        form = FAQForm()
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


def signup_view(request):
    form = None
    if request.method == 'POST':
        try:
            form = SignUpForm(request.POST)
        except ValidationError as err:
            # Field were filled incorrectly
            messages.error(request, err)
            return render(request, 'webapp/signup.html', {'form': form})

        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.set_password(form.cleaned_data.get('password'))
            save_form.save()

            user = User(username=save_form.username, password=save_form.password, name=save_form.name,
                        email=save_form.email, phone=save_form.phone)
            user.save()

            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('profile')
        else:
            return render(request, 'webapp/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'webapp/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'webapp/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'webapp/logout.html', {})


def policy(request):
    return render(request, 'webapp/policy.html', {})
