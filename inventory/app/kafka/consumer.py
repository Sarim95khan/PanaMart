from aiokafka import AIOKafkaConsumer
import json
from app.kafka.producer import get_kafka_producer
from app.db import get_session   
from app.db import Inventory


async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="inventory-service",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print("Consumer test")
            print(f"Product passed test inventory: {message.value.decode()} on topic {message.topic}")
            message = message.value.decode()
            print("message", message)
            if message == "Product not found":
                print("Product Not Found")
            else:
                db_product = json.loads(message)
                print("Product Found!!")
                print(db_product)
                with next(get_session()) as session:  
                    db_inventory = Inventory.model_validate(db_product)
                    session.add(db_inventory)
                    session.commit()
                    session.refresh(db_inventory)  
                    print("Inserted Stock", db_inventory)                      
    except:
        print("Error Consuming")
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()