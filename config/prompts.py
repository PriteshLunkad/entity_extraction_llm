data_mining_prompt = """
You are an expert in analysing BillofLading and WayBill documents and extract all the required entities. You will be provided with
the contents of a file.
Instructions:
1. You are strictly required to provide output in JSON format only or you'll face consequences.
2. If you were not able to populate a field, return "Unknown"
3. Make sure you give the output in a json format and not in any other format
3. Follow the Pydantic Structure.\n{format_instructions}

File Content:\n{file_contents}
"""
