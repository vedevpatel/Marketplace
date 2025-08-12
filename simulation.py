from agents import BuyerAgent, SellerAgent
from marketplace import Marketplace

def main():
    # Creating buyers and sellers
    buyers = [
        BuyerAgent(agent_id=1, budget=1000, demand=10, price_limit=50),
        BuyerAgent(agent_id=2, budget=500, demand=5, price_limit=60),
        BuyerAgent(agent_id=3, budget=800, demand=8, price_limit=55),
        BuyerAgent(agent_id=4, budget=200, demand=4, price_limit=50),
        BuyerAgent(agent_id=5, budget=900, demand=10, price_limit=40),
    ]
    
    
    sellers = [
        SellerAgent(agent_id=101, inventory=15, min_price=40, starting_price=45, max_per_tick=10),
        SellerAgent(agent_id=102, inventory=20, min_price=35, starting_price=40, max_per_tick=8),
        SellerAgent(agent_id=103, inventory=10, min_price=45, starting_price=50, max_per_tick=9),
        SellerAgent(agent_id=104, inventory=90, min_price=25, starting_price=30, max_per_tick=20),
        SellerAgent(agent_id=105, inventory=130, min_price=15, starting_price=10, max_per_tick=15),
    ]
    
    # initializing marketplace
    market = Marketplace(buyers, sellers)
    
    # running simulation 
    market.run_market(num_ticks=10)
    
    # Printing transaction history
    print("Transaction History")
    for transaction in market.history:
        print(transaction)
        
    print("Final Buyer States")
    for buyer in buyers:
        print(f"Buyer{buyer.id}: Budget={buyer.budget}, Inventory={buyer.inventory}, Demand={buyer.demand}")

    print("Final Seller States")
    for seller in sellers:
        print(f"Seller {seller.id} Inventory = {seller.inventory}, Total Revenue = {seller.total_revenue}")
        
if __name__ == "__main__":
    main()    
    