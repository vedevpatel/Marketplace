from operator import itemgetter


class Marketplace:
    def __init__(self, buyers, sellers):
        self.buyers = buyers
        self.sellers = sellers
        self.tick = 0
        self.history = [] # Stores transactions
     
     
    # Running one round of the market simulation
    def run_tick(self):
        offers = self.collect_offers()
        requests = self.collect_requests()
        
        matches = self.match_offers_requests(offers, requests)
        self.execute_transactions(matches)
        
        self.tick += 1
        
    
    # Asking all sellers for their offers
    def collect_offers(self):
        offers = []
        for seller in self.sellers:
            offer = seller.decide_offer()
            
            if offer:
                offers.append(offer)
        return offers
    
    
    # Asking all buyers for their buy requests
    def collect_requests(self):
        requests = []
        for buyer in self.buyers:
            request = buyer.decide_bid()
            
            if request:
                requests.append(request)
                
        return requests
        
    # matches buyers and sellers
    def match_offers_requests(self, offers, requests):
        matches = []
        
        # matching cheapest offers to highest paying buyers
        offers_sorted = sorted(offers, key=itemgetter('price per unit'))
        requests_sorted = sorted(requests, key=itemgetter('max price per unit'))
        
        # Buyer should be willing to pay the seller's price per unit, and seller must have inventory
        for reqs in requests_sorted:
            for offs in offers_sorted:
                if reqs['price per unit'] >= offs['price per unit'] and offs['quantity'] > 0:
                    quantity = min(reqs['quantity'], offs['quantity'])

                    # if so, add a match to the record
                    matches.append({
                        'buyer id': reqs['agent id'],
                        'seller id': offs['agent id'],
                        'quantity': quantity,
                        'price per unit': offs['price per unit']
                    })

                    # rightly decrease the respective quantities
                    reqs['quantity'] -= quantity
                    offs['quantity'] -= quantity
                    
                    if reqs['quantity'] <= 0:
                        break
        return matches            
        

    def execute_transaction(self, matches):
        # Updating buyer-seller state and transactions
        
        for m in matches:
            buyer = self.get_agent_by_id(m['buyer id'], self.buyers)
            seller = self.get_agent_by_id(m['seller id'], self.sellers)
            
            total_cost = m['quantity'] * m['price per unit']
            
            if buyer.budget < total_cost:
                affordable_quantity = int(buyer.budget // m['price per unit'])
                
                # Skip transaction entirely (cant afford even 1 unit)
                if affordable_quantity == 0:
                    continue
            
                # Adjusting total cost & quantity to affordable amt
                total_cost = affordable_quantity * m['price per unit']
                quantity = affordable_quantity
            
            else:
                quantity = m['quantity']
                
            buyer.budget -= total_cost
            buyer.inventory += quantity
            
            seller.inventory -= quantity
            seller.total_revenue += total_cost
            
            
    def get_agent_by_id(self, agent_id, agent_list):
        for agent in agent_list:
            if agent.id == agent_id:
                return agent
        return None
    
    def run_market(self, num_ticks):
        for _ in range(num_ticks):
            self.run_tick()