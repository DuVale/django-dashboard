from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass
    
    def gadget_info(self):
        return {'name':'gadget6',
                'title':'This is a gadget6',
                'description':'This is gadget6',
                'colour':'color-white'}

    def view(self,request):
        return render_to_response('dashboard/gadgets/gadget6.html',{})
    
