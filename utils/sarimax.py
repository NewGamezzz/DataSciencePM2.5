from utils.base import *

def sarimax_training(best_order, best_seasonal_order, train_data, exog_columns, target):
  mod = SARIMAX(train_data[target],
              exog=train_data[exog_columns],
              order=best_order,
              seasonal_order=best_seasonal_order,
              enforce_stationarity=False,
              enforce_invertibility=False)

  result = mod.fit()

  results_exog = []
  
  for e in exog_columns:
    mod_exog = SARIMAX(train_data[e],
              order=best_order,
              seasonal_order=best_seasonal_order,
              enforce_stationarity=False,
              enforce_invertibility=False)

    result_exog = mod_exog.fit()
    results_exog.append(result_exog)
  return result, results_exog


def predict_target(result, results_exog, exog_columns, steps=12):
  li = []
  for exog_name, result_exog in zip(exog_columns, results_exog):
    forcast_exog = result_exog.forecast(steps=steps).rename(exog_name)
    li.append(forcast_exog)
  forcast_exog = pd.concat(li, axis=1)

  return result.forecast(exog=forcast_exog[exog_columns], steps=steps)