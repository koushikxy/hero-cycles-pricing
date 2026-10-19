# UI Notes & Design Sensibility

Before the redesign I looked at Apple's Mac configurator, which shows the price on every option card and marks the chosen one with a strong border, and kept the total in one fixed place the way checkout screens do. I used plain neutrals with one dark colour for actions, and Hero's red only as a small mark next to the name.

**1. What is the most important thing on the configurator screen?**
The total. It sits in a quote panel that stays on screen while you scroll on a laptop, and in a bar fixed to the bottom on a phone, so the salesperson never loses it while picking parts. The price date sits in the top bar because every number on the page depends on it.

**2. The salesperson uses this 20 times a day. What did you do to make repetitive use fast and easy?**
- Every part is a card that shows its price for the chosen date, so comparing a steel and aluminium frame takes one glance instead of picking each one.
- One click picks a part and clicking it again removes it. There is no submit button; the quote updates on every change.
- The quote panel groups parts by component, the same way the printed quote does.
- "Today" resets the price date in one click, and "Clear all" starts the next customer.
- "Save quote" stores it and gives a link to a printable page, and the last five quotes are one click away.

**3. What happens when a part combination is invalid?**
It is stopped before it happens. Once a tubeless tyre is picked, the Tube card greys out with "Can't go with Tubeless Tyre" (and the other way round). If a quote still fails, for example a date before the price list starts, the server's message shows in red in the quote panel, the total shows "-" instead of an old number, and Save is turned off so a wrong price can't be saved.

**4. Saving and sharing a quote.**
The salesperson often has to hand a written quote to the customer. "Save Quote" stores the quote with the prices for the chosen date. Its page shows the parts, prices, pricing date and a quote number, and "Download PDF" uses the browser's save-as-PDF, so no extra library is needed. Saved quotes keep their prices even if a price changes later.

**5. The Prices page.**
Each part shows today's price and its next planned change, with the full history folded away. Search and component filters keep the list short, and "Change price" on any row fills in the form above.

**6. One thing I would improve if I had more time.**
The Prices page has no login, so anyone who can open the tool can change a price. In a real showroom I would add staff logins and only let managers add price changes.
