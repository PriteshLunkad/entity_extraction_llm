from fastapi import FastAPI, APIRouter, HTTPException, status, File, UploadFile, Depends
from langchain_community.callbacks import get_openai_callback
from fastapi.responses import JSONResponse
from .schemas import FileInfo
from .utils import generate_hash_key
import json
from loguru import logger
from .documents import BillOfLading, ParsedDocument, MetaInfo
from .utils import process_pdf
from .llm import get_llm_chain
from base64 import encode
import asyncio

file_route = APIRouter()


@file_route.post("/upload")
def upload_file(file_info: FileInfo = Depends(), file: UploadFile = File(...)):
    """
    Uploads a file and processes it to extract information.

    Args:
        file_info (FileInfo): Metadata and configurations for the file processing.
        file (UploadFile): The file to be uploaded and processed.

    Returns:
        JSONResponse: Contains the task_id and extracted information or an error message.
    """
    try:
        # Generate a unique UUID for the task
        uuid = generate_hash_key(
            f"{json.dumps(file_info.json())}{file.filename}".encode("utf-8")
        )

        # Check if the document is already present in the database
        if BillOfLading.objects(task_id=uuid).first() is None:
            # Process the uploaded PDF file
            contents = asyncio.run(process_pdf(file, file_info.parser_type.value))
            chain = get_llm_chain(llm_model_name=file_info.entity_extractor)

            # Extract information using the language model chain
            with get_openai_callback() as cb:
                response = chain.invoke({"file_contents": contents}).dict()

            # Add additional information to the response
            response["task_id"] = uuid
            response["parsed_content"] = str(contents)
            meta_info = MetaInfo(
                document_name=file.filename,
                doc_parser_model=file_info.parser_type.value,
                entity_extractor_model=file_info.entity_extractor.value,
                total_cost=cb.total_cost,
                total_tokens=cb.total_tokens,
            )
            response["meta_info"] = meta_info.to_mongo().to_dict()

            # Save the extracted information to the database
            BillOfLading(**response).save()
        else:
            response = "Document already present in MongoDB"

        # Return the task_id and extracted information
        return JSONResponse(
            {"task_id": uuid, "extracted_info": response},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException("Some error here", status.HTTP_403_FORBIDDEN)
