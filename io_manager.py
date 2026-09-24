"""
Module Name: io_manager.py
Purpose: Handles all user-facing interactions, including CLI menus with strict numeric validation,
         comprehensive input validation loops, and formatted displays with strict type annotations.
"""

import os
import re
from datetime import datetime
from typing import Any, Optional

def _get_severity_icon(severity: str) -> str:
    """
    Helper function that maps raw text severity levels to visual color circles 
    and labels for rapid hazard triage and UI display.
    """
    mapping = {
        "Low": "🟢 [Low]",
        "Medium": "🟡 [Medium]",
        "High": "🟠 [High]",
        "Critical": "🔴 [Critical]"
    }
    return mapping.get(severity, "⚪ [Unknown]")

def select_image_interactively() -> str:
    """
    Scans the 'images' folder, displays a numbered list of available image files,
    and loops safely until the user enters a valid option number or chooses to skip.
    """
    images_dir = "images"
    
    # Fallback input if the images directory doesn't exist
    if not os.path.exists(images_dir):
        return input("Enter path or filename of visual evidence (optional, press Enter to skip): ").strip()
    
    valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(valid_extensions)]
    
    # Fallback input if the directory contains no valid image formats
    if not image_files:
        return input("Enter path or filename of visual evidence (optional, press Enter to skip): ").strip()
    
    # Display interactive selection menu for images
    print("\n--- Available Visual Evidence in /images ---")
    for idx, filename in enumerate(image_files, 1):
        print(f"[{idx}] {filename}")
    print("[0] Skip / No image")
    
    # Loop until valid numeric selection is made
    while True:
        choice = input("Select an image number (or press Enter to skip): ").strip()
        
        if not choice or choice == "0":
            return "None"
            
        if choice.isdigit():
            selected_index = int(choice) - 1
            if 0 <= selected_index < len(image_files):
                chosen_file = os.path.join(images_dir, image_files[selected_index])
                print(f"[Selected] {chosen_file}")
                return chosen_file
            else:
                print(f"[Error] Invalid selection number. Please enter a number between 0 and {len(image_files)}.")
        else:
            print("[Error] Invalid input. Please enter a valid number.")

def display_menu() -> str:
    """
    Displays the main interactive CLI menu, strips whitespace, 
    and strictly loops until the user enters a valid option number between 1 and 8.
    """
    print("\n==============================================")
    print("     CAMPUS SAFETY HAZARD REPORTING SYSTEM      ")
    print("==============================================")
    print("1. Submit New Hazard Report")
    print("2. View All Logged Incidents")
    print("3. Query Incidents by Location or Asset")
    print("4. Export Incidents to Excel Report")
    print("5. Clear All Logged Records")
    print("6. Mark Incident as Resolved")
    print("7. Delete Specific Incident Record")
    print("8. Exit")
    
    # Enforce strict numeric range validation loop (1 to 8)
    while True:
        choice = input("Select an option (1-8): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 8:
            return choice
        print("[Error] Invalid input. Please enter a valid number between 1 and 8.")

def get_user_input() -> dict[str, Any]:
    """
    Prompts front-line reporters for structured incident details, enforcing robust 
    validation loops for names, institutional contacts, headcount, and character lengths.
    """
    print("\n--- Submit New Hazard Report (SIT Punggol Coast) ---")
    
    # Step 1: Validate Reporter Name (letters, spaces, apostrophes, periods, and hyphens only)
    reporter_name = ""
    name_pattern = r"^[A-Za-z\s'\.-]+$"
    while True:
        reporter_name = input("Enter reporter name (Student/Teacher): ").strip()
        if not reporter_name:
            print("Error: Reporter name cannot be empty.")
        elif not re.match(name_pattern, reporter_name):
            print("Error: Please enter a valid name (letters and spaces only, no numbers).")
        else:
            break
            
    # Step 2: Validate Institutional Contact (SIT email domain or 8-11 digit phone number)
    reporter_contact = ""
    email_pattern = r"^[\w\.-]+@([\w-]+\.)?singaporetech\.edu\.sg$"
    phone_pattern = r"^\d{8,11}$"
    while True:
        reporter_contact = input("Enter SIT email or phone number: ").strip()
        if re.match(email_pattern, reporter_contact, re.IGNORECASE) or re.match(phone_pattern, reporter_contact):
            break
        print("Error: Please enter a valid SIT email (e.g., user@sit.singaporetech.edu.sg) or an 8-11 digit phone number.")
    
    # Step 3: Validate Location (non-empty string)
    location = ""
    while not location.strip():
        location = input("Enter location (e.g., SIT@Punggol Coast, Level 3 MakerSpace): ").strip()
        if not location:
            print("Error: Location cannot be empty.")
    
    # Step 4: Capture Visual Evidence path via interactive folder scanner
    visual_evidence = select_image_interactively()
    if not visual_evidence:
        visual_evidence = "None"
        
    # Step 5: Validate Headcount (realistic campus range between 1 and 1000)
    impact = 0
    while True:
        impact_input = input("Enter estimated number of people affected (headcount): ").strip()
        if impact_input.isdigit():
            impact = int(impact_input)
            if 1 <= impact <= 1000:
                break
            print("Error: Please enter a realistic headcount between 1 and 1000.")
        else:
            print("Error: Please enter a valid non-negative number.")
        
    # Step 6: Validate Asset Info (minimum 3 characters required)
    asset_info = ""
    while True:
        asset_info = input("Enter asset information (e.g., Smart Projector, Lab Bench Socket): ").strip()
        if len(asset_info) >= 3:
            break
        print("Error: Asset information must be at least 3 characters long.")
            
    # Step 7: Validate Description (minimum 15 characters required for contextual AI analysis)
    description = ""
    while True:
        description = input("Enter detailed description of the hazard: ").strip()
        if len(description) >= 15:
            break
        print("Error: Description is too brief. Please provide at least 15 characters of detail for accurate AI analysis.")
            
    # Compile validated fields into a structured dictionary record with a timestamp
    record: dict[str, Any] = {
        "reporter_name": reporter_name,
        "reporter_contact": reporter_contact,
        "location": location,
        "visual_evidence": visual_evidence,
        "impact_headcount": impact,
        "asset_info": asset_info,
        "description": description,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return record

def get_confirmation() -> str:
    """Prompts user to confirm submission of the report."""
    return input("Do you wish to submit this report? (y/n): ").strip().lower()

def confirm_clear() -> str:
    """Prompts user for confirmation before wiping database records."""
    return input("Are you sure you want to permanently delete all logged incident records? (y/n): ").strip().lower()

def get_search_keyword() -> str:
    """Prompts for a search term to query records by location or asset name."""
    return input("Enter search keyword (location or asset name): ").strip().lower()

def select_incident_interactively(records: list[dict[str, Any]]) -> Optional[str]:
    """
    Displays a numbered list of incident records sorted sequentially by ID 
    and allows the user to choose one by typing its index number.
    """
    if not records:
        print("\n[Notice] No incident records available.")
        return None
        
    sorted_records = sorted(records, key=lambda x: str(x.get('incident_id', '')))
        
    print("\n--- Select Incident Record ---")
    for idx, r in enumerate(sorted_records, 1):
        inc_id = str(r.get('incident_id', 'N/A'))
        loc = str(r.get('location', 'N/A'))
        asset = str(r.get('asset_info', 'N/A'))
        status = str(r.get('status', 'Pending Review'))
        print(f"[{idx}] {inc_id} - {loc} ({asset}) [Status: {status}]")
    print("[0] Cancel")
    
    choice = input("Select an incident number: ").strip()
    
    if not choice or choice == "0":
        return None
        
    try:
        selected_index = int(choice) - 1
        if 0 <= selected_index < len(sorted_records):
            chosen_record = sorted_records[selected_index]
            return str(chosen_record.get('incident_id'))
        else:
            print("[Warning] Invalid selection number.")
            return None
    except ValueError:
        print("[Warning] Please enter a valid number.")
        return None

def display_summary(ai_summary: Optional[str]) -> None:
    """Displays the AI-generated pre-submission risk summary."""
    print("\n--- AI Pre-Submission Risk Summary ---")
    print(ai_summary or "No summary available.")
    print("---------------------------------------")

def display_result(record: dict[str, Any]) -> None:
    """Displays a formatted receipt view for a successfully logged incident record."""
    print("\n=== Hazard Report Successfully Logged ===")
    print(f"Incident ID     : {record.get('incident_id')}")
    print(f"Timestamp       : {record.get('timestamp', 'N/A')}")
    print(f"Reporter Name   : {record.get('reporter_name')}")
    print(f"Contact Info    : {record.get('reporter_contact')}")
    print(f"Location        : {record.get('location')}")
    print(f"Asset           : {record.get('asset_info')}")
    print(f"Visual Evidence : {record.get('visual_evidence')}")
    print(f"Category        : {record.get('category')}")
    print(f"Severity        : {_get_severity_icon(str(record.get('severity', '')))}")
    print(f"Priority Queue  : {record.get('final_priority')}")
    print(f"Duplicate Flag  : {record.get('is_duplicate')}")
    print(f"Status          : {record.get('status')}")
    print("=========================================\n")

def display_list(records: list[dict[str, Any]]) -> None:
    """Iterates through and prints a structured, readable list of incident records."""
    if not records:
        print("No incident records found.")
        return
    print(f"\n--- Found {len(records)} Incident Records (Sorted by Severity) ---")
    for index, r in enumerate(records, 1):
        sev_icon = _get_severity_icon(str(r.get('severity', '')))
        print(f"[{index}] Incident ID : {r.get('incident_id')}")
        print(f"    Timestamp   : {r.get('timestamp', 'N/A')}")
        print(f"    Reporter    : {r.get('reporter_name')} ({r.get('reporter_contact')})")
        print(f"    Location    : {r.get('location')}")
        print(f"    Asset       : {r.get('asset_info')}")
        print(f"    Evidence    : {r.get('visual_evidence')}")
        print(f"    Severity    : {sev_icon}")
        print(f"    Priority    : {r.get('final_priority')}")
        print(f"    Status      : {r.get('status', 'Pending Review')}")
        print("-" * 42)
    print()

def display_message(message: str) -> None:
    """Prints a standard system status or notice message to the console."""
    print(message)