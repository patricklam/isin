from django.shortcuts import render
from isin.models import Status

from dns import resolver, reversename
from datetime import datetime, timedelta
import pytz

def index(request):
    params = request.POST
    uid = request.user.username
    as_superuser = request.user.is_superuser and not('fake' in params and params['fake'] != '')
    isin = Status.objects.first()
    context = {'who' : uid,
               'in' : isin.status}
    return render(request, 'in/index.html', context)

def init(request):
    if not request.user.is_superuser: return render(request, 'in/index.html', {})

    params = request.POST
    msgs = ''
    if 'status' in params:
        eastern=pytz.timezone('US/Eastern')
        Status.objects.all().delete()
        s = params['status'].replace('_', ' ')
        if s == 'other': s = params['other_status']
        Status(status=s, pub_date=datetime.now(eastern)).save()
        msgs = msgs + "Reset status to "+s+".<br />"
    return render(request, 'in/init.html', {'msgs': msgs})

def quickinit(request):
    if not request.user.is_superuser: return render(request, 'in/index.html', {})
    eastern=pytz.timezone('US/Eastern')

    msgs = 'unknown IP'
    ip = request.META.get('REMOTE_ADDR')
    if (ip == '129.97.90.101'): 
        msgs = 'cambridge'
        Status(status='in DC2597D', pub_date=datetime.now(eastern)).save()
    ip_addr = reversename.from_address(ip)
    ip_text = str(resolver.query(ip_addr, "PTR")[0])
    if (ip_text.endswith("teksavvy.com.")): 
        msgs = 'home'
        Status(status='out', pub_date=datetime.now(eastern)).save()
    return render(request, 'in/init.html', {'msgs': msgs})
