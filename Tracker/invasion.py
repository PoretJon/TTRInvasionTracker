class Invasion:

    _cogType = ""
    _district = ""

    _progress = ""

    def __init__(self, cogType, district, progress):
        self._cogType = cogType
        self._district = district
        self._progress = progress

    def __eq__(self, other):
        if not isinstance(other, Invasion):
            return False
        return (
            self.getCogType() == other.getCogType()
            and self.getDistrict() == other.getDistrict()
        )

    def __hash__(self):
        return hash((self.getCogType(), self.getDistrict()))

    # these probably aren't needed but im going to make and use them anyway
    def getCogType(self):
        return self._cogType

    def getDistrict(self):
        return self._district

    def printOut(self):
        str = f"**District:** {self._district}\n**Cog Type:** {self._cogType}\n**Progress:** {self._progress}"
        return str
