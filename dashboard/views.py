from django.shortcuts import render_to_response
from djangodashboard.dashboard.widgets import find_widgets, open_widget
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
        widget_nodes = children(column_node, 'widget')
        for widget_node in widget_nodes:
            widget_data = {}
            widget_data['id'] = widget_node.getAttribute('id')
            widget_data['colour'] = widget_node.getAttribute('colour')
            widget_data['title'] = widget_node.getAttribute('title')
            widget_data['collapsed'] = widget_node.getAttribute('collapsed')
            try:
                widget_data['class'] = open_widget(widget_data['id']).widget_info()['class']
            except:
                continue
            column_data.append(widget_data)
        dashboard_data[column_node.getAttribute('id')] = column_data
    return dashboard_data

#------------------------------------------------------------------------------

def dashboard(request, name):
    try:
        dashboard = models.Dashboard.objects.get(name=name,user=request.user)
        widgets = read_xml(dashboard.xml)
    except models.Dashboard.DoesNotExist:
        widgets = {'1':[],'2':[],'3':[]}
    return render_to_response('dashboard/dashboard.html', 
        { 'name':name, 'widgets':widgets })

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

def widget(request,name):
    w = open_widget(name)
    return (w.view(request))
    assert False, "Error"

#------------------------------------------------------------------------------

def view_widgets(request):
    return render_to_response('dashboard/view_widgets.html', {'widgets':find_widgets()})

#------------------------------------------------------------------------------
