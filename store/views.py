import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Product, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY




def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully. You are now logged in.")
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "store/register.html", {"form": form})





def store_home(request):
    products = Product.objects.filter(is_active=True).order_by("id")

    session_id = request.GET.get("session_id")
    if session_id:
        order = Order.objects.filter(stripe_session_id=session_id).first()

        if not order:
            messages.error(request, "We could not find an order for this payment session.")
            return redirect("home")

        if order.status == Order.Status.PENDING:
            try:
                session = stripe.checkout.Session.retrieve(session_id)
            except Exception:
                messages.error(request, "Unable to verify payment status. Please try again.")
                return redirect("home")

            if session.payment_status == "paid":
                order.status = Order.Status.PAID
                order.stripe_payment_intent_id = session.payment_intent
                order.save()
                messages.success(request, "Payment successful! Your order has been confirmed.")
            else:
                messages.error(request, "Payment not completed. No charge was made.")
                return redirect("home")

    paid_orders = Order.objects.none()
    if request.user.is_authenticated:
        paid_orders = (
            Order.objects.filter(user=request.user, status=Order.Status.PAID)
            .prefetch_related("items__product")
            .order_by("-created_at")
        )

    return render(request, "store/index.html", {"products": products, "paid_orders": paid_orders})






@login_required(login_url="login")
def create_checkout(request):
    if request.method != "POST":
        return redirect("home")

    products = Product.objects.filter(is_active=True).order_by("id")

    order = Order.objects.create(
        user=request.user,
        status=Order.Status.PENDING,
    )

    line_items = []
    total = 0

    for product in products:
        raw_qty = request.POST.get(f"qty_{product.id}", "0")
        try:
            qty = int(raw_qty)
        except ValueError:
            qty = 0

        if qty <= 0:
            continue

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            unit_price_inr=product.price_in_inr,
        )

        line_items.append(
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {"name": product.name},
                    "unit_amount": product.price_in_inr * 100,
                },
                "quantity": qty,
            }
        )
        total += product.price_in_inr * qty

    if not line_items:
        order.delete()
        messages.error(request, "Please select at least one product quantity to continue.")
        return redirect("home")

    order.total_amount_inr = total
    order.save()

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=line_items,
            success_url=request.build_absolute_uri("/") + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri("/"),
            client_reference_id=str(order.id),
        )
    except Exception:
        order.status = Order.Status.CANCELED
        order.save()
        messages.error(request, "Payment service is temporarily unavailable. Please try again.")
        return redirect("home")

    order.stripe_session_id = session.id
    order.save()

    return redirect(session.url, code=303)
