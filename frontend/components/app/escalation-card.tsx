'use client';

import { motion } from 'motion/react';

interface EscalationCardProps {
  referenceId: string;
  status: 'Open' | 'In Progress' | 'Resolved';
  onClose?: () => void;
}

export function EscalationCard({ referenceId, status, onClose }: EscalationCardProps) {
  const getStatusColor = () => {
    switch (status) {
      case 'Open':
        return 'bg-yellow-500';
      case 'In Progress':
        return 'bg-blue-500';
      case 'Resolved':
        return 'bg-green-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 max-w-md mx-auto"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center">
            🧑‍💼
          </div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-white">
            Human Support Requested
          </h3>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          >
            ✕
          </button>
        )}
      </div>

      {/* Reference ID */}
      <div className="mb-4">
        <div className="text-sm text-gray-500 dark:text-gray-400 mb-1">Reference</div>
        <div className="text-lg font-mono font-bold text-gray-900 dark:text-white">
          {referenceId}
        </div>
      </div>

      {/* Status */}
      <div className="mb-4">
        <div className="text-sm text-gray-500 dark:text-gray-400 mb-1">Status</div>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${getStatusColor()}`} />
          <span className="text-sm font-medium text-gray-900 dark:text-white">{status}</span>
        </div>
      </div>

      {/* Checkmarks */}
      <div className="space-y-2 mb-4">
        <div className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
          <div className="w-5 h-5 rounded-full bg-emerald-100 dark:bg-emerald-900/50 flex items-center justify-center text-emerald-600 dark:text-emerald-400 text-xs">
            ✓
          </div>
          <span>Permission received</span>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
          <div className="w-5 h-5 rounded-full bg-emerald-100 dark:bg-emerald-900/50 flex items-center justify-center text-emerald-600 dark:text-emerald-400 text-xs">
            ✓
          </div>
          <span>Request created</span>
        </div>
      </div>

      {/* Message */}
      <div className="bg-indigo-50 dark:bg-indigo-900/20 rounded-lg p-3">
        <p className="text-sm text-gray-700 dark:text-gray-300">
          "A support representative will review your request."
        </p>
      </div>
    </motion.div>
  );
}