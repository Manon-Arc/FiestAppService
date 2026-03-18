import numpy as np

def mse(y):
    return np.mean((y - np.mean(y)) ** 2)

def best_split(X, y, feature_idxs):
    best_feature, best_threshold, best_score = None, None, float('inf')
    for feature in feature_idxs:
        values = X[:, feature]
        for val in np.unique(values):
            left = values <= val
            right = values > val
            if len(y[left]) == 0 or len(y[right]) == 0:
                continue
            score = (len(y[left]) * mse(y[left]) + len(y[right]) * mse(y[right])) / len(y)
            if score < best_score:
                best_feature, best_threshold, best_score = feature, val, score
    return best_feature, best_threshold

class DecisionTreeRegressor:
    
    def __init__(self, max_depth=5, min_samples=2, feature_subsample_ratio=1.0):
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.feature_subsample_ratio = feature_subsample_ratio
        self.is_leaf = False
        self.prediction = None
        self.feature = None
        self.threshold = None
        self.left = None
        self.right = None
    
    def fit(self, X, y, depth=0):
        self.n_features = X.shape[1]
        self.feature_idxs = np.random.choice(self.n_features, 
                                           max(1, int(self.n_features * self.feature_subsample_ratio)), 
                                           replace=False)
        
        # Condition d'arrêt : feuille
        if depth >= self.max_depth or len(y) <= self.min_samples:
            self.is_leaf = True
            self.prediction = np.mean(y)
            return
        
        # Chercher la meilleure division
        feature, threshold = best_split(X, y, self.feature_idxs)
        if feature is None:
            self.is_leaf = True
            self.prediction = np.mean(y)
            return
        
        # Sauvegarder les paramètres de division
        self.feature = feature
        self.threshold = threshold
        
        # Créer les masques pour diviser les données
        mask = X[:, feature] <= threshold
        
        # Créer et entraîner les sous-arbres
        self.left = DecisionTreeRegressor(self.max_depth, self.min_samples, self.feature_subsample_ratio)
        self.right = DecisionTreeRegressor(self.max_depth, self.min_samples, self.feature_subsample_ratio)
        self.left.fit(X[mask], y[mask], depth + 1)
        self.right.fit(X[~mask], y[~mask], depth + 1)
    
    def predict_single(self, x):
        if self.is_leaf:
            return self.prediction
        
        if x[self.feature] <= self.threshold:
            return self.left.predict_single(x)
        else:
            return self.right.predict_single(x)
    
    def predict(self, X):
        return np.array([self.predict_single(x) for x in X])

class RandomForestRegressor:
    def __init__(self, n_estimators=5, max_depth=5, min_samples=2, feature_subsample_ratio=0.8):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.feature_subsample_ratio = feature_subsample_ratio
        self.trees = []
    
    def fit(self, X, y):
        self.trees = []
        for _ in range(self.n_estimators):
            # Bootstrap sampling
            idxs = np.random.choice(len(X), len(X), replace=True)
            tree = DecisionTreeRegressor(self.max_depth, self.min_samples, self.feature_subsample_ratio)
            tree.fit(X[idxs], y[idxs])
            self.trees.append(tree)
    
    def predict(self, X):
        preds = np.array([tree.predict(X) for tree in self.trees])
        return np.mean(preds, axis=0)