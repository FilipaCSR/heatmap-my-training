import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, Normalize
import calendar

def plot_training_heatmap(df_exercise, year=2024, vmin=0, vmax=None):
    df = df_exercise[df_exercise['year'] == year].copy()

    # Pivot table: months as rows, days as columns
    pivot_df = df.pivot_table(index='month', columns='day', values='n', fill_value=0)

    # Reorder months (Jan to Dec, top to bottom)
    month_order = list(calendar.month_abbr)[1:]
    pivot_df = pivot_df.reindex(month_order)

    # Apple-inspired blues
    apple_cool_blues = ["#e6f0ff", "#99ccff", "#4d94ff", "#1a75ff", "#003380"]
    apple_cmap = LinearSegmentedColormap.from_list("apple_blues", apple_cool_blues)

    # 📏 Smaller figure size
    plt.figure(figsize=(9, 4))  # Was (18, 8)

    sns.set_theme(style="whitegrid")
    ax = sns.heatmap(
        pivot_df,
        cmap=apple_cmap,
        linewidths=0.3,
        linecolor='white',
        cbar_kws={
            'label': 'Minutes of Exercise',
            'shrink': 0.7,
            'orientation': 'vertical'
        },
        norm=Normalize(vmin=vmin, vmax=vmax if vmax is not None else df['n'].max())
    )

    # ✨ Streamlined styling
    plt.title(f"Exercise Heatmap – {year}", fontsize=14, pad=10, weight='medium', color='#1a1a1a')
    plt.xlabel("Day", fontsize=10, labelpad=6)
    plt.ylabel("Month", fontsize=10)
    plt.xticks(rotation=0, fontsize=8)
    plt.yticks(rotation=0, fontsize=9)
    plt.grid(False)
    plt.tight_layout()

    return plt.gcf()
