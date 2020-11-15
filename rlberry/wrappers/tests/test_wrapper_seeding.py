import numpy as np 
import pytest
import rlberry.seeding as seeding
import rlberry.spaces as spaces

from copy import deepcopy
from rlberry.envs.classic_control import MountainCar, Acrobot
from rlberry.envs.finite import Chain
from rlberry.envs.finite import GridWorld
from rlberry.envs.toy_exploration import PBall2D
from rlberry.envs.toy_exploration import SimplePBallND
from rlberry.wrappers import Wrapper, RescaleRewardWrapper

classes = [
    MountainCar,
    GridWorld,
    Chain,
    PBall2D,
    SimplePBallND,
    Acrobot
]


def get_env_trajectory(env, horizon):
    states = []
    ss = env.reset()
    for ii in range(horizon):
        states.append(ss)
        ss, _, _, _ = env.step(env.action_space.sample())
    return states

def compare_trajectories(traj1, traj2):
    for ss1, ss2 in zip(traj1, traj2):
        if not np.array_equal(ss1, ss2):
            return False 
    return True

@pytest.mark.parametrize("ModelClass", classes)
def test_wrapper_seeding(ModelClass):
    
    seeding.set_global_seed(123)
    env1 = Wrapper(ModelClass())

    seeding.set_global_seed(456)
    env2 = Wrapper(ModelClass())

    seeding.set_global_seed(123)
    env3 = Wrapper(ModelClass())

    if deepcopy(env1).is_online():
        traj1 = get_env_trajectory(env1, 500)
        traj2 = get_env_trajectory(env2, 500)
        traj3 = get_env_trajectory(env3, 500)

        assert not compare_trajectories(traj1, traj2)
        assert compare_trajectories(traj1, traj3)


@pytest.mark.parametrize("ModelClass", classes)
def test_rescale_wrapper_seeding(ModelClass):
    
    seeding.set_global_seed(123)
    env1 = RescaleRewardWrapper(ModelClass(), (0,1))

    seeding.set_global_seed(456)
    env2 = RescaleRewardWrapper(ModelClass(), (0,1))

    seeding.set_global_seed(123)
    env3 = RescaleRewardWrapper(ModelClass(), (0,1))

    if deepcopy(env1).is_online():
        traj1 = get_env_trajectory(env1, 500)
        traj2 = get_env_trajectory(env2, 500)
        traj3 = get_env_trajectory(env3, 500)

        assert not compare_trajectories(traj1, traj2)
        assert compare_trajectories(traj1, traj3)


@pytest.mark.parametrize("ModelClass", classes)
def test_wrapper_copy_reseeding(ModelClass):
    
    seeding.set_global_seed(123)
    env = Wrapper(ModelClass())

    c_env = deepcopy(env)
    c_env.reseed()

    if deepcopy(env).is_online():
        traj1 = get_env_trajectory(env, 500)
        traj2 = get_env_trajectory(c_env, 500)
        assert not compare_trajectories(traj1, traj2)