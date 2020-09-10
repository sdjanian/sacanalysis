import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import warnings
warnings.filterwarnings('ignore')

class Plotting_class:
    palette = sns.color_palette("bright")
    _class_label_color_gazecom = {0: ['Unknown', palette[1]],
                         1: ['Fixation',palette[0]],
                         2: ['Saccade',palette[2]],
                         3: ['Smooth Pursuit',palette[3]],
                         4: ['Noise',palette[4]]}
    
    _class_label_color_lund = {
                              0: ['Fixation',palette[0]],
                         1: ['Saccade',palette[2]],
                         3: ['PSO',palette[5]],
                         2: ['Smooth Pursuit',palette[3]]}
    
    sizeOfMarkerOnLegend = 10
    
    
    def __init__(self, colors:str,rater_col_name="handlabeller_final",plot_style="seaborn"):
        if colors == "GazeCom":
            self._class_label_color = self._class_label_color_gazecom
        if colors == "Lund2013":
            self._class_label_color = self._class_label_color_lund
            
        self._rater_col_name=rater_col_name
        plt.style.use(plot_style)
            



    def plotEyeMovementClass(self,_xname,_yname,data,_range = None):
        '''
        parameters:
            _xname, _yname : string that is used to call the collumn from data
            data : the GazeCom data for 1 session loaded as pandas
            _range : Default None. It's the range of data that is plotted
        '''
        
        if _range == None:
            _range = range(0,data.size)
            data_subset = data
        else:
            data_subset = data[_range]
        
        for key,value in self._class_label_color.items():
            x = np.extract(data_subset[self._rater_col_name]==key,data_subset[_xname])
            y = np.extract(data_subset[self._rater_col_name]==key,data_subset[_yname])
            #if x.size != 0:
                #plt.plot(x,y,value[1]) 
            #    print(key,value)
            plt.plot(x,y,marker=".",linestyle="",color=value[1],label = value[0],markersize=6) 
            #print(key,value)
        plt.legend()    
         
    
    def x_y_velocity_plot(self,df=None,title="No title set",
                                   figsize=(10,6)):
        '''
        Plots the x, y and velocty for a recording.
        parameters:
            df : The recording you want plot as a pandas dataframe. It will use columns "x", "y", "time" and "speed_1"
            title : Default "No title set". It's the suptitle of the plots
            figsize : Default is (10,6). Look up figsize in matplotlib.
        '''        
        fig = plt.figure(figsize=figsize)
        limit_buffer = 2
        
        ax1 = plt.subplot(3, 1, 1)
        self.plotEyeMovementClass("time","x",df,_range = None)
        ax1.get_legend().remove()
        plt.title(title)
        plt.ylabel("X Position (deg)")
        ymin1, ymax1 = ax1.get_ylim()
        ax1.set_ylim(ymin1-limit_buffer, ymax1+limit_buffer) # Adjust limits to acount for +- 2 deg
    
        ax2 = plt.subplot(3, 1, 2)
        self.plotEyeMovementClass("time","y",df,_range = None)
        ax2.get_legend().remove()
        plt.ylabel("Y Position (deg)")
        ymin2, ymax2 = ax2.get_ylim()
        ax2.set_ylim(ymin2-limit_buffer, ymax2+limit_buffer) # Adjust limits to acount for +- 2 deg

        #if (ymax1-ymin1) >= (ymax2-ymin2):
        #    scale = (ymax1-ymin1)/(ymax2-ymin2)
        #else:
        #    scale = (ymax2-ymin2)/(ymax1-ymin1)

        ax2 = plt.subplot(3, 1, 3)
        self.plotEyeMovementClass("time","speed_1",df,_range = None)
        plt.ylabel("Velocity (deg/s)")    
        fig.text(0.5, 0.04, 'Time (ms)', ha='center')
        lgnd = plt.legend(scatterpoints=1, fontsize=10,loc='center left', bbox_to_anchor=(1, 1.7))
        for handle in lgnd.legendHandles:
            handle._legmarker.set_markersize(self.sizeOfMarkerOnLegend)
        return fig
    
    def x_y_radial_pos_plot(self,df=None,title="No title set",
                                   figsize=(10,6)):
        '''
        Plots the x, y and velocty for a recording.
        parameters:
            df : The recording you want plot as a pandas dataframe. It will use columns "x", "y", "time" and "speed_1"
            title : Default "No title set". It's the suptitle of the plots
            figsize : Default is (10,6). Look up figsize in matplotlib.
        '''        
        fig = plt.figure(figsize=figsize)
        limit_buffer = 2
        
        ax1 = plt.subplot(3, 1, 1)
        self.plotEyeMovementClass("time","x",df,_range = None)
        ax1.get_legend().remove()
        plt.title(title)
        plt.ylabel("X Position (deg)")
        ymin1, ymax1 = ax1.get_ylim()
        ax1.set_ylim(ymin1-limit_buffer, ymax1+limit_buffer) # Adjust limits to acount for +- 2 deg
    
        ax2 = plt.subplot(3, 1, 2)
        self.plotEyeMovementClass("time","y",df,_range = None)
        ax2.get_legend().remove()
        plt.ylabel("Y Position (deg)")
        ymin2, ymax2 = ax2.get_ylim()
        ax2.set_ylim(ymin2-limit_buffer, ymax2+limit_buffer) # Adjust limits to acount for +- 2 deg

        #if (ymax1-ymin1) >= (ymax2-ymin2):
        #    scale = (ymax1-ymin1)/(ymax2-ymin2)
        #else:
        #    scale = (ymax2-ymin2)/(ymax1-ymin1)

        ax2 = plt.subplot(3, 1, 3)
        self.plotEyeMovementClass("time","radial_pos",df,_range = None)
        plt.ylabel("Radial_pos (deg)")    
        fig.text(0.5, 0.04, 'Time (ms)', ha='center')
        lgnd = plt.legend(scatterpoints=1, fontsize=10,loc='center left', bbox_to_anchor=(1, 1.7))
        for handle in lgnd.legendHandles:
            handle._legmarker.set_markersize(self.sizeOfMarkerOnLegend)
        return fig
    
    def plotDistributions(self,df,feature:str,xlabel_:str,ylabel_:str,num_rows=2,num_cols=2,labels=[1,2,3,4],sup_title="",titles=["Fixation",
                                "Saccade","Smooth pursuit","Noise"],fig_size=(6,4),use_log=True,bins=None,plotType=None,
                                remove_outliers = True, outlier_threshold = 99):
        '''
        parameters:
            df : the pandas dataframe used that is plottet from
            xlabel_,ylabel_ : The common xlabel and ylabel for the subplot
            num_rows=2,num_cols=2 : shape of the subplot. By default (2,2)
            labels=[1,2,3,4] : the labels of the classes
            titles=["Fixations","Saccade","Smooth pursuit","Noise"] : the titles of the subplots (not the overall name title of the plot!)
            use_log=True : if y axis should be logarithmic.
            bins=None : bins of the histogram. Look at matplotlib documentation to see how to use
            plotType=None : Specifies the type of data that is being plottet. Currently two modes exist:
                            "features" for when the df is all the recordings
                            "event duration" for when df is event dataframe
        '''
        fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=fig_size,sharey=True)
        fig.suptitle(sup_title,y=1.02, fontsize=18)
    
        ax_flat = axes.flatten()
        ax_flat[0].get_shared_x_axes().join(ax_flat[0], ax_flat[2])
    
        for i, ax in enumerate(ax_flat):
            if i>= len(labels):
                continue
            if plotType == "features":
                if remove_outliers is True:
                  if df[feature][df[self._rater_col_name]==labels[i]].empty:
                      threshold = 0
                  else:
                      threshold = np.percentile(df[feature][df[self._rater_col_name]==labels[i]],outlier_threshold)
                  without_outliers = df[feature][df[self._rater_col_name]==labels[i]] > threshold
                  data_to_plot = df[feature][df[self._rater_col_name]==labels[i]][~without_outliers] # df has to be all recordings
                else:
                  data_to_plot = df[feature][df[self._rater_col_name]==labels[i]]
            if plotType == "event duration":
                data_to_plot = df["event_duration"][df["event_type"]==labels[i]] # df has to be frame of events
                
            if plotType == "event amplitude":
                data_to_plot = df["event_amplitude"][df["event_type"]==labels[i]] # df has to be frame of events       
                
            if plotType is None:
                print("No type of distribution plot was specified, so nothing was produced")
                return
            
            #g.set(yscale="log")
            g = sns.distplot(data_to_plot,rug=False,kde=False,ax=ax,bins=bins)
            ax.set(title=titles[i], xlabel='') 
            if use_log:
                if (self._rater_col_name=="RA_encoded") & (feature=="direction_1"):
                    ylabel_ = ylabel_.replace('(log)',"")
                    continue
                else:
                    ax.set_yscale('log',nonposy='clip')
                #None
                #ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
                #ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
                if plotType is "event duration":
                    ax.xaxis.set_major_formatter(ScalarFormatter())
                    ax.yaxis.set_major_formatter(ScalarFormatter()) # These behave very funky for some reason. They have to be disabled for the feature plots.
             
        fig.text(-0.01, 0.5,ylabel_, va='center', rotation='vertical',fontsize=14)
        fig.text(0.5, -0.01, xlabel_, ha='center',fontsize=14)
    
        plt.tight_layout()
        return fig, axes
    
if __name__ == "__main__":
    import load_gazecom_class
    import calculateEvents as cEvents
    
    #Example of how to use plotting_class
    
    #Load dataset as df
    if 'df' not in locals():
        load_gazecom = load_gazecom_class.Load_gazecom()
        df = load_gazecom.load_all_data()
    
    plotting_class = Plotting_class(colors="GazeCom")

    ### Example 1
    # Select a specific recording
    df_subj_1 = df[df['source']==r'..\GazeCom_Data\all_features\beach\JJK_beach.arff']

    # Plotting using plotEyeMovementClass
    fig,ax = plt.subplots()
    plotting_class.plotEyeMovementClass("time","speed_1",df_subj_1[(df_subj_1["time"]>11400) & (df_subj_1["time"]<12800)],_range = None)
    plt.title("Example of velocity plot")
    plt.ylabel("Velocity (deg/s)")    
    fig.text(0.5, 0.04, 'Time (ms)', ha='center') # Place the x label. Can be done in other ways.
    lgnd = plt.legend(scatterpoints=1, fontsize=10,loc='center left', bbox_to_anchor=(1, 0.5))
    # Change the sizes of the dots in the legend
    for handle in lgnd.legendHandles:
        handle._legmarker.set_markersize(plotting_class.sizeOfMarkerOnLegend)
        
    ### Example 2 using x_y_velocity_plot
    fig2 = plotting_class.x_y_velocity_plot(df=df_subj_1[(df_subj_1["time"]>11400) & (df_subj_1["time"]<12800)],title="Example of x,y and velocty plot",
                                   figsize=(10,6))
    
    ### Example 3 plotting distributions
    CEvents = cEvents.CalculateEventDurationClass()
    
    event_df = CEvents.calculateBasicEventStatistics(df)
    label_list = []
    label_name_list = []
    for key,val in load_gazecom.class_label_gazecom.items():
        if val!="Unknown":
            label_name_list.append(val)
            label_list.append(key)
    bins_event_duration = np.arange(event_df["event_duration"][event_df["event_type"]==2].min(),event_df["event_duration"][event_df["event_type"]==2].max(),10)
    fig,ax = plotting_class.plotDistributions(df=event_df,feature="None",xlabel_="Duration (ms)",ylabel_="Frequency (log)",labels=label_list,titles=label_name_list,plotType="event duration",
                               bins = None, sup_title="Event duration")