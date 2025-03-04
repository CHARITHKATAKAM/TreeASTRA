// File: static/js/tree.js
document.addEventListener('DOMContentLoaded', function() {
    const canvas = new TreeCanvas('treeCanvas');
    let currentTree = null;

    // Add node button handler
    document.getElementById('addNode').addEventListener('click', async () => {
        const input = document.getElementById('nodeValue');
        const value = parseInt(input.value);
        const treeType = document.getElementById('treeType').value;

        if (isNaN(value)) {
            alert('Please enter a valid number');
            return;
        }

        try {
            const response = await fetch('/api/add_node', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ value, tree_type: treeType })
            });

            const data = await response.json();
            if (data.success) {
                currentTree = data.tree;
                canvas.drawTree(currentTree);
                input.value = '';
            }
        } catch (error) {
            console.error('Error adding node:', error);
        }
    });

    // Tree type change handler
    document.getElementById('treeType').addEventListener('change', async () => {
        document.getElementById('traversalResult').textContent = '';
        canvas.clear();
    });

    // Traversal buttons handler
    document.querySelectorAll('[data-traverse]').forEach(button => {
        button.addEventListener('click', async () => {
            const type = button.dataset.traverse;
            const treeType = document.getElementById('treeType').value;

            try {
                const response = await fetch('/api/traverse', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ type, tree_type: treeType })
                });

                const data = await response.json();
                if (data.success) {
                    document.getElementById('traversalResult').textContent = 
                        `${type.charAt(0).toUpperCase() + type.slice(1)} Traversal: ${data.traversal.join(' → ')}`;
                }
            } catch (error) {
                console.error('Error during traversal:', error);
            }
        });
    });

    // Clear tree button handler
    document.getElementById('clearTree').addEventListener('click', async () => {
        const treeType = document.getElementById('treeType').value;

        try {
            const response = await fetch('/api/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ tree_type: treeType })
            });

            const data = await response.json();
            if (data.success) {
                currentTree = null;
                canvas.clear();
                document.getElementById('traversalResult').textContent = '';
            }
        } catch (error) {
            console.error('Error clearing tree:', error);
        }
    });

    // Handle Enter key in input
    document.getElementById('nodeValue').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            document.getElementById('addNode').click();
        }
    });
});
