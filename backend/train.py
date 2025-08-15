import gymnasium as gym
from gymnasium import spaces
import numpy as np
from stable_baselines3 import PPO
from simulation import generate_agents, Marketplace
from agents.seller import SellerAgent


class MarketPlaceEnv(gym.Env):
    def __init__(self, num_buyers, num_other_sellers):
        super(MarketPlaceEnv, self).__init__()
        
        self.num_buyers = num_buyers
        self.num_other_sellers = num_other_sellers
        
        # Action space for RL Agent
        # 5 actions: price changes of -10%, -5%, 0%, 5%, 10%
        self.action_space = spaces.Discrete(5)
        
        # Observation Space (state)
        # [normalized_inventory, normalized_price]
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(2,), dtype=np.float32)
        
    def reset(self, seed=None, options=None):
        # Generate agents for new episode
        buyers, other_sellers = generate_agents(self.num_buyers, self.num_other_sellers)
        
        # making a single RL seller agent
        self.rl_agent = SellerAgent(
            agent_id=9999, 
            inventory=100,
            min_price=10,
            starting_price=30,
            max_per_tick=10
        )
        
        all_sellers = other_sellers + [self.rl_agent]
        
        # create the marketplace for this episode
        self.market = Marketplace(buyers, all_sellers)
        self.current_step = 0
        
        # getting init state
        initial_state = self.rl_agent.get_state(self.market.average_price)
        return np.array(initial_state, dtype=np.float32), {}

    def step(self, action):
        # RL model provides an action 0, 1, 2, 3, 4

        # --- RL Agent acts ---
        # override the agent's brain and force it to take the action
        price_change_percent = self.rl_agent.actions[action]
        self.rl_agent.current_price *= (1 + price_change_percent)
        if self.rl_agent.current_price < self.rl_agent.min_price_per_unit:
            self.rl_agent.current_price = self.rl_agent.min_price_per_unit
        
        self.rl_agent.last_tick_sales = 0 # reset counter
        
        # rest of the market simulates one tick ---
        self.market.run_tick()
        
        # results ---
        # reward = revenue RL agent made this step
        reward = self.rl_agent.last_tick_sales * self.rl_agent.current_price
        
        # get next state for agent
        next_state = self.rl_agent.get_state(self.market.average_price)
        
        # check if episode is done
        self.current_step += 1
        done = self.current_step >= 1000 # end episode after 1000 ticks

        return np.array(next_state, dtype=np.float32), reward, done, False, {}


if __name__ == '__main__':
    # creates training environment
    env = MarketPlaceEnv(num_buyers=100, num_other_sellers=20)

    # initializes ppo model
    model = PPO("MlpPolicy", env, verbose=1)

    
    # model trains for 100,000 ticks
    model.learn(total_timesteps=100000)

    print("Training complete. Saving.")
    model.save("ppo_marketplace_seller")

    print("Model saved as ppo_marketplace_seller.zip")