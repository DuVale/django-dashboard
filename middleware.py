from django.contrib.auth.views import login
from django.http import HttpResponseRedirect

class SiteLogin:
    "This middleware requires a login for every view"
    def process_request(self, request):
        if request.path == '/accounts/login/':
            return
        
        if not request.user.is_anonymous():
            return

        # list of anonymous-ok url starts 
        urlStarts = []
        urlStarts.append('/media/homepage/')
        
        for urlStart in urlStarts:
            if request.path.startswith(urlStart):
                return
        
        if request.POST:
            return login(request)
        else:
            return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
        