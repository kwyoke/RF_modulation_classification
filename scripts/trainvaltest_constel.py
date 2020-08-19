from sklearn.externals import joblib
import numpy as np
from matplotlib import pyplot as plt 

#function to apply colormap to array and return the array in colour form
def arr2img(arr, chnum):
  norm = plt.Normalize(vmin=arr.min(), vmax=arr.max())
  if chnum == 1:
      cmap = plt.cm.gray
      image4d = cmap(norm(arr)) #RGBA
      img = image4d[:,:,0] #All RGBA channels identical
      
  elif chnum == 3:
      cmap = plt.cm.hot #or can choose any other colormap
      image4d = cmap(norm(arr)) #RGBA
      img = image4d[:,:,:3] #ignore A channel
  
  return img

root_path = ''
dataset = 'hard'
data = joblib.load(root_path + 'data/' + dataset + '_trainvaltest.hdf5')

#load data
X_train = data['train']['X']
labels_train = data['train']['labels'] 

X_val = data['val']['X']
labels_val = data['val']['labels'] 

X_test = data['test']['X']
labels_test = data['test']['labels'] 


snrthresh = 4
snrs = labels_train[:,1]
snrs = np.array([int(snr) for snr in snrs])
y = np.array([str(mod) for mod in labels_train[:,0]])
idx = np.where((snrs >= snrthresh) & ((y =='a16QAM') | (y =='a64QAM') | (y=='bQPSK') | (y=='b8PSK')))
X_train = X_train[idx]
labels_train = labels_train[idx]
idx = np.where(labels_train )

snrs = labels_val[:,1]
snrs = np.array([int(snr) for snr in snrs])
y = np.array([str(mod) for mod in labels_val[:,0]])
idx = np.where((snrs >= snrthresh) & ((y =='a16QAM') | (y =='a64QAM')| (y=='bQPSK') | (y=='b8PSK')))
X_val = X_val[idx]
labels_val = labels_val[idx]

snrs = labels_test[:,1]
snrs = np.array([int(snr) for snr in snrs])
y = np.array([str(mod) for mod in labels_test[:,0]])
idx = np.where((snrs >= snrthresh) & ((y =='a16QAM') | (y =='a64QAM')| (y=='bQPSK') | (y=='b8PSK')))
X_test = X_test[idx]
labels_test = labels_test[idx]


nbins = [64] #set the ones you want
ch = [1]
xyrange = 0.05 #0.02 for radioml

for b in nbins:
    for c in ch:
        filename = root_path + 'data/' + dataset + '_QAMPSK_trainvaltest_constel' + str(b) + '_' + str(c) + '.hdf5'
        constel_train = []
        constel_val = []
        constel_test = []

        print(b,c, 'train')
        for i, samp in enumerate(X_train):
            counts, xedges, yedges = np.histogram2d(samp[0], samp[1], bins=b,range = [[-xyrange, xyrange], [-xyrange, xyrange]])
            img = arr2img(counts, c)
            constel_train.append(img)
        constel_train = np.array(constel_train)

        print(b,c, 'val')
        for i, samp in enumerate(X_val):
            counts, xedges, yedges = np.histogram2d(samp[0], samp[1], bins=b,range = [[-xyrange, xyrange], [-xyrange, xyrange]])
            img = arr2img(counts, c)
            constel_val.append(img)
        constel_val = np.array(constel_val)

        print(b,c, 'test')
        for i, samp in enumerate(X_test):
            counts, xedges, yedges = np.histogram2d(samp[0], samp[1], bins=b,range = [[-xyrange, xyrange], [-xyrange, xyrange]])
            img = arr2img(counts, c)
            constel_test.append(img)
        constel_test = np.array(constel_test)

        trainvaltest = {}
        trainvaltest['train'] = {}
        trainvaltest['train']['X'] = constel_train
        trainvaltest['train']['labels'] = labels_train

        trainvaltest['val'] = {}
        trainvaltest['val']['X'] = constel_val
        trainvaltest['val']['labels'] = labels_val

        trainvaltest['test'] = {}
        trainvaltest['test']['X'] = constel_test
        trainvaltest['test']['labels'] = labels_test

        joblib.dump(trainvaltest, filename)