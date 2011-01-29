from django.shortcuts import render_to_response
from djangodashboard.dashboard.gadgets import find_gadgets, open_gadget
from django.http import HttpResponse
import models
import xml.dom.minidom as minidom

#------------------------------------------------------------------------------

def children(dom, name):
    children = []
    for node in dom.childNodes:
        if node.localName == name:
            children.append(node)
    return children

#------------------------------------------------------------------------------

def read_xml(xml):
    dom = minidom.parseString(xml)
    parent = children(dom, 'xml')[0]
    column_nodes = children(parent, 'column')
    dashboard_data = {}
    for column_node in column_nodes:
        column_data = []
        gadget_nodes = children(column_node, 'gadget')
        for gadget_node in gadget_nodes:
            gadget_data = {}
            gadget_data['id'] = gadget_node.getAttribute('id')
            gadget_data['colour'] = gadget_node.getAttribute('colour')
            gadget_data['title'] = gadget_node.getAttribute('title')
            gadget_data['collapsed'] = gadget_node.getAttribute('collapsed')
            try:
                gadget_data['class'] = open_gadget(gadget_data['id']).gadget_info()['class']
            except:
                continue
            column_data.append(gadget_data)
        dashboard_data[column_node.getAttribute('id')] = column_data
    return dashboard_data

#------------------------------------------------------------------------------

def dashboard(request, name):
    try:
        dashboard = models.Dashboard.objects.get(name=name,user=request.user)
        gadgets = read_xml(dashboard.xml)
    except models.Dashboard.DoesNotExist:
        gadgets = {'1':[],'2':[],'3':[]}
    return render_to_response('dashboard/dashboard.html', 
        { 'name':name, 'gadgets':gadgets })

#------------------------------------------------------------------------------

def update_ajax(request,name):
    try:
        dashboard = models.Dashboard.objects.get(name=name,user=request.user)
    except models.Dashboard.DoesNotExist:
        dashboard = models.Dashboard(name=name,user=request.user)

    if request.method == 'POST':
        dashboard.xml = request.POST["xml"]
        dashboard.save()
    return HttpResponse("<xml>Done</xml>")

#------------------------------------------------------------------------------

def gadget(request,name):
    w = open_gadget(name)
    return (w.view(request))

#------------------------------------------------------------------------------

def view_gadgets(request):
    return render_to_response('dashboard/view_gadgets.html', {'gadgets':find_gadgets()})

#------------------------------------------------------------------------------
