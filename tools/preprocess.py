import numpy as np


def preprocess_seq(data, index):
    '''
    Given whole seq, return input(z) and target.
    Args:
        data: 3D array; (n_sample, seq_len, n_features)
    '''
    # original seq and shifted seq
    data_org = data[:, :-1, :]  # from 0 to t-1
    data_shifted = data[:, 1:, :]  # from 1 to t

    # indexing
    z = data_org[:, :, index]  # z.shape == (N, seq_len)
    target = data_shifted[:, :, index]  # target.shape == (N, seq_len)

    # reshape
    input = np.expand_dims(z, -1)  # input.shape == (N, seq_len, 1)
    target = np.expand_dims(target, -1)  # target.shape == (N, seq_len, 1)

    return input, target

def preprocess_seq_with_cov(data):
    '''
    Given whole seq, return input(z) and target.
    Args:
        data: 3D array; (n_sample, seq_len, n_features)
    '''
    # original seq and shifted seq
    data_org = data[:, :-1, :]  # from 0 to t-1
    data_shifted = data[:, 1:, :]  # from 1 to t

    # indexing from axis = -1
    z = data_org[:, :, 0:1]  # z.shape == (N, seq_len)
    cov = data_shifted[:, :, 1:]
    target = data_shifted[:, :, 0:1]  # target.shape == (N, seq_len)

    # reshape
    input = np.concatenate((z,cov), -1)

    return input, target


def to_return(array):  # (N, seq_len, 1)
    '''
    Make an array of return defined by log.
    '''
    all_returns = []
    for i in range(array.shape[0]):
        returns = []
        for j in range(array.shape[1] - 1):
            return_ = np.log(array[i, j+1, :] / array[i, j, :])
            returns.append(return_)
        all_returns.append(returns)

    return np.stack(all_returns, axis=0)
            

def cut_seq(data, window_len, stride=1):
    '''Cut seq by given window_len and stride.

    Args:
        data: 3D array; (n_sample, seq_len, n_features)
        window_len: int; window length. Look up to window_len before when predicting the next value.
        stride: int; stride of start of the window
    Example:
    arr = np.arange(9)
    arr = np.expand_dims(arr, axis=(0,2))
    arr_cut = cut_seq(arr, window_len=5, stride=2)
    for i in range(arr_cut.shape[0]):
        print(arr_cut[i].squeeze(-1))

    >>> [0 1 2 3 4]
        [2 3 4 5 6]
        [4 5 6 7 8]
    '''

    new_data = []

    for i in range(data.shape[0]):
        for j in range(data.shape[1]): # for loop will end with if -> break
            if (j*stride + window_len) > data.shape[1]:
                break
            new_data.append(data[i][j*stride : j*stride + window_len])

    return np.stack(new_data, axis=0)
