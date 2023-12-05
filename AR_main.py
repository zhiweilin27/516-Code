import torch
import numpy as np
from NetWorkAR import PortfolioModel
from utility import UtilityLoss
from Model import Optimize

x_train_0 = torch.tensor([1])
x_train_1 = torch.tensor([1, 1, 1, 1, 1])
num_simulations = 20000
x_train_0 = x_train_0.repeat(num_simulations, 1)
x_train_1 = x_train_1.repeat(num_simulations, 1)

P = 5 
alpha = np.array([0.015,0.015,0.015,0.015,0.015])
K = 40
A = np.array([[-0.15, 0, 0, 0, 0],
              [0,-0.15,0,0,0],
              [0,0,-0.15,0,0],
              [0,0, 0,-0.15,0],
              [0,0, 0,0,-0.15]])
cov = np.array([[0.0238, 0.0027, 0.0027, 0.0027, 0.0027],
                [0.0027, 0.0238, 0.0027, 0.0027, 0.0027],
                [0.0027, 0.0027, 0.0238, 0.0027, 0.0027],
                [0.0027, 0.0027, 0.0027, 0.0238, 0.0027],
                [0.0027, 0.0027, 0.0027, 0.0027, 0.0238]])
R_neg1 = np.linalg.inv(np.eye(P) - A)@alpha
R_neg1
Rf = 1.03 
M = 20000 # number of path 
lb =0 
ub = 0.5
save_path = 'model_epoch_10AR.pth'
max_epoch = 10
batch_size = 64
trainer = Optimize(P, cov, K, lb, ub, Rf, batch_size, alpha, A)
trainer.train(x_train_0,x_train_1, max_epoch,batch_size,save_path)
x_test = torch.ones((20000))  
batch_size = 20000
trainer = Optimize(P, cov, K, lb, ub, Rf, batch_size, alpha, A)
trainer.test(x_test, save_path)