import os
import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, url_for
import logging

DATABASE = 'items.db'

app = Flask(__name__)

# 设置logging到stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # 展示主页面
    conn = get_db_connection()
    items = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    return render_template('index.html', items=items)

# API接口
@app.route('/items', methods=['GET'])
def get_items():
    # 返回JSON的API（可选保留）
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    items_list = [dict(item) for item in items]
    return jsonify(items_list), 200

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    conn.close()
    if item is None:
        logging.warning(f'Item with id {item_id} not found')
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(dict(item)), 200

# Create item (从表单提交)
@app.route('/items', methods=['POST'])
def create_item():
    name = request.form.get('name')
    description = request.form.get('description', '')

    if not name:
        logging.error('Name field is required for item creation.')
        return redirect(url_for('index'))  # 如果失败，也可以返回主页或错误页面

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    logging.info(f'Item created with id {new_id}')
    # 创建成功后返回首页，而非返回JSON
    return redirect(url_for('index'))

# Update item (从表单提交)
@app.route('/items/<int:item_id>/update', methods=['POST'])
def update_item(item_id):
    name = request.form.get('name')
    description = request.form.get('description')

    if not name:
        logging.error('Name field is required for item update.')
        return redirect(url_for('index'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE items SET name = ?, description = ? WHERE id = ?', (name, description, item_id))
    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected == 0:
        logging.warning(f'No item with id {item_id} found to update.')
        return redirect(url_for('index'))

    logging.info(f'Item with id {item_id} updated.')
    return redirect(url_for('index'))

# Delete item (从表单提交)
@app.route('/items/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected == 0:
        logging.warning(f'No item with id {item_id} found to delete.')
        return redirect(url_for('index'))

    logging.info(f'Item with id {item_id} deleted.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 8080))
    logging.info(f'Starting app on port {port}')
    app.run(host='0.0.0.0', port=port)
