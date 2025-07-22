"""
This is an example of an analysis-specific schema for the parameters required by that analysis
"""

from typing import List, Optional, Union

from aind_data_schema.base import GenericModel
from pydantic import Field
from pydantic_settings import BaseSettings


class AnalysisSpecification(GenericModel):
    """
    Represents the specification for an analysis, including its name,
    version, libraries to track, and parameters.
    """

    analysis_name: str = Field(..., description="User-defined name for the analysis")
    analysis_tag: str = Field(..., description="User-defined tag to organize results for querying analysis output")
    isi_violations_cutoff: float = Field(
         ..., description="The value to be using when filtering units by this"
    )

class AnalysisOutputs(GenericModel):
    """
    Represents the outputs of an analysis, including a list of ISI violations.
    """

    isi_violations: List[Union[str, int]] = Field(
        ..., description="List of ISI violations detected by the analysis"
    )
    additional_info: Optional[str] = Field(
        default=None, description="Additional information about the analysis"
    )

class AnalysisSpecificationCLI(
    AnalysisSpecification, BaseSettings, cli_parse_args=True
):
    """
    This class is needed only if you want to parse settings passed from the command line (including the app builder)
    """

    pass
