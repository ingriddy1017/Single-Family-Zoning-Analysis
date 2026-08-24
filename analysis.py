"""
analysis.py

Single-Family Zoning & the Housing Crisis -- a small data pipeline built to
accompany the presentation "The U.S. Housing Crisis: Ending Single-Family
Zoning" (Yang, University of Maryland).

What it does:
  1. Loads a regional segregation-index dataset (1880 vs. 1940) and plots
     the increase by U.S. Census region, replicating the pattern in
     Shertzer, Twinam & Walsh (2021).
  2. Loads a six-city dataset of cumulative housing approvals per 1,000
     residents and median rent index (2018-2023) and plots both, comparing
     Minneapolis -- which ended single-family-only zoning citywide in
     2019 -- against peer Midwestern metros.
  3. Reports the correlation between cumulative housing approvals and rent
     growth across the six cities.

Run:
    pip install -r requirements.txt
    python analysis.py

Outputs (written to output/):
    segregation_index_by_region.png
    housing_approvals_by_city.png
    median_rent_index_by_city.png
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=1.0)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BLUE = "#1533C4"
NAVY = "#0B1B63"
CORAL = "#C1502E"
INK = "#14151A"
CITY_COLORS = {
    "Minneapolis": CORAL,
    "Omaha": "#8A8F98",
    "Columbus": "#8A8F98",
    "Kansas City": "#8A8F98",
    "Cincinnati": "#8A8F98",
    "Indianapolis": "#8A8F98",
}


def load_data():
    seg = pd.read_csv(os.path.join(DATA_DIR, "segregation_index_by_region.csv"))
    housing = pd.read_csv(os.path.join(DATA_DIR, "housing_approvals_rent.csv"))
    return seg, housing


def plot_segregation(seg: pd.DataFrame):
    seg = seg.copy()
    seg["increase"] = seg["segregation_index_1940"] - seg["segregation_index_1880"]
    seg = seg.sort_values("increase", ascending=True)

    x = np.arange(len(seg))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(x - width / 2, seg["segregation_index_1880"], height=width, color=BLUE, label="1880")
    ax.barh(x + width / 2, seg["segregation_index_1940"], height=width, color=CORAL, label="1940")
    ax.set_yticks(x)
    ax.set_yticklabels(seg["region"])
    ax.set_xlabel("Segregation index")
    ax.set_title(
        "Residential segregation roughly doubled, 1880-1940\n"
        "(approximated from Shertzer, Twinam & Walsh, 2021 -- see README)",
        fontsize=13, fontweight="bold", loc="left"
    )
    ax.legend(loc="lower right")
    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "segregation_index_by_region.png")
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"Saved {out_path}")

    print("\nSegregation index increase by region (1880 -> 1940):")
    print(seg[["region", "segregation_index_1880", "segregation_index_1940", "increase"]]
          .sort_values("increase", ascending=False).to_string(index=False))


def plot_housing_approvals(housing: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 6))
    for city, group in housing.groupby("city"):
        color = CITY_COLORS.get(city, "#8A8F98")
        lw = 2.6 if city == "Minneapolis" else 1.4
        ax.plot(group["year"], group["cumulative_dwelling_approvals_per_1000"],
                label=city, color=color, linewidth=lw)

    ax.set_xlabel("Year")
    ax.set_ylabel("Cumulative new dwelling approvals per 1,000 residents")
    ax.set_title(
        "Minneapolis built more housing than peer Midwestern metros\n"
        "after ending single-family-only zoning citywide in 2019",
        fontsize=13, fontweight="bold", loc="left"
    )
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "housing_approvals_by_city.png")
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"Saved {out_path}")


def plot_rent_index(housing: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 6))
    for city, group in housing.groupby("city"):
        color = CITY_COLORS.get(city, "#8A8F98")
        lw = 2.6 if city == "Minneapolis" else 1.4
        ax.plot(group["year"], group["median_rent_index"],
                label=city, color=color, linewidth=lw)

    ax.axhline(100, color="#B8B4A6", linewidth=1, linestyle="--")
    ax.set_xlabel("Year")
    ax.set_ylabel("Median rent index (Jan 2018 = 100)")
    ax.set_title(
        "...and rents fell relative to peer cities as supply increased",
        fontsize=13, fontweight="bold", loc="left"
    )
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "median_rent_index_by_city.png")
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"Saved {out_path}")


def report_correlation(housing: pd.DataFrame):
    totals = housing.groupby("city").agg(
        total_approvals=("cumulative_dwelling_approvals_per_1000", "max"),
        final_rent_index=("median_rent_index", "last"),
    )
    corr = totals["total_approvals"].corr(totals["final_rent_index"])
    print("\n--- Approvals vs. rent growth across 6 cities ---")
    print(totals.to_string())
    print(f"\nCorrelation (total approvals vs. final rent index): {corr:.2f}")
    print(
        "A negative correlation here means cities that approved more new "
        "housing per resident tended to see relatively lower rent growth -- "
        "consistent with the presentation's 'missing middle' argument."
    )


def main():
    seg, housing = load_data()
    plot_segregation(seg)
    plot_housing_approvals(housing)
    plot_rent_index(housing)
    report_correlation(housing)


if __name__ == "__main__":
    main()
