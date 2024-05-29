from home.forms import ReviewForm
from django.shortcuts import render,redirect,get_object_or_404
from home.models import *
from orders.models import *
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render,redirect
from django.contrib import messages


def home(request):
    category=Category.objects.all()
    return render(request,'home/index.html',{'category':category})


def product(request,slug,id):
    product=Product.objects.filter(category__slug=slug,category__id=id)
    product=product.filter(available_quantity__gt=0)

    product_count=product.count()
    context={
        'sitem':product,
        'product_count':product_count
    }
    return render(request,'home/product.html',context)

def productView(request,slug):
    product=Product.objects.filter(product_slug=slug).order_by('discount')

    # review=product.average_rating()
    # reviews=ReviewRating.objects.filter(product=product)
    # print(reviews)
    context={
        'sitem':product,
        # 'review':review
    }
    return render(request,"home/productView.html",context)

def search(request):
    query=request.GET['search_kw']
    product=Product.objects.annotate(search=SearchVector('product_name','category__category_name')).filter(search=query)
    product_count=product.count()
    context={
        'sitem':product,
        'product_count':product_count
    }
    return render(request,"home/product.html",context)

def sellProducts(request):
    if request.method == 'POST':
        product_name=request.POST['product_name']
        category=request.POST['category']
        available_quantity=request.POST['available_quantity']
        quantity=request.POST['quantity']
        min_quantity=request.POST['min_quantity']
        price=request.POST['price']
        discount=request.POST['discount']
        product_image=request.FILES['product_image']
        category=Category.objects.get(category_name=category)
        product=Product(product_name=product_name,category=category,available_quantity=available_quantity,user=request.user,
        quantity=quantity,min_quantity_to_fix_price=min_quantity,price_for_min_quantity=price,discount=discount,product_image=product_image)
    
        try:
            product.product_image1=request.FILES['product_image1']
        except:
            pass
        try:
            product.product_image2=request.FILES['product_image2']
        except:
            pass
        try:
            product.product_image3=request.FILES['product_image3']
        except:
            pass
        try:
            product.product_image4=request.FILES['product_image4']
        except:
            pass
        product.save()
        return redirect('deliveryDetails')
    else:
        category=Category.objects.all()
        context={
            'category':category,
        }
        return render(request,"home/sellProducts.html",context)
    
def cold(request):
    return render(request,"home/cold.html")
def add_cart(request, product_id):
        product = Product.objects.get(id=product_id)
        user=request.user
        try:
            cart = Cart.objects.get(user=user) # get the cart using the cart_id present       
        except Cart.DoesNotExist:
            print("cart doesnt exizst")
            cart = Cart.objects.create(user=user) # create a new cart if no cart is assigned to the session
        try:
                item = CartItem.objects.get(product=product, cart=cart)
                item.quantity += 1
                item.save()

        except Exception:
                print("cart item doesnt exizst")
                item = CartItem.objects.create(product=product, quantity=1, cart=cart,user=request.user)
                item.save()
        return redirect('cartnew')
        


def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cartnew')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    # if request.user.is_authenticated:
    #     cart_item = CartItem.objects.get(product=product, user=request.user)
    # else:
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(product=product, cart=cart,user=request.user,id=cart_item_id)
    cart_item.delete()
    return redirect('cartnew')



def cartnew(request, total=0, quantity=0):
    print("cart invoked")
    try:
        grand_total = 0
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            print(cart)
            cart_items = CartItem.objects.filter(user=request.user,cart=cart)
           
            print(cart_items)
        
        for cart_item in cart_items:
            total += (cart_item.product.discount * cart_item.quantity)
            quantity += cart_item.quantity
        
        grand_total = total
    except Exception as e:
        print(e)

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
    }
    # return render(request,'home/ekart.html',context)
    
    return render(request, 'home/cart1.html', context)

def deliveryDetails(request):
    return render(request,"home/deliveryDetails.html")


def checkout(request):
    print("checkout")
    try:
        grand_total = 0
        total=0
        quantity=0
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        
            print(cart)
            cart_items = CartItem.objects.filter(user=request.user,cart=cart)
           
            print(cart_items)
        
        for cart_item in cart_items:
            total += (cart_item.product.price_for_min_quantity * cart_item.quantity)
            quantity += cart_item.quantity
        
        grand_total = total
    except Exception as e:
        print(e)

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
    }

    return render(request,'home/checkout.html',context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
            
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        messages.success(request, 'Thank you! Your message has been submitted.')
        return redirect('/')
    return render(request,"home.html")

# Farmers Dashboard
def farmer_requests(request):
    op=OrderProduct.objects.filter(product__user=request.user,ordered=False)
    context={
        'op':op,
    }
    return render(request,"dashboards/farmer_db.html",context)


# check ones there is a confusion
def confirm_otp(request,id):
    op=OrderProduct.objects.get(id=id)
    if request.method=="POST":
        enteredopt=request.POST['otp']
        if enteredopt==op.order.deliver_otp:
            op.ordered=True
            op.save()
    
    o=len(OrderProduct.objects.filter(id=op.order.id,ordered=False))
    if o==0:
        op.order.ordered=True
        op.order.save()
    return redirect('farmer_requests')
