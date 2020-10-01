# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 23:34:42 2020

@author: NatalyR
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def preproc(df):    
    df.rename(columns=lambda x: x.replace('-', '_'), inplace=True)
    feature_names = df.columns[1:]
    # PastDue
    df['NumberOfTimes_PastDue'] = (df.NumberOfTime30_59DaysPastDueNotWorse + 
                                  df.NumberOfTimes90DaysLate + 
                                  df.NumberOfTime60_89DaysPastDueNotWorse)
    df['NumberOfTimesLate_high'] = np.where(
        df.NumberOfTime30_59DaysPastDueNotWorse > 95, 1, 0)
    df['NumberOfTimesLate_96'] = np.where(
        df.NumberOfTime30_59DaysPastDueNotWorse == 96, 1, 0)
    df['NumberOfTimesLate_98'] = np.where(
        df.NumberOfTime30_59DaysPastDueNotWorse == 98, 1, 0)
    df['NumberOfTime30_59Days_none'] = np.where(
        df.NumberOfTime30_59DaysPastDueNotWorse == 0, 1, 0)
    df['NumberOfTimes90Days_none'] = np.where(
        df.NumberOfTimes90DaysLate == 0, 1, 0)
    df['NumberOfTime60_89Days_none'] = np.where(
        df.NumberOfTime60_89DaysPastDueNotWorse == 0, 1, 0)
    df.NumberOfTime30_59DaysPastDueNotWorse[
        df.NumberOfTime30_59DaysPastDueNotWorse > 95] = 20
    df.NumberOfTimes90DaysLate[
        df.NumberOfTime30_59DaysPastDueNotWorse > 95] = 20
    df.NumberOfTime60_89DaysPastDueNotWorse[
        df.NumberOfTime60_89DaysPastDueNotWorse > 95] = 20
    df.NumberOfTime30_59DaysPastDueNotWorse = np.log1p(
        df.NumberOfTime30_59DaysPastDueNotWorse)
    df.NumberOfTimes90DaysLate = np.log1p(df.NumberOfTimes90DaysLate)
    df.NumberOfTime60_89DaysPastDueNotWorse = np.log1p(
        df.NumberOfTime60_89DaysPastDueNotWorse)
    # DebtRatio
    df['MonthlyIncomeFilled'] = df.MonthlyIncome
    df.MonthlyIncomeFilled.fillna(1, inplace=True)
    df['MonthlyPayment'] = df.DebtRatio * df.MonthlyIncomeFilled
    df = df.drop('MonthlyIncomeFilled', axis=1)
    df['MonthlyIncome_none'] = np.where(
        df.MonthlyIncome.isna(), 1, 0)
    df['MonthlyIncome_zero'] = np.where(
        df.MonthlyIncome==0.0, 1, 0)
    df['DebtRatio_zero'] = np.where(
        df.DebtRatio==0.0, 1, 0)
    df.DebtRatio[df.DebtRatio > 1.0] = 0.0
    df['DebtRatio_log'] = np.log1p(df.DebtRatio)
    # RUUL
    df['RUUL_high'] = np.where(
        df.RevolvingUtilizationOfUnsecuredLines > 1, 1, 0)
    df['RUUL_zero'] = np.where(
        df.RevolvingUtilizationOfUnsecuredLines==0, 1, 0)
    df['RUUL_ones'] = np.where(
        df.RevolvingUtilizationOfUnsecuredLines==1, 1, 0)
    df['RUUL_log'] = np.log1p(df.RevolvingUtilizationOfUnsecuredLines)
    
    # Nan & 0
    rep_age = df.age.mode()
    df.age[df.age==0] = int(rep_age)
    del rep_age
    df['NumberOfDependents_none'] = np.where(
        df.NumberOfDependents.isna(), 1, 0)
    df.NumberOfDependents.fillna(0, inplace=True)
    df_mi = df.dropna()
    
    choose_cols = list(feature_names)
    del choose_cols[4]
    
    X_mi = df_mi[choose_cols]
    y_mi = df_mi.MonthlyIncome
    
    rf_reg = RandomForestRegressor(n_estimators=100).fit(X_mi, y_mi)
    df_fill_mi = df[df.MonthlyIncome.isna()]
    
    mi_fill = rf_reg.predict(df_fill_mi[choose_cols])
    df.loc[df.MonthlyIncome.isna(), 'MonthlyIncome'] = mi_fill

    df['NumberOfCredits_perPerson'] = df.NumberOfOpenCreditLinesAndLoans / (
        1 + df.NumberOfDependents)
    df['NumberRealEstate_perPerson'] = df.NumberRealEstateLoansOrLines / (
        1 + df.NumberOfDependents)
    df['MonthlyIncome_perPerson'] = df.MonthlyIncome / (
        1 + df.NumberOfDependents)
    df['Household_size'] = np.log1p(df.NumberOfDependents)

    df['NOCLL_log'] = np.log1p(df.NumberOfOpenCreditLinesAndLoans)
    df['NRELL_log'] = np.log1p(df.NumberRealEstateLoansOrLines)
    df['NumberOfDependents_log'] = np.log1p(df.NumberOfDependents)
    df['MonthlyIncome_log'] = np.log1p(df.MonthlyIncome)
    
    df = df.drop(['NumberOfOpenCreditLinesAndLoans', 'MonthlyIncome',
             'NumberRealEstateLoansOrLines', 'NumberOfDependents',
             'MonthlyIncome', 'DebtRatio',
              'RevolvingUtilizationOfUnsecuredLines'], axis=1)