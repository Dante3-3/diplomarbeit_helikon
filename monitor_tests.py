#!/usr/bin/env python3
"""Monitor and auto-restart the CLIL benchmark tests.

This script continuously monitors the test_harness.py process and automatically
restarts it if it fails or exits unexpectedly. Perfect for overnight runs.

Usage:
    python monitor_tests.py                    # Start fresh run with monitoring
    python monitor_tests.py --resume           # Resume existing run with monitoring
    python monitor_tests.py --check-interval 60  # Custom check interval (seconds)
"""

import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


class TestMonitor:
    def __init__(self, check_interval=30, resume=False):
        self.check_interval = check_interval
        self.resume = resume
        self.restart_count = 0
        self.start_time = datetime.now()
        self.log_file = Path("monitor.log")
        
    def log(self, message):
        """Log message to both console and file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
    
    def run_tests(self):
        """Run the test harness and monitor it."""
        cmd = [sys.executable, "test_harness.py"]
        if self.resume:
            cmd.append("--resume")
        
        self.log(f"Starting tests: {' '.join(cmd)}")
        
        try:
            # Run the test harness
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Stream output in real-time
            while True:
                output = process.stdout.readline()
                if output:
                    print(output.rstrip())
                    
                # Check if process is still running
                if process.poll() is not None:
                    break
            
            # Get return code
            return_code = process.poll()
            
            if return_code == 0:
                self.log("✓ Tests completed successfully!")
                return True
            else:
                self.log(f"✗ Tests exited with error code {return_code}")
                return False
                
        except KeyboardInterrupt:
            self.log("Monitor interrupted by user (Ctrl+C)")
            if process:
                process.terminate()
                process.wait()
            raise
        except Exception as e:
            self.log(f"✗ Unexpected error: {e}")
            return False
    
    def monitor_loop(self):
        """Main monitoring loop."""
        self.log("=" * 70)
        self.log("CLIL Benchmark Monitor Started")
        self.log(f"Check interval: {self.check_interval}s")
        self.log(f"Resume mode: {self.resume}")
        self.log("=" * 70)
        
        try:
            while True:
                success = self.run_tests()
                
                if success:
                    # Tests completed successfully - we're done!
                    elapsed = datetime.now() - self.start_time
                    self.log("=" * 70)
                    self.log(f"All tests completed successfully!")
                    self.log(f"Total time: {elapsed}")
                    self.log(f"Restarts: {self.restart_count}")
                    self.log("=" * 70)
                    break
                else:
                    # Tests failed - restart
                    self.restart_count += 1
                    self.log("=" * 70)
                    self.log(f"⚠️  Test run #{self.restart_count} failed!")
                    self.log(f"Waiting {self.check_interval}s before restart...")
                    self.log("=" * 70)
                    
                    time.sleep(self.check_interval)
                    
                    # After first failure, always resume
                    if not self.resume:
                        self.log("Switching to --resume mode for subsequent runs")
                        self.resume = True
                    
                    self.log(f"Restarting tests (attempt #{self.restart_count + 1})...")
                    
        except KeyboardInterrupt:
            elapsed = datetime.now() - self.start_time
            self.log("\n" + "=" * 70)
            self.log("Monitor stopped by user")
            self.log(f"Total runtime: {elapsed}")
            self.log(f"Restarts performed: {self.restart_count}")
            self.log("=" * 70)
            sys.exit(0)


def main():
    """Parse arguments and start monitoring."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Monitor and auto-restart CLIL benchmark tests"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from existing results (passed to test_harness.py)"
    )
    parser.add_argument(
        "--check-interval",
        type=int,
        default=30,
        help="Seconds to wait before restarting after failure (default: 30)"
    )
    
    args = parser.parse_args()
    
    # Verify test_harness.py exists
    if not Path("test_harness.py").exists():
        print("ERROR: test_harness.py not found in current directory")
        sys.exit(1)
    
    # Create monitor and start
    monitor = TestMonitor(
        check_interval=args.check_interval,
        resume=args.resume
    )
    
    monitor.monitor_loop()


if __name__ == "__main__":
    main()
