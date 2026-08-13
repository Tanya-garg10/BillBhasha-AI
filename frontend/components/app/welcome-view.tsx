import React, { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { VoiceOrb } from './voice-orb';
import { Navigation } from './navigation';
import { MobileNavigation } from './mobile-navigation';

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
  connectionState?: string;
  hasCalled?: boolean;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  connectionState,
  hasCalled,
  ref,
  ...props
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  void startButtonText;
  const [permissionBlocked, setPermissionBlocked] = useState(false);
  const [checkingPermission, setCheckingPermission] = useState(false);

  const isConnecting = connectionState === 'connecting';

  const verifyAndStart = async () => {
    setCheckingPermission(true);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.getTracks().forEach((track) => track.stop());
      setPermissionBlocked(false);
      onStartCall();
    } catch (err: unknown) {
      console.error('Microphone access check failed:', err);
      const errorName = err instanceof Error ? err.name : '';
      if (errorName === 'NotAllowedError' || errorName === 'PermissionDeniedError') {
        setPermissionBlocked(true);
      } else {
        try {
          const status = await navigator.permissions.query({
            name: 'microphone' as PermissionName,
          });
          if (status.state === 'denied') {
            setPermissionBlocked(true);
          } else {
            onStartCall();
          }
        } catch {
          setPermissionBlocked(true);
        }
      }
    } finally {
      setCheckingPermission(false);
    }
  };

  if (permissionBlocked) {
    return (
      <div
        ref={ref}
        className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 flex flex-col items-center justify-center px-6 py-12 text-center min-h-screen"
        {...props}
      >
        <div className="text-red-500 mb-6 text-6xl">🎙️</div>
        <h2 className="text-gray-900 dark:text-white mb-3 text-2xl font-bold">Microphone access is blocked</h2>
        <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-md text-sm leading-6">
          Please allow microphone access in your browser settings and try again.
        </p>
        <Button
          size="lg"
          onClick={verifyAndStart}
          className="w-64 rounded-full text-base font-bold tracking-wider bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500"
        >
          Try Again
        </Button>
      </div>
    );
  }

  const getOrbState = () => {
    if (isConnecting) return 'connecting';
    if (hasCalled) return 'ended';
    return 'ready';
  };

  return (
    <div ref={ref} className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-indigo-950" {...props}>
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-xl">
                🧾
              </div>
              <div>
                <h1 className="text-lg font-bold text-gray-900 dark:text-white">BillBhasha AI</h1>
                <p className="text-xs text-gray-500 dark:text-gray-400">AI Voice Assistant</p>
              </div>
            </div>

            {/* Connection Status */}
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${isConnecting ? 'bg-yellow-500 animate-pulse' : 'bg-green-500'}`} />
              <span className="text-sm text-gray-600 dark:text-gray-400">
                {isConnecting ? 'Connecting...' : 'Ready'}
              </span>
            </div>

            {/* Navigation */}
            <Navigation className="hidden md:flex" />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-24 pb-20 md:pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Your voice assistant for smarter bills.
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Understand GST, invoices, charges and payments — simply by talking.
            </p>
          </div>

          {/* Voice Orb */}
          <div className="mb-12">
            <VoiceOrb state={getOrbState()} />
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col items-center gap-4">
            {isConnecting ? (
              <Button
                disabled
                size="lg"
                className="w-72 rounded-full py-7 text-lg font-bold tracking-wider bg-gradient-to-r from-indigo-600 to-purple-600 opacity-80"
              >
                <span className="animate-spin mr-2">⏳</span> Connecting...
              </Button>
            ) : hasCalled ? (
              <Button
                size="lg"
                disabled={checkingPermission}
                onClick={verifyAndStart}
                className="w-72 rounded-full py-7 text-lg font-bold tracking-wider bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 transition-all duration-300 hover:scale-105"
              >
                <span className="mr-2">↻</span> Start Another Conversation
              </Button>
            ) : (
              <Button
                size="lg"
                disabled={checkingPermission}
                onClick={verifyAndStart}
                className="w-72 rounded-full py-7 text-lg font-bold tracking-wider bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 transition-all duration-300 hover:scale-105 shadow-lg"
              >
                <span className="mr-2">🎙️</span> Start Conversation
              </Button>
            )}

            {!isConnecting && (
              <Link
                href="#how-it-works"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                How it works →
              </Link>
            )}
          </div>

          {/* Visual Context Elements */}
          <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { icon: '🧾', label: 'Invoices' },
              { icon: '💰', label: 'GST' },
              { icon: '💳', label: 'Payments' },
              { icon: '📊', label: 'Analytics' },
            ].map((item) => (
              <div
                key={item.label}
                className="bg-white dark:bg-gray-800 rounded-2xl p-6 text-center shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow"
              >
                <div className="text-3xl mb-2">{item.icon}</div>
                <div className="text-sm font-medium text-gray-900 dark:text-white">{item.label}</div>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Mobile Navigation */}
      <MobileNavigation />
    </div>
  );
};