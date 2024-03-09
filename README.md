# Precision@N

Precision@N measures the proportion of recommended items in the top-N list that are relevant to the user. It's crucial
for understanding how many of the items presented to the user are actually of interest. The relevance of an item is
typically determined based on whether the user has interacted with (e.g., viewed, clicked on, or purchased) the item.

Identify Relevant Items: For each user, identify the set of items that are considered relevant. This could be based on
historical interactions or explicit ratings.

Generate Recommendations: Use your item-based recommender system to generate a list of the top-N recommendations for
each user.

Calculate Precision: For each user, calculate Precision@N as the number of relevant items in the top-N recommendations
divided by N. Then, average these precision values across all users to get the overall Precision@N.

# NDCG (Normalized Discounted Cumulative Gain)

NDCG accounts for the position of the relevant items within the recommendation list, giving higher importance to items
ranked higher. It's a more nuanced metric than Precision@N because it considers not just the presence of relevant items,
but their ranking. This is particularly important in real-world scenarios where users might only consider the top few
recommendations.

Calculate DCG (Discounted Cumulative Gain): For each user, calculate the DCG for their list of recommendations. DCG is
the sum of the relevance scores of recommended items, discounted logarithmically based on their position in the
recommendation list. The relevance score is typically binary (1 for relevant, 0 for non-relevant) but can be a real
number indicating the degree of relevance.

Calculate IDCG (Ideal DCG): For each user, calculate the IDCG, which is the DCG calculated for a hypothetically perfect
recommendation list where the items are sorted by their relevance.

Calculate NDCG: For each user, NDCG is the ratio of DCG to IDCG. This normalizes the score, making it possible to
compare across users and systems. Finally, average the NDCG scores across all users to get the overall NDCG.

Python Implementation

```python
import numpy as np

def precision_at_n(recommended_items, relevant_items, n):
    relevant_and_recommended = np.intersect1d(recommended_items[:n], relevant_items)
    precision = len(relevant_and_recommended) / n
    return precision

def dcg_at_n(recommended_items, relevant_items, n):
    relevances = np.isin(recommended_items[:n], relevant_items).astype(int)
    discounts = np.log2(np.arange(len(relevances)) + 2)  # +2 because the index starts at 1
    dcg = np.sum(relevances / discounts)
    return dcg

def ndcg_at_n(recommended_items, relevant_items, n):
    actual_dcg = dcg_at_n(recommended_items, relevant_items, n)
    ideal_dcg = dcg_at_n(sorted(relevant_items, reverse=True), relevant_items, n)
    ndcg = actual_dcg / ideal_dcg if ideal_dcg > 0 else 0
    return ndcg

# Example usage:
recommended_items = np.array([5, 1, 3, 4, 2])  # IDs of recommended items
relevant_items = np.array([1, 2, 4])  # IDs of items the user finds relevant
n = 5

print("Precision@N:", precision_at_n(recommended_items, relevant_items, n))
print("NDCG:", ndcg_at_n(recommended_items, relevant_items, n))
```

This example assumes binary relevance (an item is either relevant or not), which is common in many recommendation system
evaluations. For cases where relevance is graded, you would adjust the relevance scores accordingly in the dcg_at_n
function.

# Thesis

- Research pages with articles:
    - arxiv
    - springer -> DOI -> scihub.__
    - https://repo.pw.edu.pl/search/diploma
    - ieee
- Thesis structure
    - Research
        - ML algorithms
            - Classification: LinReg, DecTree, SVC, KNN
            - Recommendations: Collaborative Filtering with NearestNeighbors, ...
            -
        -

# ChatGPT

Custom Instructions
How would you like ChatGPT to respond?
"""
You are an autoregressive language model that has been fine-tuned with instruction-tuning and RLHF. You carefully
provide accurate, factual, thoughtful, and nuanced answers, and are brilliant at reasoning. If you think there might not
be a correct answer, you say so. Since you are autoregressive, each token you produce is another opportunity to use
computation, therefore you always spend a few sentences explaining background context, assumptions, and step-by-step
thinking BEFORE you try to answer a question. Your users are experts in AI and ethics, so they already know you're a
language model and your capabilities and limitations, so don't remind them of that. They're familiar with ethical issues
in general so you don't need to remind them about those either.
Your users can specify the level of detail they would like in your response with the following notation: V=<level>,
where <level> can be 0-5. Level 0 is the least verbose (no additional context, just get straight to the answer), while
level 5 is extremely verbose. Your default level is 3. This could be on a separate line like so:
V=4
<question>
Or it could be on the same line as a question (often used for short questions), for example:
V=0 How do tidal forces work?
"""

# Sample ToC

## Prompt

I have a thesis that describes the use of ML in recommendation of music songs.
I'am generating a synthetic dataset that resembles spotify data (users, artists, streams tables)
Help me to define the table of content for the thesis. Make sure it will cover research regarding ML models, techniques
of generating synthetic data, propose my approach to solve the problem using ML and other techniques, and methodology
and results. Also propose all other sections and subsections that may fit in the thesis content. Dont put any
descriptions, just the structured table of contents. Be specific, but give me a lot of ideas of what can be included.

Result:

Introduction
1.1 Background and Motivation
1.2 Objectives of the Study
1.3 Research Questions
1.4 Scope and Delimitations
1.5 Structure of the Thesis

Literature Review
2.1 Overview of Machine Learning in Music Recommendation
2.2 Previous Approaches and Models
2.3 Synthetic Data in Machine Learning
2.4 Challenges in Music Recommendation Systems
2.5 Summary and Gaps in Existing Research
Theoretical Framework

3.1 Fundamentals of Machine Learning
3.2 Music Recommendation Systems: An Overview
3.3 Synthetic Data Generation: Techniques and Approaches
3.4 Evaluation Metrics for Music Recommendation Systems
Methodology

4.1 Research Design
4.2 Data Collection
4.2.1 Description of the Synthetic Dataset
4.2.2 Process of Synthetic Data Generation
4.3 Machine Learning Models
4.3.1 Model Selection
4.3.2 Model Training
4.3.3 Model Evaluation
4.4 Implementation of the Recommendation System
4.4.1 System Architecture
4.4.2 Feature Engineering
4.4.3 Algorithm Development
Developing the Synthetic Dataset

5.1 Rationale for Synthetic Data
5.2 Techniques for Generating Synthetic Data
5.3 Ensuring Realism and Variability
5.4 Ethical Considerations and Privacy
Experimentation and Results

6.1 Experiment Setup
6.2 Model Performance and Evaluation
6.3 Analysis of Recommendation Quality
6.4 Comparison with Existing Approaches
6.5 Discussion of Results
Discussion

7.1 Interpretation of Findings
7.2 Implications for Music Recommendation Systems
7.3 Limitations of the Study
7.4 Suggestions for Future Research
Conclusion

8.1 Summary of Key Findings
8.2 Contributions of the Thesis
8.3 Final Thoughts and Future Directions
References

Appendices

10.1 Appendix A: Code Listings
10.2 Appendix B: Additional Tables and Figures
10.3 Appendix C: Ethical Approval (if applicable)

# Source:

- https://towardsdatascience.com/evaluation-metrics-for-recommendation-systems-an-overview-71290690ecba
