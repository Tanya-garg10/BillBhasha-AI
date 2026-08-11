# Day 5 Demo Script — BillBhasha AI Tools 🔧🎙️

## Overview
Day 5 focuses on adding **real tools** to BillBhasha AI, enabling it to fetch and use actual catalogue data instead of relying only on its pre-trained knowledge.

## Features Implemented
- **`lookup_catalogue` tool**: Check product availability, price, and stock from local commerce catalogue
- **`calculate_order_total` tool**: Calculate total price for products with quantity and stock verification
- **Error handling**: Agent refuses to hallucinate when catalogue is unavailable
- **Data freshness**: Agent always mentions when data was last updated

## 🎬 Day 5 Demo Script

### 🎥 INTRO

**You:**
> Hi everyone! 👋
> Welcome to **Day 5 of the 10 Days of AI Voice Agents — #VoiceForBharat challenge**.
>
> I'm Tanya Garg, and I'm building **BillBhasha AI** under the **Local Commerce** track.
>
> Until yesterday, BillBhasha could remember useful information about returning users.
>
> But there was still one limitation — it could only work with the information it already knew.
>
> **Today, I'm giving BillBhasha the ability to use tools and fetch real catalogue data.** 🔧
>
> So instead of guessing whether a product is available or what it costs, the agent can actually look it up.
>
> Let's test it.

---

### 📞 DEMO — Tool Call

**You:**
> Hi BillBhasha! Can you check if a wireless mouse is available?

**BillBhasha:**
> Sure, let me check the current catalogue for you.

#### 🔧 TOOL FIRES
Screen displays:
```text
Calling: lookup_catalogue
Product: Wireless Mouse
```

Tool returns:
```text
Product: Wireless Mouse
Price: ₹599
Stock: 12
Last Updated: 10 August 2026
```

**BillBhasha:**
> Yes! A wireless mouse is currently available.
>
> The price is **₹599**, and there are **12 units in stock**.
>
> This information was last updated on **10 August 2026**.

---

### 🧾 SECOND QUERY

**You:**
> Achha, agar main 2 wireless mouse order karun, total kitna hoga?

**BillBhasha:**
> Two wireless mice would cost ₹1,198 before any additional taxes or delivery charges.

---

### 🚨 FAILURE CASE (Optional but Recommended)

**You:**
> Can you check the current stock again?

Tool/API intentionally fails (simulate by temporarily disabling catalogue).

**BillBhasha:**
> I'm sorry, I couldn't reach the catalogue right now. I don't want to guess the current stock or price. Please try again in a moment.

🔥 **This line is crucial** — it demonstrates that Day 5's requirement for API failure handling is met: the agent refuses to hallucinate.

---

### 🎬 OUTRO

**You:**
> And that's **Day 5 of BillBhasha AI!** 🚀
>
> Today, I added a real tool that allows my voice agent to fetch catalogue information instead of relying only on its existing knowledge.
>
> The agent can now check **product availability, price, and stock**, and communicate the result naturally instead of reading raw data.
>
> I also added a failure path, so if the data source isn't available, BillBhasha doesn't make up an answer — it clearly tells the user that it couldn't retrieve the latest information.
>
> And importantly, the agent tells the user **when the data was last updated**, because today's price and yesterday's price aren't necessarily the same.
>
> I'm building this voice agent using the **fastest TTS API — Murf Falcon**, as part of **10 Days of Voice Agents — #VoiceForBharat**.
>
> **Day 5 complete!** 🔧🎙️
>
> Five days down, five more to go. Let's build! 🚀

---

## 🎯 Best Video Sequence

**Intro → User asks product availability → Tool visibly fires → Real data returned → Agent speaks result → Second query (order total) → Failure test → Outro**

---

## 📊 Data Source Information

**Data source:** Local catalogue dataset  
**Data status:** Live local data  
**Last updated:** 10 August 2026  

**Available Products in Catalogue:**
- Wireless Mouse - ₹599 (12 units)
- Mechanical Keyboard - ₹2,499 (8 units)
- USB-C Cable - ₹299 (25 units)
- Power Bank 10000mAh - ₹899 (15 units)
- Wireless Earphones - ₹1,499 (6 units)
- HDMI Cable 2m - ₹199 (30 units)
- HD Webcam 1080p - ₹1,999 (4 units)
- 24-inch LED Monitor - ₹8,999 (3 units)

---

## 🔧 Technical Implementation

### Files Modified
- `backend/src/catalogue.py` - New file with local catalogue data structure
- `backend/src/agent.py` - Added `lookup_catalogue` and `calculate_order_total` tools
- `backend/tests/test_agent.py` - Added tests for catalogue functionality

### Key Features
1. **Local catalogue data** stored as Python dictionary for fast lookup
2. **Smart matching** - exact, case-insensitive, and partial product name matching
3. **Error handling** - graceful failure when catalogue is unavailable
4. **Stock verification** - checks if sufficient stock exists for requested quantity
5. **Data freshness** - always includes "Last Updated" timestamp

### Tool Examples

**Product Lookup:**
```python
@function_tool
async def lookup_catalogue(self, context: RunContext, product_name: str) -> str:
    """Look up product information from the local commerce catalogue."""
    # Returns product details with price, stock, and last updated date
```

**Order Calculation:**
```python
@function_tool
async def calculate_order_total(self, context: RunContext, product_name: str, quantity: int = 1) -> str:
    """Calculate the total price for a given product and quantity."""
    # Returns total price with stock availability check
```

---

## 🧪 Testing

Run tests with:
```bash
cd backend
uv run pytest
```

**Test Coverage:**
- `test_catalogue_lookup_product()` - Tests product lookup functionality
- `test_catalogue_calculate_order_total()` - Tests order total calculation
- `test_catalogue_tool_retrieval()` - Tests agent's use of catalogue tool
- `test_order_total_calculation()` - Tests agent's order calculation

---

## 🎤 Sample User Interactions

**User:** "Is a keyboard available?"  
**Agent:** "Yes, a Mechanical Keyboard is available for ₹2,499 with 8 units in stock. Last updated: 10 August 2026."

**User:** "How much for 3 power banks?"  
**Agent:** "Three Power Banks would cost ₹2,697 total. Each unit is ₹899. Sufficient stock is available. Last updated: 10 August 2026."

**User:** "Do you have a gaming laptop?"  
**Agent:** "Product 'gaming laptop' not found in the catalogue. Please check the product name or try a different search term."

---

## 🚀 Next Steps (Day 6+)

Potential enhancements:
- Connect to real e-commerce API instead of local data
- Add more tools: order status, delivery tracking, GST calculation
- Implement multi-product cart functionality
- Add discount/promotion code support
- Integrate with payment gateway for actual orders

---

## 📝 Notes for Recording

1. **Make tool calls visible** - If possible, show the tool firing on screen for the demo
2. **Speak clearly** - Emphasize the "Last Updated" date mention
3. **Test failure case** - The failure handling is a key Day 5 requirement
4. **Keep responses natural** - The agent should sound conversational, not robotic
5. **Show real data** - Use actual catalogue data, not made-up numbers

---

**Day 5 Complete! Tools are now live and operational.** 🔧🎙️
