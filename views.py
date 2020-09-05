# Import necessary classes
from time import ctime
from django.http import HttpResponse, HttpResponseRedirect, response
from django.shortcuts import redirect
from django.urls import reverse
from .forms import OrderForm, InterestForm, RegisterForm
from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request,'myapp/index.html',{'top_list':top_list})
def about(request):
    if request.COOKIES.get('about_visits', False):
        visit = int(request.COOKIES.get('about_visits')) + 1
        # dt = datetime.now() + timedelta(minutes=5)
        resp=HttpResponse(response)
        resp.set_cookie('about_visits', value=visit, max_age=300)
    else:
        visit = int(1)
        # dt = datetime.now() + timedelta(minutes=5)
        resp = HttpResponse(response)
        #resp.set_cookie('about_visits', value=visit, max_age=300)
    return render(request, 'myapp/about.html',{'noofvisit':visit})
def detail(request,top_no):
    #get_object_or_404(Topic,id=top_no)
    top=Topic.objects.get(id=top_no)
    courname = Course.objects.all().filter(topic__exact=top)
    return render(request,'myapp/detail.html',{'cour':courname})
def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request,'myapp/courses.html',{'co_list':courlist})
def order_response(request):
    return render(request, 'myapp/order_response.html')
def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                order.save()
                msg = 'Your course has been ordered successfully.'
                if order.course.price > 150:
                    c=Course()
                    order.discountedprice=c.discount()
            else:
                    msg = 'You exceeded the number of levels for this course.'
            return redirect('/myapp/order_response/')
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form':form, 'msg':msg,
'courlist':courlist})
def coursedetail(request, cour_id):
    cour = Course.objects.get(id=cour_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid and cour.interested == 1:
            cour.interested = cour.interested+1
            cour.save()
            return redirect('/index/')
    else:
        form = InterestForm()
    return render(request,'myapp/coursedetail.html',{'form':form,'co_req':cour})
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            raw_password = form.cleaned_data.get('password1')
            user.set_password(user.password)
            user.is_staff=True
            user.save()
            #user = authenticate(username=user.username, password=user.password)
            #request.session['username'] = user.username
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('myapp:myaccount'))
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})
def user_login(request):
    request.session['last_login'] = ctime()
    request.session.set_expiry(0)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
                request.session['username'] = username
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:myaccount'))
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))
def myaccount(request):
    if request.user.is_authenticated:
        if Student.objects.filter(username__iexact=request.user.username):
            id=Student.objects.filter(username__iexact=request.user.username)
            Firstname= request.user.first_name
            Lastname= request.user.last_name
            # Orders
            orders = Order.objects.filter(student__username__iexact=request.user.username)
            interest_list=Student.objects.get(first_name__iexact=request.user.username).interested_in.all()
            context= {'First_name': Firstname,'Last_name':Lastname,'interested_list':interest_list, 'orders': orders}

            return render(request, 'myapp/myaccount.html',  context)
        else:
             msg='You are not a registered student!'
             return render(request, 'myapp/myaccount.html', {'msg':msg})
    else:
        return redirect('/myapp/login/')

