from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
# ----
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Product, Category, User, Order, Cart
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    UserSerializer,
    OrderSerializer,
    CartSerializer
)


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def logout_view(request):
    logout(request)
    return redirect('home')


# -----------------
# def profile(request):
#     user = request.user
#     return render(request, 'profile.html', {'user': user})
#
#
# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'register.html', {'form': form})
#
#
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('profile')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})
#
#
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             count = int(request.POST['count'])
#             # Calculate the total amount
#             total_amount = count * float(product.price)
#             return render(request, 'order.html', {'product': product, 'count': count, 'total_amount': total_amount})
#         else:
#             return redirect('register')
#
#     return render(request, 'product_detail.html', {'product': product})
#
#
# def category_detail(request, pk):
#     category = Category.objects.get(pk=pk)
#     products = Product.objects.filter(category=category)
#     return render(request, 'category_detail.html', {'category': category, 'products': products})
#
#
# @login_required(login_url='login_view')
# def add_to_cart(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart.products.add(product)
#     return redirect('cart')
#
#
# @login_required(login_url='login_view')
# def remove_from_cart(request, pk):
#     product = Product.objects.get(pk=pk)
#     cart = Cart.objects.get(user=request.user)
#     cart.products.remove(product)
#     return redirect('cart')
#
#
# @login_required(login_url='login_view')
# def cart(request):
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     products = cart.products.all()
#     total_price = sum(product.price for product in products)
#     product_quantities = cart.products.through.objects.filter(cart=cart).values('product').annotate(
#         quantity=Count('product')).values('product', 'quantity')
#
#     product_quantity_map = {item['product']: item['quantity'] for item in product_quantities}
#
#     return render(request, 'cart.html', {'products': products, 'total_price': total_price, 'cart': cart,
#                                          'product_quantity_map': product_quantity_map})
#
#
# @login_required(login_url='login_view')
# def place_order(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         count = int(request.POST['count'])
#         total_amount = count * float(product.price)
#
#         # Create the order here
#         order = Order.objects.create(
#             product=product,
#             user=request.user,
#             count=count,
#             total_amount=total_amount
#         )
#
#         return render(request, 'order_placed.html', {'product': product, 'count': count, 'total_amount': total_amount})
#
#     return render(request, 'order_placed.html', {'product': product})

# API

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PlaceOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        count = int(request.data.get('count', 0))
        total_amount = count * float(product.price)

        order = Order(
            product=product,
            user=request.user,
            count=count,
            total_amount=total_amount
        )
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart


class AddToCartView(generics.GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class RemoveFromCartView(generics.GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        cart = Cart.objects.get(user=request.user)
        cart.products.remove(product)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)
