import numpy as np
from casadi import *
from casadi.tools import *
import pdb
import sys
sys.path.append('../../')
import do_mpc


def bicycle_mpc(model):
    """
    --------------------------------------------------------------------------
    template_mpc: tuning parameters
    --------------------------------------------------------------------------
    """
    mpc = do_mpc.controller.MPC(model)

    setup_mpc = {
        'n_robust': 0,
        'n_horizon': 20,
        't_step': .2,
        'store_full_solution': True,
        # Use MA27 linear solver in ipopt for faster calculations:
        #'nlpsol_opts': {'ipopt.linear_solver': 'MA27'}
    }
    mpc.set_param(**setup_mpc)

    v = model.x['v']
    y = model.x['y']
    psi = model.x['psi']
    v_des = 15 #desired car velocity, [m/s]

    w_vert = 10
    w_vel = 1
    w_psi = 1


    lterm = w_vel*(v-v_des)**2+w_vert*y**2
    mterm = w_vel*(v-v_des)**2+w_vert*y**2
    #lterm = w_vel*(v-v_des)**2+w_vert*y**2+w_psi*psi**2
    #mterm = w_vel*(v-v_des)**2+w_vert*y**2+w_psi*psi**2


    mpc.set_objective(mterm=mterm, lterm=lterm)
    mpc.set_rterm(a=1e-1)
    mpc.set_rterm(phi=10.)


    a = model.u['a']
    phi = model.u['phi']
    mpc.bounds['lower','_u','a'] = -1.25
    mpc.bounds['upper','_u','a'] = 4
    mpc.bounds['lower','_u','phi'] = -np.pi/3
    mpc.bounds['upper','_u','phi'] = np.pi/3

    mpc.setup()

    return mpc
