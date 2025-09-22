# app.py
import streamlit as st
import pandas as pd
import os
from PIL import Image


# 1. Load and Prepare the Dataset
@st.cache_data
def load_data():
    # Load CSV
    df = pd.read_csv("cleaned_metadata.csv")
    
    # Convert publish_time to datetime
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    
    # Extract year from publish_time
    df['publish_year'] = df['publish_time'].dt.year

    # Fill missing journals with "Unknown"
    df['journal'] = df['journal'].fillna("Unknown")
    
    return df

df = load_data()

# 2. Dashboard Title and Description
st.title("🧬 Cord-19 COVID-19 Research Explorer")

st.markdown("""
This dashboard allows you to **explore the Cord-19 dataset**, which contains a large collection of research papers
related to **COVID-19 and coronaviruses**.

**Features:**
- Filter data by year and journal
- View summary statistics and visualizations
- Analyze trends in COVID-19 research over time
""")

# 3. Sidebar Filters
st.sidebar.header("Filters")
st.sidebar.markdown("Use the filters below to customize the dataset view:")

# Filter by Year
min_year = int(df['publish_year'].min())
max_year = int(df['publish_year'].max())

year_range = st.sidebar.slider(
    "Select Publication Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Filter by Journal
selected_journal = st.sidebar.multiselect(
    "Select Journal(s)",
    options=df['journal'].dropna().unique(),
    default=df['journal'].dropna().unique()
)

# Apply filters
filtered_df = df[
    (df['publish_year'] >= year_range[0]) &
    (df['publish_year'] <= year_range[1]) &
    (df['journal'].isin(selected_journal))
]

# 4. Show Filtered Data Sample
st.subheader("Sample of Filtered Data")
st.write("Here are the first 10 rows of the filtered dataset:")
st.dataframe(filtered_df.head(10))

# Display basic stats
st.markdown("### Dataset Summary")
st.write(f"**Total Papers:** {len(filtered_df)}")
st.write(f"**Selected Journals:** {', '.join(selected_journal[:5])} {'...' if len(selected_journal) > 5 else ''}")
st.write(f"**Year Range:** {year_range[0]} - {year_range[1]}")

# 5. Helper Function to Show Images
def display_image(image_filename, caption):
    # If images are in the same folder as app.py
    if os.path.exists(image_filename):
        image = Image.open(image_filename)
        st.image(image, caption=caption, use_column_width=True)
    else:
        st.warning(f"Image not found: {image_filename}")

# 6. Show Visualizations
st.subheader("📈 Visualizations")

# Visualization 1: Publications Over Time
st.write("### 1. Publications Over Time")
display_image("publications_over_time.png", "Number of Publications Over Time")

# Visualization 2: Top Publishing Journals
st.write("### 2. Top Publishing Journals")
display_image("top_journals.png", "Top 10 Journals by Publication Count")

# Visualization 3: Word Cloud of Paper Titles
st.write("### 3. Word Cloud of Paper Titles")
display_image("titles_wordcloud.png", "Word Cloud of Paper Titles")

# Visualization 4: Distribution by Source
st.write("### 4. Distribution of Papers by Source")
display_image("papers_by_source.png", "Distribution of Papers by Source")

#  Summary Insights
st.subheader("🔍 Summary Insights")
st.markdown("""
- **Publications Over Time:** Shows how COVID-19 research output has changed annually.
- **Top Journals:** Identifies the journals with the most publications.
- **Word Cloud:** Highlights common keywords in research paper titles.
- **Source Distribution:** Displays which sources contributed most to the dataset.
""")

st.success("Dashboard loaded successfully! Use the filters on the left to customize the data view.")
