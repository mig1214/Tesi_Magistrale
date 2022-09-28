# Import train_test_split function
import numpy
from sklearn.model_selection import train_test_split
#Import svm model
from sklearn.model_selection import GridSearchCV
from sklearn import svm, preprocessing
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

functions_p = open("./vectors/p_vectors/p_vectors.txt")
functions_c = open("./vectors/c_vectors/c_vectors.txt")
with functions_p as dp:
    p_lines = dp.readlines()
with functions_c as cp:
    c_lines = cp.readlines()

dataset = []
target = []
i = 0
while i < len(p_lines):
    data_1 = p_lines[i].split(",")[0:len(p_lines[i].strip().split(",")) - 1]
    data_2 = c_lines[i].split(",")[0:len(c_lines[i].strip().split(",")) - 1]
    # Salto quei vettori che non cambiano nonostante l'applicazione della patch
    if data_1 == data_2:
        p_lines.remove(p_lines[i])
        c_lines.remove(c_lines[i])
    else:
        num_data_1 = []
        for num in data_1:
            num_data_1.append(int(num))
        num_data_2 = []
        for num in data_2:
            num_data_2.append(int(num))
        first_part_p = num_data_1[:4]
        first_part_c = num_data_2[:4]
        j = 0
        while j < len(first_part_p):
            if first_part_c[j] < first_part_p[j]:
                num_data_1[j] = 0
                num_data_2[j] = 1
            else:
                num_data_1[j] = 1
                num_data_2[j] = 0
            j += 1
        dataset.append(num_data_1)
        target.append(int(p_lines[i].strip().split(",")[-1]))
        dataset.append(num_data_2)
        target.append(int(c_lines[i].strip().split(",")[-1]))
        '''
    num_data = []
    for num in data_1:
        num_data.append(int(num))
    dataset.append(num_data)
    target.append(int(p_lines[i].strip().split(",")[-1]))
    num_data = []
    for num in data_2:
        num_data.append(int(num))
    dataset.append(num_data)
    target.append(int(c_lines[i].strip().split(",")[-1]))
    '''
    i += 1

print(len(dataset))
print(len(target))
dataset = numpy.array(dataset)
target = numpy.array(target)
#print(dataset)
# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(dataset, target, test_size=0.3, random_state=42) # 80% training and 20% test
#sc = preprocessing.StandardScaler()
#X_train = sc.fit_transform(X_train)
#X_test = sc.transform(X_test)

#Create a svm Classifier
param_grid = {'C': [0.1, 1, 10, 100], 'kernel':  ['poly'],
              'gamma': ['scale', 'auto'], 'degree': [2, 3, 4]}
'''param_grid = [{'C': [1, 10, 100, 1000], 'kernel': ['linear']},
              {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
              {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'degree': [3, 4, 5, 6],
               'kernel': ['poly']},
              {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['sigmoid']}]'''

#svc = svm.SVC(kernel='sigmoid', class_weight='balanced', C=100, degree=1)
#scoring = ['accuracy_macro', 'precision_macro', 'recall_macro']
#clf = svm.SVC(kernel='sigmoid', C=0.1, gamma='scale', degree=1, random_state=42)
#scores = cross_val_score(clf, dataset, target, cv=10, scoring="accuracy")
#print(scores)
'''clf = GridSearchCV(SVC(), param_grid, scoring='accuracy')
clf.fit(X_train, y_train)
print("Best estimator found by grid search:")
print(clf.best_estimator_)
y_pred = clf.predict(X_test)
print(clf.best_params_)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
# Model Precision: what percentage of positive tuples are labeled as such?
print("Precision:", metrics.precision_score(y_test, y_pred, zero_division=True))
# Model Recall: what percentage of positive tuples are labelled as such?
print("Recall:", metrics.recall_score(y_test, y_pred))
'''
#print("Recall:", metrics.recall_score(y_test, y_pred))

Cs = [0.1, 1, 10, 100, 1000]
degrees = [2, 3, 4]
for c in Cs:
    svc = svm.SVC(kernel='linear', C=c, gamma="scale") # Linear Kernel
    #scores = cross_val_score(svc, dataset, target, cv=10, scoring="accuracy")
    #print(scores)
    svc.fit(X_train, y_train)
    print("Valore C:" + str(c))
    print(svc.score(X_test, y_test))
    y_pred = svc.predict(X_test)

    # Model Accuracy: how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    # Model Precision: what percentage of positive tuples are labeled as such?
    print("Precision:", metrics.precision_score(y_test, y_pred, zero_division=True))

    # Model Recall: what percentage of positive tuples are labelled as such?
    print("Recall:", metrics.recall_score(y_test, y_pred))

    print("F1-Score:", metrics.f1_score(y_test, y_pred))
    print("--------------\n")
#print(y_pred)
#print(y_test)'''


'''grid = GridSearchCV(svc, param_grid)
#Train the model using the training sets
grid.fit(X_train, y_train)

print(grid.best_params_)
print(grid.score(X_test, y_test))

#Predict the response for test dataset
y_pred = grid.predict(X_test)
'''
#print(y_pred)







