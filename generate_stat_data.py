import numpy as np

mu, sigma = 0, 0.1 # mean and standard deviation

distrib_normale = np.random.normal(mu, sigma, 1000)
layers = np.linspace(1, 1000, 1000)
print(list(zip(layers,distrib_normale)))

np.savetxt("test.csv", list(zip(layers,distrib_normale)), delimiter=",", header="layer,mean_ir_pwr")