import os


#--------------------------------------------------------------------------------------------

def find_widgets():
    widget_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        if True:
            fileDict = [f[:-3] for f in os.listdir(widget_dir)
                    if not f.startswith('_') and f.endswith('.py')]
        else:
            fileDict = [f[:-4] for f in os.listdir(widget_dir)
                    if not f.startswith('_') and f.endswith('.pyc')]
    except OSError:
        return []
    
    widgetArray=[]
    for file in fileDict:
        widgetArray.append(open_widget(file).widget_info())

    return widgetArray
        

#--------------------------------------------------------------------------------------------

def open_widget(widget):
    w = __import__("mysite.dashboard.widgets." + widget, globals(), locals(), ["Widgets"])
    return w.Widgets()
