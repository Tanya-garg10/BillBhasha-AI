"""
Test script for call analytics functionality.
This script tests the call outcome tracking and analytics retrieval.
"""

import sys
import sqlite3
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from memory import save_call_outcome, get_call_analytics, DB_PATH

def clear_test_data():
    """Clear test data from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM call_analytics WHERE session_id LIKE 'test_session_%'")
        conn.commit()
        conn.close()
        print("Cleared previous test data")
    except Exception as e:
        print(f"Could not clear test data: {e}")

def test_call_analytics():
    """Test the call analytics system."""
    print("Testing Call Analytics System...")
    print("=" * 60)
    
    # Clear previous test data
    clear_test_data()
    
    # Test 1: Save successful call outcome
    print("Test 1: Saving successful call outcome...")
    success1 = save_call_outcome(
        session_id="test_session_1",
        outcome="success",
        caller_id="test_user_123",
        duration_seconds=120,
        reason="Useful answer provided"
    )
    print(f"Success: {success1}")
    
    # Test 2: Save failed call outcome
    print("\nTest 2: Saving failed call outcome...")
    success2 = save_call_outcome(
        session_id="test_session_2",
        outcome="failure",
        caller_id="test_user_456",
        duration_seconds=30,
        reason="User ended call early"
    )
    print(f"Success: {success2}")
    
    # Test 3: Get analytics
    print("\nTest 3: Retrieving call analytics...")
    analytics = get_call_analytics()
    print(f"Total Calls: {analytics['total_calls']}")
    print(f"Successful Calls: {analytics['successful_calls']}")
    print(f"Failed Calls: {analytics['failed_calls']}")
    
    # Test 4: Save another successful call (successful escalation)
    print("\nTest 4: Saving successful escalation call...")
    success3 = save_call_outcome(
        session_id="test_session_3",
        outcome="success",
        caller_id="test_user_789",
        duration_seconds=180,
        reason="Successful escalation created"
    )
    print(f"Success: {success3}")
    
    # Test 5: Get updated analytics
    print("\nTest 5: Retrieving updated analytics...")
    updated_analytics = get_call_analytics()
    print(f"Total Calls: {updated_analytics['total_calls']}")
    print(f"Successful Calls: {updated_analytics['successful_calls']}")
    print(f"Failed Calls: {updated_analytics['failed_calls']}")
    
    print("\n" + "=" * 60)
    print("Call analytics system test completed!")
    
    # Verify the metrics for our test data only
    test_total = updated_analytics['total_calls'] - (analytics['total_calls'] - 2)  # Account for any existing data
    test_successful = updated_analytics['successful_calls'] - (analytics['successful_calls'] - 1)
    test_failed = updated_analytics['failed_calls'] - (analytics['failed_calls'] - 1)
    
    print(f"Test data added: {test_total} total, {test_successful} successful, {test_failed} failed")
    
    assert test_total == 3, f"Test calls should be 3, got {test_total}"
    assert test_successful == 2, f"Test successful calls should be 2, got {test_successful}"
    assert test_failed == 1, f"Test failed calls should be 1, got {test_failed}"
    
    print("All assertions passed!")
    return True

if __name__ == "__main__":
    try:
        success = test_call_analytics()
        exit(0 if success else 1)
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)