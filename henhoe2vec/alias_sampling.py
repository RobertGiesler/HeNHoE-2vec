import numpy as np

def alias_setup(probs):
    '''
	Compute utility lists for non-uniform sampling from discrete distributions.
	Refer to https://lips.cs.princeton.edu/the-alias-method-efficient-sampling-with-many-discrete-outcomes/
	for details.
	'''
    K = len(probs)
    q = np.zeros(K)
    J = np.zeros(K, dtype=np.int)

    # Sort the data into the outcomes with probabilities
    # that are larger and smaller than 1/K.
    smaller = []
    larger  = []
    for kk, prob in enumerate(probs):
        q[kk] = K*prob
        if q[kk] < 1.0:
            smaller.append(kk)
        else:
            larger.append(kk)

    # Loop though and create little binary mixtures that
    # appropriately allocate the larger outcomes over the
    # overall uniform mixture.
    while len(smaller) > 0 and len(larger) > 0:
        small = smaller.pop()
        large = larger.pop()

        J[small] = large
        q[large] = q[large] - (1.0 - q[small])

        if q[large] < 1.0:
            smaller.append(large)
        else:
            larger.append(large)

    return J, q


def alias_draw(J, q):
    '''
	Draw a sample from a non-uniform discrete distribution using alias sampling.
	'''
    K = len(J)

    # Draw from the overall uniform mixture.
    kk = int(np.floor(np.random.rand()*K))

    # Draw from the binary mixture, either keeping the
    # small one, or choosing the associated larger one.
    if np.random.rand() < q[kk]:
        return kk
    else:
        return J[kk]