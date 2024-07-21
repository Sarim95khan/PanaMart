from fastapi import APIRouter, Depends, HTTPException, Request, Header
from fastapi.responses import RedirectResponse
from typing import Annotated
from sqlmodel import select
import logging

import json
from aiokafka import AIOKafkaProducer
from app.kafka.producer import get_kafka_producer

from app.db import get_session, Session,Inventory

import stripe

logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


payment_router = APIRouter(tags=["payment"], prefix="/payment")

stripe.api_key = 'sk_test_51NJdQ5EeY9w1IjmkOTQtgcUe5RewfCsLEquzcKQExlcI585M9Sf7gV3PepH2i8LjoCdeOBpgWsOznkVxNcWQodBu00rrrUcsHc'

@payment_router.post('/create-checkout-session')
def create_checkout_session():
    try:
        
      session = stripe.checkout.Session.create(
      line_items=[{
        'price_data': {
          'currency': 'usd',
          'product_data': {
            'name': 'T-shirt',
          },
          'unit_amount': 2000,
        },
        'quantity': 1,
      }],

    #   line_items=[
    #     {
    #         "price_data": {
    #             "currency": "usd",
    #             "product_data": {
    #                 "name": "FastAPI Stripe Checkout",
    #             },
    #             "unit_amount": 30000,
    #         },
    #         "quantity": 1,
    #     }
    # ],
    # metadata={
    #     "user_id": 3,
    #     "email": "abc@gmail.com",
    #     "request_id": 1234567890,
    #     "products_ordered": ["Product A", "Product B"],  # Add product names here
    # },
      mode='payment',
      success_url='http://localhost:3000/success',
      cancel_url='http://localhost:3000/cancel',
    )
      # return RedirectResponse(url=session.url) 
      # return {'url':session.url}
      return {"session":session}
    except Exception as e:
      return HTTPException(status_code=500, detail=str(e)
                           
)

endpoint_secret = 'whsec_70863fe9d7f9da6590efaf2354259c4ada3a0d4446a0636c25fc91eb1c69bfd6 '

producer = get_kafka_producer()

@payment_router.post("/webhook/")
async def stripe_webhook(request: Request,
                          stripe_signature: str = Header(str),
                          # producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)
                          # ] 
                          ):
    payload = await request.body()
    event = None
    try:
        event = stripe.Event.construct_from(payload=payload, signature=stripe_signature)
        event_data = event['data']
    except Exception as e:
       return {"error":str(e)}

    if event["type"] == "checkout.session.completed":
        payment = event["data"]["object"]
        print("Checkout session completed")
    elif event["type"] == "payment_intent.succeeded":
        payment = event["data"]["object"]
        print("Payment succeeded")
        logging.info(f"Succeeded Payment")
        await producer.send_and_wait(('order-confirmed', b'Order confirmed'))
    elif event["type"] == "payment_method.attached":
        payment = event["data"]["object"]
        # amount = payment["amount_total"]
        # currency = payment["currency"]
        # user_id = payment["metadata"]["user_id"]
        print("Payment", payment)
        # user_email = payment["customer_details"]["email"]
        # order_id = payment["id"]
        # Save order details to your database
        # Send email confirmation (you can use background tasks for this)
    return {"status":"success"}

@payment_router.post('/test')
def process_input(request_body: dict):
    print("Received request body:", request_body)
    return {"message": "Request body received successfully!"}

