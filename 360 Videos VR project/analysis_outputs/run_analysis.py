import os
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.anova import AnovaRM

BASE = os.path.dirname(os.path.dirname(__file__))

main = pd.read_excel(os.path.join(BASE, "data", "data.xlsx"))

records = []
for vid in ["v1", "v2", "v3", "v4", "v5"]:
    for _, row in main[["participant", vid]].dropna().iterrows():
        fname = str(row[vid]).strip()
        fpath = os.path.join(BASE, "data", "headtracking-data", vid, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        parts = lines[-1].split(",")
        try:
            records.append(
                {
                    "participant": row["participant"],
                    "video": vid,
                    "file": fname,
                    "circ_avg_x": float(parts[1]),
                    "circ_avg_y": float(parts[2]),
                    "circ_avg_z": float(parts[3]),
                    "circ_sd_x": float(parts[5]),
                    "circ_sd_y": float(parts[6]),
                    "circ_sd_z": float(parts[7]),
                    "rot_speed_avg_x": float(parts[9]),
                    "rot_speed_avg_y": float(parts[10]),
                    "rot_speed_avg_z": float(parts[11]),
                    "rot_speed_avg_total": float(parts[12]),
                }
            )
        except (IndexError, ValueError):
            continue

ht = pd.DataFrame(records)

keep_cols = [
    "participant",
    "score_phq",
    "score_gad",
    "score_stai_t",
    "score_vrise",
    "age",
    "gender",
    "vr_experience",
]
long_df = ht.merge(main[keep_cols], on="participant", how="left")

# IQR outliers per video
outlier_frames = []
for vid, grp in long_df.groupby("video"):
    q1, q3 = np.percentile(grp["rot_speed_avg_total"], [25, 75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outlier_frames.append(
        grp[
            (grp["rot_speed_avg_total"] < lo)
            | (grp["rot_speed_avg_total"] > hi)
        ][["participant", "video", "rot_speed_avg_total"]]
    )
outliers = pd.concat(outlier_frames, ignore_index=True)

pm = (
    long_df.groupby("participant")
    .agg(
        {
            "rot_speed_avg_total": "mean",
            "circ_sd_x": "mean",
            "circ_sd_y": "mean",
            "circ_sd_z": "mean",
            "score_phq": "first",
            "score_gad": "first",
            "score_stai_t": "first",
            "score_vrise": "first",
            "age": "first",
        }
    )
    .reset_index()
)
pm["circ_sd_mean"] = pm[["circ_sd_x", "circ_sd_y", "circ_sd_z"]].mean(axis=1)
pm["depr_group"] = np.where(pm["score_phq"] >= 10, "elevated_depression", "low_depression")

# Group t-tests
group_tests = []
for metric in ["rot_speed_avg_total", "circ_sd_mean"]:
    a = pm.loc[pm["depr_group"] == "elevated_depression", metric].dropna()
    b = pm.loc[pm["depr_group"] == "low_depression", metric].dropna()
    t_stat, p_val = stats.ttest_ind(a, b, equal_var=False)
    pooled_sd = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    cohen_d = (a.mean() - b.mean()) / pooled_sd
    group_tests.append(
        {
            "metric": metric,
            "n_elevated": len(a),
            "n_low": len(b),
            "mean_elevated": a.mean(),
            "mean_low": b.mean(),
            "t": t_stat,
            "p": p_val,
            "cohen_d": cohen_d,
        }
    )
group_tests = pd.DataFrame(group_tests)

# Correlations
corr_rows = []
for metric in ["rot_speed_avg_total", "circ_sd_mean"]:
    r_phq, p_phq = stats.pearsonr(pm["score_phq"], pm[metric])
    r_gad, p_gad = stats.pearsonr(pm["score_gad"], pm[metric])
    corr_rows.append(
        {
            "metric": metric,
            "r_phq": r_phq,
            "p_phq": p_phq,
            "r_gad": r_gad,
            "p_gad": p_gad,
        }
    )
correlations = pd.DataFrame(corr_rows)

# Regression controlling anxiety
reg_rows = []
for metric in ["rot_speed_avg_total", "circ_sd_mean"]:
    X = sm.add_constant(pm[["score_phq", "score_gad"]])
    y = pm[metric]
    model = sm.OLS(y, X).fit()
    reg_rows.append(
        {
            "metric": metric,
            "beta_const": model.params["const"],
            "beta_phq": model.params["score_phq"],
            "p_phq": model.pvalues["score_phq"],
            "beta_gad": model.params["score_gad"],
            "p_gad": model.pvalues["score_gad"],
            "r2": model.rsquared,
        }
    )
regression = pd.DataFrame(reg_rows)

# Repeated-measures ANOVA and pairwise tests
anova_data = long_df[["participant", "video", "rot_speed_avg_total"]].dropna()
anova = AnovaRM(anova_data, depvar="rot_speed_avg_total", subject="participant", within=["video"]).fit()

wide = long_df.pivot_table(index="participant", columns="video", values="rot_speed_avg_total", aggfunc="mean")
videos = ["v1", "v2", "v3", "v4", "v5"]
pair_rows = []
raw_p = []
for i in range(len(videos)):
    for j in range(i + 1, len(videos)):
        a, b = videos[i], videos[j]
        tmp = wide[[a, b]].dropna()
        t_stat, p_val = stats.ttest_rel(tmp[a], tmp[b])
        pair_rows.append(
            {
                "video_a": a,
                "video_b": b,
                "n": len(tmp),
                "mean_a": tmp[a].mean(),
                "mean_b": tmp[b].mean(),
                "t": t_stat,
                "p_raw": p_val,
            }
        )
        raw_p.append(p_val)

reject, p_adj, _, _ = multipletests(raw_p, alpha=0.05, method="bonferroni")
for idx in range(len(pair_rows)):
    pair_rows[idx]["p_bonf"] = p_adj[idx]
    pair_rows[idx]["significant_bonf"] = bool(reject[idx])
pairs = pd.DataFrame(pair_rows)

video_desc = long_df.groupby("video")["rot_speed_avg_total"].agg(["mean", "std", "min", "max", "count"]).reset_index()

phq_gad_r, phq_gad_p = stats.pearsonr(pm["score_phq"], pm["score_gad"])

out_dir = os.path.dirname(__file__)
os.makedirs(out_dir, exist_ok=True)

pm.to_csv(os.path.join(out_dir, "participant_level_metrics.csv"), index=False)
long_df.to_csv(os.path.join(out_dir, "long_video_metrics.csv"), index=False)
outliers.to_csv(os.path.join(out_dir, "outliers_speed_iqr.csv"), index=False)
group_tests.to_csv(os.path.join(out_dir, "group_tests.csv"), index=False)
correlations.to_csv(os.path.join(out_dir, "correlations.csv"), index=False)
regression.to_csv(os.path.join(out_dir, "regression_controls.csv"), index=False)
pairs.to_csv(os.path.join(out_dir, "pairwise_video_tests_bonferroni.csv"), index=False)
video_desc.to_csv(os.path.join(out_dir, "video_speed_descriptives.csv"), index=False)

with open(os.path.join(out_dir, "anova_speed.txt"), "w", encoding="utf-8") as f:
    f.write(str(anova))

with open(os.path.join(out_dir, "key_summary.txt"), "w", encoding="utf-8") as f:
    f.write(f"n_participants={len(pm)}\n")
    f.write(f"n_video_rows={len(long_df)}\n")
    f.write(f"outlier_rows={len(outliers)}\n")
    f.write(f"group_counts={pm['depr_group'].value_counts().to_dict()}\n")
    f.write(f"phq_gad_r={phq_gad_r:.4f}, p={phq_gad_p:.6f}\n")

print("Analysis complete.")
print(f"n_participants={len(pm)}, n_video_rows={len(long_df)}, outlier_rows={len(outliers)}")
print(f"group_counts={pm['depr_group'].value_counts().to_dict()}")
print(f"phq_gad_r={phq_gad_r:.4f}, p={phq_gad_p:.6f}")
print("Outputs written to:", out_dir)
