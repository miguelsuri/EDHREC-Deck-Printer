# EDHREC Deck Printer
A web scrapper for people who ofter print MTG cards to speed up the process of copying cards from the internet into a PDF. This is a simple web scrapper for EDHREC that compies a pre-made deck into a PDF for easy printing.
The Repo comes with two example PDFs generated from the following decks:
1) https://edhrec.com/deckpreview/_LcDEBuh8xdSZsOumL0iOg
2) https://edhrec.com/deckpreview/tW_OWzJwFuDlM0AYPrYR3Q

# How to use
Step 1: Clone repository
Step 2: Open command line and navigate to where the repository has been cloned
Step 3: Change directory to the src folder
step 4: run the following comand `python main.py --Url <the url of the EDHREC you want to copy>`

The deck will be saved under the documents > pdfs. The PDF will have the last bit of the URL as the last part of the name. For example, the URL https://edhrec.com/deckpreview/tW_OWzJwFuDlM0AYPrYR3Q will be saved as a PDF with the name "deck-tW_OWzJwFuDlM0AYPrYR3Q.pdf".
The documents > images folder contains all the images of the cards for that deck

### Disclaimer
The code was quickly generated with the help of LLMs as a quick afternoon project for a friend. The code quality is not great but will be improved in the future.