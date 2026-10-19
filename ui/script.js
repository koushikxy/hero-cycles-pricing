const LABELS = { "Rims": "Rims & accessories" };
const MULTI = new Set(["Rims"]);
const CONFLICTS = { tube: "tubeless_tyre", tubeless_tyre: "tube" };

const $ = id => document.getElementById(id);
const rupees = n => "₹" + Math.round(n).toLocaleString("en-IN");
const niceDate = d => new Date(d + "T00:00:00").toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });

let catalog = [];
let requestNo = 0;
const selected = new Set();

function localToday() {
    const d = new Date();
    return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

const priceOn = (part, date) => (part.prices.find(([, from, until]) => from <= date && (!until || date < until)) || [null])[0];
const partName = id => catalog.find(p => p.id === id).name;

function groups() {
    const out = {};
    for (const p of catalog) (out[p.component] ??= []).push(p);
    return out;
}

function renderOptions(focusId) {
    const date = $("quote-date").value;
    $("builder").innerHTML = Object.entries(groups()).map(([comp, parts]) => `
        <fieldset class="group">
            <legend>${LABELS[comp] || comp}<small>${MULTI.has(comp) ? "Pick any" : "Pick one"}</small></legend>
            <div class="options">${parts.map(p => optionHtml(p, comp, date)).join("")}</div>
        </fieldset>`).join("");
    if (focusId) document.querySelector(`#builder input[value="${focusId}"]`)?.focus();
}

function optionHtml(part, comp, date) {
    const price = priceOn(part, date);
    const other = CONFLICTS[part.id];
    const blocked = other && selected.has(other);
    const checked = selected.has(part.id);
    const note = blocked ? `Can't go with ${partName(other)}` : price === null ? "No price on this date" : "";
    return `<label class="option${checked ? " selected" : ""}${blocked ? " blocked" : ""}">
        <input type="${MULTI.has(comp) ? "checkbox" : "radio"}" name="${comp}" value="${part.id}"${checked ? " checked" : ""}${blocked ? " disabled" : ""}>
        <span class="option-name">${part.name}</span>
        <span class="option-price">${price === null ? "-" : rupees(price)}</span>
        ${note ? `<span class="option-note">${note}</span>` : ""}
    </label>`;
}

function choose(input) {
    const part = catalog.find(p => p.id === input.value);
    if (input.type === "radio") {
        const wasOn = selected.has(part.id);
        catalog.filter(p => p.component === part.component).forEach(p => selected.delete(p.id));
        if (!wasOn) selected.add(part.id);
    } else if (selected.has(part.id)) {
        selected.delete(part.id);
    } else {
        selected.add(part.id);
    }
    renderOptions(part.id);
    updateQuote();
}

function setTotal(text) {
    $("grand-total").innerText = text;
    $("mobile-total").innerText = text;
}

function showError(message) {
    $("error-box").innerText = message;
    $("error-box").hidden = false;
    $("lines").innerHTML = "";
    setTotal("-");
}

async function updateQuote() {
    const date = $("quote-date").value;
    const parts = catalog.filter(p => selected.has(p.id)).map(p => p.id);
    const myRequest = ++requestNo;

    $("summary-date").innerText = date ? `Prices as on ${niceDate(date)}` : "Pick a price date";
    $("error-box").hidden = true;
    $("saved-note").hidden = true;
    $("save-btn").disabled = true;

    if (parts.length === 0) {
        $("lines").innerHTML = '<p class="empty-note">Pick parts on the left to build a quote.</p>';
        return setTotal(rupees(0));
    }

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ date, parts })
        });
        const data = await response.json();
        if (myRequest !== requestNo) return;
        if (!response.ok) return showError(data.detail);

        const byComp = {};
        for (const item of data.items) (byComp[item.component] ??= []).push(item);
        $("lines").innerHTML = Object.entries(byComp).map(([comp, items]) => `
            <div class="line-group">
                <div class="line-comp">${LABELS[comp] || comp}</div>
                ${items.map(i => `<div class="line"><span>${i.name}</span><span>${rupees(i.price)}</span></div>`).join("")}
            </div>`).join("");
        setTotal(rupees(data.total));
        $("save-btn").disabled = false;
    } catch (error) {
        if (myRequest === requestNo) showError("Could not reach the server. Try again.");
    }
}

async function saveQuote() {
    const button = $("save-btn");
    button.disabled = true;
    const response = await fetch('/api/quotes', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ date: $("quote-date").value, parts: catalog.filter(p => selected.has(p.id)).map(p => p.id) })
    });
    const data = await response.json();
    if (!response.ok) {
        button.disabled = false;
        return showError(data.detail);
    }
    $("saved-note").innerHTML = `Saved as quote #${data.id}. <a href="quote.html?id=${data.id}">Open to print or download</a>`;
    $("saved-note").hidden = false;
    loadRecentQuotes();
}

async function loadRecentQuotes() {
    try {
        const quotes = await (await fetch('/api/quotes')).json();
        $("recent-quotes").innerHTML = quotes.length
            ? quotes.slice(0, 5).map(q => `<a href="quote.html?id=${q.id}"><strong>#${q.id}</strong><span>${niceDate(q.quote_date)}</span><strong>${rupees(q.total)}</strong></a>`).join("")
            : '<p class="empty-note">No saved quotes yet.</p>';
    } catch (error) { console.error("Could not load quotes:", error); }
}

function onDateChange() {
    renderOptions();
    updateQuote();
}

window.addEventListener('DOMContentLoaded', async () => {
    $("quote-date").value = localToday();
    $("quote-date").addEventListener('change', onDateChange);
    $("today-btn").addEventListener('click', () => { $("quote-date").value = localToday(); onDateChange(); });
    $("clear-btn").addEventListener('click', () => { selected.clear(); renderOptions(); updateQuote(); });
    $("save-btn").addEventListener('click', saveQuote);
    $("builder").addEventListener('click', e => {
        if (e.target.matches('input') && !e.target.disabled) {
            e.preventDefault();
            choose(e.target);
        }
    });

    loadRecentQuotes();
    try {
        catalog = await (await fetch('/api/prices')).json();
        renderOptions();
        updateQuote();
    } catch (error) {
        $("builder").innerHTML = '<p class="empty-note">Could not load parts. Refresh the page.</p>';
    }
});
