# UI Notes & Design Sensibility

**1. What is the most important thing on the configurator screen?**
The most important elements are the "Live Quote" total and the selected Pricing Date. The salesperson's primary goal is to quickly communicate a final price to a customer. By keeping the live calculation pinned to the right side (Dashboard layout), the user always has immediate visibility of the final number without needing to scroll or refresh.

**2. The salesperson uses this 20 times a day. What did you do to make repetitive use fast and easy?**
* **The "Today" Button:** Most quotes are for walk-in customers. Instead of manually navigating a date-picker 20 times a day, the user can click one button to instantly inject today's date.
* **Auto-Calculation:** There is no "Submit" button. The engine listens for changes (`addEventListener('change')`) on the dropdowns and recalculates instantly, saving the user a click every single time they alter a part.
* **Reset Button:** A dedicated, visually distinct button allows the salesperson to clear the form instantly for the next customer.

**3. What happens when a part combination is invalid?**
The frontend prevents silent failures by utilizing the backend's logic. In `engine.py`, the system checks for invalid combinations (like selecting both "Tubeless Tyre" and "Tube") and raises a `ValueError`. The API returns this as an HTTP 400 error. The UI catches this specific error and dynamically displays a red `#error-box` above the receipt, immediately informing the salesperson of the conflict without breaking the application.

**4. One thing you would improve if you had more time.**
A quote export feature. The salesperson often needs to hand a written quote to a customer or email it to them. Right now the price is only visible on-screen. I would add a "Generate Quote PDF" button that produces a simple printable document with the cycle configuration, itemised prices, the pricing date, and a quote reference number. This closes the gap between the digital tool and the physical sales workflow.