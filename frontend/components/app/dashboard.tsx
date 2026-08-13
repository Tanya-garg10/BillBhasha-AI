'use client';

import { useEffect, useState } from 'react';
import { motion } from 'motion/react';
import Link from 'next/link';
import { Navigation } from './navigation';
import { MobileNavigation } from './mobile-navigation';

interface AnalyticsData {
  total_calls: number;
  successful_calls: number;
  failed_calls: number;
}

interface RecentActivity {
  id: string;
  type: 'success' | 'escalation' | 'failure';
  timestamp: string;
  duration?: number;
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
    const interval = setInterval(fetchAnalytics, 30000);
    return () => clearInterval(interval);
  }, []);

  const successRate = analytics.total_calls > 0 
    ? Math.round((analytics.successful_calls / analytics.total_calls) * 100)
    : 0;

  const metricCards = [
    {
      title: 'Total Calls',
      value: analytics.total_calls,
      icon: '📞',
      color: 'from-blue-500 to-cyan-500',
      description: 'All processed calls',
    },
    {
      title: 'Successful',
      value: analytics.successful_calls,
      icon: '✓',
      color: 'from-emerald-500 to-teal-500',
      description: 'Completed successfully',
    },
    {
      title: 'Failed',
      value: analytics.failed_calls,
      icon: '✕',
      color: 'from-red-500 to-orange-500',
      description: 'Unsuccessful attempts',
    },
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-indigo-950 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-indigo-950 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">⚠️</div>
          <p className="text-red-500 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-indigo-950">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-xl">
                🧾
              </div>
              <div>
                <h1 className="text-lg font-bold text-gray-900 dark:text-white">BillBhasha Analytics</h1>
                <p className="text-xs text-gray-500 dark:text-gray-400">Performance metrics</p>
              </div>
            </div>
            <Navigation />

          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-24 pb-20 md:pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          {/* Page Header */}
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              Analytics Dashboard
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Understand how your voice assistant is performing.
            </p>
          </div>

          {/* Metric Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {metricCards.map((card, index) => (
              <motion.div
                key={card.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${card.color} flex items-center justify-center text-white text-2xl`}>
                    {card.icon}
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">{card.description}</div>
                </div>
                <div className="text-4xl font-bold text-gray-900 dark:text-white mb-1">
                  {card.value}
                </div>
                <div className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  {card.title}
                </div>
              </motion.div>
            ))}
          </div>

          {/* Success Rate Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 mb-8"
          >
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white">Success Rate</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">Percentage of successful calls</p>
              </div>
              <div className="text-3xl font-bold text-emerald-600">{successRate}%</div>
            </div>
            <div className="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-emerald-500 to-teal-500"
                initial={{ width: 0 }}
                animate={{ width: `${successRate}%` }}
                transition={{ duration: 1, delay: 0.5 }}
              />
            </div>
          </motion.div>

          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
          >
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Recent Activity</h3>
            <div className="space-y-3">
              {analytics.total_calls === 0 ? (
                <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                  No activity yet. Start a conversation to see metrics.
                </div>
              ) : (
                <>
                  {analytics.successful_calls > 0 && (
                    <div className="flex items-center gap-3 p-3 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg">
                      <div className="w-8 h-8 rounded-full bg-emerald-500 flex items-center justify-center text-white">
                        ✓
                      </div>
                      <div className="flex-1">
                        <div className="text-sm font-medium text-gray-900 dark:text-white">
                          Successful conversation
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {analytics.successful_calls} completed
                        </div>
                      </div>
                    </div>
                  )}
                  {analytics.failed_calls > 0 && (
                    <div className="flex items-center gap-3 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                      <div className="w-8 h-8 rounded-full bg-red-500 flex items-center justify-center text-white">
                        ✕
                      </div>
                      <div className="flex-1">
                        <div className="text-sm font-medium text-gray-900 dark:text-white">
                          Incomplete conversation
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {analytics.failed_calls} ended early
                        </div>
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          </motion.div>

          {/* Auto-refresh notice */}
          <div className="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
            Analytics refresh automatically every 30 seconds
          </div>
        </div>
      </main>

      {/* Mobile Navigation */}
      <MobileNavigation />
    </div>
  );
}