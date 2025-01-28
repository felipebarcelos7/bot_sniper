import React, { useState, useEffect } from 'react';
import { Settings, Wallet, RefreshCw, AlertTriangle } from 'lucide-react';
import { supabase } from './lib/supabase';
import type { Database } from './lib/database.types';

type Settings = Database['public']['Tables']['settings']['Row'];
type Trade = Database['public']['Tables']['trades']['Row'];

function App() {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [settings, setSettings] = useState<Settings | null>(null);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [authError, setAuthError] = useState<string | null>(null);

  const [tokenAddress, setTokenAddress] = useState('0xd2fa93e043033613c472c2b10f91f4e6fa942f5');
  const [payCoin, setPayCoin] = useState('0.0001');
  const [gweiToTrade, setGweiToTrade] = useState('25');
  const [isAutoGwei, setIsAutoGwei] = useState(true);
  const [buySlippage, setBuySlippage] = useState('10');
  const [sellSlippage, setSellSlippage] = useState('10');

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      if (session) {
        fetchUserData(session.user.id);
      }
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      if (session) {
        fetchUserData(session.user.id);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const fetchUserData = async (userId: string) => {
    try {
      // Fetch user settings
      const { data: userSettings } = await supabase
        .from('settings')
        .select('*')
        .eq('user_id', userId)
        .single();
      
      if (userSettings) {
        setSettings(userSettings);
        setIsAutoGwei(userSettings.auto_gwei);
      }

      // Fetch recent trades
      const { data: userTrades } = await supabase
        .from('trades')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false })
        .limit(10);

      if (userTrades) {
        setTrades(userTrades);
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const handleSignIn = async () => {
    try {
      setAuthError(null);
      const { error } = await supabase.auth.signInWithPassword({
        email: 'test@example.com',
        password: 'test123456'
      });
      
      if (error) {
        setAuthError(error.message);
      }
    } catch (error) {
      setAuthError('An unexpected error occurred');
    }
  };

  const handleSignUp = async () => {
    try {
      setAuthError(null);
      const { error } = await supabase.auth.signUp({
        email: 'test@example.com',
        password: 'test123456'
      });
      
      if (error) {
        setAuthError(error.message);
      } else {
        // Try to sign in immediately after signup
        await handleSignIn();
      }
    } catch (error) {
      setAuthError('An unexpected error occurred');
    }
  };

  const handleStart = async () => {
    if (!session?.user) return;

    try {
      const { data: trade } = await supabase
        .from('trades')
        .insert({
          token_address: tokenAddress,
          amount: parseFloat(payCoin),
          type: 'BUY',
          gwei: parseFloat(gweiToTrade),
          slippage: parseFloat(buySlippage),
          wallet_id: session.user.id, // This should be the actual wallet ID
          user_id: session.user.id
        })
        .select()
        .single();

      if (trade) {
        setTrades(prev => [trade, ...prev]);
      }
    } catch (error) {
      console.error('Error starting trade:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-gray-100 flex items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="min-h-screen bg-gray-900 text-gray-100 flex items-center justify-center">
        <div className="bg-gray-800 p-8 rounded-lg">
          <h1 className="text-2xl font-bold mb-4">Login Required</h1>
          {authError && (
            <div className="bg-red-900/50 text-red-400 p-3 rounded mb-4">
              {authError}
            </div>
          )}
          <div className="space-y-2">
            <button
              onClick={handleSignIn}
              className="bg-blue-600 px-4 py-2 rounded w-full"
            >
              Sign In
            </button>
            <button
              onClick={handleSignUp}
              className="bg-gray-700 px-4 py-2 rounded w-full"
            >
              Create Test Account
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-4">
      <header className="flex justify-between items-center mb-6 border-b border-gray-700 pb-4">
        <h1 className="text-xl font-bold">Sniper Bot</h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-400">Current block: 26775489</span>
          <button className="bg-blue-600 px-3 py-1 rounded text-sm">Signatures</button>
        </div>
      </header>

      <div className="grid grid-cols-12 gap-4">
        {/* Left Panel */}
        <div className="col-span-4 space-y-4">
          <div className="bg-gray-800 p-4 rounded-lg">
            <div className="space-y-3">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Token Address</label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={tokenAddress}
                    onChange={(e) => setTokenAddress(e.target.value)}
                    className="bg-gray-700 rounded px-3 py-2 w-full text-sm"
                  />
                  <button className="bg-blue-600 p-2 rounded">
                    <Wallet className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Pay Coin to trade</label>
                  <input
                    type="text"
                    value={payCoin}
                    onChange={(e) => setPayCoin(e.target.value)}
                    className="bg-gray-700 rounded px-3 py-2 w-full text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Buy tax</label>
                  <div className="bg-red-900/50 text-red-400 rounded px-3 py-2 text-sm">
                    Not available
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm text-gray-400 mb-1">GWEI to trade</label>
                  <input
                    type="text"
                    value={gweiToTrade}
                    onChange={(e) => setGweiToTrade(e.target.value)}
                    className="bg-gray-700 rounded px-3 py-2 w-full text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Tip (GWEI)</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value="5"
                      className="bg-gray-700 rounded px-3 py-2 w-full text-sm"
                    />
                    <button
                      className={`px-3 rounded ${
                        isAutoGwei ? 'bg-green-600' : 'bg-gray-600'
                      }`}
                      onClick={() => setIsAutoGwei(!isAutoGwei)}
                    >
                      Auto
                    </button>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Buy slippage %</label>
                  <input
                    type="text"
                    value={buySlippage}
                    onChange={(e) => setBuySlippage(e.target.value)}
                    className="bg-gray-700 rounded px-3 py-2 w-full text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Sell slippage %</label>
                  <input
                    type="text"
                    value={sellSlippage}
                    onChange={(e) => setSellSlippage(e.target.value)}
                    className="bg-gray-700 rounded px-3 py-2 w-full text-sm"
                  />
                </div>
              </div>

              <div className="flex gap-2">
                <button 
                  className="bg-green-600 px-4 py-2 rounded flex-1 font-medium"
                  onClick={handleStart}
                >
                  START
                </button>
                <button className="bg-red-600 px-4 py-2 rounded flex-1 font-medium">
                  STOP
                </button>
              </div>
            </div>
          </div>

          {/* Mempool Section */}
          <div className="bg-gray-800 p-4 rounded-lg">
            <h3 className="text-sm font-medium mb-3">Mempool Functions</h3>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <input type="checkbox" className="rounded" />
                <span className="text-sm">Liquidity adding Mempool</span>
              </div>
              <div className="flex items-center gap-2">
                <input type="checkbox" className="rounded" />
                <span className="text-sm">Enabling Trading Mempool</span>
              </div>
              <div className="flex items-center gap-2">
                <input type="checkbox" className="rounded" />
                <span className="text-sm">TTSA (Try to Save Ass)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content / Logs */}
        <div className="col-span-5">
          <div className="bg-gray-800 p-4 rounded-lg h-[600px] flex flex-col">
            <div className="flex justify-between items-center mb-4">
              <div className="flex gap-2">
                <button className="bg-gray-700 px-3 py-1 rounded text-sm">Low 5</button>
                <button className="bg-gray-700 px-3 py-1 rounded text-sm">Avg 5</button>
                <button className="bg-gray-700 px-3 py-1 rounded text-sm">High 5</button>
              </div>
              <button className="text-blue-400 text-sm">Clear log</button>
            </div>
            <div className="flex-1 bg-gray-900 rounded p-3 text-sm font-mono overflow-y-auto">
              <div className="text-green-400">Welcome to the new aviddot bot!</div>
              {trades.map(trade => (
                <div key={trade.id} className={`text-${trade.type === 'BUY' ? 'green' : 'red'}-400`}>
                  {trade.type}: {trade.amount} @ {trade.gwei} GWEI
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Panel - Stats */}
        <div className="col-span-3">
          <div className="bg-gray-800 p-4 rounded-lg">
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-400">Pay coin in wallet:</span>
                <span className="text-sm">0.0106 WBNB</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-400">Pay coin value:</span>
                <span className="text-sm">3.44</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-400">Pay coin price:</span>
                <span className="text-sm">324.42$ WBNB</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-400">Amount snipe coin:</span>
                <span className="text-sm text-red-400">0.0 Not available</span>
              </div>
              <div className="border-t border-gray-700 my-2"></div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-400">Liquidity pool:</span>
                <span className="text-sm text-yellow-400">no liquidity pool found</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-400">RPC:</span>
            <select className="bg-gray-800 rounded px-2 py-1 text-sm">
              <option>https://bsc-dataseed3.binance.org</option>
            </select>
          </div>
          <button className="bg-blue-600 px-3 py-1 rounded text-sm flex items-center gap-1">
            <RefreshCw className="w-4 h-4" />
            Check Latency
          </button>
        </div>
        <div className="flex items-center gap-4">
          <button className="bg-blue-600 px-3 py-1 rounded text-sm">UPDATE SCORE</button>
          <button className="bg-red-600 px-3 py-1 rounded text-sm">CLEAR</button>
          <button 
            onClick={() => supabase.auth.signOut()} 
            className="bg-gray-700 px-3 py-1 rounded text-sm"
          >
            Sign Out
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;