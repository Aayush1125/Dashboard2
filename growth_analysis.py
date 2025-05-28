import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def plot_logest_growth_from_csv(csv_path, category_name):
    # Load historical data
    df = pd.read_csv(csv_path)

    # Ensure expected format
    df = df[df['Year'].astype(str).str.match(r"^\d{4}$")]
    df['Year'] = df['Year'].astype(int)
    df = df[['Year', 'Total']].dropna()
    df.set_index('Year', inplace=True)

    # Interpolate missing years
    all_years = np.arange(df.index.min(), df.index.max() + 1)
    df = df.reindex(all_years)

    for year in df.index[df['Total'].isnull()]:
        prev_year = max(df.index[df.index < year])
        next_year = min(df.index[df.index > year])
        step = (df.loc[next_year, 'Total'] - df.loc[prev_year, 'Total']) / (next_year - prev_year)
        df.loc[year, 'Total'] = df.loc[prev_year, 'Total'] + step * (year - prev_year)

    # Define decades
    min_decade_start = (df.index.min() // 10) * 10 + 1
    decades = []
    year = min_decade_start
    while year + 9 <= 2020:
        decades.append((year, year + 9))
        year += 10
    if df.index.min() < min_decade_start:
        decades[0] = (df.index.min(), decades[0][1])
    if df.index.max() > 2020:
        decades[-1] = (decades[-1][0], df.index.max())

    # Calculate trend growth rates
    decade_growth_rates = {}
    for start, end in decades:
        mask = (df.index >= start) & (df.index <= end)
        x = np.arange(len(df.loc[mask]))
        y = np.log(df.loc[mask, 'Total'])
        slope, _, _, _, _ = linregress(x, y)
        decade_growth_rates[f"{start}-{end}"] = (np.exp(slope) - 1) * 100

    # Overall growth
    x_all = np.arange(len(df))
    y_all = np.log(df['Total'])
    slope_all, _, _, _, _ = linregress(x_all, y_all)
    overall = (np.exp(slope_all) - 1) * 100

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(decade_growth_rates.keys(), decade_growth_rates.values(), label="Decade-wise Trend Growth Rate")
    ax.axhline(overall, color='red', linestyle='--', label=f'Overall Growth Rate ({overall:.2f}%)')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, f"{yval:.2f}%", ha='center', va='bottom')

    ax.set_title(f"Decade-wise Trend Growth Rate for {category_name}")
    ax.set_ylabel("Trend Growth Rate (%)")
    ax.set_xlabel("Decade Range")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
