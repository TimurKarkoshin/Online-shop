from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.http import HttpRequest, HttpResponse
from .forms import OrderStep1Form, DeliveryStep2Form, DeliveryStep3Form
from order.services.make_order import MakeOrder
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import Order, ProductInOrder
from django.utils.translation import gettext_lazy as _


class MakeOrderStepOne(LoginRequiredMixin, View):
    """
    Класс создания заказа шаг первый
    """

    def get(self, request: HttpRequest) -> HttpRequest:
        context = {
            "form_profile": OrderStep1Form,
        }
        return render(request, "order/make-order-step1.jinja2", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = OrderStep1Form(request.POST)
        if form.is_valid():
            make_order = MakeOrder(request=request)
            make_order.writing_data_order_in_session(key="step_1", cleaned_data=form.cleaned_data)
        return redirect(to="order:make_order_step_2")


class MakeOrderStepTwo(LoginRequiredMixin, View):
    """
    Класс создания заказа шаг второй
    """

    def get(self, request: HttpRequest) -> HttpRequest:
        context = {
            "form_delivery": DeliveryStep2Form,
        }
        return render(request, "order/make-order-step2.jinja2", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = DeliveryStep2Form(request.POST)
        if form.is_valid():
            make_order = MakeOrder(request=request)
            make_order.writing_data_order_in_session(key="step_2", cleaned_data=form.cleaned_data)
        return redirect(to="order:make_order_step_3")


class MakeOrderStepThree(LoginRequiredMixin, View):
    """
    Класс создания заказа шаг третий
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form_delivery": DeliveryStep3Form,
        }
        return render(request, "order/make-order-step3.jinja2", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = DeliveryStep3Form(request.POST)
        if form.is_valid():
            make_order = MakeOrder(request=request)
            make_order.writing_data_order_in_session(key="step_3", cleaned_data=form.cleaned_data)
        return redirect("order:make_order_step_4")


class MakeOrderStepFour(LoginRequiredMixin, View):
    """
    Класс создания заказа шаг четвертый - подтверждение и оплата заказа
    При неполноте данных, недостаточном балансе или отсутствия товара рендерит страницу-ошибку
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        order = MakeOrder(request=request)
        error = order.cheking_func()
        if not error:
            order = Order.objects.filter(user=request.user).select_related("order_status", "delivery").last()
            products = ProductInOrder.objects.select_related("product").filter(order=order)
            context = {"order": order, "products": products, "sum": sum([product.price for product in products])}
            if order.delivery.delivery_type == _("Экспресс доставка"):
                context["delivery_sum"] = context["sum"] / 100 * 5

            return render(request, "order/make-order-step4.jinja2", context=context)
        return render(request, "order/page-error.jinja2", {"error": error})


class PaymentView(LoginRequiredMixin, View):
    """
    Класс для проведения оплаты товара пользователем
    """

    template_name = "order/payment/payment.jinja2"

    def get(self, request: HttpRequest, order_pk) -> HttpResponse:
        order = Order.objects.select_related("delivery").get(user=request.user, pk=order_pk)
        if order.delivery.pay == _("Онлайн со случайного счета"):
            self.template_name = "order/payment/payment-someone.jinja2"

        return render(request, self.template_name)

    def post(self, request: HttpRequest, order_pk) -> HttpResponse:
        # str_card_number = request.POST["numero1"]
        # int_card_numaber = int(str_card_number.replace(" ", ""))
        return redirect(to="order:payment_progress", order_pk=order_pk)


class PaymentProgressView(LoginRequiredMixin, ListView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "order/payment/payment-progress.jinja2")


class HistoryOrdersView(LoginRequiredMixin, ListView):
    context_object_name = "products"
    template_name = "order/history-orders.jinja2"

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user)
        products = ProductInOrder.objects.filter(order__in=orders).select_related("product", "order")
        return products


class OneOrderView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, order_pk) -> HttpResponse:
        order = Order.objects.select_related("order_status", "delivery").get(pk=order_pk, user=request.user)
        products = ProductInOrder.objects.select_related("product").filter(order_id=order_pk)

        context = {
            "order": order,
            "products": products,
            "status": order.order_status,
            "delivery": order.delivery,
            "total": sum([product.price for product in products]),
        }
        if order.delivery.delivery_type == _("Экспресс доставка"):
            context["delivery_sum"] = context["total"] / 100 * 5

        return render(request, "order/one-order.jinja2", context=context)
