# TODO [RL] Replace static selection logic with RL-driven offer selection
# TODO [RL] Store state-action-reward tuples for learning
# TODO [RL] Define reward signal (e.g., satisfaction, utility from purchase)
# TODO [RL] Add policy update method for learning after each episode
import random

class BuyerAgent:
    def __init__(self, agent_id, budget, demand, price_limit):
        self.id = agent_id
        self.budget = budget
        self.demand = demand
        self.current_price_limit = price_limit
        self.inventory = 0
        self.income_per_tick = random.randint(5,20)
        # buyer consumes 1-5% of inventory each tick
        self.consumption_rate = random.uniform(0.01, 0.05)
        
    def decide_bid(self, available_offers):
        """
        Smarter buyer logic:
        1. Filters for affordable offers based on price limit.
        2. Sorts them to find the best deal.
        3. Decides a quantity based on budget, demand, and seller inventory.
        """
        if not available_offers:
            return None

        # 1. Filter for offers the buyer is willing to consider
        affordable_offers = [o for o in available_offers if o['price_per_unit'] <= self.current_price_limit]
        
        if not affordable_offers:
            return None # Nothing is cheap enough

        # 2. Sort to find the best deal (cheapest price first)
        best_offers = sorted(affordable_offers, key=lambda x: x['price_per_unit'])
        
        chosen_offer = best_offers[0]
        price = chosen_offer['price_per_unit']

        # 3. Decide how much to buy
        if price <= 0: return None # Avoid division by zero
        
        quantity_they_can_afford = int(self.budget // price)
        quantity_to_bid = min(self.demand, chosen_offer['quantity'], quantity_they_can_afford)
        
        # If unaffordable, skip bidding
        if quantity_to_bid <= 0:
            return None
        
        bid = {
            'agent id': self.id,
            'quantity': quantity_to_bid,
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
        self.budget += self.income_per_tick
        
         # Buyer consumes a portion of their inventory each tick
        if self.inventory > 0:
            consumed_amount = round(self.inventory * self.consumption_rate)
            if consumed_amount > 0:
                self.inventory -= consumed_amount
                # Consumption replenishes demand
                self.demand += consumed_amount

        # If trade failed, the buyer gets more impatient...
        if not market_feedback['successful_trade']:
            if random.random() < 0.5: 
                self.current_price_limit *= 1.05
        else:
            pass # On success, do nothing
        
        if self.current_price_limit > self.budget:
            self.current_price_limit = self.budget
    
    def is_active(self):
        return (self.demand > 0 and self.budget > 0)