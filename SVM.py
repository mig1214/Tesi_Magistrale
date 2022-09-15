# Import train_test_split function
from sklearn.model_selection import train_test_split
#Import svm model
from sklearn import svm
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics

functions_p = open("./vectors/p_vectors/p_vectors.txt")
functions_c = open("./vectors/c_vectors/c_vectors.txt")
with functions_p as dp:
    p_lines = dp.readlines()
with functions_c as cp:
    c_lines = cp.readlines()

dataset = []
target = []
for element in p_lines:
    data_p = element.strip().split(",")[0:len(element.strip().split(",")) - 1]
    num_data = []
    for num in data_p:
        num_data.append(int(num))
    dataset.append(num_data)
    target.append(int(element.strip().split(",")[-1]))
for element in c_lines:
    data_c = element.strip().split(",")[0:len(element.strip().split(",")) - 1]
    num_data = []
    for num in data_c:
        num_data.append(int(num))
    dataset.append(num_data)
    target.append(int(element.strip().split(",")[-1]))


# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(dataset, target, test_size=0.3,random_state=109) # 70% training and 30% test

#Create a svm Classifier
clf = svm.SVC(kernel='sigmoid', gamma='auto') # Linear Kernel

#Train the model using the training sets
clf.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

print(y_pred)


# Model Accuracy: how often is the classifier correct?
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

# Model Precision: what percentage of positive tuples are labeled as such?
print("Precision:", metrics.precision_score(y_test, y_pred))

# Model Recall: what percentage of positive tuples are labelled as such?
print("Recall:",metrics.recall_score(y_test, y_pred))




