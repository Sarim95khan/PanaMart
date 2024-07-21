from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from app.db import get_session
from app.kafka.producer import get_kafka_producer
# from app.db import Order
from app.models import Order



async def order_verification_consumer(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="order_verification",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print("Order Verifcation Recieved message by Order Service")
            print(f"Received message: {message.value.decode()} on topic {message.topic}")
            message = message.value.decode()
            print("Message: ", message)
            if message == "Stock Not Available":
                print("Stock Not Available")
            else:
                db_order_message = json.loads(message)
                print("DB Order JSON", db_order_message)
                with next(get_session()) as session:
                    db_order = Order.model_validate(db_order_message)
                    session.add(db_order)
                    session.commit()
                    session.refresh(db_order)

            

            # inventory_data = json.loads(message.value.decode())
            # product_id = inventory_data['product_id']
            # print("Product ID Recieved in Produce Microservice:", product_id)

            # with next(get_session()) as session:
            #     db_product = session.get(Product, inventory_data["product_id"])
            #     producer = AIOKafkaProducer(bootstrap_servers='broker:19092')

            #     await producer.start()
            #     if db_product is None:
            #         try:
            #             print('Product not found')
            #             await producer.send_and_wait("product-passed", b'Product not found')
            #         finally:
            #             await producer.stop()
            #     if db_product is not None:
            #         try:
            #             print('Validation passed')
            #             await producer.send_and_wait("product-passed", message.value)
            #         finally:
            #             await producer.stop()

    except:
        print("Error Consuming")
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()

