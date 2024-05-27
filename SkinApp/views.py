from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import home, about, OurTeam, teamMemebers, Treatments, clinicInfo, Appointment
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.
def index(request):
    homeDB = home.objects.get(pk=1)
    aboutDB = about.objects.get(pk=1)
    OurTeamDB = OurTeam.objects.get(pk=1)
    TreatmentsDB = Treatments.objects.all()
    clinicInfoDB = clinicInfo.objects.get(pk=1)
    teamMemebersDB = teamMemebers.objects.all()
    return render(request, 'index.html', {
        'homeDB':homeDB,
        'aboutDB':aboutDB,
        'OurTeamDB':OurTeamDB,
        'TreatmentsDB':TreatmentsDB,
        'clinicInfoDB':clinicInfoDB,
        'teamMemebersDB':teamMemebersDB
    })

def booking(request):
    clinicInfoDB = clinicInfo.objects.get(pk=1)
    appointmentDB = Appointment.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        time = request.POST.get('time')
        date = request.POST.get('date')
        description = request.POST.get('description')
        # Create an instance of the Appointment model
        if description:
            appointment = Appointment(
                name=name,
                email=email,
                phone=phone,
                time=time,
                date=date,
                description=description
            )
        else:
                appointment = Appointment(
                name=name,
                email=email,
                phone=phone,
                time=time,
                date=date
            )
        # Save the instance to the database
        appointment.save()
        clinicInfoDB = clinicInfo.objects.get(pk=1)

        html_message = render_to_string('email_template.html', {
            'name': name,
            'email': email,
            'phone': phone,
            'time': time,
            'date': date,
            'description': description,
        })
        plain_message = strip_tags(html_message)

        subject = f'Newage Skincare Clinic Booking'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['newageskincareclinic@gmail.com', email]
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

        return render(request, 'booking.html', {
            'clinicInfoDB':clinicInfoDB,
            'appoints' : appointmentDB
        })
    else:
        return render(request, 'booking.html', {
            'clinicInfoDB':clinicInfoDB,
            'appoints' : appointmentDB
        })