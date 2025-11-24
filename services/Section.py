import math
from dataclasses import dataclass
from dataTransferObjects.SectionData import SectionDTO, SegmentDTO, Point, ResultsDTO
from services.SegmentCalculator import SegmentCalculator

class Section:
    #private vars
    _area_sum: float 
    _static_y: float 
    _static_z: float 
    _inertia_yy: float 
    _inertia_zz: float
    _inertia_yz: float
    _p_inertia_ksi: float
    _p_inertia_nu: float
    _centroid: Point
    _sectionData: SectionDTO
    _translated_section: SectionDTO
    _segment_calculator: SegmentCalculator
    _segments: list[SegmentCalculator]

    def __init__(self, sectionData: SectionDTO) -> None:
        self._area_sum = 0.0
        self._static_y = 0.0
        self._static_z = 0.0
        self._inertia_yy = 0.0
        self._inertia_zz = 0.0
        self._inertia_yz = 0.0
        self._centroid = Point(0.0, 0.0)
        self._sectionData = sectionData
        self._segments = []

        for segment in sectionData.segments:
            self._segments.append(SegmentCalculator(segment))
        self._calculate_section()

    def _calculate_section(self) -> None:
        self._calculate_area()
        self._calculate_centroid()
        self._translate_section()
        self._calculate_inertia()
        self._calculate_principal_inertia()

    def get_section_properties(self) -> ResultsDTO:
        return ResultsDTO(
            self._area_sum,
            self._centroid,
            self._inertia_yy,
            self._inertia_zz,
            self._inertia_yz
        )
    
    def _calculate_area(self) -> None:
        for segment in self._segments:
            self._area_sum += segment.get_area()
    
    def _calculate_centroid(self) -> None:
        for segment in self._segments:
            self._static_z += segment.get_static_moment_around_z()
            self._static_y += segment.get_static_moment_around_y()
        
        centroid_y = self._static_y / self._area_sum
        centroid_z = self._static_z / self._area_sum

        self._centroid = Point(centroid_y, centroid_z)

    # translate section to centroidal axes to simplify inertia and 
    # shear centercalculation
    def _translate_section(self) -> None:
        dy = -self._centroid.y
        dz = -self._centroid.z

        if self._centroid.y == 0.0 and self._centroid.z == 0.0:
            self._translated_section = self._sectionData
            return
        
        self._translated_section = SectionDTO()
        self._segments = []
        for segment in self._sectionData.segments:
            start_pt = Point(segment.start_pt.y + dy, segment.start_pt.z + dz)
            end_pt = Point(segment.end_pt.y + dy, segment.end_pt.z + dz)
            translated_segment = SegmentDTO(start_pt, end_pt, segment.thickness)
            self._translated_section.add_segment(translated_segment)
            self._segments.append(SegmentCalculator(translated_segment))
    
    #calculate inertia around centroidal axes and product of inertia
    def _calculate_inertia(self) -> None:
        for segment in self._segments:
           self._inertia_yy += segment.get_inertia_yy()
           self._inertia_zz += segment.get_inertia_zz()
           self._inertia_yz += segment.get_inertia_yz()

    def _calculate_principal_inertia(self) -> None:
        delta = (( self._inertia_yy - self._inertia_zz) ** 2 + 4 * self._inertia_yz ** 2) ** 0.5
        self._p_inertia_ksi = ( self._inertia_yy + self._inertia_zz) / 2 + delta / 2
        self._p_inertia_nu = ( self._inertia_yy + self._inertia_zz) / 2 - delta / 2