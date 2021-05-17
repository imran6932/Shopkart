from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Customer,Product,Cart,Order_placed
from django.views import View
from django.views.generic import ListView
from .forms import CustomerRegistraion, CustomerLogin, CustomerProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# All Products  Class Based View for Home Page
class ProductView(View):
    def get(self,request):
        topwear = Product.objects.filter(category='TW')
        bottomwear = Product.objects.filter(category='BW')
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        book = Product.objects.filter(category='B')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        context = {'topwear':topwear, 'bottomwear':bottomwear,'mobile':mobile,'laptop':laptop, 'book':book, 'totalitem':totalitem}
        return render(request,'app/home.html', context)

# Single Product Details Class Based View
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        product_already_in_cart = False
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            product_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user))
        context = {'product':product, 'product_already_in_cart':product_already_in_cart, 'totalitem':totalitem}
        return render(request, 'app/productdetail.html', context)

# Add to Cart button Function Based View
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return redirect('/cart', {'totalitem':totalitem})

@login_required
def buy(request):
    user = request.user
    product_id = request.GET.get('prod_id_buy')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        add = Customer.objects.filter(user=user)
        totalitem = 0
        totalitem = len(Cart.objects.filter(user=request.user))
        amount = 0
        shipping_charge = 0
        totalamount = 0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discount_price)
                amount += temp_amount
                if amount < 499:
                    shipping_charge = 50
                    totalamount = amount + shipping_charge
                else:
                    shipping_charge = 'Free'
                    totalamount = amount
    context =  {'cart':cart , 'add':add, 'totalamount':totalamount, 'amount':amount, 'shipping_charge':shipping_charge, 'totalitem':totalitem}
    return redirect('/checkout', context)

# Show Cart items Function Based View
@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        final_amount = 0
        amount = 0
        shipping_charge = 0
        discount = 0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.price)
                amount += temp_amount
                discount_temp = (p.product.price - p.product.discount_price) * p.quantity
                discount += discount_temp
                final_amount = amount - discount
                if final_amount < 499:
                    shipping_charge = 50
                    totalamount = final_amount + shipping_charge
                else:
                    shipping_charge = 'Free'
                    totalamount = final_amount
            context = {'carts':cart, 'totalamount':totalamount, 'amount':amount, 'shipping_charge':shipping_charge, 'totalitem':totalitem, 'discount':discount}
            return render(request, 'app/addtocart.html', context)
        else:
            return render(request, 'app/emptycart.html')

# Cart items increase Function Based View
@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        amount = 0
        final_amount = 0
        shipping_charge = 0
        discount = 0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.price)
                amount += temp_amount
                discount_temp = (p.product.price - p.product.discount_price) * p.quantity
                discount += discount_temp
                final_amount = amount - discount
                if final_amount < 499:
                    shipping_charge = 50
                    totalamount = final_amount + shipping_charge
                else:
                    shipping_charge = 'Free'
                    totalamount = final_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'shipping_charge': shipping_charge,
            'totalamount': totalamount,
            'discount': discount
        }
        return JsonResponse(data)

# Cart Items Decrease Function Based View
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))        
        c.quantity -=1
        if c.quantity >0:
            c.save()
            amount = 0
            final_amount = 0
            shipping_charge = 0
            discount = 0
            cart_product = [p for p in Cart.objects.all() if p.user == request.user]
            if cart_product:
                for p in cart_product:
                    temp_amount = (p.quantity * p.product.price)
                    amount += temp_amount
                    discount_temp = (p.product.price - p.product.discount_price) * p.quantity
                    discount += discount_temp
                    final_amount = amount - discount
                    if final_amount < 499:
                        shipping_charge = 50
                        totalamount = final_amount + shipping_charge
                    else:
                        shipping_charge = 'Free'
                        totalamount = final_amount
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'shipping_charge': shipping_charge,
                'totalamount': totalamount,
                'discount': discount
            }
            return JsonResponse(data)

# Remove items From Cart Function Based View
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0
        final_amount = 0
        totalamount = 0
        shipping_charge = 0
        discount = 0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.price)
                amount += temp_amount
                discount_temp = (p.product.price - p.product.discount_price) * p.quantity
                discount += discount_temp
                final_amount = amount - discount
                if final_amount < 499:
                    shipping_charge = 50
                    totalamount = final_amount + shipping_charge
                else:
                    shipping_charge = 'Free'
                    totalamount = final_amount
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        
        data = {
            'status': 1,
            'amount': amount,
            'shipping_charge': shipping_charge,
            'totalamount': totalamount,
            'discount': discount,
            'totalitem':totalitem
        }
        return JsonResponse(data)
    
   


# All Order Items Function Based View
@login_required
def orders(request):
    op = Order_placed.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html', {'order_placed':op, 'totalitem':totalitem})


# Customer Address Function Based View
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    context = {'add':add, 'active':'btn-primary', 'totalitem':totalitem}
    return render(request, 'app/address.html', context)


# Change Password Function Based View
@login_required
def change_password(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/changepassword.html', {'totalitem':totalitem})


# All Mobiles category Show Function Based View
def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Samsung' or data == 'Xiaomi' or data == 'Apple' or data == 'Realme' or data == 'Lg' or data == 'Poco':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discount_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discount_price__gt=10000)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html', {'mobiles':mobiles, 'totalitem':totalitem})

# All Laptop category Show Function Based View
def laptop(request,data=None):
    if data == None:
        laptop = Product.objects.filter(category='L')
    elif data == 'Hp' or data == 'Apple' or data == 'Microsoft' or data == 'Accer' or data == 'AleinWare' or data == 'Msi':
        laptop = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptop = Product.objects.filter(category='L').filter(discount_price__lt=40000)
    elif data == 'above':
        laptop = Product.objects.filter(category='L').filter(discount_price__gt=40000)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/laptop.html',{'laptop':laptop, 'totalitem':totalitem})

# All Books category Show Function Based View
def book(request,data=None):
    if data == None:
        book = Product.objects.filter(category='B')
    elif data == 'JeffKeller' or data == 'BobMighlani' or data == 'NapoleanHill' or data == 'George' or data == 'RobinSharma' or data == 'Morgan' or data == 'Robert' or data == 'Kalam' or data == 'JosephMurphy':
        book = Product.objects.filter(category='B').filter(brand=data)
    elif data == 'below':
        book = Product.objects.filter(category='B').filter(discount_price__lt=200)
    elif data == 'above':
        book = Product.objects.filter(category='B').filter(discount_price__gt=200)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/book.html',{'book':book, 'totalitem':totalitem})

# All Topwears category Show Function Based View
def topwear(request,data=None):
    if data == None:
        topwear = Product.objects.filter(category='TW')
    elif data == 'Spyker' or data == 'Lee' or data == 'Pepe_Jeans':
        topwear = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwear = Product.objects.filter(category='TW').filter(discount_price__lt=500)
    elif data == 'above':
        topwear = Product.objects.filter(category='TW').filter(discount_price__gt=500)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/topwear.html',{'topwear':topwear, 'totalitem':totalitem})


# All Bottomwear category Show Function Based View
def bottomwear(request,data=None):
    if data == None:
        bottomwear = Product.objects.filter(category='BW')
    elif data == 'Spyker' or data == 'Lee' or data == 'Pepe_Jeans':
        bottomwear = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottomwear = Product.objects.filter(category='BW').filter(discount_price__lt=1500)
    elif data == 'above':
        bottomwear = Product.objects.filter(category='BW').filter(discount_price__gt=1500)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/bottomwear.html',{'bottomwear':bottomwear, 'totalitem':totalitem})

# Customer Login Class Based View
class Customer_Login(View):
    def get(self,request):
        form = CustomerLogin()
        return render(request, 'app/login.html',{'form':form})
    def post(self,request):
        if request.method == 'POST':
            form = CustomerLogin(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect('/')
            else:
                return render(request, 'app/login.html',{'form':form})


# Customer Registration Class Based View
class CustomerReg(View):
    def get(self,request):
        form = CustomerRegistraion()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        if request.method == 'POST':
            form = CustomerRegistraion(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Registration Successfully')
        else:
            form = CustomerRegistraion()
        return render(request, 'app/customerregistration.html',{'form':form})


# Customer Add Address Profile Class Based View
@method_decorator(login_required, name='dispatch')
class Customer_profile(View):
    def get(self, request):
        form = CustomerProfile()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/add_profile.html',{'form':form, 'totalitem':totalitem})
    def post(self, request):
        form = CustomerProfile(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            pin = form.cleaned_data['pin']
            state = form.cleaned_data['state']
            reg = Customer(user=usr, name=name, locality=locality, city=city, pin=pin, state=state)
            reg.save()
            form = CustomerProfile()
            messages.success(request,'Address Added')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/add_profile.html',{'form':form, 'totalitem':totalitem})

# Delete Address Function Based View
@login_required
def delete_customer_add(request,id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        pi.delete()
        messages.warning(request, 'Address Deleted')
        return redirect('address')


# Update Address Function Based View
@login_required
def update_customer_add(request,id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        fm = CustomerProfile(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Address updated')
            
    else:
        pi = Customer.objects.get(pk=id)
        fm = CustomerProfile(instance=pi)
    return render(request, 'app/update.html', {'form':fm})

# My Profile Function Based View        
@login_required
def profile_page(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/profile.html', {'totalitem':totalitem})

# Cart Items Checkout Function Based View
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart = Cart.objects.filter(user=user)
    amount = 0
    totalamount = 0
    shipping_charge = 0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            print(temp_amount)
            amount += temp_amount
            if amount < 499:
                shipping_charge = 50
                totalamount = amount + shipping_charge
            else:
                shipping_charge = 'Free'
                totalamount = amount
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    context = {'add':add, 'cart':cart, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem, 'shipping_charge':shipping_charge}
    return render(request, 'app/checkout.html', context)

# Payment Done Function Based View
@login_required
def payment_done(request):
    try:
        custid = request.GET.get('custid')
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=request.user)
        for c in cart:
            Order_placed(user=request.user, customer=customer, product=c.product, quantity=c.quantity).save()
            c.delete()
        return redirect('/orders')
    except:
        return HttpResponse('<h1>Please select address first then try to make payment.</h1>')

# Search Bar function Based View
def search_bar(request):
    search = request.GET.get('search')
    query = Product.objects.filter(title__contains=search)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/search.html', {'search':search, 'query':query, 'totalitem':totalitem})