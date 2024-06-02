from django.shortcuts import render
from .utils import send_request


def chat_view(request):
    if request.method == "POST":
        message = request.POST.get("message")
        response = send_request(message)
        return render(request, "Gigachat/chat.html", {"response": response})
    return render(request, "Gigachat/chat.html")
