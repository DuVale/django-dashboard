from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass
    
    def gadget_info(self):
        fields = []
        return {'name':'gadget3',
                'title':'This is a gadget3',
                'description':'This is gadget3',
                'colour':'color-blue',
                'icon':'/media/img/circle.png',
                'fields':fields}


    def view(self,request,gadget_information):
        return render_to_response('dashboard/gadgets/gadget3.html',{})
