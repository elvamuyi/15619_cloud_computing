from django.http import HttpResponse
import datetime

def hello(request):
    return HttpResponse("Hello world")

def q1(request):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = "<html><body><p>Alvin, 1111-1111-1111</p><p>%s</p></body></html>" % now
    return HttpResponse(html)

