import logging
import random
import threading
import time
import uuid

# noinspection PyPackageRequirements
from pubsub.pubsub_client import PubSubClient

# Configure un logging plus détaillé pour voir les messages du client et du producteur
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)


# --- NOUVELLE FONCTION POUR PUBLIER DES ÉVÉNEMENTS ---
def publish_events(client: PubSubClient, stop_event: threading.Event):
    """
    Cette fonction s'exécute dans un thread séparé et publie des
    messages aléatoires à intervalle régulier.
    """
    topics = ["orders", "inventory", "shipping"]
    items = ["item-A7X", "item-B9Y", "item-C3Z"]

    while not stop_event.is_set():
        try:
            # Choisit un sujet au hasard
            topic = random.choice(topics)
            message = {}
            message_id = str(uuid.uuid4())

            # Crée un message adapté au sujet
            if topic == "orders":
                message = {
                    "order_id": message_id,
                    "item": random.choice(items),
                    "quantity": random.randint(1, 5)
                }
            elif topic == "inventory":
                message = {
                    "item_id": random.choice(items),
                    "quantity": random.randint(-10, 20),
                    "warehouse": "central"
                }
            elif topic == "shipping":
                message = {
                    "tracking_number": f"TN{random.randint(1000000, 9999999)}",
                    "order_id": str(uuid.uuid4())
                }

            # Publie le message
            logging.info(f"PUBLISHING to '{topic}': {message}")
            client.publish(
                topic=topic,
                message=message,
                producer=client.consumer,  # Le client est aussi le producteur dans cet exemple
                message_id=message_id
            )

            # Attend un moment avant le prochain envoi
            time.sleep(random.uniform(2, 5))

        except Exception as e:
            logging.error(f"Error in publisher thread: {e}")
            time.sleep(5)


# --- CONFIGURATION DU CLIENT (INCHANGÉE) ---

# Crée le client
client = PubSubClient(
    url="http://localhost:5000",
    consumer="service-a",
    topics=["orders", "inventory", "shipping"]
)


# Définit les handlers pour chaque sujet
def process_order(message):
    order_id = message.get("order_id")
    logging.info(f"--- PROCESSING ORDER: {order_id}")

def update_inventory(message):
    item_id = message.get("item_id")
    quantity = message.get("quantity")
    logging.info(f"--- UPDATING INVENTORY for item {item_id}: {quantity}")

def track_shipping(message):
    tracking_number = message.get("tracking_number")
    logging.info(f"--- TRACKING SHIPMENT: {tracking_number}")


# Enregistre les handlers
client.register_handler("orders", process_order)
client.register_handler("inventory", update_inventory)
client.register_handler("shipping", track_shipping)

# --- DÉMARRAGE DU CLIENT ET DU PRODUCTEUR ---

if __name__ == "__main__":
    # Événement pour arrêter proprement le thread de publication
    stop_publisher = threading.Event()

    # Crée et lance le thread qui va publier les messages en boucle
    publisher_thread = threading.Thread(
        target=publish_events,
        args=(client, stop_publisher),
        name="PublisherThread",
        daemon=True  # Permet au programme de se fermer même si ce thread tourne encore
    )
    publisher_thread.start()

    try:
        # Démarre le client pour écouter les messages (ceci est bloquant)
        logging.info("Client starting to listen...")
        client.start()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
        # Signale au thread de publication de s'arrêter
        stop_publisher.set()
        # Attend que le thread se termine proprement
        publisher_thread.join(timeout=2)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        stop_publisher.set()
        publisher_thread.join(timeout=2)

    logging.info("Client shut down.")
