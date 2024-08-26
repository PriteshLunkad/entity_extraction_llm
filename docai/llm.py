from typing import List
import os
import sys

from loguru import logger
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
from config.prompts import data_mining_prompt
from config.secrets import GROQ_API_KEY, GROQ_BASE_URL, OPENAI_API_KEY

# Set OpenAI API key from environment variables
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


class PackageDetails(BaseModel):
    """
    Pydantic model for package details in a Bill of Lading.
    """

    description: str = Field(..., description="Description of the package contents")
    quantity: int = Field(..., description="Number of items in the package")
    gross_weight: str = Field(
        ..., description="Gross weight of the package in kilograms"
    )
    seal_number: str = Field(None, description="Seal number of the package")
    container_number: str = Field(
        None, description="Container number housing the package"
    )


class ContactInfo(BaseModel):
    """
    Pydantic model for contact information in a Bill of Lading.
    """

    name: str = Field(description="Name of the contact person or company")
    address: str = Field(description="Street address of the contact")
    city: str = Field(description="City of the contact")
    state: str = Field(description="State or province of the contact")
    postal_code: str = Field(description="Postal or ZIP code of the contact")
    country: str = Field(description="Country of the contact")
    phone: str = Field(description="Phone number of the contact")
    email: str = Field(description="Email address of the contact")
    tax_id: str = Field(description="Tax identification number of the contact")


class BillOfLading(BaseModel):
    """
    Pydantic model for a Bill of Lading, including details about the shipper, consignee, vessel, ports, packages, and metadata.
    """

    shipper: ContactInfo = Field(
        description="Name of the shipper responsible for sending the goods"
    )
    consignee: ContactInfo = Field(
        description="Name of the consignee receiving the goods"
    )
    vessel: str = Field(description="Name of the vessel carrying the goods")
    voyage_number: str = Field(description="Voyage number assigned to the shipment")
    port_of_loading: str = Field(
        description="Port where the goods are loaded onto the vessel"
    )
    port_of_discharge: str = Field(
        description="Port where the goods will be unloaded from the vessel"
    )
    place_of_delivery: str = Field(description="Final delivery location for the goods")
    packages: List[PackageDetails] = Field(
        description="Details of the packages, including quantity and description"
    )
    issue_date: str = Field(description="Date the Bill of Lading was issued")
    bl_number: str = Field(description="Unique Bill of Lading number")
    meta_info: str = Field(description="Additional meta-information about the shipment")


def get_llm_model(model: str) -> BaseModel:
    """
    Returns a language model instance based on the specified model name.

    Args:
        model (str): The name of the model to use.

    Returns:
        BaseModel: The instantiated language model.
    """
    if model in ["gpt-4o", "gpt-4", "gpt-4o-mini"]:
        llm = ChatOpenAI(model=model, temperature=0)
        return llm
    elif model in ["llama3", "llama3.1"]:
        llm = ChatOpenAI(
            base_url=GROQ_BASE_URL,
            model="llama-3.1-70b-versatile",
            temperature=0,
            api_key=GROQ_API_KEY,
        )
        return llm


def get_llm_chain(llm_model_name: str):
    """
    Creates and returns a language model processing chain using the specified model name.

    Args:
        llm_model_name (str): The name of the model to use in the chain.

    Returns:
        Chain: The configured language model processing chain.
    """
    llm_model = get_llm_model(model=llm_model_name)
    parser = PydanticOutputParser(pydantic_object=BillOfLading)

    prompt = PromptTemplate(
        template=data_mining_prompt,
        input_variables=["file_contents"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm_model | parser
    return chain
