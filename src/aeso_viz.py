import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go



def total_gen_all_fuel(aeso_clean):
    generation_cols = [col for col in aeso_clean.columns if 'total_generation__' in col]
    yearly_generation = aeso_clean.groupby('year')[generation_cols + ['total_gen_all']].sum().reset_index()
    plot_df = yearly_generation.set_index('year').drop(columns=['total_gen_all'])
    plot_df.columns = [col.replace('total_generation__', '') for col in plot_df.columns]

    fig = go.Figure()
    for col in plot_df.columns:
        fig.add_trace(go.Bar(x=plot_df.index, y=plot_df[col], name=col))

    fig.update_layout(
        barmode='stack',
        title='Total Generation by Fuel Type Over Years',
        xaxis_title='Year',
        yaxis_title='Total Generation (MWh)',
        legend_title='Fuel Type',
        xaxis=dict(tickmode='linear'),
        hovermode='x unified'
    )
    return fig


def market_share(aeso_clean):
    monthly_mark = (
        aeso_clean.groupby(['year', 'month'], as_index=False)
        .agg({
            'total_generation__solar': 'sum',
            'total_gen_all': 'sum'
        })
    )

    monthly_mark['time'] = pd.to_datetime(monthly_mark[['year', 'month']].assign(day=1))
    monthly_mark = monthly_mark.sort_values('time').reset_index(drop=True)
    monthly_mark['solar_market_share'] = (
        monthly_mark['total_generation__solar'] / monthly_mark['total_gen_all']
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_mark['time'], monthly_mark['solar_market_share'])
    ax.set_title('Monthly Alberta Solar Market Share')
    ax.set_xlabel('Time')
    ax.set_ylabel('Solar Market Share')
    ax.grid(True, alpha=0.3)
    return fig


def total_gen_box(aeso_clean):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='hour', y='total_gen_all', data=aeso_clean, ax=ax)
    ax.set_title('Distribution of Total Generation (MWh) by Hour')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Total Generation (MWh)')
    ax.grid(True, alpha=0.3)
    return fig


# add other aeso graphs below