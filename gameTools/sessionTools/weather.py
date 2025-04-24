import os
from typing import Literal, Tuple

import numpy as np
from numpy.typing import DTypeLike

type _fileModes = Literal['r','r+','w+']
type _displayModes = Literal['all','description','gameEffect']
type _PathLike = str | bytes | os.PathLike

class weatherData:
    """
    Provides methods for generating, reading, manipulating, and displaying weather data arrays based on the following values.
        Possible altitude values: [0-4]: 'None', 'Low', 'Moderate', 'High', 'Extreme'
        Possible climate values: [0-4]: 'Cold', 'Cool', 'Temperate', 'Warm', 'Hot'
        Possible season values: [0-3]: 'Spring', 'Summer', 'Autumn', 'Winter'
        Possible wind values: [0-3]: 'None', 'Low', 'Moderate', 'High'
        Possible temperature values: Any int, -40°F - 120°F recommended.
        Possible precipitation values: [0-3]: 'None', 'Low', 'Moderate', 'Heavy'
        Possible fog values: [0-3]: 'None', 'Low', 'Moderate', 'Heavy'
        Possible cloud cover values: [0-3]: 'None', 'Low', 'Moderate', 'Heavy'
    """
    def __init__(self, file: _PathLike, mode: _fileModes = 'r'):
        # Initialize Properties for memmap
        self.file = file
        self.mode = mode
        # Map weather data array to a binary file on disk
        self.memmap(mode = mode, file = file, shape = 8, dtype = np.int8)

    def __str__(self):
        return f"File: {self.file}\tMode: {self.mode}\tWeather Array: {self.arrWeather}"

    def __len__(self):
        return self.arrWeather.shape[0]

    def memmap(self, file: _PathLike, shape: int | Tuple[int,...], dtype: DTypeLike, mode: _fileModes = 'r'):
        """
        Maps a weather data array to a file on memory and makes it accessible as a numpy arrayLike.

        Parameters
        ----------
        file : str | bytes | os.PathLike
            The binary file to be opened.
        shape : int | Tuple[int,...]
            The dimensions of the array to be created.
        dtype : numpy.typing.DtypeLike
            The data type of each element of the array.
        mode : 'r', 'r+', 'w+'
            The mode with which to map the data array.
            Possible Values: 'r': Read only. 'r+': Read/write. 'w+": Overwrite.
            Defaults to 'r'

        Returns
        -------
        None if the weather array was successfully opened or created.
        """
        if os.path.isfile(file):
            self.arrWeather = np.memmap(filename = file, mode = mode, shape = shape, dtype = dtype)
        elif mode in ['r+', 'w+']:
            print(f"File: {file} was not found, creating memory mapped file.")
            self.arrWeather = np.memmap(filename = file, mode = 'w+', shape = shape, dtype = dtype)
        else:
            raise FileNotFoundError(f"File: {file} was not found, and can not be created in {mode} mode.")
        return None
    
    def setWeather(self, altitude : int = None, climate : int = None, season : int = None, wind : int = None, temperature : int = None, precipitation : int = None, fog : int = None, cloudCover : int = None, flush : bool = True):
        """
        Allows manual updating of all weather values in the weather data array if it is not open in read only mode.

        Parameters
        ----------
        altitude : int
            The altitude of the region.
            Possible values: 0: None, 1:, Low, 2: Moderate, 3: High, 4: Extreme
            Defaults to value from current array.
        climate : int
            The climate of the region.
            Possible values: 0: Cold, 1: Cool, 2: Temperate, 3: Warm, 4: Hot
            Defaults to value from current array.
        season : int
            The season of the region.
            Possible values: 0: Spring, 1: Summer, 2: Fall, 3: Winter
            Defaults to value from current array.
        wind : int
            The wind value of the region.
            Possible values: 0: None, 1: Low, 2: Moderate, 3: High
            Defaults to value from current array.
        temperature : int
            The temperature of the region.
            Defaults to value from current array.
        precipitation : int
            The precipitation value of the region.
            Possible values: 0: None, 1: Low, 2: Moderate, 3: Heavy
            Defaults to value from current array.
        fog : int
            The fog value of the region.
            Possible values: 0: None, 1: Low, 2: Moderate, 3: Heavy
            Defaults to value from current array.
        cloudCover : int
            The cloud cover value of the region.
            Possible values: 0: None, 1: Low, 2: Moderate, 3: Heavy
            Defaults to value from current array.
        flush : bool
            If true, flushes changes to the weather array to the memory mapped file.

        Returns
        -------
        None if the weather array was successfully updated.
        """
        if self.mode == 'r':
            raise Exception(f"File: {self.file} is opened in {self.mode} mode and thus cannot be updated.")
        self.arrWeather[:] = [altitude if altitude else self.arrWeather[0],
                              climate if climate else self.arrWeather[1],
                              season if season else self.arrWeather[2],
                              wind if wind else self.arrWeather[3],
                              temperature if temperature else self.arrWeather[4],
                              precipitation if precipitation else self.arrWeather[5],
                              fog if fog else self.arrWeather[6],
                              cloudCover if cloudCover else self.arrWeather[7]]
        if flush == True: self.arrWeather.flush()
        return None

    def randomizeWeather(self, flush : bool = True):
        """
        Randomly progresses all weather values in the weather data array if it is not open in read only mode.

        Parameters
        ----------
        flush : bool
            If true, flushes changes to the weather array to the memory mapped file.

        Returns
        -------
        None if the weather array was successfully updated.
        """
        if self.mode == 'r':
            raise Exception(f"File: {self.file} is opened in {self.mode} mode and thus cannot be updated.")
        self.updateWind(flush = False)
        self.updateTemperature(flush = False)
        self.updatePrecipitation(flush = False)
        self.updateObscurement(flush = False)
        self.updateClouds(flush = False)
        if flush == True: self.arrWeather.flush()
        return None
        
    def updateWind(self, flush : bool = True):
        """
        Updates wind value based on altitude, climate, season, and previous wind values.
    
        Parameters
        ----------
        flush : bool
            If true, flushes changes to the weather array to the memory mapped file.

        Returns
        -------
        None if the weather array was successfully updated.
        """
        if self.mode == 'r':
            raise Exception(f"File: {self.file} is opened in {self.mode} mode and thus cannot be updated.")
        # Generate 2d6 for randomizing wind value, weighted towards returning to no wind
        diceRoll = np.sum(np.random.randint(1,7,2))
        randomization = -2 if diceRoll in [2] \
            else -1 if diceRoll in [3,4,5,6] \
            else 0 if diceRoll in [7,8,9,10] \
            else 1 if diceRoll in [11] \
            else 2
        # Generate random floats to determine if wind value changes for altitude, climate, and season
        windChangeChance = np.random.random(3)
        # Alter wind value by altitude
        altitudeChange = 1 if any([
            self.arrWeather[0] == 4 and windChangeChance[0] <= 0.20,
            self.arrWeather[0] == 3 and windChangeChance[0] <= 0.15,
            self.arrWeather[0] == 2 and windChangeChance[0] <= 0.10,
            self.arrWeather[0] == 1 and windChangeChance[0] <= 0.05
        ]) else 0
        # Alter wind value by climate
        climateChange = -1 if self.arrWeather[1] == 4 and windChangeChance[1] <= 0.20 \
            else -1 if self.arrWeather[1] == 3 and windChangeChance[1] <= 0.15 \
            else 0 if self.arrWeather[1] == 2 \
            else 1 if self.arrWeather[1] == 1 and windChangeChance[1] <= 0.15 \
            else 1 if self.arrWeather[1] == 0 and windChangeChance[1] <= 0.20 \
            else 0
        # Alter wind value by season
        seasonChange = 0 if self.arrWeather[2] == 0 \
            else -1 if self.arrWeather[2] == 1 and windChangeChance[2] <= 0.25 \
            else 1 if self.arrWeather[2] == 2 and windChangeChance[2] <= 0.20 \
            else 1 if self.arrWeather[2] == 3 and windChangeChance[2] <= 0.15 \
            else 0
        # Bound minimum and maximum wind values
        self.arrWeather[3] = min(3,max(0,self.arrWeather[3] + randomization + altitudeChange + climateChange + seasonChange))
        if flush == True: self.arrWeather.flush()
        return None
    
    def updateTemperature(self, flush : bool = True):
        """
        Updates temperature value based on altitude, climate, season, previous temperature, and wind.

        Parameters
        ----------
        flush : bool
            If true, flushes changes to the weather array to the memory mapped file.

        Returns
        -------
        None if the weather array was successfully updated.
        """
        if self.mode == 'r':
            raise Exception(f"File: {self.file} is opened in {self.mode} mode and thus cannot be updated.")
        # Set base temperature depending on climate
        baseTemp = 75 if self.arrWeather[1] == 4 \
            else 65 if self.arrWeather[1] == 3 \
            else 55 if self.arrWeather[1] == 2 \
            else 45 if self.arrWeather[1] == 1 \
            else 35 if self.arrWeather[1] == 0 \
            else 55
        # Apply a modifier based on the altitude
        altitudeFactor = -30 if self.arrWeather[0] == 4 \
            else -20 if self.arrWeather[0] == 3 \
            else -10 if self.arrWeather[0] == 2 \
            else -5 if self.arrWeather[0] == 1 \
            else 0
        # Generate 2d6 and randomize temperature based on it
        diceRoll = np.sum(np.random.randint(1,7,2))
        randomization = -20 if diceRoll == 2 \
            else -15 if diceRoll == 3 \
            else -10 if diceRoll == 4 \
            else -5 if diceRoll == 5 \
            else 0 if diceRoll in [6,7,8] \
            else 5 if diceRoll == 9 \
            else 10 if diceRoll == 10 \
            else 15 if diceRoll == 11 \
            else 20
        # Apply a modifier based on the season
        seasonFactor = 10 if self.arrWeather[2] == 0 \
            else 20 if self.arrWeather[2] == 1 \
            else -5 if self.arrWeather[2] == 2 \
            else -10 if self.arrWeather[2] == 3 \
            else 0
        # Apply a modifier based on wind speed
        windChill = -15 if self.arrWeather[3] == 3 \
            else -10 if self.arrWeather[3] == 2 \
            else -5 if self.arrWeather[3] == 1 \
            else 0
        # Calculate the new temperature based on current conditions
        newTemperature = baseTemp + randomization + altitudeFactor + seasonFactor + windChill
        # Average the new temperature with the previous one so that extreme values return to the mean
        self.arrWeather[4] = int(newTemperature + self.arrWeather[4])**0.5
        if flush == True: self.arrWeather.flush()
        return None
    
    def updatePrecipitation(self, flush : bool = True):
        """
        Updates precipitation value based on altitude, climate, previous precipitation, and season.

        Parameters
        ----------
        flush : bool
            If true, flushes changes to the weather array to the memory mapped file.

        Returns
        -------
        None if the weather array was successfully updated.
        """
        if self.mode == 'r':
            raise Exception(f"File: {self.file} is opened in {self.mode} mode and thus cannot be updated.")
       # Generate 2d6 for randomizing precipitation value, weighted towards returning to no precipitation
        diceRoll = np.sum(np.random.randint(1,7,2))
        randomization = -2 if diceRoll in [2] \
            else -1 if diceRoll in [3,4,5,6] \
            else 0 if diceRoll in [7,8,9,10] \
            else 1 if diceRoll in [11] \
            else 2
        # Generate random floats to determine if precipitation changes based on altitude, climate, and season
        precipChangeChance = np.random.random(3)
        # Alter precipitation value by altitude
        altitudeChange = 1 if any([
            self.arrWeather[0] == 4 and precipChangeChance[0] <= 0.20,
            self.arrWeather[0] == 3 and precipChangeChance[0] <= 0.15,
            self.arrWeather[0] == 2 and precipChangeChance[0] <= 0.10,
            self.arrWeather[0] == 1 and precipChangeChance[0] <= 0.05
        ]) else 0
        # Alter precipitation value by climate
        climateChange = 1 if self.arrWeather[1] == 4 and precipChangeChance[1] <= 0.05 \
            else 1 if self.arrWeather[1] == 3 and precipChangeChance[1] <= 0.05 \
            else 0 if self.arrWeather[1] == 2 \
            else -1 if self.arrWeather[1] == 1 and precipChangeChance[1] <= 0.05 \
            else -1 if self.arrWeather[1] == 0 and precipChangeChance[1] <= 0.05 \
            else 0
        # Alter precipitation value by season
        seasonChange = 1 if self.arrWeather[2] == 0 and precipChangeChance[2] <= 0.05 \
            else -1 if self.arrWeather[2] == 1 and precipChangeChance[2] <= 0.25 \
            else 0 if self.arrWeather[2] == 2 and precipChangeChance[2] <= 0.00 \
            else 1 if self.arrWeather[2] == 3 and precipChangeChance[2] <= 0.10 \
            else 0
        # Bound minimum and maximum precipitation values
        self.arrWeather[5] = min(3,max(0,self.arrWeather[5] + randomization + altitudeChange + climateChange + seasonChange))
        if flush == True: self.arrWeather.flush()
        return None
    
    def updateObscurement(self, flush : bool = True):
        """
        Updates fog value based on altitude, climate, previous fog, season, and wind.

        Parameters
        ----------
        flush : bool
            If true, flushes changes to the weather array to the memory mapped file.

        Returns
        -------
        None if the weather array was successfully updated.
        """
        if self.mode == 'r':
            raise Exception(f"File: {self.file} is opened in {self.mode} mode and thus cannot be updated.")
       # Generate 2d6 for randomizing fog value, weighted towards returning to no fog
        diceRoll = np.sum(np.random.randint(1,7,2))
        randomization = -2 if diceRoll in [2] \
            else -1 if diceRoll in [3,4,5,6] \
            else 0 if diceRoll in [7,8,9,10] \
            else 1 if diceRoll in [11] \
            else 2
        # Generate random floats to determine if fog changes based on altitude, climate, season, and wind
        obscurementChangeChance = np.random.random(4)
        # Alter fog value by altitude
        altitudeChange = -2 if self.arrWeather[0] == 4 \
            else -1 if self.arrWeather[0] == 3 \
            else -1 if self.arrWeather[0] == 2 and obscurementChangeChance[0] <= 0.50 \
            else -1 if self.arrWeather[0] == 1 and obscurementChangeChance[0] <= 0.25 \
            else 0
        # Alter fog value by climate
        climateChange = -1 if self.arrWeather[1] == 4 and obscurementChangeChance[1] <= 0.05 \
            else -1 if self.arrWeather[1] == 3 and obscurementChangeChance[1] <= 0.05 \
            else 0 if self.arrWeather[1] == 2 \
            else 1 if self.arrWeather[1] == 1 and obscurementChangeChance[1] <= 0.05 \
            else 1 if self.arrWeather[1] == 0 and obscurementChangeChance[1] <= 0.05 \
            else 0
        # Alter fog value by season
        seasonChange = 1 if self.arrWeather[2] == 0 and obscurementChangeChance[2] <= 0.05 \
            else -1 if self.arrWeather[2] == 1 and obscurementChangeChance[2] <= 0.25 \
            else 1 if self.arrWeather[2] == 2 and obscurementChangeChance[2] <= 0.15 \
            else 1 if self.arrWeather[2] == 3 and obscurementChangeChance[2] <= 0.10 \
            else 0
        # Alter fog value by wind
        windChange = -2 if self.arrWeather[3] == 3 \
            else -1 if self.arrWeather[3] == 2 and obscurementChangeChance[3] <= 0.50 \
            else -1 if self.arrWeather[3] == 1 and obscurementChangeChance[3] <= 0.25 \
            else 0
        # Bound minimum and maximum fog values
        self.arrWeather[6] = min(3,max(0,self.arrWeather[6] + randomization + altitudeChange + climateChange + seasonChange + windChange))
        if flush == True: self.arrWeather.flush()
        return None
    
    def updateClouds(self, flush : bool = True):
        """
        Updates cloud cover value based on altitude, climate, previous cloud cover, precipitation, and season.

        Parameters
        ----------
        flush : bool
            If true, flushes changes to the weather array to the memory mapped file.

        Returns
        -------
        None if the weather array was successfully updated.
        """
        if self.mode == 'r':
            raise Exception(f"File: {self.file} is opened in {self.mode} mode and thus cannot be updated.")
       # Generate 2d6 for randomizing cloud cover value, weighted towards returning to no clouds
        diceRoll = np.sum(np.random.randint(1,7,2))
        randomization = -2 if diceRoll in [2] \
            else -1 if diceRoll in [3,4,5,6] \
            else 0 if diceRoll in [7,8,9,10] \
            else 1 if diceRoll in [11] \
            else 2
        # Generate random floats to determine if clouds changes based on altitude, climate, season, and weather
        cloudsChangeChance = np.random.random(4)
        # Alter clouds value by altitude
        altitudeChange = 2 if self.arrWeather[0] == 4 \
            else 1 if self.arrWeather[0] == 3 and cloudsChangeChance[0] <= 0.75 \
            else 1 if self.arrWeather[0] == 2 and cloudsChangeChance[0] <= 0.50 \
            else 1 if self.arrWeather[0] == 1 and cloudsChangeChance[0] <= 0.25 \
            else 0
        # Alter clouds value by climate
        climateChange = -1 if self.arrWeather[1] == 4 and cloudsChangeChance[1] <= 0.50 \
            else -1 if self.arrWeather[1] == 3 and cloudsChangeChance[1] <= 0.25 \
            else 0 if self.arrWeather[1] == 2 \
            else 1 if self.arrWeather[1] == 1 and cloudsChangeChance[1] <= 0.10 \
            else 1 if self.arrWeather[1] == 0 and cloudsChangeChance[1] <= 0.25 \
            else 0
        # Alter clouds value by season
        seasonChange = 1 if self.arrWeather[2] == 0 and cloudsChangeChance[2] <= 0.25 \
            else -1 if self.arrWeather[2] == 1 \
            else 1 if self.arrWeather[2] == 2 and cloudsChangeChance[2] <= 0.25 \
            else 1 if self.arrWeather[2] == 3 and cloudsChangeChance[2] <= 0.50 \
            else 0
        # Alter clouds value by precipitation
        precipitationChange = 2 if self.arrWeather[5] == 3 and cloudsChangeChance[3] <= 0.75 \
            else 1 if self.arrWeather[5] == 2 and cloudsChangeChance[3] <= 0.50 \
            else 1 if self.arrWeather[5] == 1 and cloudsChangeChance[3] <= 0.25 \
            else 0
        # Bound minimum and maximum cloud cover values
        self.arrWeather[7] = min(3,max(0,self.arrWeather[7] + randomization + altitudeChange + climateChange + seasonChange + precipitationChange))
        if flush == True: self.arrWeather.flush()
        return None

    def displayWeather(self, displayMode : _displayModes = 'all'):
        """
        Displays description of weather and/or game mechanical effects based on the weather array.

        Parameters
        ----------
        displayMode : 'all', 'description', 'gameEffect'
            The type of display to perform from the weather array values.
            Possible Values: 'all': Both modes are performed. 'description': Print only descriptive texts. 'gameEffect": Print only mechanical effects.
            Defaults to 'all'

        Returns
        -------
        None if weather display was successful.
        """
        # Set default weather flags for all display types
        dustStorm = False
        thunderstorm = False
        precipType = None
        # Determine if a dust storm occurs
        if self.arrWeather[5] == 0:
            if self.arrWeather[1] in [3,4] and \
            self.arrWeather[3] == 3 and \
            np.random.random() <= 0.05:
                dustStorm = True
        else:
            # Determine if a thunderstorm occurs
            if self.arrWeather[5] == 3:
                thunderstormChance = np.random.random()
                if self.arrWeather[2] == 0 and thunderstormChance <= 0.12 or \
                self.arrWeather[2] == 1 and thunderstormChance <= 0.20 or \
                self.arrWeather[2] == 2 and thunderstormChance <= 0.07 or \
                self.arrWeather[2] == 3 and thunderstormChance <= 0.01:
                    thunderstorm = True
            # Determine precipiration type
            altPrecipChances = np.random.random(2)
            if self.arrWeather[4] <= 32 and altPrecipChances[0] <= 0.25: precipType = 'Freezing Rain'
            elif self.arrWeather[4] <= 32: precipType = 'Snow'
            elif 33 <= self.arrWeather[4] <= 38: precipType = 'Sleet'
            elif altPrecipChances[1] <= 0.10: precipType = 'Hail'
            else: precipType = 'Rain'
        # Provide descriptive text for the weather array
        if displayMode in ['all', 'description']:
            # Set display strings from weather array data
            altitudeDisplay = ['None', 'Low', 'Moderate', 'High', 'Extreme'][self.arrWeather[0]]
            climateDisplay = ['Cold', 'Cool', 'Temperate', 'Warm', 'Hot'][self.arrWeather[1]]
            seasonDisplay = ['Spring', 'Summer', 'Autumn', 'Winter'][self.arrWeather[2]]
            windDisplay = ['None', 'Low', 'Moderate', 'High'][self.arrWeather[3]]
            precipitationDisplay = ['None', 'Light', 'Moderate', 'Heavy'][self.arrWeather[5]]
            obscurementDisplay = ['None', 'Light', 'Moderate', 'Heavy'][self.arrWeather[6]]
            cloudCoverDisplay = ['None', 'Light', 'Moderate', 'Heavy'][self.arrWeather[7]]
            # Print the resulting descriptive text
            print(f"Weather was generated for {seasonDisplay} in a {climateDisplay} climate{f' at {altitudeDisplay} altitude' if self.arrWeather[0] != 0 else ''}.")
            if self.arrWeather[4] >= 90: print("Extreme Heat is in effect.")
            elif self.arrWeather[4] <= 32: print("Extreme Cold is in effect.")
            print(f"The High Temperature is {self.arrWeather[4] + 10} and the Low Temperature is {self.arrWeather[4] - 10}.")
            if self.arrWeather[3] != 0: print(f"There are {windDisplay} Winds.")
            if dustStorm == True: print("A dust storm will occur today.")
            elif thunderstorm == True: print(f"A thunderstorm will occur today with {precipitationDisplay} {precipType}.")
            elif self.arrWeather[5] != 0: print(f"{precipitationDisplay} {precipType} will occur today.")
            if self.arrWeather[6] != 0: print(f"There is {obscurementDisplay} Fog.")
            if self.arrWeather[7] != 0: print(f"There is {cloudCoverDisplay} Cloud Cover.")

        # Provide mechanical effects for the weather array
        if displayMode in ['all', 'gameEffect']:
            # Set default values for game effects
            sightPerceptionPenalty = 0
            hearingPerceptionPenalty = 0
            surpriseChance = 1
            encounterDistance = 1
            rangedWeaponAttackPenalty = 0
            travelPaceMult = 1
            # Calculate game effects based on weather conditions
            if dustStorm == True:
                encounterDistance /= 2
                surpriseChance += 1
                sightPerceptionPenalty -=4
                hearingPerceptionPenalty -=4
            if precipType == 'Rain' and self.arrWeather[5] == 3:
                encounterDistance /= 2
                surpriseChance += 1
                sightPerceptionPenalty -=4
                hearingPerceptionPenalty -=4
            if precipType == 'Snow' and self.arrWeather[5] == 3:
                encounterDistance /= 2
                surpriseChance += 1
                sightPerceptionPenalty -=4
                travelPaceMult /= 2
            if precipType == 'Rain' and self.arrWeather[5] == 2:
                sightPerceptionPenalty -=2
                hearingPerceptionPenalty -=2
            if precipType == 'Snow' and self.arrWeather[5] == 2:
                sightPerceptionPenalty -=2
            if self.arrWeather[6] == 3:
                encounterDistance /= 2
                surpriseChance += 1
                sightPerceptionPenalty -=4
                travelPaceMult /= 2
            if self.arrWeather[6] == 2:
                encounterDistance /= 2
                surpriseChance += 1
                sightPerceptionPenalty -=2
            if self.arrWeather[3] == 3:
                hearingPerceptionPenalty -=4
                rangedWeaponAttackPenalty -=2
            # Print the resulting game mechanics text
            print("Travel Effects")
            if self.arrWeather[4] >= 90: print("Characters gain Fatigue equal to 1d4 plus their Encumbrance at the end of each period of Extended Travel. This increases by 1 if the creature is wearing Medium or Heavy Armor or has any Encumbrance.")
            elif self.arrWeather[4] <= 32: print("Characters gain Fatigue equal to 1d4 plus their Encumbrance at the end of each period of Extended Travel.")
            else: print("Characters gain Fatigue equal to their Encumbrance at the end of each period of Extended Travel.")
            if travelPaceMult == 1/2: print(f"The party's Travel Pace is halved.")
            if travelPaceMult == 1/4: print(f"The party's Travel Pace is quartered.")
            if dustStorm: print("Unprotected creatures take 1 Slashing Damage at the end of each hour they spend exposed to the storm.")
            if precipType in ['Hail', 'Sleet'] and self.arrWeather[5] == 3: print(f"Unprotected creatures take 1 Bludgeoning Damage at the end of each hour they spend exposed to the storm.")
            if thunderstorm: print("Each hour there is a 1 / 100 chance of lightning striking near a group of travelers. If lightning strikes near a group of travelers, there is a 1 / 100 chance for a character at random to be struck, or a 1 / 10 chance if that character is wearing Heavy Armor. The struck creature is Dazed for 1 hour and must make a Fortitude Saving Throw. A creature takes 2d12 Lightning Damage on a failed saving throw, or half as much on a success.")
            if self.arrWeather[3] == 3: print("The High Winds count as Difficult Terrain for flying creatures and disperse fog and mists.")
            if precipType == 'Rain' and self.arrWeather[5] == 3: print("Flash floods may occur.")
            if precipType == 'Rain' and self.arrWeather[5] != 0 or self.arrWeather[5] == 3: print("Open flames are extinguished.")
            print("Combat Effects")
            print(f"If a side of a combat is unaware of the other's presence, they have a {surpriseChance} in 6 chance of being Surprised.")
            if sightPerceptionPenalty != 0: print(f"Creatures have a {sightPerceptionPenalty} Penalty to Perception that relies on sight.")
            if hearingPerceptionPenalty != 0: print(f"Creatures have a {hearingPerceptionPenalty} Penalty to Perception that relies on sight.")
            print(f"Enclosed Encounters Occur: 2d10 x {int(encounterDistance * 6)} feet apart\nWide Open Encounters Occur: 4d10 x {int(encounterDistance * 12)} feet apart.")
            if rangedWeaponAttackPenalty != 0: print(f"Creatures have a {rangedWeaponAttackPenalty} Penalty to Ranged Weapon Attacks.")
        return None


if __name__ == "__main__":
    dataTest = weatherData("../../savedData/weather/asiir.dat",'r')
    dataTest.displayWeather()