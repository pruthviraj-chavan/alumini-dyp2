#!/usr/bin/env python
"""
Test runner script for DYP Salokhenagar Alumni Portal
This script runs tests for specific apps or all apps in the project.
"""

import os
import sys
import argparse
import subprocess

def run_tests(app_name=None):
    """Run tests for a specific app or all apps"""
    command = [sys.executable, "manage.py", "test"]
    
    if app_name:
        command.append(app_name)
    
    try:
        subprocess.run(command, check=True)
        print(f"✅ Tests {'for ' + app_name if app_name else ''} completed successfully!")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Tests {'for ' + app_name if app_name else ''} failed!")
        return False

def main():
    """Main function to parse arguments and run tests"""
    parser = argparse.ArgumentParser(description='Run tests for the Alumni Portal')
    parser.add_argument('--app', type=str, help='Specific app to test (e.g., chat, accounts, posts)')
    parser.add_argument('--all', action='store_true', help='Run tests for all apps')
    
    args = parser.parse_args()
    
    if args.app:
        run_tests(args.app)
    elif args.all:
        # Test each app individually
        apps = ['accounts', 'chat', 'posts', 'core']
        results = {}
        
        for app in apps:
            print(f"\n{'=' * 50}")
            print(f"Running tests for {app}...")
            print(f"{'=' * 50}")
            results[app] = run_tests(app)
        
        # Print summary
        print(f"\n{'=' * 50}")
        print("Test Summary")
        print(f"{'=' * 50}")
        
        all_passed = True
        for app, passed in results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{app}: {status}")
            all_passed = all_passed and passed
        
        sys.exit(0 if all_passed else 1)
    else:
        # Default: run all tests together
        run_tests()

if __name__ == "__main__":
    main()
