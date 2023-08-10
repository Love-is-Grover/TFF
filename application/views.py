from django.shortcuts import render,redirect
from .models import Category,Product,Order,Feedback
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

def home(request) :
    category = Category.objects.all()
    product = Product.objects.all()
    special = Product.objects.filter(special_product = 1)
    sale = Product.objects.filter(on_sale = 1)
    content = {
        "category" : category,
        "product" : product,
        "special_product" : special,
        "sale" : sale,
        "title" : "Home",
    }
    return render(request,"home.html",content)


def product_details(request,product_slug):
    if Product.objects.filter(slug = product_slug):
        all_products = Product.objects.all()
        product = Product.objects.filter(slug = product_slug).first()
        try:
            product_id = request.session['cart'][str(product.id)]['product_id']
        except:
            product_id = None
        content = {
            "product" : product,
            "title" : product_slug,
            "added" : product_id,
            "recommend" : all_products
        }
        return render(request,'detail.html',content)
    else:
        messages.error(request,"something went wrong")
        return redirect("home")
    return redirect("home")


@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    messages.info(request,"Product added to cart successfully")
    return redirect(f"/product/{product.slug}")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_detail(request):
    try:
        product_id = len(request.session['cart'])
    except:
        product_id = None
    if product_id == None or product_id == 0:
        messages.info(request,"Cart is empty")
        return redirect("home")
    else:
        cart = Cart(request)
        category = []
        for i in cart.cart:
            category.append(Product.objects.get(id=i).category)
        content = {
            "title" : "Cart",
            "category" : category,
        }
        # print(cart.cart)
        return render(request, 'cart.html',content)
    

@login_required(login_url="login")
def order(request):
    u_id = request.session.get('_auth_user_id')
    user = User.objects.get(pk = u_id)
    order = Order.objects.filter(user = user)
    content = {
        "title" : "Order",
        "order" : order,
    }
    return render(request,"order.html",content)

@login_required(login_url="login")
def checkout(request):
    if request.method == "POST":
        mobile = request.POST.get('phone')
        house_no = request.POST.get('hno')
        location = request.POST.get('location')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        landmark = request.POST.get('landmark')
        cart = request.session.get('cart')
        u_id = request.session.get('_auth_user_id')
        user = User.objects.get(pk = u_id)
        for i in cart:
            total = float(cart[i]['price']) * int(cart[i]['quantity'])
            prod_qty = Product.objects.get(id = cart[i]['product_id'])
            if prod_qty.quantity == 0:
                messages.info(request,"Product not available for the moment")
            elif prod_qty.quantity < cart[i]["quantity"] :
                messages.info(request,"Product quantity not available at the moment, Please decrease the quantity.")
            elif len(str(mobile)) > 10 or len(str(mobile)) <10:
                messages.info(request,"The mobile number was invalid. it should be 10 digit valid mobile number")
            elif len(str(pincode)) > 6 or len(str(pincode)) <6:
                messages.info(request,"You have entered a wrong pincode")
            elif str(pincode)[0:4] != "1100":
                print(str(pincode)[0:5])
                messages.info(request,"Sorry! we dont deliver at your place.")
            else:
                order = Order(
                    user = user,
                    product = Product.objects.get(pk = cart[i]['product_id']),
                    price = cart[i]['price'],
                    quantity = cart[i]['quantity'],
                    phone = mobile,
                    total = total,
                    house = house_no,
                    location = location,
                    city = city,
                    pincode = pincode,
                    landmark = landmark
                )
                prod_qty.quantity = (prod_qty.quantity) - (cart[i]['quantity'])
                prod_qty.save()
                order.save()
                request.session['cart'] = {}
                messages.success(request,"Order Placed Successfully")
                return redirect("order")
            return redirect("cart_detail")
    
@login_required(login_url="login")
def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('mobile')
        message = request.POST.get('message')

        fbk = Feedback(
            name = name,
            email = email,
            phone = phone,
            message = message,
        )
        messages.success(request,"Feedback sent Successfully!")
        fbk.save()
    return redirect("home")
    