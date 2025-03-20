import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

# Read datasets
legitimate_df = pd.read_csv("structured_data_legitimate.csv")
phishing_df = pd.read_csv("structured_data_phishing.csv")

# Combine and shuffle
df = pd.concat([legitimate_df, phishing_df], axis=0)
df = df.sample(frac=1)

# Data cleaning
df = df.drop('URL', axis=1)
df = df.drop_duplicates()

# Feature selection
X = df.drop('label', axis=1)
Y = df['label']

# Split data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=10)

# Neural Network Model
nn_model = MLPClassifier(alpha=1)

# Train Neural Network
nn_model.fit(np.array(x_train), np.array(y_train))

# Predictions using Neural Network
nn_predictions = nn_model.predict(x_test)

# Confusion Matrix
tn, fp, fn, tp = confusion_matrix(y_true=y_test, y_pred=nn_predictions).ravel()

# Calculate performance metrics
accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)
recall = tp / (tp + fn)

print("Neural Network Accuracy --> ", accuracy)
print("Neural Network Precision --> ", precision)
print("Neural Network Recall --> ", recall)

# K-Fold Cross Validation (K=5)
K = 5
total = X.shape[0]
index = int(total / K)

# 1
X_1_test = X.iloc[:index]
X_1_train = X.iloc[index:]
Y_1_test = Y.iloc[:index]
Y_1_train = Y.iloc[index:]

# 2
X_2_test = X.iloc[index:index*2]
X_2_train = X.iloc[np.r_[:index, index*2:]]
Y_2_test = Y.iloc[index:index*2]
Y_2_train = Y.iloc[np.r_[:index, index*2:]]

# 3
X_3_test = X.iloc[index*2:index*3]
X_3_train = X.iloc[np.r_[:index*2, index*3:]]
Y_3_test = Y.iloc[index*2:index*3]
Y_3_train = Y.iloc[np.r_[:index*2, index*3:]]

# 4
X_4_test = X.iloc[index*3:index*4]
X_4_train = X.iloc[np.r_[:index*3, index*4:]]
Y_4_test = Y.iloc[index*3:index*4]
Y_4_train = Y.iloc[np.r_[:index*3, index*4:]]

# 5
X_5_test = X.iloc[index*4:]
X_5_train = X.iloc[:index*4]
Y_5_test = Y.iloc[index*4:]
Y_5_train = Y.iloc[:index*4]

X_train_list = [X_1_train, X_2_train, X_3_train, X_4_train, X_5_train]
X_test_list = [X_1_test, X_2_test, X_3_test, X_4_test, X_5_test]

Y_train_list = [Y_1_train, Y_2_train, Y_3_train, Y_4_train, Y_5_train]
Y_test_list = [Y_1_test, Y_2_test, Y_3_test, Y_4_test, Y_5_test]

def calculate_measures(TN, TP, FN, FP):
    model_accuracy = (TP + TN) / (TP + TN + FN + FP)
    model_precision = TP / (TP + FP)
    model_recall = TP / (TP + FN)
    return model_accuracy, model_precision, model_recall

nn_accuracy_list, nn_precision_list, nn_recall_list = [], [], []

for i in range(0, K):
    nn_model.fit(X_train_list[i], Y_train_list[i])
    nn_predictions = nn_model.predict(X_test_list[i])
    tn, fp, fn, tp = confusion_matrix(y_true=Y_test_list[i], y_pred=nn_predictions).ravel()
    nn_accuracy, nn_precision, nn_recall = calculate_measures(tn, tp, fn, fp)
    nn_accuracy_list.append(nn_accuracy)
    nn_precision_list.append(nn_precision)
    nn_recall_list.append(nn_recall)

# Final Model Performance
NN_accuracy = sum(nn_accuracy_list) / len(nn_accuracy_list)
NN_precision = sum(nn_precision_list) / len(nn_precision_list)
NN_recall = sum(nn_recall_list) / len(nn_recall_list)

print("Neural Network Final Accuracy ==> ", NN_accuracy)
print("Neural Network Final Precision ==> ", NN_precision)
print("Neural Network Final Recall ==> ", NN_recall)

# Plot results
data = {'accuracy': [NN_accuracy], 'precision': [NN_precision], 'recall': [NN_recall]}
df_results = pd.DataFrame(data, index=['NN'])

# Visualize results
ax = df_results.plot.bar(rot=0)
plt.show()