from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass
    
    def gadget_info(self):
        return {'name':'gadget2',
                'heading':'This is a test',
                'description':'This is gadget2',
                'class':'gadget color-red'}

    def view(self,request):
        return render_to_response('dashboard/gadgets/gadget2.html',{})
    
