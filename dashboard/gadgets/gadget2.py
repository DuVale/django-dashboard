from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass
    
    def gadget_info(self):
        fields = [{'title':'This is a test field','id':'test','type':'text','value':'test'},
                  {'title':'This is a test field2','id':'test2','type':'choice','choices':['UK','USA'],'value':'UK'}]
        return {'name':'gadget2',
                'title':'This is a gadget2',
                'description':'This is gadget2',
                'colour':'color-red',
                'fields':fields}


    def view(self,request):
        return render_to_response('dashboard/gadgets/gadget2.html',{})
    
