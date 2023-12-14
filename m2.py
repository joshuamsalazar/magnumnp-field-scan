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

tf = 6e-9
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
K1 *= 1.1
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
mi2 = state.Tensor([0,0,0])
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
state.m[:,yi:yf,:,:] = torch.randn(state.m[:,yi:yf,:,:].shape) if random == True else mi2

# Calculate the average magnetization for the horizontal stripe
horizontal_stripe_magnetization = state.m[:, yi:yf, :, :]
average_magnetization_horizontal = torch.mean(horizontal_stripe_magnetization, dim=[0, 1, 2])

# Calculate the average magnetization for the vertical stripe
vertical_stripe_magnetization = state.m[xi:xf, :, :, :]
average_magnetization_vertical = torch.mean(vertical_stripe_magnetization, dim=[0, 1, 2])

# Extract the components as individual numbers
average_horizontal_x, average_horizontal_y, average_horizontal_z = average_magnetization_horizontal.tolist()
average_vertical_x, average_vertical_y, average_vertical_z = average_magnetization_vertical.tolist()

# Isolating the overlapping region
overlap_region_magnetization = state.m[xi:xf, yi:yf, :, :]
average_magnetization_overlap = torch.mean(overlap_region_magnetization, dim=[0, 1, 2, 3])

# Creating a mask for the union of the horizontal and vertical stripes
# Adjust the shape of the mask to match the shape of state.m, excluding the last component dimension
union_mask = torch.zeros(state.m.shape[:-1], dtype=torch.bool)
union_mask[xi:xf, :, :] = True  # Covering the vertical stripe
union_mask[:, yi:yf, :] = True  # Covering the horizontal stripe

# Selecting the magnetization for the union
union_magnetization = state.m[union_mask]

# Calculating the average magnetization for the union
average_magnetization_union = torch.mean(union_magnetization)

# Print the result
print("Average Magnetization in the UNION of Stripes:", average_magnetization_union.item())

print("Average Magnetization in INTERSECT Region:", average_magnetization_overlap.tolist())
print("Average Magnetization in XX Stripe (x, y, z):", average_horizontal_x, average_horizontal_y, average_horizontal_z)
print("Average Magnetization in YY Stripe (x, y, z):", average_vertical_x, average_vertical_y, average_vertical_z)
print("Structure average:", [f"{x:1.3e}" for x in state.m.average().tolist()])

state.m.normalize()

exchange = ExchangeField()
aniso = UniaxialAnisotropyField()
torque = SpinOrbitTorque()
demag = DemagField()

Hx = 0.001*hampl/constants.mu_0
external = ExternalField([Hx, 0, 0])
state.t = 0.
llg = LLGSolver([demag, exchange, torque, aniso, external])
logger = Logger(f"data_H{int(hampl):04d}", scalars=['t','m',torque.h, external.h],
                fields_every=500, scalars_every=1,
                fields=['m',torque.h, external.h])

if logger.is_resumable():
    print("\t \n \t Logger data files found! ")
    logger.resume(state)
    default_increase=3e-9
    print("\t \t last @ ", state.t.item(), "\t adding...", default_increase)
    tf+= 1e-9*float(sys.argv[2]) if len(sys.argv) > 2 else default_increase
    print("\t\t\tt_f:", tf)
else:
    print(" \t\n\t\n...nothing found")
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
            write_vti(state.m, name_rxstep, state) 
        llg.step(state, 1e-12)
        cnt+=1
        
except KeyboardInterrupt:
    print("\033[91m### Extiting job... ###")
write_vti(state.m, name_relaxed, state)
Timer.print_report()

    
