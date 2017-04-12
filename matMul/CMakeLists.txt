# CMakeLists.txt for CUDA
cmake_minimum_required( VERSION 2.8.0 )
find_package(CUDA QUIET REQUIRED)

# nvcc options
set(CUDA_NVCC_FLAGS ${CUDA_NVCC_FLAGS};-O2 
-gencode arch=compute_30,code=sm_30 
-gencode arch=compute_35,code=sm_35 
-gencode arch=compute_50,code=sm_50 
-gencode arch=compute_52,code=sm_52 
)

# indicate include dir
include_directories(
/usr/local/cuda/include
/usr/local/cuda/samples/common/inc
) 

# indicate library dir 
link_directories(
/usr/local/cuda/lib64		
)


# Indicate target & source files to compile
cuda_add_executable(mm4 mm4.cu )
target_link_libraries(mm4 -lcudart) 

cuda_add_executable(mm8 mm8.cu )
target_link_libraries(mm8 -lcudart) 

cuda_add_executable(mm16 mm16.cu )
target_link_libraries(mm16 -lcudart) 

cuda_add_executable(mm32 mm32.cu )
target_link_libraries(mm32 -lcudart) 
