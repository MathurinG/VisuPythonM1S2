import matplotlib
import bokeh


print("-----------------------------------------------")
#version de Matplotlib recommandée :
vplot = "3.8.2"
print("Version actuelle de matplotlib : ",matplotlib.__version__)
if matplotlib.__version__ != vplot :
    print("Attention, il est recommandé d'utiliser la version {} de Matplotlib.".format(vplot))
    print("Nous vous conseillons de mettre à jour l'installation depuis Anaconda Prompt avec :")
    print("\t \tpip install matplotlib --upgrade")
    print("ou")
    print("\t \tpip install matplotlib=={}".format(vplot))
else :
    print("Vous utilisez bien la version préconisée pour Matplotlib.")
print("-----------------------------------------------")


#version de Bokeh recommandée :
vbokeh = "3.3.3"
print("Version actuelle de Bokeh : ",bokeh.__version__)
if bokeh.__version__ != vbokeh :
    print("Attention, il est recommandé d'utiliser la version {} de bokeh.".format(vbokeh))
    print("Nous vous conseillons de mettre à jour l'installation depuis Anaconda Prompt avec :")
    print("\t \tpip install bokeh --upgrade")
    print("ou")
    print("\t \tpip install bokeh=={}".format(vbokeh))
else :
    print("Vous utilisez bien la version préconisée pour Bokeh.")
print("-----------------------------------------------")

