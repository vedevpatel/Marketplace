# TODO [RL] Track historical offers and sales for training data
# TODO [RL] Replace static min_price_per_unit with RL-predicted price
# TODO [RL] Adjust quantity_to_offer dynamically using RL policy
# TODO [RL] Store state-action-reward tuples after each tick
# TODO [RL] Define reward signal (e.g., profit, revenue, inventory turnover)
# TODO [RL] Add method to update policy/weights after each episode


class SellerAgent:
    def __init__(self, agent_id, inventory, min_price, starting_price, max_per_tick):
        self.id = agent_id
        self.inventory = inventory
        self.min_price_per_unit = min_price
        self.starting_price = starting_price
        self.max_per_tick = max_per_tick
        self.total_revenue = 0
        
    # Willing to sell X units at $Y each 
    def decide_offer(self):
        if self.inventory <= 0:
            return None
        
        else:
            quantity_to_offer = min(self.inventory, self.max_per_tick)
            
            offer = {
                'agent id': self.id,
                'quantity': quantity_to_offer,
                'price_per_unit': self.min_price_per_unit
            }
            
        return offer
            
    # Updating revenue and tracking revenue after a sale
    def process_sales(self, quantity_sold, sale_price_per_unit):
        self.inventory -= quantity_sold
        self.total_revenue += quantity_sold * sale_price_per_unit
        
    
    def is_active(self):
        return self.inventory > 0
    
    