from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FAQ, Order, User, UserFeedback, Product, Delivery
from .forms import FAQForm, ProductForm, OrderForm, UserUpdateForm, SignUpForm, LoginForm
from django.forms import modelformset_factory

from django.contrib.auth import login, authenticate, logout
import random
import time

# TODO: fix delivery price
_DEFAULT_PRICE = 666


def index(request):
    # TODO: add logo
    # TODO: add button 'наверх' instead of link
    # TODO: change policy and terms links
    # TODO: make footer stay at the bottom of the page
    # TODO: deal with footer svg (center)
    # TODO: navbar fix
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


def order(request):
    # Redirect to profile page if the user is already authenticated
    if not request.user.is_authenticated:
        return redirect('profile')

    fields = ('length', 'width', 'height', 'handles', 'legs', 'groove', 'material', 'use_type', 'price')
    product_formset = modelformset_factory(Product, fields=fields)

    class Stages():
        stages = {1: 'product', 2: 'details', 3: 'confirm', 4: 'done'}

        def __init__(self):
            self.stage = 1

        def inc_stage(self):
            self.stage += 1
            return self.stage

        def dec_stage(self):
            self.stage -= 2
            return self.stage

    stage = Stages()

    # For tracking the state of the page
    # stages = {1: 'product', 2: 'details', 3: 'confirm', 4: 'done'}
    #
    # if request.method == 'POST':
    #     data = request.POST
    # else:
    #     data = request.GET

    # Getting defaults (GET case)
    # stage = data.get('stage', 1)
    # formset = data.get('formset', product_formset())
    # order_form = data.get('order_form', OrderForm())

    formset = product_formset(queryset=Product.objects.none())
    order_form = OrderForm()

    if request.method == 'POST':
        formset = product_formset(request.POST)
        # Here we go for the initial check meaning that the user only dealt with product list
        if formset.is_valid():
            product_forms = formset.save(commit=False)

            # TODO: calcualate new prices for each product if stage <= 1

            stage.stage += 1
            if stage.stage <= 3:
                return render(request, 'webapp/order.html',
                              {'formset': formset, 'order_form': order_form, 'stage': stage})
            else:
                # TODO: redirect to success page and save all data
                # TODO: success page = stage == 4 with reset of context so the next call will be a new order
                user = request.user
                # This time with saving to DB
                total_price = 0
                for item in product_forms:
                    product = item.save()
                    total_price += product.price

                if order_form.delivery_type.value() == 1:
                    delivery = Delivery(address=order_form.address.value(), description=order_form.delivery_description.value(),
                                        price=_DEFAULT_PRICE)
                    total_price += delivery.price
                else:
                    delivery = None

                order_instance = Order(delivery_type=order_form.delivery_type.value(), description=order_form.description.value(),
                                       user=user, delivery=delivery, price=total_price)
                order_instance.save()

                return redirect('profile')
        else:
            # TODO: handle form errors
            pass
    else:
        # Loading page for the first time, we've assigned initials earlier
        pass
    return render(request, 'webapp/order.html', {'formset': formset, 'order_form': order_form, 'stage': stage})


def profile(request):
    # Redirecting unauthorized users
    if not request.user.is_authenticated:
        return redirect('login')

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
    # TODO: set group by default

    # Redirect to profile page if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.errors:
            return render(request, 'webapp/signup.html', {'form': form})

        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.set_password(form.cleaned_data.get('password'))

            user = User(username=save_form.username, password=save_form.password, name=save_form.name,
                        email=save_form.email, phone=save_form.phone)
            user.save()

            form.success = True
            login(request, user)
            # TODO: sleep is cringe
            time.sleep(3)
            return redirect('profile')
        else:
            return render(request, 'webapp/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'webapp/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'webapp/login.html', {'form': form})


def logout_view(request):
    # TODO: something more elegant (e.g., suggestion to logout)
    # TODO: custom 404 page
    if not request.user.is_authenticated:
        return redirect('home')

    logout(request)
    return render(request, 'webapp/logout.html', {})


def policy(request):
    return render(request, 'webapp/policy.html', {})
