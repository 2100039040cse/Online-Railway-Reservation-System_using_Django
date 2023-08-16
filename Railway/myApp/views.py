from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import ensure_csrf_cookie
from myApp.models import Train, Passenger
from datetime import datetime
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserRegistrationForm, PassengerForm

# Create your views here.
def home(request):
    context={}
    return render(request,"myApp/UserRegister.html",context)


def get_filtered_trains(from_station, to_station, date):
    # Implement your logic here to filter trains based on the parameters
    # Return the filtered trains as a queryset or a list of train objects
    # Example:
    trains = Train.objects.filter(
        from_station__icontains=from_station,
        to_station__icontains=to_station,
        date=date
    )
    return trains



def user_view_trains(request):
    if request.method == 'POST':
        from_station = request.POST.get('from-station')
        to_station = request.POST.get('to-station')
        date = request.POST.get('date')

        # Retrieve the train details from the database based on the selected values
        trains = Train.objects.filter(
            from_station=from_station,
            to_station=to_station,
            date=date
        )

        if trains.exists():
            # Render the user_view_trains.html template with the train details
            return render(request, 'UserViewTrains.html', {'trains': trains})
        else:
            return render(request, 'UserViewTrains.html', {'error_message': 'No trains found.'})

    else:
        return render(request, 'UserViewTrains.html')




def my_bookings(request):
    context = {}
    return render(request, "myApp/MyBookings.html", context)
def pnr_status(request):
    context = {}
    return render(request, "myApp/PNRStatus.html", context)
def avail_ability(request):
    context = {}
    return render(request, "myApp/Availability.html", context)


def user_profile(request):
    # Retrieve the user's profile using the logged-in user's information
    profile = UserProfile.objects.get(user=request.user)
    
    return render(request, 'UserProfile.html', {'profile': profile})

def view_trains(request):
    trains = Train.objects.all()
    return render(request, 'AdminViewTrains.html', {'trains': trains})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pword')

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('myApp:user-home')
            else:
                messages.error(request, 'Invalid credentials.')
                return redirect('myApp:user-login')
        else:
            messages.error(request, 'Please enter your credentials.')
            return redirect('myApp:user-login')
    else:
        messages.info(request, 'Please login.')
        return render(request, 'UserLogin.html')

def user_register(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pword = request.POST['pword']
        aadhar = request.POST['aadhar']
        dob = request.POST['dob']
        address = request.POST['address']
        phoneno = request.POST['phoneno']
        mailid = request.POST['mailid']

        # Create a new user
        user = User.objects.create_user(username=uname, password=pword)
        user.save()

        # Create a UserProfile and associate it with the User
        profile = UserProfile(user=user, aadhar=aadhar, dob=dob, address=address, phoneno=phoneno, mailid=mailid)
        profile.save()

        messages.success(request, 'Registration successful! You can now login.')
        return redirect('myApp:user-login')  # Redirect to UserLogin.html

    return render(request, 'UserRegister.html')


def user_home(request):
    return render(request, 'UserHome.html')


def user_confirm_train(request):
    if request.method == 'POST':
        train_id_str = request.POST.get('train_id')

        # Check if train_id_str is not None and not an empty string
        if train_id_str:
            try:
                train_id = int(train_id_str)
                train = Train.objects.get(id=train_id)

                # Store the train_id and user-entered data in the session
                request.session['selected_train_id'] = train_id
                request.session['passenger_data'] = request.POST

                return redirect('myApp:user-payment-view')  # Redirect to UserPayment.html

            except (ValueError, Train.DoesNotExist):
                # Handle the case when train_id cannot be converted to an integer or the train does not exist
                # For example, redirect to an error page or user_view_trains page
                return redirect('myApp:user-view-trains')

    # Retrieve the train details for rendering in the template
    train_id = request.session.get('selected_train_id')
    if train_id:
        try:
            train = Train.objects.get(id=train_id)
        except Train.DoesNotExist:
            train = None
    else:
        train = None

    return render(request, 'UserConfirmtrain.html', {'train': train})

def user_payment_confirm(request):
    if request.method == 'POST':
        train_id_str = request.POST.get('train_id')

        if train_id_str:
            try:
                train_id = int(train_id_str)
                # train = Train.objects.get(id=train_id)

                # Store the train_id and user-entered data in the session
                request.session['selected_train_id'] = train_id
                request.session['passenger_data'] = request.POST

                return redirect('myApp:user-payment-view')  # Redirect to UserPayment.html

            except (ValueError, Train.DoesNotExist):
                # Handle the case when train_id cannot be converted to an integer or the train does not exist
                # For example, redirect to an error page or user_view_trains page
                return redirect('myApp:user-view-trains')

    return render(request, 'UserConfirmtrain.html')

def user_payment_view(request):
    train_id = request.session.get('selected_train_id')
    if train_id is None:
        return redirect('myApp:user-view-trains')

    try:
        train = Train.objects.get(id=train_id)

        # Retrieve passenger_data from session and populate the form
        passenger_data = request.session.get('passenger_data', {})
        form = PassengerForm(initial=passenger_data)

        if request.method == 'POST':
            form = PassengerForm(request.POST)
            if form.is_valid():
                passenger_data = form.cleaned_data
                passenger = Passenger(
                    train=train,
                    name=passenger_data['name'],
                    age=passenger_data['age'],
                    gender=passenger_data['gender'],
                    nationality=passenger_data['nationality'],
                    email=passenger_data['email'],
                    address=passenger_data['address'],
                    berth=passenger_data['berth'],
                    acCategory=passenger_data['acCategory']
                )
                passenger.save()

                # Clear the session data after saving the passenger details
                request.session['selected_train_id'] = None
                request.session['passenger_data'] = None

                # Display a success message
                messages.success(request, 'Payment successful!')

                # Redirect to UserPaymenttype.html and pass the passenger details as context
                return redirect('myApp:user-payment-type')

        return render(request, 'UserPayment.html', {'train': train, 'form': form})

    except Train.DoesNotExist:
        # Handle the case when the train does not exist
        # For example, redirect to an error page or user_view_trains page
        return redirect('myApp:user-view-trains')







def user_payment(request):
    return render(request, 'UserPayment.html')
    



def user_payment_type(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment-method')

        passenger_details = {}
        passenger_fields = ['passenger_name', 'passenger_age', 'passenger_gender', 'passenger_contact']
        for field in passenger_fields:
            passenger_details[field] = request.POST.get(field)

        return render(request, 'PaymentStatus.html', {
            'payment_method': payment_method,
            'passenger_data': passenger_details,  # Pass the data using 'passenger_data' key
        })

    return render(request, 'UserPaymenttype.html')



def payment_status(request):
    
    train_id = request.session.get('selected_train_id')
    if train_id is None:
        return redirect('myApp:user-view-trains')

    try:
        train = Train.objects.get(id=train_id)

        # Retrieve passenger_data from session and populate the form
        passenger_data = request.session.get('passenger_data', {})
        form = PassengerForm(initial=passenger_data)

        if request.method == 'POST':
            form = PassengerForm(request.POST)
            if form.is_valid():
                passenger_data = form.cleaned_data
                passenger = Passenger(
                    train=train,
                    name=passenger_data['name'],
                    age=passenger_data['age'],
                    gender=passenger_data['gender'],
                    nationality=passenger_data['nationality'],
                    email=passenger_data['email'],
                    address=passenger_data['address'],
                    berth=passenger_data['berth'],
                    acCategory=passenger_data['acCategory']
                )
                passenger.save()

                # Clear the session data after saving the passenger details
                request.session['selected_train_id'] = None
                request.session['passenger_data'] = None

                # Display a success message
                messages.success(request, 'Payment successful!')

                # Redirect to PaymentStatus.html and pass the passenger details as context
                return render(request, 'PaymentStatus.html', {'payment_method': 'Credit Card', 'passenger_data': passenger_data})

        return render(request, 'UserPayment.html', {'train': train, 'form': form})

    except Train.DoesNotExist:
        # Handle the case when the train does not exist
        # For example, redirect to an error page or user_view_trains page
        return redirect('myApp:user-view-trains')



def user_payment_type(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment-method')

        passenger_details = {}
        passenger_fields = ['passenger-name', 'passenger-age', 'passenger-gender', 'passenger-contact']
        for field in passenger_fields:
            passenger_details[field] = request.POST.get(field)

        
        return render(request, 'PaymentStatus.html', {
            'payment_method': payment_method,
            'passenger_details': passenger_details,
            
        })

    return render(request, 'UserPaymenttype.html')






















@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@ensure_csrf_cookie
def admin_super_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            # Authentication successful, redirect to admin home or any other desired page
            return redirect('myApp:admin-home')
        else:
            # Authentication failed or user is not a superuser, show error message
            messages.error(request, 'Invalid credentials')
            return redirect('myApp:admin-login')
    else:
        context = {}
        return render(request, "myApp/AdminLogin.html", context)




def admin_add_train(request):
    if request.method == 'POST':
        train_number = request.POST.get('trainno')
        train_name = request.POST.get('trainname')
        from_station = request.POST.get('fromstation')
        to_station = request.POST.get('tostation')
        available = request.POST.get('available')
        fare = request.POST.get('fare')
        selected_date_str = request.POST.get('date')
        selected_time = request.POST.get('time')  # Get the selected time from the form
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

        train = Train(
            train_number=train_number,
            train_name=train_name,
            from_station=from_station,
            to_station=to_station,
            available=available,
            fare=fare,
            date=selected_date,
            time=selected_time,  # Assign the selected time to the 'time' field
        )
        train.save()

        # Pass the selected_time variable to the template context
        return redirect('myApp:view-trains')

    return render(request, 'AdminAddTrains.html')



def admin_cancel_train(request):
    if request.method == 'POST':
        train_no = request.POST.get('trainno', '')  # Get the value of 'trainno' or use an empty string if not found
        if train_no:
            train = Train.objects.filter(train_number=train_no)
            if train.exists():
                # Handle the queryset accordingly
                train.delete()  # Example: Delete all matching trains
                return redirect('myApp:view-trains')
            else:
                return render(request, 'myApp/AdminCancleTrain.html', {'error_message': 'Train not found.'})
        else:
            return render(request, 'myApp/AdminCancleTrain.html', {'error_message': 'Invalid train number.'})
    else:
        return render(request, 'myApp/AdminCancleTrain.html')

    
def admin_search_train(request):
    if request.method == 'POST':
        train_no = request.POST['trainnumber']
        print("Train Number:", train_no)

        # Retrieve the train details from the database
        trains = Train.objects.filter(train_number=train_no)
        print("Queryset:", trains)

        if trains.exists():
            # Render the AdminSearchTrain.html template with the train details
            return render(request, 'AdminSearchTrain.html', {'trains': trains})
        else:
            return render(request, 'AdminSearchTrain.html', {'error_message': 'Train not found.'})

    else:
        return render(request, 'AdminSearchTrain.html')
    




def admin_view_trains(request):
    trains = Train.objects.all()
    context = {'trains': trains}
    return render(request, 'myApp/AdminViewTrains.html', context)


def admin_update_train(request):
    context = {}
    return render(request, "myApp/AdminUpdateTrain.html", context)

def add_trains(request):
    context = {}
    return render(request, "myApp/AdminAddTrains.html", context)


def admin_login(request):
    context = {}
    return render(request, "myApp/AdminLogin.html", context)

def admin_home(request):
    context = {}
    return render(request, "myApp/AdminHome.html", context)

def cancle_train(request):
    context = {}
    return render(request, "myApp/AdminCancleTrain.html", context)

def admin_search_train(request):
    context = {}
    return render(request, "myApp/AdminSearchTrain.html", context)