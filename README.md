# Single-Family Zoning & the Housing Crisis — Data Analysis

A small Python data pipeline built to accompany the presentation
**"The U.S. Housing Crisis: Ending Single-Family Zoning"** (Yang,
University of Maryland). It turns the presentation's two central claims
into runnable, chartable analysis:

1. Single-family-only zoning has deep roots in residential segregation —
   segregation indices roughly doubled across U.S. regions between 1880
   and 1940.
2. Cities that reform restrictive zoning build more housing and see
   relatively slower rent growth — using Minneapolis (which ended
   single-family-only zoning citywide in 2019) against five peer
   Midwestern metros as a case study.

## What's here

- **`data/segregation_index_by_region.csv`** — segregation index by U.S.
  Census region, 1880 vs. 1940.
- **`data/housing_approvals_rent.csv`** — cumulative new dwelling
  approvals per 1,000 residents and a median rent index (2018 = 100),
  2018–2023, for Minneapolis, Omaha, Columbus, Kansas City, Cincinnati,
  and Indianapolis.
- **`analysis.py`** — loads both datasets, produces three charts, and
  reports the correlation between housing approvals and rent growth
  across the six cities.
- **`output/`** — generated charts (PNG).

## Running it

```bash
pip install -r requirements.txt
python analysis.py
```

This writes three charts to `output/`:

- `segregation_index_by_region.png` — 1880 vs. 1940 segregation index by
  region
- `housing_approvals_by_city.png` — cumulative housing approvals,
  Minneapolis vs. peer metros
- `median_rent_index_by_city.png` — median rent index over the same
  period

## A note on the data

- `segregation_index_by_region.csv` values are **approximated by reading
  the published chart** in Shertzer, Twinam & Walsh (2021) — they are not
  the authors' exact replication data. For exact figures, request the
  replication files from the *Regional Science and Urban Economics*
  supplementary materials.
- `housing_approvals_rent.csv` is **illustrative**, shaped to match the
  pattern reported in reporting on Minneapolis's 2040 Plan (ending
  single-family-only zoning citywide in 2019) relative to peer cities.
  For a research-grade version, pull real permitting data from the
  Census Bureau's Building Permits Survey and rent data from Zillow's
  Observed Rent Index (ZORI) or Apartment List's national rent estimates.

## Sources

1. Shertzer, A., Twinam, T., & Walsh, R. P. (2021). Zoning and segregation
   in urban economic history. *Regional Science and Urban Economics*.
2. Wegmann, J. (2019). Death to single-family zoning... and new life to
   the missing middle. *Journal of the American Planning Association*.
3. von Hoffman, A. (2021). Single-family zoning: Can history be reversed?
   Joint Center for Housing Studies, Harvard University.
4. Hanley, A. (2024). Rethinking zoning to increase affordable housing.
   NAHRO Journal.

Full source list in the original presentation
(`housing-crisis-presentation.pdf` in the portfolio).

## License

MIT — reuse freely, attribution appreciated.
