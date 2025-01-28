export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      wallets: {
        Row: {
          id: string
          address: string
          enabled: boolean
          user_id: string
          created_at: string
        }
        Insert: {
          id?: string
          address: string
          enabled?: boolean
          user_id: string
          created_at?: string
        }
        Update: {
          id?: string
          address?: string
          enabled?: boolean
          user_id?: string
          created_at?: string
        }
      }
      trades: {
        Row: {
          id: string
          token_address: string
          amount: number
          type: 'BUY' | 'SELL'
          status: string
          gwei: number
          slippage: number
          wallet_id: string
          user_id: string
          created_at: string
        }
        Insert: {
          id?: string
          token_address: string
          amount: number
          type: 'BUY' | 'SELL'
          status?: string
          gwei: number
          slippage: number
          wallet_id: string
          user_id: string
          created_at?: string
        }
        Update: {
          id?: string
          token_address?: string
          amount?: number
          type?: 'BUY' | 'SELL'
          status?: string
          gwei?: number
          slippage?: number
          wallet_id?: string
          user_id?: string
          created_at?: string
        }
      }
      settings: {
        Row: {
          id: string
          user_id: string
          rpc_url: string
          dex: string
          pool_coin: string
          pay_coin: string
          auto_gwei: boolean
          created_at: string
        }
        Insert: {
          id?: string
          user_id: string
          rpc_url?: string
          dex?: string
          pool_coin?: string
          pay_coin?: string
          auto_gwei?: boolean
          created_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          rpc_url?: string
          dex?: string
          pool_coin?: string
          pay_coin?: string
          auto_gwei?: boolean
          created_at?: string
        }
      }
    }
  }
}