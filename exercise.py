from rlrs.dp import q_value, value_iteration
from rlrs.envs import ACTION_NAMES, GridWorld

env = GridWorld()
valores, politica, barridos = value_iteration(env, gamma=0.9)

for a in range(env.n_actions):
    print(f'{ACTION_NAMES[a]:<10} {q_value(env, valores, (0.3), a, 0.9):+.6f}')