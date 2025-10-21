#!/usr/bin/env python3
"""
Basic Ping Monitor
"""

import subprocess
import re
import time
import sys
from datetime import datetime

class PingMonitor:
    def __init__(self):
        self.results = {
            'ping_times': [],
            'packet_loss': 0,
            'successful_pings': 0
        }

    def get_valid_input(self):
        print("🚀 Basic Ping Monitor")
        print("=" * 40)
        
        target_host = input("Enter target host (default: 8.8.8.8): ").strip()
        if not target_host:
            target_host = "8.8.8.8"
        
        while True:
            ping_count_input = input("Enter number of pings (default: 10): ").strip()
            if not ping_count_input:
                ping_count = 10
                break
            try:
                ping_count = int(ping_count_input)
                if ping_count <= 0:
                    print("❌ Please enter a positive number!")
                    continue
                break
            except ValueError:
                print("❌ Invalid input! Please enter a number")
        
        return target_host, ping_count

    def single_ping(self, host, sequence):
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '2', host],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                match = re.search(r'time=([\d.]+) ms', result.stdout)
                if match:
                    ping_time = float(match.group(1))
                    self.results['ping_times'].append(ping_time)
                    self.results['successful_pings'] += 1
                    
                    strength = self.get_ping_strength(ping_time)
                    print(f"[{timestamp}] Packet {sequence}: {ping_time:6.2f} ms {strength}")
                    return ping_time
            else:
                print(f"[{timestamp}] Packet {sequence}: ❌ Request timeout")
                
        except subprocess.TimeoutExpired:
            print(f"[{timestamp}] Packet {sequence}: ⏰ Timeout")
        except Exception as e:
            print(f"[{timestamp}] Packet {sequence}: 💥 Error: {e}")
        
        self.results['packet_loss'] += 1
        return None

    def get_ping_strength(self, ping_time):
        if ping_time < 50:
            return "💚 Excellent"
        elif ping_time < 100:
            return "💛 Good"
        elif ping_time < 200:
            return "🟡 Fair"
        elif ping_time < 500:
            return "🟠 Poor"
        else:
            return "🔴 Very Poor"

    def display_statistics(self, host, total_packets):
        ping_times = self.results['ping_times']
        packet_loss = self.results['packet_loss']
        
        print("\n" + "=" * 50)
        print("📈 PING STATISTICS SUMMARY")
        print("=" * 50)
        
        if ping_times:
            min_ping = min(ping_times)
            max_ping = max(ping_times)
            avg_ping = sum(ping_times) / len(ping_times)
            jitter = max_ping - min_ping
            
            packet_loss_rate = (packet_loss / total_packets) * 100
            
            print(f"🌐 Target Host: {host}")
            print(f"📦 Packets Sent: {total_packets}")
            print(f"✅ Successful: {len(ping_times)}")
            print(f"❌ Lost: {packet_loss}")
            print(f"📊 Packet Loss: {packet_loss_rate:.1f}%")
            print(f"⚡ Min/Avg/Max: {min_ping:.2f}/{avg_ping:.2f}/{max_ping:.2f} ms")
            print(f"📏 Jitter: {jitter:.2f} ms")
            
            quality = self.get_connection_quality(avg_ping, packet_loss_rate)
            print(f"🏆 Connection Quality: {quality}")
        else:
            print("❌ No successful pings recorded")

    def get_connection_quality(self, avg_ping, packet_loss):
        if packet_loss > 20:
            return "🔴 UNSTABLE"
        elif avg_ping < 50 and packet_loss < 1:
            return "💚 EXCELLENT"
        elif avg_ping < 100 and packet_loss < 5:
            return "💛 GOOD"
        elif avg_ping < 200 and packet_loss < 10:
            return "🟡 FAIR"
        else:
            return "🟠 POOR"

    def run(self):
        try:
            target_host, ping_count = self.get_valid_input()
            
            print(f"\n🎯 Starting {ping_count} pings to {target_host}")
            print("Press Ctrl+C to stop early\n")
            
            for i in range(ping_count):
                self.single_ping(target_host, i + 1)
                if i < ping_count - 1:
                    time.sleep(1)
            
            self.display_statistics(target_host, ping_count)
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

def main():
    monitor = PingMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
