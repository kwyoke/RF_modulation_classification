'''
Splits up radioML 2016.10A dataset into train, val, test splits
Saves train-val-test splits in the form of a dictionary of arrays
'''
import numpy as np
from sklearn.externals import joblib

#original dataset to be split
dataset = 'easy'
data = joblib.load('data/matlab_dict_' + dataset + '.hdf5')

#set split points
TEST_PERCENTAGE = 0.2
VAL_PERCENTAGE = 0.13
TRAIN_PERCENTAGE = 0.67


#rename dictionary keys
old2newkey = {}
oldkeys = [ '16QAM', '64QAM', 'QPSK', '8PSK', 'CPFSK', 'GFSK', 'BPSK', 'PAM4']
newkeys = ['a16QAM', 'a64QAM', 'bQPSK', 'b8PSK', 'cCPFSK', 'cGFSK', 'dBPSK', 'd4PAM']
for i in range(8):
  old2newkey[oldkeys[i]] = newkeys[i]


#reformat dict into arrays with new labels
X = []
labels = [] # label each example by a pair (modulation type, snr)
total_examples = 0
for mod_type, snr in data.keys():
    mod_new = old2newkey[mod_type]
    current_matrix = data[(mod_type, snr)]
    for i in range(current_matrix.shape[0]):
      X.append(current_matrix[i])
      labels.append((mod_new, snr)) # mod_type is of type bytes
X = np.array(X)
labels = np.array(labels)

#shuffle and split
np.random.seed(7)
perm_idx = np.random.permutation(labels.shape[0])
X_perm = X[perm_idx]
labels_perm = labels[perm_idx]
split_point1 = int(TRAIN_PERCENTAGE*X_perm.shape[0])
split_point2 = int((TRAIN_PERCENTAGE + VAL_PERCENTAGE)*X_perm.shape[0])
X_train = X_perm[0:split_point1]
X_val = X_perm[split_point1:split_point2]
X_test = X_perm[split_point2:]
labels_train = labels_perm[0:split_point1]
labels_val= labels_perm[split_point1:split_point2]
labels_test = labels_perm[split_point2:]



#init train val test dictionaries to be created
trainvaltest = {}
trainvaltest['train'] = {}
trainvaltest['train']['X'] = X_train
trainvaltest['train']['labels'] = labels_train

trainvaltest['val'] = {}
trainvaltest['val']['X'] = X_val
trainvaltest['val']['labels'] = labels_val

trainvaltest['test'] = {}
trainvaltest['test']['X'] = X_test
trainvaltest['test']['labels'] = labels_test


#save dict
joblib.dump(trainvaltest, 'data/' + dataset + '_trainvaltest.hdf5')