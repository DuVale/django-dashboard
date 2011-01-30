from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass
    
    def gadget_info(self):
        return {'name':'gadget2',
                'title':'This is a gadget2',
                'description':'This is gadget2',
                'colour':'color-red'}

    def view(self,request):
        return render_to_response('dashboard/gadgets/gadget2.html',{})
    
