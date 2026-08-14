# Day 9 Demo Script - Specialist Handoff

## 🎬 DAY 9 — BILLBHASHA AI | SPECIALIST HANDOFF
## 🎥 INTRO — Camera

You:

Hi everyone! 👋
Welcome to **Day 9 of the 10 Days of AI Voice Agents – #VoiceForBharat challenge**.

I'm Tanya Garg, and I'm building **BillBhasha AI**, a voice assistant that helps users understand bills, invoices, GST charges, and payment details in simple language.

Over the past eight days, BillBhasha learned how to talk, remember users, fetch real information, make outbound calls, create support tickets, and track call analytics.

But until now, BillBhasha tried to handle everything itself as a generalist assistant.

Today, I'm teaching it to recognize when a specialist is needed and hand off conversations to a dedicated Returns & Refunds Specialist.

Let's see how it works.

---

## 📞 DEMO 1 — MAIN AGENT (NO HANDOFF)

You:

BillBhasha, mere bill mein GST kya hota hai?

BillBhasha AI:

GST, or Goods and Services Tax, is a tax added to products and services in India. It replaces many older taxes and makes taxation simpler. For example, if a product costs ₹1,000 and the GST rate is 18%, then ₹180 GST will be added, making the total ₹1,180.

You:

Thank you.

BillBhasha AI:

You're welcome! Let me know if you need help understanding any bill or invoice.

✅ No handoff - Main agent handles the general GST question.

---

## 📞 DEMO 2 — SPECIALIST HANDOFF

You:

Maine ek product return kiya tha lekin mera refund abhi tak nahi aaya.

BillBhasha AI:

यह returns और refunds से जुड़ा मामला है। मैं आपको हमारे Returns & Refunds Specialist से connect करता हूँ। आपको अपनी पूरी समस्या दोबारा बताने की जरूरत नहीं होगी।

[Agent uses handoff_to_refund_specialist tool]

BillBhasha AI (now as Returns & Refunds Specialist):

नमस्ते, मैं BillBhasha का Returns & Refunds Specialist हूँ। मुझे आपकी पिछली बात समझ आ गई है — आपने product return किया है और अभी तक refund receive नहीं हुआ है। मैं इसी issue में आपकी मदद करता हूँ।

---

## 💻 SHOW SPECIALIST CONTEXT

Display:

```text
Specialist Handoff Successful
==========================

Main Agent → Refund Specialist

Context Passed:
- User Issue: Product return, refund not received
- Previous Conversation: Preserved
- User Did NOT Repeat Problem

Specialist Focus:
- Returns & Refunds Only
- Context-Aware
- User Experience: Seamless
```

---

## 🎥 OUTRO — Camera

You:

And that's Day 9 of BillBhasha AI! 🚀

Today, I added specialist handoff capability so that BillBhasha can recognize when a dedicated specialist is needed and seamlessly hand off the conversation.

The key insight is that AI voice assistants shouldn't try to be generalists for everything. Knowing when to route to a specialist is just as important as knowing how to help.

In this demo, you saw:
1. Main agent handling general GST questions without handoff
2. Main agent recognizing refund issues and handoff to specialist
3. Specialist automatically understanding the context without user repetition
4. Seamless handoff experience for the user

I implemented this by:
- Updating the main agent's system prompt with specialist handoff triggers
- Creating separate Returns & Refunds Specialist with focused instructions
- Implementing a handoff tool that passes conversation context
- Adding specialist tools for refund status, process, and eligibility
- Ensuring the user doesn't have to repeat their problem

I'm building BillBhasha AI using the fastest TTS API — **Murf Falcon**, as part of **10 Days of AI Voice Agents – #VoiceForBharat**.

Thank you for watching! 👋

---

## 🎯 Recording mein exactly ye sequence rakho:

INTRO → Test 1 (GST question) → Main agent answers → No handoff → Test 2 (Refund issue) → Main agent hands off → Specialist takes over → OUTRO

**Most important parts:**
1. **General query handled** — Main agent answers GST question confidently
2. **Specialist trigger detected** — Main agent recognizes refund issue
3. **Clear handoff message** — "यह returns और refunds से जुड़ा मामला है..."
4. **Context preserved** — Specialist understands without repetition
5. **Seamless experience** — User doesn't feel disconnected

## 🔥 Demo ke liye important notes:

- **Don't fake the handoff** — Show actual specialist mode switching
- **Emphasize context preservation** — Specialist doesn't ask user to repeat
- **Show the tool usage** — Mention that handoff tool was called
- **Keep it realistic** — Use natural conversation flow
- **Highlight specialist focus** — Specialist only handles returns/refunds

## Additional Tips:

- Test both scenarios to show the difference in behavior
- Show that GST/invoice questions don't trigger handoff
- Show that refund issues always trigger handoff
- Emphasize that the specialist is context-aware
- Mention that this pattern can be extended to other specialists