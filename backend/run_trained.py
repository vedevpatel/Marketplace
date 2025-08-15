import asyncio
import traceback
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from stable_baselines3 import PPO

# Import your existing simulation classes
from simulation import generate_agents, Marketplace
from agents.seller import SellerAgent

# --- Create a New Agent Class for the RL Model ---
class RLSellerAgent(SellerAgent):
    def __init__(self, agent_id, inventory, min_price, starting_price, max_per_tick, model_path):
        super().__init__(agent_id, inventory, min_price, starting_price, max_per_tick)
        # Load the trained model into this agent
        self.model = PPO.load(model_path)
        print(f"RL Agent {self.id} loaded model from {model_path}")

    def choose_action(self, state):
        """ The agent's 'brain' is now the trained neural network. """
        # The model.predict method takes the state and returns the best action
        action_index, _ = self.model.predict(state, deterministic=True)
        return action_index

# --- Main Application Setup ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Create the Market with One RL Agent ---
START_INVENTORY = 100
MIN_PRICE = 15
STARTING_PRICE = 30
MAX_PER_TICK = 10

# Generate the buyers
buyers, _ = generate_agents(6, 0) # We only need 6 buyers and 0 random sellers

# Manually create the rule-based seller with the defined stats
rule_based_seller = SellerAgent(
    agent_id=1001, # Give it a normal ID
    inventory=START_INVENTORY,
    min_price=MIN_PRICE,
    starting_price=STARTING_PRICE,
    max_per_tick=MAX_PER_TICK
)
# Create and add our one special RL agent
rl_agent = RLSellerAgent(
    agent_id=9999,
    inventory=START_INVENTORY,
    min_price=MIN_PRICE,
    starting_price=STARTING_PRICE,
    max_per_tick=MAX_PER_TICK,
    model_path="/app/ppo_marketplace_seller.zip" # Path inside the container
)

all_sellers = [rule_based_seller, rl_agent]
market = Marketplace(buyers, all_sellers)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("INFO:     connection open")
    try:
        while True:
            offers, requests, matches = market.run_tick()
            data = {
                "tick": market.tick,
                "transactions": matches,
                "offers": offers,
                "requests": requests,
                "buyers": [{"id": b.id, "budget": round(b.budget, 2), "inventory": b.inventory, "demand": b.demand} for b in market.buyers],
                "sellers": [{"id": s.id, "inventory": s.inventory, "price": round(s.current_price, 2), "revenue": round(s.total_revenue, 2)} for s in market.sellers]
            }
            try:
                await websocket.send_json(data)
            except Exception:
                break
            await asyncio.sleep(1)
    except Exception as e:
        print(f"ERROR: An exception occurred: {e}")
        traceback.print_exc()
    finally:
        print("INFO:     connection closed")