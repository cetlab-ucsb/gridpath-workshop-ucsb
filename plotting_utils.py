import os

import pandas as pd
import numpy as np
import itertools

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# TODO:
# * Short the legend following the color code

plt.rcParams['legend.handlelength'] = 1
plt.rcParams['legend.handleheight'] = 1.125
plt.rcParams["font.family"]         = "Avenir"
#mpl.rcParams['pdf.fonttype'] = 42

mpl.rcParams.update({"pdf.use14corefonts": True})

tech_colors_  = pd.DataFrame(columns = ['color'], 
                             index   = ['Battery', 'Hydrogen', 'WHR',  'Nuclear', 
                                        'Biomass', 'Hydro_Pumped', 'Hydro_ROR', 'Hydro_Storage', 
                                        'Diesel', 'CCGT', 'CT', 'Subcritical_Coal_Large', 
                                        'Subcritical_Coal_Small', 'Supercritical_Coal', 'SolarPV_tilt', 'SolarPV_single', 
                                        'Wind', 'Export', 'Curtailment', 'Tx_Losses', 'Import'])

tech_colors_['color'] = ['#e7c41f', 'teal', '#6ba661', '#8d72b3', 
                         '#6a96ac', '#2a648a', '#2a648a', '#2a648a', 
                         '#924B00', '#6c757d', '#6c757d', '#343a40', 
                         '#343a40', '#343a40', '#ef9226', '#daac77', 
                         '#8dc0cd', '#55A182', '#c94f39', '#656d4a', '#900C3F']

color_groups_  = pd.DataFrame(columns = ['color'], 
                             index   = ['Battery', 'Hydrogen', 'Other',  'Nuclear', 
                                        'Pumped Storage', 'Hydro', 'Diesel', 'Gas', 
                                        'Coal', 'Solar', 'Wind', 'Export', 
                                        'Curtailment', 'Tx_Losses', 'Import'])

color_groups_['color'] = ['#e7c41f', 'teal', '#6ba661', '#8d72b3', 
                          '#6a96ac', '#2a648a', '#924B00', '#6c757d', 
                          '#343a40', '#ef9226', '#8dc0cd', '#55A182', 
                          '#c94f39', '#656d4a', '#900C3F']

scen_colors_ = pd.DataFrame(columns = ['color', 'lines'], 
                            index   = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'])
    
scen_colors_['color'] = ['#92918B', '#126463', '#521A1A', '#2CB7B5', '#756A00', '#CA8250', '#D8A581', '#1F390D', '#900C3F']
scen_colors_['lines'] = ['solid', 'solid', 'dotted', 'dotted', 'dashed', 'dashed', 'dashdot', 'dashdot', 'dashdot']


# Plot new and existing capacity for different scenarios
def _plot_new_and_existing_capacity(data_, scens_label_, tech_label_,
                                    units        = 1e3,
                                    units_label  = '(GW)',
                                    y_period     = 0.,
                                    y_grid_inc   = 500,
                                    div_line_len = 0.,
                                    save         = True,
                                    legend       = True,
                                    title        = '',
                                    file_name    = 'noname.pdf'):

    def __make_new_and_existing_capacit_legend(df_, techs_, colors_, ax):

        ax.bar(0., 0., 0., bottom    = 0.,
                           label     = 'Existing',
                           color     = 'None',
                           lw        = 0.,
                           hatch     = 'xx',
                           edgecolor = 'lightgray',
                           zorder    = 10)

        for tech, i_tech in zip(techs_, range(len(techs_))):
            idx_ = df_['Technology'] == tech
            if idx_.sum() > 1:
                if df_.loc[idx_, 'Power'].sum() != 0:
                    ax.bar(0., 0., 0., bottom = 0.,
                                       color  = colors_[i_tech],
                                       label  = tech,
                                       zorder = 10)

    scens_  = scens_label_['scenario'].to_list()
    labels_ = scens_label_['label'].to_list()
    zones_  = scens_label_['zone'].to_list()

    periods_ = np.sort(data_['Period'].unique())

    techs_, idx_ = np.unique(tech_label_['group'], return_index = True)
    colors_      = tech_label_.loc[tech_label_.index[idx_], 'group_color'].to_list()


    offset = 0.
    y_max  = 0
    width  = .225
    x_     = np.linspace(0, len(periods_) - 1, len(periods_))
    fig = plt.figure(figsize = (10, 7.5))
    ax  = plt.subplot(111)

    ticks_        = []
    ticks_labels_ = []
    ticks_labels_length_ = []

    offsets_  = []
    lengths_  = []
    x_period_ = []
    for scen, i_scen in zip(scens_, range(len(scens_))):

        zone = zones_[i_scen]

        df_ = data_.loc[data_['Zone'] == zone].sort_values(by = ['Period'])

        lengths_.append(len(scen))
        for period, i_period in zip(periods_, range(len(periods_))):
            if (i_scen == 0) & (i_period == 0): __make_new_and_existing_capacit_legend(df_, techs_, colors_, ax)

            for tech, i_tech in zip(techs_, range(len(techs_))):
                idx_ = (df_['Zone'] == zone) & (df_['Period'] == period)
                idx_ = idx_ & (df_['Scenario'] == scen) & (df_['Technology'] == tech)
                idx_ = idx_ & (df_['Status'] == 'existing')

                if idx_.sum() == 1.:
                    power = df_.loc[idx_, 'Power'].to_numpy()[0]
                    color = tech_label_.loc[tech_label_['group'] == tech, 'group_color'] .unique()

                    ax.bar(x_[i_period], power/units, width, bottom    = offset/units,
                                                             color     = color,
                                                             lw        = 0.,
                                                             hatch     = 'x',
                                                             edgecolor = 'lightgray', zorder = 10)

                    offset += power

            for tech, i_tech in zip(techs_, range(len(techs_))):
                idx_ = (df_['Zone'] == zone) & (df_['Period'] == period) & (df_['Scenario'] == scen)
                idx_ = idx_ & (df_['Technology'] == tech) & (df_['Status'] == 'new')

                if idx_.sum() == 1.:
                    power = df_.loc[idx_, 'Power'].to_numpy()[0]
                    color = tech_label_.loc[tech_label_['group'] == tech, 'group_color'] .unique()

                    ax.bar(x_[i_period], power/units, width, bottom = offset/units,
                                                             color  = color,
                                                             zorder = 10)

                    offset += power

            if y_max < offset:
                y_max = offset

            ticks_.append(x_[i_period])
            ticks_labels_.append('{}'.format(labels_[i_scen]))
            offsets_.append(offset/units)

            ticks_labels_length_.append(len(ticks_labels_[-1]))


            offset = 0.

            x_period_.append(x_[i_period])


        x_ = x_ + .9/len(scens_)
    z_ = x_ - .9/len(scens_)

    y_period_ = np.max(np.array(offsets_).reshape(len(periods_), len(scens_)), axis = 0)
    x_period_ = np.mean(np.array(x_period_).reshape(len(periods_), len(scens_)), axis = 0) 

    for x_period, y_period, period in zip(x_period_, y_period_, periods_):
        plt.text(x_period, (0.05*y_period_[-1] + y_period), '{}'.format(period), fontsize            = 18, 
                                                                                 weight              = 'bold',
                                                                                 horizontalalignment = 'center', 
                                                                                 verticalalignment   = 'center')

    x_ = np.linspace(0, len(periods_), len(periods_) + 1)
    dz = (x_[1] - z_[0])
    for x in x_:
        ax.axvline(x - dz/2., ymin      = div_line_len,
                              ymax      = 0.,
                              linewidth = .75,
                              linestyle = '-',
                              color     = 'k',
                              clip_on   = False,
                              zorder    = 10)

    N_steps  = int(np.ceil((y_max/units)/y_grid_inc))
    y_ticks_ = np.linspace(0, int(N_steps*y_grid_inc), N_steps + 1, dtype = int)

    ax.set_xticks(ticks_, ticks_labels_, rotation = 90)

    ax.xaxis.set_tick_params(labelsize = 12, left = False)
    ax.yaxis.set_tick_params(labelsize = 12, left = False)

    ax.set_ylabel(units_label, fontsize = 18)
    ax.set_yticks(y_ticks_, y_ticks_)

    if legend:
        ax.legend(loc            = 'center left',
                  bbox_to_anchor = (1, 0.5),
                  frameon        = False,
                  prop           = {'size': 12})

    plt.ylim(-1.,y_period_.max()*1.2)

    plt.title(title, fontsize = 20,
                     y        = 0.912)

    ax.spines[['right', 'top', 'left', 'bottom']].set_visible(False)
    plt.grid(axis = 'y')

    if save:
        plt.savefig(file_name, bbox_inches = 'tight', dpi = 300)
        plt.show()



# Plot GHG emissions for different scenarios
def _plot_emissions(emissions_, scen_labels_, save       = False,
                                              title      = '',
                                              legend     = False,
                                              units      = 1e6,
                                              unit_label = r'GHG Emissions (MtCO$_2$)',
                                              file_name  = 'noname.pdf'):


    scens_      = scen_labels_['scenario'].to_list()
    zones_      = scen_labels_['zone'].to_list()
    colors_     = scen_labels_['color'].to_list()
    labels_     = scen_labels_['label'].to_list()
    linestyles_ = scen_labels_['linestyle'].to_list()


    data_ = emissions_.groupby(['Scenario', 'Period', 'Zone']).sum().reset_index(drop = False)


    fig = plt.figure(figsize = (4., 5))
    ax  = plt.subplot(111)

    for i_scen in range(len(scens_)):

        df_ = data_.loc[(data_['Scenario'] == scens_[i_scen]) & (emissions_['Zone'] == zones_[i_scen])]

        ax.plot(df_['Period'], df_['GHG']/units, color     = colors_[i_scen],
                                                 linestyle = linestyles_[i_scen],
                                                 label     = '{}'.format(labels_[i_scen]),
                                                 linewidth = 1.5,
                                                 alpha     = 0.75)

    x_labels_ = emissions_['Period'].unique()
    x_        = np.linspace(0, x_labels_.shape[0] - 1, x_labels_.shape[0])

    ax.set_xticks(x_, x_labels_)
    ax.xaxis.set_tick_params(labelsize = 14)
    ax.yaxis.set_tick_params(labelsize = 14)
    ax.set_ylabel(r'GHG Emissions (MtCO$_2$)', fontsize = 18)
    ax.set_ylim(df_['GHG'].min()*.9/units,df_['GHG'].max()*1.1/units)

    if legend:
        ax.legend(loc            = 'center left',
                  title          = 'Scenarios',
                  bbox_to_anchor = (1, 0.5),
                  frameon        = False,
                  title_fontsize = 16,
                  prop           = {'size': 12})

    plt.title(title, fontsize = 18,
                     y        = 0.9125)

    if save: plt.savefig(file_name, bbox_inches = 'tight',
                                    dpi         = 300)

    plt.show()
    
    
# Plot system cost for different scenarios
def _plot_system_cost(system_cost_, scens_, scen_lables_, colors_, zone, save      = False, 
                                                                         legend    = False,
                                                                         title     = '', 
                                                                         path      = '', 
                                                                         file_name = 'noname.pdf'):

    fig = plt.figure(figsize = (4, 5))
    ax  = plt.subplot(111)
    
    for i_scen in range(len(scens_)):
        scen  = scens_[i_scen]
        data_ = system_cost_.loc[(system_cost_['Scenario'] == scen) & (system_cost_['Zone'] == zone)]
        idx_  = np.argsort(data_['Period'])

        ax.plot(data_['Period'].to_numpy()[idx_], data_['LCOE'].to_numpy()[idx_], 
                color     = colors_.loc['C{}'.format(i_scen + 1), 'color'],                                                 
                linestyle = colors_.loc['C{}'.format(i_scen + 1), 'lines'],                                                 
                label     = '{}'.format(scen_lables_[i_scen]),                                                             
                linewidth = 1.5,                                                                  
                alpha     = 0.75) 
    
    x_labels_ = np.sort(system_cost_['Period'].unique())
    x_        = np.linspace(0, x_labels_.shape[0] - 1, x_labels_.shape[0])
    
    ax.set_xticks(x_, x_labels_)
    ax.xaxis.set_tick_params(labelsize = 14)
    ax.yaxis.set_tick_params(labelsize = 14)
    ax.set_ylabel(r'Costs (USD per MWh)', fontsize = 18)
    #ax.set_ylim(40, 75)

    if legend:
        ax.legend(loc            = 'center left', 
                  title          = 'Scenario',
                  bbox_to_anchor = (1, 0.5), 
                  frameon        = False,
                  title_fontsize = 16,
                  prop           = {'size': 12})
    
    plt.title(title, fontsize = 18, 
                     y        = 0.9125)

    #plt.ylim(data_.min() - 0.035*data_.min(), data_.max() + 0.035*data_.max())

    if save: plt.savefig(path + file_name, bbox_inches = 'tight', 
                                           dpi         = 300)

    plt.show()
#
# # Plot GHG emissions for different scenarios
# def _plot_emissions(emissions_, scen_labels_, save      = False,
#                                               title     = '',
#                                               legend    = False,
#                                               units = 1e6,
#                                               unit_label = r'GHG Emissions (MtCO$_2$)',
#                                               file_name = 'noname.pdf'):
#
#
#     scens_      = scen_labels_['scenario'].to_list()
#     zones_      = scen_labels_['zone'].to_list()
#     colors_     = scen_labels_['color'].to_list()
#     labels_     = scen_labels_['label'].to_list()
#     linestyles_ = scen_labels_['linestyle'].to_list()
#
#
#     data_ = emissions_.groupby(['Scenario', 'Period', 'Zone']).sum().reset_index(drop = False)
#
#
#     fig = plt.figure(figsize = (4., 5))
#     ax  = plt.subplot(111)
#
#     for i_scen in range(len(scens_)):
#
#         df_ = data_.loc[(data_['Scenario'] == scens_[i_scen]) & (emissions_['Zone'] == zones_[i_scen])]
#
#         ax.plot(df_['Period'], df_['GHG']/units, color     = colors_[i_scen],
#                                                      linestyle = linestyles_[i_scen],
#                                                      label     = '{}'.format(labels_[i_scen]),
#                                                      linewidth = 1.5,
#                                                      alpha     = 0.75)
#
#     x_labels_ = np.sort(emissions_['Period'].unique())
#     x_        = np.linspace(0, x_labels_.shape[0] - 1, x_labels_.shape[0])
#
#     ax.set_xticks(x_, x_labels_)
#     ax.xaxis.set_tick_params(labelsize = 14)
#     ax.yaxis.set_tick_params(labelsize = 14)
#     ax.set_ylabel(unit_label, fontsize = 18)
#     #ax.set_ylim(0, 100)
#
#     if legend:
#         ax.legend(loc            = 'center left',
#                   title          = 'Scenarios',
#                   bbox_to_anchor = (1, 0.5),
#                   frameon        = False,
#                   title_fontsize = 16,
#                   prop           = {'size': 12})
#
#     plt.title(title, fontsize = 18,
#                      y        = 0.9125)
#
#     if save: plt.savefig(file_name, bbox_inches = 'tight',
#                                     dpi         = 300)
#
#     plt.show()
#

# Plot GHG emissions for different scenarios
def _plot_emissions_intensity(emissions_, scen_labels_, save       = False,
                                                        title      = '',
                                                        legend     = False,
                                                        unit_label = r'GHG Intensity (MtCO$_2$/MWh)',
                                                        file_name  = 'noname.pdf'):


    scens_      = scen_labels_['scenario'].to_list()
    zones_      = scen_labels_['zone'].to_list()
    colors_     = scen_labels_['color'].to_list()
    labels_     = scen_labels_['label'].to_list()
    linestyles_ = scen_labels_['linestyle'].to_list()
    data_       = emissions_.groupby(['Scenario', 'Period', 'Zone']).sum().reset_index(drop = False)

    fig = plt.figure(figsize = (4., 5))
    ax  = plt.subplot(111)

    for i_scen in range(len(scens_)):

        df_ = data_.loc[(data_['Scenario'] == scens_[i_scen]) & (emissions_['Zone'] == zones_[i_scen])]

        ax.plot(df_['Period'], df_['Intensity'], color     = colors_[i_scen],
                                                 linestyle = linestyles_[i_scen],
                                                 label     = '{}'.format(labels_[i_scen]),
                                                 linewidth = 1.5,
                                                 alpha     = 0.75)

    x_labels_ = np.sort(emissions_['Period'].unique())
    x_        = np.linspace(0, x_labels_.shape[0] - 1, x_labels_.shape[0])

    ax.set_xticks(x_, x_labels_)
    ax.xaxis.set_tick_params(labelsize = 14)
    ax.yaxis.set_tick_params(labelsize = 14)
    ax.set_ylabel(unit_label, fontsize = 18)
    ax.set_ylim(df_['Intensity'].min()*0.9, df_['Intensity'].max()*1.1)

    if legend:
        ax.legend(loc            = 'center left',
                  title          = 'Scenarios',
                  bbox_to_anchor = (1, 0.5),
                  frameon        = False,
                  title_fontsize = 16,
                  prop           = {'size': 12})

    plt.title(title, fontsize = 18,
                     y        = 0.9125)

    if save: plt.savefig(file_name, bbox_inches = 'tight',
                                    dpi         = 300)

    plt.show()

# Plot system cost for different scenarios
def _plot_system_cost(system_cost_, scen_labels_, save       = False,
                                                  legend     = False,
                                                  title      = '',
                                                  units      = 1,
                                                  unit_label = r'Costs (USD per MWh)',
                                                  file_name  = 'noname.pdf'):

    scens_      = scen_labels_['scenario'].to_list()
    zones_      = scen_labels_['zone'].to_list()
    colors_     = scen_labels_['color'].to_list()
    labels_     = scen_labels_['label'].to_list()
    linestyles_ = scen_labels_['linestyle'].to_list()
    data_       = system_cost_.groupby(['Scenario', 'Period', 'Zone']).sum().reset_index(drop = False)

    fig = plt.figure(figsize = (4, 5))
    ax  = plt.subplot(111)

    for i_scen in range(len(scens_)):
        scen  = scens_[i_scen]
        data_ = system_cost_.loc[(system_cost_['Scenario'] == scen) & (system_cost_['Zone'] == zones_[i_scen])]
        idx_  = np.argsort(data_['Period'])

        ax.plot(data_['Period'].to_numpy()[idx_], data_['LCOE'].to_numpy()[idx_],
                color     = colors_[i_scen],
                linestyle = linestyles_[i_scen],
                label     = labels_[i_scen],
                linewidth = 1.5,
                alpha     = 0.75)

    x_labels_ = np.sort(system_cost_['Period'].unique())
    x_        = np.linspace(0, x_labels_.shape[0] - 1, x_labels_.shape[0])

    ax.set_xticks(x_, x_labels_)
    ax.xaxis.set_tick_params(labelsize = 14)
    ax.yaxis.set_tick_params(labelsize = 14)
    ax.set_ylabel(unit_label, fontsize = 18)
    ax.set_ylim(data_['LCOE'].min()*0.9,  data_['LCOE'].max()*1.1)

    if legend:
        ax.legend(loc            = 'center left',
                  title          = 'Scenario',
                  bbox_to_anchor = (1, 0.5),
                  frameon        = False,
                  title_fontsize = 16,
                  prop           = {'size': 12})

    plt.title(title, fontsize = 18,
                     y        = 0.9125)

    if save: plt.savefig(file_name, bbox_inches = 'tight', dpi = 300)

    plt.show()

# Plot energy dispatch per technology for different scenarios
def _plot_dispatch(data_, scens_label_, tech_label_,
                   units        = 1e6,
                   units_label  = r'Electricity Generation (TWh)',
                   y_period     = 0.,
                   y_grid_inc   = 500,
                   div_line_len = 0.,
                   save         = True,
                   legend       = True,
                   title        = '',
                   file_name    = 'noname.pdf'):

    def __make_dispatch_legend(data_, techs_, colors_, ax):
        for tech, i_tech in zip(techs_, range(len(techs_))):
            idx_ = data_['Technology'] == tech
            if idx_.sum() > 1:
                if data_.loc[idx_, 'Energy'].to_numpy().sum() != 0:
                    ax.bar(0., 0., 0., bottom = 0.,
                                       color  = colors_[i_tech],
                                       label  = tech.replace('_', ' '),
                                       zorder = 2,
                                       ec     = 'None',
                                       lw     = 0.,
                                       aa     = True)


    scens_  = scens_label_['scenario'].to_list()
    labels_ = scens_label_['label'].to_list()
    zones_  = scens_label_['zone'].to_list()

    periods_ = np.sort(data_['Period'].unique())
    techs_   = pd.unique(tech_label_['group'])

    colors_ = [tech_label_.loc[tech_label_['group'] == tech, 'group_color'].unique()[0] for tech in techs_]

    width           = .225
    offset_positive = 0.
    offset_negative = 0.
    y               = 0
    y_max           = 0
    y_min           = 0

    x_  = np.linspace(0, len(periods_) - 1, len(periods_))

    fig = plt.figure(figsize = (10., 7.5))
    ax  = plt.subplot(111)

    ticks_        = []
    ticks_labels_ = []
    x_period_     = []
    y_period_     = []
    offset_       = []
    for scen, i_scen in zip(scens_, range(len(scens_))):

        zone = zones_[i_scen]
        df_  = data_.loc[data_['Zone'] == zone].sort_values(by = ['Period'])

        for period, i_period in zip(periods_, range(len(periods_))):

            if (i_scen == 0) & (i_period == 0): __make_dispatch_legend(df_, techs_, colors_, ax)

            for tech, i_tech in zip(techs_, range(len(techs_))):
                idx_ = (df_['Scenario'] == scen) & (df_['Technology'] == tech) & (df_['Period'] == period)

                if idx_.sum() == 1:
                    energy = df_.loc[idx_, 'Energy'].to_numpy()[0]
                    color  = tech_label_.loc[tech_label_['group'] == tech, 'group_color'].unique()

                    if energy != 0:
                        if energy > 0:
                            offset = offset_positive
                        else:
                            offset = offset_negative

                        ax.bar(x_[i_period], energy/units, width, bottom = offset/units,
                                                                  color  = color,
                                                                  zorder = 2,
                                                                  ec     = 'None',
                                                                  lw     = 0.,
                                                                  aa     = True)

                        if energy >= 0:
                            offset_positive += energy
                        else:
                            offset_negative += energy

                if y_max < offset_positive:
                    y_max = offset_positive

            ticks_.append(x_[i_period])
            ticks_labels_.append('{}'.format(labels_[i_scen]))

            if offset_negative/units < y_min: y_min = offset_negative/units
            if offset_positive/units > y_max: y_max = offset_positive/units

            x_period_.append(x_[i_period])
            y_period_.append(offset_positive)
            offset_.append(offset_negative)
            offset_positive = 0.
            offset_negative = 0.
            #x_period_.append(x_[i_period])

            y += 1

        x_ = x_ + .9/len(scens_)
    z_ = x_ - .9/len(scens_)

    x_period_ = np.mean(np.array(x_period_).reshape(len(periods_), len(scens_)), axis = 0)
    y_period_ = np.max(np.array(y_period_).reshape(len(periods_), len(scens_)), axis = 0)

    for x_period, y_period, period in zip(x_period_, y_period_, periods_):
        plt.text(x_period, (0.05*y_period_[-1] + y_period)/units, '{}'.format(period), fontsize            = 18, 
                                                                                       weight              = 'bold',
                                                                                       horizontalalignment = 'center', 
                                                                                       verticalalignment   = 'center')

    ax.set_xticks(ticks_, ticks_labels_, rotation = 90)
    ax.xaxis.set_tick_params(labelsize = 12, left = False)

    N_steps  = int(np.ceil((y_max/units)/y_grid_inc))
    y_ticks_ = np.linspace(0, int(N_steps*y_grid_inc), N_steps + 1, dtype = int)

    ax.set_ylabel(units_label, fontsize = 18)
    ax.set_yticks(y_ticks_, y_ticks_)
    ax.yaxis.set_tick_params(labelsize = 12, left = False)


    x_ = np.linspace(0, len(periods_), len(periods_) + 1)
    dz = (x_[1] - z_[0])
    for x in x_:
        ax.axvline(x - dz/2., ymin      = div_line_len,
                              ymax      = 0.,
                              linewidth = .75,
                              linestyle = '-',
                              color     = 'k',
                              clip_on   = False,
                              zorder    = 10)

    if legend:
        ax.legend(loc            = 'center left',
                  bbox_to_anchor = (1, 0.5),
                  frameon        = False,
                  prop           = {'size': 12})

    plt.title(title, fontsize = 18,
                     y        = 0.9125)

    plt.ylim(1.1*np.min(offset_)/units, 1.1*y_period_.max()/units)

    ax.spines[['right', 'top', 'left', 'bottom']].set_visible(False)
    ax.grid(axis = 'y')

    if save:
        plt.savefig(file_name, bbox_inches = 'tight',
                               dpi         = 300)

    plt.show()
    
    
__all__ = ['_plot_new_and_existing_capacity',
           '_plot_emissions_intensity',
           '_plot_emissions',
           '_plot_system_cost',
           '_plot_dispatch']
