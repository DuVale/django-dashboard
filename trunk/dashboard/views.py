from django.shortcuts import render_to_response, get_object_or_404
from djangodashboard.dashboard.gadgets import find_gadgets, open_gadget
from django.http import HttpResponse, HttpResponseRedirect
import models
import xml.dom.minidom as minidom
from xml_utils import children
from django.template.loader import render_to_string

#------------------------------------------------------------------------------

def dashboard(request, name):
    try:
        dashboard = models.Dashboard.objects.get(name=name,user=request.user)
    except models.Dashboard.DoesNotExist:
        dashboard = models.Dashboard(name=name,user=request.user,layout='three')
        dashboard.save()
    dashboard_data = {}
    column_data = []
    
    dashboard_items = models.DashboardItem.objects.filter(dashboard=dashboard).order_by('column_number','position')
    
    column_number=0
    
    for gadget in dashboard_items:
        if gadget.column_number != column_number and column_number != 0:
            dashboard_data[column_number] = column_data
            column_data = []
        column_number = gadget.column_number
        column_data.append(render_to_string('dashboard/gadget.html', { 'gadget': gadget }))
    if len(dashboard_items)>0:
        dashboard_data[column_number] = column_data

    return render_to_response('dashboard/layouts/%s.html' %(dashboard.layout), 
            { 'name':name, 'dashboard_data':dashboard_data,'dashboard_items':dashboard_items})

#------------------------------------------------------------------------------

def update_ajax(request,name):
    try:
        dashboard = models.Dashboard.objects.get(name=name,user=request.user)
    except models.Dashboard.DoesNotExist:
        dashboard = models.Dashboard(name=name,user=request.user)
    models.DashboardItem.objects.filter(dashboard=dashboard).update(active=False)
    if request.method == 'POST':
        dom = minidom.parseString(request.POST["xml"])
        parent = children(dom, 'xml')[0]
        column_nodes = children(parent, 'column')
        column_number=1
        for column_node in column_nodes:
            position=1
            gadget_nodes = children(column_node, 'gadget')
            for gadget_node in gadget_nodes:
                dashboard_item = models.DashboardItem.objects.get(uuid=gadget_node.getAttribute('id'))
                dashboard_item.active = True
                dashboard_item.column_number = column_number
                dashboard_item.position = position
                dashboard_item.title = gadget_node.getAttribute('title')
                dashboard_item.colour = gadget_node.getAttribute('colour')
                if gadget_node.getAttribute('collapsed') == 'false':
                    dashboard_item.collapsed = False
                else:
                    dashboard_item.collapsed = True
                if len(gadget_node.childNodes) > 0:
                    mods = '<xml>'
                    for gn in gadget_node.childNodes:
                        mods += gn.toxml()
                    mods += '</xml>'
                    dashboard_item.modifier = mods
                dashboard_item.save()
                position = position+1
            column_number = column_number+1
        models.DashboardItem.objects.filter(dashboard=dashboard,active=False).delete()
    return HttpResponse("<xml>Done</xml>")

#------------------------------------------------------------------------------

def gadget(request,uuid):
    dashboard_item = get_object_or_404(models.DashboardItem,uuid=uuid)
    w = open_gadget(dashboard_item.gadget)
    return (w.view(request,dashboard_item))

#------------------------------------------------------------------------------

def view_gadgets(request,name):
    return render_to_response('dashboard/view_gadgets.html', 
            {'name':name,'gadgets':find_gadgets()})

#------------------------------------------------------------------------------

def add_gadget(request,name,gadget):
    try:
        dashboard = models.Dashboard.objects.get(name=name,user=request.user)
    except models.Dashboard.DoesNotExist:
        dashboard = models.Dashboard(name=name,user=request.user)
    dashboard_item = models.DashboardItem(dashboard=dashboard)
    dashboard_item.active = True
    dashboard_item.collapsed = False
    dashboard_item.position = 100
    dashboard_item.column_number = 1
    dashboard_item.gadget = gadget
    dashboard_item.title = open_gadget(gadget).gadget_info()['title']
    dashboard_item.save()
    url = "/dashboard/%s/" %(name)
    return HttpResponseRedirect(url)

#------------------------------------------------------------------------------