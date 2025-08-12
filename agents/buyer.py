class BuyerAgent:
    def __init__(self, agent_id, budget, demand, price_limit):
        self.id = agent_id
        self.budget = budget
        self.demand = demand
        self.current_price_limit = price_limit
        self.inventory = 0
        
    def decide_bid(self):
        # Calculating units a buyer can afford given current price limit
        max_affordable_quantity = int(self.budget // self.current_price_limit)
        
        # Determining units a buyer actually wants (choosing minimum to avoid overspending)
        desired_quantity = min(self.demand, max_affordable_quantity)
        
        # If unaffordable, skip bidding
        if (desired_quantity <= 0):
            return None
        
        bid = {
            'agent id': self.id,
            'quantity': desired_quantity,
            'price_per_unit': self.current_price_limit
        }
        # Return the bid offer with quantity and price
        return bid
    
    
    def update_after_trade(self, trade):
        quantity_bought = trade['quantity']
        price_per_unit = trade['price_per_unit']
        
        total_cost = quantity_bought * price_per_unit
        
        self.budget = self.budget - total_cost
        self.demand = self.demand - quantity_bought
        self.inventory = self.inventory + quantity_bought
        
        if self.budget < 0:
            self.budget = 0
            
        if self.demand < 0:
            self.demand = 0
            
    
    """
    Adapt bidding strategy based on market feedback
    If buyer didn't buy in the last tick, maybe lower max willing price
    If buyer bought in last tick, maintain or increase price limit
    
    market_feedback should be a dictionary/object indicating whether
    last trade succeeded or not
    """
    
    def maybe_adjust_price_limit(self, market_feedback):
        if market_feedback['successful_trade'] == False:
            # Decrease price limit by 5%
            self.current_price_limit *= 0.95
            
        else:
            # Maintaining for now
            pass
         
    
    def is_active(self):
        return (self.demand > 0 and self.budget > 0)