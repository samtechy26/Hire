import json
from distutils.log import error
from turtle import title
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from job.models import Job, Bid
from job.forms import BidForm
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import stripe
from itertools import chain
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Review

from .tokens import account_activation_token




def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('job-home')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            Firstname = form.cleaned_data.get('firstname')
            messages.success(request, f'Account created for {Firstname}!')
            return redirect('login')
    form = UserRegistrationForm
    return render(request, 'user/register.html', {'form': form})

def dashboard(request):
    return render(request, 'user/dashboardprofile.html')



def reviews(request):
    #job_lists = Job.objects.all()
    review_lists = Review.objects.filter(active=True)
    job_lists = Job.objects.exclude(reviews__in =review_lists)
    lists = list(chain(review_lists, job_lists))
    paginator = Paginator(lists, per_page=2)
    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    
    return render(request, 'user/reviews.html',{
        'jobs':jobs
    })

def dashboard_task(request):
    user = request.user
    jobs = Job.objects.filter(author=user)
    jobs_count = jobs.count()
    bids = Bid.objects.filter(job__in=jobs)
    bid_count = bids.count
    
    context={
        "tasks":jobs,
        'bids':bids,
        'bid_count':bid_count,
        'jobs_count':jobs_count
    }
    return render(request, 'user/task_list.html', context)


@login_required
def profile(request, id):
    users = User.objects.get(id=id)
    jobs = Job.objects.filter(author=users)
    reviews_list = Review.objects.filter(freelancer=id, active=True)
    paginator = Paginator(reviews_list, per_page=1)
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        current_user = request.user
        data = request.POST
        action = data.get('bookmark')
        if action == 'bookmark':
            current_user.profile.favourite.add(users)
        elif action == 'bookmarked':
            current_user.profile.favourite.remove(users)
        current_user.save()
        return redirect('profile', id)
    context={
        'users':users,
        'reviews':reviews,
        'jobs':jobs
    }
    return render(request, 'user/profile.html', context)


@login_required
def profileUpdate(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'user/profile_update.html', context)
@login_required
def dashboard_bidders(request, id):
    
    jobs = Job.objects.filter(id=id)
    job = Job.objects.get(id=id)
    bids = Bid.objects.filter(job__in=jobs)
    bid_count = bids.count()
    
    context = {
        'job':job,
        'bids':bids,
        'bid_count':bid_count
    }
    return render(request, 'user/manage_bidders.html', context)

@login_required
def dashboard_mybids(request):
    current_user = request.user
    bids = Bid.objects.filter(user=current_user)
    
    form = BidForm()
    
    
    context = {
        'bids':bids,
        'form':form
    }
    return render(request, 'user/my_bids.html', context)

@login_required
def bid_update(request, id):
    current_user = request.user
    bid = Bid.objects.get(id=id)
    
    form = BidForm(instance=bid)
    
    if request.method == 'POST':
        form = BidForm(request.POST, instance=bid)
        if form.is_valid():
            form.save()
            return redirect('my_bids')
    context = {
        'bid':bid,
        'form':form
    }
    return render(request, 'user/bid_update.html', context)


@login_required
def manage_offer(request, id):
    bid = Bid.objects.get(id=id)
    
    context = {
        'bid':bid,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'user/manage_offer.html', context)

@login_required
def add_review(request):

    
    if request.method == 'POST':
        data = json.loads(request.body)
        comment = data.get('comment','')
        rating = data.get('rating','1')
        timely = False
        on_budget = False


        if data.get('timely') == "1":
            timely = True
        #project_id = data.get('project_id')
        if data.get('on_budget') == "1":
            on_budget = True
        
        freelancer = get_object_or_404(User, username = data.get('freelancer'))
        client = get_object_or_404(User, username = data.get('employer'))
        project = get_object_or_404(Job, id = int(data.get('project')))
        
        #project = get_object_or_404(Job, id = project_id)
        new_review = Review.objects.update_or_create(employer =client, freelancer = freelancer,project=project,\
             comment=comment, rating=rating, on_budget=on_budget, timely=timely)
        #ew_review.save()

        return JsonResponse({
                "message":"Your review has been sucessfully added! "
            },status=200)
       
            
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        comment = data.get('comment','')
        rating = data.get('rating','1')
        review_id = data.get('reveiw_id','')
        timely = False
        on_budget = False


        if data.get('timely') == "1":
            timely = True
        #project_id = data.get('project_id')
        if data.get('on_budget') == "1":
            on_budget = True
        
        try:
            review = Review.objects.get(id= int(review_id))
            review.comment = comment
            review.timely = timely
            review.on_budget = on_budget
            review.rating = rating
            review.save()
            return JsonResponse({
                "message":"Your review has been updated successfully!"
            }, status=200)
        except Review.DoesNotExist:
            return JsonResponse({
                "message":"No such review existed"
            }, status=400)


    elif request.method == 'DELETE':
        data = json.loads(request.body)
        review_id = data.get('review_id')
        try:
            review = Review.objects.get(id=review_id)
            review.active = False
            review.save()
            return JsonResponse({
                "message":"Your review has been sucessfully deleted!"
            }, status = 201)

        except Review.DoesNotExist:
            return JsonResponse({
                "message":"There is no such review"
            }, status=400 )

