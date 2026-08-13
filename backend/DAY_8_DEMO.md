# Day 8 Demo Script - Call Analytics Dashboard

## 🎬 DAY 8 — BILLBHASHA AI | CALL ANALYTICS DASHBOARD
## 🎥 INTRO — Camera

You:

Hi everyone! 👋
Welcome to **Day 8 of the 10 Days of AI Voice Agents – #VoiceForBharat challenge**.

I'm Tanya Garg, and I'm building **BillBhasha AI**, a voice assistant that helps users understand bills, invoices, GST charges, and payment details in simple language.

Over the past seven days, BillBhasha learned how to talk, remember users, fetch real information, make outbound calls, and even create support tickets for complex issues.

But until now, I had no way to measure how well BillBhasha is actually performing.

Today, I added a Call Analytics Dashboard that tracks real call performance metrics from actual call data.

Let's see how it works.

---

## 📞 DEMO 1 – SUCCESSFUL CALL

You:

Hi BillBhasha, what is GST?

BillBhasha AI:

GST, or Goods and Services Tax, is a tax added to products and services in India. It replaces many older taxes and makes taxation simpler.

You:

Thank you.

BillBhasha AI:

You're welcome! Let me know if you need help understanding any bill or invoice.

[Call ends]

---

## 💻 SHOW DASHBOARD UPDATE

Display:

```text
Call Analytics Dashboard
=======================

Total Calls: 1
Successful Calls: 1
Failed Calls: 0

Success Rate: 100%
```

---

## 📞 DEMO 2 – FAILED CALL

You:

Hi BillBhasha, can you check my payment status?

BillBhasha AI:

माफ़ कीजिए, मैं अभी payment status की information retrieve नहीं कर पा रहा हूँ। मैं गलत information guess नहीं करना चाहता। कृपया थोड़ी देर बाद फिर try करें।

[User ends call immediately]

---

## 💻 SHOW DASHBOARD UPDATE

Display:

```text
Call Analytics Dashboard
=======================

Total Calls: 2
Successful Calls: 1
Failed Calls: 1

Success Rate: 50%
```

---

## 📞 DEMO 3 – SUCCESSFUL ESCALATION

You:

I haven't received my refund yet.

BillBhasha AI:

I'm sorry to hear that. Refund disputes may require support from a human representative. I can create a support request for you and share only the necessary details. Would you like me to proceed?

You:

Yes.

BillBhasha AI:

Thank you. I will share: Your name, Issue type: Refund dispute, Preferred language, Urgency level. No payment passwords, OTPs, PINs, or sensitive information will be shared. Shall I create the request?

You:

Yes.

BillBhasha AI:

Your support request has been created successfully. Reference ID: BB-2045. A support representative may contact you soon through your preferred method. Please keep this reference number for future communication.

[Call ends]

---

## 💻 SHOW DASHBOARD UPDATE

Display:

```text
Call Analytics Dashboard
=======================

Total Calls: 3
Successful Calls: 2
Failed Calls: 1

Success Rate: 67%
```

---

## 🎥 OUTRO — Camera

You:

And that's Day 8 of BillBhasha AI! 🚀

Today, I added a Call Analytics Dashboard that tracks real call performance metrics from actual call data.

The dashboard shows:

✅ **Total Calls** — Complete count of all processed calls
✅ **Successful Calls** — Calls where users got useful answers or successful escalations
✅ **Failed Calls** — Calls that ended early, had tool failures, or incomplete requests
✅ **Success Rate** — Percentage of successful calls

The key insight is that real call analytics are essential for:
- Measuring AI performance and effectiveness
- Identifying patterns in user interactions
- Optimizing system prompts and responses
- Making data-driven improvements

I implemented this by:
- Extending the existing Day 4 database with call analytics table
- Adding automatic call outcome tracking when sessions end
- Creating a Flask API to serve analytics data
- Building a clean dashboard UI component
- Adding navigation to access the dashboard

I'm building BillBhasha AI using the fastest TTS API — **Murf Falcon**, as part of **10 Days of AI Voice Agents – #VoiceForBharat**.

Thank you for watching! 👋

---

## 🎯 Recording mein exactly ye sequence rakho:

INTRO → Successful call → Dashboard shows 1 total, 1 successful → Failed call → Dashboard shows 2 total, 1 successful, 1 failed → Successful escalation → Dashboard shows 3 total, 2 successful, 1 failed → OUTRO

**Most important parts:**
1. **Real database integration** — Show that data is actually stored in the database
2. **Automatic tracking** — Calls are tracked automatically when they end
3. **Real-time updates** — Dashboard updates as calls complete
4. **Clean dashboard UI** — Simple, focused on the three required metrics
5. **No hardcoded numbers** — All metrics come from actual call data

## 🔥 Demo ke liye important notes:

- **Show the database file** — Briefly show that data is actually stored in billbhasha.db
- **Emphasize automatic tracking** — Call outcomes are saved automatically, no manual entry
- **Show the API working** — Mention that Flask API serves the data to the dashboard
- **Real-time updates** — Dashboard refreshes every 30 seconds automatically
- **Privacy focus** — Emphasize that no sensitive data is stored

## Additional Tips:

- Show the database file location briefly: backend/src/billbhasha.db
- Mention that the system tracks useful answers and successful escalations
- Highlight that the dashboard is simple and clean, not cluttered
- Show that the metrics are calculated from actual stored call records