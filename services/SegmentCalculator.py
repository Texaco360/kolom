import math
from dataclasses import dataclass
from dataTransferObjects.SectionData import  SegmentDTO

class SegmentCalculator:
    _area: float
    _length: float
    _mid_y: float
    _mid_z: float
    _inertia_yy: float
    _inertia_zz: float
    _inertia_yz: float
    _segment: SegmentDTO

    def __init__(self, segment: SegmentDTO) -> None:
        self._area = 0.0
        self._length = 0.0
        self._mid_y = 0.0
        self._mid_z = 0.0
        self._inertia_yy = 0.0
        self._inertia_zz = 0.0
        self._inertia_yz = 0.0
        self._segment = segment
        self.calculate_properties()
    
    def calculate_properties(self) -> None:
        self._calculate_length()
        self._calculate_area()
        self._calculate_midpoints()
        self._calculate_inertia_yy()
        self._calculate_inertia_zz()
        self._calculate_inertia_yz()

    def _calculate_length(self) -> None:
        dy = self._segment.end_pt.y - self._segment.start_pt.y
        dz = self._segment.end_pt.z - self._segment.start_pt.z
        self._length = math.sqrt(dy**2 + dz**2)
    
    def _calculate_area(self) -> None:
        self._area = self._length * self._segment.thickness
    
    def _calculate_midpoints(self) -> None:
        self._mid_y = (self._segment.start_pt.y + self._segment.end_pt.y) / 2
        self._mid_z = (self._segment.start_pt.z + self._segment.end_pt.z) / 2

    def _calculate_inertia_yy(self) -> None:
        inertia_zz_local = self._segment.thickness * (self._segment.end_pt.z - self._segment.start_pt.z)**3 / 12
        self._inertia_yy = inertia_zz_local + self._mid_z**2 * self._area

    def _calculate_inertia_zz(self) -> None:
        inertia_yy_local = self._segment.thickness * (self._segment.end_pt.y - self._segment.start_pt.y)**3 / 12
        self._inertia_zz = inertia_yy_local + self._mid_y**2 * self._area

    def _calculate_inertia_yz(self) -> None:
        self._inertia_yz = self._mid_y * self._mid_z * self._area

    def get_area(self) -> float:
        return self._area
    def get_static_moment_around_y(self) -> float:
        return self._mid_y * self._area
    def get_static_moment_around_z(self) -> float:
        return self._mid_z * self._area
    def get_inertia_yy(self) -> float:
        return self._inertia_yy
    def get_inertia_zz(self) -> float:
        return self._inertia_zz
    def get_inertia_yz(self) -> float:
        return self._inertia_yz
    

