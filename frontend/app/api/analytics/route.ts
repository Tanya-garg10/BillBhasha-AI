import { NextResponse } from 'next/server';

// NOTE: This endpoint proxies requests to the backend analytics API
// The backend analytics API runs on port 8001

export async function GET() {
  try {
    // Call the backend analytics API
    const backendUrl = 'http://localhost:8001/api/analytics';
    const response = await fetch(backendUrl);
    
    if (!response.ok) {
      throw new Error(`Backend analytics API returned ${response.status}`);
    }
    
    const analytics = await response.json();
    
    return NextResponse.json(analytics);
  } catch (error) {
    console.error('Error fetching analytics from backend:', error);
    
    // Return fallback data if backend is not available
    return NextResponse.json({
      total_calls: 0,
      successful_calls: 0,
      failed_calls: 0,
      error: 'Backend analytics unavailable'
    });
  }
}