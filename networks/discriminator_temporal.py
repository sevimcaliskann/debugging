import torch.nn as nn
import numpy as np
from .networks import NetworkBase
from .convgru import ConvGRU
import torch
import os


class Flatten(nn.Module):
    def forward(self, x):
        x = x.view(1, x.size()[0], -1)
        return x

class DiscriminatorTemporal(NetworkBase):
    """Discriminator. PatchGAN."""
    def __init__(self, image_size=128, conv_dim=64, repeat_num=6):
        super(DiscriminatorTemporal, self).__init__()
        self._name = 'discriminator_temporal'

        feat_layers = []
        feat_layers.append(nn.Conv3d(3, conv_dim, kernel_size=(3,4,4), stride=(1,2,2), padding=(1,1,1)))
        feat_layers.append(nn.LeakyReLU(0.01, inplace=True))

        curr_dim = conv_dim
        for i in range(1, repeat_num):
            feat_layers.append(nn.Conv3d(curr_dim, curr_dim*2, kernel_size=(3,4,4), stride=(1,2,2), padding=(1,1,1)))
            feat_layers.append(nn.LeakyReLU(0.01, inplace=True))
            #if i <=repeat_num/2:
            #    self.feat_layers.append(nn.Sequential(nn.Conv2d(curr_dim, curr_dim*2, kernel_size=4, stride=2, padding=1), \
            #                                 nn.LeakyReLU(0.01, inplace=True)))
            #else:
            #    self.feat_layers.append(nn.Sequential(nn.Conv2d(2*curr_dim, curr_dim*2, kernel_size=4, stride=2, padding=1), \
            #                                 nn.LeakyReLU(0.01, inplace=True)))

            curr_dim = curr_dim * 2

        k_size = int(image_size / np.power(2, repeat_num))
        #feat_layers.append(Flatten())
        self.main = nn.Sequential(*feat_layers)

        self.adv = nn.Conv2d(curr_dim, 1, kernel_size=(3,3,3), stride=(1,1,1), padding=(1,1,1), bias=False)
        #self.gru = ConvGRU(input_size=curr_dim, hidden_sizes=128, kernel_sizes=3, n_layers=1)
        #self.regress = nn.Conv2d(128, c_dim, kernel_size=k_size, bias=False)




    def forward(self, x, hidden=None):
        h = self.main(x)
        out_real = self.adv(h)

        return out_real.squeeze()

    def load_from_checkpoint(self, save_dir, epoch_label):
        load_filename = 'net_epoch_%s_id_D.pth' % (epoch_label)
        load_path = os.path.join(save_dir, load_filename)
        state_dict = torch.load(load_path, map_location='cuda:0')
        own_state = self.state_dict()
        for name, param in state_dict.items():
            if name not in own_state:
                continue
            own_state[name].copy_(param)