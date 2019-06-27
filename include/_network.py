import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from tqdm import tqdm

class HopfieldNetwork(object):      
    def train_weights(self, train_data):
        ## print("Start to train weights...")
        num_data = len(train_data)
        self.num_neuron = np.size(train_data[0])

        _train_data = []

        for i in range(num_data):
            _train_data.append(np.reshape(train_data[i],self.num_neuron))
        
        W = np.zeros((self.num_neuron, self.num_neuron))
        I = np.identity(self.num_neuron)

        # By genereal rule (Doesn't work)
        '''
        for i in range(num_data):
            W += np.outer(train_data[i],train_data[i])

        W = W - num_data*I
        '''

        # By Hebb rule
        # initialize weights
        rho = np.sum([np.sum(t) for t in _train_data]) / (num_data*self.num_neuron)
        
        # Hebb rule
        for i in range(num_data):
            t = _train_data[i] - rho
            W += np.outer(t, t)
        
        # Make diagonal element of W into 0
        diagW = np.diag(np.diag(W))
        W = W - diagW
        W /= num_data

        self.W = W 
        self.save_weights()
    
    def predict(self, data, fmt, num_iter=500, threshold=0, asyn=False):
    
        ## print("Start to predict...")
        self.num_iter = num_iter
        self.threshold = threshold
        self.asyn = asyn
        self.num_neuron = np.size(data[0])
        
        # Define predict list
        predicted = []
        _copied_data = []

        # Copy to avoid call by reference 
        copied_data = np.copy(data)
    
        ## For general rule (Doesn't work)
        '''
        _copied_data = (np.reshape(copied_data,self.num_neuron))
        predicted.append(np.sign(np.dot(self.W,_copied_data)))
        predicted[0] = np.reshape(predicted[0],(fmt,fmt))
        '''

        for i in range(len(data)):
            _copied_data.append(np.reshape(copied_data[i],self.num_neuron))
            predicted.append(self._run(_copied_data[i]))
            predicted[i] = np.reshape(predicted[i],(fmt,fmt))

        return predicted

    def _run(self, init_s):
        if self.asyn==False:
            '''
            Synchronous update
            '''
            # Compute initial state energy
            s = init_s

            e = self.energy(s)

            # Iteration
            for i in range(self.num_iter):
                # Update s
                s = np.sign(np.matmul(self.W,s) - self.threshold)

                # Compute new state energy
                e_new = self.energy(s)

                # s is converged
                if e == e_new:
                    return s
                # Update energy
                e = e_new
            return s
    
    
    def energy(self, s):
        return -0.5 * np.matmul(np.matmul(s,self.W),s) + np.sum(s * self.threshold)

    def plot_weights(self):
        plt.figure(figsize=(6, 5))
        w_mat = plt.imshow(self.W, cmap=cm.coolwarm)
        plt.colorbar(w_mat)
        plt.title("Network Weights")
        plt.tight_layout()
        plt.savefig("../img/tmp/weights.png")
        plt.show()

    def save_weights(self):
        np.save("../data/weights.npy",self.W)

    def load_weights(self):
        self.W = np.load("../data/weights.npy")
        return self.W
