
how_it_works_zero_shot = """
Jim is interviewing Applicant for a job as a Data Scientist. Jim knows all concepts in Data Science and always applies them correctly.

Perform the task specified within the <<>>.

Topic: {0}
What Amol used: {1}
Jim: <<Jim asks Applicant a question about how the approach Applicant chose works. Jim only asks this question and no other.>>
"""

how_it_works_k_shot = """
Jim is interviewing Applicant for a job as a Data Scientist. Jim knows all concepts in Data Science and always applies them correctly.

Jim asks Applicant questions about how the approaches Applicant uses work, in the following format:
Topic: $<a data science topic>
What Applicant used: $<the approach Applicant used to solve the problem>
Jim: $<a question about how Applicant's approach works>


Below are some correct examples:

Topic: encoding categorical values
What Applicant did: one-hot encoding
Jim: How does one hot encoding work?

Topic: class imbalance
What Applicant did: downsample the majority class
Jim: How does downsampling work?

Topic: model metrics
What Applicant used: precision
Jim: How do you calculate precision?

Topic: algorithm selection
What Applicant used: random forest
Jim: How does a random forest model work?

Topic: scaling continuous values
What Applicant used: standard scaler
Jim: Can you explain to me how a standard scaler transforms values?

Topic: {0}
What Applicant used: {1}
Jim: 
"""

ask_applicant_questions_set1 = """Jim is interviewing Applicant for a job as a Data Scientist. Jim knows all concepts in Data Science and is exceptional at applying them correctly.

Jim asks Applicant questions about the approach Applicant uses, in the following format:
What Applicant used: $<the approach Applicant used to solve the problem>
Question type: $<what type of question jim should ask>
Is question correct: $<1 or 0 - whether the question jim asks is of the right type or not>
Jim: $<a question about Applicant's approach>

Below are some examples:

What Applicant used: precision
Question type: how it works
Is question correct: 0
Jim: What is the difference between precision and recall?

What Applicant used: precision
Question type: how it works
Is question correct: 0
Jim: What are the advantages and disadvantages of using precision as a metric?

What Applicant used: precision
Question type: how it works
Is question correct: 0
Jim: What is the difference between precision and accuracy?

What Applicant used: precision
Question type: how it works
Is question correct: 0
Jim: What are the differences between precision, recall, and accuracy?

What Applicant used: precision
Question type: how it works
Is question correct: 0
Jim: What is the relationship between precision and recall?

What Applicant used: precision
Question type: how it works
Is question correct: 0
Jim: What are the assumptions behind the calculation of precision?

What Applicant used: precision
Question type: how it works
Is question correct: 0
Jim: What are the advantages and drawbacks of using precision as a metric?

What Applicant used: precision
Question type: how it works
Is question correct: 0
Jim: What are the differences between precision and recall?

What Applicant used: precision
Question type: how it works
Is question correct: 0
Jim: What are the implications of using precision as a metric for evaluating a model?

What Applicant did: one-hot encoding
Question type: how it works
Is question correct: 1
Jim: How does one hot encoding work?

What Applicant did: downsample the majority class
Question type: how it works
Is question correct: 1
Jim: How does downsampling work?

What Applicant used: precision
Question type: how it works
Is question correct: 1
Jim: How do you calculate precision? 

What Applicant used: random forest
Question type: how it works
Is question correct: 1
Jim: How does a random forest model work?

What Applicant used: standard scaler
Question type: how it works
Is question correct: 1
Jim: Can you explain to me how a standard scaler works?

What Applicant used: precision
Question type: compare
Is question correct: 1
Jim: What is the difference between precision and recall?

What Applicant used: precision
Question type: pros and cons
Is question correct: 1
Jim: What are the advantages and disadvantages of using precision as a metric?

What Applicant used: precision
Question type: compare
Is question correct: 1
Jim: What is the difference between precision and accuracy?

What Applicant used: precision
Question type: compare
Is question correct: 1
Jim: What are the differences between precision, recall, and accuracy?

What Applicant used: precision
Question type: compare
Is question correct: 1
Jim: What is the relationship between precision and recall?

What Applicant used: precision
Question type: assumptions
Is question correct: 1
Jim: What are the assumptions behind the calculation of precision?

What Applicant used: precision
Question type: pros and cons
Is question correct: 1
Jim: What are the advantages and drawbacks of using precision as a metric?

What Applicant used: precision
Question type: compare
Is question correct: 1
Jim: What are the differences between precision and recall?

What Applicant used: precision
Question type: implications
Is question correct: 1
Jim: What are the implications of using precision as a metric for evaluating a model?

What Applicant used: gridsearch
Question type: how it works
Is question correct: 0
Jim: What is the difference between gridsearch and random search?

What Applicant used: NA
Question type: how it works
Is question correct: 0
Jim: Can you explain to me what hyperparameter tuning is?

What Applicant used: NA
Question type: how it works
Is question correct: 1
Jim: <<skip>>

What Applicant used: NA
Question type: how it works
Is question correct: 0
Jim: What is the purpose of scaling continuous values?

What Applicant used: NA
Question type: how it works
Is question correct: 1
Jim: <<skip>>

What Applicant used: NA
Question type: how it works
Is question correct: 0
Jim: What is feature engineering?

What Applicant used: NA
Question type: how it works
Is question correct: 1
Jim: <<skip>>

What Applicant did: NA
Question type: how it works
Is question correct: 0
Jim: What are some techniques to address class imbalance?

What Applicant used: gridsearch
Question type: how it works
Is question correct: 1
Jim: Can you explain how Grid Search works?

{0}
"""

validate_jims_question_zero_shot = """
Jim is interviewing Applicant for a job as a Data Scientist. Jim knows all concepts in Data Science and always applies them correctly.

Jim has to validate whether a prospective question is valid. Jim performs the task specified within the <<>>.

Topic: {0}
What Applicant used: {1}
Prospective question: {2}
Is question valid: <<whether the question only asks how the approach Applicant chose works. Answer with "Yes" or "No". If the question asks anything other than this, answer "No".>>
"""

validate_jims_question_k_shot = """Jim is interviewing Amol for a job as a Data Scientist. Jim knows all concepts in Data Science and always applies them correctly.

Jim assesses whether a prospective question satisfies a certain requirement, in the following format:
Topic: $<a data science topic>
What Applicant used: $<the approach Applicant used to perform a task>
Prospective question: $<a question about how Applicant's approach work>
Is question valid: $<whether the question only asks how the approach Applicant chose works. Answer with "Yes" or "No". If the question asks anything other than how the approach works, answer "No".>

Below are some correct examples:

Topic: encoding categorical values
What Applicant used: one-hot encoding
Prospective question: How does one hot encoding work?
Is question valid: Yes

Topic: class imbalance
What Applicant used: downsample the majority class
Prospective question: How does downsampling work?
Is question valid: Yes

Topic: model metrics
What Applicant used: precision
Prospective question: How do you calculate precision?
Is question valid: Yes

Topic: algorithm selection
What Applicant used: random forest
Prospective question: How does a random forest model work?
Is question valid: Yes

Topic: scaling continuous values
What Applicant used: standard scaler
Prospective question: Can you explain to me how a standard scaler transforms values?
Is question valid: Yes

Topic: encoding categorical values
What Applicant used: one-hot encoding
Prospective question: Why did you choose one hot encoding instead of binary encoding?
Is question valid: No

Topic: class imbalance
What Applicant used: downsample the majority class
Prospective question: What are the advantages of using downsampling in this situation?
Is question valid: No

Topic: model metrics
What Applicant used: precision
Prospective question: Can you please explain how precision works and why it is an important metric for evaluating a model? 
Is question valid: No

Topic: algorithm selection
What Applicant used: random forest
Prospective question: Can you explain to me why you chose to use random forest as your algorithm?
Is question valid: No

Topic: scaling continuous values
What Applicant used: standard scaler
Prospective question: Could you explain how standard scaler works and why it is a good approach for scaling continuous values?
Is question valid: No

Topic: model metrics
What Applicant used: precision
Prospective question: Jim: Can you explain why you chose precision as a metric for your model?
Is question valid: No

Topic: {0}
What Applicant used: {1}
Prospective question: {2}
Is question valid:
"""

clarify_applicants_questions = """
Jim is interviewing Applicant for a job as a Data Scientist. Jim knows all concepts in Data Science and always applies them correctly.

Rules for Jim:
- If Applicant says they don’t understand the question and asks claryfying questions, Jim answers the clarifying questions to help Applicant better understand Jim's question.

Topic: {0}
Jim: {1}
Applicant: I don't understand. {2}
Jim:
"""

validate_applicants_answer = """
Jim is interviewing Applicant for a job as a Data Scientist. Jim knows all concepts in Data Science and always applies them correctly.

Jim validates Applicant's answer in the following format:
Problem: $<a data science challenge for Applicant>
What Applicant used: $<the approach Applicant used to solve the problem>
Applicant's explanation: $<applicant's explanation of how Applicant's approach works>
Correct explation: $<correct explanation of how Applicant's approach works>
Validation of explanation: $<whether Applicant's explanation is correct, incomplete, or incorrect>

Below are some correct examples:

Problem: dealing with class imbalance
What Applicant used: undersampled the majority class
Applicant's explanation: By undersampling the majority class, the ratio between the number of observations in the majority and minority classes increases, making the dataset less imbalanced.
Correct explation: By undersampling the majority class, the ratio between the number of observations in the majority and minority classes decreases, making the dataset less imbalanced.
Validation of explanation: incorrect

Problem: dealing with class imbalance
What Applicant used: undersampled the majority class
Applicant's explanation: By undersampling the majority class, the ratio between the number of observations in the majority and minority classes decreases, making the dataset less imbalanced.
Correct explation: By undersampling the majority class, the ratio between the number of observations in the majority and minority classes decreases, making the dataset less imbalanced.
Validation of explanation: correct

Problem: dealing with class imbalance
What Applicant used: undersampled the majority class
Applicant's explanation: By undersampling the majority class, class imbalance is addressed.
Correct explanation: By undersampling the majority class, the ratio between the number of observations in the majority and minority classes decreases, making the dataset less imbalanced.
Validation of explanation: incomplete

Problem: model metrics
What Applicant used: precision
Applicant's explanation: Precision is a model metric that measures what fraction of the actual positives the model predicted as positive.
Correct explation: Precision is a model metric that measures what fraction of the predicted positives the model predicted correctly.
Validation of explanation: incorrect

Problem: model metrics
What Applicant used: precision
Applicant's explanation: Precision is a model metric
Correct explation: Precision is a model metric that measures what fraction of the predicted positives the model predicted correctly.
Validation of explanation: incomplete

Problem: feature selection
What Applicant used: forward selection
Applicant's explanation: With forward selection, you start with a model with zero features and add the feature which has the best score. The score is chosen beforehand, like the p value of a t test. We keep doing this iteratively until a stopping criterion is reached, like a max number of features or a min increase in performance by adding a feature. 
Correct explation: With forward selection, you start with a model with zero features and add the feature which has the best score. The score is chosen beforehand, like the p value of a t test. We keep doing this iteratively until a stopping criterion is reached, like a max number of features or a min increase in performance by adding a feature. 
Validation of explanation: correct

Problem: encoding categorical values
What Applicant used: one-hot encoding
Applicant's explanation: One-hot encoding converts each unique categorical value to a number.
Correct explation: One-hot encoding converts each unique categorical value to a binary vector.
Validation of explanation: incorrect

Problem: algorithm selection
What Applicant used: random forest
Applicant's explanation: random forest is a tree-based ensemble model. Multiple decision trees are fit on the data. At each decision stump, a random subset of features and observations is used. By doing so, the model learns to not overfit to features and observations. The final model output is the mode of the decision trees for classification tasks, and the mean of the decision trees for regression tasks. 
Correct explation: A random forest model is an ensemble machine learning algorithm that is used for classification, regression, and other tasks. It works by constructing a multitude of decision trees from randomly selected subsets of the data and then combining their individual predictions to form a final prediction. The random forest model uses bagging and random feature selection to create the decision trees, and then aggregates the predictions of each tree to determine the final prediction. This makes the model robust and resilient to outliers, as the predictions of any one single tree can be offset by the other trees in the forest. It is also resistant to overfitting, as each tree only has access to a subset of the data, which prevents it from overfitting on the training data.
Validation of explanation: correct

Problem: algorithm selection
What Applicant used: random forest
Applicant's explanation: random forest is a neural network where model accuracy is optimized using backpropagation.
Correct explation: A random forest model is an ensemble machine learning algorithm that is used for classification, regression, and other tasks. It works by constructing a multitude of decision trees from randomly selected subsets of the data and then combining their individual predictions to form a final prediction.
Validation of explanation: incorrect

Problem: algorithm selection
What Applicant used: random forest
Applicant's explanation: random forest is an ensemble model
Correct explation: A random forest model is an ensemble machine learning algorithm that is used for classification, regression, and other tasks. It works by constructing a multitude of decision trees from randomly selected subsets of the data and then combining their individual predictions to form a final prediction.
Validation of explanation: incomplete

Problem: feature selection
What Applicant used: forward selection
Applicant's explanation: With forward selection, you start with zero features and keep adding features till you have a model you like.
Correct explation: With forward selection, you start with a model with zero features and add the feature which has the best score. The score is chosen beforehand, like the p value of a t test. We keep doing this iteratively until a stopping criterion is reached, like a max number of features or a min increase in performance by adding a feature. 
Validation of explanation: incomplete

Problem: scaling continuous values
What Applicant used: standard scaler
Applicant's explanation: it normalizes the data
Correct explation: Standard scaler transforms the data by subtracting the mean and dividing by the standard deviation, so that the resulting distribution has a mean of 0 and a standard deviation of 1.
Validation of explanation: incomplete

Problem: scaling continuous values
What Applicant used: standard scaler
Applicant's explanation: it gives the data a mean of 0 and standard deviation of 1
Correct explation: Standard scaler transforms the data by subtracting the mean and dividing by the standard deviation, so that the resulting distribution has a mean of 0 and a standard deviation of 1.
Validation of explanation: correct

Problem: missing values
What Applicant used: mean imputing
Applicant's explanation: it imputes the missing value with the last known value of that feature
Correct explation: Mean imputing replaces missing values with the mean of the feature.
Validation of explanation: incorrect

Problem: missing values
What Applicant used: mean imputing
Applicant's explanation: it fills the missing values
Correct explation: Mean imputing replaces missing values with the mean of the feature.
Validation of explanation: incomplete

Problem: hyper tuning
What Applicant used: grid search
Applicant's explanation: creates a grid of parameters and picks the best hyperparameters
Correct explation: Grid search is an algorithm tuning technique that exhaustively searches through a manually specified subset of the hyperparameter space of a learning algorithm for the best performing set of hyperparameters.
Validation of explanation: incomplete

Problem: business metrics
What Applicant used: calculate total dollar cost of solution
Applicant's explanation: use model confusion matrix to calculate total dollars cost of the solution
Correct explation: The total dollar cost of a solution can be calculated by multiplying the cost of a false positive and false negative by the number of false positives and false negatives in the model's confusion matrix.
Validation of explanation: incomplete

Problem: business metrics
What Applicant used: calculate number of accidents prevented by using my model
Applicant's explanation: subtract the number of false negatives after using my model from the number of false negatives before using my model
Correct explation: The number of accidents prevented by using a model can be calculated by subtracting the number of false negatives after using the model from the number of false negatives before using the model.
Validation of explanation: correct

Problem: business metrics
What Applicant used: calculate number of accidents prevented after using my model
Applicant's explanation: calculate difference in the number of true positives between the client's approach before my solution and with my solution
Correct explation: The number of accidents prevented after using a model can be calculated by subtracting the number of true positives from the model's confusion matrix before the model was implemented from the number of true positives after the model was implemented.
Validation of explanation: correct

Problem: business metrics
What Applicant used: calculate number of accidents prevented after using my model
Applicant's explanation: subtract the number of true positives before using my model from the number of true positives after using the model
Correct explation: The number of accidents prevented after using a model can be calculated by subtracting the number of true positives from the model's confusion matrix before the model was implemented from the number of true positives after the model was implemented.
Validation of explanation: correct

Problem: business metrics
What Applicant used: calculate number of accidents prevented after using my model
Applicant's explanation: compare the confusion matrices before and after using my model
Correct explation: The number of accidents prevented after using a model can be calculated by subtracting the number of true positives from the model's confusion matrix before the model was implemented from the number of true positives after the model was implemented.
Validation of explanation: incomplete

Problem: dealing with class imbalance
What Applicant used: SMOTE
Applicant's explanation: SMOTE synthetically generates observations
Correct explation: SMOTE (Synthetic Minority Oversampling Technique) is an oversampling technique that synthetically generates observations of the minority class by interpolating between existing observations.
Validation of explanation: incomplete

Problem: dealing with class imbalance
What Applicant used: SMOTE
Applicant's explanation: SMOTE synthetically generates observations by creating new data points between observations and their nearest neighbors.
Correct explation: SMOTE (Synthetic Minority Oversampling Technique) is an oversampling technique that synthetically generates observations of the minority class by interpolating between existing observations and their nearest neighbors.
Validation of explanation: correct

Problem: feature selection
What Applicant used: Lasso
Applicant's explanation: It is a linear model that contains an L1 regularization penalty that reduces the coefficients of non-predictive features to zero. This model can thus be used to perform feature selection.
Correct explation: A lasso model is a type of regularization technique that helps to reduce model complexity and mitigate overfitting. It does this by introducing a penalty term to the cost function of the model, which penalizes the magnitude of the coefficients of the predictors in the model. This encourages the model to only include the most important predictors and reduces the complexity of the model. The result is a more accurate and reliable model.
Validation of explanation: correct

Problem: feature selection
What Applicant used: Lasso
Applicant's explanation: It is a linear model that helps to select features for you.
Correct explation: A lasso model is a type of regularization technique that helps to reduce model complexity and mitigate overfitting. It does this by introducing a penalty term to the cost function of the model, which penalizes the magnitude of the coefficients of the predictors in the model. This encourages the model to only include the most important predictors and reduces the complexity of the model. The result is a more accurate and reliable model.
Validation of explanation: incomplete

Problem: {0}
What Applicant used: {1}
Applicant's explanation: {2}
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