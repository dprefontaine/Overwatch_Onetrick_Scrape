import pandas as pd
from ow_preprocess import preprocess
import ow_graphing as graph

def main():
	##GET THE DATA TABLES FIRST
	one_tricker_data = "one_trickers.csv"


	stat_columns = ['Player', 'Winrate', 'AvgEliminations', 'AvgDeaths', 'TimeOnFire']
	one_tricker_import = pd.read_csv(one_tricker_data, delimiter = ",")
	generalist_import = pd.read_csv("generalists.csv", delimiter = ",")

	##MERGE EACH DATA SET
	merged_dataframe = pd.concat([generalist_import.assign(is_onetricker=0),one_tricker_import.assign(is_onetricker=1)])

	merged_x, merged_y = preprocess(merged_dataframe)


	##SINCE ONE TRICKERS ARE TOO SMALL, TEST AND TRAIN ARE GOING TO BE ON GENERALISTS

	from sklearn.model_selection import train_test_split

	##IDEA HERE IS:
	##ONE TRICKERS AS THE STATIC GROUP
	##
	##GENERALISTS ARE GOING TO BE TRAINED AGAINST THE ONE TRICKERS

	import sklearn.linear_model as lm
	from sklearn.model_selection import RepeatedKFold, StratifiedKFold, cross_val_score

	##repeat for accuracy
	repeats = range(1,12)
	results_of_win_vs_elim = list()

	from numpy import mean
	from numpy import std
	from numpy import linspace
	import scipy.stats as s
	from scipy.stats import sem

	model = lm.LinearRegression()

	##SET A TEST AND TRAIN SET UNTIL AT LEAST 5 ONE TRICKERS ARE COUNTED

	##THIS IS KEPT IN CASE OF ANYTHING

	x_train, x_test, y_train, y_test = train_test_split(merged_x, merged_y, test_size = 0.1)

	while (x_test[:,4] == 1).sum() < 6:
		x_train, x_test, y_train, y_test = train_test_split(merged_x, merged_y, test_size = 0.1)
		##print(x_test[:4])
		##print((x_test[:,4] == 1).sum())
		
	cv = None

	print('--------------------------LINEAR REGRESSION TESTS--------------------------------')

	for r in repeats:
		cv = RepeatedKFold(n_splits=10, n_repeats=r, random_state=1)
		scores = cross_val_score(model, x_test, y_test, cv=cv, n_jobs=-1)
		results_of_win_vs_elim.append(scores)
		print('Mean Accuracy: %.3f (%.3f) %.3f' % (mean(scores), std(scores), sem(scores)))

	print('---------------------------------------------------------------------------')


	##GETTING LINE DATA
	#FOR ONE TRICKERS

	#ELIMINATIONS
	ot_x = one_tricker_import.iloc[:,2]
	ot_y = one_tricker_import.iloc[:,1]
	ot_elim_slope, ot_elim_intercept, ot_r_value, ot_p_value, ot_std_err = s.linregress(ot_x,ot_y)
	print('--------------------------ONE TRICKER LINES--------------------------------')
	print('AVERAGE ELIMINATIONS TO WINRATE|Slope: %.3f |Intercept: %.3f |R Value: %.3f |P Value: %.3f |Std Error: %.3f' % (ot_elim_slope, ot_elim_intercept, ot_r_value, ot_p_value, ot_std_err))

	#DEATHS
	ot_x = one_tricker_import.iloc[:,3]
	ot_elim_slope, ot_elim_intercept, ot_r_value, ot_p_value, ot_std_err = s.linregress(ot_x,ot_y)
	print('AVERAGE DEATHS TO WINRATE|Slope: %.3f |Intercept: %.3f |R Value: %.3f |P Value: %.3f |Std Error: %.3f' % (ot_elim_slope, ot_elim_intercept, ot_r_value, ot_p_value, ot_std_err))

	#TIME ON FIRE
	ot_x = one_tricker_import.iloc[:,4]
	ot_elim_slope, ot_elim_intercept, ot_r_value, ot_p_value, ot_std_err = s.linregress(ot_x,ot_y)
	print('AVERAGE T.O.F. TO WINRATE: |Slope: %.3f |Intercept: %.3f |R Value: %.3f |P Value: %.3f |Std Error: %.3f' % (ot_elim_slope, ot_elim_intercept, ot_r_value, ot_p_value, ot_std_err))
	print('--------------------------------------------------------------------------')

	##CREATING GRAPHS

	##JOINTPLOTS
	##THE ONE TRICKER GRAPHS
	graph.graphing_one_tricker_histogram()
	graph.graphing_jointplot(one_tricker_data, "AvgEliminations","Winrate", "Average Eliminations vs Winrate among One Trickers", "blue")
	graph.graphing_jointplot(one_tricker_data, "AvgDeaths","Winrate", "Average Deaths vs Winrate among One Trickers", "red")
	graph.graphing_jointplot(one_tricker_data, "TimeOnFire","Winrate", "Time On Fire vs Winrate among One Trickers", "orange")

	total_one_trickers,y=one_tricker_import.shape
	random_sample = None

	##THE GENERALIST GRAPHS (ALSO DOING LINES HERE FOR CONSISTENT RESULTS)
	for i in repeats:
		random_sample = generalist_import.sample(n=total_one_trickers, random_state=i)
		graph.graphing_jointplot_data(random_sample, "AvgEliminations","Winrate", "Average Eliminations vs Winrate among Generalists "+str(i), "green")
		graph.graphing_jointplot_data(random_sample, "AvgDeaths","Winrate", "Average Deaths vs Winrate among Generalists "+str(i), "purple")
		graph.graphing_jointplot_data(random_sample, "TimeOnFire","Winrate", "Time On Fire vs Winrate among Generalists "+str(i), "yellow")
		
		print('--------------------------LINE OF GENERALIST SAMPLE ' + str(i) + '--------------------------------')
		
		ot_y = random_sample.iloc[:,1]
		
		#ELIMINATIONS
		ot_x = random_sample.iloc[:,2]
		ot_elim_slope, ot_elim_intercept, ot_r_value, ot_p_value, ot_std_err = s.linregress(ot_x,ot_y)
		print('AVERAGE ELIMINATIONS TO WINRATE|Slope: %.3f |Intercept: %.3f |R Value: %.3f |P Value: %.3f |Std Error: %.3f' % (ot_elim_slope, ot_elim_intercept, ot_r_value, ot_p_value, ot_std_err))


		#DEATHS
		ot_x = random_sample.iloc[:,3]
		ot_elim_slope, ot_elim_intercept, ot_r_value, ot_p_value, ot_std_err = s.linregress(ot_x,ot_y)
		print('AVERAGE DEATHS TO WINRATE|Slope: %.3f |Intercept: %.3f |R Value: %.3f |P Value: %.3f |Std Error: %.3f' % (ot_elim_slope, ot_elim_intercept, ot_r_value, ot_p_value, ot_std_err))

		#TIME ON FIRE
		ot_x = random_sample.iloc[:,4]
		ot_elim_slope, ot_elim_intercept, ot_r_value, ot_p_value, ot_std_err = s.linregress(ot_x,ot_y)
		print('AVERAGE T.O.F. TO WINRATE: |Slope: %.3f |Intercept: %.3f |R Value: %.3f |P Value: %.3f |Std Error: %.3f' % (ot_elim_slope, ot_elim_intercept, ot_r_value, ot_p_value, ot_std_err))
		print('---------------------------------------------------------------------------------')

	##GENERALIST HISTOGRAM
	graph.graphing_generalist_histogram()
	graph.graphing_both_histogram()
		
	##PUT OUT A TON OF GRAPHS HERE
	graph.graphing_comparison_of_winrate_and_eliminations();
	graph.graphing_comparison_of_winrate_and_deaths();
	graph.graphing_comparison_of_winrate_and_time_on_fire();

    

if __name__ == "__main__":
	main()



