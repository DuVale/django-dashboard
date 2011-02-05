from django.shortcuts import render_to_response, get_object_or_404

class Gadget:

    def __init__(self):
        pass
    
    def gadget_info(self):
        fields = [{'title':'This is a test field','id':'test','type':'text','value':'test'},
                  {'title':'List of countries','id':'test2','type':'choice',
                                    'choices':[('0','UK'),('1','USA'),('2','France'),('3','Italy')],'value':'UK'}]
        return {'name':'gadget2',
                'title':'This is a gadget2',
                'description':'This is gadget2',
                'colour':'color-red',
                'fields':fields}


    def view(self,request,gadget_information):
        options = gadget_information.get_extra_fields()
        return render_to_response('dashboard/gadgets/gadget2.html',{'options':options})
