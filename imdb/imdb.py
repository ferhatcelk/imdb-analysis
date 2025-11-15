#!/usr/bin/env python3
"""
imdb.py
IMDb Film Veri Seti Analizi - movies_initial.csv ile çalışmak üzere hazırlanmıştır.

Aşamalar:
1) Veri Yükleme ve Temizleme
2) Keşifsel Veri Analizi (EDA)
3) Görselleştirmeler (Matplotlib)
4) Rapor (Markdown + kaydedilmiş görseller)

Kullanım:
- Bu dosyayı movies_initial.csv ile aynı klasöre koyun (varsayılan: movies_initial.csv)
- python imdb.py
- Çıktılar ./output altında saklanacaktır.

Gerekli paketler: pandas, numpy, matplotlib
"""
import os, re
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

INPUT_CSV = "movies_initial.csv"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data(path=INPUT_CSV):
    print("Loading", path)
    df = pd.read_csv(path)
    print("Loaded shape:", df.shape)
    return df

def clean_data(df):
    df = df.copy()
    # Standardize column names (trim)
    df.columns = [c.strip() for c in df.columns]
    # rating: convert to numeric where possible; handle common non-numeric labels
    def clean_rating(x):
        try:
            return float(x)
        except:
            if pd.isna(x): return np.nan
            s = str(x).strip().upper()
            if s in ("NOT RATED","UNRATED","N/A","NA","NONE","TBD","NOT RATED/NOT RATED"):
                return np.nan
            m = re.search(r"(\d+(\.\d+)?)", s)
            return float(m.group(1)) if m else np.nan
    if 'rating' in df.columns:
        df['rating'] = df['rating'].map(clean_rating)
    else:
        df['rating'] = np.nan

    # runtime: extract integer minutes
    def clean_runtime(x):
        if pd.isna(x): return np.nan
        s = str(x)
        m = re.search(r"(\d+)", s)
        return int(m.group(1)) if m else np.nan
    for col in ['runtime','Runtime']:
        if col in df.columns:
            df['runtime_min'] = df[col].map(clean_runtime)
            break
    if 'runtime_min' not in df.columns:
        df['runtime_min'] = np.nan

    # year to numeric if possible
    if 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')

    # lastupdated to datetime
    if 'lastupdated' in df.columns:
        df['lastupdated'] = pd.to_datetime(df['lastupdated'], errors='coerce')

    # genre: explode into list
    if 'genre' in df.columns:
        df['genre_list'] = df['genre'].fillna('').astype(str).apply(lambda s: [g.strip() for g in re.split('[,;/|]', s) if g.strip()])
    else:
        df['genre_list'] = [[] for _ in range(len(df))]

    # director: ensure string
    if 'director' in df.columns:
        df['director'] = df['director'].fillna('').astype(str)
    # title trim
    if 'title' in df.columns:
        df['title'] = df['title'].astype(str).str.strip()

    # drop duplicates
    if 'imdbID' in df.columns:
        df = df.drop_duplicates(subset=['imdbID'])
    else:
        df = df.drop_duplicates(subset=['title','year'])
    df.reset_index(drop=True, inplace=True)
    print("After cleaning shape:", df.shape)
    return df

def basic_stats(df):
    stats = {}
    stats['num_movies'] = int(len(df))
    stats['years_range'] = (int(df['year'].min()) if df['year'].notna().any() else None,
                            int(df['year'].max()) if df['year'].notna().any() else None)
    stats['rating_mean'] = float(df['rating'].mean(skipna=True)) if df['rating'].notna().any() else None
    stats['rating_median'] = float(df['rating'].median(skipna=True)) if df['rating'].notna().any() else None
    stats['runtime_mean'] = float(df['runtime_min'].mean(skipna=True)) if df['runtime_min'].notna().any() else None
    stats['runtime_median'] = float(df['runtime_min'].median(skipna=True)) if df['runtime_min'].notna().any() else None
    return stats

def top_genres(df, top_n=10):
    cnt = Counter()
    for lst in df['genre_list']:
        cnt.update(lst)
    return cnt.most_common(top_n)

def top_directors_by_count(df, top_n=15):
    if 'director' not in df.columns:
        return []
    names = df['director'].fillna('')
    cnt = Counter(names[names!=''])
    return cnt.most_common(top_n)

def top_directors_by_rating(df, top_n=15, min_movies=3):
    if 'director' not in df.columns:
        return pd.DataFrame()
    agg = df[df['director']!=''].groupby('director').agg({'rating':['mean','count']})
    agg.columns = ['rating_mean','count']
    agg = agg[agg['count']>=min_movies].sort_values('rating_mean', ascending=False).head(top_n)
    return agg.reset_index()

def plot_rating_distribution(df):
    plt.figure(figsize=(8,5))
    vals = df['rating'].dropna()
    plt.hist(vals, bins=20)
    plt.title("Rating Distribution")
    plt.xlabel("IMDb Rating")
    plt.ylabel("Count")
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "rating_distribution.png")
    plt.savefig(out)
    plt.close()
    print("Saved", out)
    return out

def plot_runtime_hist(df):
    plt.figure(figsize=(8,5))
    vals = df['runtime_min'].dropna()
    plt.hist(vals, bins=30)
    plt.title("Runtime (minutes) Distribution")
    plt.xlabel("Minutes")
    plt.ylabel("Count")
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "runtime_distribution.png")
    plt.savefig(out)
    plt.close()
    print("Saved", out)
    return out

def plot_top_genres(df, top_n=10):
    tg = top_genres(df, top_n=top_n)
    if not tg: return None
    genres, counts = zip(*tg)
    plt.figure(figsize=(10,5))
    plt.bar(genres, counts)
    plt.xticks(rotation=45, ha='right')
    plt.title(f"Top {top_n} Genres by Movie Count")
    plt.ylabel("Count")
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "top_genres.png")
    plt.savefig(out)
    plt.close()
    print("Saved", out)
    return out

def plot_rating_vs_runtime(df):
    plt.figure(figsize=(8,6))
    sub = df[['rating','runtime_min']].dropna()
    plt.scatter(sub['runtime_min'], sub['rating'], alpha=0.5, s=8)
    plt.xlabel("Runtime (min)")
    plt.ylabel("Rating")
    plt.title("Rating vs Runtime")
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "rating_vs_runtime.png")
    plt.savefig(out)
    plt.close()
    print("Saved", out)
    return out

def plot_boxplot_ratings_by_top_genres(df, top_n=6):
    tg = [g for g,_ in top_genres(df, top_n=top_n)]
    data = []
    labels = []
    for g in tg:
        vals = df[df['genre_list'].apply(lambda lst: g in lst)]['rating'].dropna()
        if len(vals)>0:
            data.append(vals)
            labels.append(g)
    if not data: return None
    plt.figure(figsize=(10,6))
    plt.boxplot(data, labels=labels, patch_artist=True)
    plt.title("Ratings by Genre (Top Genres)")
    plt.ylabel("Rating")
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "boxplot_ratings_by_genre.png")
    plt.savefig(out)
    plt.close()
    print("Saved", out)
    return out

def summarize_and_save_report(df, stats, plots, top_dirs_count, top_dirs_rating, top_genres_list):
    report_lines = []
    report_lines.append("# IMDb Dataset Analysis Report\n")
    report_lines.append(f"Generated: {datetime.utcnow().isoformat()} UTC\n\n")
    report_lines.append("## Basic statistics\n")
    for k,v in stats.items():
        report_lines.append(f"- **{k}**: {v}\n")
    report_lines.append("\n## Top genres\n")
    for g,c in top_genres_list:
        report_lines.append(f"- {g}: {c}\n")
    report_lines.append("\n## Top directors by movie count\n")
    for name,c in top_dirs_count:
        report_lines.append(f"- {name}: {c}\n")
    report_lines.append("\n## Top directors by average rating (min movies threshold applied)\n")
    report_lines.append(top_dirs_rating.to_markdown(index=False) if hasattr(top_dirs_rating,'to_markdown') else str(top_dirs_rating))
    report_lines.append("\n## Plots\n")
    for p in plots:
        if p: report_lines.append(f"- {os.path.basename(p)}\n")
    report_text = "\n".join(report_lines)
    out_md = os.path.join(OUTPUT_DIR, "report.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(report_text)
    print("Saved report to", out_md)
    return out_md

def main():
    df = load_data(INPUT_CSV)
    df = clean_data(df)
    stats = basic_stats(df)
    tg = top_genres(df, top_n=15)
    td_count = top_directors_by_count(df, top_n=20)
    td_rating = top_directors_by_rating(df, top_n=20, min_movies=3)
    # Plots
    plots = []
    plots.append(plot_rating_distribution(df))
    plots.append(plot_runtime_hist(df))
    plots.append(plot_top_genres(df, top_n=15))
    plots.append(plot_rating_vs_runtime(df))
    plots.append(plot_boxplot_ratings_by_top_genres(df, top_n=8))
    # Save cleaned CSV sample
    cleaned_csv = os.path.join(OUTPUT_DIR, "movies_cleaned_sample.csv")
    df.head(1000).to_csv(cleaned_csv, index=False)
    print("Saved cleaned sample to", cleaned_csv)
    # Save report
    report = summarize_and_save_report(df, stats, plots, td_count, td_rating, tg)
    print("Done. Outputs in", OUTPUT_DIR)

if __name__ == "__main__":
    main()
