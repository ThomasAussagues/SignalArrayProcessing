import numpy as np
from utils.performance import eval_perf
def run_test():

    image = np.load('test_DAS_image.npy')
    eval_perf(image, np.arange(-5,5,0.01), np.arange(0,5,0.005))
