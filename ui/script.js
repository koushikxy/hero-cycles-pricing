const componentMap = {
    "Frame": "frame",
    "Handle Bar & Brakes": "brakes",
    "Seating": "seating",
    "Rims": "rims",
    "Tyres": "tyres",
    "Chain Assembly": "gears"
};

const rupees = n => "₹" + n.toLocaleString("en-IN");
const emptyNote = '<p class="empty-note">Select parts to see price</p>';

function localToday() {
    const d = new Date();
    return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

async function populateDropdowns() {
    try {
        const response = await fetch('/api/parts');
        const partCatalog = await response.json();

        for (const [compName, parts] of Object.entries(partCatalog)) {
            const box = document.getElementById(componentMap[compName]);
            if (!box) continue;

            if (box.tagName === "SELECT") {
                box.innerHTML = '<option value="">-- Select a part --</option>';
                for (const [id, name] of Object.entries(parts)) box.add(new Option(name, id));
                box.addEventListener('change', calculatePrice);
            } else {
                box.innerHTML = "";
                for (const [id, name] of Object.entries(parts)) {
                    const label = document.createElement("label");
                    label.innerHTML = `<input type="checkbox" class="part-check" value="${id}"> ${name}`;
                    label.firstChild.addEventListener('change', calculatePrice);
                    box.appendChild(label);
                }
            }
        }
    } catch (error) { console.error("Could not fetch parts:", error); }
}

function setToday() {
    document.getElementById('quote-date').value = localToday();
    calculatePrice();
}

function showEmpty() {
    document.getElementById("receipt-list").innerHTML = emptyNote;
    document.getElementById("grand-total").innerText = rupees(0);
}

function resetForm() {
    document.querySelectorAll(".part-select").forEach(s => s.value = "");
    document.querySelectorAll(".part-check").forEach(c => c.checked = false);
    document.getElementById("error-box").style.display = "none";
    showEmpty();
}

async function calculatePrice() {
    const errorBox = document.getElementById("error-box");
    errorBox.style.display = "none";

    const parts = [
        ...Array.from(document.querySelectorAll(".part-select")).map(s => s.value),
        ...Array.from(document.querySelectorAll(".part-check:checked")).map(c => c.value)
    ].filter(v => v !== "");

    if (parts.length === 0) return showEmpty();

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ date: document.getElementById("quote-date").value, parts })
        });

        const data = await response.json();
        if (!response.ok) {
            errorBox.innerText = data.detail;
            errorBox.style.display = "block";
            return;
        }

        document.getElementById("grand-total").innerText = rupees(data.total);
        document.getElementById("receipt-list").innerHTML = data.items
            .map(item => `<div class="receipt-row"><span>${item.name}:</span><span>${rupees(item.price)}</span></div>`)
            .join("");

    } catch (error) { console.error('Fetch error:', error); }
}

window.addEventListener('DOMContentLoaded', () => {
    populateDropdowns();
    showEmpty();
    const dateInput = document.getElementById('quote-date');
    dateInput.value = localToday();
    dateInput.addEventListener('change', calculatePrice);
});
