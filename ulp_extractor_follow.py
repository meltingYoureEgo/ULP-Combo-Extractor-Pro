#!/usr/bin/env python3
"""
ULP Combo Extractor Pro — Neon Edition v3.0
Author: ａᏰᏥì ⃟  🇺🇸|🕯️🍷 (meltingYoureEgo)
GitHub: https://github.com/meltingYoureEgo
Description: Follower-Only combo extractor with Secret Code bypass.
"""

import os
import sys
import re
import json
import urllib.request

# ==================== CONFIG ====================
AUTHOR_NAME = "ａᏰᏥì ⃟  🇺🇸|🕯️🍷"
GITHUB_USERNAME = "meltingYoureEgo"
SECRET_CODE = "124421"  # 🔑 Owner's secret code (bypass follower check)
VERSION = "3.0"

# ==================== FOLLOWER CHECK ====================
def is_follower(username):
    """Check if user follows meltingYoureEgo."""
    try:
        req = urllib.request.Request(
            f"https://api.github.com/users/{GITHUB_USERNAME}/followers",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            followers = json.loads(response.read().decode())
            for f in followers:
                if f.get("login", "").lower() == username.lower():
                    return True
            return False
    except Exception as e:
        print(f"⚠️ Could not verify follower status: {e}")
        return False

def get_github_username():
    """Get GitHub username or secret code from user."""
    return input("🔑 Enter your GitHub username (or secret code): ").strip()

# ==================== MAIN EXTRACTION ENGINE ====================
def process_file(filepath, filter_keyword=None):
    """Process a single file and extract combos."""
    print(f"\n📂 Processing: {filepath}")
    
    if not os.path.exists(filepath):
        print("❌ File not found.")
        return
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    print(f"📊 Total lines: {len(lines)}")
    
    extracted = []
    domains = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}):(.+)', line)
        if match:
            email = match.group(1)
            password = match.group(2)
            combo = f"{email}:{password}"
            
            if filter_keyword:
                if filter_keyword.lower() in combo.lower():
                    extracted.append(combo)
                    domain = email.split('@')[1].lower()
                    domains[domain] = domains.get(domain, 0) + 1
            else:
                extracted.append(combo)
                domain = email.split('@')[1].lower()
                domains[domain] = domains.get(domain, 0) + 1
    
    if not extracted:
        print("❌ No valid combos found.")
        return
    
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_file = f"{base_name}_extracted.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for combo in sorted(set(extracted)):
            f.write(combo + '\n')
    
    print(f"✅ Extracted {len(set(extracted))} unique combos.")
    print(f"📁 Saved to: {output_file}")
    
    if domains:
        print("\n📊 Top Domains:")
        sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:5]
        for domain, count in sorted_domains:
            print(f"   {domain}: {count}")
        
        choice = input("\n💾 Save domain-specific files? (y/n): ").strip().lower()
        if choice == 'y':
            for domain, _ in sorted_domains:
                domain_file = f"{base_name}_extracted_{domain.replace('.', '_')}.txt"
                with open(domain_file, 'w', encoding='utf-8') as f:
                    for combo in extracted:
                        if domain in combo:
                            f.write(combo + '\n')
                print(f"   ✅ Saved: {domain_file}")

def process_folder(folderpath):
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
    filter_keyword = input("🔍 Enter filter keyword (or press Enter to skip): ").strip() or None
    
    for file in txt_files:
        process_file(os.path.join(folderpath, file), filter_keyword)

# ==================== MAIN ====================
def main():
    print("=" * 70)
    print(f"   ULP Combo Extractor Pro — Neon Edition v{VERSION}")
    print(f"   🔒 Follower-Only Edition by {AUTHOR_NAME}")
    print(f"   📎 https://github.com/{GITHUB_USERNAME}")
    print("=" * 70)
    
    username = get_github_username()
    if not username:
        print("❌ No input provided. Exiting.")
        sys.exit(1)
    
    # 🔑 Secret Code Check
    if username == SECRET_CODE:
        print("\n🔓 Secret code accepted! Bypassing follower check.")
        print(f"👋 Welcome, Owner {AUTHOR_NAME}!")
    else:
        print(f"\n🔍 Checking if @{username} follows @{GITHUB_USERNAME}...")
        if not is_follower(username):
            print("\n❌ You are NOT a follower of meltingYoureEgo.")
            print(f"👉 Follow @{GITHUB_USERNAME} first, or use the secret code to bypass.")
            print(f"📎 GitHub profile: https://github.com/{GITHUB_USERNAME}")
            sys.exit(1)
        print(f"\n✅ Verified! @{username} is a follower.")
    
    print("\n▶️ Starting combo extraction...\n")
    
    print("📂 Select input source:")
    print("[1] Single file")
    print("[2] Batch mode (folder)")
    choice = input("Enter choice (1/2): ").strip()
    
    if choice == "1":
        file_path = input("Enter file path: ").strip()
        if not os.path.exists(file_path):
            print("❌ File not found.")
            sys.exit(1)
        filter_keyword = input("🔍 Enter filter keyword (or press Enter to skip): ").strip() or None
        process_file(file_path, filter_keyword)
    elif choice == "2":
        folder_path = input("Enter folder path: ").strip()
        if not os.path.isdir(folder_path):
            print("❌ Folder not found.")
            sys.exit(1)
        process_folder(folder_path)
    else:
        print("❌ Invalid choice.")
        sys.exit(1)
    
    print("\n✅ Extraction complete! Thank you for supporting the author.")

if __name__ == "__main__":
    main()