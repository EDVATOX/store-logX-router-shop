from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Category, Product, Cart, CartItem, Vote, SingleVote
from django.contrib import messages
import random


def store(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    vote_query = Vote.objects.filter(is_active=True)
    vote: Vote = vote_query.first() if vote_query.exists() else None
    all_agrees = 0
    all_disagrees = 0
    if vote:
        try:
            all_single_votes = vote.singlevote_set.all()
            all_agrees = int(all_single_votes.filter(is_agree=True).count()/all_single_votes.count() * 100)
            all_disagrees = int(all_single_votes.filter(is_agree=False).count()/all_single_votes.count() * 100)
        except ZeroDivisionError:
            pass
    user_can_vote = True
    if vote:
        user = request.user
        if vote.singlevote_set.filter(user=user.id).exists():
            user_can_vote = False
    context = {
        'products': products,
        'products2': products,
        'categories': categories,
        'vote': vote,
        'agree': all_agrees,
        'disagree': all_disagrees,
        'can_vote': user_can_vote,
    }

    return render(request, 'index.html', context=context)


def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})


def search(request):
    ctx = {}
    if request.method == 'POST':
        if 'keyword' in request.POST:
            keyword = request.POST['keyword']
            if keyword:
                products = Product.objects.filter(title__icontains=keyword)
                product_count = products.count()
                ctx = {
                    "products": products,
                    "item_count": product_count
                }
    return render(request, 'search.html', ctx)


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.num_of_buy >= 1:
        product.num_of_buy -= 1
        product.save()
        cart, created = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        return redirect('profile')


@login_required(login_url='login')
def add_quantity(request, product_id):
    item, created = CartItem.objects.get_or_create(id=product_id)
    if item.product.num_of_buy == 0:
        return redirect('profile')
    item.quantity += 1
    item.product.num_of_buy -= 1
    item.product.save()
    item.save()
    return redirect('profile')


@login_required(login_url='login')
def sub_quantity(request, product_id):
    item, created = CartItem.objects.get_or_create(id=product_id)
    item.quantity -= 1
    item.product.num_of_buy += 1
    item.product.save()
    item.save()
    if item.quantity < 1:
        item.delete()
    return redirect('profile')


def category_filtered_page(request, category):
    if Category.objects.filter(name=category).exists():
        products = Product.objects.filter(category__name=category)
        return render(request, 'category_filtered.html', {'products': products})
    return render(request, 'category_filtered.html', {'products': None})


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        all_products = set(Product.objects.filter(category_id=product.category.id))
        n = 5 if len(all_products) >=5 else len(all_products)
        related = random.sample(sorted(all_products, key=lambda i: i.title), k=n)
    except:
        product = None
        related = None
    return render(request, 'product-details.html', {'product': product, 'related': related})


@login_required(login_url='login')
def agree_vote(request, vote):
    vote = Vote.objects.filter(id=vote, is_active=True)
    if vote.exists():
        vote = vote.first()
        if SingleVote.objects.filter(user=request.user, vote=vote).exists():
            return redirect('store')
        SingleVote.objects.create(user=request.user, vote=vote, is_agree=True)
        return redirect('store')
    return HttpResponse('error')


@login_required(login_url='login')
def disagree_vote(request, vote):
    vote = Vote.objects.filter(id=vote, is_active=True)
    if vote.exists():
        vote = vote.first()
        if SingleVote.objects.filter(user=request.user, vote=vote).exists():
            return redirect('store')
        SingleVote.objects.create(user=request.user, vote=vote, is_agree=False)
        return redirect('store')
    return HttpResponse('error')


# ---------------------payment section----------------------

@login_required(login_url='login')
def check_out(request, cart_id):
    if request.method == 'GET':
        cart = get_object_or_404(Cart, id=cart_id)
        items = CartItem.objects.filter(cart=cart)
        items.delete()
        messages.success(request, 'پرداخت کامل شد')
        return redirect('profile')

