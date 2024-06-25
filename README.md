# PDFTableRAG
Answers questions about contextual information only found in tables in PDF files

For example, with these complex nested header tables found in the PDF of the National Electrical Code:  
![image](https://github.com/rcorvus/PDFTableRAG/assets/5025458/cb02f88f-28fb-46a8-b31f-c4739b465dcf)

Asking this question:  
"What is the Current limitations of an Alternating-Current Inherently Limited Power Source (Overcurrent Protection Not Required) with a source voltage of 10 volts?"  

The AI correctly answers with this information from Table 11 (A) (the answer is correct: 8 amps):  
"The current limitation for an Alternating-Current Inherently Limited Power Source with a source voltage of 10 volts is 8.0 amperes."  

Asking this question:  
What is the Maximum overcurrent protection (amperes) for a Direct-Current Not Inherently Limited Power Source (Overcurrent Protection Required) with a source voltage of 75 volts?"  

The AI correctly answers with this information from Table 11 (B) (the answer is correct: 100/V max):  
"The Maximum overcurrent protection (amperes) for a Direct-Current Not Inherently Limited Power Source (Overcurrent Protection Required) with a source voltage of 75 volts is 100/V, max."  

## How to get the API key  
Currently, all PDF table extractors require a paid API since it take specialized bounding and OCR to find and extract table data from PDFs. This example uses Unstructured which gives you 1000 pages for free, you can create your account to get your API key here: unstructured.io  
