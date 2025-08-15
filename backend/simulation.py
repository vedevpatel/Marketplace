import random
from agents import BuyerAgent, SellerAgent
from marketplace import Marketplace


def generate_agents(num_buyers, num_sellers):
    # creates lists of buyers and sellers with random parameters 
    buyers = []
    sellers = []
    
    # Generate Buyers
    for i in range(num_buyers):
        # Most buyers will have a price limit around $50, with some variance
        price_limit = round(random.gauss(50, 10), 2)
        if price_limit < 1: price_limit = 1 # Ensure price is not negative
        
        buyers.append(
            BuyerAgent(
                agent_id=i + 1,
                budget=random.randint(500, 5000),
                demand=random.randint(50, 200),
                price_limit=price_limit
            )
        )
        
    # Generate Sellers
    for i in range(num_sellers):
        min_price = random.randint(10, 40) # Seller's cost basis
        # Starting price is a 10-50% markup on their cost
        starting_price = round(min_price * random.uniform(1.1, 1.5), 2)

        sellers.append(
            SellerAgent(
                agent_id=i + 1001, # Using a different ID range for sellers
                inventory=random.randint(20, 100),
                min_price=min_price,
                starting_price=starting_price,
                max_per_tick=random.randint(5, 15)
            )
        )
        
    return buyers, sellers


# Setting market size
NUM_BUYERS = 200
NUM_SELLERS = 50

# Creating agent populations
buyers, sellers = generate_agents(NUM_BUYERS, NUM_SELLERS)

# Create the marketplace globally with the generated agents
market = Marketplace(buyers, sellers)


def run_simulation_tick():
    # Runs simulation for a single tick and return the latest data."""
    market.run_market(num_ticks=1)  # Advance by 1 tick
    last_tick_data = {
        "transactions": market.history[-1] if market.history else [],
        "buyers": [
            {"id": b.id, "budget": b.budget, "inventory": b.inventory, "demand": b.demand}
            for b in buyers
        ],
        "sellers": [
            {"id": s.id, "inventory": s.inventory, "revenue": s.total_revenue, "price": s.min_price_per_unit}
            for s in sellers
        ]
    }
    return last_tick_data