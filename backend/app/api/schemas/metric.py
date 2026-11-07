"""Metric definition schemas."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

MetricName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=64),
]
MetricUnit = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=32),
]


class MetricRead(BaseModel):
    """A metric definition returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    unit: str
    is_builtin: bool
