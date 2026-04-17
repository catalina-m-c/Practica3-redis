import redis

def initialize_products(redis_client):
    productos = [
        {"id": "1", "name": "Laptop", "price": 999.99, "description": "Portatil potente", "stock": 10},
        {"id": "2", "name": "Raton", "price": 19.99, "description": "Raton inalambrico", "stock": 50},
        {"id": "3", "name": "Teclado", "price": 49.99, "description": "Teclado mecanico", "stock": 30},
        {"id": "4", "name": "Monitor", "price": 199.99, "description": "Monitor 24 pulgadas", "stock": 20},
        {"id": "5", "name": "Auriculares", "price": 89.99, "description": "Auriculares Bluetooth", "stock": 25},
        {"id": "6", "name": "Webcam", "price": 59.99, "description": "Webcam HD", "stock": 15},
        {"id": "7", "name": "Microfono", "price": 79.99, "description": "Microfono USB", "stock": 18},
        {"id": "8", "name": "Tablet", "price": 299.99, "description": "Tablet ligera", "stock": 12},
        {"id": "9", "name": "Smartphone", "price": 699.99, "description": "Telefono inteligente", "stock": 22},
        {"id": "10", "name": "Cargador", "price": 29.99, "description": "Cargador rapido", "stock": 40}
    ]

    # Guardar productos en Redis
    for producto in productos:
        clave = f"producto:{producto['id']}"
        redis_client.hset(clave, mapping=producto)

    print("Productos cargados en Redis")

    # Verificación (IMPORTANTE para la práctica)
    print("\nLista de productos en Redis:")
    for clave in redis_client.scan_iter("producto:*"):
        producto = redis_client.hgetall(clave)
        print(producto)



if __name__ == "__main__":
    try:
        #TODO: Configura la conexión a Redis 
        redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

        # Inicializa los productos en Redis
        initialize_products(redis_client)
        print("¡Productos inicializados en Redis!")

    except Exception as e:
        print(f"Error al conectarse a Redis: {e}")
