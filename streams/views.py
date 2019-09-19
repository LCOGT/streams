from django.http import HttpResponse

def view_healthz(request):
    return HttpResponse('Healthy!', content_type='text/plain', status=200)
