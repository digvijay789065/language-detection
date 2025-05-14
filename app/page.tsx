'use client';

import React from 'react';
import { useState } from 'react';
import axios from 'axios';

// Loading skeleton component
const LoadingSkeleton: React.FC = () => (
  <div className="animate-pulse" role="status" aria-label="Loading results">
    <div className="h-16 w-3/4 bg-gray-200 rounded-lg mb-4 mx-auto"></div>
    <div className="bg-gray-50 rounded-xl p-6">
      <div className="h-6 w-1/2 bg-gray-200 rounded mb-4 mx-auto"></div>
      <div className="h-10 w-1/3 bg-gray-200 rounded mb-4 mx-auto"></div>
      <div className="w-full bg-gray-200 rounded-full h-2"></div>
    </div>
    <span className="sr-only">Loading language detection results...</span>
  </div>
);

const Home: React.FC = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState<{ language: string; confidence: number } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const detectLanguage = async () => {
    if (!text.trim()) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('/api/detect', { text });
      setResult(response.data);
    } catch (error) {
      setError('Failed to detect language. Please try again.');
      console.error('Error detecting language:', error);
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-200 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-lg p-8 text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 flex items-center justify-center gap-2">
            🌍 Language Detective
          </h1>
          <p className="text-gray-600 mt-2">
            Detect the language of any text instantly
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="space-y-4">
            <div className="relative">
              <label htmlFor="text-input" className="sr-only">
                Enter text for language detection
              </label>
              <textarea
                id="text-input"
                aria-label="Enter text for language detection"
                className={`w-full h-40 p-4 rounded-xl border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 resize-none text-gray-700 text-lg transition-all ${loading ? 'opacity-50' : ''}`}
                placeholder="Type or paste your text here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                disabled={loading}
              />
              {loading && (
                <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50 rounded-xl" aria-hidden="true">
                  <div className="flex items-center space-x-2" role="status">
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    <span className="sr-only">Analyzing text...</span>
                  </div>
                </div>
              )}
            </div>
            <button
              onClick={detectLanguage}
              disabled={loading || !text.trim()}
              className={`w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white py-3 px-6 rounded-xl font-semibold hover:shadow-lg transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed ${loading ? 'animate-pulse' : ''}`}
              aria-label={loading ? 'Analyzing text...' : 'Detect Language'}
            >
              {loading ? '🔍 Analyzing...' : '🔍 Detect Language'}
            </button>
            {error && (
              <div className="text-red-500 text-center p-2 bg-red-50 rounded-lg" role="alert" aria-live="polite">
                {error}
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="bg-white rounded-2xl shadow-lg p-8" role="region" aria-label="Detection Results">
            {loading ? (
              <LoadingSkeleton />
            ) : result ? (
              <div className="text-center transform transition-all duration-300 ease-in-out">
                <div className="text-4xl font-bold text-gray-800 mb-4" role="heading" aria-level={2}>
                  {result.language}
                </div>
                <div className="bg-gray-50 rounded-xl p-6">
                  <div className="text-gray-600 mb-2">Confidence Score</div>
                  <div className="text-3xl font-bold text-blue-600" aria-label={`Confidence score: ${Math.round(result.confidence * 100)}%`}>
                    {Math.round(result.confidence * 100)}%
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-4 overflow-hidden" role="progressbar" aria-valuenow={Math.round(result.confidence * 100)} aria-valuemin={0} aria-valuemax={100}>
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-1000 ease-out"
                      style={{ width: `${result.confidence * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-500" aria-label="No results yet">
                <div className="text-center">
                  <div className="text-4xl mb-2" aria-hidden="true">🔍</div>
                  <div>Enter text to detect its language</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
};

export default Home; 