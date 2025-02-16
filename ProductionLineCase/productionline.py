# -*- coding: utf-8 -*-
"""ProductionLine.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1goqI8XIB5jk8-rw5fyAIVJASthJU427b
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns
import scipy
import matplotlib.pyplot as plt
# %matplotlib inline
from plotly.offline import iplot
import plotly.graph_objs as go
#pd.set_option("display.max_columns", 100)
#pd.set_option("precision", 5)
#%pylab inline
#from tqdm import tqdm_notebook

# Loading/Extracting data
# I stored data on my github
data = pd.read_csv("https://raw.githubusercontent.com/joobernardo/Portfolio_DS/master/ProductionLineCase/continuous_factory_process.csv")
data.info()

# Transforming data
data["time_stamp"] = pd.to_datetime(data["time_stamp"])
data = data.sort_values("time_stamp").reset_index(drop=True) #just to be sure about timeline order
data.head(5)

# Separating dataframe into each production line component
ProdLine = data
#Start col	End col	Description
Time = data.iloc[:,0] # 0	0	Time stamp
Factory_Amb_Conditions = data.iloc[:,1:3] # 1	2	Factory ambient conditions

M1_rawmaterial = data.iloc[:,3:7] # 3	6	First stage, Machine 1, raw material properties (material going in to Machine 1)
M1_process = data.iloc[:,7:15] # 7	14	First stage, Machine 1 process variables

M2_rawmaterial = data.iloc[:,15:19] # 15	18	First stage, Machine 2, raw material properties (material going in to Machine 2)
M2_process = data.iloc[:,19:27] # 19	26	First stage, Machine 2 process variables

M3_rawmaterial = data.iloc[:,27:31] # 27	30	First stage, Machine 3, raw material properties (material going in to Machine 3)
M3_process = data.iloc[:,31:39] # 31	38	First stage, Machine 3 process variables

Combiner_stage = data.iloc[:,39:42] # 39	41	Combiner stage process parameters. Here we combines the outputs from Machines 1, 2, and 3.

Output1 = data.iloc[:,42:72] # 42	71	PRIMARY OUTPUT TO CONTROL: Measurements of 15 features (in mm), along with setpoint or target for each

M4_process = data.iloc[:,72:79] # 72	78	Second stage, Machine 4 process variables
M5_process = data.iloc[:,79:86] # 79	85	Second stage, Machine 5 process variables
Ouput2 = data.iloc[:,31:39] # 86	115	SECONDARY OUTPUT TO CONTROL: Measurements of 15 features (in mm), along with setpoint or target for each

"""# Simple Analysis to understand the production line
EDA for the first stage

## Measurements time
"""

print("First measurement at " + str(Time.min()))
print("Last measurement at " + str(Time.max()))
print("Production line was measured for " + str((Time.max()-Time.min())))

"""## Factory Ambient Conditions
Humidity and Temperature
"""

df = Factory_Amb_Conditions
col1 = 'AmbientConditions.AmbientHumidity.U.Actual'
col2 = 'AmbientConditions.AmbientTemperature.U.Actual'

sns.kdeplot(df[col1], color= 'blue', label= 'Humidity')
plt.title("Variable distribution")

sns.kdeplot(df[col2], color= 'red', label= 'Temperature')
plt.title("Variable distribution")

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=df[col1], name='Humidity',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=df[col2], name='Temperature',
                         line=dict(color='red')))
fig.update_layout(title='Factory Ambient Conditions',
                   xaxis_title='Time',
                   yaxis_title='Unit')

"""## Raw Materials' Properties for each machine
There are 4 raw materials' properties described as Property1, Property2, Property3 and Property4.
"""

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=M1_rawmaterial["Machine1.RawMaterial.Property1"], name='Machine 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=M2_rawmaterial["Machine2.RawMaterial.Property1"], name='Machine 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=M3_rawmaterial["Machine3.RawMaterial.Property1"], name='Machine 3',
                         line=dict(color='green')))
fig.update_layout(title='Raw Material Property 1',
                   xaxis_title='Time',
                   yaxis_title='Unit')

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=M1_rawmaterial["Machine1.RawMaterial.Property2"], name='Machine 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=M2_rawmaterial["Machine2.RawMaterial.Property2"], name='Machine 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=M3_rawmaterial["Machine3.RawMaterial.Property2"], name='Machine 3',
                         line=dict(color='green')))
fig.update_layout(title='Raw Material Property 2',
                   xaxis_title='Time',
                   yaxis_title='Unit')

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=M1_rawmaterial["Machine1.RawMaterial.Property3"], name='Machine 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=M2_rawmaterial["Machine2.RawMaterial.Property3"], name='Machine 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=M3_rawmaterial["Machine3.RawMaterial.Property3"], name='Machine 3',
                         line=dict(color='green')))
fig.update_layout(title='Raw Material Property 3',
                   xaxis_title='Time',
                   yaxis_title='Unit')

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=M1_rawmaterial["Machine1.RawMaterial.Property4"], name='Machine 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=M2_rawmaterial["Machine2.RawMaterial.Property4"], name='Machine 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=M3_rawmaterial["Machine3.RawMaterial.Property4"], name='Machine 3',
                         line=dict(color='green')))
fig.update_layout(title='Raw Material Property 4',
                   xaxis_title='Time',
                   yaxis_title='Unit')

"""## Process Data for each machine
Raw material feeder parameter, zone 1 temperature, zone 2 temperature, motor amperage, motor rpm, material pressure, material temperature and exit zone temperature.
"""

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=M1_process["Machine1.RawMaterialFeederParameter.U.Actual"], name='Machine 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=M2_process["Machine2.RawMaterialFeederParameter.U.Actual"], name='Machine 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=M3_process["Machine3.RawMaterialFeederParameter.U.Actual"], name='Machine 3',
                         line=dict(color='green')))
fig.update_layout(title='Raw Material Feeder Parameter',
                   xaxis_title='Time',
                   yaxis_title='Unit')

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=M1_process["Machine1.Zone1Temperature.C.Actual"], name='Machine 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=M2_process["Machine2.Zone1Temperature.C.Actual"], name='Machine 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=M3_process["Machine3.Zone1Temperature.C.Actual"], name='Machine 3',
                         line=dict(color='green')))
fig.update_layout(title='Zone 1 Temperature',
                   xaxis_title='Time',
                   yaxis_title='Unit')

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=M1_process["Machine1.Zone2Temperature.C.Actual"], name='Machine 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=M2_process["Machine2.Zone2Temperature.C.Actual"], name='Machine 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=M3_process["Machine3.Zone2Temperature.C.Actual"], name='Machine 3',
                         line=dict(color='green')))
fig.update_layout(title='Zone 2 Temperature',
                   xaxis_title='Time',
                   yaxis_title='Unit')

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=M1_process["Machine1.MotorAmperage.U.Actual"], name='Machine 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=M2_process["Machine2.MotorAmperage.U.Actual"], name='Machine 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=M3_process["Machine3.MotorAmperage.U.Actual"], name='Machine 3',
                         line=dict(color='green')))
fig.update_layout(title='Motor Amperage',
                   xaxis_title='Time',
                   yaxis_title='Unit')

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=M1_process["Machine1.MotorRPM.C.Actual"], name='Machine 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=M2_process["Machine2.MotorRPM.C.Actual"], name='Machine 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=M3_process["Machine3.MotorRPM.C.Actual"], name='Machine 3',
                         line=dict(color='green')))
fig.update_layout(title='Motor RPM',
                   xaxis_title='Time',
                   yaxis_title='Unit')

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=M1_process["Machine1.MaterialPressure.U.Actual"], name='Machine 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=M2_process["Machine2.MaterialPressure.U.Actual"], name='Machine 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=M3_process["Machine3.MaterialPressure.U.Actual"], name='Machine 3',
                         line=dict(color='green')))
fig.update_layout(title='Material Pressure',
                   xaxis_title='Time',
                   yaxis_title='Unit')

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=M1_process["Machine1.MaterialTemperature.U.Actual"], name='Machine 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=M2_process["Machine2.MaterialTemperature.U.Actual"], name='Machine 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=M3_process["Machine3.MaterialTemperature.U.Actual"], name='Machine 3',
                         line=dict(color='green')))
fig.update_layout(title='Material Temperature',
                   xaxis_title='Time',
                   yaxis_title='Unit')

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=M1_process["Machine1.ExitZoneTemperature.C.Actual"], name='Machine 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=M2_process["Machine2.ExitZoneTemperature.C.Actual"], name='Machine 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=M3_process["Machine3.ExitZoneTemperature.C.Actual"], name='Machine 3',
                         line=dict(color='green')))
fig.update_layout(title='Exit Zone Temperature',
                   xaxis_title='Time',
                   yaxis_title='Unit')

"""## First Stage - Combiner Operation
Temperature 1, 2 and 3.
"""

df = Combiner_stage
col1 = 'FirstStage.CombinerOperation.Temperature1.U.Actual'
col2 = 'FirstStage.CombinerOperation.Temperature2.U.Actual'
col3 = 'FirstStage.CombinerOperation.Temperature3.C.Actual'
fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=df[col1], name='Temperature 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=df[col2], name='Temperature 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=df[col3], name='Temperature 3',
                         line=dict(color='green')))
fig.update_layout(title='Combiner Stage Temperature - Stage 1',
                   xaxis_title='Time',
                   yaxis_title='Unit')

"""## Stage 1 - Output 1
15 measurements error
"""

a=0
for i in (np.linspace(0,30,16)):
  Output1["Meas_"+str(int(a))+"_Error"] = Output1.iloc[:,int(i)] - Output1.iloc[:,int(i)+1]
  a = a+1

Output1 = Output1.drop(['Meas_15_Error'], axis=1)
Output1_error = Output1.iloc[:,-15:]
Output1_error

fig = go.Figure()

for i in range(0,len(Output1_error.columns)):
  fig.add_trace(go.Scatter(x=Time, y=Output1_error.iloc[:,i], name=Output1_error.columns[i]))


fig.update_layout(title='Stage 1 - Output 1 - All Measurements Errors - You are able to select which line you want to see in legends',
                   xaxis_title='Time',
                   yaxis_title='Unit')

"""## Simple Model to predict only the first measurement"""

!pip install shap
import shap
shap.initjs()

Output1_error.iloc[:,0]

# LightGBM is a gradient boosting framewo rk that uses tree based learning algorithms. 
# https://towardsdatascience.com/understanding-gradient-boosting-machines-9be756fe76ab
#3.2.4.3.2. sklearn.ensemble.RandomForestRegressor¶
#A random forest regressor.
#A random forest is a meta estimator that fits a number of classifying decision trees on various sub-samples of 
#the dataset and uses averaging to improve the predictive accuracy and control over-fitting. 
#The sub-sample size is always the same as the original input sample size but the samples are drawn with replacement if bootstrap=True (default).
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, median_absolute_error

x = data.iloc[:, 1:42]
y = Output1_error.iloc[:,0]

np.random_state=0

Xtrain, Xval = x.iloc[:7000], x.iloc[7000:]
ytrain, yval = y.iloc[:7000], y.iloc[7000:]

p_base = ytrain.mean() * np.ones(yval.shape[0])
mae_b, medae_b = mean_absolute_error(yval, p_base), median_absolute_error(yval, p_base)
print("Baseline MAE: {} - MEDAE: {}".format(mae_b, medae_b))

# Fit regression model
regr_1 = DecisionTreeRegressor(criterion = "mae")
regr_1.fit(Xtrain, ytrain)
y_1 = regr_1.predict(Xval)
mae_m, medae_m = mean_absolute_error(yval, y_1),median_absolute_error(yval, y_1)
print("Modelo MAE: {} - MEDAE: {}\n".format(mae_m, medae_m))
importances = regr_1.feature_importances_

error = (yval - y_1).clip(upper=1)
error.plot(figsize=(20,7))

pd.Series(regr_1.feature_importances_, index=Xtrain.columns).sort_values().tail(10).plot.barh(figsize=(10,10))

explainer = shap.TreeExplainer(regr_1)
shap_values = explainer.shap_values(Xtrain)

shap.summary_plot(shap_values, Xtrain)

pd.DataFrame([importances,x.columns]).T

plt.figure(figsize=[10,10])
plt.bar(importances,x.columns, align="center")

from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, median_absolute_error
import seaborn as sns

features = data.iloc[:, 1:42]

lift = []
for stage in [1,2]:
    for measure in range(15): 
        print("Stage {} - Measurement: {}".format(stage, measure))

        data['Y'] = data['Stage{}.Output.Measurement{}.U.Actual'.format(stage, measure)] - data['Stage{}.Output.Measurement{}.U.Setpoint'.format(stage, measure)]
        y = data['Y']

        Xtrain, Xval = features.iloc[:7000], features.iloc[7000:]
        ytrain, yval = y.iloc[:7000], y.iloc[7000:]

        p_base = ytrain.mean() * np.ones(yval.shape[0])
        mae_b, medae_b = mean_absolute_error(yval, p_base), median_absolute_error(yval, p_base)
        print("Baseline MAE: {} - MEDAE: {}".format(mae_b, medae_b))

        mdl = LGBMRegressor(n_estimators=100, learning_rate=0.003, num_leaves=2**6, 
                            subsample=0.75, subsample_freq=1, colsample_bytree=1., random_state=0)
        mdl.fit(Xtrain, ytrain)
        p = mdl.predict(Xval)
        
        mae_m, medae_m = mean_absolute_error(yval, p),median_absolute_error(yval, p)
        
        print("Modelo MAE: {} - MEDAE: {}\n".format(mae_m, medae_m))
        
        lift.append({"stage": stage, "measure": measure, "mae_lift": mae_m / mae_b - 1, "medae_lift": medae_m / medae_b - 1 })

lift

features.shape

Xtrain, Xval = features.iloc[:7000], features.iloc[7000:]
ytrain, yval = y.iloc[:7000], y.iloc[7000:]

mdl = LGBMRegressor(random_state=0)
mdl.fit(Xtrain, ytrain)
p = mdl.predict(Xval)

naive_error = (yval - p).clip(upper=1)
#naive_error.plot(figsize=(20,7))

fig = go.Figure()
fig.add_trace(go.Scatter(x=Time, y=naive_error, name='Temperature 1',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=Time, y=df[col2], name='Temperature 2',
                         line=dict(color='red')))
fig.add_trace(go.Scatter(x=Time, y=df[col2], name='Temperature 3',
                         line=dict(color='green')))
fig.update_layout(title='Combiner Stage Temperature - Stage 1',
                   xaxis_title='Time',
                   yaxis_title='Unit')

from sklearn.metrics import mean_absolute_error, median_absolute_error

p_base = ytrain.mean() * np.ones(yval.shape[0])
#p_base = ytrain.median() * np.ones(yval.shape[0])
mean_absolute_error(yval, p_base), median_absolute_error(yval, p_base)

# (0.07976598605663952, 0.04836065519425792) - baseline mae
# (0.08625496927059799, 0.07000000000000028) - baseline median

mean_absolute_error(yval, p),median_absolute_error(yval, p)

mdl = LGBMRegressor(n_estimators=100, learning_rate=0.003, num_leaves=2**6, 
                    subsample=0.75, subsample_freq=1, colsample_bytree=1., min_child_samples=20,
                    random_state=0)
mdl.fit(Xtrain, ytrain)
p = mdl.predict(Xval)
mean_absolute_error(yval, p),median_absolute_error(yval, p)

error = (yval - p).clip(upper=1)
error.plot(figsize=(20,7))

pd.Series(mdl.feature_importances_, index=Xtrain.columns).sort_values().tail(10).plot.barh(figsize=(10,10))

!pip install shap

import shap
shap.initjs()

explainer = shap.TreeExplainer(mdl)
shap_values = explainer.shap_values(Xtrain)

shap.summary_plot(shap_values, Xtrain)

f,a  = pylab.subplots(1,1, figsize=(10,10))
shap.dependence_plot("Machine3.MaterialTemperature.U.Actual", shap_values, Xtrain, ax=a, interaction_index=None)

plt.scatter(ProdLine["Machine3.MaterialTemperature.U.Actual"],y)

y

