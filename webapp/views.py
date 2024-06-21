from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FAQ, Order, User, UserFeedback, Product, Delivery, ProductList
from .forms import FAQForm, ProductForm, OrderForm, UserUpdateForm, SignUpForm, LoginForm
from django.forms import formset_factory

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

    product_formset = formset_factory(ProductForm)

    formset = product_formset()
    order_form = OrderForm()

    if request.method == 'POST':
        formset = product_formset(request.POST)
        order_form = OrderForm(request.POST)
        # Here we go for the initial check meaning that the user only dealt with product list
        if formset.is_valid():
            for form in formset:
                form.submitted = True

            # product_forms = formset.save(commit=False)

            if order_form.is_valid():
                order_form.submitted = True

            else:
                order_form.submitted = False
                # TODO: handle order_form errors
                pass

            # TODO: calcualate new prices for each product if stage <= 1

            # TODO: redirect to success page and save all data
            # TODO: success page = stage == 4 with reset of context so the next call will be a new order
            user = request.user
            # This time with saving to DB
            total_price = 0
            product_instances = []

            for form in formset:
                # TODO: proper form save
                product_attrs = {
                    'material': form.cleaned_data['material'],
                    'use_type': form.cleaned_data['use_type'],
                    'length': form.cleaned_data['length'],
                    'width': form.cleaned_data['width'],
                    'height': form.cleaned_data['height'],
                    'handles': form.cleaned_data['handles'],
                    'legs': form.cleaned_data['legs'],
                    'groove': form.cleaned_data['groove'],
                    'price': float(form.cleaned_data['price'][:-2])
                }
                try:
                    product = Product.objects.get(**product_attrs)
                except Product.DoesNotExist as err:
                    product = Product(**product_attrs)

                # product = item.save()
                total_price += product.price * form.cleaned_data['number']
                
                product.save()
                product_instances.append(product)

            delivery_type = request.POST.get('delivery_type')
            order_attrs = {
                'description': order_form.cleaned_data['description'],
                'delivery_type': order_form.cleaned_data['delivery_type'],
                'user': user,
                'delivery': None
            }

            if delivery_type == 1:
                delivery = Delivery(address=order_form.cleaned_data['address'],
                                    description=order_form.cleaned_data['delivery_description'],
                                    price=_DEFAULT_PRICE)
                delivery.save()
                total_price += delivery.price
                order_attrs['delivery'] = delivery

            order_instance = Order(**order_attrs)
            order_instance.save()

            for this_item in product_instances:
                product_list = ProductList(product=this_item, order=order_instance)
                product_list.save()

            print('Everything is saved!')
            return redirect('profile')
        else:
            formset.submitted = False
            # TODO: handle form errors
            pass

    else:
        # Loading page for the first time, we've assigned initials earlier
        pass
    return render(request, 'webapp/order.html', {'formset': formset, 'order_form': order_form})


def profile(request):
    # Redirecting unauthorized users
    if not request.user.is_authenticated:
        return redirect('login')

    # Ensure request.user is a User instance
    user = request.user
    user_orders = Order.objects.filter(user=user)
    user_products = []
    for order in user_orders:
        user_products.append({
            'order': order,
            'products': ProductList.objects.filter(order=order).select_related('product')
        })

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'webapp/profile.html', {'form': form,  'orders': user_products})


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
