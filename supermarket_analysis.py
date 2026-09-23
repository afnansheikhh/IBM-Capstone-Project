#!/usr/bin/env python3
import csv
import os
from collections import defaultdict

DATASET_PATH = "/Users/afnansheikh/Downloads/IBM Capstone Project/SUPER MARKET DATA - supermarket_sales_500_rows.csv"

def step1_load_dataset(filepath):
    rows = []
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows, reader.fieldnames

def step2_check_data_quality(rows):
    missing_counts = defaultdict(int)
    invalid_records = []
    
    for idx, r in enumerate(rows, start=2):
        for col, val in r.items():
            if val is None or val.strip() == "":
                missing_counts[col] += 1
        
        try:
            qty = int(r["Quantity"])
            unit_price = float(r["Unit Price"])
            rating = float(r["Rating"])
            sales = float(r["Sales"])
            
            if qty <= 0:
                invalid_records.append((idx, "Quantity <= 0", r))
            if unit_price <= 0:
                invalid_records.append((idx, "Unit Price <= 0", r))
            if not (1.0 <= rating <= 5.0):
                invalid_records.append((idx, "Rating out of range [1, 5]", r))
        except ValueError as e:
            invalid_records.append((idx, f"Parsing Error: {e}", r))

    return missing_counts, invalid_records

def step3_calculate_sales(rows):
    discrepancies = []
    for idx, r in enumerate(rows, start=2):
        qty = int(r["Quantity"])
        unit_price = float(r["Unit Price"])
        existing_sales = float(r["Sales"])
        
        calculated_sales = round(qty * unit_price, 2)
        r["Calculated_Sales"] = calculated_sales
        
        if abs(calculated_sales - round(existing_sales, 2)) > 0.05:
            discrepancies.append((idx, r["Invoice ID"], qty, unit_price, existing_sales, calculated_sales))
    return discrepancies

def step4_group_and_summarize(rows):
    total_sales = sum(r["Calculated_Sales"] for r in rows)
    total_qty = sum(int(r["Quantity"]) for r in rows)
    avg_rating_overall = sum(float(r["Rating"]) for r in rows) / len(rows)
    avg_order_value = total_sales / len(rows)

    def summarize_by(key_fn):
        grouped = defaultdict(lambda: {"count": 0, "total_sales": 0.0, "total_qty": 0, "ratings": []})
        for r in rows:
            k = key_fn(r)
            s = r["Calculated_Sales"]
            q = int(r["Quantity"])
            rate = float(r["Rating"])
            grouped[k]["count"] += 1
            grouped[k]["total_sales"] += s
            grouped[k]["total_qty"] += q
            grouped[k]["ratings"].append(rate)
        
        result = []
        for k, stats in sorted(grouped.items(), key=lambda x: x[1]["total_sales"], reverse=True):
            avg_s = stats["total_sales"] / stats["count"]
            avg_r = sum(stats["ratings"]) / len(stats["ratings"])
            share = (stats["total_sales"] / total_sales) * 100
            result.append({
                "group": k,
                "count": stats["count"],
                "units": stats["total_qty"],
                "total_sales": round(stats["total_sales"], 2),
                "avg_sales": round(avg_s, 2),
                "avg_rating": round(avg_r, 2),
                "share_pct": round(share, 2)
            })
        return result

    return {
        "overall": {
            "total_transactions": len(rows),
            "total_qty": total_qty,
            "total_sales": round(total_sales, 2),
            "avg_order_value": round(avg_order_value, 2),
            "avg_rating": round(avg_rating_overall, 2)
        },
        "category": summarize_by(lambda r: r["Category"]),
        "city": summarize_by(lambda r: f"{r['City']} ({r['Branch']})"),
        "customer": summarize_by(lambda r: r["Customer Type"]),
        "payment": summarize_by(lambda r: r["Payment"]),
        "gender": summarize_by(lambda r: r["Gender"]),
        "product": summarize_by(lambda r: r["Product"])
    }

def main():
    rows, fields = step1_load_dataset(DATASET_PATH)
    missing, invalid = step2_check_data_quality(rows)
    discrepancies = step3_calculate_sales(rows)
    summaries = step4_group_and_summarize(rows)
    
    # Also save to the user's workspace
    import shutil
    dest = "/Users/afnansheikh/Downloads/IBM Capstone Project/supermarket_analysis.py"
    shutil.copyfile(__file__, dest)
    print(f"Copied script to {dest}")
    print("Execution complete.")

if __name__ == "__main__":
    main()
