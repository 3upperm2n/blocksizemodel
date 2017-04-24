from __future__ import print_function
from math import *
import operator
import sys

import pandas as pd
import numpy as np

class WarpInst():
    """
    class to analyze warp
    """
    def __init__(self):
        self.inst_per_warp = 0
        self.total_threads = 0
        self.thread_fp_32 = 0
        self.thread_fp_64 = 0
        self.thread_integer = 0
        self.thread_bit_convert = 0
        self.thread_control = 0
        self.thread_compute_ld_st = 0
        self.thread_misc = 0

        self.gld_transactions_per_request = 0
        self.gst_transactions_per_request = 0
        self.gld_gst_ratio = 0

        # sass hist dictionary
        self.sass_hist = {}

        # global mem
        self.thread_gld = 0
        self.thread_gst = 0

        # warp compute 
        self.int_clks = 0
        self.fp32_clks = 0
        self.fp64_clks = 0
        self.cmp_clks = 0

        # warp memory
        self.gld_clks = 0 # gld clocks
        self.gst_clks = 0 # gst clocks
        self.shared_ld_clks = 0 # shared load  clocks
        self.shared_st_clks = 0 # shared store clocks
        self.const_ld_clks  = 0 # const  load  clocks
        self.tex_ld_clks    = 0 # tex    load  clocks
        self.mem_clks = 0

    def compute_all_thread_inst(self):
        """comptue all the instructions per thread"""
        return self.thread_fp_32 + self.thread_fp_64 + \
        self.thread_integer + self.thread_bit_convert + \
        self.thread_control + self.thread_compute_ld_st + self.thread_misc

    def dumpinfo(self):
        """print out the log info"""
        print('\nTotal running threads : {}\n'.format(self.total_threads))

        print('thread_fp_32: {}'.format(self.thread_fp_32))
        print('thread_fp_64: {}'.format(self.thread_fp_64))
        print('thread_integer: {}'.format(self.thread_integer))
        print('thread_bit_convert: {}'.format(self.thread_bit_convert))
        print('thread_control: {}'.format(self.thread_control))
        print('thread_compute_ld_st: {}'.format(self.thread_compute_ld_st))
        print('thread_thread_misc: {}'.format(self.thread_misc))

        print('instructions per thread : {}'.format(str(self.compute_all_thread_inst())))
        print('instructions per warp   : {}'.format(str(self.inst_per_warp)))

        print('gld transaction  / gst transaction = {}\n'.format(str(self.gld_gst_ratio)))


    def dump_sass_hist(self):
        for key, value in self.sass_hist.iteritems():
            print('{} : {}'.format(key, value))


    def read_df_kern(self, df_kern):
        """Read info from kernel dataframe"""
        gridx = float(df_kern.gridx)
        gridy = float(df_kern.gridy)
        gridz = float(df_kern.gridz)
        blkx = float(df_kern.blkx)
        blky = float(df_kern.blky)
        blkz = float(df_kern.blkz)
        total_threads = gridx * gridy * gridz * blkx * blky * blkz
        self.total_threads = total_threads

        # compute the instruction for each warp/thread
        self.inst_per_warp = float(df_kern.inst_per_warp)
        self.thread_fp_32 = float(df_kern.inst_fp_32) / total_threads
        self.thread_fp_64 = float(df_kern.inst_fp_64) / total_threads
        self.thread_integer = float(df_kern.inst_integer) / total_threads
        self.thread_bit_convert = float(df_kern.inst_bit_convert) / total_threads
        self.thread_control = float(df_kern.inst_control) / total_threads
        self.thread_compute_ld_st = float(df_kern.inst_compute_ld_st) / total_threads
        self.thread_misc = float(df_kern.inst_misc) / total_threads

        self.gld_transactions_per_request = float(df_kern.gld_transactions_per_request)
        self.gst_transactions_per_request = float(df_kern.gst_transactions_per_request)
        self.gld_gst_ratio = self.gld_transactions_per_request / self.gst_transactions_per_request

    def read_sass(self, sass_result_file):
        """read sass from result file"""
        data = pd.read_csv(sass_result_file, header=None)
        sass_list = data[0].unique()
        sass_hist = {}
        for inst in sass_list:
            sass_hist[inst] = len(data.loc[data[0] == inst])
        self.sass_hist = sass_hist

    def compute_int_clocks(self):
        """ compute integer sass clocks"""
        #total_int_inst = ceil(self.thread_integer)
        total_int_inst = np.rint(self.thread_integer)
        print('Int inst. number (before)    = {}'.format(self.thread_integer))
        print('Int inst. number (round up)  = {}'.format(total_int_inst))

        # on maxwell gpu + cuda 8.0
        # imul is 86 , imad is 101, others are 15
        imul_count, imad_count = 0, 0
        for key, value in self.sass_hist.iteritems():
            #print('{}'.format(key))
            if 'IMUL' in key: imul_count += 1
            if 'IMAD' in key: imad_count += 1

        self.int_clks = 15 * (total_int_inst - imul_count - imad_count) + \
        86 * imul_count + 101 * imad_count 
                

    def compute_fp32_clocks(self):
        """ compute fp32 instructions clocks per warp"""
        #total_fp32_inst = ceil(self.thread_fp_32)
        total_fp32_inst = np.rint(self.thread_fp_32)
        print('FP32 inst. number (before)    = {}'.format(self.thread_fp_32))
        print('FP32 inst. number (round up)  = {}'.format(total_fp32_inst))

        # each fp32 SASS is 15 clocks
        self.fp32_clks = total_fp32_inst * 15


    def compute_fp64_clocks(self):
        """ compute fp64 instructions clocks per warp"""
        #total_fp64_inst = ceil(self.thread_fp_64)
        total_fp64_inst = np.rint(self.thread_fp_64)
        print('FP64 inst. number (before)    = {}'.format(self.thread_fp_64))
        print('FP64 inst. number (round up)  = {}'.format(total_fp64_inst))

        # on maxwell gpu + cuda 8.0
        # imul is 86 , imad is 101, others are 15
        dfma_count = 0
        for key, value in self.sass_hist.iteritems():
            if 'DFMA' in key: dfma_count += 1

        self.fp64_clks = 48 * (total_fp64_inst - dfma_count) + 51 * dfma_count



    def cal_cmp_clocks(self):
        """ compute instructions clocks per warp"""
        #
        # integer
        #
        self.compute_int_clocks()
        print('Integer inst. (per warp) = {} (clocks)'.format(self.int_clks))

        #
        # fp32 
        #
        self.compute_fp32_clocks()
        print('FP32 inst. (per warp) = {} (clocks)'.format(self.fp32_clks))

        #
        # fp64 
        #
        self.compute_fp64_clocks()
        print('FP64 inst. (per warp) = {} (clocks)'.format(self.fp64_clks))

        #
        # sum up
        #
        self.cmp_clks = self.int_clks + self.fp32_clks + self.fp64_clks

        print('=> Compute inst. (per warp) = {} (clocks)\n'.format(self.cmp_clks))

    def cal_mem_clocks(self):
        """ compute memory instructions clocks per warp"""
        ld_count, st_count = 0, 0
        for key, value in self.sass_hist.iteritems():
            if 'LD' in key: ld_count += 1
            if 'ST' in key: st_count += 1

        print('ld sass = {} , st sass = {}'.format(ld_count, st_count))

        #self.thread_compute_ld_st;
        print('thread_compute_ld_st: {}'.format(self.thread_compute_ld_st))

        #
        # global mem : load and store
        #
        gld_portion = self.gld_gst_ratio / (1 + self.gld_gst_ratio)
        gst_portion = 1 - gld_portion

        if ld_count > 0:
            gld_num = np.rint(self.thread_compute_ld_st) * gld_portion 
            gld_num = np.rint(gld_num)
            print('gld inst num = {}'.format(gld_num))
            self.gld_clks = gld_num * 650
            print('Global load inst. (per warp) = {} (clocks)'.format(self.gld_clks))

        if st_count > 0:
            gst_num = np.rint(self.thread_compute_ld_st) * gst_portion 
            gst_num = np.rint(gst_num)
            print('gst inst num = {}'.format(gst_num))
            self.gst_clks = gst_num * 15
            print('Global store inst. (per warp) = {} (clocks)'.format(self.gst_clks))

        #
        # shared mem : load and store
        #

        #
        # const mem : load
        #

        #
        # texture mem : load
        #

        #
        # Sum total 
        #
        self.mem_clks = self.gld_clks + self.gst_clks + self.shared_ld_clks + \
                self.shared_st_clks + self.const_ld_clks + self.tex_ld_clks

        print('=> Memory inst. (per warp) = {} (clocks)\n'.format(self.mem_clks))


    def run(self, df_kern, sass_result):
        """ Run kernel analysis and find out warp execution time"""
        self.read_df_kern(df_kern)

        self.read_sass(sass_result)

        self.dumpinfo()
        #self.dump_sass_hist()

        self.cal_mem_clocks()

        self.cal_cmp_clocks()



