import torch
import numpy as np
from NetWorkAR import PortfolioModel
from utility import UtilityLoss
from ModelAR import Optimize

x_train_0 = torch.tensor([1])
x_train_1 = torch.tensor([1]).repeat(30)
num_simulations = 20000
x_train_0 = x_train_0.repeat(num_simulations, 1)
x_train_1 = x_train_1.repeat(num_simulations, 1)

P = 30 
alpha = np.tile(np.array([0.015]),30) 
K = 10
A = np.diag([-0.15] * 30)

diagonal_value = 0.0238
non_diagonal_value = 0.0027
cov = np.full((30, 30), non_diagonal_value)
np.fill_diagonal(cov , diagonal_value)

R_neg1 = np.linalg.inv(np.eye(P) - A)@alpha
R_neg1
Rf = 1.03 
M = num_simulations # number of path 
lb =0 
ub = 0.5
save_path = 'model_epoch_10AR.pth'
max_epoch = 10
batch_size = 64
trainer = Optimize(P, cov, K, lb, ub, Rf, batch_size,alpha, A)
trainer.train(x_train_0,x_train_1, max_epoch,save_path)
# batch_size = M
# trainer = Optimize(P, cov, K, lb, ub, Rf, batch_size, alpha, A)
# trainer.test(x_test_0, x_test_1, save_path)
