from django.shortcuts import render

def about_view(request):
    team = [
        {"name": "Іван", "role": "Backend Developer"},
        {"name": "Діма", "role": "Frontend Developer"},
    ]
    return render(request, "techblog/about.html", {"team": team})

def contact_view(request):
    return render(request, "contact.html")