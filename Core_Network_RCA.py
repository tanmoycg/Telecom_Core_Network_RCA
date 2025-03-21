import os
import csv
import random
import datetime
from collections import defaultdict
from sklearn.cluster import DBSCAN
import numpy as np
from collections import defaultdict

# Ensure the logs directory exists
LOG_DIR = "logs"
NO_OF_LOGS = 2000


# Main execution flow
def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    logs = generate_synthetic_logs(NO_OF_LOGS)  # Generate and save logs
    log_file = save_logs(logs)
    converted_logs = load_logs(log_file)  # Load logs from file
    data = preprocess_logs(converted_logs)  # Convert logs to numerical format
    clusters = cluster_alarms(data)  # Perform clustering
    rca_results = root_cause_analysis(logs, clusters)  # Perform RCA

    # Print results
    print("\nRoot Cause Analysis Results:")
    for cluster, details in rca_results.items():
        print(f"Cluster {cluster}: {details}")

# Generate synthetic telecom alarm logs (list of dictionaries)
def generate_synthetic_logs(num_logs=1000):
    components = ["Router", "RAN", "DWDM", "Switch", "Server"]
    types = ["Link Failure", "High Latency", "Packet Loss", "Hardware Fault"]
    severity_levels = [1, 2, 3, 4, 5]  # 1 (Low) to 5 (Critical)

    logs = []
    for _ in range(num_logs):
        log = {
            "timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=random.randint(1, 10000))).isoformat(),
            "component": random.choice(components),
            "type": random.choice(types),
            "severity": random.choice(severity_levels)
        }
        logs.append(log)
    return logs

# Save generated logs to a CSV file inside logs directory
def save_logs(logs):
    log_file = os.path.join(LOG_DIR, "alarm_logs.csv")
    with open(log_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=logs[0].keys())
        writer.writeheader()
        writer.writerows(logs)

    print(f"Synthetic logs saved to {log_file}")
    return log_file

# Load logs from file
def load_logs(file_path):
    converted_logs = []
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["severity"] = int(row["severity"])  # Convert severity to integer
            row["timestamp"] = datetime.datetime.fromisoformat(row["timestamp"])
            converted_logs.append(row)
    return converted_logs

# Convert logs to numerical format for clustering
def preprocess_logs(logs):
    """
    Convert logs into a numerical format suitable for DBSCAN clustering.
    """
    # Extract timestamps and normalize them
    timestamps = [log["timestamp"] for log in logs]
    start_time = min(timestamps)
    normalized_timestamps = [(t - start_time).total_seconds() for t in timestamps]

    # Extract components and types
    components = [log["component"] for log in logs]
    types = [log["type"] for log in logs]

    # Encode components
    unique_components = list(set(components))
    component_mapping = {comp: idx for idx, comp in enumerate(unique_components)}
    component_encoded = [component_mapping[comp] for comp in components]

    # Encode alarm types
    unique_types = list(set(types))
    type_mapping = {typ: idx for idx, typ in enumerate(unique_types)}
    type_encoded = [type_mapping[typ] for typ in types]

    # Extract severity scores
    severity_scores = [log["severity"] for log in logs]

    # Combine all numerical data into a structured format
    processed_logs = []
    for i in range(len(logs)):
        processed_logs.append([
            normalized_timestamps[i],
            component_encoded[i],
            type_encoded[i],
            severity_scores[i],
        ])

    return np.array(processed_logs)

# Cluster alarms using DBSCAN
def cluster_alarms(data):
    clustering = DBSCAN(eps=1000, min_samples=3).fit(data)  # eps controls sensitivity
    return clustering.labels_


def root_cause_analysis(logs, clusters):
    """
    Perform Root Cause Analysis (RCA) by identifying the most common components,
    alarm types, and average severity for each cluster.

    Parameters:
        logs (list of dicts): List of alarm logs, where each log is a dictionary.
        clusters (list): List of cluster IDs corresponding to each log.

    Returns:
        dict: RCA results with cluster IDs as keys and identified root causes as values.
    """
    root_causes = defaultdict(list)

    # Group logs by cluster ID
    for idx, cluster_id in enumerate(clusters):
        if cluster_id != -1:  # Ignore noise points (-1)
            root_causes[cluster_id].append(logs[idx])

    rca_results = {}

    # Analyze each cluster
    for cluster_id, cluster_logs in root_causes.items():
        component_counts = {}
        type_counts = {}
        total_severity = 0

        # Count occurrences and sum severity
        for log in cluster_logs:
            component_counts[log["component"]] = component_counts.get(log["component"], 0) + 1
            type_counts[log["type"]] = type_counts.get(log["type"], 0) + 1
            total_severity += log["severity"]

        # Determine most common component and type
        most_common_component = max(component_counts, key=component_counts.get)
        most_common_type = max(type_counts, key=type_counts.get)

        # Compute average severity
        avg_severity = total_severity / len(cluster_logs)

        # Store RCA results
        rca_results[cluster_id] = {
            "Primary Component": most_common_component,
            "Primary Alarm Type": most_common_type,
            "Average Severity": avg_severity
        }

    return rca_results


if __name__ == "__main__":
    main()
