def randomstate(state, seed=42):
    state.m = state.Constant([1,0,1])
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    random_vectors = 2 * torch.rand(*state.m.shape) - 1
    normalized_vectors = random_vectors / (random_vectors.norm(dim=-1, keepdim=True) + 1e-10)  # Add a small value to avoid division by zero
    state.m = normalized_vectors

def relax(state, tf):
    while state.t < tf-eps:
        logger << state
        llg.step(state, 1e-10)

def sweep(Hext, a, vec=[1,0,0],i=3):
    listHsweep = torch.linspace(-a, a, i)
    for H in listHsweep:
        state.t = 0.
        Hext = a/constants.mu_0
        external = ExternalField(Hext*torch.tensor(vec))
        llg = LLGSolver([exchange, torque, aniso, external])
        #randomstate(state)
        state.m = state.Constant([1,0,0])
        state.m.normalize()
        
        while state.t < tf-eps:
            logger << state
            llg.step(state, 1e-10)
        print(f"####################### relaxed for {H} in {len(listHsweep)}")
        
#Failed to use boolean mask for state.material properties
#x1 = x1 * n[0]
#x2 = x2 * n[0]
#y1 = y1 * n[1]
#y2 = y2 * n[1]

#x1 = x1 #* n[0]
#x2 = x2 #* n[0]
#y1 = y1 #* n[1]
#y2 = y2 #* n[1]

#mask_cross = (-x2 < x ) & ( x < x2 ) | ( -y2 < y ) & ( y < y2  ) 
#state.material["Ms"][~mask_cross] = 0
#state.material["Ms"][~mask_cross] = 0 #Makes non-magnetic properties outside the cross arms
#write_vti(state.material, "hallcross.vti") # why expression fails ?
