# Core Network RCA  

Practical demo of **alarm clustering and Root Cause Analysis (RCA)** in telecom networks using Python and DBSCAN.  

## Overview  
Modern telecom networks generate thousands of alarms every day. Without automation, identifying the **true root cause** among cascades of alarms becomes difficult and delays recovery.  

This project demonstrates a simple but effective approach:  
1. **Cluster alarms** that occur close in time using DBSCAN.  
2. **Analyze each cluster** to identify the most common components, alarm types, and severity patterns.  
3. Provide an **RCA summary** that highlights the likely cause of network issues.  

## Why RCA Matters in Telecom  
- **Reduces downtime** by helping engineers pinpoint problems quickly.  
- **Cuts alarm noise** — avoids chasing hundreds of correlated alarms.  
- **Improves efficiency** through automated analysis rather than manual checks.  
- **Supports proactive maintenance** by spotting recurring problem patterns.  

## Features  
- Load and preprocess alarm logs (CSV input)  
- Cluster alarms using DBSCAN (with noise handling)  
- Perform Root Cause Analysis (RCA) per cluster  
- Output structured RCA results for easy interpretation  

## File Structure  
- `Core_Network_RCA.py` → Main script containing the logic  
- `alarms_logs.csv` → Sample dataset (example alarm logs)  

## Usage  
1. Clone this repository  
   git clone <your-repo-url>
   cd <your-repo-name>

Run the script
python Core_Network_RCA.py

## Example Output
```json
{
  "0": {
      "Primary Component": "Router",
      "Primary Alarm Type": "Link_Failure",
      "Average Severity": 3.5
  },
  "1": {
      "Primary Component": "Switch",
      "Primary Alarm Type": "Port_Error",
      "Average Severity": 2.0
  }
}
```
✦ Created as part of my personal portfolio to showcase data analysis, clustering, and RCA skills for real-world telecom use cases.