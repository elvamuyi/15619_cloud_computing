from django.http import HttpResponse
from cloud.backend import q2_hbase, q3_hbase, q4_hbase
import datetime

TEAMID = 'Alvin'
AWS_ACCOUNT_ID = '3374-9456-1394'

def hello(request):
    return HttpResponse("Hello world")

def q1(request):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = TEAMID + ", " + AWS_ACCOUNT_ID + "\n" + now
    return HttpResponse(response)

def q2(request):
    time = request.GET.get('time')
    response = TEAMID + ", " + AWS_ACCOUNT_ID + "\n"
    response += q2_hbase(time)
    return HttpResponse(response)
#    return HttpResponse('time: ' + time)

def q3(request):
    userid_min = request.GET.get('userid_min')
    userid_max = request.GET.get('userid_max')
    response = TEAMID + ", " + AWS_ACCOUNT_ID + "\n"
    response += q3_hbase(userid_min, userid_max)
    return HttpResponse(response)
#    return HttpResponse('userid_min: ' + userid_min +' userid_max: ' + userid_max)
    
def q4(request):
    userid = request.GET.get('userid')
    response = TEAMID + ", " + AWS_ACCOUNT_ID + "\n"
    response += q4_hbase(userid)
    return HttpResponse(response)
#    return HttpResponse('userid: ' + userid)
