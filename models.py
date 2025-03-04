from app import db
from datetime import datetime

class TreeNode(db.Model):
    __tablename__ = 'tree_nodes'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('tree_nodes.id'), nullable=True)
    is_left_child = db.Column(db.Boolean, nullable=True)
    tree_type = db.Column(db.String(20), nullable=False, default='bst')  # 'bst', 'avl', 'rb'
    color = db.Column(db.String(10), nullable=True)  # for Red-Black tree: 'RED' or 'BLACK'
    height = db.Column(db.Integer, nullable=True)  # for AVL tree
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Self-referential relationship
    children = db.relationship(
        'TreeNode',
        backref=db.backref('parent', remote_side=[id]),
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'parent_id': self.parent_id,
            'is_left_child': self.is_left_child,
            'tree_type': self.tree_type,
            'color': self.color,
            'height': self.height
        }