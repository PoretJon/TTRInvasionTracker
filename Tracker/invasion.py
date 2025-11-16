class Invasion:

    _cogType = ""
    _district = ""

    _progress = ""

    def __init__(self, cogType, district, progress):
        self._cogType = cogType
        self._cogType = self._cogType.replace(
            chr(3), ""
        )  # remove soft hyphen since its not needed
        self._district = district
        self._progress = progress

    def __eq__(self, other):
        if not isinstance(other, Invasion):
            return False
        return self._cogType == other._cogType and self._district == other._district

    def __hash__(self):
        return hash((self._cogType, self._district))

    def __str__(self):
        return f"**District:** {self._district}\n**Cog Type:** {self._cogType}\n**Progress:** {self._progress}"

    # these probably aren't needed but im going to make and use them anyway
    def getCogType(self):
        return self._cogType
