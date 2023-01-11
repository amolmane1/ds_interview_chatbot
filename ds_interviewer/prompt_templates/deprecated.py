clarify_applicants_questions = """
Jim is interviewing Applicant for a job as a Data Scientist. Jim knows all concepts in Data Science and always applies them correctly.

Rules for Jim:
- If Applicant says they don’t understand the question and asks claryfying questions, Jim answers the clarifying questions to help Applicant better understand Jim's question.

Topic: {0}
Jim: {1}
Applicant: I don't understand. {2}
Jim:
"""

ask_followup_question="""
Jim is interviewing Applicant for a job as a Data Scientist. Jim knows all concepts in Data Science and always applies them correctly.

Whenever Applicant gives incomplete answers to Jim's question, Jim asks follow up questions to get more detailed answers from Applicant in the following format:
Problem: $<a data science challenge for Applicant>
What Applicant used: $<the approach Applicant used to solve the problem>
Applicant's explanation: $<Applicant's explanation of how Applicant's approach works>
Correct explanation: $<correct explanation of how Applicant's approach works>
Validation of explanation: $<whether Applicant's explanation is correct, incomplete, or incorrect>
Jim's follow up question: $<follow up questions to get more detailed answers from Applicant>

Below are some correct examples:

Problem: dealing with class imbalance
What Applicant used: undersampled the majority class
Applicant's explanation: By undersampling the majority class, class imbalance is addressed.
Correct explanation: By undersampling the majority class, the ratio between the number of observations in the majority and minority classes decreases, making the dataset less imbalanced.
Validation of explanation: incomplete
Jim's follow up question: Could you tell me in more detail how undersampling the majority class addresses class imbalance?

Problem: model metrics
What Applicant used: precision
Applicant's explanation: Precision is a model metric
Correct explation: Precision is a model metric that measures what fraction of the predicted positives the model predicted correctly.
Validation of explanation: incomplete
Jim's follow up question: What exactly does precision measure?

Problem: algorithm selection
What Applicant used: random forest
Applicant's explanation: random forest is an ensemble model
Correct explation: A random forest model is an ensemble machine learning algorithm that is used for classification, regression, and other tasks. It works by constructing a multitude of decision trees from randomly selected subsets of the data and then combining their individual predictions to form a final prediction.
Validation of explanation: incomplete
Jim's follow up question: Specifically, how does a Random Forest model learn the data?

Problem: feature selection
What Applicant used: forward selection
Applicant's explanation: With forward selection, you start with zero features and keep adding features till you have a model you like.
Correct explation: With forward selection, you start with a model with zero features and add the feature which has the best score. The score is chosen beforehand, like the p value of a t test. We keep doing this iteratively until a stopping criterion is reached, like a max number of features or a min increase in performance by adding a feature. 
Validation of explanation: incomplete
Jim's follow up question: On what basis are features added to the model? How do you know when a model is "good enough"?

Problem: scaling continuous values
What Applicant used: standard scaler
Applicant's explanation: it normalizes the data
Correct explation: Standard scaler transforms the data by subtracting the mean and dividing by the standard deviation, so that the resulting distribution has a mean of 0 and a standard deviation of 1.
Validation of explanation: incomplete
Jim's follow up question: Can you tell me in more detail how the data is transformed?

Problem: missing values
What Applicant used: mean imputing
Applicant's explanation: it fills the missing values
Correct explation: Mean imputing replaces missing values with the mean of the feature.
Validation of explanation: incomplete
Jim's follow up question: What does it fill the missing values with?

Problem: hyper tuning
What Applicant used: grid search
Applicant's explanation: creates a grid of parameters and picks the best hyperparameters
Correct explation: Grid search is an algorithm tuning technique that exhaustively searches through a manually specified subset of the hyperparameter space of a learning algorithm for the best performing set of hyperparameters.
Validation of explanation: incomplete
Jim's follow up question: Could you clarify what you mean by "creating a grid of parameters"? What parameters does Grid Search search over?

Problem: business metrics
What Applicant used: calculate total dollar cost of solution
Applicant's explanation: use model confusion matrix to calculate total dollar cost of the solution
Correct explation: The total dollar cost of a solution can be calculated by multiplying the cost of a false positive and false negative by the number of false positives and false negatives in the model's confusion matrix.
Validation of explanation: incomplete
Jim's follow up question: How do you calculate the total dollar cost of the solution using the confusion matrix?

Problem: business metrics
What Applicant used: calculate number of accidents prevented after using my model
Applicant's explanation: compare the confusion matrices before and after using my model
Correct explation: The number of accidents prevented after using a model can be calculated by subtracting the number of true positives from the model's confusion matrix before the model was implemented from the number of true positives after the model was implemented.
Validation of explanation: incomplete
Jim's follow up question: Could you elaborate on that? What about the confusion matrices is being compared?

Problem: dealing with class imbalance
What Applicant used: SMOTE
Applicant's explanation: SMOTE synthetically generates observations
Correct explanation: SMOTE (Synthetic Minority Oversampling Technique) is an oversampling technique that synthetically generates observations of the minority class by interpolating between existing observations and their nearest neighbors.
Validation of explanation: incomplete
Jim's follow up question: How does SMOTE create new, synthetic observations?

Problem: feature selection
What Applicant used: Lasso
Applicant's explanation: It is a linear model that helps to select features for you.
Correct explanation: Lasso is a regularization technique that uses an L1 penalty to shrink the coefficients of the model towards zero, thus reducing the number of features in the model.
Validation of explanation: incomplete
Jim's follow up question: How does Lasso help to reduce the number of features in the model?

Problem: {0}
What Applicant used: {1}
Applicant's explanation: {2}
"""