import torch
import torch.nn as nn
import torch.optim as optim
import time
from NetWorkAR import *
from utility import *

class Optimize(nn.Module):
    def __init__(self, P, cov, K, lb, ub, Rf, batch_size, alpha, A):
        super (Optimize, self).__init__()
        self.batch_size = batch_size
        self.model = PortfolioModel(P, cov, K, lb, ub, Rf, batch_size, alpha, A)
        self.criterion = UtilityLoss()
        self.optimizer = optim.Adam(self.model.parameters())

    def train(self, x_train_0, x_train_1, max_epoch, save_path):
        self.model.train()
        num_samples = x_train_0.shape[0] 
        print(f"num_samples: {num_samples}")
        print(f"self.batch_size: {self.batch_size}")
        num_batches = int(num_samples / self.batch_size)

        print('### Training... ###')
        for epoch in range(1, max_epoch + 1):
            start_time = time.time()
            total_loss = 0.0
            for i in range(num_batches):
                start = i * self.batch_size 
                end = start + self.batch_size 
                x_batch_0 = x_train_0[start:end]
                x_batch_0 = torch.tensor(x_batch_0, dtype=torch.float32)
                x_batch_1 = x_train_1[start:end]
                x_batch_1 = torch.tensor(x_batch_1, dtype=torch.float32)


                output_0, output_1 = self.model(x_batch_0,x_batch_1)
                loss = self.criterion(output_0, gamma=4)
                total_loss += loss.item()
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                print('Batch {:d}/{:d} Loss {:.6f}'.format(i, num_batches, loss), end='\r', flush=True)

            duration = time.time() - start_time
            loss = total_loss / num_batches
            print('Epoch {:d} Loss {:.6f} Duration {:.3f} seconds.'.format(epoch, loss, duration))
            if epoch % 10 == 0:
                torch.save(self.model.state_dict(), save_path.format(epoch))

    def test(self, x_test_0, x_test_1, save_path):
        print('### Testing... ###')
        self.model.eval()
        self.model.load_state_dict(torch.load(save_path))
        with torch.no_grad():
                output = self.model(x_test)
                loss = self.criterion(output, gamma=4)
#                 total_loss += loss.item()
#         test_loss = total_loss / x_test.shape[0]
        print('Test Loss {:.6f}'.format(loss))
