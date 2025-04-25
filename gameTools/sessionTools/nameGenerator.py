"""
This module provides a function to generate names from a provided list of syllables.
"""
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

def generateNames(syllables : Iterable[str],
                  numNames : int = 100,
                  minSyllables : int = 2,
                  maxSyllables : int = 3) -> NDArray[np.str_]:
    """
    Generates an array of the requested numer of names from a list of syllables, \
    with minimum and maximum number of syllables as specified by the user.

    Parameters
    ----------
    syllables : Iterable[str]
        An Iterable containing strings to use as syllables for name generation.
    numNames : int
        Sets the number of names to be generated.
        Defaults to 100
    minSyllables: int
        Sets the minimum number of syllables a generated name can have.
        Defaults to 2
    maxSyllables: int
        Sets the maximum number of syllables a generated name can have.
        Defaults to 3

    Returns
    -------
    NDArray[np.str_]
        A numpy array of the generated names.
    """
    # Randomly chooses a number of syllables equal to maxSyllables * the number of requested names
    chosenSyllables = np.random.choice(a = syllables, size = (numNames, maxSyllables))
    # Randomly determines the number of syllables in each name
    nameLengths= np.random.choice(a = np.arange(minSyllables, maxSyllables+1), size = numNames)
    # Calculate maximum possible string length for returned np array dtype
    returnDtype = "U" + str(len(max(syllables,key=len))*maxSyllables)
    # Joins syllables to generate the number of requested names
    # Capitalizes the resulting string and returns all names as a numpy array
    names = np.fromiter((
        ''.join(chosenSyllables[index, :nameLength]).capitalize()
        for index, nameLength in enumerate(nameLengths)),
        dtype=returnDtype)
    return names


if __name__ == "__main__":
    testSyllables = ['a', 'ah', 'ak', 'al', 'an', 'ar', 'as', 'ba', 'ban', 'bar',
                 'bor', 'can', 'clor', 'dal', 'dan', 'dar', 'e', 'el', 'en', 'er',
                 'fan', 'far', 'fen', 'gal', 'gar', 'gral', 'ha', 'han', 'har', 'hin',
                 'i', 'il', 'in', 'ir', 'jan', 'ka', 'kan', 'kar', 'kin', 'kor',
                 'la', 'lan', 'lar', 'lin', 'lon', 'lor', 'mal', 'man', 'mar', 'mi',
                 'min', 'na', 'nan', 'nar', 'nor', 'o', 'ol', 'on', 'or', 'pan',
                 'par', 'quin', 'ral', 'ran', 're', 'ri', 'rin', 'san', 'sar', 'sel',
                 'shan', 'shi', 'tan', 'tar', 'thar', 'tin', 'tir', 'tor', 'u', 'ul',
                 'un', 'ur', 'val', 'van', 'var', 'vi', 'vor', 'win', 'yan', 'yo',
                 'zan', 'zar', 'zor']
    print(*generateNames(testSyllables,1000,2,3))
