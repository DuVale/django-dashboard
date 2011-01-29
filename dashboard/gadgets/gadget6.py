from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass
    
    def gadget_info(self):
        return {'name':'gadget6',
                'heading':'This is a test',
                'description':'This is gadget6',
                'class':'gadget color-white'}

    def view(self,request):
        return render_to_response('dashboard/gadgets/gadget6.html',{})
    
