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
                inventory=random.randint(70, 300),
                min_price=min_price,
                starting_price=starting_price,
                max_per_tick=random.randint(5, 15)
            )
        )
        
    return buyers, sellers


# Setting market size
NUM_BUYERS = 20
NUM_SELLERS = 10

# Creating agent populations
buyers, sellers = generate_agents(NUM_BUYERS, NUM_SELLERS)

# Create the marketplace globally with the generated agents
market = Marketplace(buyers, sellers)


def run_simulation_tick():
    # Runs simulation for a single tick and return the latest data."""
    offers, requests, matches = market.run_tick()  
    last_tick_data = {
        "tick": market.tick,
        "transactions": matches,
        "offers": offers,
        "requests": requests,
        "buyers": [
            {"id": b.id, "budget": round(b.budget, 2), "inventory": b.inventory, "demand": b.demand}
            for b in market.buyers
        ],
        "sellers": [
            {"id": s.id, "inventory": s.inventory, "price": round(s.current_price, 2), "revenue": round(s.total_revenue, 2)}
            for s in market.sellers
        ]
    }
    return last_tick_data