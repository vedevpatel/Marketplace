import numpy as np
import gymnasium as gym
from gymnasium import spaces

import pettingzoo
from pettingzoo.utils import parallel_to_aec, wrappers as pz_wrappers

from supersuit import pettingzoo_env_to_vec_env_v1, concat_vec_envs_v1

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecMonitor
from stable_baselines3.common.callbacks import CheckpointCallback

# Your simulation classes
from simulation import generate_agents, Marketplace


# 1) PettingZoo Environment
class MarketplaceEnv(pettingzoo.ParallelEnv):
    metadata = {"render_modes": ["human"], "name": "marketplace-v0"}

    def __init__(self, num_buyers: int, num_sellers: int):
        super().__init__()
        self.num_buyers = num_buyers
        self.num_sellers = num_sellers
        self.render_mode = "human"

        # Agent identifiers
        self.agents = [f"seller_{i}" for i in range(self.num_sellers)]
        self.possible_agents = self.agents[:]

    # Define spaces as methods, not attributes in __init__
    def observation_space(self, agent):
        # State: [normalized_inventory, normalized_price]
        return spaces.Box(low=0.0, high=np.inf, shape=(2,), dtype=np.float32)

    def action_space(self, agent):
        # 5 actions: price change of -10%, -5%, 0, +5%, +10%
        return spaces.Discrete(5)

    def reset(self, seed=None, options=None):
        self.buyers, self.sellers = generate_agents(self.num_buyers, self.num_sellers)
        self.market = Marketplace(self.buyers, self.sellers)
        self.current_step = 0
        self.agents = [f"seller_{i}" for i in range(self.num_sellers)]

        observations = {
            f"seller_{i}": self.sellers[i].get_state(self.market.average_price)
            for i in range(self.num_sellers)
        }
        return observations, {}

    def step(self, actions):
        for i, agent_name in enumerate(self.agents):
            action = int(actions[agent_name])
            seller = self.sellers[i]
            price_change_percent = seller.actions[action]
            seller.current_price *= (1 + price_change_percent)
            seller.current_price = max(seller.current_price, seller.min_price_per_unit)
            seller.last_tick_sales = 0

        self.market.run_tick()

        rewards = {}
        observations = {}
        for i, agent_name in enumerate(self.agents):
            seller = self.sellers[i]
            rewards[agent_name] = float(seller.last_tick_sales * seller.current_price)
            observations[agent_name] = seller.get_state(self.market.average_price)

        self.current_step += 1
        terminations = {agent: self.current_step >= 1000 for agent in self.agents}
        truncations = {agent: False for agent in self.agents}
        
        # Create an info dict with a key for each agent (can be empty)
        infos = {agent: {} for agent in self.agents}

        return observations, rewards, terminations, truncations, infos # Return the new infos dict

    def render(self):
        pass


# 2) Training with SB3 PPO
if __name__ == "__main__":
    print("Creating PettingZoo ParallelEnv...")
    parallel_env = MarketplaceEnv(num_buyers=100, num_sellers=10)
    
    print("Converting PettingZoo env to SB3 VecEnv via SuperSuit...")
    vec_env = pettingzoo_env_to_vec_env_v1(parallel_env)
    vec_env = concat_vec_envs_v1(
        vec_env,
        num_vec_envs=1,
        num_cpus=1,
        base_class="stable_baselines3",
    )
    vec_env = VecMonitor(vec_env)

    print("Initializing PPO (shared policy)...")
    model = PPO(
        policy="MlpPolicy",
        env=vec_env,
        device="cuda",
        verbose=1,
        n_steps=2048,
        batch_size=64,
        learning_rate=3e-4,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.0,
        vf_coef=0.5,
    )

    checkpoint_cb = CheckpointCallback(
        save_freq=100_000,
        save_path="./checkpoints",
        name_prefix="ppo_marl_shared",
    )

    total_timesteps = 1_000_000
    print(f"Training for {total_timesteps:,} timesteps...")
    model.learn(total_timesteps=total_timesteps, callback=checkpoint_cb)

    print("Saving final model...")
    model.save("ppo_marl_shared_policy")
    print("Done: ppo_marl_shared_policy.zip")