from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from app.db import get_session
from app.models import Product
from app.kafka.producer import get_kafka_producer
from app.models import Product



async def inventory_consumer(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="product-inventory",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print("Product- Inventory Consumer test")
            print(f"Received message: {message.value.decode()} on topic {message.topic}")

            inventory_data = json.loads(message.value.decode())
            product_id = inventory_data['product_id']
            print("Product ID Recieved in Produce Microservice:", product_id)

            with next(get_session()) as session:
                db_product = session.get(Product, inventory_data["product_id"])
                producer = AIOKafkaProducer(bootstrap_servers='broker:19092')

                await producer.start()
                if db_product is None:
                    try:
                        print('Product not found')
                        await producer.send_and_wait("product-passed", b'Product not found')
                    finally:
                        await producer.stop()
                if db_product is not None:
                    try:
                        print('Validation passed')
                        await producer.send_and_wait("product-passed", message.value)
                    finally:
                        await producer.stop()

    except:
        print("Error Consuming")
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()

