from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass
    
    def gadget_info(self):
        return {'name':'gadget4',
                'heading':'This is a test',
                'description':'This is gadget4',
                'class':'gadget color-yellow'}

    def view(self,request):
        return render_to_response('dashboard/gadgets/gadget4.html',{})

