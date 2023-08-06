from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.views.decorators.csrf import csrf_exempt  
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .forms import CustomerForm
from django.db.models import Max
import uuid
from django.db.models import Q



# Create your views here.
def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'navigation.html')

def about(request):
    return render(request, 'about.html')




def adminLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Login Successfully")
                return redirect('admin_dashboard')
            else:
                messages.success(request, "Invalid Credentials")
        except:
            messages.success(request, "Invalid Credentials")
    return render(request, 'admin_login.html')

def logoutuser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('admin_login')


def adminHome(request):
    if not request.user.is_staff:
      return redirect('admin_login')
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    context = {'cart_count': cart_count, 'notify_count': notify_count}
    return render(request, 'admin_base.html', context)


def admin_dashboard(request):
    if not request.user.is_staff:
      return redirect('admin_login')
    category_count = Category.objects.count()
    product_count = Product.objects.count()
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    invoice_count = Customer.objects.count()
    context = {
        'category_count': category_count,
        'product_count': product_count, 
        'cart_count': cart_count,
        'notify_count': notify_count,
        'invoice_count': invoice_count
    }
    return render(request, 'admin_dashboard.html', context=context)


def admin_change_password(request):
    if not request.user.is_staff:
      return redirect('admin_login')
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('admin_login')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')



def add_category(request):
    if not request.user.is_staff:
      return redirect('admin_login')
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request, "Category Added")
        return redirect('view_category')
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    context = {'cart_count': cart_count, 'notify_count': notify_count}
    return render(request, 'add_category.html', context) 


def view_category(request):
    if not request.user.is_staff:
      return redirect('admin_login')
    category = Category.objects.all()
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    context = {'category': category, 'cart_count': cart_count, 'notify_count': notify_count}
    return render(request, 'view_category.html', context) 


def edit_category(request, pid):
    if not request.user.is_staff:
      return redirect('admin_login')
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        messages.success(request, "Category Updated")
        return redirect('view_category')
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    context = {'category': category, 'cart_count': cart_count, 'notify_count': notify_count}
    return render(request, 'edit_category.html', context)


def delete_category(request, pid):
    if not request.user.is_staff:
      return redirect('admin_login')
    category = Category.objects.get(id=pid)
    category.delete()
    messages.success(request, "Category Deleted")
    return redirect('view_category') 




def add_product(request):
    if not request.user.is_staff:
      return redirect('admin_login')
    if request.method == 'POST':
        category = Category.objects.get(id=request.POST['category'])
        name = request.POST['name']
        cost_price = request.POST['cost_price']
        selling_price = request.POST['selling_price']
        stock = int(request.POST['stock'])
        description = request.POST['description']
        product = Product(category=category, name=name, cost_price=cost_price, selling_price=selling_price, stock=stock, description=description)
        product.save()
        return redirect('view_product')
    categories = Category.objects.all()
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    context = {'categories': categories, 'cart_count': cart_count, 'notify_count': notify_count}
    return render(request, 'add_product.html', context)




def view_product(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    search_query = request.GET.get('q')
    products = Product.objects.all()
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(product_id__icontains=search_query) | Q(category__name__icontains=search_query))
    context = {
        'products': products,
        'cart_count': cart_count, 
        'notify_count': notify_count
    }
    return render(request, 'view_product.html', context)






def edit_product(request, pk):
    if not request.user.is_staff:
      return redirect('admin_login')
    product = Product.objects.get(pk=pk)
    categories = Category.objects.all()
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    context = {
        'product': product,
        'categories': categories, 
        'cart_count': cart_count, 
        'notify_count': notify_count
    }
    if request.method == 'POST':
        product.category_id = request.POST['category']
        product.name = request.POST['name']
        product.cost_price = request.POST['cost_price']
        product.selling_price = request.POST['selling_price']
        product.stock = int(request.POST['stock'])
        product.description = request.POST['description']
        product.save()
        return redirect('view_product')
    return render(request, 'edit_product.html', context)


def delete_product(request, product_id):
    if not request.user.is_staff:
      return redirect('admin_login')
    product = Product.objects.get(pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('view_product')
  



  


def notification_list(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    products = Product.objects.all().order_by('stock')
    notifications = []
    for product in products:
        try:
            notification = Notification.objects.filter(product=product).latest('created_at')
            notifications.append(notification)
        except Notification.DoesNotExist:
            pass
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    context = {'notifications': notifications, 'cart_count': cart_count, 'notify_count': notify_count}
    return render(request, 'notification.html', context)


@receiver(post_save, sender=Product)
def product_stock_change(sender, instance, **kwargs):
    if instance.stock < 100:
        try:
            notification = Notification.objects.get(product=instance)
            notification.message = f"Stock of {instance.name} is now {instance.stock}."
            notification.save()
        except Notification.DoesNotExist:
            message = f"Stock of {instance.name} is now {instance.stock}."
            Notification.objects.create(product=instance, message=message)
    elif instance.stock >= 100:
        Notification.objects.filter(product=instance).delete()


def add_stock(request, pk):
    if not request.user.is_staff:
        return redirect('admin_login')
    product = Product.objects.get(pk=pk)
    notification = Notification.objects.get(product=product)
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        product.stock += quantity
        product.save()
        messages.success(request, f"{quantity} units added to stock successfully!")
        return redirect('notification_list')
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    context = {'product': product, 'cart_count': cart_count, 'notify_count': notify_count}
    return render(request, 'add_stock.html', context)







def add_to_cart(request, pk):
    if not request.user.is_staff:
      return redirect('admin_login')
    product = Product.objects.get(pk=pk)
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    if request.method == 'POST':
        quantity = request.POST['quantity']
        if int(quantity) > product.stock:
            messages.error(request, 'Requested quantity not available in stock')
        else: 
            product.stock -= int(quantity)
            product.save()
            cart_items = Cart.objects.filter(product=product)
            if cart_items.exists():
              cart_item = cart_items.first()
              cart_item.quantity += int(quantity)
              cart_item.save()
            else:
              cart_item = Cart(product=product, quantity=quantity)
              cart_item.save()
            messages.success(request, 'Item added to cart successfully!')
            return redirect('view_cart')
    context = {'product': product, 'cart_count': cart_count, 'notify_count': notify_count}
    return render(request, 'add_to_cart.html', context)


def view_cart(request):
    if not request.user.is_staff:
      return redirect('admin_login')
    invno = 100001 if Customer.objects.count() == 0 else Customer.objects.aggregate(max=Max('invnumber'))["max"]+1
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_mobile = request.POST.get('customer_mobile')
        payment_mode = request.POST.get('payment_mode')
        data = Customer.objects.create(customer_name=customer_name, invnumber=invno, customer_mobile=customer_mobile, payment_mode=payment_mode)
        # cart_items = Cart.objects.all()

    #     customer = Invoice.objects.create(
    #         customer_name=customer_name,
    #         customer_mobile=customer_mobile,
    #         payment_mode=payment_mode,
    #     )
    #     customer.cart_items.set(cart_items)
        messages.success(request, f"Invoice generated with invoice number : {invno} ")
        Cart.objects.all().delete()
        return redirect('view_cart')
    cart_items = Cart.objects.all().order_by('product__product_id')
    subtotal = 0
    for item in cart_items:
        item.total_price = item.product.selling_price * item.quantity
        subtotal += item.total_price
    grand_total = subtotal
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    context = {'cart_items': cart_items, 'subtotal': subtotal, 'grand_total': grand_total, 'cart_count': cart_count, 'notify_count': notify_count, 'invno': invno}
    return render(request, 'view_cart.html', context)


def remove_from_cart(request, pk):
    if not request.user.is_staff:
      return redirect('admin_login')
    cart_item = get_object_or_404(Cart, pk=pk)
    product = cart_item.product
    product.stock += cart_item.quantity
    product.save()
    cart_item.delete()
    return redirect('view_cart')








def view_invoice_history(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    search_query = request.GET.get('que')
    invoices = Customer.objects.all()
    cart_count = Cart.objects.count()
    notify_count = Notification.objects.count()
    if search_query:
        invoices = invoices.filter(
            Q(customer_name__icontains=search_query) |
            Q(invnumber__icontains=search_query) |
            Q(customer_mobile__icontains=search_query) |
            Q(payment_mode__icontains=search_query)
        )
    context = {
        'invoices': invoices,
        'cart_count': cart_count,
        'notify_count': notify_count,
    }
    return render(request, 'view_invoice_history.html', context)


