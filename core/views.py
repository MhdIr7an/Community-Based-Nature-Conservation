from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
import os
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta


from .models import Base_User, Base_Events, Base_Volunteer, Base_Issue, Base_Donations, Base_Items, Base_Order, Base_Resources, Base_Discussions


import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def user_verified(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.user_type <2:
            return view_func(request, *args, **kwargs)
        if request.user.verified == True:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('not_verified') 
    return wrapped_view

def admin_only(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 0:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('not_authorized') 
    return wrapped_view



def sent_mail(mail):
    # Email configuration
    sender_email = settings.SMTP_USERNAME
    receiver_email = mail
    subject = 'User Verified'
    body = 'Your account has been verified.'

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the email body
    message.attach(MIMEText(body, 'plain'))

    # Attach a file (optional)
    # file_path = 'attachment.txt'
    # with open(file_path, 'rb') as attachment:
    #     part = MIMEApplication(attachment.read())
    #     part.add_header('Content-Disposition', f'attachment; filename={file_path}')
    #     message.attach(part)

    # SMTP server configuration
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_username = settings.SMTP_USERNAME
    smtp_password = settings.SMTP_PASSWORD

    # Create an SMTP session
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        
        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        # print('Email sent successfully!')
        
    except Exception as e:
        pass
        # print('Email could not be sent. Error:', str(e))

    finally:
        server.quit()







@login_required(login_url='/login')
def index(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        if user_type == 0:
            return redirect('organiser_requests')
        elif user_type == 1:
            return redirect('volunteer')
        elif user_type == 2:
            return redirect('organise_event')
        elif user_type == 3:
            return redirect('orders')
        elif user_type == 4:
            return redirect('publish_paper')
    return redirect('login')

@login_required(login_url='/login')
def organiser_requests(request):
    organisers = Base_User.objects.filter(user_type=2, verified=False)
    return render(request, 'main/organiser_requests.html',{'organisers': organisers})

def organiser_request_approve(request, organiser_id):
    organiser = Base_User.objects.get(user_id=organiser_id)
    organiser.verified = True
    organiser.save()
    sent_mail(organiser)
    return redirect('organiser_requests')
    

def organiser_request_reject(request, organiser_id):
    organiser = Base_User.objects.get(user_id=organiser_id)
    organiser.delete()
    return redirect('organiser_requests')

@login_required(login_url='/login')
def supplier_requests(request):
    suppliers = Base_User.objects.filter(user_type=3, verified=False)
    context = { 'suppliers': suppliers }
    return render(request, 'main/supplier_requests.html', context)

def supplier_request_approve(request, supplier_id):
    supplier = Base_User.objects.get(user_id=supplier_id)
    supplier.verified = True
    supplier.save()
    sent_mail(supplier)
    return redirect('supplier_requests')

def supplier_request_reject(request, supplier_id):
    supplier = Base_User.objects.get(user_id=supplier_id)
    supplier.delete()
    return redirect('supplier_requests')

@login_required(login_url='/login')
def researcher_requests(request):
    researchers = Base_User.objects.filter(user_type=4, verified=False)
    return render(request, 'main/researcher_requests.html',{'researchers':researchers})

def researcher_request_approve(request, researcher_id):
    researcher = Base_User.objects.get(user_id=researcher_id)
    researcher.verified = True
    researcher.save()
    sent_mail(researcher.email)
    return redirect('researcher_requests')

def researcher_request_reject(request, researcher_id):
    researcher = Base_User.objects.get(user_id=researcher_id)
    researcher.delete()
    return redirect('researcher_requests')

@login_required(login_url='/login')
@user_verified
def raised_issues(request):
    issues_raised = Base_Issue.objects.filter(is_verified=False)
    if request.user.user_type == 0:
        return render(request, 'main/raised_issues.html',{'issues_raised':issues_raised})
    else:
        return render(request, 'Organiser/raised_issues.html',{'issues_raised':issues_raised})    

@login_required(login_url='/login')
def donations(request):
    donations_received = Base_Donations.objects.all()
    return render(request, 'main/donations.html',{'donations_received':donations_received})




@login_required(login_url='/login')
def volunteer(request):
    today = timezone.now().date()
    events = Base_Events.objects.filter(
    Q(event_date__gte=today) &
    ~Q(event_id__in=Base_Volunteer.objects.filter(user_id=request.user).values('event_id')))
    event_volunteers = dict()
    for event in events:
        volunteers_count = Base_Volunteer.objects.filter(event_id=event).count()
        event_volunteers[event]=volunteers_count

    registered_events = Base_Events.objects.filter(
    Q(event_date__gte=today) &
    Q(event_id__in=Base_Volunteer.objects.filter(user_id=request.user).values('event_id')))
    registered_event_volunteers = dict()
    for event in registered_events:
        registered_volunteers_count = Base_Volunteer.objects.filter(event_id=event).count()
        registered_event_volunteers[event]=registered_volunteers_count
        
    context = {'event_volunteers':event_volunteers,'registered_event_volunteers': registered_event_volunteers}
    return render(request, 'endUser/volunteer.html',context)

@login_required(login_url='/login')
def register_event(request, event_id):
    event = Base_Events.objects.get(event_id=event_id)
    Base_Volunteer.objects.create(
        event_id=event,
        user_id=request.user
    )
    return redirect('volunteer')

@login_required(login_url='/login')
def unregister_event(request, event_id):
    event = Base_Volunteer.objects.get(event_id=event_id,user_id=request.user)
    event.delete()
    return redirect('volunteer')

    

@login_required
def raise_issues(request):
    if request.method == 'POST':
        location = request.POST.get('Location')
        issues = request.POST.get('issues')
        issue_date = request.POST.get('issue-date')
        
        uploaded_image = request.FILES.get('Img')
        
        today = timezone.now().date() 

        # if uploaded_image:
        try:
            if not uploaded_image:
                raise ValidationError("Image not uploaded")
            elif uploaded_image.size > 2 * 1024 * 1024:
                raise ValidationError("File size must be less than 2 mb.")
            elif not uploaded_image.content_type.startswith('image/'):
                raise ValidationError("Only image files are allowed.")
            elif date.fromisoformat(issue_date) > today:
                raise ValidationError("Date must be valid.")
            
            image_path = f'uploads/{uploaded_image.name}'
            with open(os.path.join(settings.MEDIA_ROOT, image_path), 'wb') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)
            
            Base_Issue.objects.create(
                user_id=request.user,
                location=location,
                issues=issues,
                issue_date=issue_date,
                img=image_path
            )
            messages.success(request, 'Issue raised successfully')
            
        except ValidationError as e:
            request.session['data'] = {
            'location' : location,
            'issues' : issues,
            }
            msg = str(e).strip('[]\'"')
            messages.error(request, msg)
            
        return redirect('raise_issues')
    
    if request.session.get('data'):
        context = request.session.get('data')
        del request.session['data']
    else:
        context = { }
    return render(request, 'endUser/raise_issues.html', context)

@login_required(login_url='/login')
def marketPlace(request):
    items = Base_Items.objects.all()
    context = {'items': items}
    return render(request, 'endUser/marketPlace.html', context)

@login_required(login_url='/login')
def active_orders(request):
    active_orders = Base_Order.objects.filter(is_delivered=False, is_cancelled=False, customer_id=request.user)
    orders = Base_Order.objects.filter(is_delivered=True, is_cancelled=False, customer_id=request.user)

    context = {
        'active_orders': active_orders,
        'orders': orders,
    }

    return render(request, 'endUser/active_orders.html', context)


@login_required(login_url='/login')
def cancel_order(request, order_id):
    order = Base_Order.objects.get(order_id=order_id)
    qty, item = order.qty, order.item_id
    item = Base_Items.objects.get(item_id=item.item_id)
    stock = item.stock + int (qty)
    item.stock = stock
    item.save()
    order.is_cancelled = True
    order.save()
    return redirect('orders_')

@login_required(login_url='/login')
def buy_item(request, item_id):
    item = Base_Items.objects.get(item_id=item_id)
    if request.method == 'POST':
        qty = request.POST.get('qty')
        itemPrice = item.price
        total = int(qty)*float(itemPrice)

        product = stripe.Product.create(name=item.item_name)

# Create a price for the product
        price = stripe.Price.create(
            unit_amount=int(itemPrice)*100,  # The amount in cents (e.g., 2000 for $20.00)
            currency='inr',
            product=product.id,
        )

        session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price.id,  # Use the price ID here
                'quantity': qty,
            },
        ],
        mode='payment',
        success_url='http://127.0.0.1:8000/payment_success',
        cancel_url='http://127.0.0.1:8000/payment_cancelled',
        )
        request.session['data'] = { 'payment' : 'payment' ,'item_id' : item_id, 'qty': qty} 
        return redirect(session.url, code=303)

        # return redirect('marketPlace')
    
    context = {'item': item}
    return render(request, 'endUser/buy_item.html', context)

@login_required(login_url='/login')
def resources(request):
    view_resources = Base_Resources.objects.all()
    context = {'view_resources': view_resources}
    return render(request, 'endUser/resources.html',context)


@login_required
def donate(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')

        product = stripe.Product.create(name='Donate')

# Create a price for the product
        price = stripe.Price.create(
            unit_amount=int(amount)*100,  # The amount in cents (e.g., 2000 for $20.00)
            currency='inr',
            product=product.id,
        )

        session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price.id,  # Use the price ID here
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='http://127.0.0.1:8000/payment_success',
        cancel_url='http://127.0.0.1:8000/payment_cancelled',
        )
        request.session['data'] = { 'payment' : 'donation', 'amount' : amount }
        return redirect(session.url, code=303)
    context = {'key': settings.STRIPE_PUBLISHABLE_KEY}
    return render(request, 'endUser/donate.html', context)


@login_required(login_url='/login')
@user_verified
def organise_event(request):
    if request.method == 'POST':
        location = request.POST.get('Location')
        task = request.POST.get('task')
        no_of_volunteers = request.POST.get('no-of-volunteers')
        event_date = request.POST.get('event-date')

        today = timezone.now().date()
        if date.fromisoformat(event_date) < today:
            messages.error(request, 'Event date must be in the future')
            request.session['data'] = {
            'location' : location,
            'task' : task,
            'no_of_volunteers' : no_of_volunteers
            }
            return redirect('organise_event')
        

        Base_Events.objects.create(
            organiser_id=request.user,
            location=location,
            task=task,
            no_of_volunteers=no_of_volunteers,
            event_date=event_date
        )
        return redirect('manage_volunteers')
    
    if request.session.get('data'):
        context = request.session.get('data')
        del request.session['data']
    else:
        context = { }

    return render(request, 'Organiser/organise_event.html', context)

@login_required(login_url='/login')
@user_verified
def manage_volunteers(request):
    today = timezone.now().date()
    events = Base_Events.objects.filter(event_date__gte=today, organiser_id = request.user)

    event_volunteers = dict()
    for event in events:
        volunteers_count = Base_Volunteer.objects.filter(event_id=event).count()
        event_volunteers[event]=volunteers_count
    
    context = {'event_volunteers': event_volunteers}
    return render(request, 'Organiser/manage_volunteers.html', context)

@login_required(login_url='/login')
@user_verified
def manage_volunteer_details(request, event_id):
    volunteers = Base_Volunteer.objects.filter(event_id=event_id)
    context = { 'volunteers': volunteers }
    request.session['data'] = { 'event_id': event_id }
    return render(request, 'Organiser/manage_volunteer_details.html', context)

@login_required(login_url='/login')
@user_verified
def remove_volunteer(request, volunteer_id):
    volunteer = Base_Volunteer.objects.get(volunteer_id=volunteer_id)
    volunteer.delete()
    event_id = request.session.get('data')['event_id']
    del request.session['data']
    return redirect('manage_volunteer_details', event_id = event_id)




@login_required(login_url='/login')
@user_verified
def orders(request):
    active_orders = Base_Order.objects.filter(is_delivered=False, is_cancelled = False, supplier_id=request.user)
    orders = Base_Order.objects.filter(is_delivered=True, is_cancelled = False, supplier_id=request.user)
    for order in orders:
        order.total = order.qty * order.price
    context = {'active_orders':active_orders,'orders': orders}
    return render(request, 'Supplier/orders.html', context)

@login_required(login_url='/login')
@user_verified
def list_items(request):
    items = Base_Items.objects.filter(supplier_id=request.user)
    context = {'items': items}
    return render(request, 'Supplier/list_items.html', context)

@login_required(login_url='/login')
@user_verified
def add_item(request):
    if request.method == 'POST':
        item_name = request.POST.get('item-name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        
        uploaded_image = request.FILES.get('Img')
        
        # if uploaded_image:
        try:
            if not uploaded_image:
                raise ValidationError("Image not uploaded")
            if uploaded_image.size > 2 * 1024 * 1024:
                raise ValidationError("File size must be below 2 mb.")
            if not uploaded_image.content_type.startswith('image/'):
                raise ValidationError("Only image files are allowed.")
            
            image_path = f'uploads/{uploaded_image.name}'
            with open(os.path.join(settings.MEDIA_ROOT, image_path), 'wb') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)
            
            Base_Items.objects.create(
                supplier_id=request.user,
                item_name=item_name,
                img=image_path,
                price=price,
                stock=stock,
                description=description 
            )
            return redirect('list_items') 
            
        except ValidationError as e:
            msg = str(e).strip('[]\'"')
            messages.error(request, msg)
            request.session['data'] = {
                'item_name' : item_name,
                # 'img' : image_path,
                'price' : price,
                'stock' : stock,
                'description' : description 
            }
            return redirect('add_item_')
        
    if request.session.get('data'):
        context = request.session.get('data')
        del request.session['data']
    else:
        context = {}
    return render(request, 'Supplier/add_item.html', context)


@login_required(login_url='/login')
@user_verified
def cancelled_orders(request):
    orders = Base_Order.objects.filter(supplier_id=request.user, is_cancelled=True)
    context = {'orders': orders}
    return render(request, 'Supplier/cancelled_orders.html', context)

@login_required(login_url='/login')
@user_verified
def return_pay(request, order_id):
    orders = Base_Order.objects.get(order_id=order_id)
    amount = orders.total
    productName = 'Return ' + orders.item_id.item_name

    product = stripe.Product.create(name=productName)

# Create a price for the product
    price = stripe.Price.create(
        unit_amount=int(amount)*100,  # The amount in cents (e.g., 2000 for $20.00)
        currency='inr',
        product=product.id,
    )

    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[
        {
            'price': price.id,  # Use the price ID here
            'quantity': 1,
        },
    ],
    mode='payment',
    success_url='http://127.0.0.1:8000/payment_success',
    cancel_url='http://127.0.0.1:8000/payment_cancelled',
    )
    request.session['data'] = { 'payment' : 'return', 'order_id' : orders.order_id }
    return redirect(session.url, code=303)

 
@login_required(login_url='/login')
@user_verified
def edit_item(request, item_id):
    item = Base_Items.objects.get(item_id=item_id)
    if request.method == 'POST':
        item_name = request.POST.get('item-name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        
        uploaded_image = request.FILES.get('Img')
        
        try:
            if not uploaded_image:
                raise ValidationError("Image not uploaded")
            if uploaded_image.size > 2 * 1024 * 1024:
                raise ValidationError("File size must be below 2 mb.")
            if not uploaded_image.content_type.startswith('image/'):
                raise ValidationError("Only image files are allowed.")
            
            image_path = f'uploads/{uploaded_image.name}'
            with open(os.path.join(settings.MEDIA_ROOT, image_path), 'wb') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            item.item_name = item_name
            item.price = price
            item.stock = stock
            item.description = description
            item.img = image_path
            
        except ValidationError as e:
            msg = str(e).strip('[]\'"')
            messages.error(request, msg)
            request.session['data'] = {
                'item_name' : item_name,
                # 'img' : image_path,
                'price' : price,
                'stock' : stock,
                'description' : description 
            }
            return redirect('edit_item', item_id = item_id)
        
        item.save()
        return redirect('list_items') 
    if request.session.get('data'):
        context = request.session.get('data')
        del request.session['data']
    else:
        context = {'item': item}    
    return render(request, 'Supplier/edit_item.html',context)

@login_required(login_url='/login')
@user_verified
def delete_item(request, item_id):
    item = Base_Items.objects.get(item_id=item_id)
    item.delete()
    return redirect('list_items')

@login_required(login_url='/login')
@user_verified
def order_delivered(request, order_id):
    order = Base_Order.objects.get(order_id=order_id)
    order.is_delivered = True
    order.delivered_date = timezone.now().date()
    order.save()
    return redirect('orders')




@login_required(login_url='/login')
@user_verified
def publish_paper(request):
    if request.method == 'POST':
        description = request.POST.get('description')

        uploaded_file = request.FILES.get('publish-file')

        # if uploaded_file:
        try:
            if uploaded_file.size > 10 * 1024 * 1024:
                raise ValidationError("File size must be below 10 mb.")
            if not uploaded_file.content_type.startswith('application/pdf'):
                raise ValidationError("Only PDF files are allowed.")

            file_path = f'uploads/{uploaded_file.name}'
            with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            Base_Resources.objects.create(
                publisher_id=request.user,
                published_date=timezone.now(),
                description=description,
                published_file=file_path
            )
            return redirect('manage_resources')
        except ValidationError as e:
            msg = str(e).strip('[]\'"')
            messages.error(request, msg)
            request.session['data'] = {
                'description' : description 
            }
            return redirect('publish_paper')
            
    if request.session.get('data'):
        context = request.session.get('data')
        del request.session['data']
    else:
        context = {}

    return render(request, 'Researcher/publish_paper.html', context)


@login_required(login_url='/login')
@user_verified
def manage_resources(request):
    resources = Base_Resources.objects.filter(publisher_id=request.user)
    context = {'resources': resources}

    return render(request, 'Researcher/manage_resources.html',context)


@login_required(login_url='/login')
@user_verified
def delete_resource(request, resource_id):
    resource = Base_Resources.objects.get(resource_id=resource_id)
    resource.delete()
    return redirect('manage_resources')





def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Base_User.objects.get(email=email)
        except Base_User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('login')
        
        
        user_login = authenticate(request, email=email, password=password)

        if user_login is not None:
            login(request, user_login)
            if user_login.user_type == 0:
                return redirect('organiser_requests')
            elif user_login.user_type == 1:
                return redirect('volunteer')
            elif user_login.user_type == 2:
                return redirect('organise_event')
            elif user_login.user_type == 3:
                return redirect('orders')
            elif user_login.user_type == 4:
                return redirect('publish_paper')
        else:
            messages.error(request, "Invalid password")
            request.session['data'] = { 'email' : email }
            return redirect('login')
        
    if request.session.get('data'):
        context = request.session.get('data')
        del request.session['data']
    else:
        context = {}
 
    return render(request, 'login.html', context)




def userRegister(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('name')
        contact = request.POST.get('number')
        location = request.POST.get('location')
        email = request.POST.get('email')
        password = request.POST.get('password')
        pincode = request.POST.get('pincode')
        user_type = request.POST.get('usertype')

        if Base_User.objects.filter(email=email).exists():
            messages.info(request, 'Email already taken')
            request.session['data'] = { 
            'name': username, 
            'contact': contact, 
            'location': location,
            'email': email,
            'pincode': pincode,
            }
            return redirect('register')
        # elif Base_User.objects.filter(username=username).exists():
        #     messages.info(request, 'Username already taken')
        #     return redirect('register')
        if len(password) < 4 or len(password) > 10:
            messages.info(request, 'Password must be between 4 to 10 characters')
            request.session['data'] = { 
            'name': username, 
            'contact': contact, 
            'location': location,
            'email': email,
            'pincode': pincode,
            }
            return redirect('register')
        elif user_type is None or user_type == '0':
            messages.error(request, 'User type not specified')
            request.session['data'] = { 
            'name': username, 
            'contact': contact, 
            'location': location,
            'email': email,
            'pincode': pincode,
            }
            return redirect('register')
        else:
            hashed_password = make_password(password)
            x = Base_User.objects.create(
                username=username,
                contact=contact,
                location=location,
                pincode = pincode,
                email=email,
                user_type=user_type,
                password=hashed_password, 
            )
            x.save()
            user_login = authenticate(request, email=email, password=password)

            if user_login is not None:
                login(request, user_login)
                if user_login.user_type == 0:
                    return redirect('organiser_requests')
                elif user_login.user_type == 1:
                    return redirect('volunteer')
                elif user_login.user_type == 2:
                    return redirect('organise_event')
                elif user_login.user_type == 3:
                    return redirect('orders')
                elif user_login.user_type == 4:
                    return redirect('publish_paper')
                
    if request.session.get('data'):
        context = request.session.get('data')
        del request.session['data']
    else:
        context = { }

    return render(request, 'register.html', context)


@login_required(login_url='/login')
def logoutUser(request):
    logout(request)

    return redirect('login')


@login_required(login_url='/login')
def userProfile(request, user_id):
    user = Base_User.objects.get(user_id=user_id)
    context = {'user': user}
    return render(request, 'user_profile.html', context)

@login_required(login_url='/login')
def itemDescription(request, item_id):
    item = Base_Items.objects.get(item_id=item_id)
    context = {'item': item}
    return render(request, 'item_description.html', context)

@login_required(login_url='/login')
def not_verified(request):
    return render(request, 'not_verified.html')

@login_required(login_url='/login')
def issues_raised(request):
    active_issues = Base_Issue.objects.filter(is_verified=True, is_closed=False)
    issues = Base_Issue.objects.filter(is_closed=True)
    context = {'active_issues':active_issues,'issues': issues}
    return render(request, 'issues_raised.html',context)

@login_required(login_url='/login')
def view_issue(request, issue_id):
    issue = Base_Issue.objects.get(issue_id=issue_id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        # issue = Base_Issue.objects.get(issue_id=issue_id)
        Base_Discussions.objects.create(
            user_id = request.user,
            comment = comment,
            issue_id = issue,
            datetime = timezone.now()
        )
        return redirect('view_issue_', issue_id=issue_id)
    comments = Base_Discussions.objects.filter(issue_id=issue_id)
    context = {'issue':issue,'comments':comments}
    return render(request, 'view_issue.html', context)

@login_required(login_url='/login')
@admin_only
def close_issue(request, issue_id):
    issue = Base_Issue.objects.get(issue_id=issue_id)
    issue.is_closed = True
    issue.save()
    return redirect('issues_raised')

@login_required(login_url='/login')
def issue_approve(request, issue_id):
    issue = Base_Issue.objects.get(issue_id=issue_id)
    issue.is_verified = True
    issue.save()
    return redirect('raised_issues')

@login_required(login_url='/login')
def issue_reject(request, issue_id):
    issue = Base_Issue.objects.get(issue_id=issue_id)
    issue.delete()
    return redirect('raised_issues')


@login_required(login_url='/login')
def payment_success(request):
    data = request.session.get('data')
    del request.session['data']
    if data.get('payment') == 'payment':
        item_id = data.get('item_id')
        qty = data.get('qty')
        item = Base_Items.objects.get(item_id=item_id)
        supplier_id = item.supplier_id
        customer_id = request.user
        item_id = item
        qty = qty
        itemPrice = item.price
        total = int(qty)*float(itemPrice)

        today = timezone.now()
        expected = today + timedelta(days=3)

        Base_Order.objects.create(
            supplier_id=supplier_id, 
            customer_id=customer_id,
            item_id=item_id,qty=qty, 
            price=itemPrice, 
            total=total,
            date=timezone.now(),
            delivered_date=expected
        )
        stock = item.stock - int(qty)
        item.stock = stock
        item.save()
    elif data.get('payment') == 'return':
        order_id = data.get('order_id')
        order = Base_Order.objects.get(order_id=order_id)
        order.delete()
    else:
        amount = data.get('amount')
        Base_Donations.objects.create(
            donator_id=request.user,
            amount=amount,
            dated=timezone.now()
        )
    context = { 'payment' : data.get('payment') }
    return render(request, 'payment-success.html', context)

@login_required(login_url='/login')
def payment_cancelled(request):
    data = request.session.get('data')
    del request.session['data']
    context = { 'payment' : data.get('payment') }
    return render(request, 'payment-cancelled.html', context)