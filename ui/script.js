const componentMap = {
    "Frame": "frame",
    "Handle Bar & Brakes": "brakes",
    "Seating": "seating",
    "Rims": "rims",
    "Tyres": "tyres",
    "Chain Assembly": "gears"
};

async function populateDropdowns() {
    try {
        const response = await fetch('/api/parts');
        const partCatalog = await response.json();

        for (const [compName, parts] of Object.entries(partCatalog)) {
            const selectId = componentMap[compName];
            const select = document.getElementById(selectId);
            
            if (select) {
                select.innerHTML = '<option value="">-- Select a part --</option>';
                for (const [id, name] of Object.entries(parts)) {
                    const opt = document.createElement("option");
                    opt.value = id; 
                    opt.text = name;
                    select.appendChild(opt);
                }
                select.addEventListener('change', calculatePrice);
            }
        }
    } catch (error) { console.error("Could not fetch parts:", error); }
}

function setToday() {
    const dateInput = document.getElementById('quote-date');
    dateInput.value = new Date().toISOString().split('T')[0];
    calculatePrice();
}

// Reset Function
function resetForm() {
    document.querySelectorAll(".part-select").forEach(s => s.value = "");
    document.getElementById("receipt-list").innerHTML = '<p style="color: #888; text-align: center;">Select parts to see price</p>';
    document.getElementById("grand-total").innerText = "₹0";
    document.getElementById("error-box").style.display = "none";
}

async function calculatePrice() {
    const errorBox = document.getElementById("error-box");
    errorBox.style.display = "none";

    const parts = Array.from(document.querySelectorAll(".part-select"))
                       .map(s => s.value)
                       .filter(v => v !== "");

    if (parts.length === 0) {
        document.getElementById("grand-total").innerText = "₹0";
        document.getElementById("receipt-list").innerHTML = '<p style="color: #888; text-align: center;">Select parts to see price</p>';
        return;
    }

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                date: document.getElementById("quote-date").value,
                parts: parts
            })
        });

        const data = await response.json();
        if (!response.ok) {
            errorBox.innerText = data.detail;
            errorBox.style.display = "block";
            return;
        }

        document.getElementById("grand-total").innerText = "₹" + data.total.toFixed(2);
        const list = document.getElementById("receipt-list");
        list.innerHTML = "";
        data.items.forEach(item => {
            list.innerHTML += `<div class="receipt-row"><span>${item.name}:</span><span>₹${item.price}</span></div>`;
        });

    } catch (error) { console.error('Fetch error:', error); }
}

window.addEventListener('DOMContentLoaded', () => {
    populateDropdowns();
    const dateInput = document.getElementById('quote-date');
    if (!dateInput.value) { dateInput.value = new Date().toISOString().split('T')[0]; }
    dateInput.addEventListener('change', calculatePrice);
});