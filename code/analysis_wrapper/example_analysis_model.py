"""
This is an example of an analysis-specific schema
for the parameters required by that analysis
"""

from typing import List, Optional, Type, TypeVar, Union

from aind_data_schema.base import GenericModel
from pydantic import Field, create_model
from pydantic_settings import BaseSettings

T = TypeVar("T", bound=GenericModel)


def make_optional_model(
    model_cls: Type[T],
) -> GenericModel:  # move to pipeline utils
    """
    creates a partial pydantic model

    Parameters
    ----------
    model_cls: Type[T]
        Generic pydantic class to create partial model from

    Returns
    -------
    GenericModel
        Partial model with all optional fields from model passed in
    """

    return create_model(
        f"Partial{model_cls.__name__}",
        __base__=GenericModel,
        **{
            name: (Optional[field.annotation], None)
            for name, field in model_cls.model_fields.items()
        },
    )


class ExampleAnalysisSpecification(GenericModel):
    """
    Represents the specification for an analysis, including its name,
    version, libraries to track, and parameters.
    """

    analysis_name: str = Field(
        ..., description="User-defined name for the analysis"
    )
    analysis_tag: str = Field(
        ...,
        description=(
            "User-defined tag to organize results "
            "for querying analysis output",
        ),
    )
    isi_violations_cutoff: float = Field(
        ..., description="The value to be using when filtering units by this"
    )


class ExampleAnalysisOutputs(GenericModel):
    """
    Represents the outputs of an analysis, including a list of ISI violations.
    """

    isi_violations: List[Union[str, int]] = Field(
        ..., description="List of ISI violations detected by the analysis"
    )
    additional_info: Optional[str] = Field(
        default=None, description="Additional information about the analysis"
    )


class ExampleAnalysisSpecificationCLI(
    BaseSettings,
    make_optional_model(ExampleAnalysisSpecification),
    cli_parse_args=True,
):
    """
    This class is needed only if you want to
    parse settings passed from the command line (including the app builder)
    """

    pass
