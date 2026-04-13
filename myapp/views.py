from django.shortcuts import render
from .ai_logic import run_ai

def home(request):
    result = None

    if request.method == "POST":
        question = request.POST.get("question")
        result = run_ai(question)

    return render(request, "index.html", {"result": result})