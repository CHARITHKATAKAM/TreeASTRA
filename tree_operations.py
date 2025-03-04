class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # for AVL tree
        self.color = 'RED'  # for Red-Black tree
        self.parent = None  # for Red-Black tree

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    def get_tree_structure(self):
        def serialize_node(node):
            if not node:
                return None
            return {
                'value': node.value,
                'color': getattr(node, 'color', None),
                'left': serialize_node(node.left),
                'right': serialize_node(node.right)
            }
        return serialize_node(self.root)

    def clear(self):
        self.root = None

    def inorder_traversal(self):
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.value)
                inorder(node.right)
        inorder(self.root)
        return result

    def preorder_traversal(self):
        result = []
        def preorder(node):
            if node:
                result.append(node.value)
                preorder(node.left)
                preorder(node.right)
        preorder(self.root)
        return result

    def postorder_traversal(self):
        result = []
        def postorder(node):
            if node:
                postorder(node.left)
                postorder(node.right)
                result.append(node.value)
        postorder(self.root)
        return result

class AVLTree(BinarySearchTree):
    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = max(self._get_height(y.left), self._get_height(y.right)) + 1
        x.height = max(self._get_height(x.left), self._get_height(x.right)) + 1

        return x

    def _left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = max(self._get_height(x.left), self._get_height(x.right)) + 1
        y.height = max(self._get_height(y.left), self._get_height(y.right)) + 1

        return y

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if not node:
            return Node(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        else:
            node.right = self._insert_recursive(node.right, value)

        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and value < node.left.value:
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and value > node.right.value:
            return self._left_rotate(node)

        # Left Right Case
        if balance > 1 and value > node.left.value:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Left Case
        if balance < -1 and value < node.right.value:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

class RedBlackTree(BinarySearchTree):
    def insert(self, value):
        node = Node(value)
        if not self.root:
            self.root = node
            node.color = 'BLACK'
        else:
            current = self.root
            parent = None
            while current:
                parent = current
                if value < current.value:
                    current = current.left
                else:
                    current = current.right

            node.parent = parent
            if value < parent.value:
                parent.left = node
            else:
                parent.right = node

            self._fix_insert(node)

    def _fix_insert(self, node):
        while node != self.root and node.parent.color == 'RED':
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left
                if uncle and uncle.color == 'RED':
                    uncle.color = 'BLACK'
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self._left_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.right
                if uncle and uncle.color == 'RED':
                    uncle.color = 'BLACK'
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self._right_rotate(node.parent.parent)

        self.root.color = 'BLACK'

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right:
            x.right.parent = y
        x.parent = y.parent
        if not y.parent:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x