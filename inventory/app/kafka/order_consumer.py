from aiokafka import AIOKafkaConsumer
import json
from app.kafka.producer import get_kafka_producer
from app.db import get_session   
from app.db import Inventory
from sqlmodel import select
from aiokafka import AIOKafkaProducer


async def order_consumer(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="order-verifier",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print("Consumer test")
            print(f"Order receieved data: {message.value.decode()} on topic {message.topic}")
            order_data = message.value 
            message = message.value.decode()
            json_data = json.loads(message)
            productId = json_data["product_id"]
            print("JSON DATA: ", json_data)
            print("Product ID: ", productId)

                # producer = AIOKafkaProducer(bootstrap_servers='broker:19092')

                # await producer.start()
                # if db_product is None:
                #     try:
                #         print('Product not found')
                #         await producer.send_and_wait("product-passed", b'Product not found')
                #     finally:
                #         await producer.stop()
                # if db_product is not None:
                #     try:
                #         print('Validation passed')
                #         await producer.send_and_wait("product-passed", message.value)
                #     finally:
                #         await producer.stop()

            with next(get_session()) as session:
                stmt = select(Inventory).where(Inventory.product_id == productId)
                producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
                await producer.start()

                db_product = session.exec(stmt).first()
                print("Inventory Product Found for stock calculation: ", db_product)
                if db_product is not None:
                    print("DB Product",db_product)
                    if db_product.stock >= json_data["quantity"]:
                        try:
                            print("Quantity Available/ In Stock")
                            await producer.send_and_wait("order-verified", order_data)
                        finally:
                            await producer.stop()
                    else:
                        print("Quantity not available")
                        try:
                            print('Validation passed')
                            await producer.send_and_wait("order-verified", b"Stock Not Available")
                        finally:
                            await producer.stop()                        

    except:
        print("Error Consuming")
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()