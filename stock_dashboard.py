# ============================================================
# PROFESSIONAL STOCK HISTORY RESEARCH DASHBOARD
# STREAMLIT VERSION
# ============================================================

import streamlit as st
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
# DARK PROFESSIONAL CSS
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

        [data-testid="stSidebar"] * {
            color: #F8FAFC !important;
        }

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {
            color: #E5E7EB !important;
            opacity: 1 !important;
        }

        input, textarea, select {
            color: #111827 !important;
            background-color: #FFFFFF !important;
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

        div[data-testid="stMetric"] {
            background: #1E293B;
            border: 1px solid #475569;
            padding: 16px;
            border-radius: 14px;
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

        table {
            color: #F8FAFC !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #475569;
            border-radius: 12px;
        }

        .stButton > button {
            background: #2563EB !important;
            color: #FFFFFF !important;
            border: 1px solid #60A5FA !important;
            font-weight: 800 !important;
            border-radius: 10px !important;
        }

        .stButton > button:hover {
            background: #1D4ED8 !important;
            color: #FFFFFF !important;
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


def return_class(x):
    if x is None or pd.isna(x):
        return "neutral"
    return "positive" if x >= 0 else "negative"


def drawdown_class(x):
    if x is None or pd.isna(x):
        return "neutral"
    return "negative" if x < 0 else "neutral"


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

def apply_chart_layout(fig, title, yaxis_title):
    fig.update_layout(
        template=PLOT_TEMPLATE,
        title=dict(
            text=title,
            x=0.02,
            xanchor="left",
            font=dict(size=20, color="#F9FAFB")
        ),
        paper_bgcolor="#0B1120",
        plot_bgcolor="#111827",
        font=dict(color="#D1D5DB"),
        margin=dict(l=40, r=30, t=65, b=40),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#1F2937",
            zeroline=False
        ),
        yaxis=dict(
            title=yaxis_title,
            showgrid=True,
            gridcolor="#1F2937",
            zeroline=False
        )
    )

    return fig


def price_chart(data, ticker):
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

    fig = apply_chart_layout(fig, f"{ticker} Adjusted Price History", "Adjusted Price")
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
        "Portfolio Value"
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
        "Portfolio Value"
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

    fig = apply_chart_layout(fig, f"{ticker} Drawdown Over Time", "Drawdown")
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

    fig = apply_chart_layout(fig, f"{ticker} {rolling_years}-Year Rolling Returns", "Rolling Return")
    fig.update_yaxes(tickformat=".0%")

    return fig


def annual_returns_chart(data, ticker):
    annual_returns = data["Close"].resample("YE").last().pct_change().dropna()
    annual_returns.index = annual_returns.index.year

    colors = ["#22C55E" if x >= 0 else "#EF4444" for x in annual_returns.values]

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

    fig = apply_chart_layout(fig, f"{ticker} Calendar-Year Returns", "Annual Return")
    fig.update_yaxes(tickformat=".0%")

    return fig, annual_returns


# ============================================================
# UI CARD HELPERS
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
            f"of {fmt_pct(excess_cagr)} over the selected period."
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
    index=3
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

run_button = st.sidebar.button("Run Analysis", type="primary", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("Data source: Yahoo Finance via yfinance. Verify externally for client-facing use.")


# ============================================================
# MAIN APP
# ============================================================

st.markdown('<div class="main-title">📈 Stock History Research Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Advisor-facing stock research with performance, risk, stress-period testing, sector context, and benchmark comparison.</div>',
    unsafe_allow_html=True
)

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
# TOP OVERVIEW STRIP
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

tab_overview, tab_risk, tab_benchmark, tab_stress, tab_tables = st.tabs(
    [
        "Overview",
        "Risk",
        "Benchmark Comparison",
        "Stress Periods",
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
        st.plotly_chart(price_chart(stock_data, ticker), use_container_width=True)

    with chart_col2:
        st.plotly_chart(growth_chart(stock_data, ticker, initial_investment), use_container_width=True)


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
        st.plotly_chart(drawdown_chart(stock_data, ticker), use_container_width=True)

    with c2:
        st.plotly_chart(rolling_return_chart(stock_data, ticker, rolling_years), use_container_width=True)

    section_header("Calendar-Year Returns")

    annual_fig, annual_returns = annual_returns_chart(stock_data, ticker)
    st.plotly_chart(annual_fig, use_container_width=True)


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
            use_container_width=True
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
                    fmt_pct(metrics["Total Return"]),
                    fmt_pct(metrics["CAGR"]),
                    fmt_pct(metrics["Annualized Volatility"]),
                    fmt_pct(metrics["Max Drawdown"]),
                    fmt_dollar(metrics["Ending Value"])
                ],
                benchmark: [
                    fmt_pct(benchmark_metrics["Total Return"]),
                    fmt_pct(benchmark_metrics["CAGR"]),
                    fmt_pct(benchmark_metrics["Annualized Volatility"]),
                    fmt_pct(benchmark_metrics["Max Drawdown"]),
                    fmt_dollar(benchmark_metrics["Ending Value"])
                ]
            }
        )

        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

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
                use_container_width=True
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
                        fmt_pct(stress_summary["Stock Return"]),
                        fmt_pct(stress_summary["Benchmark Return"]),
                        fmt_pct(stress_summary["Excess Return"]),
                        fmt_pct(stress_summary["Stock Max Drawdown"]),
                        fmt_pct(stress_summary["Benchmark Max Drawdown"]),
                        fmt_dollar(stress_summary["Stock Ending Value"]),
                        fmt_dollar(stress_summary["Benchmark Ending Value"])
                    ]
                }
            )

            st.dataframe(stress_df, use_container_width=True, hide_index=True)

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

            st.plotly_chart(growth_chart(stress_stock_data, ticker, initial_investment), use_container_width=True)


# ============================================================
# TABLES TAB
# ============================================================

with tab_tables:
    section_header("Annual Returns Table")

    _, annual_returns = annual_returns_chart(stock_data, ticker)

    annual_table = pd.DataFrame(
        {
            "Year": annual_returns.index,
            "Annual Return": [fmt_pct(x) for x in annual_returns.values]
        }
    )

    st.dataframe(annual_table, use_container_width=True, hide_index=True)

    section_header("Most Recent Data")

    recent = stock_data.tail(20).copy()

    recent_table = pd.DataFrame(
        {
            "Date": [x.date() for x in recent.index],
            "Open": [fmt_dollar(x) for x in recent["Open"]],
            "High": [fmt_dollar(x) for x in recent["High"]],
            "Low": [fmt_dollar(x) for x in recent["Low"]],
            "Close": [fmt_dollar(x) for x in recent["Close"]],
            "Volume": [f"{x:,.0f}" for x in recent["Volume"]],
            "Daily Return": [fmt_pct(x) for x in recent["Daily Return"]],
            "Portfolio Value": [fmt_dollar(x) for x in recent["Portfolio Value"]],
            "Drawdown": [fmt_pct(x) for x in recent["Drawdown"]]
        }
    )

    st.dataframe(recent_table, use_container_width=True, hide_index=True)

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
