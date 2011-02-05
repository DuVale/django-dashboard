import os


#--------------------------------------------------------------------------------------------

def find_gadgets():
    gadget_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        if True:
            fileDict = [f[:-3] for f in os.listdir(gadget_dir)
                    if not f.startswith('_') and f.endswith('.py')]
        else:
            fileDict = [f[:-4] for f in os.listdir(gadget_dir)
                    if not f.startswith('_') and f.endswith('.pyc')]
    except OSError:
        return []
    gadgetArray=[]
    for file in fileDict:
        gadgetArray.append(open_gadget(file).gadget_info())
    return gadgetArray

#--------------------------------------------------------------------------------------------

def open_gadget(gadget):
    g = __import__("djangodashboard.dashboard.gadgets." + gadget, globals(), locals(), ["Gadget"])
    return g.Gadget()
