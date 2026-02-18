from django.shortcuts import render,redirect,get_object_or_404
from .models import Tbl_user,Tbl_insurance_plan,Tbl_cart,Tbl_Family_member,Tbl_Transaction
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.core.mail import send_mail
from django.contrib import messages
import paypalrestsdk
from django.conf import settings
from decimal import Decimal
from django.utils.timezone import now
from datetime import date,timedelta
from django.utils import timezone
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Q



# Create your views here.
def homepage(request):
    user=Tbl_insurance_plan.objects.all()
    return render(request, 'users/homepage.html',{'user':user})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            # print(f"Authenticated user: {user}")
            if user.groups.filter(name='admin_user').exists():         
                return redirect('admindash')
            else:
                # return HttpResponse("not an admin user")
                return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'users/login.html')

@login_required
def admindash(request):
    # user=Tbl_user.objects.all()
    # user2=Tbl_insurance_plan.objects.all()

    today = timezone.now().date()
    current_month = today.month
    current_year = today.year

    #  daily revenue
    daily_revenue = Tbl_Transaction.objects.filter(Fld_Created_at__date=today).aggregate(total_revenue=Sum('Fld_Total_amount'))
    total_daily_revenue = daily_revenue['total_revenue'] or 0
    formatted_daily_revenue = f"{total_daily_revenue:.2f}"

    #  monthly revenue
    monthly_revenue = Tbl_Transaction.objects.filter(Fld_Created_at__month=current_month, Fld_Created_at__year=current_year).aggregate(total_revenue=Sum('Fld_Total_amount'))
    total_monthly_revenue = monthly_revenue['total_revenue'] or 0
    formatted_monthly_revenue = f"{total_monthly_revenue:.2f}"

    #  yearly revenue
    yearly_revenue = Tbl_Transaction.objects.filter(Fld_Created_at__year=current_year).aggregate(total_revenue=Sum('Fld_Total_amount'))
    total_yearly_revenue = yearly_revenue['total_revenue'] or 0
    formatted_yearly_revenue = f"{total_yearly_revenue:.2f}"

    active_policies_count = Tbl_insurance_plan.objects.filter(Fld_Status='active').count()

    #daily, monthly, and yearly growth

    today = date.today()
    start_of_day = today
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    daily_growth = Tbl_Transaction.objects.filter(Fld_Date__date=start_of_day).count()
    monthly_growth = Tbl_Transaction.objects.filter(Fld_Date__date__gte=start_of_month).count()
    yearly_growth = Tbl_Transaction.objects.filter(Fld_Date__date__gte=start_of_year).count()

    return render(request, "users/admindash.html",{'total_daily_revenue': formatted_daily_revenue,'total_monthly_revenue': formatted_monthly_revenue,'total_yearly_revenue': formatted_yearly_revenue,'active_policies_count':active_policies_count,'daily_growth': daily_growth,'monthly_growth': monthly_growth,'yearly_growth': yearly_growth,})

@login_required
def dashboard(request):
    user_plans = Tbl_cart.objects.filter(user=request.user)
    family_members= Tbl_Family_member.objects.filter(user=request.user)
    user2=Tbl_insurance_plan.objects.all()
    plans = Tbl_insurance_plan.objects.all()

    category = request.GET.get('Fld_Category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    coverage_min = request.GET.get('coverage_min')
    coverage_max = request.GET.get('coverage_max')
    period = request.GET.get('Fld_Period')

    if category or price_min or price_max or coverage_min or coverage_max or period:
        if category:
            plans = plans.filter(Fld_Category=category)
        if price_min:
            plans = plans.filter(Fld_Premium__gte=price_min)
        if price_max:
            plans = plans.filter(Fld_Premium__lte=price_max)
        if coverage_min:
            plans = plans.filter(Fld_Coverage_amount__gte=coverage_min)
        if coverage_max:
            plans = plans.filter(Fld_Coverage_amount__lte=coverage_max)
        if period:
            plans = plans.filter(Fld_Period=period)
        search_used = True
    else:
        search_used = False

    return render(request,"users/dashboard.html",{"user_plans":user_plans,"user2":user2,"family_members":family_members,'plans':plans,'search_used':search_used})
    
@login_required
def add_plan(request):
    user=Tbl_insurance_plan.objects.filter(user=request.user)
    if request.method=="POST":
        Fld_Plan_name=request.POST['Fld_Plan_name']
        Fld_Description=request.POST['Fld_Description']
        Fld_Coverage_amount=request.POST['Fld_Coverage_amount']
        Fld_Premium=request.POST['Fld_Premium']
        Fld_Period=request.POST['Fld_Period']
        Fld_Coverage_details=request.POST['Fld_Coverage_details']
        Fld_Insurance_pic = request.FILES.get('Fld_Insurance_pic', None)
        Fld_Category=request.POST['Fld_Category']
        Fld_Validity=request.POST['Fld_Validity']
        Fld_Status=request.POST['Fld_Status']

        Tbl_insurance_plan.objects.create(Fld_Plan_name=Fld_Plan_name,Fld_Description=Fld_Description,Fld_Coverage_amount=Fld_Coverage_amount,Fld_Premium=Fld_Premium,Fld_Period=Fld_Period,Fld_Coverage_details=Fld_Coverage_details,Fld_Insurance_pic=Fld_Insurance_pic,Fld_Category=Fld_Category,user=request.user,Fld_Validity=Fld_Validity,Fld_Status=Fld_Status)

        messages.success(request,'A new insurance has been added successfully!')

        return redirect('admindash')
    return render(request,'users/addplan.html',{'user':user})

@login_required
def update_plan(request,userid):
    data=get_object_or_404(Tbl_insurance_plan,id=userid)
    if request.method=="POST":
        data.Fld_Plan_name=request.POST['Fld_Plan_name']
        data.Fld_Description=request.POST['Fld_Description']
        data.Fld_Coverage_amount=request.POST['Fld_Coverage_amount']
        data.Fld_Premium=request.POST['Fld_Premium']
        data.Fld_Period=request.POST['Fld_Period']
        data.Fld_Coverage_details=request.POST['Fld_Coverage_details']

        if 'Fld_Insurance_pic' in request.FILES:
            data.Fld_Insurance_pic = request.FILES['Fld_Insurance_pic']
        data.Fld_Category=request.POST['Fld_Category']
        data.Fld_Validity=request.POST['Fld_Validity']
        data.Fld_Status=request.POST['Fld_Status']

        data.save()

        messages.success(request,'Insurance plan is updated successfully!')

        return redirect('admindash')
    return render(request,'users/addplan.html',{'data':data})

@login_required
def delete_plan(request,userid):
    data = get_object_or_404(Tbl_insurance_plan, id=userid)
    if request.method == 'POST':
        data.delete()
        return redirect('admindash')  
    return render(request, 'users/confirmdelete.html', {'data': data})

def register(request):
    is_admin = False
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin_user').exists()
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        profile_pic = request.FILES.get('Fld_Profile_pic', None)

        if Tbl_user.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {'error': 'Email already exists'})

        user = Tbl_user(first_name=first_name, last_name=last_name, email=email, username=email)

        if profile_pic:
            user.Fld_Profile_pic = profile_pic 
            
        user.set_password(password)  
        user.save()

        # customer_group = Group.objects.get(name='customer_user')
        # user.groups.add(customer_group)

        try:
            login(request, user)
            send_mail(
                'Welcome to Our Platform',
                f'Hello {first_name},\n\nThank you for registering on our platform.',
                'isayn635@gmail.com',
                [email],
                fail_silently=False,
            )
            if is_admin:  
                return redirect('admindash')
            else:
                return redirect('dashboard')  
        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred during registration. Please try again.')

    return render(request, 'users/register.html',{'is_admin': is_admin})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login') 

@login_required
def change_profile(request):
    user_profile = Tbl_user.objects.get(username=request.user.username)
    if request.method == 'POST':

        if request.FILES.get('Fld_Profile_pic'):
            profile_pic = request.FILES['Fld_Profile_pic']
            user_profile.Fld_Profile_pic = profile_pic
            user_profile.save()
            messages.success(request, 'Your profile photo was successfully updated!')
        
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if old_password and new_password1 and new_password2:
            if not request.user.check_password(old_password):
                messages.error(request, 'Old password is incorrect.')
            elif new_password1 != new_password2:
                messages.error(request, 'New passwords do not match.')
            else:
                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Keeps the user logged in
                messages.success(request, 'Your password was successfully updated!')
        
        if request.user.is_superuser:
            return redirect('admindash')
        else:
            return redirect('dashboard')

    return render(request, 'users/changeprofile.html', {'user_profile': user_profile, 'is_admin': request.user.is_superuser})

@login_required
def cart(request):
    family_cart = Tbl_Family_member.objects.filter(user=request.user, is_hidden=False)
    user_cart = Tbl_cart.objects.filter(user=request.user, is_hidden=False)

    total_cost = sum(item.plan.Fld_Premium * item.Fld_Quantity for item in user_cart)
    for member in family_cart:
        if member.plan:
            total_cost += member.plan.Fld_Premium * member.Fld_Member_count

    gst = total_cost * Decimal(0.18)
    gst_str=format(gst,'.2f')
    total_cost_with_gst = total_cost + gst
    total_cost_with_gst_str=format(total_cost_with_gst,'.2f')

    return render(request, 'users/cart.html', {'user_cart':user_cart,'family_cart':family_cart, 'total_cost_with_gst': total_cost_with_gst_str, 'gst': gst_str ,'total_cost':total_cost})

@login_required
def add_to_cart(request, plan_id):
    plan = get_object_or_404(Tbl_insurance_plan, id=plan_id)
    cart_item, created = Tbl_cart.objects.get_or_create(user=request.user, plan=plan, is_hidden=False )
    if not created:
        cart_item.Fld_Quantity += 1
        cart_item.save()
    messages.success(request, 'Plan added to cart successfully!')
    return redirect('dashboard')

@login_required
def remove_from_cart(request, plan_id):
    cart_item = get_object_or_404(Tbl_cart, user=request.user, id=plan_id)
    cart_item.delete()
    messages.success(request, 'Plan removed from cart successfully!')
    return redirect('cart')

@login_required
def add_family_member(request):
    if request.method == 'POST':
        Fld_Name = request.POST['Fld_Name']
        plan_id = request.POST.get('plan_id')
        plan = Tbl_insurance_plan.objects.get(id=plan_id) if plan_id else None
        Fld_Plan_type = request.POST.get('Fld_Plan_type', 'individual')
        Fld_Member_count = request.POST.get('Fld_Member_count', 1)

        Tbl_Family_member.objects.create(user=request.user, Fld_Name=Fld_Name, plan=plan, Fld_Plan_type=Fld_Plan_type, Fld_Member_count=Fld_Member_count, is_hidden=False  )
        messages.success(request, 'Family member added successfully!')
        return redirect('dashboard')
    plans = Tbl_insurance_plan.objects.all()
    return render(request, 'users/addfamily.html', {'plans': plans})

@login_required
def remove_family_member(request, member_id):
    family_member = get_object_or_404(Tbl_Family_member, id=member_id, user=request.user)
    family_member.delete()
    messages.success(request, 'Family member removed successfully!')
    return redirect('cart')

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

@login_required
def create_payment(request):
    cart_items = Tbl_cart.objects.filter(user=request.user, is_hidden=False )
    family_members = Tbl_Family_member.objects.filter(user=request.user, is_hidden=False)

    total_cost = Decimal(0)
    for item in cart_items:
        total_cost += item.plan.Fld_Premium * item.Fld_Quantity

    for member in family_members:
        if member.plan:
            total_cost += member.plan.Fld_Premium * Decimal(member.Fld_Member_count)

    gst = total_cost * Decimal(0.18)
    gst_str=format(gst,'.2f')
    total_cost_with_gst = total_cost + gst
    total_cost_with_gst_str = format(total_cost_with_gst, '.2f')

    if request.method == 'POST':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/user/paymentexecute/'),
                "cancel_url": request.build_absolute_uri('/user/paymentcancel/')
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Insurance Plan",
                        "sku": "001",
                        "price": str(total_cost_with_gst_str),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(total_cost_with_gst_str),
                    "currency": "USD"
                },
                "description": "Purchase of insurance plan."
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        else:
            messages.error(request, "Payment creation failed. Please try again.")
            return redirect('cart')

    return render(request, 'users/payment.html', {
        'total_cost': total_cost,
        'gst': gst_str,
        'total_cost_with_gst': total_cost_with_gst_str
    })

@login_required
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if not payment_id or not payer_id:
        messages.error(request, 'Payment execution failed. Missing paymentId or PayerID.')
        return redirect('cart')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        transaction = Tbl_Transaction.objects.create(
            user=request.user,
            Fld_Amount=Decimal(payment.transactions[0].amount.total) / Decimal(1.18),
            Fld_gst=Decimal(payment.transactions[0].amount.total) * Decimal(0.18),
            Fld_Total_amount=Decimal(payment.transactions[0].amount.total),
            Fld_Paypal_transaction_id=payment_id  # Store the PayPal transaction ID
        )

        cart_items = Tbl_cart.objects.filter(user=request.user)
        family_members = Tbl_Family_member.objects.filter(user=request.user)

        for item in cart_items:
            transaction.plan = item.plan
            transaction.save()
            item.is_hidden = True  # Mark the cart item as hidden
            item.save()

        for member in family_members:
            transaction.family_members.add(member)
            transaction.save()
            member.is_hidden = True  # Mark the cart item as hidden
            member.save()

        # cart_items.delete()  # Clear the cart after successful payment
        # family_members.delete()

        # Send confirmation email to customer
        subject = 'Payment Confirmation and Receipt'
        message = (
            f"Dear {transaction.user.first_name},\n\n"
            f"Thank you for your purchase. Here are the details of your transaction:\n\n"
            # f"Transaction ID: {transaction.id}\n"
            f"PayPal Transaction ID: {transaction.Fld_Paypal_transaction_id}\n"  # Include PayPal transaction ID
            f"Plan: {transaction.plan.Fld_Plan_name}\n"
            f"Amount: ₹{transaction.Fld_Amount}\n"
            f"GST (18%): ₹{transaction.Fld_gst}\n"
            f"Total Amount: ₹{transaction.Fld_Total_amount}\n\n"
            f"Family Members:\n"
        )
        for member in transaction.family_members.all():
            message += f" - {member.Fld_Name} - {member.plan.Fld_Plan_name} ({member.Fld_Plan_type} plan for {member.Fld_Member_count} members)\n"
        message += "\nBest Regards,\nYour System"
        send_mail(subject, message, 'isayan635@gmail.com', [request.user.email])

        # Notify admin about the new purchase
        admin_subject = 'New Purchase Notification'
        admin_message = (
            f"Dear Admin,\n\n"
            f"A new purchase has been made. Here are the details of the transaction:\n\n"
            # f"Transaction ID: {transaction.id}\n"
            f"PayPal Transaction ID: {transaction.Fld_Paypal_transaction_id}\n"  # Include PayPal transaction ID
            f"User: {transaction.user.username}\n"
            f"Plan: {transaction.plan.Fld_Plan_name}\n"
            f"Amount: ₹{transaction.Fld_Amount}\n"
            f"GST (18%): ₹{transaction.Fld_gst}\n"
            f"Total Amount: ₹{transaction.Fld_Total_amount}\n\n"
            f"Family Members:\n"
        )
        for member in transaction.family_members.all():
            admin_message += f" - {member.Fld_Name} - {member.plan.Fld_Plan_name} ({member.Fld_Plan_type} plan for {member.Fld_Member_count} members)\n"
        admin_message += "\nBest Regards,\nYour System"
        send_mail(admin_subject, admin_message, 'isayan635@gmail.com', ['isayan635@gmail.com'])

        messages.success(request, 'Payment successful! An invoice has been generated and sent to your email.')
        return redirect('invoice', transaction_id=transaction.id)
    else:
        messages.error(request, 'Payment execution failed. Please try again.')
        return redirect('cart')

@login_required
def cancel_payment(request):
    messages.error(request, 'Payment canceled.')
    return redirect('cart')

@login_required
def invoice(request, transaction_id):
    transaction = get_object_or_404(Tbl_Transaction, id=transaction_id)
    return render(request, 'users/invoice.html', {'transaction': transaction})

@login_required
def transaction_history(request):
    transactions = Tbl_Transaction.objects.filter(user=request.user).order_by('-Fld_Date')
    return render(request, 'users/transaction.html', {'transactions': transactions})

@login_required
def admin_tran(request):
    tran=Tbl_Transaction.objects.all()
    return render(request,'users/admintran.html',{'tran':tran})

@login_required
def expired_policy(request):
    today = timezone.now().date()
    expired_transactions = Tbl_Transaction.objects.filter(Fld_Expiration_date__lte=today, plan__Fld_Status='active')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        transaction = Tbl_Transaction.objects.get(id=user_id)
        
        subject = 'Your Insurance Plan has Expired'
        message = f'Dear {transaction.user.first_name}, your insurance plan "{transaction.plan.Fld_Plan_name}" has expired. Please renew your plan at the earliest convenience.'
        recipient = transaction.user.email
        
        send_mail(subject, message, 'isayan635@gmail.com', [recipient])
        messages.success(request, f'Email sent to {transaction.user.username}')
        
        transaction.plan.Fld_Status = 'expired'
        transaction.plan.save()
        return redirect('expiredplans')

    return render(request, 'users/expiredpolicy.html', {'expired_transactions': expired_transactions})

def about_us(request):
    return render(request,'users/aboutus.html')

@login_required
def manage_customers(request):
    # user=Tbl_user.objects.all()
    # user2=Tbl_insurance_plan.objects.all()

    #search

    query = request.GET.get('q', '')
    if query:
        user_list = Tbl_user.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(username__icontains=query)
        )
    else:
        user_list = Tbl_user.objects.all()

    paginator = Paginator(user_list, 5)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/managecus.html',{'page_obj':page_obj,'query': query})

@login_required
def manage_insurance(request):
    # user=Tbl_user.objects.all()
    # user2=Tbl_insurance_plan.objects.all()

    #search
    query = request.GET.get('q', '')
    if query:
        user_list = Tbl_insurance_plan.objects.filter(
            Q(Fld_Plan_name__icontains=query) |
            Q(Fld_Description__icontains=query) |
            Q(Fld_Coverage_amount__icontains=query) |
            Q(Fld_Premium__icontains=query) |
            Q(Fld_Period__icontains=query) |
            Q(Fld_Coverage_details__icontains=query)

        )
    else:
        user_list = Tbl_insurance_plan.objects.all()

    paginator = Paginator(user_list, 5)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/manageins.html',{'page_obj':page_obj,'query': query})

@login_required
def expired_plans(request):

    months = request.GET.get('months')
    expired_plans = []

    if months:
        expiration_date = now() - timedelta(days=30 * int(months))
        expired_plans = Tbl_insurance_plan.objects.filter(Fld_Validity__lt=expiration_date)
    return render(request,'users/expiredplans.html',{'expired_plans':expired_plans,'selected_months': months})

@login_required
def deactivate_user(request, user_id):
    user = get_object_or_404(Tbl_user, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request,f'The customer {user.username} account is deactivated')
    return redirect('admindash')


