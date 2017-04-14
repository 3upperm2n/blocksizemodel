import pandas as pd
import numpy as np                                                              
from math import *                                                              
import operator                                                                 
import sys

# There are max 17 columns in the output csv                                
TraceCols = ["Start","Duration","Grid X","Grid Y","Grid Z","Block X",        
    "Block Y","Block Z","Registers Per Thread","Static SMem",           
    "Dynamic SMem","Size","Throughput","Device","Context","Stream","Name"]

MetricsCols = ["Device", "Kernel", "Invocations", "Metric Name", "Metric Description",
    "Min", "Max", "Avg"]

#------------------------------------------------------------------------------
#  Read csv trace to dataframe in pandas.                                       
#------------------------------------------------------------------------------ 
def Trace2dataframe(trace_file):                                                
    """                                                                         
    read the trace file into dataframe using pandas                             
    """                                                                         
    
    df_trace = pd.read_csv(trace_file, names=TraceCols, engine='python')         
    
    ows_to_skip = 0                                                            
    # find out the number of rows to skip                                       
    for index, row in df_trace.iterrows():
        if row['Start'] == 'Start':                                             
            rows_to_skip = index                                                
            break                                                               
    # read the input csv again                                                  
    df_trace = pd.read_csv(trace_file, skiprows=rows_to_skip)                   

    return df_trace 


def GetKernel(df_trace):
    df = df_trace.copy(deep=True)
    drop_rows = []
    for rowID in xrange(1, df_trace.shape[0]):
        df_row = df_trace.iloc[[rowID]]
        api_name = df_row['Name'].to_string()
        if "DtoH" in api_name or "HtoD" in api_name:
            drop_rows.append(rowID)
    df.drop(df.index[drop_rows], inplace=True)
    return df


def Metrics2dataframe(metrics_file):
    df_trace = pd.read_csv(metrics_file, names=MetricsCols, engine='python')         
    
    ows_to_skip = 0                                                            
    # find out the number of rows to skip                                       
    for index, row in df_trace.iterrows():
        if row['Device'] == 'Device':                                             
            rows_to_skip = index                                                
            break                                                               
    # read the input csv again                                                  
    df_metrics = pd.read_csv(metrics_file, skiprows=rows_to_skip)

    # drop min , max, Metric Description, Invocations column
    df_metrics.drop('Metric Description', axis=1, inplace=True)
    df_metrics.drop('Min', axis=1, inplace=True)
    df_metrics.drop('Max', axis=1, inplace=True)
    df_metrics.drop('Invocations', axis=1, inplace=True)

    return df_metrics


#------------------------------------------------------------------------------ 
# Use ms for timing                                                             
#------------------------------------------------------------------------------ 
def time_coef_ms(df_trace):                                                     
    rows, cols = df_trace.shape                                                 
                                                                                
    start_unit = df_trace['Start'].iloc[0]                                      
    duration_unit = df_trace['Duration'].iloc[0]                                
                                                                                
    start_coef =  1.0                                                           
    if start_unit == 's':                                                       
        start_coef = 1e3                                                        
    if start_unit == 'us':                                                      
        start_coef = 1e-3                                                       
                                                                                
    duration_coef =  1.0                                                        
    if duration_unit == 's':                                                    
        duration_coef = 1e3                                                     
    if duration_unit == 'us':                                                   
        duration_coef = 1e-3                                                    
                                                                                
    return start_coef, duration_coef

#------------------------------------------------------------------------------ 
# Use bytes for shared memory                                                   
#------------------------------------------------------------------------------ 
def sm_coef_bytes(df_trace):                                                    
    ssm_unit = df_trace['Static SMem'].iloc[0]                                  
    dsm_unit = df_trace['Dynamic SMem'].iloc[0]                                 
                                                                                
    ssm_coef = 1.0                                                              
    if ssm_unit == 'KB':                                                        
        ssm_coef = 1e3                                                          
    if ssm_unit == 'MB':                                                        
        ssm_coef = 1e6                                                          
                                                                                
    dsm_coef = 1.0                                                              
    if dsm_unit == 'KB':                                                        
        dsm_coef = 1e3                                                          
    if dsm_unit == 'MB':                                                        
        dsm_coef = 1e6                                                          
                                                                                
    return ssm_coef, dsm_coef 


def read_row_kernel(df_row, duration_coef, ssm_coef, dsm_coef):
    duration = float(df_row['Duration']) * duration_coef  

    gridx = float(df_row['Grid X'])                                        
    gridy = float(df_row['Grid Y'])                                        
    gridz = float(df_row['Grid Z'])                                        
    blkx = float(df_row['Block X'])                                        
    blky = float(df_row['Block Y'])                                        
    blkz = float(df_row['Block Z'])                                        
    reg = float(df_row['Registers Per Thread'])

    static_sm = float(df_row['Static SMem'])                                
    dynamic_sm = float(df_row['Dynamic SMem'])                              
    smem = static_sm * ssm_coef + dynamic_sm * dsm_coef 

    return duration, gridx, gridy, gridz, blkx, blky, blkz, reg, smem



def GenCurKernInfo(df_trace, df_metrics, target_kern, out_columns):
    """
    """
    duration, gridx, gridy, gridz, blkx, blky, blkz, reg, smem = \
    None,None,None,None,None,None,None,None,None

    start_coef, duration_coef = time_coef_ms(df_trace)
    ssm_coef, dsm_coef = sm_coef_bytes(df_trace)

    target_kern = target_kern.lower()

    #
    # find the target kernel trace 
    # If there the kernel are repeated, it will get the info from the last occurrence
    #print df_trace.shape
    for index, row in df_trace.iterrows():
        # skip the 1st row
        if index > 0:
            kern_name = row.Name.lower()

            if target_kern in kern_name:
                # found kernel 
                duration, gridx, gridy, gridz, blkx, blky, blkz, reg, smem = \
                read_row_kernel(row, duration_coef, ssm_coef, dsm_coef)
            else:
                sys.stderr.write('Kernel not found!')
    #
    # fill in column val
    #
    row_list = []
    for i in range(len(out_columns)):
        colname = out_columns[i]
        if colname == 'kern_name': 
            row_list.append(target_kern)
        elif colname == 'duration_ms': 
            row_list.append(duration)
        elif colname == 'gridx': 
            row_list.append(gridx)
        elif colname == 'gridy': 
            row_list.append(gridy)
        elif colname == 'gridz': 
            row_list.append(gridz)
        elif colname == 'blkx': 
            row_list.append(blkx)
        elif colname == 'blky': 
            row_list.append(blky)
        elif colname == 'blkz': 
            row_list.append(blkz)
        elif colname == 'reg_per_thread': 
            row_list.append(reg)
        elif colname == 'shared_mem': 
            row_list.append(smem)
        else:
            row_list.append(FindColVal(df_metrics, target_kern, colname))

    df_current = pd.DataFrame([row_list], columns=out_columns)
    
    return df_current



def FindColVal(df_metrics, target_kern, colname):
    for index, row in df_metrics.iterrows():
        kern_name = row.Kernel.lower()
        if target_kern in kern_name: # find the right kernel
            if row['Metric Name'] == colname: # right metric names
                return row['Avg']


def init_df_columns(df_metrics):
    out_columns = ['kern_name', 'duration_ms', 
                'gridx', 'gridy', 'gridz',
                'blkx', 'blky', 'blkz',
                'reg_per_thread', 'shared_mem']

    # find the unique metrics
    metric_list = df_metrics["Metric Name"].unique()
    #print metric_list 

    out_columns.extend(metric_list)
    #print out_columns

    return out_columns


def Prep_trace_metrics(trace_file, metrics_file):
    df_trace = Trace2dataframe(trace_file) # read trace file
    df_kernel_trace = GetKernel(df_trace) # read kernel trace
    df_metrics = Metrics2dataframe(metrics_file) # read metrics
    return df_kernel_trace, df_metrics