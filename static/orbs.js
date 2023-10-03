const canvas = document.getElementById("orbCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const orbs = [];

class Orb {
    constructor(x, y, radius, color) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;
        this.velocity = {
            x: (Math.random() - 0.5) * 5,
            y: (Math.random() - 0.5) * 5
        };
    }

    draw() {
        const aspectRatio = canvas.width / canvas.height;
        ctx.beginPath();
        ctx.ellipse(this.x, this.y, this.radius, this.radius / aspectRatio, 0, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.filter = "blur(60px)";
    }

    update() {
        this.x += this.velocity.x;
        this.y += this.velocity.y;

        if (this.x + this.radius > canvas.width || this.x - this.radius < 0) {
            this.velocity.x = -this.velocity.x;
        }

        if (this.y + this.radius > canvas.height || this.y - this.radius < 0) {
            this.velocity.y = -this.velocity.y;
        }

        this.draw();
    }
}

function init() {
    for (let i = 0; i < 3; i++) {
        // generate a random radius between 100 and 200
        const radius = 300;
        const x = Math.random() * (canvas.width - radius * 2) + radius;
        const y = Math.random() * (canvas.height - radius * 2) + radius;
        const color = `rgb(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255})`;
        orbs.push(new Orb(x, y, radius, color));
    }
}

function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    orbs.forEach(orb => {
        orb.update();
    });

    // add a timer to stop the animation
    setTimeout(function () {
        cancelAnimationFrame(animate);
    }, 60 * 1000);
}

window.addEventListener("resize", () => {
    orbs = [];
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    init();
});

init();
animate();