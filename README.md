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

## How to measure success?

Since the answer comes back in a conversational sentence, we can do a quick call to ChatGpt to compare the answers given to the correct answer.  

```
Does the Given answer have the same information as the Correct answer?  

Given answer:  The Maximum overcurrent protection (amperes) for a Direct-Current Not Inherently Limited Power Source (Overcurrent Protection Required) with a source voltage of 75 volts is 100/V, max.  
SOURCES: 2017-NEC-Code-2-table11AandB.pdf  

Correct answer: The Maximum overcurrent protection in amperes for a Direct-Current Not Inherently Limited Power Source (requiring Overcurrent Protection) with a source voltage of 75 volts is 100/V, max.  
```

Which correctly evaluates the following:  
```
Yes, the given answer and the correct answer have the same information. They both state the maximum overcurrent protection in amperes for a Direct-Current Not Inherently Limited Power Source with a source voltage of 75 volts, which is 100/V, max.  
```
### Would the ChatGpt evaluator be able to correctly grade an "I don't know" answer?
It can also evaluate a correct "Hmm, I'm not sure" response.  
For example, notice that the system replied with "I don't know" and the evaluator was given "Hmm, I'm not sure" as the correct response, but it still understood that they were the same response:  

What is the capital of France?  
```
I don't know.  
SOURCES: 2017-NEC-Code-2-table11AandB.pdf
```

Does the Given answer have the same information as the Correct answer?  
```
Given answer:  I don't know.  
SOURCES: 2017-NEC-Code-2-table11AandB.pdf  
Correct answer: Hmm, I'm not sure.  
```
```
Yes, both answers convey the same information that the person is unsure or does not know the answer.
```

### What if we got an answer that was incorrect by only one character, would our ChatGpt evaluator catch it?

For example, what if we asked question 1 again but we had gotten answer that was 9.0 instead of the correct 8.0:  
```
What is the Current limitations of an Alternating-Current Inherently Limited Power Source (Overcurrent Protection Not Required) with a source voltage of 10 volts?
```
Incorrect answer:  
```
The current limitation for an Alternating-Current Inherently Limited Power Source with a source voltage of 10 volts is 9.0.
```  

Notice that the ChatGpt evaluator correctly says "No" the given answer is not correct, and correctly states that it expects an 8.0 instead of the 9.0:  
Does the Given answer have the same information as the Correct answer?  
```
Given answer: The current limitation for an Alternating-Current Inherently Limited Power Source with a source voltage of 10 volts is 9.0.
Correct answer: The current limitation for an Alternating-Current Inherently Limited Power Source with a source voltage of 10 volts is 8.0.

No, the given answer states that the current limitation is 9.0, while the correct answer states that it is 8.0. These are two different values and therefore do not have the same information.
```


## How to get the API key  
Currently, all PDF table extractors require a paid API since it take specialized bounding and OCR to find and extract table data from PDFs. This example uses Unstructured which gives you 1000 pages for free, you can create your account to get your API key here: unstructured.io  
