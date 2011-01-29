from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass
    
    def gadget_info(self):
        return {'name':'gadget3',
                'heading':'This is a test',
                'description':'This is gadget3',
                'class':'gadget color-blue'}

    def view(self,request):
        return render_to_response('dashboard/gadgets/gadget3.html',{})
    
