'use client';

import { useEffect, useState } from 'react';

interface AnalyticsData {
  total_calls: number;
  successful_calls: number;
  failed_calls: number;
}

export function Dashboard() {
  const [analytics, setAnalytics] = useState<AnalyticsData>({
    total_calls: 0,
    successful_calls: 0,
    failed_calls: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchAnalytics() {
      try {
        const response = await fetch('/api/analytics');
        if (!response.ok) {
          throw new Error('Failed to fetch analytics');
        }
        const data = await response.json();
        setAnalytics(data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load analytics data');
        setLoading(false);
      }
    }

    fetchAnalytics();
    // Refresh analytics every 30 seconds
    const interval = setInterval(fetchAnalytics, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[200px]">
        <div className="text-gray-500">Loading analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[200px]">
        <div className="text-red-500">{error}</div>
      </div>
    );
  }

  const successRate = analytics.total_calls > 0 
    ? Math.round((analytics.successful_calls / analytics.total_calls) * 100)
    : 0;

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900">Call Analytics Dashboard</h2>
        <p className="text-gray-600 mt-1">Real-time call performance metrics</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Total Calls */}
        <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
          <div className="text-sm font-medium text-gray-500 mb-2">Total Calls</div>
          <div className="text-4xl font-bold text-gray-900">{analytics.total_calls}</div>
        </div>

        {/* Successful Calls */}
        <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
          <div className="text-sm font-medium text-gray-500 mb-2">Successful Calls</div>
          <div className="text-4xl font-bold text-green-600">{analytics.successful_calls}</div>
        </div>

        {/* Failed Calls */}
        <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
          <div className="text-sm font-medium text-gray-500 mb-2">Failed Calls</div>
          <div className="text-4xl font-bold text-red-600">{analytics.failed_calls}</div>
        </div>
      </div>

      {/* Success Rate */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm font-medium text-gray-500 mb-1">Success Rate</div>
            <div className="text-2xl font-bold text-gray-900">{successRate}%</div>
          </div>
          <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className="h-full bg-green-500 transition-all duration-500"
              style={{ width: `${successRate}%` }}
            />
          </div>
        </div>
      </div>

      {/* Last Updated */}
      <div className="text-center text-sm text-gray-500">
        Analytics refresh automatically every 30 seconds
      </div>
    </div>
  );
}