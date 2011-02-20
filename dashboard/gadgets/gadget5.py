from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass
    
    def gadget_info(self):
        fields = []
        return {'name':'gadget5',
                'title':'This is a gadget5',
                'description':'This is gadget5',
                'colour':'color-orange',
                'icon':'/media/img/circle.png',
                'fields':fields}


    def view(self,request,gadget_information):
        return render_to_response('dashboard/gadgets/gadget5.html',{})