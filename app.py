import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# Page config
# ---------------------------------------------------------
st.set_page_config(
    page_title="Movie Revenue Analysis Dashboard",
    page_icon="🎬",
    layout="wide",
)

# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("movies_cleaned.csv")
    df["genre"] = df["genre"].fillna("Unknown")
    return df

df = load_data()

# ---------------------------------------------------------
# Title
# ---------------------------------------------------------
st.title("🎬 Movie Revenue Analysis Dashboard")
st.markdown(
    "Explore movie performance across genres, budgets, ratings and revenue "
    "to uncover what drives box office success."
)

# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------
st.sidebar.header("🔎 Filters")

genres = sorted(df["genre"].unique().tolist())
selected_genres = st.sidebar.multiselect(
    "Genre", options=genres, default=genres
)

budget_min, budget_max = int(df["budget"].min()), int(df["budget"].max())
selected_budget = st.sidebar.slider(
    "Budget Range ($)",
    min_value=budget_min,
    max_value=budget_max,
    value=(budget_min, budget_max),
    step=100_000,
    format="$%d",
)

rating_min, rating_max = float(df["vote_average"].min()), float(df["vote_average"].max())
selected_rating = st.sidebar.slider(
    "Rating Range",
    min_value=round(rating_min, 1),
    max_value=round(rating_max, 1),
    value=(round(rating_min, 1), round(rating_max, 1)),
    step=0.1,
)

# Apply filters
filtered_df = df[
    (df["genre"].isin(selected_genres))
    & (df["budget"].between(selected_budget[0], selected_budget[1]))
    & (df["vote_average"].between(selected_rating[0], selected_rating[1]))
]

st.sidebar.markdown(f"**{len(filtered_df):,}** movies match your filters")

if filtered_df.empty:
    st.warning("No movies match the selected filters. Please adjust your filter criteria.")
    st.stop()

# ---------------------------------------------------------
# Dataset preview
# ---------------------------------------------------------
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df, use_container_width=True, height=250)

# ---------------------------------------------------------
# KPI Cards
# ---------------------------------------------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Movies", f"{len(filtered_df):,}")
col2.metric("Average Revenue", f"${filtered_df['revenue'].mean():,.0f}")
col3.metric("Average Budget", f"${filtered_df['budget'].mean():,.0f}")
col4.metric("Average Rating", f"{filtered_df['vote_average'].mean():.2f} / 10")

st.markdown("---")

# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------
st.subheader("📈 Interactive Charts")

# Row 1: Top 10 Revenue Movies & Revenue by Genre
c1, c2 = st.columns(2)

with c1:
    st.markdown("**Top 10 Revenue Movies**")
    top10 = filtered_df.nlargest(10, "revenue").sort_values("revenue")
    fig = px.bar(
        top10,
        x="revenue",
        y="title",
        orientation="h",
        color="genre",
        labels={"revenue": "Revenue ($)", "title": "Movie"},
    )
    fig.update_layout(showlegend=True, height=450)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("**Revenue by Genre**")
    genre_rev = (
        filtered_df.groupby("genre")["revenue"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig = px.bar(
        genre_rev,
        x="genre",
        y="revenue",
        color="genre",
        labels={"revenue": "Average Revenue ($)", "genre": "Genre"},
    )
    fig.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig, use_container_width=True)

# Row 2: Budget vs Revenue & Popularity vs Revenue
c3, c4 = st.columns(2)

with c3:
    st.markdown("**Budget vs Revenue**")
    fig = px.scatter(
        filtered_df,
        x="budget",
        y="revenue",
        color="genre",
        hover_data=["title"],
        labels={"budget": "Budget ($)", "revenue": "Revenue ($)"},
        trendline="ols",
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.markdown("**Popularity vs Revenue**")
    fig = px.scatter(
        filtered_df,
        x="popularity",
        y="revenue",
        color="genre",
        hover_data=["title"],
        labels={"popularity": "Popularity", "revenue": "Revenue ($)"},
        trendline="ols",
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

# Row 3: Runtime Distribution & Rating Distribution
c5, c6 = st.columns(2)

with c5:
    st.markdown("**Runtime Distribution**")
    fig = px.histogram(
        filtered_df,
        x="runtime",
        nbins=30,
        labels={"runtime": "Runtime (minutes)"},
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

with c6:
    st.markdown("**Rating Distribution**")
    fig = px.histogram(
        filtered_df,
        x="vote_average",
        nbins=30,
        labels={"vote_average": "Rating"},
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# Business Insights
# ---------------------------------------------------------
st.subheader("💡 Business Insights")

# Compute dynamic insight values
top_genre_by_revenue = genre_rev.iloc[0]["genre"]
top_genre_revenue_val = genre_rev.iloc[0]["revenue"]

corr_budget_rev = filtered_df["budget"].corr(filtered_df["revenue"])
corr_pop_rev = filtered_df["popularity"].corr(filtered_df["revenue"])

profitable = filtered_df[filtered_df["profit"] > 0]
pct_profitable = len(profitable) / len(filtered_df) * 100

avg_runtime = filtered_df["runtime"].mean()
high_rated = filtered_df[filtered_df["vote_average"] >= 7]
avg_revenue_high_rated = high_rated["revenue"].mean() if not high_rated.empty else 0
avg_revenue_overall = filtered_df["revenue"].mean()

st.markdown(f"""
- **{top_genre_by_revenue}** is the top-performing genre by average revenue, generating an average of **${top_genre_revenue_val:,.0f}** per movie.
- Budget and revenue show a correlation of **{corr_budget_rev:.2f}**, indicating that {"higher budgets tend to be associated with higher revenue" if corr_budget_rev > 0.3 else "budget alone is not a strong predictor of revenue"}.
- Popularity and revenue show a correlation of **{corr_pop_rev:.2f}**, suggesting {"popularity is a strong driver of box office performance" if corr_pop_rev > 0.3 else "popularity has only a weak relationship with revenue"}.
- **{pct_profitable:.1f}%** of the filtered movies are profitable (revenue exceeds budget).
- The average runtime across filtered movies is **{avg_runtime:.0f} minutes**.
- Highly rated movies (rating ≥ 7) earn an average revenue of **${avg_revenue_high_rated:,.0f}**, compared to the overall average of **${avg_revenue_overall:,.0f}**.
""")

st.markdown("---")

# ---------------------------------------------------------
# Business Recommendations
# ---------------------------------------------------------
st.subheader("🚀 Business Recommendations")

st.markdown(f"""
1. **Prioritize investment in {top_genre_by_revenue}** and other high-revenue genres identified above, while continuing to monitor emerging genres for shifting audience preferences.
2. **{"Increase budgets selectively" if corr_budget_rev > 0.3 else "Avoid assuming bigger budgets guarantee returns"}** — since the budget-revenue correlation is {corr_budget_rev:.2f}, allocate spend based on genre and concept strength rather than budget size alone.
3. **Invest in marketing and audience engagement to boost popularity**, since popularity {"correlates strongly" if corr_pop_rev > 0.3 else "shows a modest correlation"} with revenue — pre-release buzz and trailers can meaningfully impact box office results.
4. **Focus on quality and audience satisfaction** — movies rated 7+ significantly outperform the average in revenue, so investing in strong scripts, casting, and production values pays off.
5. **Diversify the portfolio** across profitable genres and budget tiers to balance risk, since only {pct_profitable:.1f}% of movies in the current selection are profitable.
6. **Target an optimal runtime** close to the dataset average (~{avg_runtime:.0f} minutes) to align with audience attention spans and viewing habits.
""")
