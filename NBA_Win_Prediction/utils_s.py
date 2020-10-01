# -*- coding: utf-8 -*-
"""
Created on Sat May 16 13:50:29 2020

@author: NatalyR
"""

import pandas as pd
import numpy as np

def preproc_s(train_part):
    train_part['home_win'] = np.where(
        (train_part.host_score - train_part.visitor_score) > 0, 1, 0)
    train_part['visitor_win'] = np.where(
        (train_part.host_score - train_part.visitor_score) < 0, 1, 0)
    
    train_part['num_hostGames_season9'] = (
        train_part.groupby('host')['host'].transform('count'))
    train_part['num_visitorGames_season9'] = (
        train_part.groupby('visitor')['visitor'].transform('count'))
    
    train_part['num_hostWins_season9'] = (
        train_part.groupby('host')['home_win'].transform('sum'))
    train_part['num_visitorWins_season9'] = (
        train_part.groupby('visitor')['visitor_win'].transform('sum'))
    
    train_part['differ'] = train_part.host_score - train_part.visitor_score
    train_part['diff_range'] = pd.cut(
        train_part['differ'],
        bins=[-np.inf, -28, -16, 20, 32, np.inf],
        labels=[
            'super_neg_diff', 'large_neg_diff', 'middle', 'large_pos_diff',
            'super_pos_diff'
        ])
    
    del train_part['differ']
    
    train_part_cat = pd.get_dummies(train_part.diff_range)
    train_part_new = pd.concat((train_part, train_part_cat), axis=1)
    
    del train_part_new['diff_range'], train_part_new['middle']
    
    train_part_new['num_super_negDiff'] = train_part_new.groupby(
    ['host', 'super_neg_diff'])['super_neg_diff'].transform('sum')
    train_part_new['num_super_posDiff'] = train_part_new.groupby(
    ['host', 'super_pos_diff'])['super_pos_diff'].transform('sum')

    train_part_new['num_large_negDiff'] = train_part_new.groupby(
        ['host', 'large_neg_diff'])['large_neg_diff'].transform('sum')
    train_part_new['num_large_posDiff'] = train_part_new.groupby(
        ['host', 'large_pos_diff'])['large_pos_diff'].transform('sum')
    
    del (train_part_new['super_neg_diff'], train_part_new['large_neg_diff'],
         train_part_new['large_pos_diff'], train_part_new['super_pos_diff'])
    
    train_part_new['superPosDiff_ratio_season9'] = train_part_new[
        'num_super_posDiff'] / train_part_new['num_hostGames_season9']
    train_part_new['largePosDiff_ratio_season9'] = train_part_new[
        'num_large_posDiff'] / train_part_new['num_hostGames_season9']

    train_part_new['superNegDiff_ratio_season9'] = train_part_new[
        'num_super_negDiff'] / train_part_new['num_visitorGames_season9']
    train_part_new['largeNegDiff_ratio_season9'] = train_part_new[
        'num_large_negDiff'] / train_part_new['num_visitorGames_season9']
    
    del (train_part_new['num_super_negDiff'], 
         train_part_new['num_super_posDiff'],
         train_part_new['num_large_negDiff'], 
         train_part_new['num_large_posDiff'],train_part_new['year'], 
         train_part_new['month'], train_part_new['host_score'], 
         train_part_new['visitor_score'])
    
    train_part_new['host_winRatio_season9'] = train_part_new[
        'num_hostWins_season9'] / train_part_new['num_hostGames_season9']
    train_part_new['visitor_winRatio_season9'] = train_part_new[
        'num_visitorWins_season9'] / train_part_new['num_visitorGames_season9']
    
    train_part_new[
        'host_diffRatio_season9'] = (train_part_new.largePosDiff_ratio_season9+
                                     train_part_new.superPosDiff_ratio_season9)
    train_part_new[
        'visitor_diffRatio_season9'] = (train_part_new.largeNegDiff_ratio_season9+
                                      train_part_new.superNegDiff_ratio_season9)
                                      
    del (train_part_new['num_hostGames_season9'],
         train_part_new['num_visitorGames_season9'],
         train_part_new['num_hostWins_season9'],
         train_part_new['num_visitorWins_season9'],
         train_part_new['superPosDiff_ratio_season9'],
         train_part_new['superNegDiff_ratio_season9'],
         train_part_new['largePosDiff_ratio_season9'],
         train_part_new['largeNegDiff_ratio_season9'],
         train_part_new['visitor_win'])

    train_part_new[
        'host_ratio_season9'] = (train_part_new.host_diffRatio_season9 + 
                             train_part_new.host_winRatio_season9)
    train_part_new[
        'visitor_ratio_season9'] = (train_part_new.visitor_diffRatio_season9 + 
                                train_part_new.visitor_winRatio_season9)                                  
                                    
    del (train_part_new['host_diffRatio_season9'],
         train_part_new['host_winRatio_season9'],
         train_part_new['visitor_diffRatio_season9'],
         train_part_new['visitor_winRatio_season9'])                               
    
    train_part_new['host_ratio_season9'] = (
        train_part_new.groupby('host')['host_ratio_season9'].transform('mean'))
    train_part_new['visitor_ratio_season9'] = (
        train_part_new.groupby('visitor')['visitor_ratio_season9'].transform('mean'))
        
    train_part_new['host_ratio_season9'] = (
        train_part_new['host_ratio_season9'].apply(lambda x: round(x, 5)))
    train_part_new['visitor_ratio_season9'] = (
        train_part_new['visitor_ratio_season9'].apply(lambda x: round(x, 5)))
    
    return train_part_new    
    