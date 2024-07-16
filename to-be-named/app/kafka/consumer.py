# from aiokafka import AIOKafkaConsumer


# async def consume_messages(topic, bootstrap_servers):
#     # Create a consumer instance.
#     consumer = AIOKafkaConsumer(
#         topic,
#         bootstrap_servers=bootstrap_servers,
#         group_id="product-microservice",
#         auto_offset_reset='earliest'
#     )

#     # Start the consumer.
#     await consumer.start()
#     try:
#         # Continuously listen for messages.
#         async for message in consumer:
#             print("Consumer test")
#             print(f"Received message: {message.value.decode()} on topic {message.topic}")

#             # new_todo 
#         # Here you can add code to process each message.
#         # Example: parse the message, store it in a database, etc.
#     except:
#         print("Error Consuming")
#     finally:
#         # Ensure to close the consumer when done.
#         await consumer.stop()