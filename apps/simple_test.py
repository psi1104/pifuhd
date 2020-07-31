# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.


from .recon import reconWrapper, get_model
import argparse

def get_render_model():
       ckpt_path = './checkpoints/pifuhd.pt'

       cmd = ['--load_netMR_checkpoint_path', ckpt_path]

       return get_model(cmd)

def render_obj(net, data_path):
       ###############################################################################################
       ##                   Setting
       ###############################################################################################
       parser = argparse.ArgumentParser()
       parser.add_argument('-i', '--input_path', type=str, default='./sample_images')
       parser.add_argument('--results_path', type=str, default='./results', help='path to save results ply')
       parser.add_argument('-c', '--ckpt_path', type=str, default='./checkpoints/pifuhd.pt')
       parser.add_argument('-r', '--resolution', type=int, default=256)
       parser.add_argument('--use_rect', action='store_true', help='use rectangle for cropping')
       args = parser.parse_args()
       ###############################################################################################
       ##                   Modify args
       ###############################################################################################

       args.use_rect = True
       args.input_path = data_path
       args.results_path = data_path
       ###############################################################################################
       ##                   Upper PIFu
       ###############################################################################################

       resolution = str(args.resolution)
       results_path = str(args.results_path)

       start_id = -1
       end_id = -1
       cmd = ['--dataroot', args.input_path, '--results_path', results_path, \
              '--loadSize', '1024', '--resolution', resolution, '--load_netMR_checkpoint_path', \
              args.ckpt_path, \
              '--start_id', '%d' % start_id, '--end_id', '%d' % end_id]
       reconWrapper(net, cmd, args.use_rect)

