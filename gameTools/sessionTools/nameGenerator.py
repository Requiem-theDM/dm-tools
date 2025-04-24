from typing import Iterable

import numpy as np
from numpy.typing import NDArray

def generateNames(syllables : Iterable[str], numNames : int = 100, maxSyllables : int = 3, minSyllables : int = 2) -> NDArray[np.str_]:
    """
    Generates an array of the requested numer of names from a list of syllables, with minimum and maximum number of syllables as specified by the user.

    Parameters
    ----------
    syllables : Iterable[str]
        An Iterable containing strings to use as syllables for name generation.
    numNames : int
        Sets the number of names to be generated.
        Defaults to 100
    maxSyllables: int
        Sets the maximum number of syllables a generated name can have.
        Defaults to 3
    minSyllables: int
        Sets the minimum number of syllables a generated name can have.
        Defaults to 2

    Returns
    -------
    NDArray[np.str_]
        A numpy array of the generated names.
    """
    # Randomly chooses a number of syllables equal to maxSyllables * the number of requested names for use in name building
    chosenSyllables = np.random.choice(a = syllables, size = (numNames, maxSyllables), replace = True)
    # Randomly determines the number of syllables in each name, bounded by maxSyllables and minSyllables
    nameLengths= np.random.choice(a = np.arange(minSyllables, maxSyllables+1), size = numNames)
    # Calculate maximum possible string length for returned np array dtype.
    returnDtype = "U" + str(len(max(syllables,key=len))*maxSyllables)
    # Joins syllables to generate the number of requested names, then capitalizes the resulting string and returns all names as a numpy array
    names = np.fromiter((''.join(chosenSyllables[index, :nameLength]).capitalize() for index, nameLength in enumerate(nameLengths)),dtype=returnDtype)
    return names
        

if __name__ == "__main__":
    syllables = [
            "ah", "ak", "as", "ba", "mi", "ha", "re", "ka", "shi", "ri", "na", "vi", "la", "tor", "zan", "fen", "sar", "lon", "tir", "gal",
            "an", "ar", "en", "er", "In", "ir", "on", "or", "un", "ur", "el", "al", "il", "ol", "ul", "mal", "dal", "ral", "val", "sel",
            "har", "mar", "bar", "kar", "nar", "par", "gar", "far", "dar", "sar", "tar", "lar", "var", "zar", "rin", "kin", "lin", "win", "min",
            "ban", "ran", "san", "lan", "man", "dan", "van", "pan", "can", "fan", "han", "jan", "kan", "nan", "tan", "yan", "zan", "hin", "tin",
            "nor", "kor", "bor", "tor", "lor", "vor", "zor", "or", "er", "ar", "an", "en", "in", "on", "un", "shan", "thar", "quin", "gral", "clor",
            "a", "e", "i", "o", "u", "yo"
        ]
    print(*generateNames(syllables,1000,3,2))