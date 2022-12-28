import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
import pickle

# import cleaned data
df = pd.read_csv('YT_data_cleaned.csv')

# choose variables
df.columns

df_model = df[['likes', 'cat_id', 'vid_duration', 'definition', 'comments',
               'veiws', 'desc_length']]

# get dummy vars
df_dum = pd.get_dummies(df_model)

# create train test split
X = df_dum.drop('likes', axis=1)
y = df_dum['likes'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Multible Linear Regression
mlr = LinearRegression()
mlr.fit(X_train, y_train)

cv_score_mlr = np.mean(cross_val_score(mlr, X_train, y_train, cv = 3, scoring='neg_mean_absolute_error'))

# Lasso Regression
las = Lasso(max_iter = 3000)
las.fit(X_train, y_train)

cv_score_las = np.mean(cross_val_score(las, X_train, y_train, cv = 3, scoring='neg_mean_absolute_error'))

# Ridge Regression
rdg = Lasso(max_iter = 3000)
rdg.fit(X_train, y_train)

cv_score_rdg = np.mean(cross_val_score(rdg, X_train, y_train, cv = 3, scoring='neg_mean_absolute_error'))

# Random Forest Regression
rf = RandomForestRegressor()
rf.fit(X_train, y_train)

cv_score_rf = np.mean(cross_val_score(rf, X_train, y_train, cv=3, scoring='neg_mean_absolute_error'))

# use gridsearch to optimize rf model
rf_parameters = {'n_estimators':range(10,300,10),
                 'criterion':('squared_error', 'absolute_error', 'friedman_mse', 'poisson'),
                 'max_features':('auto', 'sqrt', 'log2', 1.0)}
rf_gs = GridSearchCV(rf, rf_parameters, cv=3)
rf_gs.fit(X_train, y_train)

rf_gs.best_score_
rf_gs.best_estimator_

cv_score_rf_gs = np.mean(cross_val_score(rf_gs.best_estimator_, X_train, y_train,
                                         cv=3, scoring='neg_mean_absolute_error'))
# test models with test dataset
t_pred_mlr = mlr.predict(X_test)
t_pred_las = las.predict(X_test)
t_pred_rdg = rdg.predict(X_test)
t_pred_rf = rf_gs.best_estimator_.predict(X_test)

mae_mlr = mean_absolute_error(y_test, t_pred_mlr)
mae_las = mean_absolute_error(y_test, t_pred_las)
mae_rdg = mean_absolute_error(y_test, t_pred_rdg)
mae_rf = mean_absolute_error(y_test, t_pred_rf)

# pickle best model
model = rf_gs.best_estimator_
pickle.dump(model, open('YT_likes_model.pkl', 'wb'))

model.predict(X_test.iloc[1].array.reshape(1, -1))