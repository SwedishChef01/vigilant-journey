import plotly.graph_objects as go

def cum_profit(tidm, strategy, timeframe, position_size, trade_list):
    """Plot of Cumulative Profit vs Date."""

    # Create plot trace.
    trace = go.Scatter(
        x=trade_list.index,
        y=trade_list.cum_profit,
        line=dict(color='rgba(92, 230, 174, 1.0)', width=1.0),
        yhoverformat=".0f",
    )

    # Create figure and add trace.
    fig = go.Figure(trace)

    # Customise plot.
    fig.update_layout(
        autosize=True,
        showlegend=False,
        paper_bgcolor='rgba(28, 28, 28, 1.0)',
        plot_bgcolor='rgba(28, 28, 28, 1.0)',
        font=dict(color='rgba(226, 226, 226, 1.0)'),
        title=dict(
            text=f'TIDM: {tidm}'
            + f'<br>{strategy} {timeframe}'
            + f'<br>Position Size = '
            + '{:,}'.format(position_size),
            font_color='rgba(226, 226, 226, 1.0)',
            font_size=14,
        ),
        xaxis=dict(rangeslider=dict(visible=False)),
        hovermode='x unified',
        hoverlabel=dict(bgcolor='rgba(28, 28, 28, 0.5)'),
        dragmode='pan',
    )

    fig.update_xaxes(
        linecolor='rgba(226, 226, 226, 1.0)',
        gridcolor='rgba(119, 119, 119, 0.5)',
        mirror=True,
    )

    fig.update_yaxes(
        linecolor='rgba(226, 226, 226, 1.0)',
        gridcolor='rgba(119, 119, 119, 0.5)',
        mirror=True,
        side='right',
        title=f'Cumulative Profit',
    )

    # Display plot.
    fig.show(
        config={
            'scrollZoom': True,
            'modeBarButtonsToRemove': ['zoom', 'select2d', 'lasso2d'],
        }
    )
    return