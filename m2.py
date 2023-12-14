from magnumnp import *
from myfunctions import *
import os, sys

Timer.enable()
random = False
set_log_level(30)
torch.manual_seed(42)
torch.cuda.manual_seed_all(42)

#Variables
filepath = sys.argv[0]

#Defining the geometry
L = 10e-6 # 10e-6 #length_cross 
arm_width = 2e-6 # 2e-6

#Helper coordinates
x1 = L/2.
x2 = arm_width/2.
y1 = x1
y2 = x2

#Mesh definitions
dx = (10e-9, 10e-9, 1e-9)
#dx = (1e-9, 1e-9, 1e-9)
#n = (1,1,1) 
n = (round(L/dx[0]), round(L/dx[1]), round(1e-9/dx[2]))
#origin=(0,0,0) 
origin = (-x1, -y1, 0)

#origin = (-x1*n[0]/2, -y1*n[1]/2, 0)

tf = 10e-9
eps = 1e-15
mesh = Mesh(n,dx, origin)
state = State(mesh, dtype = torch.float32)
x, y, z = state.SpatialCoordinate()

#Parameters
p = state.Tensor((0, -1, 0))
je = 1.68e11 #6.9e11
d = n[2] * dx[2]
Js = 1.2
K1 = (0.0049/constants.mu_0)/2*Js + 0.5*(Js**2)/constants.mu_0 #+ 0.5*constants.mu_0*(Js/constants.mu_0)**2 # Shape Anis.
hampl = float(sys.argv[1]) if len(sys.argv) > 1 else 0 # to 10 mT #In militesla
Ms = Js/constants.mu_0 #1200e3 #equiv 1.503 T
A0 = 20e-12#Joule/meter
J0 = 1.5#Tesla
Aex_T = A0*(Js/J0)**1.7 
A = Aex_T

state.material = {
    #"Ms": Js/constants.mu_0,
    "Ms":  0,                        #0, #equiv 1.503 T
    "A": 0,
    "Ku": K1,               
    "Ku_axis": [0, 0, 1],
    "gamma": 2.211e5,
    "alpha": 1,
    "eta_field": 0.044,
    "eta_damp": 0.044*1.22,        # both eta with opposite sign as magnum.af, same as magnum.pi
    "p": state.Tensor((0, 0, 0)), #0, 0)), #No current in all structure, just horizontal stripe
    "d": d,
    "je": je}

mi = state.Tensor([0,1,0])
state.m = state.Constant([1,0,0])

#Cross shape (why does it fail in my other trial?)
#vertical stripe
xi = round(n[0]*4/10)
xf = round(n[0]*6/10)
state.material["Ms"][xi:xf,:,:,:] = Ms 
state.material["A"][xi:xf,:,:,:] = A
state.m[xi:xf,:,:,:] = torch.randn(state.m[xi:xf,:,:,:].shape) if random == True else mi

#horizontal stripe
yi = round(n[1]*4/10)
yf = round(n[1]*6/10)
state.material["Ms"][:,yi:yf,:,:] = Ms 
state.material["p"][:,yi:yf,:,:] = p
state.material["A"][:,yi:yf,:,:] = A
state.m[:,yi:yf,:,:] = torch.randn(state.m[:,yi:yf,:,:].shape) if random == True else mi

state.m.normalize()

exchange = ExchangeField()
aniso = UniaxialAnisotropyField()
torque = SpinOrbitTorque()
demag = DemagField()

Hx = 0.001*hampl/constants.mu_0
external = ExternalField([Hx, 0, 0])
state.t = 0.
llg = LLGSolver([demag, exchange, torque, aniso, external])
#logger = Logger(f"data_H{int(hampl):04d}", ['t', 'm', torque.h, aniso.h])
logger = Logger(f"data_H{int(hampl):04d}", scalars=['t','m',torque.h, external.h],
                fields_every=500, scalars_every=1,
                fields=['m',torque.h, external.h])
write_vti(state.material, "cell.vti") 

if logger.is_resumable():
    print("\t \n \t Logger data files found! ")
    logger.resume(state)
    default_increase=3e-9
    print("\t \t last @ ", state.t.item(), "\t adding...", default_increase)
    tf+= 1e-9*float(sys.argv[2]) if len(sys.argv) > 2 else default_increase
    print("\t\t\tt_f:", tf)
else:
    print("nothing found")
    minimizer = MinimizerBB([demag, exchange, aniso])
    minimizer.minimize(state)


cnt = 1
name_minimized = f"data_H{int(hampl):04d}/m_relax_H{int(hampl):04d}_{0}.vti"
name_rxstep = f"data_H{int(hampl):04d}/m_relax_H{int(hampl):04d}_{cnt}.vti"
name_relaxed = f"data_H{int(hampl):04d}/m_relaxed.vti" 
write_vti(state.m, name_minimized, state) 

try: 
    while state.t < tf-eps:
        logger << state
        m_formatted = [f"{x:1.3e}" for x in state.m.average().tolist()]
        print("m: ", m_formatted,"\t t: ", f"{state.t.item():1.2e} /{tf:1.2e}", "\t Hext mT: ", hampl)
        if int(cnt%25) == int(0):
            write_vti(state.m, name_rxstep, state) #llg.accumulated_steps )
        llg.step(state, 1e-12)
        cnt+=1
        
except KeyboardInterrupt:
    print("\033[91m### Extiting job... ###")
write_vti(state.m, name_relaxed, state)
Timer.print_report()

    
