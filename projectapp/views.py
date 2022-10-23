from django.shortcuts import render

# Create your views here.
def register_decision(request):
    return render(request, 'commontemplates/usertypesignup.html')