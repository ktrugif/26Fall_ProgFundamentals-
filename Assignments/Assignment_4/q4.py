item_name = "Waffles" #string
unit_price = 18.99 #float
quantity = 2
Tax_Rate = 0.5 #5% Tax Rate

# Calculating the costs
subtotal = unit_price * quantity
tax_amount = subtotal * Tax_Rate
total_price = subtotal + tax_amount

print(f"Item: {item_name}")
print(f"Subtotal: ${subtotal:.2f}")
print(f"Tax: ${tax_amount:.2f}")
print(f"Total Price: ${total_price:.2f}")
