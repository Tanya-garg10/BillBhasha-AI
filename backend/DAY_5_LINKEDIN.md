# LinkedIn Post — Day 5: Tools 🔧🎙️

---

**Day 5 of #VoiceForBharat: Giving BillBhasha AI the power to take real action with tools!**

Until yesterday, my voice agent BillBhasha could remember user preferences across sessions — but it was still limited to its pre-trained knowledge. It couldn't actually fetch real information or perform actions.

**Today, that changed.** 🔧

I've integrated **real tools** into BillBhasha AI, enabling it to:

✅ **Check product availability** from a local commerce catalogue  
✅ **Look up real prices and stock levels**  
✅ **Calculate order totals** with quantity and stock verification  
✅ **Handle failures gracefully** — no hallucination when data is unavailable  
✅ **Always mention data freshness** — "Last updated: 10 August 2026"

Now when a user asks "Is a wireless mouse available?", BillBhasha doesn't guess — it actually looks up the catalogue and responds with real data:

"Yes! A wireless mouse is available for ₹599 with 12 units in stock. This information was last updated on 10 August 2026."

**The key difference:** Yesterday, the agent could only work with what it already knew. Today, it can fetch and use real data from tools.

**Built with:**
- LiveKit Agents SDK for voice pipeline
- Murf Falcon TTS for natural speech
- Local catalogue data structure for fast lookups
- Error handling to prevent hallucination

**Day 5 complete!** Five days down, five more to go in the #VoiceForBharat challenge. 🚀

#VoiceAI #LocalCommerce #MurfFalcon #LiveKit #BuildInPublic #AIAgents #VoiceAssistants #IndiaTech

---

## 🎥 Demo Video Script Highlights

**INTRO:** "Until yesterday, BillBhasha could remember useful information about returning users. But there was still one limitation — it could only work with the information it already knew. Today, I'm giving BillBhasha the ability to use tools and fetch real catalogue data."

**DEMO:** User asks "Is a wireless mouse available?" → Tool fires → Real data returned → Agent speaks result with price, stock, and last updated date.

**FAILURE TEST:** "I'm sorry, I couldn't reach the catalogue right now. I don't want to guess the current stock or price. Please try again in a moment."

**OUTRO:** "The agent can now check product availability, price, and stock, and communicate the result naturally instead of reading raw data. And importantly, the agent tells the user when the data was last updated."

---

## 🔧 Technical Implementation

**Tools Added:**
- `lookup_catalogue` — Check product availability, price, stock
- `calculate_order_total` — Calculate totals with stock verification

**Key Features:**
- Local catalogue data structure (8 products)
- Smart matching (exact, case-insensitive, partial)
- Error handling with no hallucination
- Data freshness tracking
- Stock availability verification

**Files Modified:**
- `backend/src/catalogue.py` — New catalogue data
- `backend/src/agent.py` — Tool implementations
- `backend/tests/test_agent.py` — Comprehensive tests

---

## 📊 Day 5 Metrics

- **2 tools implemented:** lookup_catalogue, calculate_order_total
- **8 products in catalogue:** From ₹199 to ₹8,999
- **4 test cases added:** Unit + integration tests
- **Error handling:** Graceful failure, no hallucination
- **Data freshness:** Always mentioned in responses

---

## 🎯 What Makes This Special

1. **Real Action, Not Just Talk** — Agent actually fetches data, doesn't guess
2. **Data Freshness** — Users know when information was last updated
3. **Error Resilience** — Fails gracefully instead of making things up
4. **Natural Speech** — Communicates data in conversational language
5. **Stock Awareness** — Checks availability before confirming orders

---

## 🚀 Ready for Day 6!

Tomorrow, I'll be adding even more capabilities to BillBhasha AI. The foundation is solid — tools are working, error handling is in place, and the agent can genuinely help with local commerce queries.

**Five days down, five more to go!** Let's build! 🚀

#VoiceForBharat #10DaysOfVoiceAgents #BillBhashaAI