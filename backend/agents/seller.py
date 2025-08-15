# TODO [RL] Track historical offers and sales for training data
# TODO [RL] Replace static min_price_per_unit with RL-predicted price
# TODO [RL] Adjust quantity_to_offer dynamically using RL policy
# TODO [RL] Store state-action-reward tuples after each tick
# TODO [RL] Define reward signal (e.g., profit, revenue, inventory turnover)
# TODO [RL] Add method to update policy/weights after each episode
import random


class SellerAgent:
    def __init__(self, agent_id, inventory, min_price, starting_price, max_per_tick):
        self.id = agent_id
        self.initial_inventory = inventory
        self.inventory = inventory
        self.min_price_per_unit = min_price
        self.starting_price = starting_price
        self.max_per_tick = max_per_tick
        self.total_revenue = 0
        self.last_tick_sales = 0
        self.restock_cooldown = 0 # ticks to wait before restocking
        self.restock_period = 20 # how long the cooldown is
        self.current_price = starting_price
        
        
    # Willing to sell X units at $Y each 
    def decide_offer(self):
        if self.inventory <= 0:
            if self.restock_cooldown > 0:
                return None
            else:
                # restock arrived
                self.inventory = self.initial_inventory
                self.restock_cooldown = self.restock_period
    
        
        quantity_to_offer = min(self.inventory, self.max_per_tick)         
        offer = {
            'agent id': self.id,
            'quantity': quantity_to_offer,
            'price_per_unit': self.min_price_per_unit
        }
            
        return offer
    
    
    def adjust_price(self, average_market_price):
        """Adjust price and handle cooldown for the next tick."""
        # Decrement cooldown timer each tick
        if self.restock_cooldown > 0:
            self.restock_cooldown -= 1

        # Calculate what percentage of the offered inventory was sold
        if self.max_per_tick > 0:
            sell_through_rate = self.last_tick_sales / self.max_per_tick
        else:
            sell_through_rate = 0

        # Create a dynamic adjustment factor.
        # A 100% sell-through (rate=1.0) increases price by 5%.
        # A 0% sell-through (rate=0.0) decreases price by 5%.
        # A 50% sell-through (rate=0.5) keeps the price the same.
        adjustment_factor = 1 + (sell_through_rate - 0.5) * 0.1  # 0.1 is the sensitivity

        # Only apply the adjustment if there were sales or if we have inventory
        if self.last_tick_sales > 0 or self.inventory > 0:
            self.current_price *= adjustment_factor

        # Clamp price to the minimum
        if self.current_price < self.min_price_per_unit:
            self.current_price = self.min_price_per_unit
        
        # Reset sales counter for the next tick
        self.last_tick_sales = 0
            
    # Updating revenue and tracking revenue after a sale
    def process_sales(self, quantity_sold, sale_price_per_unit):
        self.inventory -= quantity_sold
        self.total_revenue += quantity_sold * sale_price_per_unit
        self.last_tick_sales += quantity_sold
        
    
    def is_active(self):
        # seller always active, even while waiting for a restock
        return True
    
    