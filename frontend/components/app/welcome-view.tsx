import React, { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

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
        // Fallback check: browser permissions query if supported
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
        className="bg-background flex flex-col items-center justify-center px-6 py-12 text-center"
        {...props}
      >
        <div className="text-destructive mb-6 text-6xl">🎙️</div>
        <h2 className="text-foreground mb-3 text-2xl font-bold">Microphone access is blocked</h2>
        <p className="text-muted-foreground mb-8 max-w-md text-sm leading-6">
          Please allow microphone access in your browser settings and try again.
        </p>
        <Button
          size="lg"
          onClick={verifyAndStart}
          className="w-64 rounded-full text-base font-bold tracking-wider"
        >
          Try Again
        </Button>
      </div>
    );
  }

  return (
    <div ref={ref} className="mx-auto w-full max-w-md px-4 md:px-0 relative z-10" {...props}>
      {/* Subtle animated background layer behind the content */}
      <div className="absolute inset-0 -z-10 animate-gradient-move bg-gradient-to-br from-indigo-500/20 via-purple-500/10 to-cyan-500/20 rounded-[3rem] blur-3xl opacity-50 dark:opacity-30"></div>
      
      <section className="flex flex-col items-center justify-center text-center py-12">
        {/* Header */}
        <header className="mb-8 flex flex-col items-center">
          <h1 className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-cyan-500 dark:from-indigo-400 dark:to-cyan-300 flex items-center gap-2 text-5xl font-extrabold tracking-tight pb-1 drop-shadow-sm">
            🧾 BillBhasha AI
          </h1>
          <p className="text-muted-foreground mt-3 text-sm font-semibold tracking-widest uppercase opacity-80">
            Your Voice-Powered Bill Assistant
          </p>
        </header>

        {/* Main Hero Screen */}
        <div className="mb-8">
          <h2 className="text-foreground text-3xl font-extrabold tracking-tight md:text-4xl leading-tight">
            Understand your bills.<br/>
            <span className="text-indigo-500 dark:text-indigo-400">Simply.</span>
          </h2>
          <p className="text-muted-foreground mt-4 max-w-xs text-sm leading-6 md:max-w-sm mx-auto font-medium">
            Ask about GST, charges, invoices, receipts or payments — just speak.
          </p>
        </div>

        {/* Center Large Voice Button / State Display */}
        {isConnecting ? (
          <div className="mt-8 flex w-full flex-col items-center">
            <Button
              disabled
              size="lg"
              className="glass-card text-foreground flex w-72 items-center justify-center gap-3 rounded-full py-7 text-sm font-bold tracking-wider md:text-base opacity-80"
            >
              <span className="animate-spin text-xl">🔄</span> Connecting...
            </Button>
          </div>
        ) : hasCalled ? (
          <div className="animate-in fade-in slide-in-from-bottom-4 mt-8 flex w-full flex-col items-center gap-4 duration-500">
            <p className="flex items-center gap-2 text-base font-bold text-emerald-600 dark:text-emerald-400 drop-shadow-sm">
              ✓ Call ended
            </p>
            <Button
              size="lg"
              disabled={checkingPermission}
              onClick={verifyAndStart}
              className="glow-button bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white flex w-64 items-center justify-center gap-2 rounded-full py-6 text-base font-bold tracking-wider transition-all duration-300 hover:scale-105 border-none"
            >
              <span className="text-xl">↻</span> Start Again
            </Button>
          </div>
        ) : (
          <Button
            size="lg"
            disabled={checkingPermission}
            onClick={verifyAndStart}
            className="glow-button mt-8 bg-gradient-to-r from-indigo-600 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 text-white flex w-72 items-center justify-center gap-3 rounded-full py-7 text-lg font-bold tracking-wider transition-all duration-300 hover:scale-[1.03] border-none"
          >
            <span className="text-2xl drop-shadow-md">🎙️</span> Start Conversation
          </Button>
        )}

        {/* Track-specific UI (Suggestions) */}
        {!isConnecting && (
          <div className="animate-in fade-in slide-in-from-bottom-6 mt-12 w-full duration-700 delay-150 fill-mode-both">
            <p className="text-foreground/70 mb-4 text-xs font-bold tracking-widest uppercase md:text-xs">
              What can I help you understand?
            </p>
            <div className="flex flex-wrap justify-center gap-3">
              {['GST', 'Invoice', 'Extra Charges', 'Receipt'].map((item) => (
                <span
                  key={item}
                  className="glass-card text-foreground hover:bg-white/20 dark:hover:bg-white/10 cursor-pointer rounded-full px-5 py-2 text-sm font-semibold transition-all duration-300 hover:-translate-y-1 hover:shadow-lg"
                >
                  {item}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Track-specific UI (Features List) */}
        {!isConnecting && (
          <div className="glass-card animate-in fade-in slide-in-from-bottom-8 mt-10 w-full rounded-3xl p-6 text-left duration-1000 delay-300 fill-mode-both relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full blur-2xl -mr-10 -mt-10"></div>
            <p className="text-foreground mb-5 text-center text-xs font-bold tracking-widest uppercase md:text-xs relative z-10">
              BillBhasha can help you with
            </p>
            <ul className="text-foreground/90 space-y-4 text-sm font-medium md:text-base relative z-10">
              <li className="flex items-center gap-4 transition-transform hover:translate-x-1 duration-300">
                <span className="text-xl bg-indigo-100 dark:bg-indigo-900/50 p-2 rounded-full">🧾</span>
                <span>Understand complex invoices</span>
              </li>
              <li className="flex items-center gap-4 transition-transform hover:translate-x-1 duration-300">
                <span className="text-xl bg-purple-100 dark:bg-purple-900/50 p-2 rounded-full">💰</span>
                <span>Explain GST & hidden charges</span>
              </li>
              <li className="flex items-center gap-4 transition-transform hover:translate-x-1 duration-300">
                <span className="text-xl bg-cyan-100 dark:bg-cyan-900/50 p-2 rounded-full">🛍️</span>
                <span>Review purchase bills</span>
              </li>
              <li className="flex items-center gap-4 transition-transform hover:translate-x-1 duration-300">
                <span className="text-xl bg-emerald-100 dark:bg-emerald-900/50 p-2 rounded-full">💳</span>
                <span>Verify payment details</span>
              </li>
            </ul>
          </div>
        )}

        {/* Dashboard Link */}
        {!isConnecting && (
          <div className="animate-in fade-in slide-in-from-bottom-10 mt-6 w-full duration-1000 delay-500 fill-mode-both">
            <Link
              href="/dashboard"
              className="text-muted-foreground hover:text-foreground text-xs font-semibold tracking-widest uppercase transition-colors duration-300"
            >
              📊 View Call Analytics Dashboard
            </Link>
          </div>
        )}
      </section>
    </div>
  );
};
