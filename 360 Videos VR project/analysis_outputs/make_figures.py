import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

BASE = os.path.dirname(__file__)
FIG_DIR = os.path.join(BASE, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

long_df = pd.read_csv(os.path.join(BASE, "long_video_metrics.csv"))
pm = pd.read_csv(os.path.join(BASE, "participant_level_metrics.csv"))

sns.set_theme(style="whitegrid", context="talk")

# 1) PHQ score distribution
plt.figure(figsize=(8, 5))
sns.histplot(pm["score_phq"], bins=12, kde=True, color="#4C72B0")
plt.axvline(10, color="red", linestyle="--", linewidth=2, label="PHQ-9 cutoff = 10")
plt.xlabel("PHQ-9 score")
plt.ylabel("Count")
plt.title("Distribution of PHQ-9 Scores")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig1_phq_distribution.png"), dpi=300)
plt.close()

# 2) Group differences in average rotation speed
plt.figure(figsize=(8, 5))
sns.boxplot(data=pm, x="depr_group", y="rot_speed_avg_total", palette="Set2")
sns.stripplot(data=pm, x="depr_group", y="rot_speed_avg_total", color="black", alpha=0.5, size=4)
plt.xlabel("Depression group (PHQ-9)")
plt.ylabel("Mean rotation speed total")
plt.title("Psychomotor Speed by Depression Group")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig2_speed_by_depression_group.png"), dpi=300)
plt.close()

# 3) PHQ/GAD vs variability
fig, ax = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
sns.regplot(data=pm, x="score_phq", y="circ_sd_mean", ax=ax[0], scatter_kws={"alpha":0.7})
ax[0].set_title("PHQ-9 vs Head-movement Variability")
ax[0].set_xlabel("PHQ-9")
ax[0].set_ylabel("Mean circular SD")

sns.regplot(data=pm, x="score_gad", y="circ_sd_mean", ax=ax[1], scatter_kws={"alpha":0.7}, color="#DD8452")
ax[1].set_title("GAD-7 vs Head-movement Variability")
ax[1].set_xlabel("GAD-7")
ax[1].set_ylabel("")

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig3_symptoms_vs_variability.png"), dpi=300)
plt.close()

# 4) Video-wise speed differences
order = ["v1", "v2", "v3", "v4", "v5"]
plt.figure(figsize=(9, 5))
sns.pointplot(data=long_df, x="video", y="rot_speed_avg_total", order=order, errorbar=("ci", 95), capsize=.2)
plt.xlabel("Video")
plt.ylabel("Rotation speed total")
plt.title("Video-wise Psychomotor Response (Mean ± 95% CI)")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig4_video_speed_pointplot.png"), dpi=300)
plt.close()

# 5) Overall dataset distribution of rotation speed total (all video-level observations)
plt.figure(figsize=(9, 5))
sns.histplot(long_df["rot_speed_avg_total"], bins=20, kde=True, color="#55A868")
plt.xlabel("Rotation speed total")
plt.ylabel("Count")
plt.title("Overall Distribution of Rotation Speed (All Video-level Observations)")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig6_dataset_speed_distribution.png"), dpi=300)
plt.close()

print("Figures written to", FIG_DIR)
