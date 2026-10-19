# UI Notes & Design Sensibility

**1. What is the most important thing on the configurator screen?**
The most important elements are the "Live Quote" total and the selected Pricing Date. The salesperson's primary goal is to quickly communicate a final price to a customer. By keeping the live calculation pinned to the right side (Dashboard layout), the user always has immediate visibility of the final number without needing to scroll or refresh.

**2. The salesperson uses this 20 times a day. What did you do to make repetitive use fast and easy?**
* **The "Today" Button:** Most quotes are for walk-in customers. Instead of manually navigating a date-picker 20 times a day, the user can click one button to instantly inject today's date.
* **Auto-Calculation:** There is no "Submit" button. The engine listens for changes (`addEventListener('change')`) on the dropdowns and recalculates instantly, saving the user a click every single time they alter a part.
* **Reset Button:** A dedicated, visually distinct button allows the salesperson to clear the form instantly for the next customer.

**3. What happens when a part combination is invalid?**
The frontend prevents silent failures by utilizing the backend's logic. In `engine.py`, the system checks for invalid combinations (like selecting both "Tubeless Tyre" and "Tube") and raises a `ValueError`. The API returns this as an HTTP 400 error. The UI catches this specific error and dynamically displays a red `#error-box` above the receipt, immediately informing the salesperson of the conflict without breaking the application.

**4. Saving and sharing a quote.**
The salesperson often has to hand a written quote to the customer. "Save Quote" stores the quote with the prices for the chosen date and opens a printable page with the parts, prices, pricing date and a quote number. "Download PDF" on that page uses the browser's save-as-PDF, so no extra library is needed. Saved quotes keep their prices even if a price changes later, and the last few show under "Recent Quotes".

**5. One thing I would improve if I had more time.**
The Prices page has no login, so anyone who can open the tool can change a price. In a real showroom I would add staff logins and only let managers add price changes.
