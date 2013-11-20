from django.http import HttpResponse
import datetime

TEAMID = 'Alvin'
AWS_ACCOUNT_ID = '3374-9456-1394'

def hello(request):
    return HttpResponse("Hello world")

def q1(request):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = "<html><body><p>%s, %s</p><p>%s</p></body></html>" % (TEAMID, AWS_ACCOUNT_ID, now)
    return HttpResponse(html)

def q2(request):
    time = request.GET.get('time')
    return HttpResponse('Time: ' + time)

def q3(request):
    userid_min = request.GET.get('userid_min')
    userid_max = request.GET.get('userid_max')
    return HttpResponse('userid_min: ' + userid_min +' userid_max: ' + userid_max)
