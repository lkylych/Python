from sklearn import datasets
from scipy.spatial import distance
iris = datasets.load_iris()

def euc(a, b):
	return distance.euclidean(a, b)

class BasicKNN():
	def fit(self, X_train, y_train):
		self.X_train = X_train
		self.y_train = y_train

	def predict(self, X_test):
		predictions = []
		for row in X_test:
			label = self.closest(row)
			predictions.append(label)
		return predictions

	def closest(self, row):
		dist = euc(row, self.X_train[0])
		dindex = 0
		for i in range(1, len(self.X_train)):
			d = euc(row, self.X_train[i])
			if d < dist:
				dist = d
				dindex = i
		return self.y_train[dindex]

X = iris.data 
y = iris.target

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .5)

my_classifier = BasicKNN()

my_classifier.fit(X_train, y_train)

predictions = my_classifier.predict(X_test)

from sklearn.metrics import accuracy_score
print (accuracy_score(y_test, predictions))