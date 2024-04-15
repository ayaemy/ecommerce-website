from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from .models import Item , OrderItem, Order
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm


def product_details(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products_details.html", context)

def checkout(request):
    return render(request, "checkout.html", {})

def login_register(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return render(request, "home.html" ,{})
		else:
			messages.success(request, ("There Was An Error Logging In, Try Again..."))	
			return redirect('login-register.html')	
	else:
		return render(request, "login-register.html", {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You Were Logged Out!"))
	return render(request, "home.html" ,{})

def register(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Registration Successful!"))
			return redirect('core:home')
	else:
		form = RegisterUserForm()
        
	return render(request, 'register.html', {
		'form':form,
		})


from django.views.generic import ListView
from .models import Item

from django.views.generic import ListView
from .models import Item

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get initial queryset of items
        object_list = self.get_queryset()

        # Get additional product (item with a specific slug, e.g., 'test-product-8')
        additional_object_list = Item.objects.filter(slug='test-product-8')

        # Append additional products to the existing object_list
        context['object_list'] = list(object_list) + list(additional_object_list)

        return context

class ItemDetailView(DetailView):
    model = Item
    template_name = "product_details.html"

from django.shortcuts import redirect

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:product_details", slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:product_details", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:product_details", slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:product_details", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product_details", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product_details", slug=slug)


