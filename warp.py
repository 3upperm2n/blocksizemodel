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
        self.thread_compute_ldst = 0
        self.thread_misc = 0


        # sass hist dictionary
        self.sass_hist = {}

        # global mem
        self.thread_ldg = 0.0
        self.thread_stg = 0.0

        # shared mem
        self.thread_lds= 0.0
        self.thread_sts= 0.0

        # warp compute 
        self.int_clks = 0.0
        self.fp32_clks = 0.0
        self.fp64_clks = 0.0
        self.compute_ldst_clks = 0.0
        self.cmp_clks = 0.0

        # warp memory
        self.ldg_clks = 0
        self.stg_clks = 0
        self.lds_clks = 0
        self.sts_clks = 0
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
        self.thread_compute_ldst = float(df_kern.inst_compute_ld_st) / total_threads
        self.thread_misc = float(df_kern.inst_misc) / total_threads

        # global memory
        self.thread_ldg = float(df_kern.gld_transactions) / total_threads
        self.thread_stg = float(df_kern.gst_transactions) / total_threads

        # shared memory
        self.thread_lds = float(df_kern.shared_load_transactions) / total_threads
        self.thread_sts = float(df_kern.shared_store_transactions) / total_threads




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
        total_int_inst = ceil(self.thread_integer)
        #print('Int inst. number (round up)  = {}'.format(total_int_inst))

        # on maxwell gpu + cuda 8.0
        # imul is 86 , imad is 101, others are 15
        imul_count, imad_count = 0, 0
        for key, value in self.sass_hist.iteritems():
            if 'IMUL' in key: imul_count += 1
            if 'IMAD' in key: imad_count += 1

        self.int_clks = 15 * (total_int_inst - imul_count - imad_count) + \
        86 * imul_count + 101 * imad_count 
                

    def compute_fp32_clocks(self):
        """ compute fp32 instructions clocks per warp"""
        total_fp32_inst = ceil(self.thread_fp_32)
        #print('FP32 inst. number (round up)  = {}'.format(total_fp32_inst))

        # each fp32 SASS is 15 clocks
        self.fp32_clks = total_fp32_inst * 15


    def compute_fp64_clocks(self):
        """ compute fp64 instructions clocks per warp"""
        total_fp64_inst = ceil(self.thread_fp_64)
        #print('FP64 inst. number (round up)  = {}'.format(total_fp64_inst))

        # on maxwell gpu + cuda 8.0
        # imul is 86 , imad is 101, others are 15
        dfma_count = 0
        for key, value in self.sass_hist.iteritems():
            if 'DFMA' in key: dfma_count += 1

        self.fp64_clks = 48 * (total_fp64_inst - dfma_count) + 51 * dfma_count


    def compute_ldst_clocks(self):
        """ compute ld st instructions """
        ### compute load store instructions mostly offseting address
        total_compute_ldst = ceil(self.thread_compute_ldst)

        self.compute_ldst_clks = 15 * total_compute_ldst 


    def cal_cmp_clocks(self):
        """ compute instructions clocks per warp"""
        #
        # integer
        #
        self.compute_int_clocks()
        print('Integer inst. (per warp) \t\t = {} (clocks)'.format(self.int_clks))

        #
        # fp32 
        #
        self.compute_fp32_clocks()
        print('FP32 inst. (per warp) \t\t\t = {} (clocks)'.format(self.fp32_clks))

        #
        # fp64 
        #
        self.compute_fp64_clocks()
        print('FP64 inst. (per warp) \t\t\t = {} (clocks)'.format(self.fp64_clks))

        #
        # compute_ld_st 
        #
        self.compute_ldst_clocks()
        print('Compute load store inst. (per warp) \t = {} (clocks)'.format(self.compute_ldst_clks))


        #
        # sum up
        #
        self.cmp_clks = self.int_clks + self.fp32_clks + self.fp64_clks + self.compute_ldst_clks

        print('=> Compute inst. (per warp) \t\t = {} (clocks)\n'.format(self.cmp_clks))

    def cal_mem_clocks(self):
        """ compute memory instructions clocks per warp"""
        #
        # global mem : load and store
        #
        self.ldg_clks = ceil(self.thread_ldg) * 650.0
        print('LDG (global load) clocks (per warp) \t\t = {}'.format(self.ldg_clks))

        self.stg_clks = ceil(self.thread_stg) * 19.0
        print('STG (global store) clocks (per warp) \t\t = {}'.format(self.stg_clks))

        #
        # shared mem : load and store
        #
        self.lds_clks = ceil(self.thread_lds) * 26.0
        print('LDS (shared memory load) clocks (per warp) \t = {}'.format(self.lds_clks))

        self.sts_clks = ceil(self.thread_sts) * 19.0
        print('STS (shared memory store) clocks (per warp) \t = {}'.format(self.sts_clks))

        # const mem : load

        # texture mem : load

        #
        # Sum total 
        #
        self.mem_clks = self.ldg_clks + self.stg_clks + self.lds_clks + self.sts_clks

        print('=> Memory inst. (per warp) \t\t\t = {} (clocks)\n'.format(self.mem_clks))


    def run(self, df_kern, sass_result):
        """ Run kernel analysis and find out warp execution time"""
        self.read_df_kern(df_kern)

        self.read_sass(sass_result)

        #self.dumpinfo()
        #self.dump_sass_hist()

        self.cal_mem_clocks()

        self.cal_cmp_clocks()

        if self.mem_clks > self.cmp_clks:
            print('Memory Intensive : mem / cmp = {}'.format(self.mem_clks /  self.cmp_clks))
        else:
            print('Compute Intensive : cmp / mem = {}'.format(self.cmp_clks /  self.mem_clks))

