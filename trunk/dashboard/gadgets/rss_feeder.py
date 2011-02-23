from django.shortcuts import render_to_response, HttpResponse
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


    def view(self,request,dashboard_item):
        options = dashboard_item.get_extra_fields()
        if options['url'] == "":
            HttpResponse("<html><body>No URL</body></html>")
        rss_results = feedparser.parse(options['url'])['items'][:int(options['nor'])]
        
        return render_to_response('dashboard/gadgets/rss.html',{'rss_results':rss_results})

