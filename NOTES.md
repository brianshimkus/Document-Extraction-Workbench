## Lesson 1: the page never said the currency

> **What I did.**
>
> I read invoice 1 before I opened the answer key. Northstar Paper, INV-001, 2026-09-01, USD, 125.00. Then I read invoice 2.

> **What broke.**
>
> Invoice 2 has no currency line. The answer key keeps that field `null`. Guessing USD because invoice 1 used dollars would be wrong.

> **What I learned.**
>
> The whole page goes in. Five answers come out as JSON. If the page never gave a fact, the value stays `null`.

## Lesson 2: empty is not zero

> **What I did.**
>
> I built one field for the total `125.00`, then a Lake Office invoice at the Python prompt. Currency was still on the form.

> **What broke.**
>
> Currency's value, quote, and page were all `null`. The field was present. It was empty because the page never named a currency.

> **What I learned.**
>
> `null` means the page never gave that fact. `""` is a blank string, and it is still a value. `0.00` means the page really said zero.

## Lesson 3: the scan is a picture

> **What I did.**
>
> I taught `read_pages` to read a text file as one string and a PDF as one string per page. The Northstar text file and the Northstar PDF both came back readable.

> **What broke.**
>
> Saving the file deleted imports the new function still needed, so the PDF run crashed with `PdfReader` is not defined, then `Path` is not defined. After those imports were back, `invoice-scan.pdf` came back as `['']`.

> **What I learned.**
>
> This reader only sees text stored in the file. A scanned page is a picture. I can read it, and `extract_text()` cannot. A later lesson handles pictures.

## Lesson 4: cleanup is code

> **What I did.**
>
> I taught `normalize` three rules. A date must be a real `YYYY-MM-DD` day. Currency must be `USD`, `EUR`, or `GBP`. A total must be zero or more, with at most two decimal places. Five tests passed. `normalize("total", "125")` returned `125.00`.

> **What broke.**
>
> February 30 is rejected. So are `NaN`, `-1.00`, and `12.345`. `None` stays `None`, so a missing currency is still not guessed.

> **What I learned.**
>
> These rules live in code, not only in a prompt sentence. A credit note would need negative amounts. A customer who uses yen would need different decimal rules.
