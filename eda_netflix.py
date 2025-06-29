import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io

# Set up
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)

# Step 0: Create output folder if not exists
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Step 1: Load dataset
df = pd.read_csv("netflix_titles.csv")
with open(f"{output_dir}/summary.txt", "w", encoding="utf-8") as f:
    f.write("Dataset loaded successfully.\n")
    f.write(df.head().to_string())
    f.write("\n\n🔹 Dataset Info:\n")
    buffer = io.StringIO()
    df.info(buf=buffer)
    f.write(buffer.getvalue())

# Step 2: Explore
missing = df.isnull().sum()
desc = df.describe(include='all')

with open(f"{output_dir}/summary.txt", "a", encoding="utf-8") as f:
    f.write("\n\n Missing Values:\n")
    f.write(missing.to_string())
    f.write("\n\n Dataset Summary:\n")
    f.write(desc.to_string())

# Step 3: Data Cleaning
df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Unknown')

# Step 4: Visualizations and Save as PNG

# 4.1 Type Count
sns.countplot(data=df, x='type', palette='Set2')
plt.title("Count of Movies vs TV Shows")
plt.xlabel("Type")
plt.ylabel("Count")
plt.savefig(f"{output_dir}/type_count.png")
plt.clf()

# 4.2 Content Added by Year
df['year_added'].value_counts().sort_index().plot(kind='bar')
plt.title("Content Added by Year")
plt.xlabel("Year")
plt.ylabel("Number of Titles Added")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}/added_by_year.png")
plt.clf()

# 4.3 Top 10 Countries
top_countries = df['country'].value_counts().head(10)
sns.barplot(y=top_countries.index, x=top_countries.values, palette='magma')
plt.title("Top 10 Countries with Most Netflix Content")
plt.xlabel("Number of Titles")
plt.ylabel("Country")
plt.savefig(f"{output_dir}/top_10_countries.png")
plt.clf()

# 4.4 Rating Distribution
sns.countplot(data=df, y='rating', order=df['rating'].value_counts().index[:10], palette='cool')
plt.title("Top 10 Ratings Distribution")
plt.xlabel("Count")
plt.ylabel("Rating")
plt.savefig(f"{output_dir}/rating_distribution.png")
plt.clf()

# 4.5 Top 10 Genres
all_genres = df['listed_in'].str.split(', ').explode()
top_genres = all_genres.value_counts().head(10)
sns.barplot(x=top_genres.values, y=top_genres.index, palette='viridis')
plt.title("Top 10 Genres on Netflix")
plt.xlabel("Count")
plt.ylabel("Genre")
plt.savefig(f"{output_dir}/top_genres.png")
plt.clf()

# Step 5: Save Insights in Text File
insights = """
Key Insights from Netflix Dataset EDA:

1. Netflix has more Movies than TV Shows.
2. Most content was added in recent years (2018–2020).
3. United States leads in the number of titles, followed by India and UK.
4. The most common content rating is TV-MA, suitable for mature audiences.
5. The top genres include Dramas, International Movies, and Comedies.
"""

with open(f"{output_dir}/summary.txt", "a", encoding="utf-8") as f:
    f.write(insights)

print("All outputs saved to 'output' folder.")
