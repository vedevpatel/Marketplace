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
        self.ticks_with_no_sales = 0
        
        # RL Action Space - 5 possible actions
        self.actions = [-0.10, -0.05, 0, 0.05, 0.10] # dec. price by 10%, 5%...
        
    def get_state(self, average_market_price):
        # gathers info into state representation
        # normalizing inventory vals
        normalized_inventory = self.inventory / self.initial_inventory if self.initial_inventory > 0 else 0
        
        # normalize relative to market avg
        normalized_price = self.current_price / average_market_price if average_market_price > 0 else 1
        
        return [normalized_inventory, normalized_price]
    
    
    def choose_action(self, state):
        # agent brain
        
        # 1. if we sold max, try to raise price
        if self.last_tick_sales >= self.max_per_tick:
            return 4 # index for 10% price hike
        
        # 2. if we have inventory but sold nothing, lower price
        if self.last_tick_sales == 0 and self.inventory > 0:
            return 1 # 5% price decrease
        
        # otherwise, make no change
        return 2
    
        
    # Willing to sell X units at $Y each 
    def decide_offer(self, average_market_price):
        self.adjust_price(average_market_price)        
        
        # restocking logic        
        if self.inventory <= 0:
            if self.restock_cooldown > 0:
                self.restock_cooldown -= 1
                return None
            else:
                # restock arrived
                self.inventory = self.initial_inventory
                self.restock_cooldown = self.restock_period
    
        # creating offer
        quantity_to_offer = min(self.inventory, self.max_per_tick)         
        offer = {
            'agent id': self.id,
            'quantity': quantity_to_offer,
            'price_per_unit': self.min_price_per_unit
        }
            
        return offer
    
    
    def adjust_price(self, average_market_price):
        # --- Bubble Pop Logic ---
        # If we haven't sold anything for 10 ticks and our price is
        # more than 3x the market average, we're in a bubble. Pop it.
        if self.ticks_with_no_sales > 10 and self.current_price > average_market_price * 3 and average_market_price > 0:
            self.current_price = average_market_price * 1.1 # Reset to just above average
            self.ticks_with_no_sales = 0 # Reset counter
            return # End the adjustment for this tick

        # --- Standard Proportional Pricing ---
        if self.max_per_tick > 0:
            sell_through_rate = self.last_tick_sales / self.max_per_tick
        else:
            sell_through_rate = 0

        adjustment_factor = 1 + (sell_through_rate - 0.5) * 0.1

        # Only adjust if there was activity or we have stock to sell
        if self.last_tick_sales > 0 or self.inventory > 0:
            self.current_price *= adjustment_factor

        # Clamp price to the minimum and reset counters
        if self.current_price < self.min_price_per_unit:
            self.current_price = self.min_price_per_unit
        
        if self.last_tick_sales == 0:
            self.ticks_with_no_sales += 1
        else:
            self.ticks_with_no_sales = 0
            
        self.last_tick_sales = 0
            
    # Updating revenue and tracking revenue after a sale
    def process_sales(self, quantity_sold, sale_price_per_unit):
        self.inventory -= quantity_sold
        revenue_this_tick = quantity_sold * sale_price_per_unit
        self.total_revenue += revenue_this_tick
        self.last_tick_sales += quantity_sold
        
        reward = revenue_this_tick
        
    
    def is_active(self):
        # seller always active, even while waiting for a restock
        return True
    
    