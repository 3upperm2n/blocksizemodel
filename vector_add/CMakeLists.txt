# CMakeLists.txt for CUDA
cmake_minimum_required( VERSION 2.8.0 )
find_package(CUDA QUIET REQUIRED)

# nvcc options
set(CUDA_NVCC_FLAGS ${CUDA_NVCC_FLAGS};-O2 
-gencode arch=compute_30,code=sm_30 
-gencode arch=compute_35,code=sm_35 
-gencode arch=compute_50,code=sm_50 
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
cuda_add_executable(
vectorAdd_bs32
vectorAdd_bs32.cu
)
target_link_libraries(
vectorAdd_bs32
-lcudart
) 


cuda_add_executable(
vectorAdd_bs64
vectorAdd_bs64.cu
)
target_link_libraries(
vectorAdd_bs64
-lcudart
) 

cuda_add_executable(
vectorAdd_bs128
vectorAdd_bs128.cu
)
target_link_libraries(
vectorAdd_bs128
-lcudart
) 

cuda_add_executable(
vectorAdd_bs256
vectorAdd_bs256.cu
)
target_link_libraries(
vectorAdd_bs256
-lcudart
) 


cuda_add_executable(
vectorAdd_bs512
vectorAdd_bs512.cu
)
target_link_libraries(
vectorAdd_bs512
-lcudart
) 


cuda_add_executable(
vectorAdd_bs1024
vectorAdd_bs1024.cu
)
target_link_libraries(
vectorAdd_bs1024
-lcudart
) 
