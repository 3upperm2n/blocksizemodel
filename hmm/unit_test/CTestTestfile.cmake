# CMake generated Testfile for 
# Source directory: /home/leiming/git/blocksizemodel/hmm/unit_test
# Build directory: /home/leiming/git/blocksizemodel/hmm/unit_test
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(test_fwd "/home/leiming/git/blocksizemodel/hmm/test_fwd")
add_test(test_backwd "/home/leiming/git/blocksizemodel/hmm/test_backwd")
add_test(test_bw "/home/leiming/git/blocksizemodel/hmm/test_bw")
subdirs(gmock/gmock-1.7.0)
