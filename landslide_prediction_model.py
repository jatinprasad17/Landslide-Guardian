import numpy as np
import pandas as pd

from numpy import mean
from numpy import std
from sklearn.ensemble import GradientBoostingClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_auc_score

from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

"""Exploratory data analysis"""

df = pd.read_csv('Complete-data.csv')
df.head()

df.info()

temp_cols=df.columns.tolist()
new_cols=temp_cols[1:] + temp_cols[0:1]
df=df[new_cols]

df.describe().round(2)

for column in df.columns[0:]:
    print(column, ': ', len(df[column].unique()), ' labels')

landslide_count = df['Landslide'].value_counts()
sns.set(style = "darkgrid")
sns.barplot(x = landslide_count.index, y = landslide_count.values, alpha = 0.9)
plt.title('Frequency Distribution of Landslides')
plt.ylabel('Number of Occurrences', fontsize=12)
plt.xlabel('Landslide', fontsize=12)
plt.show()

plt.savefig('bar1.eps', format='eps')

lith_count = df['Lithology'].value_counts()
sns.set_theme(style="darkgrid")
sns.barplot(x=lith_count.index, y=lith_count.values, alpha=0.9)
plt.title('Frequency Distribution of Lithology')
plt.ylabel('Number of Occurrences', fontsize=12)
plt.xlabel('Lithology', fontsize=12)
plt.show()

plt.savefig('bar3.eps', format='eps')

sns.catplot(x="Landslide", y="NDWI", kind="swarm", data=df)

plt.savefig('box1.eps', format='eps')

"""Feature Selection"""

from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.utils._testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn import ensemble

!pip install pca

from sklearn.preprocessing import StandardScaler

from pca import pca

X_pca = df.loc[:, df.columns != 'Landslide']
model = pca()
out = model.fit_transform(X_pca)

print(out['topfeat'])

model.plot()

plt.savefig('pca1.eps', format='eps')

"""Baseline model"""

y = df.Landslide
df1 = df.loc[:, df.columns != 'Landslide']
X_train, X_test, y_train, y_test = train_test_split(df1, y, test_size=0.2)

baseline_gbm = GradientBoostingClassifier(learning_rate=0.1, n_estimators=100,max_depth=3, min_samples_split=2,
                                          min_samples_leaf=1, subsample=1,max_features='sqrt', random_state=10)
baseline_gbm.fit(X_train,y_train)
predictors_gbm=list(X_train)

print('Accuracy of the GBM on test set: {:.3f}'.format(baseline_gbm.score(X_test, y_test)))
pred_gbm=baseline_gbm.predict(X_test)
print(classification_report(y_test, pred_gbm))

baseline_lgbm = LGBMClassifier(learning_rate=0.1, n_estimators=100,max_depth=3,
                               min_samples_leaf=1, subsample=1,random_state=10)
baseline_lgbm.fit(X_train,y_train)
predictors_lgbm=list(X_train)

print('Accuracy of the LGBM on test set: {:.3f}'.format(baseline_lgbm.score(X_test, y_test)))
pred_lgbm=baseline_lgbm.predict(X_test)
print(classification_report(y_test, pred_lgbm))

"""Model Tuning"""

p_test3 = {'learning_rate':[0.15,0.1,0.05,0.01,0.005,0.001], 'n_estimators':[50,100,250,500,750,1000,1250,1500,1750]}

tuning = GridSearchCV(estimator = GradientBoostingClassifier(max_depth=4, min_samples_split=2, min_samples_leaf=1,
                                                            subsample=1,max_features='sqrt', random_state=10),
                                                            param_grid = p_test3, scoring='accuracy',n_jobs=4,
                                                            cv=5)
tuning.fit(X_train,y_train)
tuning.best_params_, tuning.best_score_
learning_rate_gbm = tuning.best_params_.get("learning_rate")
n_estimators_gbm = tuning.best_params_.get("n_estimators")

p_test3a = {'learning_rate':[0.15,0.1,0.05,0.01,0.005,0.001], 'n_estimators':[50,100,250,500,750,1000,1250,1500,1750]}

tuning = GridSearchCV(estimator =LGBMClassifier(max_depth=4, min_samples_leaf=1,
                                                subsample=1, random_state=10),
                                                param_grid = p_test3a, scoring='accuracy',n_jobs=4,
                                                cv=5)
tuning.fit(X_train,y_train)
tuning.best_params_, tuning.best_score_
learning_rate_lgbm = tuning.best_params_.get("learning_rate")
n_estimators_lgbm = tuning.best_params_.get("n_estimators")

p_test2 = {'max_depth':[2,3,4,5,6,7] }
tuning = GridSearchCV(estimator =GradientBoostingClassifier(learning_rate=learning_rate_gbm,n_estimators=n_estimators_gbm,
                                                            min_samples_split=2,
                                                            min_samples_leaf=1, subsample=1,max_features='sqrt',
                                                            random_state=10),
                                                            param_grid = p_test2, scoring='accuracy',n_jobs=4,
                                                             cv=5)
tuning.fit(X_train,y_train)
tuning.best_params_, tuning.best_score_
max_depth_gbm = tuning.best_params_.get("max_depth")

p_test2a = {'max_depth':[2,3,4,5,6,7] }
tuning = GridSearchCV(estimator =LGBMClassifier(learning_rate=learning_rate_lgbm,n_estimators=n_estimators_lgbm,
                                                min_samples_leaf=1, subsample=1, random_state=10),
                                                param_grid = p_test2, scoring='accuracy',n_jobs=4,
                                     cv=5)
tuning.fit(X_train,y_train)
tuning.best_params_, tuning.best_score_
max_depth_lgbm = tuning.best_params_.get("max_depth")

model1 = GradientBoostingClassifier(learning_rate=learning_rate_gbm, n_estimators=n_estimators_gbm,max_depth=max_depth_gbm,
                                    min_samples_split=2,
                                    min_samples_leaf=1, subsample=1,max_features='sqrt', random_state=10)
model1.fit(X_train,y_train)
predictors=list(X_train)

print('Accuracy of the GBM on test set: {:.3f}'.format(model1.score(X_test, y_test)))
pred=model1.predict(X_test)
print(classification_report(y_test, pred))

model1_lgbm = LGBMClassifier(learning_rate=learning_rate_lgbm, n_estimators=n_estimators_lgbm,max_depth=max_depth_lgbm,
                             min_samples_leaf=1, subsample=1, random_state=10)
model1_lgbm.fit(X_train,y_train)
predictors=list(X_train)

print('Accuracy of the LGBM on test set: {:.3f}'.format(model1_lgbm.score(X_test, y_test)))
pred=model1_lgbm.predict(X_test)
print(classification_report(y_test, pred))

p_test4 = {'min_samples_split':[2,4,6,8,10,20,40,60,100], 'min_samples_leaf':[1,3,5,7,9]}

tuning = GridSearchCV(estimator =GradientBoostingClassifier(learning_rate=learning_rate_gbm, n_estimators=n_estimators_gbm,
                                                            max_depth=max_depth_gbm,
                                                            subsample=1,max_features='sqrt', random_state=10),
                                                            param_grid = p_test4, scoring='accuracy',n_jobs=4,
                                                            cv=5)
tuning.fit(X_train,y_train)
tuning.best_params_, tuning.best_score_
min_samples_leaf_gbm = tuning.best_params_.get("min_samples_leaf")

p_test4a = {'min_samples_leaf':[1,3,5,7,9]}

tuning = GridSearchCV(estimator =LGBMClassifier(learning_rate=learning_rate_lgbm, n_estimators=n_estimators_lgbm,
                                                max_depth=max_depth_lgbm,
                                                subsample=1, random_state=10),
                                                param_grid = p_test4a, scoring='accuracy',n_jobs=4,
                                                cv=5)
tuning.fit(X_train,y_train)
tuning.best_params_, tuning.best_score_
min_samples_leaf_lgbm = tuning.best_params_.get("min_samples_leaf")

p_test5 = {'max_features':[2,3,4,5,6,7]}
tuning = GridSearchCV(estimator =GradientBoostingClassifier(learning_rate=learning_rate_gbm, n_estimators=n_estimators_gbm,
                                                            max_depth=max_depth_gbm,
                                                            min_samples_split=20, min_samples_leaf=min_samples_leaf_gbm,
                                                            subsample=1,
                                                            random_state=10), param_grid = p_test5, scoring='accuracy',
                                                            n_jobs=4, cv=5)
tuning.fit(X_train,y_train)
tuning.best_params_, tuning.best_score_
max_features_gbm = tuning.best_params_.get("max_features")

p_test6= {'subsample':[0.7,0.75,0.8,0.85,0.9,0.95,1]}

tuning = GridSearchCV(estimator =GradientBoostingClassifier(learning_rate=learning_rate_gbm, n_estimators=n_estimators_gbm,
                                                            max_depth=max_depth_gbm,
                                                            min_samples_split=20, min_samples_leaf=min_samples_leaf_gbm,
                                                            max_features=max_features_gbm ,
                                                            random_state=10), param_grid = p_test6, scoring='accuracy',
                                                            n_jobs=4, cv=5)
tuning.fit(X_train,y_train)
tuning.best_params_, tuning.best_score_
subsample_gbm = tuning.best_params_.get("subsample")

p_test6a= {'subsample':[0.7,0.75,0.8,0.85,0.9,0.95,1]}

tuning = GridSearchCV(estimator =LGBMClassifier(learning_rate=learning_rate_lgbm, n_estimators=n_estimators_lgbm,
                                                max_depth=max_depth_lgbm,
                                                min_samples_leaf=min_samples_leaf_lgbm,
                                                random_state=10), param_grid = p_test6, scoring='accuracy',
                                                n_jobs=4, cv=5)
tuning.fit(X_train,y_train)
tuning.best_params_, tuning.best_score_
subsample_lgbm = tuning.best_params_.get("subsample")

p_test7= {'random_state':list(range(0,101,2))}

tuning = GridSearchCV(estimator =GradientBoostingClassifier(learning_rate=learning_rate_gbm, n_estimators=n_estimators_gbm,
                                                            max_depth=max_depth_gbm,
                                                            min_samples_split=20, min_samples_leaf=min_samples_leaf_gbm,
                                                            max_features=max_features_gbm ,
                                                            subsample=subsample_gbm), param_grid = p_test7,
                                                            scoring='accuracy',
                                                            n_jobs=4, cv=5)
tuning.fit(X_train,y_train)
tuning.best_params_, tuning.best_score_
random_state_gbm = tuning.best_params_.get("random_state")

p_test7a= {'random_state':list(range(0,101,2))}

tuning = GridSearchCV(estimator =LGBMClassifier(learning_rate=learning_rate_lgbm, n_estimators=n_estimators_lgbm,
                                                max_depth=max_depth_lgbm, min_samples_leaf=min_samples_leaf_lgbm,
                                                subsample=subsample_lgbm), param_grid = p_test7a, scoring='accuracy',
                                                n_jobs=4, cv=5)
tuning.fit(X_train,y_train)
tuning.best_params_, tuning.best_score_
random_state_lgbm = tuning.best_params_.get("random_state")

a1, a2, a3, a4, a5, a6, a7, a8 = [], [], [], [], [], [], [], []

a1.append('GBM')
a2.append(learning_rate_gbm)
a3.append(n_estimators_gbm)
a4.append(max_depth_gbm)
a5.append(min_samples_leaf_gbm)
a6.append(max_features_gbm)
a7.append(subsample_gbm)
a8.append(random_state_gbm)

opt_par = pd.DataFrame({'Name': a1, 'learning_rate': a2, 'n_estimators': a3,
                         'max_depth': a4, 'min_samples_leaf': a5, 'max_features': a6,
                         'subsample_gbm': a7, 'random_state': a8})

a1.append('LGBM')
a2.append(learning_rate_lgbm)
a3.append(n_estimators_lgbm)
a4.append(max_depth_lgbm)
a5.append(min_samples_leaf_lgbm)
a6.append('--')
a7.append(subsample_lgbm)
a8.append(random_state_lgbm)

opt_par = pd.DataFrame({'Name': a1, 'learning_rate': a2, 'n_estimators': a3,
                         'max_depth': a4, 'min_samples_leaf': a5, 'max_features': a6,
                         'subsample_gbm': a7, 'random_state': a8})

opt_par

"""Evaluation of final model on test data"""

new=GradientBoostingClassifier(learning_rate=learning_rate_gbm, n_estimators=n_estimators_gbm,
                               max_depth=max_depth_gbm, min_samples_split=20, min_samples_leaf=min_samples_leaf_gbm,
                               max_features=max_features_gbm, subsample=subsample_gbm, random_state=random_state_gbm)
new.fit(X_train,y_train)
predictors=list(X_train)

print('Accuracy of the GBM on test set: {:.3f}'.format(new.score(X_test, y_test)))
pred=new.predict(X_test)
print(classification_report(y_test, pred))

new_lgbm=LGBMClassifier(learning_rate=learning_rate_lgbm, n_estimators=n_estimators_lgbm,max_depth=max_depth_lgbm,
                        min_samples_leaf=min_samples_leaf_lgbm, subsample=subsample_lgbm, random_state=random_state_lgbm)
new_lgbm.fit(X_train,y_train)
predictors=list(X_train)

print('Accuracy of the LGBM on test set: {:.3f}'.format(new_lgbm.score(X_test, y_test)))
pred=new_lgbm.predict(X_test)

print(classification_report(y_test, pred))

"""Comparison of ROC AUC

"""

from sklearn import metrics
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve



baseline = GradientBoostingClassifier(learning_rate=0.1, n_estimators=100,max_depth=3, min_samples_split=2,
                                      min_samples_leaf=1, subsample=1,max_features='sqrt', random_state=10)
baseline.fit(X_train,y_train)

model1 = GradientBoostingClassifier(learning_rate=learning_rate_gbm, n_estimators=n_estimators_gbm,max_depth=max_depth_gbm,
                                    min_samples_split=2,
                                    min_samples_leaf=1, subsample=1,max_features='sqrt', random_state=10)
model1.fit(X_train,y_train)

new=GradientBoostingClassifier(learning_rate=learning_rate_gbm, n_estimators=n_estimators_gbm,
                               max_depth=max_depth_gbm, min_samples_split=20, min_samples_leaf=min_samples_leaf_gbm,
                               max_features=max_features_gbm, subsample=subsample_gbm, random_state=random_state_gbm)
new.fit(X_train,y_train)
baseline_roc_auc = roc_auc_score(y_test, baseline.predict(X_test))
fprB, tprB, thresholdsB = roc_curve(y_test, baseline.predict_proba(X_test)[:,1])
#model 1
model1_roc_auc = roc_auc_score(y_test, model1.predict(X_test))
fpr1, tpr1, thresholds1 = roc_curve(y_test, model1.predict_proba(X_test)[:,1])
#new tuned model
new_roc_auc = roc_auc_score(y_test, new.predict(X_test))
fprnew, tprnew, thresholds_new = roc_curve(y_test, new.predict_proba(X_test)[:,1])

plt.figure()
plt.plot(fprB, tprB, label='GBM Baseline (area = %0.2f)' % baseline_roc_auc)
plt.plot(fpr1, tpr1, label='GBM Model 1 (area = %0.2f)' % model1_roc_auc)
plt.plot(fprnew, tprnew, label='GBM Final Model (area = %0.2f)' % new_roc_auc)

plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic of GBM')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()

plt.savefig('roc1.eps', format='eps')

print('Accuracy of the GBM on test set for Baseline Model: {:.3f}'.format(baseline.score(X_test, y_test)))
print('Accuracy of the GBM on test set for Model1: {:.3f}'.format(model1.score(X_test, y_test)))
print('Accuracy of the GBM on test set for New Model: {:.3f}'.format(new.score(X_test, y_test)))