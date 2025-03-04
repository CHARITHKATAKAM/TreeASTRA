class TreeCanvas {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.nodeRadius = 20;
        this.levelHeight = 60;
        this.initCanvas();

        window.addEventListener('resize', () => this.initCanvas());
    }

    initCanvas() {
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
    }

    clear() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    drawNode(x, y, value, color = null) {
        this.ctx.beginPath();
        this.ctx.arc(x, y, this.nodeRadius, 0, Math.PI * 2);

        // Handle different node colors for Red-Black trees
        if (color === 'RED') {
            this.ctx.fillStyle = '#dc3545';  // Bootstrap danger color
        } else if (color === 'BLACK') {
            this.ctx.fillStyle = '#212529';  // Bootstrap dark color
        } else {
            this.ctx.fillStyle = '#2b3035';  // Default node color
        }

        this.ctx.fill();
        this.ctx.strokeStyle = '#6c757d';
        this.ctx.stroke();

        this.ctx.fillStyle = '#fff';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.font = '14px Arial';
        this.ctx.fillText(value, x, y);
    }

    drawEdge(startX, startY, endX, endY) {
        this.ctx.beginPath();
        this.ctx.moveTo(startX, startY);
        this.ctx.lineTo(endX, endY);
        this.ctx.strokeStyle = '#6c757d';
        this.ctx.stroke();
    }

    drawTree(root) {
        this.clear();
        if (!root) return;

        const drawNode = (node, x, y, level, maxWidth) => {
            if (!node) return;

            const offset = maxWidth / Math.pow(2, level + 1);

            if (node.left) {
                this.drawEdge(x, y, x - offset, y + this.levelHeight);
                drawNode(node.left, x - offset, y + this.levelHeight, level + 1, maxWidth);
            }

            if (node.right) {
                this.drawEdge(x, y, x + offset, y + this.levelHeight);
                drawNode(node.right, x + offset, y + this.levelHeight, level + 1, maxWidth);
            }

            this.drawNode(x, y, node.value, node.color);
        };

        const startX = this.canvas.width / 2;
        const startY = 40;
        drawNode(root, startX, startY, 0, this.canvas.width / 2);
    }
}