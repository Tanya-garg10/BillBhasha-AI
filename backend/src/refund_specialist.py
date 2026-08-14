"""
Returns & Refunds Specialist Tools for BillBhasha AI
These are specialist tools that can be used by the main agent for return/refund issues.
"""

import logging
from livekit.agents import function_tool, RunContext

logger = logging.getLogger("refund_specialist")


@function_tool
async def check_refund_status(context: RunContext, order_id: str = None) -> str:
    """Check the status of a refund request.
    
    Use this tool when the user asks about their refund status.
    
    Args:
        order_id: The order ID to check refund status for (optional)
    """
    # This is a placeholder - in a real implementation, this would call a real API
    # For Day 9 demo purposes, we'll provide a helpful response
    
    if order_id:
        return f"मैं order ID {order_id} के लिए refund status check कर रहा हूँ। Current system में exact refund information access नहीं है इसलिए मैं कोई specific status provide नहीं कर सकता। Refund process normally 5-7 business days में complete होता है।"
    else:
        return "मैं आपकी refund status check कर रहा हूँ। Current system में exact refund information access नहीं है इसलिए मैं कोई specific status provide नहीं कर सकता। Refund process normally 5-7 business days में complete होता है।"


@function_tool
async def explain_refund_process(context: RunContext) -> str:
    """Explain the standard refund process to the user.
    
    Use this tool when the user asks about how refunds work.
    """
    return "Standard refund process: 1. Return request के बाद 1-2 business days में return process होता है। 2. Quality check के बाद refund initiation होता है। 3. Payment processing normally 3-5 business days लेता है। 4. Total timeline usually 5-7 business days होता है।"


@function_tool
async def check_return_eligibility(context: RunContext, days_since_purchase: int = None) -> str:
    """Check if a product is eligible for return.
    
    Use this tool when the user asks about return eligibility.
    
    Args:
        days_since_purchase: Number of days since purchase (optional)
    """
    if days_since_purchase is not None:
        if days_since_purchase <= 7:
            return f"आपका product return के लिए eligible है {days_since_purchase} days के बाद। Standard return window 7 days ह।"
        else:
            return f"Standard return window 7 days है {days_since_purchase} days हो चुके हैं, इसलिए return eligibility सीमित हो सकती है। आप customer support से directly contact कर सकते हैं।"
    else:
        return "Standard return window 7 days ह। आप अपने purchase date बता सकते हैं ताकि मैं eligibility check कर सकूँ।"