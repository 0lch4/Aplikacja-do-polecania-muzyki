function initializeLights(width) {
    const container = document.getElementById('lights-container');

    for (let i = 0; i < 25; i++) {
        const light = document.createElement('div');
        light.className = 'light';
        light.style.left = Math.random() * width + 'vw';
        light.style.top = Math.random() * 100 + 'vh';
        light.style.animationDelay = Math.random() * 5 + 's';
        container.appendChild(light);
    }
}
