#!/usr/bin/env bash

python test.py \
--data_dir /srv/glusterfs/csevim/datasets/affectnet \
--training_aus_file /srv/glusterfs/csevim/datasets/affectnet/aus_affectnet.pkl \
--test_aus_file /srv/glusterfs/csevim/datasets/affectnet/aus_affectnet.pkl \
--input_path /home/sevim/Downloads/faces/imgs/face4.jpg \
--output_dir /home/sevim/Downloads/master_thesis_study_documents/code-examples/GANimation/test_outputs \
--checkpoints_dir /home/sevim/Downloads/master_thesis_study_documents/code-examples/ganimation_checkpoints \
--name affwild_per_frame_5frames \
--cond_nc 2 \
--load_epoch -1 \
--frames_cnt 10
#--gpu_ids 2

#--name middle_mask_loss_01_02 \
