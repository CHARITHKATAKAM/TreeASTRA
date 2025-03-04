from flask import Flask, render_template, request, jsonify
import logging
import os
from app import app, db
from models import TreeNode
from tree_operations import BinarySearchTree, AVLTree, RedBlackTree

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Store tree instances
trees = {
    'bst': BinarySearchTree(),
    'avl': AVLTree(),
    'rb': RedBlackTree()
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/add_node', methods=['POST'])
def add_node():
    try:
        data = request.json
        value = int(data.get('value'))
        tree_type = data.get('tree_type', 'bst')

        if tree_type not in trees:
            return jsonify({'success': False, 'error': 'Invalid tree type'}), 400

        # Add to in-memory tree for visualization
        trees[tree_type].insert(value)

        # Add to database
        new_node = TreeNode(
            value=value,
            tree_type=tree_type,
            color='RED' if tree_type == 'rb' else None,
            height=1 if tree_type == 'avl' else None
        )
        db.session.add(new_node)
        db.session.commit()

        return jsonify({
            'success': True,
            'tree': trees[tree_type].get_tree_structure()
        })
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid input'}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding node: {str(e)}")
        return jsonify({'success': False, 'error': 'Database error'}), 500

@app.route('/api/traverse', methods=['POST'])
def traverse():
    data = request.json
    traverse_type = data.get('type', 'inorder')
    tree_type = data.get('tree_type', 'bst')

    if tree_type not in trees:
        return jsonify({'success': False, 'error': 'Invalid tree type'}), 400

    result = []
    tree = trees[tree_type]

    if traverse_type == 'inorder':
        result = tree.inorder_traversal()
    elif traverse_type == 'preorder':
        result = tree.preorder_traversal()
    elif traverse_type == 'postorder':
        result = tree.postorder_traversal()

    return jsonify({
        'success': True,
        'traversal': result
    })

@app.route('/api/clear', methods=['POST'])
def clear_tree():
    try:
        data = request.json
        tree_type = data.get('tree_type', 'bst')

        if tree_type not in trees:
            return jsonify({'success': False, 'error': 'Invalid tree type'}), 400

        # Clear in-memory tree
        trees[tree_type].clear()

        # Clear database for specific tree type
        TreeNode.query.filter_by(tree_type=tree_type).delete()
        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error clearing tree: {str(e)}")
        return jsonify({'success': False, 'error': 'Database error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)