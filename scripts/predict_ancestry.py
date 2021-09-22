# Victor Borza
# Sep 19, 21
# Predict the ancestry of a sample based on variants


import matplotlib.pyplot as plt
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np


pd.set_option('display.max_colwidth', None)

# Load input data and trim metadata
ancestry_var_df = pd.read_pickle('../ancestry_map_1k_var.pkl')
anc_var_trim_df = ancestry_var_df.drop(columns=['POS','REF','ALT','INFO'])

# Convert variant and ancestry data to numpy arrays of proper shape
anc_labels = anc_var_trim_df.iloc[0].to_numpy()
var_data = anc_var_trim_df.iloc[1:].to_numpy().transpose()
n_samples = len(anc_labels)

#clf = svm.SVC(kernel='linear',gamma=0.001)
clf = RandomForestClassifier(max_depth=None)

X_train, X_test, y_train, y_test = train_test_split(var_data, anc_labels, test_size=0.3, shuffle=True)

clf.fit(X_train, y_train)
test_pred = clf.predict(X_test)

print(f"\n\nClassification report on test set for classifier {clf}:\n"
        f"{metrics.classification_report(y_test,test_pred)}\n")


features_names = ancestry_var_df[['POS','REF','ALT','INFO']].copy()
features_names = features_names.iloc[1:]
features_names['INFO'] = features_names['INFO'].str.replace(r'^(.*?)EAS_AF',r'EAS_AF',regex=True)


#imp_coef = np.abs(np.array(clf.coef_[0]))
imp_coef = np.array(clf.feature_importances_)
features_names['Importance'] = imp_coef
top_imp_ind = np.argpartition(imp_coef, -20)[-20:]

print('\n Top 20 features with most contribution to model:\n')
print(features_names.iloc[top_imp_ind[np.argsort(-1*imp_coef[top_imp_ind])]])
