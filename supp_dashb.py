import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, time

def solve_project():
    # --- Del a) Read data ---
    # Read the Excel file
    # Use a relative path so the script works when the Excel file is in the same folder
    df = pd.read_excel('support_uke_24.xlsx')
    
    # Extract columns into arrays as requested
    u_dag = df['Ukedag'].values
    kl_slett = df['Klokkeslett'].values
    varighet = df['Varighet'].values
    score = df['Tilfredshet'].values
    
    print("--- Del a) Data loaded successfully ---")
    print(f"Total records: {len(df)}\n")

    # --- Del b) Inquiries per weekday ---
    # Count occurrences of each weekday
    weekday_counts = df['Ukedag'].value_counts()
    # Ensure correct order for visualization
    ordered_days = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag']
    counts = [weekday_counts.get(day, 0) for day in ordered_days]
    
    plt.figure(figsize=(10, 6))
    plt.bar(ordered_days, counts, color='skyblue', edgecolor='navy')
    plt.title('Antall henvendelser per ukedag (Uke 24)', fontsize=14)
    plt.xlabel('Ukedag', fontsize=12)
    plt.ylabel('Antall henvendelser', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('/home/ubuntu/weekday_inquiries.png')
    plt.close()
    
    print("--- Del b) Weekday inquiry counts ---")
    for day, count in zip(ordered_days, counts):
        print(f"{day}: {count}")
    print("Visualization saved as weekday_inquiries.png\n")

    # --- Del c) Min and Max talk time ---
    # Convert duration strings to total seconds for calculation
    def duration_to_seconds(d):
        if isinstance(d, str):
            h, m, s = map(int, d.split(':'))
            return h * 3600 + m * 60 + s
        elif isinstance(d, time):
            return d.hour * 3600 + d.minute * 60 + d.second
        return 0

    durations_sec = [duration_to_seconds(d) for d in varighet]
    min_sec = min(durations_sec)
    max_sec = max(durations_sec)
    
    def format_seconds(s):
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    print("--- Del c) Talk time statistics ---")
    print(f"Korteste samtaletid: {format_seconds(min_sec)}")
    print(f"Lengste samtaletid: {format_seconds(max_sec)}\n")

    # --- Del d) Average talk time ---
    avg_sec = sum(durations_sec) / len(durations_sec)
    print("--- Del d) Average talk time ---")
    print(f"Gjennomsnittlig samtaletid: {format_seconds(int(avg_sec))}\n")

    # --- Del e) Inquiries in 2-hour blocks ---
    def get_hour(t):
        if isinstance(t, str):
            return int(t.split(':')[0])
        elif isinstance(t, time):
            return t.hour
        return -1

    hours = [get_hour(t) for t in kl_slett]
    blocks = {
        '08-10': 0,
        '10-12': 0,
        '12-14': 0,
        '14-16': 0
    }
    
    for h in hours:
        if 8 <= h < 10: blocks['08-10'] += 1
        elif 10 <= h < 12: blocks['10-12'] += 1
        elif 12 <= h < 14: blocks['12-14'] += 1
        elif 14 <= h < 16: blocks['14-16'] += 1
        
    labels = list(blocks.keys())
    sizes = list(blocks.values())
    
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    plt.title('Henvendelser fordelt på tidsrom (Uke 24)', fontsize=14)
    plt.savefig('/home/ubuntu/time_blocks.png')
    plt.close()
    
    print("--- Del e) Time block distribution ---")
    for block, count in blocks.items():
        print(f"Tidsrom {block}: {count} henvendelser")
    print("Visualization saved as time_blocks.png\n")

    # --- Del f) Net Promoter Score (NPS) ---
    # Filter out NaN scores
    valid_scores = [s for s in score if not np.isnan(s)]
    total_valid = len(valid_scores)
    
    promoters = sum(1 for s in valid_scores if s >= 9)
    passives = sum(1 for s in valid_scores if 7 <= s <= 8)
    detractors = sum(1 for s in valid_scores if s <= 6)
    
    perc_promoters = (promoters / total_valid) * 100
    perc_detractors = (detractors / total_valid) * 100
    nps = perc_promoters - perc_detractors
    
    print("--- Del f) Net Promoter Score (NPS) ---")
    print(f"Antall gyldige tilbakemeldinger: {total_valid}")
    print(f"Promoters (9-10): {promoters} ({perc_promoters:.1f}%)")
    print(f"Passives (7-8): {passives}")
    print(f"Detractors (1-6): {detractors} ({perc_detractors:.1f}%)")
    print(f"Beregnet NPS: {nps:.1f}")

if __name__ == "__main__":
    solve_project()
