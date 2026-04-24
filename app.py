from flask import Flask, jsonify, request, render_template
import redis

app = Flask(__name__)

# TODO: Configura la conexión a Redis 
#redis_client = redis_client es el objeto de conexión a Redis
redis_client = redis.StrictRedis(
    host='localhost',  # fase 1
    port=6379,
    decode_responses=True
)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def get_products():
    
    products = []

    # TODO: Obtener la lista de productos de Redis
    for clave in redis_client.scan_iter("producto:*"):
        producto = redis_client.hgetall(clave)
        products.append(producto)

    return jsonify(products)


@app.route('/cart', methods=['GET'])
def get_cart():
    
    cart_items = []
    # TODO: Obtener los elementos de la cesta desde Redis
    for clave in redis_client.scan_iter("cart:*"):
        item = redis_client.hgetall(clave)
        cart_items.append(item)

    return jsonify(cart_items)


@app.route('/cart', methods=['POST'])
def add_to_cart():
    # TODO: Añadir un producto a la cesta en Redis con las verificaciones pertinentes

    data = request.get_json()
    product_id = data.get("id")

    # comprobar si existe el producto
    product_key = f"producto:{product_id}"
    if not redis_client.exists(product_key):
        return jsonify({"error": "Producto no existe"}), 404

    # obtener datos del producto
    product = redis_client.hgetall(product_key)

    cart_key = f"cart:{product_id}"

    # si ya está en la cesta → incrementar cantidad
    if redis_client.exists(cart_key):
        redis_client.hincrby(cart_key, "quantity", 1)
    else:
        # crear nuevo item en la cesta
        redis_client.hset(cart_key, mapping={
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": 1
        })

    return jsonify({"message": "Producto añadido a la cesta"})


@app.route('/checkout', methods=['POST'])
def checkout():
    # TODO: Procesar la compra y limpiar la cesta en Redis
    for clave in redis_client.scan_iter("cart:*"):
        redis_client.delete(clave)

    return jsonify({"message": "Compra realizada y cesta vaciada"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
