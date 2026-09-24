"""
Module Name: logic_manager.py
Purpose: Handles core scoring, routing, duplication checking, and severity sorting logic with strict type annotations.
"""

from typing import Any

def score(record: dict[str, Any]) -> float:
    """
    Calculates a numerical priority score based on severity baseline weights 
    and incremental impact headcount (formula: base + [headcount * 0.1]).
    """
    # Define baseline weight mappings for each severity tier
    sev_weights = {"Low": 1, "Medium": 5, "High": 10, "Critical": 20}
    
    # Retrieve base weight matching record severity (defaults to 1 if unspecified)
    base = sev_weights.get(str(record.get("severity", "Low")), 1)
    
    # Parse impact headcount safely as a float (defaults to 0)
    impact = float(record.get("impact_headcount", 0))
    
    # Compute and return final weighted score
    return float(base + (impact * 0.1))

def route(record: dict[str, Any]) -> str:
    """
    Determines operational dispatch queues based on the incident's severity level.
    Critical and High severities route to emergency dispatch; others go to standard maintenance.
    """
    sev = str(record.get("severity", "Low"))
    
    # Route high-risk incidents to urgent dispatch
    if sev in ["Critical", "High"]:
        return "Urgent Emergency Dispatch"
        
    # Default route for lower risk categories
    return "Standard Maintenance Queue"

def check_duplicate(new_record: dict[str, Any], existing_records: list[dict[str, Any]]) -> str:
    """
    Checks if a newly submitted report is a potential duplicate by matching 
    location and asset information against unresolved existing records in the database.
    """
    for r in existing_records:
        # Normalize and compare location strings (case-insensitive and whitespace-stripped)
        loc_match = str(new_record.get("location", "")).strip().lower() == str(r.get("location", "")).strip().lower()
        
        # Normalize and compare asset info strings (case-insensitive and whitespace-stripped)
        asset_match = str(new_record.get("asset_info", "")).strip().lower() == str(r.get("asset_info", "")).strip().lower()
        
        # Flag as duplicate if location and asset match, and the existing record is not yet resolved
        if loc_match and asset_match and r.get("status") != "Resolved":
            return f"Potential Duplicate of {r.get('incident_id')}"
            
    return "Unique"

def sort_incidents_by_severity(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Sorts incident records sequentially by severity level rank 
    (Critical -> High -> Medium -> Low).
    """
    # Define explicit numerical ordering map for sorting keys
    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    
    # Sort records using order map lookup (defaults unmapped severities to rank 4)
    return sorted(records, key=lambda x: order.get(str(x.get("severity", "Low")), 4))