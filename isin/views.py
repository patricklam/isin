from django.shortcuts import render
from isin.models import Status

from dns import resolver, reversename
from datetime import datetime, timedelta
import pytz

def get_most_recent_status_if_available():
    isin = Status.objects.order_by('pub_date').last()
    if (isin == None):
        isin = Status(status = "without status.", pub_date = "N/A")
    return isin

def index(request):
    params = request.POST
    uid = request.user.username
    as_staff = request.user.is_staff and not('fake' in params and params['fake'] != '')
    s = get_most_recent_status_if_available()
    context = {'s' : s}
    return render(request, 'in/index.html', context)

def update(request):
    if not request.user.is_staff: 
        return index(request)

    params = request.POST
    msgs = ''
    if 'status' in params:
        eastern=pytz.timezone('US/Eastern')
        s = params['status'].replace('_', ' ')
        if s == 'other': s = params['other_status']
        Status(status=s, pub_date=datetime.now(eastern)).save()
        msgs = msgs + "Reset status to "+s+".<br />"
    s = get_most_recent_status_if_available()
    context = {'s' : s,
               'msgs' : msgs}
    return render(request, 'in/update.html', context)

def quick_update(request):
    if not request.user.is_staff: return render(request, 'in/index.html', {})
    eastern=pytz.timezone('US/Eastern')

    msgs = 'unknown IP'
    ip = request.META.get('REMOTE_ADDR')
    if (ip == '129.97.90.101'): 
        msgs = 'cambridge'
        Status(status='in DC2597D.', pub_date=datetime.now(eastern)).save()
    else:
        ip_addr = reversename.from_address(ip)
        ip_text = str(resolver.query(ip_addr, "PTR")[0])
        if (ip_text.endswith("teksavvy.com.")): 
            msgs = 'home'
            Status(status='out', pub_date=datetime.now(eastern)).save()
    s = get_most_recent_status_if_available()
    context = {'s' : s,
               'msgs' : msgs}
    return render(request, 'in/update.html', context)
