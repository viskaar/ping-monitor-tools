#!/usr/bin/env python3
"""
Real-time Ping Monitor
"""

import subprocess
import re
import time
import threading
from collections import deque

class RealTimePingMonitor:
    def __init__(self, host="8.8.8.8", history_size=50):
        self.host = host
        self.history = deque(maxlen=history_size)
        self.running = False
        self.stats = {
            'total_pings': 0,
            'successful_pings': 0,
            'failed_pings': 0
        }

    def get_user_input(self):
        print("🔍 Real-time Ping Monitor")
        print("=" * 40)
        
        host = input("Enter target host (default: 8.8.8.8): ").strip()
        if host:
            self.host = host
        
        print(f"\n🎯 Monitoring: {self.host}")
        print("📊 Live statistics will update every 2 seconds")
        print("⏹️  Press Ctrl+C or Enter to stop\n")

    def single_ping(self):
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '3', self.host],
                capture_output=True,
                text=True,
                timeout=4
            )
            
            self.stats['total_pings'] += 1
            
            if result.returncode == 0:
                match = re.search(r'time=([\d.]+) ms', result.stdout)
                if match:
                    ping_time = float(match.group(1))
                    self.history.append(ping_time)
                    self.stats['successful_pings'] += 1
                    return ping_time
            
            self.stats['failed_pings'] += 1
            return None
            
        except Exception:
            self.stats['failed_pings'] += 1
            return None

    def display_realtime_stats(self):
        if not self.history:
            print("⏳ Waiting for first ping...")
            return
        
        current = self.history[-1]
        history_list = list(self.history)
        
        avg = sum(history_list) / len(history_list)
        min_ping = min(history_list)
        max_ping = max(history_list)
        
        bar_length = 20
        normalized = min(current / 300, 1.0)
        filled = int(bar_length * normalized)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        if current < 50:
            quality = "💚"
        elif current < 100:
            quality = "💛"
        elif current < 200:
            quality = "🟡"
        else:
            quality = "🔴"
        
        timestamp = time.strftime("%H:%M:%S")
        print(f"{quality} [{timestamp}] Current: {current:5.1f}ms [{bar}] "
              f"Avg: {avg:5.1f}ms | Min: {min_ping:5.1f}ms | "
              f"Success: {self.stats['successful_pings']}/{self.stats['total_pings']}")

    def display_summary(self):
        print("\n" + "=" * 50)
        print("📊 MONITORING SUMMARY")
        print("=" * 50)
        
        if self.history:
            history_list = list(self.history)
            avg_ping = sum(history_list) / len(history_list)
            min_ping = min(history_list)
            max_ping = max(history_list)
            packet_loss = (self.stats['failed_pings'] / self.stats['total_pings']) * 100
            
            print(f"🌐 Target: {self.host}")
            print(f"⏱️  Duration: {self.stats['total_pings']} samples collected")
            print(f"✅ Successful: {self.stats['successful_pings']}")
            print(f"❌ Failed: {self.stats['failed_pings']}")
            print(f"📊 Packet Loss: {packet_loss:.1f}%")
            print(f"⚡ Min/Avg/Max: {min_ping:.1f}/{avg_ping:.1f}/{max_ping:.1f} ms")
            
            if packet_loss > 20:
                quality = "🔴 UNSTABLE"
            elif avg_ping < 50 and packet_loss < 5:
                quality = "💚 EXCELLENT"
            elif avg_ping < 100 and packet_loss < 10:
                quality = "💛 GOOD"
            elif avg_ping < 200 and packet_loss < 15:
                quality = "🟡 FAIR"
            else:
                quality = "🟠 POOR"
                
            print(f"🏆 Overall Quality: {quality}")

    def wait_for_exit(self):
        input()
        self.running = False
        print("\n🛑 Stopping monitoring...")

    def run(self):
        self.get_user_input()
        self.running = True
        
        exit_thread = threading.Thread(target=self.wait_for_exit)
        exit_thread.daemon = True
        exit_thread.start()
        
        try:
            while self.running:
                self.single_ping()
                self.display_realtime_stats()
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring interrupted by user")
            self.running = False
        
        self.display_summary()

def main():
    monitor = RealTimePingMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
