from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ParserType(str, Enum):
    """
    Enumeration for different types of parsers.
    """

    PyMuPDF = "pymupdf"
    Llama_Parse = "llama_parse"


class EntityExtractorModels(str, Enum):
    """
    Enumeration for different models used for entity extraction.
    """

    GPT_4o = "gpt-4o"
    GPT_4o_MINI = "gpt-4o-mini"
    LLAMA_3_1 = "llama3.1"


class FileInfo(BaseModel):
    """
    Pydantic model for storing file information including parser type and entity extractor model.
    """

    parser_type: Optional[ParserType] = ParserType.PyMuPDF
    entity_extractor: Optional[EntityExtractorModels] = (
        EntityExtractorModels.GPT_4o_MINI
    )
