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

    analysis_version : str
        The version of the analysis to run.

    analysis_libraries : List[str]
        A list of libraries to track that will be used in the analysis.

    analysis_parameters : dict, optional
        A dictionary of user-defined input parameters that the analysis
        function will use. Defaults to an empty dictionary.

    s3_output_bucket: str
        The output bucket to write the results to
    """

    analysis_name: str = Field(..., title="The analysis function that will be run")
    analysis_version: str = Field(..., title="The version of the analysis to run")
    analysis_libraries: List[str] = Field(
        ..., title="The analysis libraries that will be used"
    )
    analysis_parameters: dict = Field(
        default={},
        title="The user defined input parameters that the analysis function will use",
    )
    s3_output_bucket: str = Field(
        ..., title="The output bucket where the results will be written to."
    )


class AnalysisSpecificationCLI(
    AnalysisSpecification, BaseSettings, cli_parse_args=True
):
    """
    For command line argument parsing
    """

    pass
