# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from plagiarism import initial

@csrf_exempt
def check_plagiarism(request):
    if request.method == 'POST':
        text = JSONParser().parse(request)
        result = initial.calculator(text)
        # res = []
        # #convert result numpy array to list
        # for i in range(len(result)):
        #     res.append(result[i])
        
        return JsonResponse(result,safe=False)