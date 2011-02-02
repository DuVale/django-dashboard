from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass

    def gadget_info(self):
        fields = [{'title':'This is a test field','id':'test','type':'text','value':''}]
        return {'name':'gadget1',
                'title':'This is a gadget1',
                'description':'This is gadget1',
                'colour':'color-green',
                'fields':fields}


    def view(self,request):
        return render_to_response('dashboard/gadgets/gadget1.html',{})

