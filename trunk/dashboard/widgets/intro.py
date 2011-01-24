from django.shortcuts import render_to_response

class Widgets:

    def __init__(self):
        pass

    def widget_info(self):
        return {'name':'intro',
                'heading':'This is a test',
                'description':'This is sample widget',
                'class':'widget color-green'}

    def view(self,request):
        return render_to_response('dashboard/widgets/intro.html',{})


