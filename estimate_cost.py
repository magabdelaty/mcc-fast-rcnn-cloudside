__author__ = 'Maged'

# https://azure.microsoft.com/en-gb/pricing/details/virtual-machines/
computeCost = 0.146  # $/hour
# https://azure.microsoft.com/en-us/pricing/details/storage/
storageCost = 0.024  # $/GB
# https://azure.microsoft.com/en-us/pricing/details/data-transfers/
# First 5 GB is free
dataTransferCost = 0.0  # $/GB


def estimateCost(data_transfer_size, compute_time, storage_size):
    """
    data_transfer_size: MB
    compute_time: sec
    storage_size: MB
    """
    cost = 0.0
    cost + dataTransferCost * (data_transfer_size / 1024.0)
    cost += computeCost * (compute_time / 3600.0)
    cost += storageCost * (storage_size / 1024.0)

    return cost