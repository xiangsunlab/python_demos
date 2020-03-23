import numpy as np
from scipy.integrate import odeint
from bokeh.io import output_notebook, curdoc, show
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models import CustomJS, ColumnDataSource, Slider


# define reaction mechanisms Problem #1
def rate1(var, t):
    A = var[0]
    B = var[1]
    C = var[2]
    D = var[3]
    k1 = var[4]
    km1 = var[5]
    k2 = var[6]
    dAdt = -k1*A*B + km1*C
    dBdt = dAdt
    dCdt = - dAdt - k2*C
    dDdt = k2*C
    #the last 3 variables are rate constants, dk/dt=0
    return [dAdt, dBdt, dCdt, dDdt, 0, 0, 0]


# define reaction mechanisms Problem #2
def rate2(var, t):
    A = var[0]
    B = var[1]
    C = var[2]
    D = var[3]
    k1 = var[4]
    km1 = var[5]
    k2 = var[6]
    dAdt = -k1*A*B + km1*C + k2*C
    dBdt = -k1*A*B + km1*C 
    dCdt = - dBdt - k2*C
    dDdt = k2*C
    #the last 3 variables are rate constants, dk/dt=0
    return [dAdt, dBdt, dCdt, dDdt, 0, 0, 0]



t = np.linspace(0,20,2000)
Conc0 = [1.0, 1.0, 0., 0.]
ks = [20, 15, 2]
var0 = Conc0 + ks
traj = odeint(rate1, var0, t)
#traj = odeint(rate2, var0, t)

source = ColumnDataSource(data={
    'x' : t,
    'ya' : traj[:,0],
    'yb' : traj[:,1],
    'yc' : traj[:,2],
    'yd' : traj[:,3],
})

p = figure(plot_width=700, plot_height=500,tools="pan,reset,save,wheel_zoom",)
p.line('x', 'ya', line_color='red',line_width=3, legend_label="A",source=source)
p.line('x', 'yb', line_color='blue', line_dash=[20,10] ,line_width=3,legend_label="B",source=source)
p.line('x', 'yc', line_color='cyan',line_width=3,legend_label="C",source=source)
p.line('x', 'yd', line_color='orange',line_width=3,legend_label="D",source=source)
p.xaxis.axis_label = "Time (s)"
p.yaxis.axis_label = "Concentration (M)"
p.xaxis.axis_label_text_font_size='16pt'
p.yaxis.axis_label_text_font_size='16pt'
p.yaxis.axis_label_text_font_size='16pt'
p.xaxis.major_label_text_font_size='12pt'
p.yaxis.major_label_text_font_size='12pt'
p.legend.location="center_right"
p.legend.label_text_font_size = "16pt"


# set up sliders
k1 = Slider(title="k1", value=20, start=0.2, end=40.0, step=0.1)
km1 = Slider(title="k-1", value=15, start=0.2, end=40.0, step=0.1)
k2 = Slider(title="k2", value=2, start=0.2, end=20.0, step=0.02)
A0 = Slider(title="[A]0", value=1, start=0.1, end=4.0, step=0.01)
B0 = Slider(title="[B]0", value=1, start=0.1, end=4.0, step=0.01)


# set up callbacks
def update_data(attrname, old, new):

    # Get the current slider values
    a1 = k1.value
    a2 = km1.value
    a3 = k2.value
    ca0 = A0.value
    cb0 = B0.value
    

    # Generate the new curve
    t = np.linspace(0,20,1000)
    Conc0 = [ca0, cb0, 0., 0.]
    ks = [a1, a2, a3]
    var0 = Conc0 + ks
    traj = odeint(rate1, var0, t)
    #traj = odeint(rate2, var0, t)

    source.data = {
    'x' : t,
    'ya' : traj[:,0],
    'yb' : traj[:,1],
    'yc' : traj[:,2],
    'yd' : traj[:,3],
    }
    
# update plot whenever changes on sliders
for w in [k1,km1,k2,A0,B0]:
    w.on_change('value', update_data)
    

# Set up layouts and add to document
inputs = column(k1,km1,k2,A0,B0)
curdoc().add_root(row(inputs, p))



