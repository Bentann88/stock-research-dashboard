# ============================================================
# PROFESSIONAL STOCK HISTORY RESEARCH DASHBOARD
# Streamlit + yfinance + Plotly
# ============================================================

import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from datetime import date, timedelta


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Stock History Research Dashboard",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# CSS — DARK PROFESSIONAL THEME + READABLE INPUTS + DARK TABLES
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background: #0B1120;
            color: #F8FAFC;
        }

        [data-testid="stSidebar"] {
            background: #111827;
            border-right: 1px solid #334155;
        }

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] h5,
        [data-testid="stSidebar"] h6 {
            color: #F8FAFC !important;
            opacity: 1 !important;
        }

        [data-testid="stSidebar"] .stCaptionContainer,
        [data-testid="stSidebar"] .stCaptionContainer p {
            color: #CBD5E1 !important;
            opacity: 1 !important;
        }

        [data-testid="stSidebar"] div[data-baseweb="input"] {
            background-color: #FFFFFF !important;
            border-radius: 8px !important;
        }

        [data-testid="stSidebar"] div[data-baseweb="input"] input,
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] input[type="number"] {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            background-color: #FFFFFF !important;
            caret-color: #000000 !important;
            font-weight: 700 !important;
        }

        [data-testid="stSidebar"] div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-radius: 8px !important;
        }

        [data-testid="stSidebar"] div[data-baseweb="select"] span {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            font-weight: 700 !important;
        }

        [data-testid="stSidebar"] div[data-baseweb="select"] svg {
            color: #000000 !important;
            fill: #000000 !important;
        }

        [data-testid="stSidebar"] .stDateInput input {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            background-color: #FFFFFF !important;
            caret-color: #000000 !important;
            font-weight: 700 !important;
        }

        [data-testid="stSidebar"] .stCheckbox label span {
            color: #F8FAFC !important;
            font-weight: 700 !important;
        }

        [data-testid="stSidebar"] .stButton button {
            background: #2563EB !important;
            color: #FFFFFF !important;
            border: 1px solid #60A5FA !important;
            font-weight: 800 !important;
            border-radius: 10px !important;
        }

        [data-testid="stSidebar"] .stButton button:hover {
            background: #1D4ED8 !important;
            color: #FFFFFF !important;
        }

        .main-title {
            font-size: 2.5rem;
            font-weight: 900;
            color: #FFFFFF;
            margin-bottom: 0.3rem;
        }

        .subtitle {
            font-size: 1.05rem;
            color: #D1D5DB;
            margin-bottom: 1.5rem;
            font-weight: 500;
        }

        .section-header {
            font-size: 1.45rem;
            font-weight: 850;
            color: #FFFFFF;
            margin-top: 1.5rem;
            margin-bottom: 0.9rem;
            border-bottom: 1px solid #334155;
            padding-bottom: 0.5rem;
        }

        .metric-card {
            background: linear-gradient(180deg, #1E293B 0%, #111827 100%);
            border: 1px solid #475569;
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: 0 8px 22px rgba(0,0,0,0.28);
            min-height: 110px;
        }

        .metric-label {
            color: #CBD5E1;
            font-size: 0.9rem;
            font-weight: 700;
            margin-bottom: 0.55rem;
        }

        .metric-value {
            font-size: 1.65rem;
            font-weight: 900;
            color: #FFFFFF;
            letter-spacing: 0.2px;
        }

        .positive {
            color: #4ADE80 !important;
        }

        .negative {
            color: #F87171 !important;
        }

        .neutral {
            color: #FFFFFF !important;
        }

        .info-card {
            background: linear-gradient(180deg, #1E293B 0%, #111827 100%);
            border: 1px solid #475569;
            border-radius: 14px;
            padding: 17px;
            box-shadow: 0 8px 22px rgba(0,0,0,0.25);
            min-height: 96px;
        }

        .info-label {
            color: #CBD5E1;
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }

        .info-value {
            color: #FFFFFF;
            font-size: 1.08rem;
            font-weight: 850;
        }

        .advisor-box {
            background: #1E293B;
            border: 1px solid #475569;
            border-left: 6px solid #60A5FA;
            border-radius: 12px;
            padding: 20px;
            color: #F8FAFC;
            font-size: 1rem;
            line-height: 1.65;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }

        .warning-box {
            background: #1E293B;
            border: 1px solid #475569;
            border-left: 6px solid #FBBF24;
            border-radius: 12px;
            padding: 20px;
            color: #F8FAFC;
            font-size: 1rem;
            line-height: 1.55;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #1E293B;
            border-radius: 10px;
            color: #F8FAFC;
            padding: 10px 18px;
            border: 1px solid #475569;
            font-weight: 700;
        }

        .stTabs [aria-selected="true"] {
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            border: 1px solid #60A5FA !important;
        }

        [data-testid="stPlotlyChart"] {
            background: #111827;
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 12px;
            box-shadow: 0 8px 22px rgba(0,0,0,0.28);
            margin-bottom: 24px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: #111827 !important;
            color: #F8FAFC !important;
            border: 1px solid #334155;
            border-radius: 14px;
            overflow: hidden;
            font-size: 0.95rem;
        }

        thead tr {
            background: #1E293B !important;
        }

        th {
            color: #CBD5E1 !important;
            font-weight: 800 !important;
            padding: 13px 15px !important;
            border-bottom: 1px solid #334155 !important;
            text-align: left !important;
            white-space: nowrap;
        }

        td {
            color: #F8FAFC !important;
            padding: 12px 15px !important;
            border-bottom: 1px solid #253044 !important;
            white-space: nowrap;
        }

        tbody tr:nth-child(even) {
            background: #0F172A !important;
        }

        tbody tr:hover {
            background: #1E293B !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONSTANTS
# ============================================================

STRESS_PERIODS = {
    "COVID Crash": ("2020-02-19", "2020-03-23"),
    "COVID Recovery": ("2020-03-24", "2021-12-31"),
    "2022 Bear Market": ("2022-01-03", "2022-10-12"),
    "Rate Hike Cycle": ("2022-03-16", "2023-12-31"),
    "Regional Banking Stress": ("2023-03-01", "2023-05-31"),
    "Tech Selloff": ("2021-11-19", "2022-12-28"),
    "Global Financial Crisis": ("2007-10-09", "2009-03-09"),
    "Dot-Com Bust": ("2000-03-24", "2002-10-09")
}

PLOT_TEMPLATE = "plotly_dark"


# ============================================================
# FORMAT HELPERS
# ============================================================

def fmt_pct(x):
    if x is None or pd.isna(x):
        return "N/A"
    return f"{x:.2%}"


def fmt_dollar(x):
    if x is None or pd.isna(x):
        return "N/A"
    return f"${x:,.2f}"


def fmt_large_number(x):
    if x is None or pd.isna(x):
        return "N/A"

    x = float(x)

    if abs(x) >= 1_000_000_000_000:
        return f"${x / 1_000_000_000_000:.2f}T"
    if abs(x) >= 1_000_000_000:
        return f"${x / 1_000_000_000:.2f}B"
    if abs(x) >= 1_000_000:
        return f"${x / 1_000_000:.2f}M"

    return f"${x:,.0f}"


def fmt_number(x):
    if x is None or pd.isna(x):
        return "N/A"
    return f"{x:,.2f}"


def fmt_volume(x):
    if x is None or pd.isna(x):
        return "N/A"
    return f"{x:,.0f}"


def return_class(x):
    if x is None or pd.isna(x):
        return "neutral"
    return "positive" if x >= 0 else "negative"


def drawdown_class(x):
    if x is None or pd.isna(x):
        return "neutral"
    return "negative" if x < 0 else "neutral"


def color_span(value, text=None, reverse=False):
    if text is None:
        text = fmt_pct(value)

    if value is None or pd.isna(value):
        color = "#FFFFFF"
    else:
        if reverse:
            color = "#4ADE80" if value >= 0 else "#F87171"
        else:
            color = "#4ADE80" if value >= 0 else "#F87171"

    return f'<span style="color:{color}; font-weight:800;">{text}</span>'


# ============================================================
# DARK TABLE HELPER
# ============================================================

def dark_table(df, title=None, height=None):
    """
    Display a pandas DataFrame as a properly formatted dark HTML table.
    Uses Streamlit components so the table does not collapse into inline text.
    """

    if df is None or df.empty:
        st.info("No table data available.")
        return

    if height is None:
        height = min(700, 120 + len(df) * 42)

    title_html = ""
    if title:
        title_html = f"""
        <div class="table-title">{title}</div>
        """

    html_table = df.to_html(index=False, escape=False)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: #0B1120;
                font-family: Arial, sans-serif;
                color: #F8FAFC;
            }}

            .table-title {{
                font-size: 20px;
                font-weight: 800;
                color: #FFFFFF;
                margin: 0 0 12px 0;
            }}

            .table-wrap {{
                background: #111827;
                border: 1px solid #334155;
                border-radius: 14px;
                overflow-x: auto;
                overflow-y: auto;
                box-shadow: 0 8px 22px rgba(0,0,0,0.25);
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: #111827;
                color: #F8FAFC;
                font-size: 14px;
                min-width: 850px;
            }}

            thead tr {{
                background: #1E293B;
            }}

            th {{
                color: #CBD5E1;
                font-weight: 800;
                padding: 12px 14px;
                border-bottom: 1px solid #334155;
                text-align: left;
                white-space: nowrap;
                position: sticky;
                top: 0;
                background: #1E293B;
                z-index: 2;
            }}

            td {{
                color: #F8FAFC;
                padding: 11px 14px;
                border-bottom: 1px solid #253044;
                text-align: left;
                white-space: nowrap;
            }}

            tbody tr:nth-child(even) {{
                background: #0F172A;
            }}

            tbody tr:hover {{
                background: #1E293B;
            }}

            span {{
                font-weight: 800;
            }}
        </style>
    </head>
    <body>
        {title_html}
        <div class="table-wrap">
            {html_table}
        </div>
    </body>
    </html>
    """

    components.html(html, height=height, scrolling=True)

# ============================================================
# DATA HELPERS
# ============================================================

def get_date_range(period_choice, custom_start, custom_end):
    today = date.today()

    if period_choice == "1 Year":
        return today - timedelta(days=365), today
    if period_choice == "3 Years":
        return today - timedelta(days=365 * 3), today
    if period_choice == "5 Years":
        return today - timedelta(days=365 * 5), today
    if period_choice == "10 Years":
        return today - timedelta(days=365 * 10), today
    if period_choice == "15 Years":
        return today - timedelta(days=365 * 15), today
    if period_choice == "20 Years":
        return today - timedelta(days=365 * 20), today
    if period_choice == "Custom":
        return custom_start, custom_end

    return None, today


@st.cache_data(show_spinner=False)
def load_price_data(ticker, start_date=None, end_date=None, period="max", initial_investment=10000):
    ticker = ticker.upper().strip()

    stock = yf.Ticker(ticker)

    if start_date is None:
        data = stock.history(period=period, auto_adjust=True)
    else:
        data = stock.history(start=start_date, end=end_date, auto_adjust=True)

    if data.empty:
        return pd.DataFrame()

    data = data.copy()
    data.index = pd.to_datetime(data.index)

    data["Daily Return"] = data["Close"].pct_change()
    data["Growth of $1"] = (1 + data["Daily Return"]).cumprod()
    data["Growth of $1"] = data["Growth of $1"].fillna(1.0)
    data["Portfolio Value"] = data["Growth of $1"] * initial_investment

    running_max = data["Portfolio Value"].cummax()
    data["Drawdown"] = data["Portfolio Value"] / running_max - 1

    return data


@st.cache_data(show_spinner=False)
def load_full_history(ticker, initial_investment=10000):
    return load_price_data(
        ticker=ticker,
        start_date=None,
        end_date=None,
        period="max",
        initial_investment=initial_investment
    )


@st.cache_data(show_spinner=False)
def load_company_info(ticker):
    ticker = ticker.upper().strip()

    try:
        info = yf.Ticker(ticker).info
        if not isinstance(info, dict):
            return {}
        return info
    except Exception:
        return {}


def calculate_metrics(data, ticker, initial_investment):
    if data.empty:
        return {}

    start_price = float(data["Close"].iloc[0])
    end_price = float(data["Close"].iloc[-1])

    total_return = (end_price / start_price) - 1

    years = (data.index[-1] - data.index[0]).days / 365.25
    cagr = (end_price / start_price) ** (1 / years) - 1 if years > 0 else np.nan

    annualized_volatility = data["Daily Return"].std() * np.sqrt(252)
    max_drawdown = data["Drawdown"].min()

    best_day = data["Daily Return"].max()
    worst_day = data["Daily Return"].min()

    positive_days = (data["Daily Return"] > 0).sum()
    negative_days = (data["Daily Return"] < 0).sum()
    total_days = positive_days + negative_days
    positive_day_pct = positive_days / total_days if total_days > 0 else np.nan

    return {
        "Ticker": ticker.upper(),
        "Start Date": data.index[0].date(),
        "End Date": data.index[-1].date(),
        "Start Price": start_price,
        "End Price": end_price,
        "Total Return": float(total_return),
        "CAGR": float(cagr),
        "Annualized Volatility": float(annualized_volatility),
        "Max Drawdown": float(max_drawdown),
        "Best Daily Return": float(best_day),
        "Worst Daily Return": float(worst_day),
        "Positive Day %": float(positive_day_pct),
        "Initial Investment": float(initial_investment),
        "Ending Value": float(data["Portfolio Value"].iloc[-1])
    }


def calculate_stress_metrics(ticker, benchmark, stress_start, stress_end, initial_investment):
    stock_data = load_price_data(
        ticker=ticker,
        start_date=stress_start,
        end_date=stress_end,
        initial_investment=initial_investment
    )

    benchmark_data = load_price_data(
        ticker=benchmark,
        start_date=stress_start,
        end_date=stress_end,
        initial_investment=initial_investment
    )

    if stock_data.empty or benchmark_data.empty:
        return None, stock_data, benchmark_data

    stock_metrics = calculate_metrics(stock_data, ticker, initial_investment)
    benchmark_metrics = calculate_metrics(benchmark_data, benchmark, initial_investment)

    stress_summary = {
        "Stock Return": stock_metrics["Total Return"],
        "Benchmark Return": benchmark_metrics["Total Return"],
        "Excess Return": stock_metrics["Total Return"] - benchmark_metrics["Total Return"],
        "Stock Max Drawdown": stock_metrics["Max Drawdown"],
        "Benchmark Max Drawdown": benchmark_metrics["Max Drawdown"],
        "Stock Ending Value": stock_metrics["Ending Value"],
        "Benchmark Ending Value": benchmark_metrics["Ending Value"]
    }

    return stress_summary, stock_data, benchmark_data


# ============================================================
# CHART HELPERS
# ============================================================

def apply_chart_layout(fig, title, yaxis_title, height=430):
    fig.update_layout(
        template=PLOT_TEMPLATE,
        title=dict(
            text=title,
            x=0.01,
            xanchor="left",
            y=0.96,
            font=dict(size=18, color="#F8FAFC", family="Arial Black")
        ),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#CBD5E1", size=12),
        height=height,
        margin=dict(l=55, r=30, t=70, b=45),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="right",
            x=1,
            font=dict(size=11, color="#CBD5E1"),
            bgcolor="rgba(17,24,39,0)"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#253044",
            zeroline=False,
            linecolor="#334155",
            tickfont=dict(color="#94A3B8", size=11),
            rangeslider=dict(visible=False)
        ),
        yaxis=dict(
            title=dict(
                text=yaxis_title,
                font=dict(color="#CBD5E1", size=12)
            ),
            showgrid=True,
            gridcolor="#253044",
            zeroline=False,
            linecolor="#334155",
            tickfont=dict(color="#94A3B8", size=11)
        )
    )

    return fig


def price_chart(data, ticker, full_history=False):
    title = f"{ticker} Full Available Price History" if full_history else f"{ticker} Adjusted Price History"

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name=ticker,
            line=dict(width=2.5, color="#38BDF8"),
            hovertemplate="Date: %{x}<br>Price: $%{y:,.2f}<extra></extra>"
        )
    )

    fig = apply_chart_layout(fig, title, "Adjusted Price", height=460)
    fig.update_yaxes(tickprefix="$")

    return fig


def growth_chart(data, ticker, initial_investment):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Portfolio Value"],
            mode="lines",
            name=ticker,
            line=dict(width=2.7, color="#22C55E"),
            hovertemplate="Date: %{x}<br>Value: $%{y:,.2f}<extra></extra>"
        )
    )

    fig = apply_chart_layout(
        fig,
        f"Growth of {fmt_dollar(initial_investment)} Invested in {ticker}",
        "Portfolio Value",
        height=460
    )
    fig.update_yaxes(tickprefix="$")

    return fig


def benchmark_growth_chart(stock_data, benchmark_data, ticker, benchmark, initial_investment):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=stock_data["Portfolio Value"],
            mode="lines",
            name=ticker,
            line=dict(width=2.8, color="#38BDF8"),
            hovertemplate=f"{ticker}: $%{{y:,.2f}}<extra></extra>"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=benchmark_data.index,
            y=benchmark_data["Portfolio Value"],
            mode="lines",
            name=benchmark,
            line=dict(width=2.8, color="#F59E0B"),
            hovertemplate=f"{benchmark}: $%{{y:,.2f}}<extra></extra>"
        )
    )

    fig = apply_chart_layout(
        fig,
        f"Growth of {fmt_dollar(initial_investment)}: {ticker} vs. {benchmark}",
        "Portfolio Value",
        height=500
    )
    fig.update_yaxes(tickprefix="$")

    return fig


def drawdown_chart(data, ticker):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Drawdown"],
            mode="lines",
            name="Drawdown",
            line=dict(width=2.2, color="#EF4444"),
            fill="tozeroy",
            fillcolor="rgba(239, 68, 68, 0.25)",
            hovertemplate="Date: %{x}<br>Drawdown: %{y:.2%}<extra></extra>"
        )
    )

    fig = apply_chart_layout(fig, f"{ticker} Drawdown Over Time", "Drawdown", height=460)
    fig.update_yaxes(tickformat=".0%")

    return fig


def rolling_return_chart(data, ticker, rolling_years):
    temp = data.copy()

    window = 252 * rolling_years
    col = f"{rolling_years}Y Rolling Return"

    temp[col] = temp["Close"] / temp["Close"].shift(window) - 1

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=temp.index,
            y=temp[col],
            mode="lines",
            name=col,
            line=dict(width=2.5, color="#A78BFA"),
            hovertemplate="Date: %{x}<br>Rolling Return: %{y:.2%}<extra></extra>"
        )
    )

    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="#6B7280")

    fig = apply_chart_layout(fig, f"{ticker} {rolling_years}-Year Rolling Returns", "Rolling Return", height=460)
    fig.update_yaxes(tickformat=".0%")

    return fig


def annual_returns_chart(data, ticker, full_history=False):
    annual_returns = data["Close"].resample("YE").last().pct_change().dropna()
    annual_returns.index = annual_returns.index.year

    colors = ["#22C55E" if x >= 0 else "#EF4444" for x in annual_returns.values]
    title = f"{ticker} Full Available Annual Returns" if full_history else f"{ticker} Calendar-Year Returns"

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=annual_returns.index.astype(str),
            y=annual_returns.values,
            marker_color=colors,
            name="Annual Return",
            hovertemplate="Year: %{x}<br>Return: %{y:.2%}<extra></extra>"
        )
    )

    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="#6B7280")

    fig = apply_chart_layout(fig, title, "Annual Return", height=520)
    fig.update_yaxes(tickformat=".0%")

    return fig, annual_returns


# ============================================================
# UI HELPERS
# ============================================================

def metric_card(label, value, css_class="neutral"):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value {css_class}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def info_card(label, value):
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-label">{label}</div>
            <div class="info-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_header(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def advisor_summary(ticker, benchmark, metrics, benchmark_metrics=None):
    total_return = metrics.get("Total Return", np.nan)
    cagr = metrics.get("CAGR", np.nan)
    max_dd = metrics.get("Max Drawdown", np.nan)
    vol = metrics.get("Annualized Volatility", np.nan)

    tone = "balanced"
    if max_dd <= -0.35 or vol >= 0.30:
        tone = "aggressive"
    elif max_dd > -0.20 and vol < 0.20:
        tone = "moderate"

    if benchmark_metrics:
        excess_cagr = cagr - benchmark_metrics.get("CAGR", np.nan)
        benchmark_text = (
            f"Relative to {benchmark}, {ticker} had an annualized return difference "
            f"of <b>{fmt_pct(excess_cagr)}</b> over the selected period."
        )
    else:
        benchmark_text = "No benchmark comparison was selected."

    summary = f"""
    <div class="advisor-box">
        <b>Advisor Summary:</b><br><br>
        Over the selected period, <b>{ticker}</b> generated a total return of
        <b>{fmt_pct(total_return)}</b> and a CAGR of <b>{fmt_pct(cagr)}</b>.
        The maximum drawdown was <b>{fmt_pct(max_dd)}</b>, with annualized volatility
        of <b>{fmt_pct(vol)}</b>. Based on the observed drawdown and volatility profile,
        this stock appears more suitable for a <b>{tone}</b> risk profile.
        <br><br>
        {benchmark_text}
    </div>
    """

    st.markdown(summary, unsafe_allow_html=True)


# ============================================================
# FULL HISTORY TABLE HELPERS
# ============================================================

def best_worst_years_table(full_data, ticker):
    annual_returns = full_data["Close"].resample("YE").last().pct_change().dropna()
    annual_returns.index = annual_returns.index.year

    worst_years = annual_returns.sort_values().head(10)
    best_years = annual_returns.sort_values(ascending=False).head(10)

    rows = []
    max_len = max(len(worst_years), len(best_years))

    for i in range(max_len):
        worst_year = worst_years.index[i] if i < len(worst_years) else ""
        worst_ret = worst_years.iloc[i] if i < len(worst_years) else np.nan

        best_year = best_years.index[i] if i < len(best_years) else ""
        best_ret = best_years.iloc[i] if i < len(best_years) else np.nan

        rows.append({
            "Worst Year": worst_year,
            "Worst Return": color_span(worst_ret),
            "Best Year": best_year,
            "Best Return": color_span(best_ret)
        })

    df = pd.DataFrame(rows)
    dark_table(df, f"{ticker} Best and Worst Calendar Years")


def rolling_period_summary_table(full_data, ticker):
    periods = {
        "1-Year": 252,
        "3-Year": 252 * 3,
        "5-Year": 252 * 5,
        "10-Year": 252 * 10
    }

    rows = []

    for label, window in periods.items():
        temp = full_data.copy()
        temp[f"{label} Rolling Return"] = temp["Close"] / temp["Close"].shift(window) - 1

        rolling_series = temp[f"{label} Rolling Return"].dropna()

        if rolling_series.empty:
            rows.append({
                "Rolling Period": label,
                "Best Return": "N/A",
                "Worst Return": "N/A",
                "Average Return": "N/A"
            })
        else:
            best_value = rolling_series.max()
            worst_value = rolling_series.min()
            avg_value = rolling_series.mean()

            rows.append({
                "Rolling Period": label,
                "Best Return": color_span(best_value),
                "Worst Return": color_span(worst_value),
                "Average Return": color_span(avg_value)
            })

    df = pd.DataFrame(rows)
    dark_table(df, f"{ticker} Historical Rolling Return Summary")


# ============================================================
# SIDEBAR INPUTS
# ============================================================

st.sidebar.markdown("## 📊 Research Inputs")

ticker = st.sidebar.text_input("Stock Ticker", value="AAPL").upper().strip()
benchmark = st.sidebar.text_input("Benchmark Ticker", value="SPY").upper().strip()

period_choice = st.sidebar.selectbox(
    "Time Period",
    [
        "1 Year",
        "3 Years",
        "5 Years",
        "10 Years",
        "15 Years",
        "20 Years",
        "Max Available",
        "Custom"
    ],
    index=6
)

today = date.today()

if period_choice == "Custom":
    custom_start = st.sidebar.date_input("Custom Start Date", value=today - timedelta(days=365 * 10))
    custom_end = st.sidebar.date_input("Custom End Date", value=today)
else:
    custom_start = today - timedelta(days=365 * 10)
    custom_end = today

initial_investment = st.sidebar.number_input(
    "Initial Investment",
    min_value=100.0,
    max_value=100_000_000.0,
    value=10_000.0,
    step=500.0
)

rolling_years = st.sidebar.selectbox(
    "Rolling Return Period",
    [1, 3, 5, 10],
    index=1
)

show_benchmark = st.sidebar.checkbox("Compare to Benchmark", value=True)

stress_period_name = st.sidebar.selectbox(
    "Stress Period Preset",
    list(STRESS_PERIODS.keys()),
    index=2
)

st.sidebar.button("Run Analysis", type="primary", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("Data source: Yahoo Finance via yfinance. Verify externally for client-facing use.")


# ============================================================
# MAIN APP HEADER
# ============================================================

st.markdown('<div class="main-title">📈 Stock History Research Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Advisor-facing stock research with performance, risk, stress-period testing, full-history context, and benchmark comparison.</div>',
    unsafe_allow_html=True
)


# ============================================================
# LOAD SELECTED PERIOD DATA
# ============================================================

start_date, end_date = get_date_range(period_choice, custom_start, custom_end)

if not ticker:
    st.warning("Enter a stock ticker to begin.")
    st.stop()

with st.spinner("Loading market data and company context..."):
    if start_date is None:
        stock_data = load_price_data(ticker, period="max", initial_investment=initial_investment)
    else:
        stock_data = load_price_data(
            ticker,
            start_date=start_date,
            end_date=end_date,
            initial_investment=initial_investment
        )

    company_info = load_company_info(ticker)

if stock_data.empty:
    st.error("No data found. Check the ticker symbol or selected date range.")
    st.stop()

metrics = calculate_metrics(stock_data, ticker, initial_investment)

benchmark_data = pd.DataFrame()
benchmark_metrics = None

if show_benchmark and benchmark:
    with st.spinner("Loading benchmark data..."):
        if start_date is None:
            benchmark_data = load_price_data(benchmark, period="max", initial_investment=initial_investment)
        else:
            benchmark_data = load_price_data(
                benchmark,
                start_date=start_date,
                end_date=end_date,
                initial_investment=initial_investment
            )

    if not benchmark_data.empty:
        benchmark_metrics = calculate_metrics(benchmark_data, benchmark, initial_investment)


# ============================================================
# TOP STRIP
# ============================================================

top_cols = st.columns(5)

with top_cols[0]:
    info_card("Ticker", ticker)

with top_cols[1]:
    info_card("Benchmark", benchmark if show_benchmark else "None")

with top_cols[2]:
    info_card("Period", period_choice)

with top_cols[3]:
    info_card("Start Date", str(metrics["Start Date"]))

with top_cols[4]:
    info_card("End Date", str(metrics["End Date"]))


# ============================================================
# TABS
# ============================================================

tab_overview, tab_risk, tab_benchmark, tab_stress, tab_full_history, tab_tables = st.tabs(
    [
        "Overview",
        "Risk",
        "Benchmark Comparison",
        "Stress Periods",
        "Full History",
        "Historical Tables"
    ]
)


# ============================================================
# OVERVIEW TAB
# ============================================================

with tab_overview:
    section_header("Company & Sector Context")

    company_name = company_info.get("longName", company_info.get("shortName", ticker))
    sector = company_info.get("sector", "N/A")
    industry = company_info.get("industry", "N/A")
    market_cap = company_info.get("marketCap", np.nan)
    beta = company_info.get("beta", np.nan)
    dividend_yield = company_info.get("dividendYield", np.nan)
    forward_pe = company_info.get("forwardPE", np.nan)
    trailing_pe = company_info.get("trailingPE", np.nan)
    fifty_two_high = company_info.get("fiftyTwoWeekHigh", np.nan)
    fifty_two_low = company_info.get("fiftyTwoWeekLow", np.nan)
    country = company_info.get("country", "N/A")
    exchange = company_info.get("exchange", "N/A")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        info_card("Company", company_name)
    with c2:
        info_card("Sector", sector)
    with c3:
        info_card("Industry", industry)
    with c4:
        info_card("Market Cap", fmt_large_number(market_cap))

    c5, c6, c7, c8 = st.columns(4)

    with c5:
        info_card("Beta", fmt_number(beta))
    with c6:
        info_card("Dividend Yield", fmt_pct(dividend_yield) if not pd.isna(dividend_yield) else "N/A")
    with c7:
        info_card("Forward P/E", fmt_number(forward_pe))
    with c8:
        info_card("Trailing P/E", fmt_number(trailing_pe))

    c9, c10, c11, c12 = st.columns(4)

    with c9:
        info_card("52W High", fmt_dollar(fifty_two_high))
    with c10:
        info_card("52W Low", fmt_dollar(fifty_two_low))
    with c11:
        info_card("Country", country)
    with c12:
        info_card("Exchange", exchange)

    section_header("Performance Summary")

    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        metric_card("Total Return", fmt_pct(metrics["Total Return"]), return_class(metrics["Total Return"]))
    with m2:
        metric_card("CAGR", fmt_pct(metrics["CAGR"]), return_class(metrics["CAGR"]))
    with m3:
        metric_card("Ending Value", fmt_dollar(metrics["Ending Value"]), return_class(metrics["Ending Value"]))
    with m4:
        metric_card("Max Drawdown", fmt_pct(metrics["Max Drawdown"]), drawdown_class(metrics["Max Drawdown"]))
    with m5:
        metric_card("Volatility", fmt_pct(metrics["Annualized Volatility"]), "neutral")

    m6, m7, m8, m9, m10 = st.columns(5)

    with m6:
        metric_card("Start Price", fmt_dollar(metrics["Start Price"]), "neutral")
    with m7:
        metric_card("End Price", fmt_dollar(metrics["End Price"]), "neutral")
    with m8:
        metric_card("Best Day", fmt_pct(metrics["Best Daily Return"]), return_class(metrics["Best Daily Return"]))
    with m9:
        metric_card("Worst Day", fmt_pct(metrics["Worst Daily Return"]), return_class(metrics["Worst Daily Return"]))
    with m10:
        metric_card("Positive Days", fmt_pct(metrics["Positive Day %"]), "neutral")

    advisor_summary(ticker, benchmark, metrics, benchmark_metrics)

    section_header("Price & Growth Visuals")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.plotly_chart(
            price_chart(stock_data, ticker),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with chart_col2:
        st.plotly_chart(
            growth_chart(stock_data, ticker, initial_investment),
            use_container_width=True,
            config={"displayModeBar": False}
        )


# ============================================================
# RISK TAB
# ============================================================

with tab_risk:
    section_header("Risk Dashboard")

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        metric_card("Max Drawdown", fmt_pct(metrics["Max Drawdown"]), "negative")
    with r2:
        metric_card("Annualized Volatility", fmt_pct(metrics["Annualized Volatility"]), "neutral")
    with r3:
        metric_card("Worst Daily Return", fmt_pct(metrics["Worst Daily Return"]), "negative")
    with r4:
        metric_card("Best Daily Return", fmt_pct(metrics["Best Daily Return"]), "positive")

    c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(
            drawdown_chart(stock_data, ticker),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with c2:
        st.plotly_chart(
            rolling_return_chart(stock_data, ticker, rolling_years),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    section_header("Calendar-Year Returns")

    annual_fig, annual_returns = annual_returns_chart(stock_data, ticker)
    st.plotly_chart(
        annual_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# ============================================================
# BENCHMARK TAB
# ============================================================

with tab_benchmark:
    section_header("Benchmark Comparison")

    if show_benchmark and benchmark_metrics is not None:
        excess_return = metrics["Total Return"] - benchmark_metrics["Total Return"]
        excess_cagr = metrics["CAGR"] - benchmark_metrics["CAGR"]
        vol_diff = metrics["Annualized Volatility"] - benchmark_metrics["Annualized Volatility"]
        dd_diff = metrics["Max Drawdown"] - benchmark_metrics["Max Drawdown"]

        b1, b2, b3, b4 = st.columns(4)

        with b1:
            metric_card("Excess Total Return", fmt_pct(excess_return), return_class(excess_return))
        with b2:
            metric_card("Excess CAGR", fmt_pct(excess_cagr), return_class(excess_cagr))
        with b3:
            metric_card("Volatility Difference", fmt_pct(vol_diff), return_class(-vol_diff))
        with b4:
            metric_card("Drawdown Difference", fmt_pct(dd_diff), return_class(-dd_diff))

        st.plotly_chart(
            benchmark_growth_chart(stock_data, benchmark_data, ticker, benchmark, initial_investment),
            use_container_width=True,
            config={"displayModeBar": False}
        )

        comparison_df = pd.DataFrame(
            {
                "Metric": [
                    "Total Return",
                    "CAGR",
                    "Annualized Volatility",
                    "Max Drawdown",
                    "Ending Value"
                ],
                ticker: [
                    color_span(metrics["Total Return"]),
                    color_span(metrics["CAGR"]),
                    fmt_pct(metrics["Annualized Volatility"]),
                    color_span(metrics["Max Drawdown"]),
                    fmt_dollar(metrics["Ending Value"])
                ],
                benchmark: [
                    color_span(benchmark_metrics["Total Return"]),
                    color_span(benchmark_metrics["CAGR"]),
                    fmt_pct(benchmark_metrics["Annualized Volatility"]),
                    color_span(benchmark_metrics["Max Drawdown"]),
                    fmt_dollar(benchmark_metrics["Ending Value"])
                ]
            }
        )

        dark_table(comparison_df, "Benchmark Comparison Table")

    else:
        st.info("Turn on benchmark comparison in the sidebar to view this section.")


# ============================================================
# STRESS PERIOD TAB
# ============================================================

with tab_stress:
    section_header("Historical Stress Period Analysis")

    stress_start, stress_end = STRESS_PERIODS[stress_period_name]

    st.markdown(
        f"""
        <div class="warning-box">
            <b>Selected Stress Period:</b> {stress_period_name}<br>
            <b>Window:</b> {stress_start} to {stress_end}
        </div>
        """,
        unsafe_allow_html=True
    )

    if show_benchmark and benchmark:
        stress_summary, stress_stock_data, stress_benchmark_data = calculate_stress_metrics(
            ticker=ticker,
            benchmark=benchmark,
            stress_start=stress_start,
            stress_end=stress_end,
            initial_investment=initial_investment
        )

        if stress_summary is None:
            st.warning("Stress-period data was not available for one or both tickers.")
        else:
            s1, s2, s3, s4 = st.columns(4)

            with s1:
                metric_card("Stock Return", fmt_pct(stress_summary["Stock Return"]), return_class(stress_summary["Stock Return"]))
            with s2:
                metric_card("Benchmark Return", fmt_pct(stress_summary["Benchmark Return"]), return_class(stress_summary["Benchmark Return"]))
            with s3:
                metric_card("Excess Return", fmt_pct(stress_summary["Excess Return"]), return_class(stress_summary["Excess Return"]))
            with s4:
                metric_card("Stock Max Drawdown", fmt_pct(stress_summary["Stock Max Drawdown"]), "negative")

            st.plotly_chart(
                benchmark_growth_chart(
                    stress_stock_data,
                    stress_benchmark_data,
                    ticker,
                    benchmark,
                    initial_investment
                ),
                use_container_width=True,
                config={"displayModeBar": False}
            )

            stress_df = pd.DataFrame(
                {
                    "Metric": [
                        "Stock Return",
                        "Benchmark Return",
                        "Excess Return",
                        "Stock Max Drawdown",
                        "Benchmark Max Drawdown",
                        "Stock Ending Value",
                        "Benchmark Ending Value"
                    ],
                    "Value": [
                        color_span(stress_summary["Stock Return"]),
                        color_span(stress_summary["Benchmark Return"]),
                        color_span(stress_summary["Excess Return"]),
                        color_span(stress_summary["Stock Max Drawdown"]),
                        color_span(stress_summary["Benchmark Max Drawdown"]),
                        fmt_dollar(stress_summary["Stock Ending Value"]),
                        fmt_dollar(stress_summary["Benchmark Ending Value"])
                    ]
                }
            )

            dark_table(stress_df, "Stress Period Summary")

    else:
        stress_stock_data = load_price_data(
            ticker=ticker,
            start_date=stress_start,
            end_date=stress_end,
            initial_investment=initial_investment
        )

        if stress_stock_data.empty:
            st.warning("Stress-period data was not available for this ticker.")
        else:
            stress_metrics = calculate_metrics(stress_stock_data, ticker, initial_investment)

            s1, s2, s3 = st.columns(3)

            with s1:
                metric_card("Stress Return", fmt_pct(stress_metrics["Total Return"]), return_class(stress_metrics["Total Return"]))
            with s2:
                metric_card("Stress Max Drawdown", fmt_pct(stress_metrics["Max Drawdown"]), "negative")
            with s3:
                metric_card("Stress Ending Value", fmt_dollar(stress_metrics["Ending Value"]), "neutral")

            st.plotly_chart(
                growth_chart(stress_stock_data, ticker, initial_investment),
                use_container_width=True,
                config={"displayModeBar": False}
            )


# ============================================================
# FULL HISTORY TAB
# ============================================================

with tab_full_history:
    section_header("Full Available History")

    full_data = load_full_history(ticker, initial_investment)

    if full_data.empty:
        st.warning("Full history was not available for this ticker.")
    else:
        full_metrics = calculate_metrics(full_data, ticker, initial_investment)

        fh1, fh2, fh3, fh4, fh5 = st.columns(5)

        with fh1:
            metric_card("Full-History Start", str(full_metrics["Start Date"]), "neutral")
        with fh2:
            metric_card("Full-History Return", fmt_pct(full_metrics["Total Return"]), return_class(full_metrics["Total Return"]))
        with fh3:
            metric_card("Full-History CAGR", fmt_pct(full_metrics["CAGR"]), return_class(full_metrics["CAGR"]))
        with fh4:
            metric_card("Worst Drawdown", fmt_pct(full_metrics["Max Drawdown"]), "negative")
        with fh5:
            metric_card("Ending Value", fmt_dollar(full_metrics["Ending Value"]), "positive")

        st.markdown(
            f"""
            <div class="advisor-box">
                <b>Advisor Note:</b><br>
                This section uses the full available history for <b>{ticker}</b>, not just the selected time period.
                This is useful when showing clients that performance has varied across market cycles.
                Even strong long-term stocks can have weak calendar years, deep drawdowns, and poor rolling-return periods.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.plotly_chart(
            price_chart(full_data, ticker, full_history=True),
            use_container_width=True,
            config={"displayModeBar": False}
        )

        full_annual_fig, full_annual_returns = annual_returns_chart(full_data, ticker, full_history=True)

        st.plotly_chart(
            full_annual_fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        best_worst_years_table(full_data, ticker)
        rolling_period_summary_table(full_data, ticker)

        full_annual_table = pd.DataFrame(
            {
                "Year": full_annual_returns.index,
                "Annual Return": [
                    color_span(x) for x in full_annual_returns.values
                ]
            }
        )

        dark_table(full_annual_table, f"{ticker} Full Annual Return History")


# ============================================================
# HISTORICAL TABLES TAB
# ============================================================

with tab_tables:
    section_header("Annual Returns Table")

    _, annual_returns = annual_returns_chart(stock_data, ticker)

    annual_table = pd.DataFrame(
        {
            "Year": annual_returns.index,
            "Annual Return": [
                color_span(x) for x in annual_returns.values
            ]
        }
    )

    dark_table(annual_table, "Selected-Period Annual Returns")

    section_header("Most Recent Data")

    recent = stock_data.tail(20).copy()

    recent_table = pd.DataFrame(
        {
            "Date": [x.date() for x in recent.index],
            "Open": [fmt_dollar(x) for x in recent["Open"]],
            "High": [fmt_dollar(x) for x in recent["High"]],
            "Low": [fmt_dollar(x) for x in recent["Low"]],
            "Close": [fmt_dollar(x) for x in recent["Close"]],
            "Volume": [fmt_volume(x) for x in recent["Volume"]],
            "Daily Return": [color_span(x) for x in recent["Daily Return"]],
            "Portfolio Value": [fmt_dollar(x) for x in recent["Portfolio Value"]],
            "Drawdown": [color_span(x) for x in recent["Drawdown"]]
        }
    )

    dark_table(recent_table, "Most Recent Data")

    csv_download = stock_data.to_csv().encode("utf-8")

    st.download_button(
        label="Download Historical Data as CSV",
        data=csv_download,
        file_name=f"{ticker}_historical_data.csv",
        mime="text/csv",
        use_container_width=True
    )


# ============================================================
# DISCLAIMER
# ============================================================

st.markdown(
    """
    <div class="advisor-box">
        <b>Disclaimer:</b><br>
        Data is sourced from Yahoo Finance via the yfinance library and may be delayed, incomplete, or inaccurate.
        For client-facing presentations or investment recommendations, verify figures against an official market data source,
        custodian platform, Morningstar, Bloomberg, FactSet, YCharts, or another approved source.
        Past performance does not guarantee future results. This tool is for research and educational purposes only.
    </div>
    """,
    unsafe_allow_html=True
)
