from langchain_core.prompts import PromptTemplate

target_identify_prompt = PromptTemplate(
    template="""
You are a data analyst AI. You are given metadata of a dataset's columns. 
Your task is to identify the most suitable **target column** for machine learning. 

Follow these rules:

1️⃣ Ignore columns that are:
   - ID-like (unique for every row)
   - Constant (same value for all rows)
   - Have 100% missing values

2️⃣ Consider columns as **targets** if:
   - They have variation in values
   - For classification: categorical columns with a reasonable number of classes (2–20)
   - For regression: numeric columns

3️⃣ Use these metadata to reason:
   - Column name
   - Data type
   - Number of unique values
   - Missing percent

4️⃣ Output in strict JSON format nothing etra no extra line other than this. no markdown nothing only this with in second bracket just it:

{{
  "target_column": string | null,
  "task_type": "classification" | "regression" | null,
  "confidence": number,
  "reason": string
}}

Metadata (JSON format):

{column_metadata}

Answer in JSON format only.
""",
input_variables=["column_metadata"]
)

eda_insight_summary_prompt = PromptTemplate(
    template="""
You are a senior data scientist generating an Exploratory Data Analysis (EDA) summary report.

You are given structured outputs from multiple EDA steps along with file paths of generated visual artifacts only the image URLs not other than that.

Your task is to synthesize them into a clear, concise, and well-organized human-readable report, while also assigning the correct visual outputs to their relevant sections. Also add some small amount of relevent explanation into each point.

==============================
STRICT RULES

Do NOT repeat raw statistics unless needed for insight, add necessary data means numbers from the given data if needed

Do NOT invent information

Do NOT describe or interpret visuals explicitly

Do NOT mention how visuals look

Do NOT add sections beyond what is requested

Visuals must be listed only under the subsection “Associated Visuals”

If no visuals are available for a section, just leave it.

==============================
SECTIONS TO GENERATE

1️⃣ Dataset Overview

Dataset size (rows, columns)

Types of features (numerical vs categorical)

Overall impression of dataset scale and complexity

Associated Visuals:

None

2️⃣ Data Quality Assessment

Missing values (presence or absence)

Duplicate rows

Constant or unusable columns

Overall data cleanliness assessment

Associated Visuals:

Use visuals related to general data integrity (if any)

3️⃣ Numerical Feature Insights

Distribution behavior (normality, skewness)

Presence or absence of outliers

Numerical features that may need transformation

Associated Visuals:

Numerical distribution visuals

Boxplot or histogram outputs related to numerical features

4️⃣ Categorical Feature Insights

Cardinality assessment

Balance vs imbalance in categories

Suitability of encoding strategies

Associated Visuals:

Category distribution visuals for categorical columns

5️⃣ Outlier Analysis

Which features contain outliers

Severity and expected impact

Whether removal or transformation is recommended

Associated Visuals:

Outlier-specific visuals only

6️⃣ Feature Relationships

Correlation strength among numerical features

Multicollinearity assessment using VIF

Whether feature redundancy is a concern

Associated Visuals:

Feature relationship or correlation visuals

7️⃣ Target Variable Assessment

Identified target column

Task type (classification or regression)

Class balance or distribution quality

Confidence in target suitability

Associated Visuals:

Target distribution visuals

8️⃣ Recommended Preprocessing Steps

Encoding recommendations

Scaling or normalization needs

Outlier handling strategy

Any transformations suggested

Associated Visuals:

None

9️⃣ Modeling Readiness Score (0–100)

Assign a score based on:

Data cleanliness

Feature quality

Target suitability

Brief justification in 1–2 lines

Associated Visuals:

None

==============================
INPUT DATA

Dataset Overview:
{data_overview}

Data Quality:
{data_quality}

Numerical Statistics:
{numerical_stats}

Categorical Analysis:
{categorical_analysis}

Outlier Analysis:
{outlier_analysis}

Correlation & VIF Analysis:
{correlation_analysis}

Target Analysis:
{target_analysis}

Visual Artifacts (Grouped):
{visual_outputs}

==============================
OUTPUT FORMAT

Use clear section headings

Use bullet points

Each section MUST include an “Associated Visuals” only URLs if it has visuals otherwise dont show

List only relevant file paths under each section

Do NOT return JSON

Do NOT include markdown fences

Do NOT include extra commentary

Remember all the points carefully.
""",
input_variables=["data_overview","data_quality","numerical_stats","categorical_analysis","outlier_analysis","correlation_analysis","target_analysis","visual_outputs"]
)

mongo_prompt = PromptTemplate(
    template = """
write in detailed on the values only that is given below. 
keep all the data exact and summarize with all the numbers
data given  : 
{mongo_doc}
""",
input_variables=["mongo_doc"]
)