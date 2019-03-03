import torch.nn as nn
import numpy as np
from .networks import NetworkBase


class Flatten(nn.Module):
    def forward(self, x):
        return x.view(x.size()[0], -1)

class Discriminator(NetworkBase):
    """Discriminator. PatchGAN."""
    def __init__(self, image_size=128, conv_dim=64, c_dim=5, repeat_num=6):
        super(Discriminator, self).__init__()
        self._name = 'discriminator_wgan'

        layers = []
        layers.append(nn.Conv2d(3, conv_dim, kernel_size=4, stride=2, padding=1))
        layers.append(nn.LeakyReLU(0.01, inplace=True))

        curr_dim = conv_dim
        for i in range(1, repeat_num):
            layers.append(nn.Conv2d(curr_dim, curr_dim*2, kernel_size=4, stride=2, padding=1))
            layers.append(nn.LeakyReLU(0.01, inplace=True))
            curr_dim = curr_dim * 2

        k_size = int(image_size / np.power(2, repeat_num))
        self.main = nn.Sequential(*layers)
        self.conv1 = nn.Conv2d(curr_dim, 1, kernel_size=3, stride=1, padding=1, bias=False)
        self.conv2 = nn.Conv2d(curr_dim, 17, kernel_size=k_size, bias=False)
        self.conv3 = nn.Sequential(Flatten(),
                                   nn.Linear(17, 100),
                                   nn.ReLU(),
                                   nn.Linear(100, 16))
        #self.conv3 = nn.Conv2d(c_dim, 11, kernel_size=3, stride = 1, padding=1, bias=False) # 7 emotions from affectnet

    def forward(self, x):
        h = self.main(x)
        out_real = self.conv1(h)
        out_aux = self.conv2(h)
        out_emo = self.conv3(out_aux.squeeze())
        return out_real.squeeze(), out_aux.squeeze(), out_emo.squeeze()
