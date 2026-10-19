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
    document.getElementById("save-btn").disabled = true;
}

function resetForm() {
    document.querySelectorAll(".part-select").forEach(s => s.value = "");
    document.querySelectorAll(".part-check").forEach(c => c.checked = false);
    document.getElementById("error-box").style.display = "none";
    showEmpty();
}

function selectedParts() {
    return [
        ...Array.from(document.querySelectorAll(".part-select")).map(s => s.value),
        ...Array.from(document.querySelectorAll(".part-check:checked")).map(c => c.value)
    ].filter(v => v !== "");
}

function quoteBody() {
    return JSON.stringify({ date: document.getElementById("quote-date").value, parts: selectedParts() });
}

async function calculatePrice() {
    const errorBox = document.getElementById("error-box");
    const saveBtn = document.getElementById("save-btn");
    errorBox.style.display = "none";
    saveBtn.disabled = true;

    if (selectedParts().length === 0) return showEmpty();

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: quoteBody()
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
        saveBtn.disabled = false;

    } catch (error) { console.error('Fetch error:', error); }
}

async function saveQuote() {
    const response = await fetch('/api/quotes', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: quoteBody()
    });
    const data = await response.json();
    if (response.ok) window.open(`quote.html?id=${data.id}`, "_blank");
    loadRecentQuotes();
}

async function loadRecentQuotes() {
    try {
        const quotes = await (await fetch('/api/quotes')).json();
        document.getElementById("recent-quotes").innerHTML = quotes.length
            ? quotes.slice(0, 5).map(q => `<a class="receipt-row" href="quote.html?id=${q.id}" target="_blank"><span>#${q.id} · ${q.quote_date}</span><span>${rupees(q.total)}</span></a>`).join("")
            : '<p class="empty-note">No saved quotes yet</p>';
    } catch (error) { console.error("Could not load quotes:", error); }
}

window.addEventListener('DOMContentLoaded', () => {
    populateDropdowns();
    loadRecentQuotes();
    showEmpty();
    const dateInput = document.getElementById('quote-date');
    dateInput.value = localToday();
    dateInput.addEventListener('change', calculatePrice);
});
