from django.shortcuts import render
def handle_404(request,exception):
     return render(request, 'customer/guest.html', status=404)
