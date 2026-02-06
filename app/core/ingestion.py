import pdfplumber
import docx
import io
import logging
from typing import Optional, Dict

# Try importing OCR libraries gracefully
try:
    import fitz  # PyMuPDF
    from rapidocr_onnxruntime import RapidOCR
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("OCR dependencies missing. Install 'pymupdf' and 'rapidocr_onnxruntime'.")

class DocumentIngestor:
    """
    Handles extracting raw text options from uploaded files.
    Includes OCR fallback for scanned PDFs.
    """
    
    @staticmethod
    def extract(file_obj, file_type: str) -> str:
        """
        Main entry point for extraction.
        """
        if file_type == "pdf":
            return DocumentIngestor._extract_pdf(file_obj)
        elif file_type == "docx":
            return DocumentIngestor._extract_docx(file_obj)
        elif file_type == "txt":
            return DocumentIngestor._extract_txt(file_obj)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def _extract_pdf(file_obj) -> str:
        text_content = []
        try:
            with pdfplumber.open(file_obj) as pdf:
                for page in pdf.pages:
                    # extract_text(x_tolerance=1) helps keep words together
                    page_text = page.extract_text(x_tolerance=1) 
                    if page_text:
                        text_content.append(page_text)
            
            full_text = "\n".join(text_content)
            
            # Heuristic: If text is extremely short relative to page count (scanned doc), try OCR
            # < 50 chars per page average?
            is_sparse = len(full_text.strip()) < 100
            
            if is_sparse and OCR_AVAILABLE:
                print("Text sparse, attempting OCR...")
                ocr_text = DocumentIngestor._extract_scanned_pdf(file_obj)
                if len(ocr_text) > len(full_text):
                    return ocr_text
            
            return full_text
            
        except Exception as e:
            # Fallback to OCR if pdfplumber fails entirely
            if OCR_AVAILABLE:
                try:
                    return DocumentIngestor._extract_scanned_pdf(file_obj)
                except Exception as ocr_e:
                    raise RuntimeError(f"Error reading PDF (OCR failed too): {str(e)} | {str(ocr_e)}")
            raise RuntimeError(f"Error reading PDF: {str(e)}")

    @staticmethod
    def _extract_scanned_pdf(file_obj) -> str:
        """
        Extracts text from scanned PDFs using RapidOCR and PyMuPDF.
        """
        extracted_text = []
        try:
            # Initialize OCR Engine
            # Use det_use_cuda=False just in case, straightforward inference
            engine = RapidOCR()
            
            # Reset file pointer to read bytes
            file_obj.seek(0)
            file_bytes = file_obj.read()
            
            # Open with PyMuPDF
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            
            for page in doc:
                # Render page to image (zoom=2 for better quality)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes("png")
                
                # Run OCR
                # result is a list of [coords, text, score]
                result, _ = engine(img_bytes)
                
                if result:
                    page_text = "\n".join([line[1] for line in result])
                    extracted_text.append(page_text)
            
            return "\n".join(extracted_text)
            
        except Exception as e:
            raise RuntimeError(f"OCR Extraction Failed: {str(e)}")

    @staticmethod
    def _extract_docx(file_obj) -> str:
        try:
            doc = docx.Document(file_obj)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise RuntimeError(f"Error reading DOCX: {str(e)}")

    @staticmethod
    def _extract_txt(file_obj) -> str:
        try:
            return file_obj.getvalue().decode("utf-8")
        except Exception as e:
            raise RuntimeError(f"Error reading TXT: {str(e)}")
