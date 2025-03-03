import os

import pandas as pd
import numpy as np
import itertools

# User-defined scenario filter (can be left blank for all scenarios)
def _filter_capacity(grouped_capacity_, scenario = '' , status = ''):
    # Apply the scenario and status filters if specified
    if scenario and status:
        filtered_data = grouped_capacity_[
            (grouped_capacity_['Status'] == status) &
            (grouped_capacity_['Scenario'] == scenario)
        ]
    elif scenario:
        filtered_data = grouped_capacity_[
            (grouped_capacity_['Scenario'] == scenario)
        ]
    elif status:
        filtered_data = grouped_capacity_[
            (grouped_capacity_['Status'] == status)
        ]
    else:
        # If neither scenario nor gen_status is specified, no filtering applied
        filtered_data = grouped_capacity_

    # Convert to wide format by pivoting
    return filtered_data.pivot_table(index   = 'Technology',
                                     columns = ['Scenario', 'Period'],
                                     values  = 'Power',
                                     aggfunc = 'sum').reset_index(drop = False)

def _resource_adequacy(df_):

    df_p_ = df_.copy()
    
    df_p_['loss_of_load_hr'] = (df_p_['unserved_energy_mw'] > 0.)*1.

    df_p_['LOLF'] = np.diff(df_p_['loss_of_load_hr'].to_numpy(), prepend = 0)
    df_p_.loc[df_p_['LOLF'] < 0., 'LOLF'] = 0.

    df_pp_ = df_p_.groupby(['period', 
                            'scenario']).agg({'overgeneration_mw': 'sum', 
                                              'unserved_energy_mw': 'sum', 
                                              'static_load_mw': 'sum', 
                                              'loss_of_load_hr': 'sum', 
                                              'LOLF': 'sum'}).reset_index(drop = False)
    N = df_p_['unserved_energy_mw'].shape[0]
    df_pp_['EUE']  = 100.*df_pp_['unserved_energy_mw']/df_pp_['static_load_mw']
    df_pp_['LOLP'] = df_pp_['loss_of_load_hr']/N
    df_pp_['LOLD'] = df_pp_['loss_of_load_hr']/df_pp_['LOLF']
    
    df_pp_ = df_pp_.rename(columns = {'overgeneration_mw':  'Overgeneration (MWh)',
                                      'unserved_energy_mw': 'Unserved Energy (MWh)',
                                      'static_load_mw':     'Total Demand (MWh)',
                                      'loss_of_load_hr':    'Loss-Of-Load Events (hr)',
                                      'EUE':                'Expected Unserved Energy (%)',
                                      'LOLP':               'Loss-Of-Load Probability',
                                      'LOLF':               'Loss-Of-Load Frequency (per period)',
                                      'LOLD':               'Loss-Of-Load Duration (hr)'})
    
    return df_pp_.set_index('scenario').T
    
__all__ = ['_filter_capacity', 
           '_resource_adequacy']
