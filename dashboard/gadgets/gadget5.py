from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass
    
    def gadget_info(self):
        return {'name':'gadget5',
                'heading':'This is a test',
                'description':'This is gadget5',
                'class':'gadget color-orange'}

    def view(self,request):
        return render_to_response('dashboard/gadgets/gadget5.html',{})
    
