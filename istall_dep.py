from rpy2.robjects.packages import importr

utils = importr('utils')
utils.install_packages('miner')
utils.install_packages('e1071')
utils.install_packages('dplyr')
utils.install_packages('rpart')
utils.install_packages('rpart.plot')
utils.install_packages('tidyr')
utils.install_packages('randomForest')

