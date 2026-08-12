# Day 7 Demo Script - Human Handoff

## 🎬 DAY 7 — BILLBHASHA AI | HUMAN HANDOFF
## 🎥 INTRO — Camera

You:

Hi everyone! 👋
I'm Tanya Garg, and this is Day 7 of my 10 Days of AI Voice Agents journey — #VoiceForBharat.

I'm building BillBhasha AI, a voice-first assistant that helps users understand bills, GST, taxes, invoices, payments, and product-related information in simple Hindi or Hinglish.

Over the last six days, I've taught BillBhasha how to talk, follow its role and boundaries, use a personalised frontend, remember users, use tools to fetch information, and make outbound calls.

But until now, BillBhasha tried to handle everything itself — even when it couldn't or shouldn't.

Today, BillBhasha knows when to ask for help. 🧑‍💼

For today's demo, I'll show three scenarios:
1. Normal question → BillBhasha handles it
2. Complex issue → BillBhasha refuses to guess
3. Human escalation → Seamless handoff to human support

## 🧠 SCENARIO 1: NORMAL QUESTION
📞 Call starts

BillBhasha:

नमस्ते Tanya! मैं BillBhasha AI से बोल रहा हूँ। यह आपके recent bill और payment details के बारे में एक quick update के लिए call है।
अगर आप ऐसे calls receive नहीं करना चाहतीं, तो आप कभी भी कह सकती हैं, "Please don't call me again."
क्या अभी बात करने का सही समय है?

You:

हाँ, बताइए।

BillBhasha:

धन्यवाद। आपके recent invoice में product amount ₹1,000 है और उस पर ₹180 GST लगाया गया है।
आपका total bill amount ₹1,180 है।

You:

GST rate kya hai?

BillBhasha:

इस invoice पर GST rate 18% है। ₹1,000 के taxable amount का 18% ₹180 होता है।
इसलिए ₹1,000 plus ₹180 GST मिलाकर total ₹1,180 होता है।

## 🚫 SCENARIO 2: COMPLEX ISSUE — AI REFUSES TO GUESS
You:

Achha, payment date kab hai?

BillBhasha:

माफ़ कीजिए, मैं अभी payment date की information retrieve नहीं कर पा रहा हूँ।
मैं गलत information guess नहीं करना चाहता। कृपया थोड़ी देर बाद फिर try करें या हमारे support team से संपर्क करें।

## 🧑‍💼 SCENARIO 3: HUMAN ESCALATION
You:

Actually, mere bill mein ek charge hai jo mujhe bilkul samajh nahi aa raha. Ek ₹500 ka charge hai jo mujhe lagta hai galat hai. Mujhe human se baat karni hai.

BillBhasha:

I understand. Since this may require checking your account or billing records, I don't want to guess or give you incorrect information. I can connect you with a human support representative. Would you like me to do that?

You:

Yes, please.

BillBhasha:

Sure. I'm escalating this conversation to human support. Please stay on the line while I arrange the handoff. A human support representative will be with you shortly.

## 🔔 HUMAN SUPPORT NOTIFICATION
(Show screen/discord notification)

You:

देखिए, human support को notification आ गया है। यहाँ पर escalation details हैं:
- Caller ID: Tanya
- Reason: Billing dispute
- Room: live room details
- Timestamp: current time

यह billbhasha ne automatically human support ko notify kar diya hai.

## 🎥 OUTRO — Camera

You:

And that's Day 7 of BillBhasha AI! 🚀

Today, I added human handoff capability, so BillBhasha can recognize when it cannot handle a request and seamlessly escalate to human support.

In this demo, you saw:
1. BillBhasha handling normal questions confidently
2. BillBhasha refusing to guess when it doesn't have information
3. BillBhasha recognizing when human support is needed and escalating appropriately

The key insight is that AI voice assistants shouldn't try to handle everything. Knowing when to escalate is just as important as knowing how to help.

I also implemented a notification system that can send alerts to human support via webhooks, Discord, or Slack — so human agents get the context they need to help the user.

I'm building BillBhasha using Murf Falcon, the fastest TTS API, as part of 10 Days of Voice Agents — #VoiceForBharat.

Day 7 complete! 🧑‍💼🎙️
Seven days down, three more to go. Let's keep building! 🚀

Thank you for watching! 👋

## 🎯 Recording mein exactly ye sequence rakho:

INTRO → Call starts → Normal question → AI answers → Complex question → AI refuses → User asks for human → AI escalates → Human support notification shown → OUTRO

**Most important parts:**
1. **AI refusing to guess** — "मैं गलत information guess नहीं करना चाहता"
2. **Escalation consent** — "Would you like me to connect you with human support?"
3. **Human notification** — Show the actual notification going to human support
4. **Clear handoff message** — "I'm escalating this conversation to human support"

## 🔥 Demo ke liye important notes:

- **Actual human transfer setup karna difficult ho**, toh Discord/webhook notification ko hi escalation destination dikhao
- **Screen recording mein clearly dikhana** ki notification human support ko gaya
- **Audio mein clearly sunna** ki agent ne escalation kiya
- **Don't fake** the escalation — show actual notification system working

## Additional Tips:

- Agar tumhare paas actual human support system nahi hai, toh Discord webhook setup karo (free hai)
- Demo mein notification screen ko zoom karke dikhana
- Background mein tumhara Discord/Slack open rakhna taaki notification real dikhe
- Escalation ke baad agent ka final message clearly sunna: "I'm escalating this conversation to human support..."