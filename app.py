import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
import logging
import redis

app = Flask(__name__)


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def init_db():

    if not r.exists('item_id_counter'):
        r.set('item_id_counter', 0)

    if not r.exists('items'):

        pass

@app.route('/')
def index():

    item_ids = r.smembers('items')
    items = []
    for item_id in item_ids:
        item_data = r.hgetall(f'item:{item_id}')
        if item_data:

            item_data['id'] = item_id
            items.append(item_data)
    return render_template('index.html', items=items)

@app.route('/items', methods=['GET'])
def get_items():
    item_ids = r.smembers('items')
    items_list = []
    for item_id in item_ids:
        item_data = r.hgetall(f'item:{item_id}')
        if item_data:
            item_data['id'] = item_id
            items_list.append(item_data)
    return jsonify(items_list), 200

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item_data = r.hgetall(f'item:{item_id}')
    if not item_data:
        logging.warning(f'Item with id {item_id} not found')
        return jsonify({'error': 'Item not found'}), 404
    item_data['id'] = item_id
    return jsonify(item_data), 200

# Create item
@app.route('/items', methods=['POST'])
def create_item():
    name = request.form.get('name')
    description = request.form.get('description', '')

    if not name:
        logging.error('Name field is required for item creation.')
        return redirect(url_for('index'))

    new_id = r.incr('item_id_counter')

    r.hset(f'item:{new_id}', mapping={'name': name, 'description': description})

    r.sadd('items', new_id)

    logging.info(f'Item created with id {new_id}')
    return redirect(url_for('index'))
@app.route('/testitems', methods=['POST'])
def create_item_test():
    name = request.form.get('name')
    description = request.form.get('description', '')

    if not name:
        logging.error('Name field is required for item creation.')
        return redirect(url_for('index'))


    new_id = r.incr('item_id_counter')

    r.hset(f'item:{new_id}', mapping={'name': name, 'description': description})

    r.sadd('items', new_id)

    logging.info(f'Item created with id {new_id}')
    return jsonify({'status': 'success', 'id': new_id, 'name': name, 'description': description}), 200

# Update item
@app.route('/items/<int:item_id>/update', methods=['POST'])
def update_item(item_id):
    name = request.form.get('name')
    description = request.form.get('description')

    if not name:
        logging.error('Name field is required for item update.')
        return redirect(url_for('index'))


    if not r.exists(f'item:{item_id}'):
        logging.warning(f'No item with id {item_id} found to update.')
        return redirect(url_for('index'))

    r.hset(f'item:{item_id}', mapping={'name': name, 'description': description})
    logging.info(f'Item with id {item_id} updated.')
    return redirect(url_for('index'))

# Delete item
@app.route('/items/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):

    if not r.exists(f'item:{item_id}'):
        logging.warning(f'No item with id {item_id} found to delete.')
        return redirect(url_for('index'))


    r.delete(f'item:{item_id}')

    r.srem('items', item_id)

    logging.info(f'Item with id {item_id} deleted.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 8080))
    logging.info(f'Starting app on port {port}')
    app.run(host='0.0.0.0', port=port)
