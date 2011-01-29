from django.shortcuts import render_to_response

class Gadget:

    def __init__(self):
        pass

    def gadget_info(self):
        return {'name':'gadget1',
                'heading':'This is a test',
                'description':'This is gadget1',
                'class':'gadget color-green'}

    def view(self,request):
        return render_to_response('dashboard/gadgets/gadget1.html',{})


