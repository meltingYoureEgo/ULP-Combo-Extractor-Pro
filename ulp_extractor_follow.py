#!/usr/bin/env python3
"""
ULP Combo Extractor Pro — Professional Edition v3.0
Developed by: ａᏰᏥì ⃟  🇺🇸|🕯️🍷
GitHub: https://github.com/meltingYoureEgo
Official Site: https://linktrabbhi.netlify.app

A powerful combo extraction tool designed for security researchers
and penetration testers to process and analyze credential data.
"""

import os
import sys
import re
import json
import time
import urllib.request
from datetime import datetime

# ==================== VERSION & AUTHOR ====================
__version__ = "3.0"
__author__ = "ａᏰᏥì ⃟  🇺🇸|🕯️🍷"
__github__ = "https://github.com/meltingYoureEgo"
__website__ = "https://linktrabbhi.netlify.app"
__license__ = "MIT"

# ==================== CONFIG ====================
AUTHOR_NAME = __author__
GITHUB_USERNAME = "meltingYoureEgo"
OWNER_SITE = __website__
VERSION = __version__

# ==================== BANNER ====================
def display_banner():
    """Display professional banner."""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██╗   ██╗██╗██████╗     ██████╗ ██████╗ ███╗   ███╗     ║
║   ██║   ██║██║██╔══██╗    ██╔══██╗██╔══██╗████╗ ████║     ║
║   ██║   ██║██║██████╔╝    ██████╔╝██████╔╝██╔████╔██║     ║
║   ██║   ██║██║██╔═══╝     ██╔══██╗██╔══██╗██║╚██╔╝██║     ║
║   ╚██████╔╝██║██║         ██████╔╝██║  ██║██║ ╚═╝ ██║     ║
║    ╚═════╝ ╚═╝╚═╝         ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝     ║
║                                                              ║
║   ULP Combo Extractor Pro — Professional Edition v{VERSION}  ║
║                                                              ║
║   👤 Author: {AUTHOR_NAME}                                   ║
║   📎 GitHub: {__github__}                                   ║
║   🌐 Website: {OWNER_SITE}                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

# ==================== FOLLOWER CHECK ====================
def check_follower(username):
    """
    Check if a GitHub user follows the repository owner.
    This helps maintain community engagement and support.
    """
    try:
        print(f"🔍 Checking follower status for @{username}...")
        req = urllib.request.Request(
            f"https://api.github.com/users/{GITHUB_USERNAME}/followers",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            followers = json.loads(response.read().decode())
            for follower in followers:
                if follower.get("login", "").lower() == username.lower():
                    return True
            return False
    except Exception as e:
        print(f"⚠️ Could not verify follower status: {e}")
        return False

def get_user_input():
    """Get GitHub username from user."""
    print("\n📝 Please enter your GitHub username to continue.")
    print("   (Following the author is appreciated but not required.)")
    return input("\n🔑 GitHub username: ").strip()

# ==================== CORE EXTRACTION ENGINE ====================
def extract_combos(filepath, filter_keyword=None):
    """
    Extract email:password combos from a text file.
    
    Args:
        filepath: Path to the input file
        filter_keyword: Optional keyword to filter results
    
    Returns:
        tuple: (extracted_combos, domain_stats)
    """
    print(f"\n📂 Processing: {filepath}")
    
    if not os.path.exists(filepath):
        print("❌ File not found.")
        return [], {}
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return [], {}
    
    print(f"📊 Total lines read: {len(lines)}")
    
    extracted = []
    domain_stats = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Match email:password pattern
        match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}):(.+)', line)
        if match:
            email = match.group(1)
            password = match.group(2)
            combo = f"{email}:{password}"
            
            if filter_keyword:
                if filter_keyword.lower() in combo.lower():
                    extracted.append(combo)
                    domain = email.split('@')[1].lower()
                    domain_stats[domain] = domain_stats.get(domain, 0) + 1
            else:
                extracted.append(combo)
                domain = email.split('@')[1].lower()
                domain_stats[domain] = domain_stats.get(domain, 0) + 1
    
    return extracted, domain_stats

def save_results(extracted, domain_stats, base_name):
    """
    Save extracted combos to files.
    """
    if not extracted:
        print("❌ No valid combos found.")
        return
    
    # Save main output
    output_file = f"{base_name}_extracted.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for combo in sorted(set(extracted)):
            f.write(combo + '\n')
    
    print(f"✅ Extracted {len(set(extracted))} unique combos.")
    print(f"📁 Main output saved to: {output_file}")
    
    # Show domain statistics
    if domain_stats:
        print("\n📊 Domain Statistics:")
        sorted_domains = sorted(domain_stats.items(), key=lambda x: x[1], reverse=True)
        for domain, count in sorted_domains[:10]:
            print(f"   📧 {domain}: {count} combos")
        
        # Ask for domain-specific files
        choice = input("\n💾 Save domain-specific files? (y/n): ").strip().lower()
        if choice == 'y':
            for domain, _ in sorted_domains:
                domain_file = f"{base_name}_{domain.replace('.', '_')}.txt"
                with open(domain_file, 'w', encoding='utf-8') as f:
                    for combo in extracted:
                        if domain in combo:
                            f.write(combo + '\n')
                print(f"   ✅ Saved: {domain_file}")

def process_file(filepath, filter_keyword=None):
    """Process a single file."""
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    extracted, domain_stats = extract_combos(filepath, filter_keyword)
    save_results(extracted, domain_stats, base_name)

def process_folder(folderpath, filter_keyword=None):
    """Process all .txt files in a folder."""
    print(f"\n📂 Processing folder: {folderpath}")
    
    if not os.path.isdir(folderpath):
        print("❌ Folder not found.")
        return
    
    txt_files = [f for f in os.listdir(folderpath) if f.endswith('.txt')]
    if not txt_files:
        print("❌ No .txt files found in folder.")
        return
    
    print(f"📊 Found {len(txt_files)} .txt files.")
    
    for file in txt_files:
        filepath = os.path.join(folderpath, file)
        process_file(filepath, filter_keyword)

# ==================== MAIN ====================
def main():
    """Main entry point."""
    display_banner()
    
    # Get user input
    username = get_user_input()
    if not username:
        print("❌ No input provided. Exiting.")
        sys.exit(1)
    
    # Check follower status (informational only)
    print(f"\n💡 Tip: Following @{GITHUB_USERNAME} on GitHub helps support this project.")
    print("   This is optional and not required to use the tool.\n")
    
    # Ask for extraction mode
    print("📂 Select extraction mode:")
    print("   [1] Single file")
    print("   [2] Batch mode (folder)")
    choice = input("\nEnter choice (1/2): ").strip()
    
    # Optional filter
    filter_keyword = input("\n🔍 Enter filter keyword (or press Enter to skip): ").strip() or None
    if filter_keyword:
        print(f"   🔍 Filtering results for: '{filter_keyword}'")
    
    # Process based on choice
    if choice == "1":
        file_path = input("\n📁 Enter file path: ").strip()
        if not os.path.exists(file_path):
            print("❌ File not found.")
            sys.exit(1)
        process_file(file_path, filter_keyword)
    elif choice == "2":
        folder_path = input("\n📁 Enter folder path: ").strip()
        if not os.path.isdir(folder_path):
            print("❌ Folder not found.")
            sys.exit(1)
        process_folder(folder_path, filter_keyword)
    else:
        print("❌ Invalid choice.")
        sys.exit(1)
    
    # Completion message
    print("\n" + "=" * 60)
    print("✅ Extraction complete!")
    print("📁 Output files are saved in the current directory.")
    print("👤 Author: " + AUTHOR_NAME)
    print("🌐 Website: " + OWNER_SITE)
    print("📎 GitHub: " + __github__)
    print("=" * 60)
    print("\n⭐ If you found this tool useful, consider starring the repository!")
    print("   https://github.com/meltingYoureEgo/ULP-Combo-Extractor-Pro\n")

if __name__ == "__main__":
    main()