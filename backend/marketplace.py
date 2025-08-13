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
        self.execute_transaction(matches)
        
        print(f"Tick {self.tick}:")
        print("Offers:", offers)
        print("Requests:", requests)
        
        # Create a map to check which buyers had successful trades this tick
        buyers_traded = {buyer.id: False for buyer in self.buyers}
        for match in matches:
            buyers_traded[match['buyer id']] = True
        
        # Let buyers adjust their price limits based on success/failure
        for buyer in self.buyers:
            market_feedback = {'successful_trade': buyers_traded[buyer.id]}
            buyer.maybe_adjust_price_limit(market_feedback)
        
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
        offers_sorted = sorted(offers, key=itemgetter('price_per_unit'))
        requests_sorted = sorted(requests, key=itemgetter('price_per_unit'), reverse=True)
        
        # Buyer should be willing to pay the seller's price per unit, and seller must have inventory
        for reqs in requests_sorted:
            for offs in offers_sorted:
                if reqs['price_per_unit'] >= offs['price_per_unit'] and offs['quantity'] > 0:
                    quantity = min(reqs['quantity'], offs['quantity'])

                    # if so, add a match to the record
                    matches.append({
                        'buyer id': reqs['agent id'],
                        'seller id': offs['agent id'],
                        'quantity': quantity,
                        'price_per_unit': offs['price_per_unit']
                    })

                    # rightly decrease the respective quantities
                    reqs['quantity'] -= quantity
                    offs['quantity'] -= quantity
                    
                    if reqs['quantity'] <= 0:
                        break
        return matches            
        

    def execute_transaction(self, matches):
        for m in matches:
            buyer = self.get_agent_by_id(m['buyer id'], self.buyers)
            seller = self.get_agent_by_id(m['seller id'], self.sellers)
            
            requested_quantity = m['quantity']
            price_per_unit = m['price_per_unit']
            total_cost = requested_quantity * price_per_unit
            
            if buyer.budget < total_cost:
                affordable_quantity = int(buyer.budget // price_per_unit)
                
                if affordable_quantity == 0:
                    # Can't afford even 1 unit, skip this transaction
                    continue
                
                quantity = affordable_quantity
                total_cost = quantity * price_per_unit
            else:
                quantity = requested_quantity
            
            trade_info = {'quantity': quantity, 'price_per_unit': price_per_unit}
            buyer.update_after_trade(trade_info)
            
            seller.process_sales(quantity, price_per_unit)
            
            self.history.append({
                'tick': self.tick,
                'buyer_id': buyer.id,
                'seller_id': seller.id,
                'quantity': quantity,
                'price_per_unit': price_per_unit,
                'total_cost': total_cost
            })

            
    def get_agent_by_id(self, agent_id, agent_list):
        for agent in agent_list:
            if agent.id == agent_id:
                return agent
        return None
    
    def run_market(self, num_ticks):
        for _ in range(num_ticks):
            self.run_tick()