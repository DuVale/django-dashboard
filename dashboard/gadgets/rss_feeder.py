from django.shortcuts import render_to_response
import feedparser



class Gadget:

    def __init__(self):
        pass

    def gadget_info(self):
        fields = [{'title':'RSS URL','id':'url','type':'text','value':''},
                  {'title':'Number of results','id':'nor','type':'text','value':'10'}
        ]
        return {'name':'rss_feeder',
                'title':'RSS Reader',
                'description':'RSS Reader',
                'colour':'color-blue',
                'icon':'/media/img/rss.png',
                'fields':fields}


    def view(self,request,gadget_information):
        options = gadget_information.get_extra_fields()
        if options['url'] == "":
            assert False, "No URL"
        rss_results = feedparser.parse(options['url'])['items'][:int(options['nor'])]
        
        return render_to_response('dashboard/gadgets/rss.html',{'rss_results':rss_results})

