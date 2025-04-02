"""
Module for extracting code and output from Jupyter notebooks.
"""
import nbformat
from langchain.schema import Document


def extract_code_and_output(notebook_path):
    """
    Extract code cells and their outputs from a Jupyter notebook.
    
    Args:
        notebook_path (str): Path to the Jupyter notebook file
        
    Returns:
        list: List of formatted code cell content and outputs
    """
    try:
        # Load the notebook
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        documents = []

        # Iterate through notebook cells
        for cell in notebook.cells:
            if cell.cell_type == "code":
                code_content = "\n".join(cell.source.splitlines())
                output_content = []
                
                if hasattr(cell, 'outputs'):
                    for output in cell.outputs:
                        if "text" in output:
                            output_content.append(output["text"])
                        elif "data" in output and "text/plain" in output["data"]:
                            output_content.append(output["data"]["text/plain"])
                        elif "ename" in output and "evalue" in output:
                            error_msg = f"{output['ename']}: {output['evalue']}"
                            output_content.append(error_msg)

                # Prepare document format
                document_content = f"'code' cell: {repr(code_content)}"
                if output_content:
                    document_content += f"\n with output: {repr(output_content)}"
                else:
                    document_content += "\n with output: []"

                # Add to documents list
                documents.append(document_content)

        return documents

    except Exception as e:
        print(f"Error while processing notebook: {str(e)}")
        return []
