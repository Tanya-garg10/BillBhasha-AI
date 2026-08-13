# Call Analytics Dashboard Setup - Day 8

This document explains the call analytics dashboard implementation for BillBhasha AI.

## Overview

The call analytics dashboard tracks real call performance metrics and displays them in a simple, clean interface. It uses the existing Day 4 database infrastructure and extends it with call outcome tracking.

## Architecture

### Database Layer (backend/src/memory.py)
- Extended existing SQLite database with `call_analytics` table
- Added `save_call_outcome()` function to store call results
- Added `get_call_analytics()` function to retrieve metrics
- Preserves existing Day 4 caller_profiles functionality

### Agent Layer (backend/src/agent.py)
- Added call outcome tracking in agent session lifecycle
- Tracks when useful answers are provided (`mark_successful_interaction()`)
- Tracks when successful escalations occur (`mark_successful_escalation()`)
- Automatically saves call outcomes when sessions end
- Success condition: useful answer OR successful escalation
- Failure condition: early termination, tool failure, incomplete request

### API Layer (backend/src/analytics_api.py)
- Flask API server on port 8001
- `/api/analytics` endpoint returns the three required metrics
- CORS enabled for frontend access
- Simple and lightweight, minimal dependencies

### Frontend Layer
- **API route** (frontend/app/api/analytics/route.ts): Proxies requests to backend API
- **Dashboard component** (frontend/components/app/dashboard.tsx): Clean UI showing the three metrics
- **Dashboard page** (frontend/app/dashboard/page.tsx): Dashboard page route
- **Navigation** (frontend/components/app/welcome-view.tsx): Link to dashboard on welcome screen

## Database Schema

### call_analytics table
```sql
CREATE TABLE call_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    caller_id TEXT,
    outcome TEXT NOT NULL,  -- "success" or "failure"
    timestamp TEXT NOT NULL,
    duration_seconds INTEGER,
    reason TEXT
)
```

## Success Conditions

### Call is SUCCESSFUL when:
- User gets a useful answer to a bill, GST, invoice, or payment-related query
- OR a required human escalation is successfully created

### Call is FAILED when:
- User ends the call before task completion
- Unresolved tool/API failure occurs
- Agent fails to complete the user's request

## Running the Analytics API

Start the analytics API server:
```bash
cd backend
uv run python src/analytics_api.py
```

The API will run on http://localhost:8001

## Accessing the Dashboard

1. Start the analytics API server
2. Start the frontend: `cd frontend && pnpm dev`
3. Navigate to http://localhost:3000/dashboard
4. Dashboard will show the three required metrics

## Privacy & Security

- **No sensitive data stored**: Only session_id, outcome, timestamp, duration, caller_id
- **No phone numbers**: No phone numbers, OTPs, PINs, or account numbers stored
- **No transcripts**: Full conversation transcripts are not stored
- **Anonymous tracking**: Uses session IDs instead of personal identifiers
- **Clean data**: Only stores what's needed for analytics

## Testing

Run the test script:
```bash
cd backend
uv run python test_call_analytics.py
```

This tests:
- Call outcome saving
- Analytics retrieval
- Database operations
- Success/failure logic

## File Changes Summary

**Modified Files:**
- `backend/src/memory.py` — Added call analytics table and functions
- `backend/src/agent.py` — Added call outcome tracking
- `backend/pyproject.toml` — Added Flask dependencies
- `frontend/components/app/welcome-view.tsx` — Added dashboard link

**New Files:**
- `backend/src/analytics_api.py` — Flask API server
- `backend/test_call_analytics.py` — Test script
- `frontend/app/api/analytics/route.ts` — Analytics API proxy
- `frontend/app/dashboard/page.tsx` — Dashboard page
- `frontend/components/app/dashboard.tsx` — Dashboard component
- `backend/DAY_8_LINKEDIN.md` — LinkedIn post
- `backend/DAY_8_DEMO.md` — Demo script

## Integration with Existing Functionality

All Day 1-7 functionality is preserved:
- ✅ Voice AI pipeline (Day 1)
- ✅ System prompts and role (Day 2)
- ✅ Frontend personalization (Day 3)
- ✅ Caller memory (Day 4) — Extended with analytics
- ✅ Tools and catalogue (Day 5)
- ✅ Outbound calling (Day 6)
- ✅ Human escalation/support tickets (Day 7)

The analytics system adds monitoring without affecting existing features.