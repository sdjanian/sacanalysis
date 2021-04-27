import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import os
from sacanalysis import __plotRankedSaccadesArticle as plotRankedSaccadesArticle
from sacanalysis import __plotRankedSaccadesAndDistributionsArticle as plotRankedSaccadesAndDistributionsArticle

#from main import GetCorrectTransformationToUseInAnalysis
plt.style.use("seaborn")


def savefig(path:str,save_folder = "article_plots") -> None:
    if not os.path.isdir(save_folder):
        os.makedirs(save_folder)      
    plt.savefig(save_folder+"\\"+path+".pdf",bbox_inches = "tight")

### Average composite saccade plot
average_saccade_20 = pd.read_csv(r"..\output\average_saccade_20ms.csv")
average_saccade_100 = pd.read_csv(r"..\output\average_saccade_100ms.csv")

plt.close()
fig, axes = plt.subplots(3,2,figsize=(8,9))
fig.suptitle('Average composite saccades',y=0.98, fontsize=18)

x_axis_lim_20 = [0,5]
axes[0,0].plot(average_saccade_20.index,average_saccade_20["x_norm_up"])
axes[0,0].set_title("20 ms")
axes[0,0].set(ylabel="Horizontal position (deg)")
axes[0,0].set_xlim(x_axis_lim_20)
axes[0,0].axes.xaxis.set_ticklabels([])

axes[1,0].plot(average_saccade_20.index,average_saccade_20["velocity_norm"])
#axes[1,0].set_title("Velocity")
axes[1,0].set(ylabel="Velocity (deg/s)")
axes[1,0].set_xlim(x_axis_lim_20)
axes[1,0].axes.xaxis.set_ticklabels([])


axes[2,0].plot(average_saccade_20.index,average_saccade_20["x_z_trans"])
#axes[2,0].set_title("Z-transform horizontal")
axes[2,0].set(ylabel="Z-transform horizontal (deg)")
axes[2,0].set_xlim(x_axis_lim_20)

x_axis_lim_100 = [0,25]

axes[0,1].plot(average_saccade_100.index,average_saccade_100["x_norm_up"])
axes[0,1].set_title("100 ms")
axes[0,1].set_xlim(x_axis_lim_100)
axes[0,1].axes.xaxis.set_ticklabels([])

axes[1,1].plot(average_saccade_100.index,average_saccade_100["velocity_norm"])
axes[1,1].set_xlim(x_axis_lim_100)
axes[1,1].axes.xaxis.set_ticklabels([])

axes[2,1].plot(average_saccade_100.index,average_saccade_100["x_z_trans"])
axes[2,1].set_xlim(x_axis_lim_100)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.text(0.5, 0.01, 'Sample number', ha='center')

savefig("average_composite_saccades_20_100ms")


### Velocity histogram plot
colors = plt.cm.tab20(range(2))
velocity_vector_df = pd.read_json(r"..\output\velocity_vectors_100ms.json")
velocity_vector = velocity_vector_df["vector"].iloc[0]
velocity = velocity_vector_df.drop(["unique_saccade_number","vector"],axis=1).iloc[0].values
bins = np.arange(-0.5,len(velocity)+0.5)
plt.figure()
plt.plot(velocity,linestyle='-', marker='o',color=colors[0])
plt.hist(velocity_vector,bins=bins,color = colors[1])
plt.title("Histogram of velocity",fontsize=18)
plt.ylabel("Velocity (Deg/s)")
plt.xlabel("Sample number")
savefig("velocity_histogram")

### Top and bottom ranked for each metric
# 52 ms saccades
processed_saccade_52 = pd.read_csv(r"..\output\horizontal_saccades_with_score_52ms.csv")
average_saccade_52 = pd.read_csv(r"..\output\average_saccade_52ms.csv")
scores_52 = pd.read_json(r"..\output\scores_52ms.json")
average_saccade_52.index = list(average_saccade_52.index*4)
def GetCorrectTransformationToUseInAnalysis2(score_column:str) -> str:
    if any(map(lambda x: x in  score_column,["main", "velocity","x_norm_up","velocity","dip","entropy","skew","kurtosis","bf"])):
        transformation_column = "x_norm_up"
    elif any(map(lambda x: x in  score_column,["x_z_trans", "flatness"])):
        transformation_column = "x_z_trans"
    return transformation_column

def plotTopBottomRankedMetrics(processed_saccades,average_saccade,score,
                               suptitle="",metric="",iloc_of_scores=[0,1,2,3,-4,-3,-2,-1],list_of_ranks_to_plot=[]):
    score = score[score[metric].notna()]
    processed_saccades = processed_saccades[processed_saccades["unique_saccade_number"].isin(score["unique_saccade_number"])]
    score_sorted = score.sort_values(by=metric).iloc[iloc_of_scores]
    transform = GetCorrectTransformationToUseInAnalysis2(metric)
    #processed_saccade_extracted = processed_saccades[processed_saccades["unique_saccade_number"].isin(score_sorted["unique_saccade_number"])]
    axlist = plotRankedSaccadesAndDistributionsArticle(processed_saccades,average_saccade[transform],score_sorted,"article_plots",saccade_pos_col=transform,
                           sup_title=suptitle,metric=metric,_nrow=3,_ncol=4,_figsize=(6,6),num_of_ranks=len(score),list_of_ranks_to_plot=list_of_ranks_to_plot)
    axlist[1].hist(score[metric])

#list_of_indexes_to_plot = [1,2,3,4,len(scores_52)-3,len(scores_52)-2,len(scores_52)-1,len(scores_52)]
metric_name_param = [("Residual sum of position","residual_sum_x_norm_up",),
                     ("Residual sum of z-score position","residual_sum_x_z_trans"),
                     ("Residual sum of velocity","residual_sum_velocity"),
                     ("Flatness","flatness_score"),
                     ("Dipvalue","dipvalue_score"),
                     ("Entropy","entropy_score"),
                     ("Kurtosis","kurtosis_score"),
                     ("Skewness","skew_score"),
                     ("Bayes Factor","bfvalue_score")]

scores_52 = scores_52.replace([np.inf, -np.inf], np.nan)
for title, metric in  metric_name_param:
   scores_without_na = scores_52[scores_52[metric].notna()]
   list_of_indexes_to_plot = [1,2,3,4,len(scores_without_na)-3,len(scores_without_na)-2,len(scores_without_na)-1,len(scores_without_na)]
   plotTopBottomRankedMetrics(processed_saccade_52,average_saccade_52,scores_52,
                           suptitle=title,metric=metric,
                           list_of_ranks_to_plot=list_of_indexes_to_plot) 
   savefig(metric)




#### Testing how the BF value is at both ends of the scale
scores_test = scores_52.replace([np.inf, -np.inf], np.nan)
processed_saccade_test = processed_saccade_52[processed_saccade_52["unique_saccade_number"].isin(scores_52["unique_saccade_number"])]
scores_test = scores_test[scores_52["bfvalue_score"].notna()]
scores_test = scores_test.sort_values(by="bfvalue_score")

worst_bf = scores_test.iloc[-1]
best_bf = scores_test.iloc[1]
fig_test = plt.figure()
best_bf_saccades = processed_saccade_test[processed_saccade_test["unique_saccade_number"]==best_bf["unique_saccade_number"]]

ax1 = plt.subplot2grid((2,3),(0,0)) 
ax1.plot(best_bf_saccades["norm_time"],best_bf_saccades["x"])
ax1.set_title("X pos")
ax1.set_xlabel("ms")
ax1.set_ylabel("deg")

ax2 = plt.subplot2grid((2,3),(0,1)) 
ax2.plot(best_bf_saccades["norm_time"],best_bf_saccades["y"])
ax2.set_title("Y pos")
ax2.set_xlabel("ms")
ax2.set_ylabel("deg")

bins = np.arange(-0.5,len(best_bf_saccades["velocity_norm"])+0.5)
ax3 = plt.subplot2grid((2,3),(0,2)) 
ax3.plot(best_bf_saccades["norm_time"]/4,best_bf_saccades["velocity"])
ax3.hist(best_bf["vector"],bins=bins)
ax3.set_title("Histogram of velocity")
ax3.set_ylabel("deg/s")
ax3.set_xlabel("Sample nr.")

worst_bf_saccades = processed_saccade_test[processed_saccade_test["unique_saccade_number"]==worst_bf["unique_saccade_number"]]

ax1 = plt.subplot2grid((2,3),(1,0)) 
ax1.plot(worst_bf_saccades["norm_time"],worst_bf_saccades["x"])
ax1.set_title("X pos")
ax1.set_xlabel("ms")
ax1.set_ylabel("deg")

ax2 = plt.subplot2grid((2,3),(1,1)) 
ax2.plot(worst_bf_saccades["norm_time"],worst_bf_saccades["y"])
ax2.set_title("Y pos")
ax2.set_xlabel("ms")
ax2.set_ylabel("deg")

bins = np.arange(-0.5,len(worst_bf_saccades["velocity_norm"])+0.5)
ax3 = plt.subplot2grid((2,3),(1,2)) 
ax3.plot(worst_bf_saccades["norm_time"]/4,worst_bf_saccades["velocity"])
ax3.hist(worst_bf["vector"],bins=bins)
ax3.set_title("Histogram of velocity")
ax3.set_ylabel("deg/s")
ax3.set_xlabel("Sample nr.")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.subplots_adjust(top=0.85)

plt.figtext(0.5,0.95, "Best BF: "+str(np.round(best_bf["bfvalue_score"],2)), ha="center", va="top", fontsize=14)
plt.figtext(0.5,0.48, "Worst BF: "+str(np.round(worst_bf["bfvalue_score"],2)), ha="center", va="top",fontsize=14)
fig_test.subplots_adjust(hspace=1)
savefig("Bf_value_example")

########