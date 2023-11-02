import stripe
stripe.api_key = "sk_test_51O88InKpZrz6Qt9A0EZHKwbaVVI1fzQK72bwEpFCtfWf6A8jEMce9sNWqIvLwfKy9hHdCOKZceMO4TwLHpgKzVjx00uFCWmj1U"

# CREATE CUSTOMER
# customer_data = stripe.Customer.create(
#   description="Customer for rajat4665@gmail.com",
#     name = 'Rajat',
#     email = "fasoprogramming@gmail.com",
#     source="tok_visa" # default testing card details
# )
# print(customer_data.id)

# # EXISTING CUSTOMER DATA
# customer_check = stripe.Customer.retrieve(customer_data.id)
# print(customer_check)

# CREATE ONE-TIME PAYMENT
charge_customer = stripe.Charge.create(
  amount=189, # amount multyply by 100 , here actual it is $20 
  currency="usd", # currency
  source="tok_mastercard", # obtained with Stripe.js
  description="Charge for rajat4665@example.com"
)
print(charge_customer)

# CREATE SUBSCRIPTION
# two things need for subsription customer_id , plan_id
# stripe.Plan.list()  # this command fetch all plans 
# plan = stripe.Plan.list()
# plan_id = plan['data'][0]['id']
# # Now create subscription
# stripe.Subscription.create(
#   customer="cus_FLqkPARN8ZxJj2", # customer_id
#   items=[
#     {
#       "plan": "plan_FLqJYiz3PiWtjo", # plan id
#     },
#   ]
# )
# # save subscription id=sub_FLqrJYMk9j81VM  it will use further
# # CANCEL SUBSCRIPTION
# stripe.Subscription.create(
#   customer="cus_FLpiGJp4IqREJj",
#   items=[
#     {
#       "plan": "plan_FLqJYiz3PiWtjo",
#     },
#   ]
# )
# # DELETE CUSTOMER
# stripe.Customer.delete('cus_id')