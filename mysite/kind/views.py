from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView,LogoutView, PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView
from django.views.generic.dates import DateMixin
from django.views.generic.base import TemplateView
from django.core.signing import Signer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page


from .cart import Cart
from .models import AbvUser, Category, Product, Types, UserData,BuyData,About
from .forms import LoginForm, RegisterUserForm,ConfirmFormPassword, CartAddProductForm, UserDetailForm
from django.core.mail import send_mail






def index(request):
    product = Product.objects.order_by('-create_at').values('slug','name','image','price')[:6]
    context = {'product':product}
    return render(request, 'main/index.html',context)


class MyLoginView(DateMixin,LoginView):
    form_class = LoginForm
    template_name = 'main/users/login.html'
    def get_success_url(self):
        return reverse_lazy('kind:index')

class RegiserUserView(CreateView):
    model = AbvUser
    template_name = 'main/users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('kind:login')

    
def user_is_activate(request, sign):
    signer = Signer()
    try:
        username = signer.unsign(sign)
    except:
        return render(request,'main/users/register.html')
    user=get_object_or_404(AbvUser, username=username)
    user.is_activated=True
    user.is_active=True
    
    user.save()
    xxx=UserData( postcode='', address='',name='', phoneNumber='',country='',userr_id=user.id)
    xxx.save()
    return redirect('kind:login')

class LogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('kind:index')

class PasswordResetViewUser(PasswordResetView):
    success_url = reverse_lazy('kind:password_reset_done')
    template_name = 'main/users/password_reset.html'
    subject_template_name = 'email/reset_subject.txt'
    email_template_name = 'email/reset_email.txt'

class PasswordRe(PasswordResetDoneView):
    template_name = 'main/users/password_reset_send.html'

class PasswordResetConfirmViews(PasswordResetConfirmView):
    template_name = 'main/users/password_confirm.html'
    form_class = ConfirmFormPassword
    success_url = reverse_lazy('kind:login')

@cache_page(60*10)
def shop_view(request):

    category = Category.objects.filter(is_active=True).values('name','pk')

    product = Product.objects.filter(is_active=True).select_related('category').values('slug','name','image','price')
    

    
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        q = Q(name__icontains=keyword)
        product = product.filter(q)
    else:
        keyword = ''

    paginator = Paginator(product, 8)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'product': page.object_list, 'page':page,'category':category,}
    return render(request, 'main/product/product_list.html', context)

def shop_cat(request,pk):
    category = Category.objects.filter(is_active=True).values('name','pk')
    product = Product.objects.filter(is_active=True, category=pk ).values('slug','name','image','price')
    x = pk

    types = Types.objects.all()
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        q = Q(name__icontains=keyword)
        product = product.filter(q)
    else:
        keyword = ''

    paginator = Paginator(product, 8)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'product': page.object_list, 'page':page,'category':category,'types':types, 'x':x}
    return render(request, 'main/product/category.html', context)

def shop_type(request,pk,id):
    category = Category.objects.filter(is_active=True).values('name','pk')
    product = Product.objects.filter(is_active=True, category=pk,types=id ).values('slug','name','image','price')
    x,y= pk,id
    
    types = Types.objects.filter(is_active=True).values('name','id')
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        q = Q(name__icontains=keyword)
        product = product.filter(q)
    else:
        keyword = ''

    paginator = Paginator(product, 8)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'product': page.object_list, 'page':page,'category':category,'types':types, 'x':x,'y':y}
    return render(request, 'main/product/category.html', context)

@cache_page(30)
def shop_detail(request,slug):
    if request.user.is_authenticated:
        form = CartAddProductForm()
            
        product = get_object_or_404(Product,  slug=slug, is_active=True)
        ais = product.additionalimage_set.all()
        context = {'product':product, 'ais':ais,'form':form}
        return render(request,'main/product/single-product.html',context)
    else:
        return redirect('kind:login')
    


@login_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                update_quantity=cd['update'])
    x =request.META.get('HTTP_REFERER')
    return redirect(x)

@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    x =request.META.get('HTTP_REFERER')
    return redirect(x)

@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    x =request.META.get('HTTP_REFERER')
    return redirect(x)

@cache_page(60)
@login_required
def cart_detail(request):
    cart = Cart(request)
    user_data = UserData.objects.get(userr_id=request.user.id)
    
    if request.method == 'POST':
        form = UserDetailForm(request.POST,instance=user_data)
        if form.is_valid():
            
            form.save()
            
    form = UserDetailForm(instance=user_data)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'update': True})

    context = {'cart': cart,'user_data':user_data ,'form':form}
    return render(request, 'main/cart.html', context)

def buy_redirect(request):
    link_buy = BuyData.objects.get(is_active=True)
    xs = link_buy.link
    user = UserData.objects.get(userr_id=request.user.id)
    cart = Cart(request)
    total = cart.get_total_price()
    price = cart.product_info()

    context = {'user':user, 'cart' : cart,'total':total,'price':price}
    subject = render_to_string('email/buy.txt')
    body_text = render_to_string('email/buy_body.txt', context)
    send_mail(subject,body_text,'from@example.com',['from@example.com'],fail_silently=False)
    cart.clear()
    return redirect(xs)

class AboutView(TemplateView):
    template_name = 'main/about.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = About.objects.filter(is_active=True).values('text','link')[:1]
        return context