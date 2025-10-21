#!/usr/bin/env python3
"""
Multi-Target Ping Comparator
"""

import subprocess
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class PingComparator:
    def __init__(self):
        self.targets = [
            "8.8.8.8",
            "1.1.1.1",
            "github.com",
            "stackoverflow.com",
            "aws.amazon.com",
        ]
        self.results = {}

    def display_banner(self):
        print("🌐 Multi-Target Ping Comparator")
        print("=" * 55)

    def get_custom_targets(self):
        print("\n📋 Default Targets:")
        for i, target in enumerate(self.targets, 1):
            print(f"  {i:2d}. {target}")
        
        print("\n🎯 Add Custom Targets (press Enter to skip):")
        while True:
            custom = input("Enter custom target (or 'done' to finish): ").strip()
            if not custom or custom.lower() == 'done':
                break
            if custom not in self.targets:
                self.targets.append(custom)
                print(f"✅ Added: {custom}")

    def ping_single_target(self, target):
        try:
            start_time = time.time()
            result = subprocess.run(
                ['ping', '-c', '3', '-W', '2', target],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                times = re.findall(r'time=([\d.]+) ms', result.stdout)
                if times:
                    times = [float(t) for t in times]
                    avg_time = sum(times) / len(times)
                    
                    return {
                        'target': target,
                        'success': True,
                        'avg_ping': avg_time,
                        'min_ping': min(times),
                        'max_ping': max(times),
                        'jitter': max(times) - min(times),
                        'packets_sent': 3,
                        'packets_received': len(times),
                        'packet_loss': (3 - len(times)) / 3 * 100,
                    }
        
        except Exception:
            pass
        
        return {
            'target': target,
            'success': False,
            'avg_ping': 0,
            'min_ping': 0,
            'max_ping': 0,
            'jitter': 0,
            'packets_sent': 3,
            'packets_received': 0,
            'packet_loss': 100,
        }

    def get_ping_quality(self, ping_time):
        if ping_time < 30:
            return "💚 EXCELLENT"
        elif ping_time < 80:
            return "💛 GOOD"
        elif ping_time < 150:
            return "🟡 FAIR"
        elif ping_time < 300:
            return "🟠 POOR"
        else:
            return "🔴 BAD"

    def display_comparison_results(self, results):
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        successful.sort(key=lambda x: x['avg_ping'])
        
        print("\n" + "=" * 80)
        print("🏆 PING PERFORMANCE RANKING")
        print("=" * 80)
        
        if successful:
            print("\n📊 SUCCESSFUL TARGETS:")
            print("-" * 80)
            print(f"{'Rank':<4} {'Target':<25} {'Avg Ping':<10} {'Min/Max':<12} {'Quality':<12} {'Loss':<6}")
            print("-" * 80)
            
            for i, result in enumerate(successful, 1):
                quality = self.get_ping_quality(result['avg_ping'])
                loss_pct = result['packet_loss']
                loss_str = f"{loss_pct:.0f}%" if loss_pct > 0 else "0%"
                
                print(f"{i:<4} {result['target']:<25} "
                      f"{result['avg_ping']:7.1f}ms  "
                      f"{result['min_ping']:.1f}/{result['max_ping']:.1f}  "
                      f"{quality:<12} "
                      f"{loss_str:<6}")
        
        if failed:
            print(f"\n❌ FAILED TARGETS ({len(failed)}):")
            for result in failed:
                print(f"   {result['target']} - No response")

    def run_comparison(self):
        print(f"\n🔄 Testing {len(self.targets)} targets simultaneously...")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_target = {
                executor.submit(self.ping_single_target, target): target 
                for target in self.targets
            }
            
            results = []
            for future in as_completed(future_to_target):
                target = future_to_target[future]
                try:
                    result = future.result()
                    results.append(result)
                    status = "✅" if result['success'] else "❌"
                    print(f"{status} {target}: {result['avg_ping']:.1f}ms" if result['success'] else f"{status} {target}: Failed")
                except Exception as e:
                    print(f"⚠️  Exception for {target}: {e}")
        
        return results

    def run(self):
        try:
            self.display_banner()
            self.get_custom_targets()
            
            if not self.targets:
                print("❌ No targets selected!")
                return
            
            print(f"\n🎯 Final target list ({len(self.targets)} targets):")
            for target in self.targets:
                print(f"  • {target}")
            
            input("\nPress Enter to start comparison...")
            
            results = self.run_comparison()
            self.display_comparison_results(results)
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Comparison stopped by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")

def main():
    comparator = PingComparator()
    comparator.run()

if __name__ == "__main__":
    main()
