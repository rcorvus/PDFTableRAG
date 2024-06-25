# PDFTableRAG
Answers questions about contextual information only found in tables in PDF files

For example, with these complex nested header tables found in the PDF of the National Electrical Code:  
![image](https://github.com/rcorvus/PDFTableRAG/assets/5025458/cb02f88f-28fb-46a8-b31f-c4739b465dcf)

Asking this question:  
"What is the Current limitations of a Inherently Limited Power Source (Overcurrent Protection Not Required) with a source voltage of 10 volts?"  

The AI correctly answers with this information (the answer is correct: 8 amps):  
"The current limitations for an Inherently Limited Power Source with a source voltage of 10 volts are 8.0 amperes."  

Asking this question:  
"What is the Maximum overcurrent protection (amperes) for a Not Inherently Limited Power Source (Overcurrent Protection Required) with a source voltage of 5 volts?"  

The AI correctly answers with this information (the answer is correct: 100/V max):  
"The Maximum overcurrent protection (amperes) for a Not Inherently Limited Power Source (Overcurrent Protection Required) with a source voltage of 5 volts is 100/V, max."  
