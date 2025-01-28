/*
  # Initial Schema Setup for Sniper Bot

  1. New Tables
    - `wallets` - Stores wallet configurations
      - `id` (uuid, primary key)
      - `address` (text, unique)
      - `enabled` (boolean)
      - `user_id` (uuid, references auth.users)
      - `created_at` (timestamp)
    
    - `trades` - Stores trade history
      - `id` (uuid, primary key)
      - `token_address` (text)
      - `amount` (numeric)
      - `type` (text) - 'BUY' or 'SELL'
      - `status` (text)
      - `gwei` (numeric)
      - `slippage` (numeric)
      - `wallet_id` (uuid, references wallets)
      - `user_id` (uuid, references auth.users)
      - `created_at` (timestamp)
    
    - `settings` - Stores user settings
      - `id` (uuid, primary key)
      - `user_id` (uuid, references auth.users)
      - `rpc_url` (text)
      - `dex` (text)
      - `pool_coin` (text)
      - `pay_coin` (text)
      - `auto_gwei` (boolean)
      - `created_at` (timestamp)

  2. Security
    - Enable RLS on all tables
    - Add policies for authenticated users to manage their own data
*/

-- Create wallets table
CREATE TABLE IF NOT EXISTS wallets (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  address text UNIQUE NOT NULL,
  enabled boolean DEFAULT true,
  user_id uuid REFERENCES auth.users NOT NULL,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE wallets ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own wallets"
  ON wallets
  FOR ALL
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Create trades table
CREATE TABLE IF NOT EXISTS trades (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  token_address text NOT NULL,
  amount numeric NOT NULL,
  type text NOT NULL CHECK (type IN ('BUY', 'SELL')),
  status text NOT NULL DEFAULT 'PENDING',
  gwei numeric NOT NULL,
  slippage numeric NOT NULL,
  wallet_id uuid REFERENCES wallets NOT NULL,
  user_id uuid REFERENCES auth.users NOT NULL,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE trades ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own trades"
  ON trades
  FOR ALL
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Create settings table
CREATE TABLE IF NOT EXISTS settings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users NOT NULL UNIQUE,
  rpc_url text DEFAULT 'https://bsc-dataseed3.binance.org',
  dex text DEFAULT 'PancakeSwap V2',
  pool_coin text DEFAULT 'WBNB',
  pay_coin text DEFAULT 'WBNB',
  auto_gwei boolean DEFAULT true,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE settings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own settings"
  ON settings
  FOR ALL
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);