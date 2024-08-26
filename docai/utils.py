import hashlib
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders.blob_loaders import Blob
from langchain_community.document_loaders.parsers.pdf import PyMuPDFParser
from llama_index.core import SimpleDirectoryReader
from loguru import logger
from typing import List, Any
from langchain_core.documents import Document
from io import BytesIO
from pathlib import Path
from fastapi import UploadFile
import nest_asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("../.env")

# Import custom LlamaParse module
from llama_parse import LlamaParse

# Apply nested asyncio patch
nest_asyncio.apply()


def generate_hash_key(data: bytes) -> str:
    """
    Generate a SHA-256 hash for a given data.

    Args:
        data (bytes): Byte data to hash.

    Returns:
        str: The SHA-256 hash value as a hexadecimal string.
    """
    sha512_hash = hashlib.sha256()
    sha512_hash.update(data)
    return sha512_hash.hexdigest()


class BytesIOPyMuPDFLoader(PyMuPDFLoader):
    """
    Load PDF files using PyMuPDF from a BytesIO stream.
    """

    def __init__(
        self,
        pdf_stream: BytesIO,
        *,
        extract_images: bool = False,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the loader with a BytesIO stream.

        Args:
            pdf_stream (BytesIO): Stream containing PDF data.
            extract_images (bool, optional): Whether to extract images. Defaults to False.
            **kwargs: Additional keyword arguments for text extraction.
        """
        try:
            import fitz  # noqa:F401
        except ImportError:
            raise ImportError(
                "`PyMuPDF` package not found, please install it with "
                "`pip install pymupdf`"
            )
        # We don't call the super().__init__ here because we don't have a file_path.
        self.pdf_stream = pdf_stream
        self.extract_images = extract_images
        self.text_kwargs = kwargs

    def load(self, **kwargs: Any) -> List[Document]:
        """
        Load the PDF file from the stream.

        Args:
            **kwargs: Additional runtime arguments.

        Returns:
            List[Document]: List of Document objects parsed from the PDF.
        """
        if kwargs:
            logger.warning(
                f"Received runtime arguments {kwargs}. Passing runtime args to `load`"
                f" is deprecated. Please pass arguments during initialization instead."
            )

        text_kwargs = {**self.text_kwargs, **kwargs}

        # Use 'stream' as a placeholder for file_path since we're working with a stream.
        blob = Blob.from_data(self.pdf_stream, path="stream")

        parser = PyMuPDFParser(
            text_kwargs=text_kwargs, extract_images=self.extract_images
        )

        return parser.parse(blob)


def get_loader(data, filename=None):
    """
    Get the appropriate data loader based on the file type.

    Args:
        data (bytes): Byte data of the file.
        filename (str, optional): Name of the file. Defaults to None.

    Returns:
        BytesIOPyMuPDFLoader: Loader for PDF files.
    """
    if isinstance(data, bytes) and Path(filename).suffix.lower() == ".pdf":
        return BytesIOPyMuPDFLoader(data)


async def llama_parse_process_pdf(file: UploadFile, local_file_upload: bool):
    """
    Process a PDF file using LlamaParse.

    Args:
        file (UploadFile): Uploaded PDF file.

    Returns:
        str: Parsed content of the PDF file in markdown format.
    """

    UPLOAD_DIR = Path("./uploads")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    if local_file_upload:
        file_path = UPLOAD_DIR / file.filename.split("/")[-1]
    else:
        file_path = UPLOAD_DIR / file.filename

    # Save the uploaded file to the uploads directory
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Set up parser
    parser = LlamaParse(result_type="markdown")  # "markdown" and "text" are available

    # Use SimpleDirectoryReader to parse the file
    file_extractor = {".pdf": parser}

    reader = SimpleDirectoryReader(
        input_dir="uploads/", file_extractor=file_extractor
    ).load_data()

    os.remove(file_path)

    return reader[0].text


async def process_pdf(
    file: UploadFile, parser_type: str, local_file_upload: bool = False
):
    """
    Process a PDF file using the specified parser type.

    Args:
        file (UploadFile): Uploaded PDF file.
        parser_type (str): Type of parser to use ("pymupdf" or "llama_parse").

    Returns:
        str: Full content of the parsed PDF.
    """
    if parser_type == "pymupdf":
        file_content_bytes = file.file.read()

        file_name = file.filename
        if Path(file_name).suffix.lower() != ".pdf":
            raise Exception(
                f"Unsupported file format uploaded. Expected .pdf, uploaded {file_name}"
            )

        loader = get_loader(file_content_bytes, file_name)

        docs = loader.load()
        full_content = "\n\n".join(doc.page_content for doc in docs)
        return full_content
    else:
        full_content = await llama_parse_process_pdf(file, local_file_upload)
        return full_content
