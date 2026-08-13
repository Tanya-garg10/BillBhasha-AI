'use client';

import { motion } from 'motion/react';

interface VoiceOrbProps {
  state: 'ready' | 'connecting' | 'listening' | 'speaking' | 'ended';
  className?: string;
}

export function VoiceOrb({ state, className = '' }: VoiceOrbProps) {
  const getStateConfig = () => {
    switch (state) {
      case 'ready':
        return {
          text: 'Ready to help',
          subtext: 'Tap to start',
          color: 'from-indigo-500 to-purple-500',
          scale: 1,
          pulse: true,
        };
      case 'connecting':
        return {
          text: 'Connecting...',
          subtext: 'Please wait',
          color: 'from-blue-500 to-cyan-500',
          scale: 0.9,
          pulse: true,
        };
      case 'listening':
        return {
          text: 'Listening to you',
          subtext: 'Speak clearly',
          color: 'from-emerald-500 to-teal-500',
          scale: 1.1,
          pulse: true,
        };
      case 'speaking':
        return {
          text: 'BillBhasha is speaking',
          subtext: 'Listen carefully',
          color: 'from-purple-500 to-pink-500',
          scale: 1.15,
          pulse: true,
        };
      case 'ended':
        return {
          text: 'Conversation completed',
          subtext: 'Start another conversation',
          color: 'from-gray-500 to-gray-600',
          scale: 1,
          pulse: false,
        };
      default:
        return {
          text: 'Ready to help',
          subtext: 'Tap to start',
          color: 'from-indigo-500 to-purple-500',
          scale: 1,
          pulse: true,
        };
    }
  };

  const config = getStateConfig();

  return (
    <div className={`flex flex-col items-center justify-center ${className}`}>
      {/* Voice Orb */}
      <motion.div
        className="relative"
        animate={{ scale: config.scale }}
        transition={{ duration: 0.3 }}
      >
        {/* Outer glow */}
        {config.pulse && (
          <motion.div
            className={`absolute inset-0 rounded-full bg-gradient-to-r ${config.color} opacity-20 blur-xl`}
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.2, 0.4, 0.2],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          />
        )}

        {/* Main orb */}
        <motion.div
          className={`relative w-48 h-48 md:w-64 md:h-64 rounded-full bg-gradient-to-r ${config.color} shadow-2xl`}
          animate={{
            scale: config.pulse ? [1, 1.05, 1] : 1,
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          {/* Inner glow */}
          <div className="absolute inset-4 rounded-full bg-gradient-to-r from-white/30 to-transparent backdrop-blur-sm" />
          
          {/* Center icon */}
          <div className="absolute inset-0 flex items-center justify-center">
            {state === 'connecting' ? (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                className="text-white text-4xl"
              >
                ⏳
              </motion.div>
            ) : state === 'listening' ? (
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 0.5, repeat: Infinity }}
                className="text-white text-5xl"
              >
                🎙️
              </motion.div>
            ) : state === 'speaking' ? (
              <motion.div
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 0.3, repeat: Infinity }}
                className="text-white text-5xl"
              >
                🔊
              </motion.div>
            ) : state === 'ended' ? (
              <div className="text-white text-5xl">✓</div>
            ) : (
              <div className="text-white text-5xl">🎙️</div>
            )}
          </div>

          {/* Audio waveform visualization (decorative) */}
          {state === 'listening' || state === 'speaking' ? (
            <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex gap-1">
              {[...Array(5)].map((_, i) => (
                <motion.div
                  key={i}
                  className="w-1 bg-white/60 rounded-full"
                  animate={{
                    height: [8, 24, 8],
                  }}
                  transition={{
                    duration: 0.5,
                    repeat: Infinity,
                    delay: i * 0.1,
                  }}
                />
              ))}
            </div>
          ) : null}
        </motion.div>
      </motion.div>

      {/* Status text */}
      <div className="mt-8 text-center">
        <motion.h3
          className="text-2xl font-bold text-gray-900 dark:text-white"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          key={state}
        >
          {config.text}
        </motion.h3>
        <motion.p
          className="text-gray-600 dark:text-gray-400 mt-2"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          key={`${state}-subtext`}
        >
          {config.subtext}
        </motion.p>
      </div>
    </div>
  );
}