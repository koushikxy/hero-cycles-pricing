# Problem Breakdown & Data Model

## Part 1: Problem Breakdown

**1. Who is using this?**
The primary user is a cycle showroom salesperson, not a software engineer. 
* **What she needs:** She needs a tool that is lightning-fast, visually clear, and requires zero technical knowledge to operate. She needs to confidently quote a price to a customer standing right in front of her. 
* **What would frustrate her:** Having to type out exact part IDs manually, dealing with complex error messages, waiting for slow calculations, or navigating a cluttered interface. 

**2. What makes this problem tricky?**
The core complexity is **time-sensitive pricing**. Prices are not static; they exist on a timeline. A single part can have multiple correct prices depending entirely on the context of the quote date. 

*Specific edge cases this creates:*
1. **The Boundary Condition:** A quote requested exactly on the day a price changes (e.g., December 1, 2016). The engine must have strict inclusive/exclusive logic (`>=` vs `<`) to avoid returning two prices or crashing.
2. **The "Part Didn't Exist" Case:** Quoting a cycle for a date in 2010, but the customer wants a part that wasn't added to the catalog until 2015. 
3. **The Missing Data Gap:** A scenario where the database has a price valid until Nov 2016, and the next price doesn't start until Jan 2017, leaving a blank gap for December where the engine might fail to find any price at all.

**3. What is your plan?**
* **Representing Parts & Prices:** I will represent each cycle part as an object. Instead of storing a single static price, each part will hold a list of historical price records. Each record represents a time window with a start date, an end date, and the specific price during that window.
* **Handling Price Changes:** When the engine receives a quote request via JSON, it will iterate through the selected part's price history. It will evaluate the requested date against the start/end bounds of each historical record and lock in the price where the date falls within the active window.
* **Structuring Output:** The engine will aggregate the individual part prices, group them by their high-level component categories (Frame, Wheels, etc.), and print a formatted receipt to the console.

---

## Part 2a: Data Model First

**1. Core Entities**

* **`PriceEntry`**
    * `valid_from`: date
    * `valid_until`: date | null (null indicates this is the currently active price)
    * `price`: float

* **`Part`**
    * `id`: string (Unique identifier, e.g., "tubeless_tyre")
    * `name`: string (Display name, e.g., "Tubeless Tyre")
    * `component`: string (High-level grouping, e.g., "Wheels")
    * `price_history`: List<PriceEntry>

* **`CycleConfiguration` (The Quote Request)**
    * `config_date`: date
    * `parts`: List<string> (List of part IDs)

**2. Entity Relationships**
* A `CycleConfiguration` contains many `Part` IDs.
* A `Part` belongs to exactly one `Component` category.
* A `Part` has a one-to-many relationship with `PriceEntry` (one part has many historical prices over time).

**3. Design Decision: Time-Sensitive Pricing Approach**
I chose to model the pricing using **Valid From / Valid Until date ranges** attached directly to the Part object. 

*Why?* The alternative would be creating a daily snapshot of prices or a massive standalone price ledger. Storing a list of time windows directly inside the Part entity minimizes data duplication and makes querying highly efficient. To find a price, the engine only needs to check a tiny list of 2 or 3 date ranges for that specific part, rather than scanning a massive, global database of all historical price changes.