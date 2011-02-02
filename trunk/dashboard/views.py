from django.shortcuts import render_to_response
from djangodashboard.dashboard.gadgets import find_gadgets, open_gadget
from django.http import HttpResponse, HttpResponseRedirect
import models
import xml.dom.minidom as minidom
from xml_utils import children

#------------------------------------------------------------------------------

def dashboard(request, name):
    try:
        dashboard = models.Dashboard.objects.get(name=name,user=request.user)
    except models.Dashboard.DoesNotExist:
        dashboard = models.Dashboard(name=name,user=request.user)
        dashboard.save()
    
    dashboard_data = []
    
    column_data = {}
    column_data['gadgets'] = models.GadgetInfomation.objects.filter(dashboard=dashboard,column_number=1).order_by('position')
    column_data['column'] = 1
    dashboard_data.append(column_data)
    column_data = {}
    column_data['gadgets'] = models.GadgetInfomation.objects.filter(dashboard=dashboard,column_number=2).order_by('position')
    column_data['column'] = 2
    dashboard_data.append(column_data)
    column_data = {}
    column_data['gadgets'] = models.GadgetInfomation.objects.filter(dashboard=dashboard,column_number=3).order_by('position')
    column_data['column'] = 3
    dashboard_data.append(column_data)
    return render_to_response('dashboard/dashboard.html', 
            { 'name':name, 'dashboard_data':dashboard_data})

#------------------------------------------------------------------------------

def update_ajax(request,name):
    try:
        dashboard = models.Dashboard.objects.get(name=name,user=request.user)
    except models.Dashboard.DoesNotExist:
        dashboard = models.Dashboard(name=name,user=request.user)
    models.GadgetInfomation.objects.filter(dashboard=dashboard).update(active=False)
    if request.method == 'POST':
        dom = minidom.parseString(request.POST["xml"])
        parent = children(dom, 'xml')[0]
        column_nodes = children(parent, 'column')
        column_number=1
        for column_node in column_nodes:
            position=1
            gadget_nodes = children(column_node, 'gadget')
            for gadget_node in gadget_nodes:
                gadget_information = models.GadgetInfomation.objects.get(uuid=gadget_node.getAttribute('id'))
                gadget_information.active = True
                gadget_information.column_number = column_number
                gadget_information.position = position
                gadget_information.title = gadget_node.getAttribute('title')
                gadget_information.colour = gadget_node.getAttribute('colour')
                if gadget_node.getAttribute('collapsed') == 'false':
                    gadget_information.collapsed = False
                else:
                    gadget_information.collapsed = True
                gadget_information.save()
                position = position+1
            column_number = column_number+1
        models.GadgetInfomation.objects.filter(dashboard=dashboard,active=False).delete()
    return HttpResponse("<xml>Done</xml>")

#------------------------------------------------------------------------------

def gadget(request,name):
    w = open_gadget(name)
    return (w.view(request))

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
    gadget_information = models.GadgetInfomation(dashboard=dashboard)
    gadget_information.active = True
    gadget_information.collapsed = False
    gadget_information.position = 100
    gadget_information.column_number = 1
    gadget_information.gadget = gadget
    gadget_information.title = open_gadget(gadget).gadget_info()['title']
    gadget_information.save()
    url = "/dashboard/%s/" %(name)
    return HttpResponseRedirect(url)