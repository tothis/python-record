from django.shortcuts import render


def index(request):
    # a = request.GET['a']
    # b = request.GET['b']
    # c = int(a) + int(b)
    # return HttpResponse(str(c))
    return render(request, 'index.html')
