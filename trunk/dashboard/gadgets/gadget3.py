from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass
    
    def gadget_info(self):
        return {'name':'gadget3',
                'title':'This is a gadget3',
                'description':'This is gadget3',
                'colour':'color-blue'}

    def view(self,request):
        return render_to_response('dashboard/gadgets/gadget3.html',{})
    
