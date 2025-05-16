from django.shortcuts import render
from django.http import HttpResponse
from .gemini_api import get_sql_query_from_nl
# Create your views here.

def home(request):
    return render(request, "home.html", {})
def generateSQL(request):

    if request.method=='POST':
        query = request.POST.get('query')

        return render(request, 'llm_response.html', {"response": get_sql_query_from_nl(query)})