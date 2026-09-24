"""
Module Name: data_manager.py
Purpose: Manages persistent storage of incident reports in a local JSON database
         and provides facilities management Excel spreadsheet export utilities and status updates with strict type annotations.
"""

import json
import os
from typing import Any, cast
import openpyxl  # <-- Required for Excel file generation

DB_FILENAME = "incidents_database.json"

def load() -> list[dict[str, Any]]:
    """
    Loads all saved incident records from disk storage. 
    Returns an empty list if the database file does not exist or cannot be parsed.
    """
    if not os.path.exists(DB_FILENAME):
        return []
        
    try:
        with open(DB_FILENAME, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure loaded data structure matches a list of dictionaries
            if isinstance(data, list):
                return cast(list[dict[str, Any]], data)
            return []
    except (json.JSONDecodeError, IOError) as e:
        print(f"[Data Error] Could not read database: {e}")
        return []

def save(records: list[dict[str, Any]]) -> bool:
    """
    Saves the current list of incident records to disk with directory verification 
    and comprehensive permission safety checks.
    """
    try:
        # Ensure target storage directory exists if a relative folder path is configured
        dir_name = os.path.dirname(DB_FILENAME)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            
        # Write records data cleanly in JSON format with indentation
        with open(DB_FILENAME, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=4)
        return True
        
    except PermissionError:
        print(f"[Data Error] Permission denied: Cannot write to '{DB_FILENAME}'. Please verify folder write permissions.")
        return False
    except IOError as e:
        print(f"[Data Error] Could not save to database due to an I/O error: {e}")
        return False

def query(keyword: str) -> list[dict[str, Any]]:
    """
    Queries stored incidents by matching a search keyword against 
    either the location string or asset information (case-insensitive).
    """
    records = load()
    keyword_lower = keyword.lower()
    
    # Filter records containing the keyword in location or asset info
    results: list[dict[str, Any]] = [
        r for r in records 
        if keyword_lower in str(r.get('location', '')).lower() or keyword_lower in str(r.get('asset_info', '')).lower()
    ]
    return results

def clear_database() -> bool:
    """Permanently wipes all records by deleting the local JSON database file from disk."""
    try:
        if os.path.exists(DB_FILENAME):
            os.remove(DB_FILENAME)
        return True
    except IOError as e:
        print(f"[Data Error] Could not clear database: {e}")
        return False

def update_incident_status(incident_id: str, new_status: str = "Resolved") -> bool:
    """
    Finds a specific incident by its unique ID and updates its review status 
    (e.g., from 'Pending Review' to 'Resolved'), then saves the changes.
    """
    records = load()
    updated = False
    
    for r in records:
        if str(r.get("incident_id")) == incident_id:
            r["status"] = new_status
            updated = True
            break
            
    if updated:
        save(records)
        return True
    return False

def delete_incident_by_id(incident_id: str) -> bool:
    """
    Deletes a specific incident record by its unique ID from the JSON database 
    using a case-insensitive lookup check.
    """
    records = load()
    initial_count = len(records)
    
    # Exclude the record matching the targeted ID
    updated_records = [
        r for r in records 
        if str(r.get("incident_id", "")).strip().upper() != incident_id.strip().upper()
    ]
    
    # If the list length shrank, save the filtered database
    if len(updated_records) < initial_count:
        save(updated_records)
        return True
    return False

def export_incidents_to_excel(filename: str = "export_safety_report.xlsx") -> bool:
    """
    Exports all logged incident records into a professional Excel spreadsheet (.xlsx) 
    optimized for facilities management review, sorting, and reporting.
    """
    records = load()
    if not records:
        return False
        
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        if ws is not None:
            ws.title = "Safety Incidents"
            
            # Define professional column headers for the spreadsheet
            headers = [
                "Incident ID", "Timestamp", "Reporter Name", "Contact", 
                "Location", "Asset", "Severity", "Priority Score", 
                "Priority Queue", "Duplicate Flag", "Status", "Risk Summary"
            ]
            ws.append(headers)
            
            # Populate spreadsheet rows with incident record details
            for r in records:
                ws.append([
                    r.get('incident_id'),
                    r.get('timestamp', 'N/A'),
                    r.get('reporter_name'),
                    r.get('reporter_contact'),
                    r.get('location'),
                    r.get('asset_info'),
                    r.get('severity'),
                    r.get('priority_score'),
                    r.get('final_priority'),
                    r.get('is_duplicate'),
                    r.get('status', 'Pending Review'),
                    r.get('risk_summary')
                ])
                
        wb.save(filename)
        return True
    except Exception as e:
        print(f"[Data Error] Excel export failed: {e}")
        return False

# Compatibility aliases for legacy method naming calls
load_database = load
save_database = save
export_incidents_to_txt = export_incidents_to_excel