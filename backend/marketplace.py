from operator import itemgetter
import copy

class Marketplace:
    def __init__(self, buyers, sellers):
        self.buyers = buyers
        self.sellers = sellers
        self.tick = 0
        self.history = []
        self.average_price = 0

    def run_tick(self):
        offers = self.collect_offers(self.average_price)
        requests = self.collect_requests(offers)
        
        matches = self.match_offers_requests(offers, requests)
        self.execute_transaction(matches)
        
        if matches:
            self.average_price = sum(m['price_per_unit'] for m in matches) / len(matches)
        
        # --- Agent Adjustment Phase ---
        buyers_traded = {buyer.id: False for buyer in self.buyers}
        for match in matches:
            buyers_traded[match['buyer id']] = True
        
        for buyer in self.buyers:
            market_feedback = {'successful_trade': buyers_traded[buyer.id]}
            buyer.maybe_adjust_price_limit(market_feedback)
        
        self.tick += 1
        
        return offers, requests, matches

    def collect_offers(self, average_price):
        offers = []
        for seller in self.sellers:
            if seller.is_active():
                offer = seller.decide_offer(average_price)
                if offer:
                    offers.append(offer)
        return offers

    def collect_requests(self, offers):
        requests = []
        for buyer in self.buyers:
            if buyer.is_active():
                request = buyer.decide_bid(offers)
                if request:
                    requests.append(request)
        return requests

    def match_offers_requests(self, offers, requests):
        matches = []
        
        # Use deep copies to avoid modifying the original lists
        offers_copy = copy.deepcopy(offers)
        requests_copy = copy.deepcopy(requests)
        
        offers_sorted = sorted(offers_copy, key=itemgetter('price_per_unit'))
        requests_sorted = sorted(requests_copy, key=itemgetter('price_per_unit'), reverse=True)
        
        for reqs in requests_sorted:
            for offs in offers_sorted:
                if reqs['price_per_unit'] >= offs['price_per_unit'] and offs['quantity'] > 0:
                    quantity = min(reqs['quantity'], offs['quantity'])

                    matches.append({
                        'buyer id': reqs['agent id'],
                        'seller id': offs['agent id'],
                        'quantity': quantity,
                        'price_per_unit': offs['price_per_unit']
                    })

                    reqs['quantity'] -= quantity
                    offs['quantity'] -= quantity
                    
                    if reqs['quantity'] <= 0:
                        break
        return matches

    def execute_transaction(self, matches):
        for m in matches:
            buyer = self.get_agent_by_id(m['buyer id'], self.buyers)
            seller = self.get_agent_by_id(m['seller id'], self.sellers)

            if not buyer or not seller:
                continue

            quantity = m['quantity']
            price_per_unit = m['price_per_unit']
            total_cost = quantity * price_per_unit

            # --- DEBUGGING PRINTS START HERE ---
            # Print details only for high-priced sellers to avoid spamming the log
            if price_per_unit > 1000:
                print("\n--- [DEBUG] High-Priced Transaction Check ---")
                print(f"[DEBUG] Match Details: Buyer {buyer.id} -> Seller {seller.id}")
                print(f"[DEBUG] Seller Price: ${price_per_unit:,.2f} | Quantity: {quantity}")
                print(f"[DEBUG] Calculated Total Cost: ${total_cost:,.2f}")
                print(f"[DEBUG] Buyer's Budget BEFORE check: ${buyer.budget:,.2f}")
            # --- DEBUGGING PRINTS END HERE ---

            if buyer.budget >= total_cost and seller.inventory >= quantity:
                if price_per_unit > 1000:
                    print(f"[DEBUG] RESULT: Budget check PASSED. This is the BUG.")
                
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
            else:
                if price_per_unit > 1000:
                    print(f"[DEBUG] RESULT: Budget check FAILED. Transaction skipped (Correct behavior).")

    def get_agent_by_id(self, agent_id, agent_list):
        for agent in agent_list:
            if agent.id == agent_id:
                return agent
        return None