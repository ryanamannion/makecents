# MakeCents: A dialogue system for coin collectors

![makecents_logo](MakeCents_logo.png)

<!-- Font for logo is IM Fell English SC from google price_utilities price_utilities.google.com/specimen/IM+Fell+English+SC -->
<!-- Coin graphic from https://etc.usf.edu/clipart/44400/44401/44401_penny.htm -->

MakeCents is a dialogue system designed to help coin collectors quickly query coin prices, and is built using Rasa.

## Installation and Testing Instructions

1. Clone repo and cd into it

2. Create and activate your environment

	* `python3 -m venv venv`
	* `. venv/bin/activate`

3. make `makecents-setup` executable and run with `chmod +x makecents-setup && . makecents-setup`

	* `makecents-setup` handles getting the latest pcgs_scraper release and pip installing all dependencies

4. Run `./makecents-test`, a browser window should open

5. On the left-hand side, navigate to `Talk to your bot`, and start chatting with MakeCents

6. To quit, close the Rasa X tab, go back to the shell, exit with `CTRL+C`
