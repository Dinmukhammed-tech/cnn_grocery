function previewImage(event) {
    const file = event.target.files[0];
    if (!file) return;

    const preview = document.getElementById('preview');
    preview.src = URL.createObjectURL(file);
    preview.style.display = 'block';
    document.getElementById('detectBtn').disabled = false;
    document.getElementById('results').style.display = 'none';
}

async function detect() {
    const file = document.getElementById('fileInput').files[0];
    if (!file) return;

    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('detectBtn').disabled = true;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/detect', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        document.getElementById('loading').style.display = 'none';
        document.getElementById('results').style.display = 'block';
        document.getElementById('detectBtn').disabled = false;

        const productsList = document.getElementById('productsList');
        productsList.innerHTML = '';

        data.products.forEach(p => {
            productsList.innerHTML += `
                <div class="product-card">
                    <div>
                        <div class="product-name">${p.name}</div>
                        <div class="product-conf">Confidence: ${p.confidence}%</div>
                    </div>
                    <div class="product-price">$${p.price.toFixed(2)}</div>
                </div>`;
        });

        document.getElementById('totalPrice').textContent =
            `$${data.total_price.toFixed(2)}`;
        document.getElementById('productCount').textContent =
            `${data.count} product(s) detected`;

    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('detectBtn').disabled = false;
        alert('Error: ' + error.message);
    }
}