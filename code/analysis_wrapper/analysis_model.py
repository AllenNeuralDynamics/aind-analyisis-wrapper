"""
Class that represents the analysis specification model
"""

from typing import List, Optional, Union

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class AnalysisSpecification(BaseModel):
    """
    Represents the specification for an analysis, including its name,
    version, libraries to track, and parameters.

    Attributes
    ----------
    analysis_name : str
        The name of the analysis function that will be run.

    analysis_tag : str
        User defined tag to organize results for querying analysis output.
    
    analysis_parameters: Optional[AnalysisParameters]
        Additional parameters for analysis, specified in the sub model where each parameter is a field in the model
    """

    analysis_name: str = Field(..., title="The analysis function that will be run")
    analysis_tag: str = Field(..., title="User defined tag to organize results for querying analysis output")
    isi_violations_cutoff: float = Field(
         ..., title="The value to be using when filtering units by this"
    )

class AnalysisSpecificationCLI(
    AnalysisSpecification, BaseSettings, cli_parse_args=True
):
    """
    For command line argument parsing
    """

    pass
