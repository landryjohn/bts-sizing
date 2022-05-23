from django.http import HttpResponse

# Vue index
def index(req):
    return HttpResponse(content='BTS Sizing')