import modality

def getDip(data):
    """ Extract only the dip value from function modality.diptest.pval_hartigan() """
    xF, yF = modality.diptest.cum_distr(data)
    dip = modality.diptest.dip_from_cdf(xF, yF)
    return dip