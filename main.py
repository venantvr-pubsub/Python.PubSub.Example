import logging

# noinspection PyPackageRequirements
from pubsub import PubSubClient

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create client with multiple topics
client = PubSubClient(
    url="http://localhost:5000",
    consumer="service-a",
    topics=["orders", "inventory", "shipping"]
)


# Define custom handlers for each topic
def process_order(message):
    order_id = message.get("order_id")
    print(f"Processing order: {order_id}")
    # Your order processing logic here


def update_inventory(message):
    item_id = message.get("item_id")
    quantity = message.get("quantity")
    print(f"Updating inventory for item {item_id}: {quantity}")
    # Your inventory logic here


def track_shipping(message):
    tracking_number = message.get("tracking_number")
    print(f"Tracking shipment: {tracking_number}")
    # Your shipping logic here


# Register handlers
client.register_handler("orders", process_order)
client.register_handler("inventory", update_inventory)
client.register_handler("shipping", track_shipping)

# Start client (blocking)
try:
    client.start()
except KeyboardInterrupt:
    print("Shutting down client...")
